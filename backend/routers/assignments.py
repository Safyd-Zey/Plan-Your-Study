from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Assignment, Course, TaskStatus
from schemas import Assignment as AssignmentSchema, AssignmentCreate, AssignmentUpdate, AssignmentWithCourse
from routers.auth import get_current_user
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=AssignmentSchema)
def create_assignment(assignment: AssignmentCreate, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
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
def get_assignments(token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    assignments = db.query(Assignment).filter(Assignment.user_id == current_user.id).all()
    return assignments

@router.get("/{assignment_id}", response_model=AssignmentSchema)
def get_assignment(assignment_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
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
def update_assignment(assignment_id: int, assignment_update: AssignmentUpdate, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    assignment = db.query(Assignment).filter(
        (Assignment.id == assignment_id) & (Assignment.user_id == current_user.id)
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    for key, value in assignment_update.dict().items():
        setattr(assignment, key, value)
    
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
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

@router.get("/course/{course_id}", response_model=List[AssignmentSchema])
def get_course_assignments(course_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    
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
