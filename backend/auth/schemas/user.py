from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class RegisterAttributes(BaseModel):
    """Поля получаемые от пользователя при регистрации"""

    username: str
    email: EmailStr
    password: str

    @model_validator(mode="before")
    def pre_validation(cls, values):
        keys = values.keys()

        if "username" not in keys or not values["username"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Укажите имя пользователя",
            )
        elif "email" not in keys or not values["email"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Укажите почту"
            )
        elif "password" not in keys or not values["password"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Укажите пароль"
            )
        return values

    @field_validator("password")
    def check_password(cls, value):
        value = str(value)

        if len(value) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль должен содержать не менее 6 символов",
            )
        if (
            not any(c.isupper() for c in value)
            or not any(c.islower() for c in value)
            or not any(c.isdigit() for c in value)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пароль должен содержать хотя бы одну заглавную букву, одну строчную букву и одну цифру",
            )
        return value


class LoginAttributes(BaseModel):
    username_or_email: str = Field(..., description="Логин или email")
    password: str
