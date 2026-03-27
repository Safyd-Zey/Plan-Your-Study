from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Course, User
from schemas import Course as CourseSchema, CourseCreate, CourseUpdate
from routers.auth import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=CourseSchema)
def create_course(course: CourseCreate, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    db_course = Course(
        user_id=current_user.id,
        **course.dict()
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/", response_model=List[CourseSchema])
def get_courses(token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    courses = db.query(Course).filter(Course.user_id == current_user.id).all()
    return courses

@router.get("/{course_id}", response_model=CourseSchema)
def get_course(course_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    course = db.query(Course).filter(
        (Course.id == course_id) & (Course.user_id == current_user.id)
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return course

@router.put("/{course_id}", response_model=CourseSchema)
def update_course(course_id: int, course_update: CourseUpdate, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    course = db.query(Course).filter(
        (Course.id == course_id) & (Course.user_id == current_user.id)
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    for key, value in course_update.dict().items():
        setattr(course, key, value)
    
    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, token: str = None, db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)
    course = db.query(Course).filter(
        (Course.id == course_id) & (Course.user_id == current_user.id)
    ).first()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    db.delete(course)
    db.commit()
