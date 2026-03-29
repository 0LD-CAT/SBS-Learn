from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SESSION_SECRET: str

    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_CLIENT_SECRET: str
    OAUTH_GITHUB_CLIENT_ID: str
    OAUTH_GITHUB_CLIENT_SECRET: str

    @property
    def DATABASE_URL_asyncpg(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def DATABASE_URL_psycopg(self):
        return (
            f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8"
    )


settings = Settings()
