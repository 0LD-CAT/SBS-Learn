from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from ..database import Base


class Language(Base):
    """Таблица языков программирования"""

    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), nullable=False, unique=True)
    extension = Column(String(10), nullable=False, unique=True)
    description = Column(Text)
    icon_url = Column(String(255))
    demo_code = Column(Text, default="")

    pairs_as_lang1 = relationship(
        "LanguagePair",
        foreign_keys="LanguagePair.lang1_id",
        back_populates="lang1",
    )
    pairs_as_lang2 = relationship(
        "LanguagePair",
        foreign_keys="LanguagePair.lang2_id",
        back_populates="lang2",
    )


class LanguagePair(Base):
    """Таблица пар языков программирования"""

    __tablename__ = "language_pairs"
    id = Column(Integer, primary_key=True)
    lang1_id = Column(
        Integer,
        ForeignKey("languages.id", ondelete="CASCADE"),
        nullable=False,
    )
    lang2_id = Column(
        Integer,
        ForeignKey("languages.id", ondelete="CASCADE"),
        nullable=False,
    )
    slug = Column(String(100), nullable=False, unique=True)
    order_index = Column(Integer, default=0)

    __table_args__ = (
        CheckConstraint(
            "lang1_id < lang2_id",
            name="check_language_pair_order",
        ),
        UniqueConstraint(
            "lang1_id",
            "lang2_id",
            name="unique_language_pair",
        ),
    )
    lang1 = relationship(
        "Language",
        foreign_keys=[lang1_id],
        back_populates="pairs_as_lang1",
    )
    lang2 = relationship(
        "Language",
        foreign_keys=[lang2_id],
        back_populates="pairs_as_lang2",
    )
    users = relationship(
        "UserLanguagePair",
        back_populates="pair",
        cascade="all, delete",
    )


class UserLanguagePair(Base):
    """Активная пара языков пользователя (выбор onboarding)"""

    __tablename__ = "user_language_pairs"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    pair_id = Column(
        Integer,
        ForeignKey("language_pairs.id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP,
        server_default=func.now(),
    )

    pair = relationship(
        "LanguagePair",
        back_populates="users",
    )


class Lesson(Base):
    """Таблица тем для уроков"""

    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, unique=True)
    slug = Column(String(50), nullable=False, unique=True)
    order_index = Column(Integer, nullable=False, unique=True)


class UserLessonProgress(Base):
    """Таблица прогресса пользователя"""

    __tablename__ = "user_lessons_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    language_pair_id = Column(
        Integer,
        ForeignKey("language_pairs.id", ondelete="CASCADE"),
        nullable=False,
    )
    status = Column(
        String(20),
        default="locked",
        nullable=False,
    )
    completed_at = Column(DateTime)

    lesson = relationship("Lesson")
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", "language_pair_id"),)


class LessonContent(Base):
    """Таблица контента для каждой темы"""

    __tablename__ = "lesson_contents"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, unique=True)
    content = Column(JSONB, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())