from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserLessonProgress, Lesson
from ...auth.models import User


class UserProgress:
    """Интерфейс для работы с прогрессом пользователя.

    Атрибуты:
        * db_session - экземпляр сессии БД

    Методы:
        * progress_exists() - проверка прогресса пользователя
        * initialize_progress() - инициализировать прогресс пользователя
        * get_user_lessons_progress() - получение прогресса по темам для пользователя
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session


    async def progress_exists(self, user_id: int, language_pair_id: int):
        """Проверка прогресса пользователя.

        :param user_id: id пользователя
        :param language_pair_id: id пары ЯП
        :return: id из UserLessonProgress
        """

        stmt = select(
            UserLessonProgress.id
        ).where(

            UserLessonProgress.user_id == user_id,
            UserLessonProgress.language_pair_id == language_pair_id,

        )

        result = await self.db_session.execute(stmt)

        return result.first() is not None


    async def initialize_progress(self, user_id: int, language_pair_id: int):
        """Инициализация прогресса пользователя

        :param user_id: id пользователя
        :param language_pair_id: id пары ЯП
        :return: None
        """

        exists = await self.progress_exists(
            user_id,
            language_pair_id,
        )

        if exists:
            return

        lessons = (

            await self.db_session.execute(

                select(Lesson)
                .order_by(Lesson.order_index)

            )

        ).scalars().all()

        progress_rows = []

        for lesson in lessons:
            status = (

                "available"
                if lesson.order_index == 1
                else "locked"

            )
            progress_rows.append(
                UserLessonProgress(

                    user_id=user_id,
                    lesson_id=lesson.id,
                    language_pair_id=language_pair_id,
                    status=status,
                )
            )
        self.db_session.add_all(progress_rows)

        await self.db_session.commit()


    async def get_user_lessons_progress(self, user_id: int):
        """Получение прогресса по темам для пользователя.

        :param user_id: id пользователя
        :return: None
        """

        user = await self.db_session.get(User, user_id)

        if not user.current_language_pair_id:
            raise HTTPException(400, "Пара языков не выбрана")

        language_pair_id = user.current_language_pair_id

        stmt = (
            select(
                Lesson,
                UserLessonProgress.status
            )
            .join(
                UserLessonProgress,
                Lesson.id == UserLessonProgress.lesson_id
            )
            .where(
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.language_pair_id == language_pair_id,
            )
            .order_by(
                Lesson.order_index
            )
        )

        result = await self.db_session.execute(stmt)
        rows = result.all()

        if not rows:
            return None

        return [
            {
                "id": lesson.id,
                "title": lesson.title,
                "slug": lesson.slug,
                "order_index": lesson.order_index,
                "status": status,
            }
            for lesson, status in rows
        ]
