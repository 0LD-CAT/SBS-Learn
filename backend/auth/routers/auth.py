from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ..packages.auth import UserAuth
from ..schemas.user import LoginAttributes, RegisterAttributes

router = APIRouter(tags=["authentication"])


@router.post("/register")
async def register(
    login: str,
    email: EmailStr,
    password: str,
    db_session: AsyncSession = Depends(get_db),
):
    """Регистрация пользователя

    :param login: логин/username пользователя
    :param email: почта пользователя
    :param password: пароль пользователя
    :param db_session: Экземпляр сессии БД.
    :return: {"User registered!": True | False}
    """

    attrs = RegisterAttributes(username=login, email=email, password=password)
    result = await UserAuth(db_session).register_user(attrs)

    return {"User registered": result}


@router.post("/login")
async def login(
    login_or_email: str, password: str, db_session: AsyncSession = Depends(get_db)
):
    """

    :param login_or_email: логин/email пользователя
    :param password: пароль пользователя
    :param db_session: Экземпляр сессии БД.
    :return: {"access_token": access_token пользователя, "token_type": "bearer"}
    """
    user = LoginAttributes(username_or_email=login_or_email, password=password)
    result = await UserAuth(db_session).login_user(user)

    return {"result": result}
