import asyncio
from itertools import combinations

from sqlalchemy import select

from backend.database import AsyncSessionLocal
from backend.lessons.models import Language, LanguagePair


async def seed_languages(db_session):
    """Добавление ЯП в таблицу languages"""
    languages = [
        Language(
            name="Python",
            slug="python",
            extension="py",
            description="Python — универсальный "
            "интерпретируемый язык программирования с простым синтаксисом.",
            icon_url="/icons/python.svg",
        ),
        Language(
            name="C++",
            slug="cpp",
            extension="cpp",
            description="C++ — компилируемый язык "
            "программирования с высокой производительностью.",
            icon_url="/icons/cpp.svg",
        ),
        Language(
            name="JavaScript",
            slug="javascript",
            extension="js",
            description="JavaScript — основной язык веб-разработки.",
            icon_url="/icons/javascript.svg",
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


async def init_db():
    """Инициалтзация БД"""
    async with AsyncSessionLocal() as db_session:
        # await seed_languages(session)
        await seed_language_pairs(db_session)


if __name__ == "__main__":
    asyncio.run(init_db())
