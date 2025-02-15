from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from app.database import SessionLocal
from sqlalchemy import text

router = APIRouter()


# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================
# Esquemas con Pydantic
# ======================

# Dashboard schemas
class LastStudySessionResponse(BaseModel):
    id: int
    activity_name: str
    group_name: str
    created_at: str
    study_activity_id: int
    group_id: int
    correct_count: int
    incorrect_count: int
    total_items: int


class StudyProgressResponse(BaseModel):
    total_words_studied: int
    total_available_words: int
    mastery_percentage: int


class QuickStatsResponse(BaseModel):
    success_rate: int
    total_study_sessions: int
    total_active_groups: int
    study_streak_days: int


# Schemas para paginación
class Pagination(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int


# Study activities schemas
class StudyActivity(BaseModel):
    id: int
    name: str
    thumbnail_url: str
    description: str
    launch_url: str
    study_session_id: Optional[int] = None
    group_id: Optional[int] = None
    created_at: Optional[str] = None


class StudyActivitiesResponse(BaseModel):
    study_activities: List[StudyActivity]
    pagination: Pagination


class StudyActivityCreateRequest(BaseModel):
    group_id: int
    study_activity_id: int


class StudyActivityCreateResponse(BaseModel):
    id: int
    group_id: int
    study_activity_id: int
    created_at: str
    launch_url: str


# Study sessions schemas
class StudySession(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: str
    end_time: str
    review_items_count: int


class StudySessionsResponse(BaseModel):
    study_sessions: List[StudySession]
    pagination: Pagination


class StudySessionDetail(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: str
    end_time: str
    review_items_count: int
    correct_count: int
    incorrect_count: int


# Words schemas
class Word(BaseModel):
    id: int
    spanish: str
    english: str
    correct_count: int = 0
    wrong_count: int = 0


class WordsResponse(BaseModel):
    items: List[Word]
    pagination: Pagination


# Groups schemas
class Group(BaseModel):
    id: int
    name: str
    word_count: int


class GroupsResponse(BaseModel):
    groups: List[Group]
    pagination: Pagination


# Word review schemas para study session
class WordReview(BaseModel):
    id: int
    spanish: str
    english: str
    correct: bool
    review_time: str


class WordReviewResponse(BaseModel):
    words: List[WordReview]
    pagination: Pagination


# ======================
# Endpoints de la API
# ======================

# Dashboard endpoints
@router.get("/dashboard/last_study_session", response_model=LastStudySessionResponse)
async def get_last_study_session(db: Session = Depends(get_db)):
    # Aquí se implementaría la lógica real para obtener la última sesión de estudio
    return LastStudySessionResponse(
        id=123,
        activity_name="Vocabulary Quiz",
        group_name="Basic Vocabulary",
        created_at="2025-02-11T22:00:00Z",
        study_activity_id=456,
        group_id=1,
        correct_count=8,
        incorrect_count=2,
        total_items=10
    )


@router.get("/dashboard/study_progress", response_model=StudyProgressResponse)
async def get_study_progress(db: Session = Depends(get_db)):
    return StudyProgressResponse(
        total_words_studied=150,
        total_available_words=200,
        mastery_percentage=75
    )


@router.get("/dashboard/quick_stats", response_model=QuickStatsResponse)
async def get_quick_stats(db: Session = Depends(get_db)):
    return QuickStatsResponse(
        success_rate=80,
        total_study_sessions=4,
        total_active_groups=3,
        study_streak_days=4
    )


# Study activities endpoints
@router.get("/study-activities", response_model=StudyActivitiesResponse)
async def list_study_activities(page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    study_activities = [
        StudyActivity(
            id=456,
            name="Vocabulary Quiz",
            thumbnail_url="https://example.com/thumbnail.png",
            description="Practice vocabulary with flashcards",
            launch_url="https://example.com/activities/vocab-quiz"
        )
    ]
    pagination = Pagination(
        current_page=page,
        total_pages=10,
        total_items=100,
        items_per_page=items_per_page
    )
    return StudyActivitiesResponse(study_activities=study_activities, pagination=pagination)


@router.get("/study-activities/{activity_id}", response_model=StudyActivity)
async def get_study_activity(activity_id: int, db: Session = Depends(get_db)):
    return StudyActivity(
        id=activity_id,
        name="Vocabulary Quiz",
        thumbnail_url="https://example.com/thumbnail.png",
        description="Practice vocabulary with flashcards",
        launch_url="https://example.com/activities/vocab-quiz"
    )


@router.get("/study-activities/{activity_id}/study_sessions", response_model=StudySessionsResponse)
async def get_study_sessions_by_activity(activity_id: int, page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    study_sessions = [
        StudySession(
            id=789,
            activity_name="Vocabulary Quiz",
            group_name="Basic Greetings",
            start_time="2024-10-19T12:00:00Z",
            end_time="2024-10-19T12:30:00Z",
            review_items_count=10
        )
    ]
    pagination = Pagination(
        current_page=page,
        total_pages=10,
        total_items=100,
        items_per_page=items_per_page
    )
    return StudySessionsResponse(study_sessions=study_sessions, pagination=pagination)


@router.post("/study-activities", response_model=StudyActivityCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_study_activity(activity: StudyActivityCreateRequest, db: Session = Depends(get_db)):
    new_session_id = 789  # En una implementación real, se guardaría en la base de datos
    created_at = datetime.utcnow().isoformat() + "Z"
    launch_url = f"https://example.com/activities/vocab-quiz?session={new_session_id}"
    return StudyActivityCreateResponse(
        id=new_session_id,
        group_id=activity.group_id,
        study_activity_id=activity.study_activity_id,
        created_at=created_at,
        launch_url=launch_url
    )


# Words endpoints
@router.get("/words", response_model=WordsResponse)
async def list_words(page: int = 1, items_per_page: int = 100, db: Session = Depends(get_db)):
    # Calculate offset
    offset = (page - 1) * items_per_page

    # Query to get words with correct and wrong counts
    query = text("""
        SELECT 
            w.id,
            w.spanish,
            w.english,
            COUNT(CASE WHEN wri.correct THEN 1 END) as correct_count,
            COUNT(CASE WHEN NOT wri.correct THEN 1 END) as wrong_count
        FROM words w
        LEFT JOIN word_review_items wri ON w.id = wri.word_id
        GROUP BY w.id, w.spanish, w.english
        ORDER BY w.id
        LIMIT :items_per_page OFFSET :offset
    """)

    # Execute the query
    words_result = db.execute(query, {
        "items_per_page": items_per_page, 
        "offset": offset
    }).fetchall()

    # Convert results to list of dictionaries
    words = [
        Word(
            id=row.id,
            spanish=row.spanish,
            english=row.english,
            correct_count=row.correct_count or 0, 
            wrong_count=row.wrong_count or 0
        ) for row in words_result
    ]

    # Get total count of words
    total_items_query = text("SELECT COUNT(*) FROM words")
    total_items = db.execute(total_items_query).scalar()

    # Calculate total pages
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Create pagination object
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )

    # Return response
    return WordsResponse(
        items=words,
        pagination=pagination
    )


@router.get("/words/{word_id}", response_model=Word)
async def get_word(word_id: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            w.id,
            w.spanish,
            w.english,
            COUNT(CASE WHEN wri.correct THEN 1 END) as correct_count,
            COUNT(CASE WHEN NOT wri.correct THEN 1 END) as wrong_count
        FROM words w
        LEFT JOIN word_review_items wri ON w.id = wri.word_id
        WHERE w.id = :word_id
        GROUP BY w.id, w.spanish, w.english
    """)
    
    result = db.execute(query, {"word_id": word_id}).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Word not found")
    
    return Word(
        id=result.id,
        spanish=result.spanish,
        english=result.english,
        correct_count=result.correct_count or 0,
        wrong_count=result.wrong_count or 0
    )


# Groups endpoints
@router.get("/groups", response_model=GroupsResponse)
async def list_groups(page: int = 1, items_per_page: int = 100, db: Session = Depends(get_db)):
    groups = [
        Group(id=1, name="Basic Greetings", word_count=10)
    ]
    pagination = Pagination(
        current_page=page,
        total_pages=10,
        total_items=100,
        items_per_page=items_per_page
    )
    return GroupsResponse(groups=groups, pagination=pagination)


@router.get("/groups/{group_id}", response_model=Group)
async def get_group(group_id: int, db: Session = Depends(get_db)):
    return Group(id=group_id, name="Basic Greetings", word_count=10)


@router.get("/groups/{group_id}/words", response_model=WordsResponse)
async def get_words_by_group(group_id: int, page: int = 1, items_per_page: int = 100, db: Session = Depends(get_db)):
    offset = (page - 1) * items_per_page
    
    query = text("""
        SELECT 
            w.id,
            w.spanish,
            w.english,
            COUNT(CASE WHEN wri.correct THEN 1 END) as correct_count,
            COUNT(CASE WHEN NOT wri.correct THEN 1 END) as wrong_count
        FROM words w
        JOIN words_groups wg ON w.id = wg.word_id
        LEFT JOIN word_review_items wri ON w.id = wri.word_id
        WHERE wg.group_id = :group_id
        GROUP BY w.id, w.spanish, w.english
        ORDER BY w.id
        LIMIT :items_per_page OFFSET :offset
    """)
    
    words_result = db.execute(query, {
        "group_id": group_id,
        "items_per_page": items_per_page,
        "offset": offset
    }).fetchall()
    
    items = [
        Word(
            id=row.id,
            spanish=row.spanish,
            english=row.english,
            correct_count=row.correct_count or 0,
            wrong_count=row.wrong_count or 0
        ) for row in words_result
    ]
    
    count_query = text("""
        SELECT COUNT(*) 
        FROM words_groups 
        WHERE group_id = :group_id
    """)
    total_items = db.execute(count_query, {"group_id": group_id}).scalar()
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )
    
    return WordsResponse(items=items, pagination=pagination)


@router.get("/groups/{group_id}/study_sessions", response_model=StudySessionsResponse)
async def get_study_sessions_by_group(group_id: int, page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    study_sessions = [
        StudySession(
            id=789,
            activity_name="Vocabulary Quiz",
            group_name="Basic Greetings",
            start_time="2024-10-19T12:00:00Z",
            end_time="2024-10-19T12:30:00Z",
            review_items_count=10
        )
    ]
    pagination = Pagination(
        current_page=page,
        total_pages=10,
        total_items=100,
        items_per_page=items_per_page
    )
    return StudySessionsResponse(study_sessions=study_sessions, pagination=pagination)


# Study sessions endpoints
@router.get("/study-sessions", response_model=StudySessionsResponse)
async def list_study_sessions(page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    study_sessions = [
        StudySession(
            id=789,
            activity_name="Vocabulary Quiz",
            group_name="Basic Greetings",
            start_time="2024-10-19T12:00:00Z",
            end_time="2024-10-19T12:30:00Z",
            review_items_count=10
        )
    ]
    pagination = Pagination(
        current_page=page,
        total_pages=10,
        total_items=100,
        items_per_page=items_per_page
    )
    return StudySessionsResponse(study_sessions=study_sessions, pagination=pagination)


@router.get("/study-sessions/{session_id}", response_model=StudySessionDetail)
async def get_study_session(session_id: int, db: Session = Depends(get_db)):
    return StudySessionDetail(
        id=session_id,
        activity_name="Vocabulary Quiz",
        group_name="Basic Greetings",
        start_time="2024-10-19T12:00:00Z",
        end_time="2024-10-19T12:30:00Z",
        review_items_count=10,
        correct_count=8,
        incorrect_count=2
    )


@router.get("/study-sessions/{session_id}/words", response_model=WordReviewResponse)
async def get_words_by_study_session(session_id: int, page: int = 1, items_per_page: int = 100, db: Session = Depends(get_db)):
    words = [
        WordReview(
            id=1,
            spanish="hola",
            english="hello",
            correct=True,
            review_time="2024-10-19T12:05:00Z"
        )
    ]
    pagination = Pagination(
        current_page=page,
        total_pages=10,
        total_items=100,
        items_per_page=items_per_page
    )
    return WordReviewResponse(words=words, pagination=pagination)
