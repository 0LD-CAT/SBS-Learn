import os
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Lesson, LessonContent


class LessonContentSeeder:
    def __init__(self, db: AsyncSession, content_dir: str = "content_lessons"):
        self.db = db
        self.content_dir = content_dir

    def _load_json_files(self):
        return [
            f for f in os.listdir(self.content_dir)
            if f.endswith(".json")
        ]

    async def _get_lesson_by_slug(self, slug: str):
        result = await self.db.execute(
            select(Lesson).where(Lesson.slug == slug)
        )
        return result.scalar_one_or_none()

    def _load_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        if not raw:
            print(f"⚠️ Skipped empty file: {file_path}")
            return None

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {file_path}: {e}")
            return None

    async def seed(self):
        files = self._load_json_files()

        for file_name in files:
            slug = file_name.replace(".json", "")
            file_path = os.path.join(self.content_dir, file_name)

            lesson = await self._get_lesson_by_slug(slug)

            if not lesson:
                print(f"❌ Lesson not found for slug: {slug}")
                continue

            content_data = self._load_file(file_path)

            if content_data is None:
                print(f"⏭️ Skipping file: {file_name}")
                continue

            result = await self.db.execute(
                select(LessonContent).where(LessonContent.lesson_id == lesson.id)
            )

            existing = result.scalar_one_or_none()

            if existing:
                existing.content = content_data
                existing.version += 1
                print(f"🔄 Updated: {slug}")

            else:
                new_content = LessonContent(
                    lesson_id=lesson.id,
                    content=content_data,
                    version=1
                )
                self.db.add(new_content)
                print(f"➕ Inserted: {slug}")

        await self.db.commit()
