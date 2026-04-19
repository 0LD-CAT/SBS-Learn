import enum

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Enum,
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
    """Таблица языков программирования"""

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


class SectionType(str, enum.Enum):
    theory = "theory"
    comparison_table = "comparison_table"
    fact = "fact"
    quiz = "quiz"
    code_example = "code_example"


class LessonSection(Base):
    """Секции внутри урока"""

    __tablename__ = "lesson_sections"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )
    type = Column(
        Enum(SectionType, name="section_type_enum"),
        nullable=False,
    )
    order_index = Column(Integer, nullable=False)
    title = Column(String(255))

    lesson = relationship(
        "Lesson",
        backref="sections",
    )


class LessonTheoryBlock(Base):
    """Теоретические блоки урока"""

    __tablename__ = "lesson_theory_blocks"
    id = Column(Integer, primary_key=True)
    section_id = Column(
        Integer,
        ForeignKey("lesson_sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    content_md = Column(Text, nullable=False)

    section = relationship("LessonSection", backref="theory_blocks")


class ComparisonTable(Base):
    """Сравнительная таблица внутри секции"""

    __tablename__ = "comparison_tables"
    id = Column(Integer, primary_key=True)
    section_id = Column(
        Integer,
        ForeignKey("lesson_sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    title = Column(String(255))

    section = relationship("LessonSection", backref="comparison_tables")


class ComparisonTableRow(Base):
    """Строки сравнительной таблицы"""

    __tablename__ = "comparison_table_rows"
    id = Column(Integer, primary_key=True)
    table_id = Column(
        Integer,
        ForeignKey("comparison_tables.id", ondelete="CASCADE"),
        nullable=False,
    )
    left_content = Column(Text, nullable=False)
    right_content = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)

    table = relationship(
        "ComparisonTable",
        backref="rows",
    )


class LessonFact(Base):
    """Интересные факты внутри урока"""

    __tablename__ = "lesson_facts"
    id = Column(Integer, primary_key=True)
    section_id = Column(
        Integer,
        ForeignKey("lesson_sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    fact_text = Column(Text, nullable=False)

    section = relationship(
        "LessonSection",
        backref="facts",
    )


class CodeExample(Base):
    """Примеры кода для Monaco Editor"""

    __tablename__ = "code_examples"
    id = Column(Integer, primary_key=True)
    section_id = Column(
        Integer,
        ForeignKey("lesson_sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    language_id = Column(
        Integer,
        ForeignKey("languages.id", ondelete="CASCADE"),
        nullable=False,
    )
    code = Column(Text, nullable=False)

    section = relationship(
        "LessonSection",
        backref="code_examples",
    )


class LessonQuiz(Base):
    """Тест урока"""

    __tablename__ = "lesson_quizzes"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(
        Integer,
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
    )

    title = Column(String(255))

    lesson = relationship(
        "Lesson",
        backref="quizzes",
    )


class QuizQuestion(Base):
    """Вопрос теста"""

    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True)
    quiz_id = Column(
        Integer,
        ForeignKey("lesson_quizzes.id", ondelete="CASCADE"),
        nullable=False,
    )
    language_pair_id = Column(
        Integer,
        ForeignKey("language_pairs.id"),
        nullable=True,
    )
    question_text = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)

    quiz = relationship(
        "LessonQuiz",
        backref="questions",
    )


class QuizAnswer(Base):
    """Ответ на вопрос теста"""

    __tablename__ = "quiz_answers"
    id = Column(Integer, primary_key=True)
    question_id = Column(
        Integer,
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    answer_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship(
        "QuizQuestion",
        backref="answers",
    )


class UserQuizAnswer(Base):
    """Ответ пользователя на тест"""

    __tablename__ = "user_quiz_answers"
    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id = Column(
        Integer,
        ForeignKey("quiz_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    selected_answer_id = Column(
        Integer,
        ForeignKey("quiz_answers.id"),
        nullable=False,
    )
    is_correct = Column(Boolean)
    answered_at = Column(
        DateTime,
        server_default=func.now(),
    )
