from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db

from ..packages.languages import Languages

router = APIRouter(tags=["Languages"])


@router.get("/languages")
async def get_languages(db_session: AsyncSession = Depends(get_db)):
    """Получение списка всех ЯП из БД.

    :param db_session: Экземпляр сессии БД.
    :return: Список ЯП.
    """

    languages = await Languages(db_session).get_languages()

    return languages
