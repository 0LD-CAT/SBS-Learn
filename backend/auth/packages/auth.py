from typing import Any, Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User as UserTable
from ..packages.helpers import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
)
from ..schemas.user import LoginAttributes, RegisterAttributes


class UserAuth:
    """Интерфейс для работы с пользователем.

    Атрибуты:
        * db_session - экземпляр сессии БД

    Методы:
        * login_user() - авторизация пользователя
        * register_user() - регистрация пользователя
        * logout_user() - завершение сессии пользователя
        * get_or_create_oauth_user() - получение или создание
          пользователя при sso авторизации
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    async def register_user(self, attrs: RegisterAttributes) -> bool:
        """Регистрация пользователя

        :param attrs: атрибуты пользователя при регистрации
        :return: True | False
        """

        result = await self.db_session.execute(
            select(UserTable).where(UserTable.email == attrs.email)
        )

        existing_user = result.scalar_one_or_none()
        if existing_user:
            # Проверка для SSO авторизации
            if existing_user.hashed_password is None:
                hashed_password = await get_password_hash(attrs.password)

                existing_user.hashed_password = hashed_password

                if not existing_user.username:
                    existing_user.username = attrs.username

                await self.db_session.commit()

                return True

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь уже зарегистрирован!",
            )

        hashed_password = await get_password_hash(attrs.password)
        new_user = UserTable(
            username=attrs.username, email=attrs.email, hashed_password=hashed_password
        )

        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)

        return True if new_user is not None else False

    @staticmethod
    def is_email(value: str) -> bool:
        email_adapter = TypeAdapter(EmailStr)

        try:
            email_adapter.validate_python(value)
            return True
        except ValidationError:
            return False

    async def login_user(self, attrs: LoginAttributes) -> dict[str, Any]:
        """Авторизация пользователя.

        :param attrs: атрибуты пользователя при авторизации
        :return: {"access_token": access_token, "token_type": "bearer"}
        """

        if self.is_email(attrs.username_or_email):
            stmt = select(UserTable).where(UserTable.email == attrs.username_or_email)
        else:
            stmt = select(UserTable).where(
                UserTable.username == attrs.username_or_email
            )

        result = await self.db_session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not await verify_password(attrs.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        user.is_active = True
        await self.db_session.commit()

        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
        }
        access_token = await create_access_token(data=token_data)
        return {"access_token": access_token, "token_type": "Bearer"}

    async def logout_user(self, token: str) -> dict[str, bool]:
        """Завершение сессии пользователя.

        :param token: Идентификатор сессии.
        :return: Результат, словарь.
        """

        payload = await decode_token(token)

        if payload is None:
            raise HTTPException(
                status_code=401, detail="Неверный токен или срок действия истёк"
            )

        user_id = int(payload["sub"])

        user = await self.db_session.get(UserTable, user_id)

        if user:
            user.is_active = False
            await self.db_session.commit()

        return {"logout": True}

    async def get_or_create_oauth_user(
        self, provider: str, provider_id: str, email: str, username: str | None = None
    ):

        provider_field = f"{provider}_id"

        stmt = select(UserTable).where(
            getattr(UserTable, provider_field) == provider_id
        )
        result = await self.db_session.execute(stmt)

        user = result.scalar_one_or_none()

        if user:
            user.is_active = True
            await self.db_session.commit()

            return user

        stmt = select(UserTable).where(UserTable.email == email)
        result = await self.db_session.execute(stmt)

        user = result.scalar_one_or_none()

        if user:
            setattr(user, provider_field, provider_id)
            user.is_active = True
            await self.db_session.commit()

            return user

        user = UserTable(
            email=email,
            username=username or email.split("@")[0],
            **{provider_field: provider_id},
        )

        self.db_session.add(user)
        user.is_active = True
        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user
