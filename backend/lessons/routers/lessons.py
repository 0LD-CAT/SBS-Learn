from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db

from ..packages.lessons import Lessons

router = APIRouter(tags=["Lessons"])


@router.get("/lessons")
async def get_lessons(db_session: AsyncSession = Depends(get_db)):
    """Получение тем уроков из таблицы lessons из БД.

    :param db_session: Экземпляр сессии БД.
    :return: Список тем.
    """

    lessons = await Lessons(db_session).get_lessons()

    return lessons


@router.get("/lessons/{lesson_id}/content")
async def get_lesson_content(
    lesson_id: int,
    left_lang: str,
    right_lang: str,
    db_session: AsyncSession = Depends(get_db)
):
    """Получение контента для темы урока из таблицы lesson_content из БД.

    :param lesson_id: id урока.
    :param left_lang: 1 язык
    :param right_lang: 2 язык
    :param db_session: Экземпляр сессии БД.
    :return: Список тем.
    """

    result = await Lessons(db_session).get_lesson_content(lesson_id, left_lang, right_lang)

    if not result:
        raise HTTPException(status_code=404, detail="Урок не найден!")

    return result
