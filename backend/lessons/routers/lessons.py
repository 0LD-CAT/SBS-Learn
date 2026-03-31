from fastapi import APIRouter, Depends
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
