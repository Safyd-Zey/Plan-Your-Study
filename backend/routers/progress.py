from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Assignment, TaskStatus, User
from backend.schemas import ProgressStats
from backend.routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/stats", response_model=ProgressStats)
def get_progress_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignments = db.query(Assignment).filter(Assignment.user_id == current_user.id).all()
    
    total = len(assignments)
    completed = len([a for a in assignments if a.status == TaskStatus.COMPLETED])
    in_progress = len([a for a in assignments if a.status == TaskStatus.IN_PROGRESS])
    not_started = len([a for a in assignments if a.status == TaskStatus.NOT_STARTED])
    
    completion_percentage = (completed / total * 100) if total > 0 else 0
    
    # Get upcoming deadlines
    now = datetime.utcnow()
    upcoming = [a for a in assignments if a.deadline > now and a.status != TaskStatus.COMPLETED]
    upcoming.sort(key=lambda x: x.deadline)
    
    return {
        "total_assignments": total,
        "completed_assignments": completed,
        "in_progress_assignments": in_progress,
        "not_started_assignments": not_started,
        "completion_percentage": completion_percentage,
        "upcoming_deadlines": upcoming[:5]  # Top 5 upcoming
    }


@router.get("/detail", response_model=dict)
def get_progress_detail(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignments = db.query(Assignment).filter(Assignment.user_id == current_user.id).all()

    now = datetime.utcnow()
    overdue = [a for a in assignments if a.deadline < now and a.status != TaskStatus.COMPLETED]
    today = [a for a in assignments if a.deadline.date() == now.date()]

    return {
        "total_assignments": len(assignments),
        "overdue_assignments": len(overdue),
        "today_assignments": len(today),
        "upcoming_assignments": len([a for a in assignments if a.deadline > now and a.status != TaskStatus.COMPLETED])
    }
