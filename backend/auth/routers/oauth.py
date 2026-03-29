from authlib.integrations.base_client.errors import OAuthError
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ..oauth import oauth
from ..packages.auth import UserAuth
from ..packages.helpers import create_access_token

router = APIRouter(tags=["Authentication"])


@router.get("/google/login")
async def google_login(request: Request):
    """SSO авторизация пользователя через google

    :param request: HTTP-запрос.
    :return: redirect на google_callback
    """

    redirect_uri = request.url_for("google_callback")

    return await oauth.google.authorize_redirect(
        request, redirect_uri, prompt="select_account"
    )


@router.get("/google/callback")
async def google_callback(request: Request, db_session: AsyncSession = Depends(get_db)):
    """Получение токена и данных об пользователе через google

    :param request: HTTP-запрос.
    :param db_session: Экземпляр сессии БД.
    :return: redirect на frontend с данными от пользователя
    """

    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        print(e)
        return RedirectResponse("http://localhost:5173/login")

    user_info = token["userinfo"]

    user = await UserAuth(db_session).get_or_create_oauth_user(
        provider="google",
        provider_id=user_info["sub"],
        email=user_info["email"],
        username=user_info.get("name"),
    )

    token_data = {"sub": str(user.id), "username": user.username, "email": user.email}
    jwt_token = await create_access_token(data=token_data)

    return RedirectResponse(f"http://localhost:5173/oauth-success?token={jwt_token}")


@router.get("/github/login")
async def github_login(request: Request):
    """SSO авторизация пользователя через github

    :param request: HTTP-запрос.
    :return: redirect на github_callback
    """

    redirect_uri = request.url_for("github_callback")

    return await oauth.github.authorize_redirect(request, redirect_uri, login="")


@router.get("/github/callback")
async def github_callback(request: Request, db_session: AsyncSession = Depends(get_db)):
    """Получение токена и данных об пользователе через github

    :param request: HTTP-запрос.
    :param db_session: Экземпляр сессии БД.
    :return: redirect на frontend с данными от пользователя
    """

    try:
        token = await oauth.github.authorize_access_token(request)
    except OAuthError as e:
        print(e)
        return RedirectResponse("http://localhost:5173/login")

    resp = await oauth.github.get("user", token=token)

    profile = resp.json()

    email_resp = await oauth.github.get("user/emails", token=token)
    emails = email_resp.json()
    primary_email = next(e["email"] for e in emails if e["primary"] and e["verified"])

    user = await UserAuth(db_session).get_or_create_oauth_user(
        provider="github",
        provider_id=str(profile["id"]),
        email=primary_email,
        username=profile["login"],
    )

    token_data = {"sub": str(user.id), "username": user.username, "email": user.email}
    jwt_token = await create_access_token(data=token_data)

    return RedirectResponse(f"http://localhost:5173/oauth-success?token={jwt_token}")
