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

# Schemas base para evitar referencias circulares
class StudyActivityBase(BaseModel):
    id: int
    name: str
    thumbnail_url: Optional[str]
    description: str
    launch_url: str

class GroupBase(BaseModel):
    id: int
    name: str
    word_count: int

class StudySessionBase(BaseModel):
    id: int
    activity_name: str
    group_name: str
    start_time: str
    end_time: Optional[str]
    review_items_count: int

class WordBase(BaseModel):
    id: int
    spanish: str
    english: str
    correct_count: int = 0
    wrong_count: int = 0

class Pagination(BaseModel):
    current_page: int
    total_pages: int
    total_items: int
    items_per_page: int

# Schemas que extienden los base
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

class StudyActivity(StudyActivityBase):
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

class StudySession(StudySessionBase):
    pass

class StudySessionsResponse(BaseModel):
    study_sessions: List[StudySession]
    pagination: Pagination

class StudySessionDetail(StudySessionBase):
    correct_count: int
    incorrect_count: int

class Word(WordBase):
    pass

class WordsResponse(BaseModel):
    items: List[Word]
    pagination: Pagination

class Group(GroupBase):
    pass

class GroupsResponse(BaseModel):
    groups: List[Group]
    pagination: Pagination

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
    query = text("""
        SELECT 
            ss.id,
            sa.name as activity_name,
            g.name as group_name,
            ss.created_at,
            sa.id as study_activity_id,
            g.id as group_id,
            COUNT(CASE WHEN wri.correct THEN 1 END) as correct_count,
            COUNT(CASE WHEN NOT wri.correct THEN 1 END) as incorrect_count,
            COUNT(*) as total_items
        FROM study_sessions ss
        JOIN study_activities sa ON ss.study_activity_id = sa.id
        JOIN groups g ON ss.group_id = g.id
        LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
        GROUP BY ss.id, sa.name, g.name, ss.created_at, sa.id, g.id
        ORDER BY ss.created_at DESC
        LIMIT 1
    """)
    
    result = db.execute(query).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No study sessions found"
        )
    
    return LastStudySessionResponse(
        id=result.id,
        activity_name=result.activity_name,
        group_name=result.group_name,
        created_at=result.created_at,
        study_activity_id=result.study_activity_id,
        group_id=result.group_id,
        correct_count=result.correct_count,
        incorrect_count=result.incorrect_count,
        total_items=result.total_items
    )


@router.get("/dashboard/study_progress", response_model=StudyProgressResponse)
async def get_study_progress(db: Session = Depends(get_db)):
    query = text("""
        WITH WordStats AS (
            SELECT 
                COUNT(DISTINCT w.id) as total_available_words,
                COUNT(DISTINCT CASE 
                    WHEN wri.correct THEN w.id 
                END) as total_words_studied
            FROM words w
            LEFT JOIN word_review_items wri ON w.id = wri.word_id
        )
        SELECT 
            total_words_studied,
            total_available_words,
            CASE 
                WHEN total_available_words > 0 THEN
                    (total_words_studied * 100 / total_available_words)
                ELSE 0 
            END as mastery_percentage
        FROM WordStats
    """)
    
    result = db.execute(query).first()
    
    return StudyProgressResponse(
        total_words_studied=result.total_words_studied or 0,
        total_available_words=result.total_available_words or 0,
        mastery_percentage=result.mastery_percentage or 0
    )


@router.get("/dashboard/quick_stats", response_model=QuickStatsResponse)
async def get_quick_stats(db: Session = Depends(get_db)):
    query = text("""
        WITH ReviewStats AS (
            SELECT 
                COUNT(CASE WHEN correct THEN 1 END) * 100 / COUNT(*) as success_rate
            FROM word_review_items
        ),
        SessionStats AS (
            SELECT 
                COUNT(DISTINCT id) as total_study_sessions
            FROM study_sessions
        ),
        GroupStats AS (
            SELECT 
                COUNT(DISTINCT id) as total_active_groups
            FROM groups
        ),
        StreakStats AS (
            SELECT 
                COUNT(DISTINCT DATE(created_at)) as study_streak_days
            FROM study_sessions
            WHERE created_at >= DATE('now', '-7 days')
        )
        SELECT 
            COALESCE(r.success_rate, 0) as success_rate,
            s.total_study_sessions,
            g.total_active_groups,
            st.study_streak_days
        FROM ReviewStats r
        CROSS JOIN SessionStats s
        CROSS JOIN GroupStats g
        CROSS JOIN StreakStats st
    """)
    
    result = db.execute(query).first()
    
    return QuickStatsResponse(
        success_rate=result.success_rate or 0,
        total_study_sessions=result.total_study_sessions or 0,
        total_active_groups=result.total_active_groups or 0,
        study_streak_days=result.study_streak_days or 0
    )


