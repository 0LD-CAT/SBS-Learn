from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...lessons.packages.languages import Languages
from ...lessons.packages.lessons import Lessons
from ...lessons.schemas.languages import LanguagesPair
from ..packages.helpers import decode_token
from ...lessons.packages.progress import UserProgress

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/protected/", tags=["Authentication"])
async def protected_route(
    token: str = Depends(oauth2_scheme), db_session: AsyncSession = Depends(get_db)
):
    """Получение данных об пользователе через jwt token

    :param token: jwt токен.
    :param db_session: Экземпляр сессии БД.
    :return: словарь с данными пользователя.
    """
    print(token)
    payload = await decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401, detail="Неверный токен или срок действия истёк"
        )

    pair = await Languages(db_session).get_languages_pairs(int(payload["sub"]))

    return {
        "user": {
            "id": int(payload["sub"]),
            "username": payload["username"],
            "email": payload["email"],
            "language_pair": pair,
        }
    }


@router.post("/select-languages-pair", tags=["Languages"])
async def select_languages_pair(
    attrs: LanguagesPair,
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_db),
):
    """Добавление пары ЯП для изучения.

    :param attrs: схема LanguagesPair (id ЯП)
    :param token: jwt токен.
    :param db_session: Экземпляр сессии БД.
    :return:
    """

    payload = await decode_token(token)

    if not payload:
        raise HTTPException(401, "Неверный токен!")

    pair = await Languages(db_session).select_languages_pair(
        user_id=int(payload["sub"]), lang1_id=attrs.lang1_id, lang2_id=attrs.lang2_id
    )

    _ = await UserProgress(db_session).initialize_progress(int(payload["sub"]), pair.id)

    return {"msg": "Пара ЯП выбрана, прогресс инициализирован", "pair_slug": pair.slug}


@router.get("/lessons/user", tags=["Lessons"])
async def get_user_lessons(token: str = Depends(oauth2_scheme), db_session: AsyncSession = Depends(get_db)):
    """Получение прогресса уроков для пользователя.

    :param token: jwt токен.
    :param db_session: Экземпляр сессии БД.
    :return: Список тем.
    """

    payload = await decode_token(token)

    if not payload:
        raise HTTPException(401, "Неверный токен!")

    user_id = int(payload["sub"])

    lessons = await UserProgress(db_session).get_user_lessons_progress(user_id=user_id)

    return {"lessons": lessons}

@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    db_session: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Обновление прогресса уроков для пользователя.

    :param lesson_id: id урока
    :param token: jwt токен.
    :param db_session: Экземпляр сессии БД.
    :return: Список тем.
    """

    payload = await decode_token(token)

    if not payload:
        raise HTTPException(401, "Неверный токен!")

    user_id = int(payload["sub"])

    result = await UserProgress(db_session).update_user_lessons_progress(
        user_id=user_id,
        lesson_id=lesson_id
    )

    return {"result": result}


@router.get("/lessons/progress", tags=["Lessons"])
async def get_progress(
    token: str = Depends(oauth2_scheme),
    db_session: AsyncSession = Depends(get_db)
):
    """Получение % прогресса изучения пар ЯП для пользователя.

    :param token: jwt токен.
    :param db_session: Экземпляр сессии БД.
    :return: % выполнения для пользователя.
    """

    payload = await decode_token(token)

    if not payload:
        raise HTTPException(401, "Неверный токен!")

    user_id = int(payload["sub"])

    progress = await Lessons(db_session).get_progress_by_language_pairs(user_id)

    return {"user_id": user_id, "progress": progress}
