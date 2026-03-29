from authlib.integrations.starlette_client import OAuth

from backend.settings import settings

oauth = OAuth()
# Регистрация провайдеров для sso авторизации через oauth 2.0
oauth.register(
    name="google",
    client_id=settings.OAUTH_GOOGLE_CLIENT_ID,
    client_secret=settings.OAUTH_GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/"
    ".well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="github",
    client_id=settings.OAUTH_GITHUB_CLIENT_ID,
    client_secret=settings.OAUTH_GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)
