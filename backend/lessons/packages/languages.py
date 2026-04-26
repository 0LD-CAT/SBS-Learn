from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from ..models import Language, LanguagePair, UserLanguagePair
from ...auth.models import User


class Languages:
    """Интерфейс для работы с пользователем.

    Атрибуты:
        * db_session - экземпляр сессии БД

    Методы:
        * get_languages() - получить все ЯП
    """

    def __init__(self, db_session: Optional[AsyncSession] = None):
        self.db_session = db_session

    async def get_languages(self):
        """Получить ЯП из таблицы languages

        :return: {"languages": languages} | None
        """

        result = await self.db_session.execute(select(Language))

        languages = result.scalars().all()
        if languages:
            return {"languages": languages}

        return None

    async def get_languages_pairs(self, user_id: int):
        """Получить пары ЯП из таблицы languages_pairs

        :param user_id: id пользователя
        :return: {"languages_pairs": languages_pairs} | None
        """

        lang1 = aliased(Language)
        lang2 = aliased(Language)

        stmt = (
            select(LanguagePair, lang1, lang2)
            .join(UserLanguagePair, UserLanguagePair.pair_id == LanguagePair.id)
            .join(lang1, LanguagePair.lang1_id == lang1.id)
            .join(lang2, LanguagePair.lang2_id == lang2.id)
            .where(UserLanguagePair.user_id == user_id)
        )

        result = await self.db_session.execute(stmt)

        row = result.first()

        if not row:
            return None

        pair, lang1_obj, lang2_obj = row

        return {
            "slug": pair.slug,
            "lang1": {
                "id": lang1_obj.id,
                "name": lang1_obj.name,
                "slug": lang1_obj.slug,
                "icon_url": lang1_obj.icon_url,
            },
            "lang2": {
                "id": lang2_obj.id,
                "name": lang2_obj.name,
                "slug": lang2_obj.slug,
                "icon_url": lang2_obj.icon_url,
            },
        }

    async def select_languages_pair(self, user_id: int, lang1_id: int, lang2_id: int):
        """Добавление пары ЯП для изучения

        :param user_id: id пользователя
        :param lang1_id: id первого ЯП
        :param lang2_id: id второго ЯП
        :return: pair
        """

        lang1_id, lang2_id = sorted([lang1_id, lang2_id])
        # проверка пары ЯП
        stmt = select(LanguagePair).where(
            LanguagePair.lang1_id == lang1_id, LanguagePair.lang2_id == lang2_id
        )

        result = await self.db_session.execute(stmt)

        pair = result.scalar_one_or_none()

        if not pair:
            raise HTTPException(404, "Пара ЯП не найдена!")
        # сохранить пару пользователю
        stmt = select(UserLanguagePair).where(UserLanguagePair.user_id == user_id)

        result = await self.db_session.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.pair_id = pair.id
        else:
            self.db_session.add(UserLanguagePair(user_id=user_id, pair_id=pair.id))

        # обновляем активную пару пользователя
        user_stmt = select(User).where(User.id == user_id)
        user_result = await self.db_session.execute(user_stmt)
        user = user_result.scalar_one()
        user.current_language_pair_id = pair.id

        await self.db_session.commit()
        await self.db_session.refresh(pair)

        return pair
