from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

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

    # constraints
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

    # relationships
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
    # relationships
    pair = relationship(
        "LanguagePair",
        back_populates="users",
    )
