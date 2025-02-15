import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Word, Group, WordGroup, StudySession, WordReviewItem, StudyActivity
from app.main import app
from fastapi.testclient import TestClient
from datetime import datetime

# Create a test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_test_data(db):
    """Seed the test database with initial data"""
    # Create a group
    group = Group(name="Test Group", words_count=2)
    db.add(group)
    db.commit()

    # Create some words
    words = [
        Word(
            spanish="hola", 
            english="hello", 
            correct_count=1,
            wrong_count=0
        ),
        Word(
            spanish="adiós", 
            english="goodbye", 
            correct_count=0,
            wrong_count=1
        )
    ]
    db.add_all(words)
    db.commit()

    # Link words to group
    for word in words:
        word_group = WordGroup(word_id=word.id, group_id=group.id)
        db.add(word_group)
    
    # Create a study activity
    study_activity = StudyActivity(
        name="Test Vocabulary Quiz", 
        thumbnail_url="http://example.com/thumbnail.png",
        description="A test vocabulary quiz",
        launch_url="http://example.com/quiz",
        created_at=datetime.now()
    )
    db.add(study_activity)
    
    # Create a study session
    study_session = StudySession(
        group_id=group.id, 
        created_at=datetime.now(),
        study_activity_id=study_activity.id,
        correct_count=1,
        incorrect_count=1,
        total_items=2
    )
    db.add(study_session)
    
    # Create word review items
    review_items = [
        WordReviewItem(
            word_id=words[0].id, 
            study_session_id=study_session.id, 
            correct=True, 
            created_at=datetime.now()
        ),
        WordReviewItem(
            word_id=words[1].id, 
            study_session_id=study_session.id, 
            correct=False, 
            created_at=datetime.now()
        )
    ]
    db.add_all(review_items)
    
    db.commit()

@pytest.fixture(scope="session")
def test_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a database session
    db = TestingSessionLocal()
    try:
        # Seed test data
        seed_test_data(db)
        yield db
    finally:
        db.close()
        # Drop all tables after tests
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)
