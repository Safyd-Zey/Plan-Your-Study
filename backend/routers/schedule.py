from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Assignment, StudySession, User
from schemas import Assignment as AssignmentSchema, StudySession as StudySessionSchema, StudySessionCreate
from routers.auth import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/daily", response_model=dict)
def get_daily_schedule(date: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all assignments and study sessions for a specific day"""
    
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
        "assignments": [AssignmentSchema.from_orm(a).dict() for a in assignments],
        "study_sessions": [StudySessionSchema.from_orm(s).dict() for s in sessions]
    }

@router.get("/weekly", response_model=dict)
def get_weekly_schedule(start_date: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all assignments and study sessions for a week"""
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
        "assignments": [AssignmentSchema.from_orm(a).dict() for a in assignments],
        "study_sessions": [StudySessionSchema.from_orm(s).dict() for s in sessions]
    }


@router.get("/calendar", response_model=dict)
def get_monthly_calendar(month: str = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all assignment deadlines and study sessions for a given month"""

    today = datetime.utcnow().date()
    if not month:
        month_year = today.replace(day=1)
    else:
        try:
            month_year = datetime.fromisoformat(month + "-01").date()
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid month format. Use YYYY-MM")

    month_start = month_year.replace(day=1)
    if month_start.month == 12:
        month_end = month_start.replace(year=month_start.year + 1, month=1, day=1)
    else:
        month_end = month_start.replace(month=month_start.month + 1, day=1)

    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline >= month_start) &
        (Assignment.deadline < month_end)
    ).all()

    sessions = db.query(StudySession).filter(
        (StudySession.user_id == current_user.id) &
        (StudySession.start_time >= month_start) &
        (StudySession.start_time < month_end)
    ).all()

    # Build calendar map
    days = []
    day = month_start
    while day < month_end:
        day_str = day.isoformat()
        days.append({
            "date": day_str,
            "assignments": [AssignmentSchema.from_orm(a).dict() for a in assignments if a.deadline.date() == day],
            "study_sessions": [StudySessionSchema.from_orm(s).dict() for s in sessions if s.start_time.date() == day],
        })
        day += timedelta(days=1)

    return {
        "month": month_start.strftime("%Y-%m"),
        "days": days,
        "assignments": [AssignmentSchema.from_orm(a).dict() for a in assignments],
        "study_sessions": [StudySessionSchema.from_orm(s).dict() for s in sessions]
    }

@router.post("/study-sessions", response_model=StudySessionSchema)
def create_study_session(session: StudySessionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Create a new study session"""
    db_session = StudySession(
        user_id=current_user.id,
        **session.dict()
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/study-sessions", response_model=List[StudySessionSchema])
def get_study_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all study sessions for current user"""
    sessions = db.query(StudySession).filter(StudySession.user_id == current_user.id).all()
    return sessions
