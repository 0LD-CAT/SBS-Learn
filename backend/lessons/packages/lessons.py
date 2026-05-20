from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Lesson, LessonContent, UserLessonProgress, LanguagePair


class Lessons:
    """Интерфейс для работы с темами.

    Атрибуты:
        * db_session - экземпляр сессии БД

    Методы:
        * get_lessons() - получить все темы
        * get_lesson_content() - получить контент для темы урока
        * filter_blocks_by_languages() - получить контент для пары ЯП
        * get_progress_by_language_pairs() - получение % прогресса изучения
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

    async def get_lesson_content(self, lesson_id: int, left_lang: str, right_lang: str):
        """Получить контент для темы урока из таблицы lesson_content

        :param lesson_id: id урока
        :param left_lang: 1 язык
        :param right_lang: 2 язык
        :return: {"lesson": lesson_data, "content": lesson_content} | None
        """

        stmt = select(LessonContent).where(LessonContent.lesson_id == lesson_id)
        result = await self.db_session.execute(stmt)
        lesson = result.scalar_one_or_none()

        if not lesson:
            return None

        content = lesson.content

        content["blocks"] = await self.filter_blocks_by_languages(
            content["blocks"],
            left_lang,
            right_lang
        )

        return content


    async def filter_blocks_by_languages(self, blocks, left_lang, right_lang):
        """Фильтрация блоков контента для пары ЯП.

        :param blocks: блок контента
        :param left_lang: 1 ЯП
        :param right_lang: 2 ЯП
        :return: нужный контент для пары ЯП
        """

        langs = {left_lang, right_lang}

        filtered_blocks = []

        for block in blocks:

            block_copy = block.copy()

            if block["type"] == "comparison_matrix":

                new_block = block_copy

                new_block["languages"] = [
                    lang for lang in block.get("languages", [])
                    if lang in langs
                ]

                new_rows = []

                for row in block.get("rows", []):

                    new_row = {
                        "attribute": row["attribute"],
                        "values": {
                            lang: row["values"].get(lang)
                            for lang in new_block["languages"]
                        }
                    }

                    new_rows.append(new_row)

                new_block["rows"] = new_rows

                filtered_blocks.append(new_block)

                continue

            if block["type"] in ["code_showcase", "side_by_side_code"]:

                new_block = block_copy

                snippets = block.get("snippets", {})

                new_block["snippets"] = {
                    lang: snippets.get(lang, {})
                    for lang in langs
                }

                filtered_blocks.append(new_block)

                continue

            language_keys = {"python", "cpp", "javascript"}

            if language_keys.intersection(block.keys()):

                new_block = {"type": block["type"]}

                for lang in langs:
                    new_block[lang] = block.get(lang, {})

                filtered_blocks.append(new_block)

                continue

            filtered_blocks.append(block_copy)

        return filtered_blocks

    async def get_progress_by_language_pairs(self, user_id: int):
        """Получение % прогресса изучения пар ЯП для пользователя.

        :param user_id: id пользователя.
        :return: % выполнения.
        """

        total_lessons_query = select(func.count(Lesson.id))
        total_lessons = (await self.db_session.execute(total_lessons_query)).scalar()


        pairs_query = select(LanguagePair.id, LanguagePair.slug)
        pairs = (await self.db_session.execute(pairs_query)).all()

        result = []

        for pair_id, slug in pairs:

            completed_query = select(func.count(UserLessonProgress.id)).where(
                UserLessonProgress.user_id == user_id,
                UserLessonProgress.language_pair_id == pair_id,
                UserLessonProgress.status == "completed"
            )

            completed = (await self.db_session.execute(completed_query)).scalar()

            if completed == 0:
                progress = 0
            else:
                progress = int((completed / total_lessons) * 100)

            result.append({
                "language_pair_id": pair_id,
                "slug": slug,
                "progress": progress
            })

        return result
