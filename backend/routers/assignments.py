from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Assignment, Course, CourseMember, TaskStatus, User, UserRole
from backend.schemas import (
    Assignment as AssignmentSchema,
    AssignmentBroadcastResult,
    AssignmentCreate,
    AssignmentStatusUpdate,
    AssignmentUpdate,
    AssignmentWithCourse,
)
from backend.routers.auth import get_current_user
from backend.notification_utils import create_notification
from typing import List, Union
from datetime import datetime, timedelta

router = APIRouter()

def _get_course_for_user(course_id: int, current_user: User, db: Session) -> Course:
    if current_user.role == UserRole.ADMIN:
        course = db.query(Course).filter(
            (Course.id == course_id) & (Course.user_id == current_user.id)
        ).first()
    else:
        member = db.query(CourseMember).filter(
            (CourseMember.course_id == course_id) & (CourseMember.user_id == current_user.id)
        ).first()
        course = db.query(Course).filter(Course.id == course_id).first() if member else None

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course

def _get_assignment_for_user(assignment_id: int, current_user: User, db: Session) -> Assignment:
    if current_user.role == UserRole.ADMIN:
        assignment = db.query(Assignment).join(Course, Course.id == Assignment.course_id).filter(
            (Assignment.id == assignment_id) & (Course.user_id == current_user.id)
        ).first()
    else:
        assignment = db.query(Assignment).filter(
            (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
        ).first()

    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assignment

@router.post("/", response_model=Union[AssignmentSchema, AssignmentBroadcastResult])
def create_assignment(
    assignment: AssignmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_course_for_user(assignment.course_id, current_user, db)

    # Admin creates identical assignment for each enrolled user of the course.
    if current_user.role == UserRole.ADMIN:
        members = db.query(CourseMember).filter(CourseMember.course_id == assignment.course_id).all()
        if not members:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No enrolled users in this course"
            )

        created_ids = []
        for member in members:
            db_assignment = Assignment(user_id=member.user_id, **assignment.dict())
            db.add(db_assignment)
            db.flush()
            created_ids.append(db_assignment.id)
            create_notification(
                db=db,
                user_id=member.user_id,
                title="New assignment",
                message=f"A new assignment '{db_assignment.title}' was added.",
                type="assignment",
                event_key=f"assignment-created-{db_assignment.id}",
                scheduled_for=db_assignment.deadline,
            )

        db.commit()
        return {
            "created_count": len(created_ids),
            "assignment_ids": created_ids,
        }

    db_assignment = Assignment(user_id=current_user.id, **assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    create_notification(
        db=db,
        user_id=current_user.id,
        title="New assignment",
        message=f"Assignment '{db_assignment.title}' was created.",
        type="assignment",
        event_key=f"assignment-created-{db_assignment.id}",
        scheduled_for=db_assignment.deadline,
    )
    db.commit()
    return db_assignment

@router.get("/", response_model=List[AssignmentWithCourse])
def get_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == UserRole.ADMIN:
        assignments = db.query(Assignment).join(Course, Course.id == Assignment.course_id).filter(
            Course.user_id == current_user.id
        ).all()
    else:
        assignments = db.query(Assignment).filter(Assignment.user_id == current_user.id).all()
    return assignments

@router.get("/upcoming", response_model=List[AssignmentSchema])
def get_upcoming_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    if current_user.role == UserRole.ADMIN:
        assignments = db.query(Assignment).join(Course, Course.id == Assignment.course_id).filter(
            (Course.user_id == current_user.id) &
            (Assignment.deadline > now) &
            (Assignment.status != TaskStatus.COMPLETED)
        ).order_by(Assignment.deadline).all()
    else:
        assignments = db.query(Assignment).filter(
            (Assignment.user_id == current_user.id) &
            (Assignment.deadline > now) &
            (Assignment.status != TaskStatus.COMPLETED)
        ).order_by(Assignment.deadline).all()
    return assignments


@router.get("/overdue", response_model=List[AssignmentSchema])
def get_overdue_assignments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.utcnow()
    if current_user.role == UserRole.ADMIN:
        assignments = db.query(Assignment).join(Course, Course.id == Assignment.course_id).filter(
            (Course.user_id == current_user.id) &
            (Assignment.deadline < now) &
            (Assignment.status != TaskStatus.COMPLETED)
        ).order_by(Assignment.deadline).all()
    else:
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

    if current_user.role == UserRole.ADMIN:
        assignments = db.query(Assignment).join(Course, Course.id == Assignment.course_id).filter(
            (Course.user_id == current_user.id) &
            (Assignment.deadline >= start_of_day) &
            (Assignment.deadline < end_of_day)
        ).order_by(Assignment.deadline).all()
    else:
        assignments = db.query(Assignment).filter(
            (Assignment.user_id == current_user.id) &
            (Assignment.deadline >= start_of_day) &
            (Assignment.deadline < end_of_day)
        ).order_by(Assignment.deadline).all()

    return assignments


@router.get("/{assignment_id}", response_model=AssignmentSchema)
def get_assignment(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _get_assignment_for_user(assignment_id, current_user, db)

@router.put("/{assignment_id}", response_model=AssignmentSchema)
def update_assignment(assignment_id: int, assignment_update: AssignmentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = _get_assignment_for_user(assignment_id, current_user, db)
    
    for key, value in assignment_update.dict().items():
        if value is not None:
            setattr(assignment, key, value)
    
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = _get_assignment_for_user(assignment_id, current_user, db)
    
    db.delete(assignment)
    db.commit()

@router.patch("/{assignment_id}", response_model=AssignmentSchema)
def patch_assignment_status(assignment_id: int, status_update: AssignmentStatusUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = _get_assignment_for_user(assignment_id, current_user, db)

    assignment.status = status_update.status
    db.commit()
    db.refresh(assignment)
    return assignment


@router.patch("/{assignment_id}/status", response_model=AssignmentSchema)
def update_assignment_status(assignment_id: int, status: TaskStatus, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignment = _get_assignment_for_user(assignment_id, current_user, db)

    assignment.status = status
    db.commit()
    db.refresh(assignment)
    return assignment

@router.get("/course/{course_id}", response_model=List[AssignmentSchema])
def get_course_assignments(course_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _get_course_for_user(course_id, current_user, db)

    if current_user.role == UserRole.ADMIN:
        assignments = db.query(Assignment).filter(Assignment.course_id == course_id).all()
    else:
        assignments = db.query(Assignment).filter(
            (Assignment.course_id == course_id) & (Assignment.user_id == current_user.id)
        ).all()
    return assignments


