from sqlalchemy import Boolean, Column, Integer, String

from ..database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    google_id = Column(String, nullable=True)
    github_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=False)
