from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Assignment, StudySession
from schemas import Assignment as AssignmentSchema, StudySession as StudySessionSchema, StudySessionCreate
from routers.auth import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/daily", response_model=dict)
def get_daily_schedule(date: str = None, token: str = None, db: Session = Depends(get_db)):
    """Get all assignments and study sessions for a specific day"""
    current_user = get_current_user(token, db)
    
    if date is None:
        target_date = datetime.utcnow().date()
    else:
        target_date = datetime.fromisoformat(date).date()
    
    # Get assignments due on this day
    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline.cast(db.Date) == target_date)
    ).all()
    
    # Get study sessions on this day
    sessions = db.query(StudySession).filter(
        (StudySession.user_id == current_user.id) &
        (StudySession.start_time.cast(db.Date) == target_date)
    ).all()
    
    return {
        "date": target_date.isoformat(),
        "assignments": assignments,
        "study_sessions": sessions
    }

@router.get("/weekly", response_model=dict)
def get_weekly_schedule(start_date: str = None, token: str = None, db: Session = Depends(get_db)):
    """Get all assignments and study sessions for a week"""
    current_user = get_current_user(token, db)
    
    if start_date is None:
        start = datetime.utcnow().date()
    else:
        start = datetime.fromisoformat(start_date).date()
    
    end = start + timedelta(days=7)
    
    # Get assignments for this week
    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline >= start) &
        (Assignment.deadline < end)
    ).all()
    
    # Get study sessions for this week
    sessions = db.query(StudySession).filter(
        (StudySession.user_id == current_user.id) &
        (StudySession.start_time >= start) &
        (StudySession.start_time < end)
    ).all()
    
    return {
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "assignments": assignments,
        "study_sessions": sessions
    }

@router.post("/study-sessions", response_model=StudySessionSchema)
def create_study_session(session: StudySessionCreate, token: str = None, db: Session = Depends(get_db)):
    """Create a new study session"""
    current_user = get_current_user(token, db)
    
    db_session = StudySession(
        user_id=current_user.id,
        **session.dict()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/study-sessions", response_model=List[StudySessionSchema])
def get_study_sessions(token: str = None, db: Session = Depends(get_db)):
    """Get all study sessions for current user"""
    current_user = get_current_user(token, db)
    sessions = db.query(StudySession).filter(StudySession.user_id == current_user.id).all()
    return sessions
