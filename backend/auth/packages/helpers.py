from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.settings import settings


async def create_access_token(data: dict):
    """Функция для создания JWT-токена

    :param data: данные
    :return: access_token
    """

    to_encode = data.copy()
    time_now = datetime.now(timezone.utc)
    expire = time_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(iat=time_now, exp=expire)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def decode_token(token: str):
    """Функция для проверки токена

    :param token: токен сессии
    :return: токен | None
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None  # Если токен недействителен или истёк


# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password):
    """Функция для хеширования пароля

    :param password: пароль пользователя
    :return: хэшированный пароль
    """

    return pwd_context.hash(password)


async def verify_password(plain_password, hashed_password):
    """Функция для проверки пароля

    :param plain_password: полученный пароль
    :param hashed_password: хэшированный пароль
    :return: True | False
    """

    return pwd_context.verify(plain_password, hashed_password)
