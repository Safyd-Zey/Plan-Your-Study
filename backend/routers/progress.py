from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Assignment, TaskStatus
from schemas import ProgressStats
from routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/stats", response_model=ProgressStats)
def get_progress_stats(token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
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
