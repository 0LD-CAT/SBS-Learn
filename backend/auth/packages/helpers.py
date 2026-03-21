from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


async def create_access_token(data: dict):
    """Функция для создания JWT-токена

    :param data: данные
    :return:
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Добавляем время истечения
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str):
    """Функция для проверки токена

    :param token: токен сессии
    :return: токен | None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)
