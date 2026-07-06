from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    word = Column(String(100), index=True, nullable=False)
    meaning = Column(Text, nullable=False)
    example = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
