from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from database import get_db
from models import Assignment, Course, TaskStatus, User
from schemas import Assignment as AssignmentSchema, AssignmentCreate, AssignmentUpdate, AssignmentWithCourse, AssignmentStatusUpdate
from routers.auth import get_current_user
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/", response_model=AssignmentSchema)
def create_assignment(assignment: AssignmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    # Verify course belongs to user
    course = db.query(Course).filter(
        (Course.id == assignment.course_id) & (Course.user_id == current_user.id)
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    db_assignment = Assignment(
        user_id=current_user.id,
        **assignment.dict()
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=List[AssignmentWithCourse])
def get_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignments = db.query(Assignment).filter(Assignment.user_id == current_user.id).all()
    return assignments

@router.get("/upcoming", response_model=List[AssignmentSchema])
def get_upcoming_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline > now) &
        (Assignment.status != TaskStatus.COMPLETED)
    ).order_by(Assignment.deadline).all()
    return assignments


@router.get("/overdue", response_model=List[AssignmentSchema])
def get_overdue_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline < now) &
        (Assignment.status != TaskStatus.COMPLETED)
    ).order_by(Assignment.deadline).all()
    return assignments


@router.get("/by-date", response_model=List[AssignmentSchema])
def get_assignments_by_date(date: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        target_date = datetime.fromisoformat(date).date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD.")

    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = start_of_day + timedelta(days=1)

    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline >= start_of_day) &
        (Assignment.deadline < end_of_day)
    ).order_by(Assignment.deadline).all()

    return assignments


@router.get("/{assignment_id}", response_model=AssignmentSchema)
def get_assignment(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    return assignment

@router.put("/{assignment_id}", response_model=AssignmentSchema)
def update_assignment(assignment_id: int, assignment_update: AssignmentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    for key, value in assignment_update.dict().items():
        if value is not None:
            setattr(assignment, key, value)
    
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    db.delete(assignment)
    db.commit()

@router.patch("/{assignment_id}", response_model=AssignmentSchema)
def patch_assignment_status(assignment_id: int, status_update: AssignmentStatusUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    assignment.status = status_update.status
    db.commit()
    db.refresh(assignment)
    return assignment


@router.patch("/{assignment_id}/status", response_model=AssignmentSchema)
def update_assignment_status(assignment_id: int, status: TaskStatus, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    assignment.status = status
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("/course/{course_id}", response_model=List[AssignmentSchema])
def get_course_assignments(course_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    # Verify course belongs to user
    course = db.query(Course).filter(
        (Course.id == course_id) & (Course.user_id == current_user.id)
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    assignments = db.query(Assignment).filter(Assignment.course_id == course_id).all()
    return assignments


@router.get("/upcoming", response_model=List[AssignmentSchema])
def get_upcoming_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id) &
        (Assignment.deadline > now) &
        (Assignment.status != TaskStatus.COMPLETED)
    ).order_by(Assignment.deadline).all()
    return assignments


