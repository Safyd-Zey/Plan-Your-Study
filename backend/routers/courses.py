from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Assignment, Course, CourseMember, CourseSchedule, TaskStatus, User, UserRole
from backend.notification_utils import create_notification
from backend.routers.auth import get_current_admin, get_current_user
from backend.schemas import (
    Course as CourseSchema,
    CourseCreate,
    CourseMemberCreate,
    CourseSchedule as CourseScheduleSchema,
    CourseScheduleCreate,
    CourseUpdate,
    User as UserSchema,
)
from typing import List

router = APIRouter()


def _get_owned_course_or_404(course_id: int, admin_id: int, db: Session) -> Course:
    course = db.query(Course).filter(
        (Course.id == course_id) & (Course.user_id == admin_id)
    ).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


def _get_visible_course_or_404(course_id: int, current_user: User, db: Session) -> Course:
    if current_user.role == UserRole.ADMIN:
        return _get_owned_course_or_404(course_id, current_user.id, db)

    member = db.query(CourseMember).filter(
        (CourseMember.course_id == course_id) & (CourseMember.user_id == current_user.id)
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return course


@router.post("/", response_model=CourseSchema, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    db_course = Course(user_id=current_admin.id, **course.dict())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/", response_model=List[CourseSchema])
def get_courses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == UserRole.ADMIN:
        return db.query(Course).filter(Course.user_id == current_user.id).all()

    return db.query(Course).join(CourseMember, CourseMember.course_id == Course.id).filter(
        CourseMember.user_id == current_user.id
    ).all()


@router.get("/{course_id}", response_model=CourseSchema)
def get_course(course_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _get_visible_course_or_404(course_id, current_user, db)


@router.put("/{course_id}", response_model=CourseSchema)
def update_course(
    course_id: int,
    course_update: CourseUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    course = _get_owned_course_or_404(course_id, current_admin.id, db)

    for key, value in course_update.dict().items():
        setattr(course, key, value)

    db.commit()
    db.refresh(course)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    course = _get_owned_course_or_404(course_id, current_admin.id, db)
    db.delete(course)
    db.commit()


@router.get("/{course_id}/members", response_model=List[UserSchema])
def get_course_members(
    course_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _get_owned_course_or_404(course_id, current_admin.id, db)
    return db.query(User).join(CourseMember, CourseMember.user_id == User.id).filter(
        CourseMember.course_id == course_id
    ).order_by(User.username.asc()).all()


@router.post("/{course_id}/members", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def add_course_member(
    course_id: int,
    member_data: CourseMemberCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _get_owned_course_or_404(course_id, current_admin.id, db)

    user = db.query(User).filter(User.id == member_data.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.role != UserRole.USER:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only regular users can be enrolled")

    exists = db.query(CourseMember).filter(
        (CourseMember.course_id == course_id) & (CourseMember.user_id == member_data.user_id)
    ).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already enrolled in this course")

    db_member = CourseMember(course_id=course_id, user_id=member_data.user_id)
    db.add(db_member)

    # When a user is enrolled after assignments already exist in the course,
    # create personal copies so each student has independent status tracking.
    templates = db.query(Assignment).filter(Assignment.course_id == course_id).all()
    seen = set()
    for template in templates:
        key = (
            template.title,
            template.description,
            template.deadline,
            template.priority,
        )
        if key in seen:
            continue
        seen.add(key)
        db.add(
            Assignment(
                user_id=user.id,
                course_id=course_id,
                title=template.title,
                description=template.description,
                deadline=template.deadline,
                priority=template.priority,
                status=TaskStatus.NOT_STARTED,
            )
        )

    create_notification(
        db=db,
        user_id=user.id,
        title="Added to course",
        message=f"You were added to course '{_get_owned_course_or_404(course_id, current_admin.id, db).name}'.",
        type="course",
        event_key=f"course-added-{course_id}-{user.id}",
    )

    db.commit()
    return user


@router.delete("/{course_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_course_member(
    course_id: int,
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _get_owned_course_or_404(course_id, current_admin.id, db)

    member = db.query(CourseMember).filter(
        (CourseMember.course_id == course_id) & (CourseMember.user_id == user_id)
    ).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")

    db.delete(member)
    db.commit()


@router.post("/{course_id}/schedules", response_model=CourseScheduleSchema, status_code=status.HTTP_201_CREATED)
def add_course_schedule(
    course_id: int,
    schedule: CourseScheduleCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _get_owned_course_or_404(course_id, current_admin.id, db)
    db_schedule = CourseSchedule(course_id=course_id, **schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


@router.get("/{course_id}/schedules", response_model=List[CourseScheduleSchema])
def get_course_schedules(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_visible_course_or_404(course_id, current_user, db)
    return db.query(CourseSchedule).filter(CourseSchedule.course_id == course_id).all()


@router.delete("/{course_id}/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_schedule(
    course_id: int,
    schedule_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    _get_owned_course_or_404(course_id, current_admin.id, db)
    db_schedule = db.query(CourseSchedule).filter(
        (CourseSchedule.id == schedule_id) & (CourseSchedule.course_id == course_id)
    ).first()
    if not db_schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    db.delete(db_schedule)
    db.commit()
