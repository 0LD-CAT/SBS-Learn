import asyncio
import json
from itertools import combinations
from pathlib import Path

from sqlalchemy import select

from backend.database import AsyncSessionLocal
from backend.lessons.models import (
    Language,
    LanguagePair,
    Lesson,
)
from backend.lessons.packages.helpers import LessonContentSeeder


async def seed_languages(db_session):
    """Добавление ЯП в таблицу languages"""

    existing = await db_session.execute(select(Language))

    if existing.scalars().first():
        return

    languages = [
        Language(
            name="Python",
            slug="python",
            extension="py",
            description="Универсальный интерпретируемый язык программирования с простым синтаксисом. Отлично подходит для начинающих и широко используется в веб-разработке, анализе данных и автоматизации.",
            icon_url="/assets/python_icon.png",
            demo_code='#Test\nprint("Hello, Python!")',
        ),
        Language(
            name="C++",
            slug="cpp",
            extension="cpp",
            description="Компилируемый язык программирования общего назначения с высокой производительностью. Используется в системном программировании, играх и высоконагруженных приложениях.",
            icon_url="/assets/cpp_icon.png",
            demo_code='#include <iostream>\nusing namespace std;\n\nint main() \n{\n\tcout << "Hello, C++!" << endl;\n\treturn 0;\n}',
        ),
        Language(
            name="JavaScript",
            slug="javascript",
            extension="js",
            description="Основной язык веб-разработки, который работает в браузере и на сервере. Используется для создания интерактивных интерфейсов и full-stack приложений.",
            icon_url="/assets/js_icon.png",
            demo_code='console.log("Hello, JavaScript!");',
        ),
    ]

    db_session.add_all(languages)

    await db_session.commit()


async def seed_language_pairs(db_session):
    """Добавление пар ЯП в таблицу language_pairs"""

    existing_pairs = await db_session.execute(select(LanguagePair))

    if existing_pairs.scalars().first():
        return

    result = await db_session.execute(select(Language))
    languages = result.scalars().all()

    pairs = []

    for lang1, lang2 in combinations(languages, 2):
        pairs.append(
            LanguagePair(
                lang1_id=lang1.id,
                lang2_id=lang2.id,
                slug=f"{lang1.slug}-vs-{lang2.slug}",
            )
        )

    db_session.add_all(pairs)
    await db_session.commit()


async def seed_lessons_content(db_session):
    """Добавление наполнения уроков для каждой темы"""
    try:
        json_path = Path(__file__).parent / "content_lessons"
        seeder = LessonContentSeeder(db_session, str(json_path))
        _ = await seeder.seed()
    except Exception as e:
        print(e)

    print("✅ Наполнение уроков контентом завершено!")


async def seed_lessons(db_session, json_path: str = "lessons.json"):
    """Заполнение таблицы уроков темами."""
    file_path = Path(json_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл {json_path} не найден.")

    with open(file_path, "r", encoding="utf-8") as f:
        lessons_data = json.load(f)

    for data in lessons_data:
        stmt = select(Lesson).where(Lesson.slug == data["slug"])
        result = await db_session.execute(stmt)
        lesson = result.scalar_one_or_none()

        if lesson:
            lesson.title = data["title"]
            lesson.order_index = data["order_index"]
        else:
            lesson = Lesson(
                title=data["title"],
                slug=data["slug"],
                order_index=data["order_index"]
            )
            db_session.add(lesson)

    await db_session.commit()
    print(f"Таблица lessons успешно заполнена из {json_path} (обработано {len(lessons_data)} записей).")


async def init_db():
    """Инициализация БД"""
    json_path = Path(__file__).parent / "lessons.json"

    async with AsyncSessionLocal() as db_session:
        await seed_languages(db_session)
        await seed_lessons(db_session, str(json_path))
        await seed_language_pairs(db_session)
        await seed_lessons_content(db_session)


if __name__ == "__main__":
    asyncio.run(init_db())
