from typing import Any, Optional

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User as UserTable
from ..packages.helpers import create_access_token, get_password_hash, verify_password
from ..schemas.user import LoginAttributes, RegisterAttributes


class UserAuth:
    """Интерфейс для работы с пользователем.

    Атрибуты:
        * db_session - экземпляр сессии БД

    Методы:
        * login_user() - авторизация пользователя
        * register_user() - регистрация пользователя
        * logout() - завершение сессии пользователя
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    async def register_user(self, attrs: RegisterAttributes) -> bool:
        """Регистрация пользователя

        :param attrs: атрибуты пользователя при регистрации
        :return: True | False
        """

        result = await self.db_session.execute(
            select(UserTable).where(
                (UserTable.username == attrs.username)
                | (UserTable.email == attrs.email)
            )
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
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

    def is_email(self, value: str) -> bool:
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

        token_data = {"sub": user.username}
        access_token = await create_access_token(data=token_data)
        return {"access_token": access_token, "token_type": "bearer"}
