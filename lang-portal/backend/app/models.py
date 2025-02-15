"""
Definición de modelos de la base de datos usando SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    spanish = Column(String, nullable=False)
    english = Column(String, nullable=False)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    groups = relationship("Group", secondary="words_groups", back_populates="words")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    words_count = Column(Integer, default=0)
    words = relationship("Word", secondary="words_groups", back_populates="groups")

class WordGroup(Base):
    __tablename__ = "words_groups"
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    created_at = Column(DateTime)
    end_time = Column(DateTime)
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"))
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    total_items = Column(Integer, default=0)

class WordReviewItem(Base):
    __tablename__ = "word_review_items"
    word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), primary_key=True)
    correct = Column(Boolean)
    created_at = Column(DateTime)

class StudyActivity(Base):
    __tablename__ = "study_activities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    thumbnail_url = Column(String)
    description = Column(String)
    launch_url = Column(String)
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    created_at = Column(DateTime)