# Study activities endpoints
@router.get("/study-activities", response_model=StudyActivitiesResponse)
async def list_study_activities(page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * items_per_page
    
    count_query = text("""
        SELECT COUNT(*) as total
        FROM study_activities
    """)
    total_items = db.execute(count_query).scalar()
    
    query = text("""
        SELECT 
            id,
            name,
            thumbnail_url,
            description,
            launch_url
        FROM study_activities
        LIMIT :limit OFFSET :offset
    """)
    
    results = db.execute(query, {
        "limit": items_per_page,
        "offset": offset
    }).fetchall()
    
    study_activities = [
        StudyActivity(
            id=row.id,
            name=row.name,
            thumbnail_url=row.thumbnail_url,
            description=row.description,
            launch_url=row.launch_url
        )
        for row in results
    ]
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )
    
    return StudyActivitiesResponse(
        study_activities=study_activities,
        pagination=pagination
    )


@router.get("/study-activities/{activity_id}", response_model=StudyActivity)
async def get_study_activity(activity_id: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            id,
            name,
            thumbnail_url,
            description,
            launch_url
        FROM study_activities
        WHERE id = :activity_id
    """)
    
    result = db.execute(query, {"activity_id": activity_id}).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study activity with id {activity_id} not found"
        )
    
    return StudyActivity(
        id=result.id,
        name=result.name,
        thumbnail_url=result.thumbnail_url,
        description=result.description,
        launch_url=result.launch_url
    )


@router.get("/study-activities/{activity_id}/study-sessions", response_model=StudySessionsResponse)
async def get_study_sessions_by_activity(activity_id: int, page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * items_per_page
    
    count_query = text("""
        SELECT COUNT(*) as total
        FROM study_sessions ss
        WHERE ss.study_activity_id = :activity_id
    """)
    total_items = db.execute(count_query, {"activity_id": activity_id}).scalar()
    
    query = text("""
        SELECT 
            ss.id,
            sa.name as activity_name,
            g.name as group_name,
            ss.created_at as start_time,
            ss.end_time,
            COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN study_activities sa ON ss.study_activity_id = sa.id
        JOIN groups g ON ss.group_id = g.id
        LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
        WHERE ss.study_activity_id = :activity_id
        GROUP BY ss.id, sa.name, g.name, ss.created_at, ss.end_time
        ORDER BY ss.created_at DESC
        LIMIT :limit OFFSET :offset
    """)
    
    results = db.execute(query, {
        "activity_id": activity_id,
        "limit": items_per_page,
        "offset": offset
    }).fetchall()
    
    study_sessions = [
        StudySession(
            id=row.id,
            activity_name=row.activity_name,
            group_name=row.group_name,
            start_time=row.start_time,
            end_time=row.end_time,
            review_items_count=row.review_items_count
        )
        for row in results
    ]
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )
    
    return StudySessionsResponse(
        study_sessions=study_sessions,
        pagination=pagination
    )


@router.post("/study-activities", response_model=StudyActivityCreateResponse)
async def create_study_activity(activity: StudyActivityCreateRequest, db: Session = Depends(get_db)):
    query = text("""
        INSERT INTO study_sessions (group_id, study_activity_id, created_at)
        VALUES (:group_id, :study_activity_id, CURRENT_TIMESTAMP)
        RETURNING id, created_at
    """)
    
    result = db.execute(query, {
        "group_id": activity.group_id,
        "study_activity_id": activity.study_activity_id
    }).first()
    
    # Get the launch URL from the study activity
    launch_url_query = text("""
        SELECT launch_url
        FROM study_activities
        WHERE id = :activity_id
    """)
    
    launch_url_result = db.execute(launch_url_query, {
        "activity_id": activity.study_activity_id
    }).first()
    
    if not launch_url_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study activity with id {activity.study_activity_id} not found"
        )
    
    db.commit()
    
    return StudyActivityCreateResponse(
        id=result.id,
        group_id=activity.group_id,
        study_activity_id=activity.study_activity_id,
        created_at=result.created_at,
        launch_url=launch_url_result.launch_url
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
    query = text("""
        SELECT g.id, g.name, g.words_count as word_count
        FROM groups g
        WHERE g.id = :group_id
    """)
    
    result = db.execute(query, {"group_id": group_id}).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found"
        )
    
    return Group(
        id=result.id,
        name=result.name,
        word_count=result.word_count
    )


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
        JOIN word_groups wg ON w.id = wg.word_id
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
        FROM word_groups 
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


@router.get("/groups/{group_id}/study-sessions", response_model=StudySessionsResponse)
async def get_study_sessions_by_group(group_id: int, page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * items_per_page
    
    count_query = text("""
        SELECT COUNT(*) as total
        FROM study_sessions ss
        WHERE ss.group_id = :group_id
    """)
    total_items = db.execute(count_query, {"group_id": group_id}).scalar()
    
    query = text("""
        SELECT 
            ss.id,
            sa.name as activity_name,
            g.name as group_name,
            ss.created_at as start_time,
            ss.end_time,
            COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN study_activities sa ON ss.study_activity_id = sa.id
        JOIN groups g ON ss.group_id = g.id
        LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
        WHERE ss.group_id = :group_id
        GROUP BY ss.id, sa.name, g.name, ss.created_at, ss.end_time
        ORDER BY ss.created_at DESC
        LIMIT :limit OFFSET :offset
    """)
    
    results = db.execute(query, {
        "group_id": group_id,
        "limit": items_per_page,
        "offset": offset
    }).fetchall()
    
    study_sessions = [
        StudySession(
            id=row.id,
            activity_name=row.activity_name,
            group_name=row.group_name,
            start_time=row.start_time,
            end_time=row.end_time,
            review_items_count=row.review_items_count
        )
        for row in results
    ]
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )
    
    return StudySessionsResponse(
        study_sessions=study_sessions,
        pagination=pagination
    )


# Study sessions endpoints
@router.get("/study-sessions", response_model=StudySessionsResponse)
async def list_study_sessions(page: int = 1, items_per_page: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * items_per_page
    
    count_query = text("""
        SELECT COUNT(*) as total
        FROM study_sessions
    """)
    total_items = db.execute(count_query).scalar()
    
    query = text("""
        SELECT 
            ss.id,
            sa.name as activity_name,
            g.name as group_name,
            ss.created_at as start_time,
            ss.end_time,
            COUNT(wri.id) as review_items_count
        FROM study_sessions ss
        JOIN study_activities sa ON ss.study_activity_id = sa.id
        JOIN groups g ON ss.group_id = g.id
        LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
        GROUP BY ss.id, sa.name, g.name, ss.created_at, ss.end_time
        ORDER BY ss.created_at DESC
        LIMIT :limit OFFSET :offset
    """)
    
    results = db.execute(query, {
        "limit": items_per_page,
        "offset": offset
    }).fetchall()
    
    study_sessions = [
        StudySession(
            id=row.id,
            activity_name=row.activity_name,
            group_name=row.group_name,
            start_time=row.start_time,
            end_time=row.end_time,
            review_items_count=row.review_items_count
        )
        for row in results
    ]
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )
    
    return StudySessionsResponse(
        study_sessions=study_sessions,
        pagination=pagination
    )


@router.get("/study-sessions/{session_id}", response_model=StudySessionDetail)
async def get_study_session(session_id: int, db: Session = Depends(get_db)):
    query = text("""
        SELECT 
            ss.id,
            sa.name as activity_name,
            g.name as group_name,
            ss.created_at as start_time,
            ss.end_time,
            COUNT(wri.id) as review_items_count,
            COUNT(CASE WHEN wri.correct THEN 1 END) as correct_count,
            COUNT(CASE WHEN NOT wri.correct THEN 1 END) as incorrect_count
        FROM study_sessions ss
        JOIN study_activities sa ON ss.study_activity_id = sa.id
        JOIN groups g ON ss.group_id = g.id
        LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
        WHERE ss.id = :session_id
        GROUP BY ss.id, sa.name, g.name, ss.created_at, ss.end_time
    """)
    
    result = db.execute(query, {"session_id": session_id}).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Study session with id {session_id} not found"
        )
    
    return StudySessionDetail(
        id=result.id,
        activity_name=result.activity_name,
        group_name=result.group_name,
        start_time=result.start_time,
        end_time=result.end_time,
        review_items_count=result.review_items_count,
        correct_count=result.correct_count,
        incorrect_count=result.incorrect_count
    )


@router.get("/study-sessions/{session_id}/words", response_model=WordReviewResponse)
async def get_words_by_study_session(session_id: int, page: int = 1, items_per_page: int = 100, db: Session = Depends(get_db)):
    offset = (page - 1) * items_per_page
    
    count_query = text("""
        SELECT COUNT(*) as total
        FROM word_review_items wri
        WHERE wri.study_session_id = :session_id
    """)
    total_items = db.execute(count_query, {"session_id": session_id}).scalar()
    
    query = text("""
        SELECT 
            w.id,
            w.spanish,
            w.english,
            wri.correct,
            wri.created_at as review_time
        FROM word_review_items wri
        JOIN words w ON wri.word_id = w.id
        WHERE wri.study_session_id = :session_id
        ORDER BY wri.created_at
        LIMIT :limit OFFSET :offset
    """)
    
    results = db.execute(query, {
        "session_id": session_id,
        "limit": items_per_page,
        "offset": offset
    }).fetchall()
    
    words = [
        WordReview(
            id=row.id,
            spanish=row.spanish,
            english=row.english,
            correct=row.correct,
            review_time=row.review_time
        )
        for row in results
    ]
    
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    pagination = Pagination(
        current_page=page,
        total_pages=total_pages,
        total_items=total_items,
        items_per_page=items_per_page
    )
    
    return WordReviewResponse(
        words=words,
        pagination=pagination
    )
