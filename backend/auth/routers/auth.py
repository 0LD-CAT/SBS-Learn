from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ..packages.auth import UserAuth
from ..schemas.user import LoginAttributes, RegisterAttributes

router = APIRouter(tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register")
async def register(
    attrs: RegisterAttributes,
    db_session: AsyncSession = Depends(get_db),
):
    """Регистрация пользователя

    :param attrs: логин/username, почта и пароль для пользователя
    :param db_session: Экземпляр сессии БД.
    :return: {"User registered!": True | False}
    """

    result = await UserAuth(db_session).register_user(attrs)

    return {"User registered": result}


@router.post("/login")
async def login(attrs: LoginAttributes, db_session: AsyncSession = Depends(get_db)):
    """

    :param attrs: логин/email и пароль пользователя
    :param db_session: Экземпляр сессии БД.
    :return: {"access_token": access_token пользователя, "token_type": "bearer"}
    """

    result = await UserAuth(db_session).login_user(attrs)

    return {"result": result}


@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_db),
):
    """Обработка запроса на завершение сессии пользователя web-приложения.

    :param token: Идентификатор сессии.
    :param db_session: Экземпляр сессии БД.
    :return: Результат, словарь.
    """

    result = await UserAuth(db_session).logout_user(token)

    return result
