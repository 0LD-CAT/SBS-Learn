from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Lesson


class Lessons:
    """Интерфейс для работы с темами.

    Атрибуты:
        * db_session - экземпляр сессии БД

    Методы:
        * get_lessons() - получить все темы
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    async def get_lessons(self):
        """Получить тем уроков из таблицы lessons

        :return: {"lessons": lessons} | None
        """

        stmt = select(Lesson).order_by(
            Lesson.order_index
        )

        result = await self.db_session.execute(stmt)

        lessons = result.scalars().all()

        if lessons:
            return {"lessons": lessons}

        return None
