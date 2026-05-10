from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.models import Assignment, Course, CourseMember, CourseSchedule, Notification, TaskStatus, StudySession, User, UserRole


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    type: str = "info",
    event_key: str | None = None,
    scheduled_for: datetime | None = None,
) -> None:
    if event_key:
        exists = db.query(Notification).filter(
            (Notification.user_id == user_id) & (Notification.event_key == event_key)
        ).first()
        if exists:
            return

    db.add(
        Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=type,
            event_key=event_key,
            scheduled_for=scheduled_for,
        )
    )


def _parse_hhmm_to_datetime(target_date, hhmm: str) -> datetime:
    hour, minute = [int(x) for x in hhmm.split(":")]
    return datetime(target_date.year, target_date.month, target_date.day, hour, minute)


def ensure_one_hour_notifications(current_user: User, db: Session) -> None:
    now = datetime.utcnow()
    in_one_hour = now + timedelta(hours=1)

    # Assignment deadline reminders
    assignments = db.query(Assignment).filter(
        (Assignment.user_id == current_user.id)
        & (Assignment.status != TaskStatus.COMPLETED)
        & (Assignment.deadline > now)
        & (Assignment.deadline <= in_one_hour)
    ).all()

    for assignment in assignments:
        event_key = f"hour-assignment-{assignment.id}-{assignment.deadline.strftime('%Y%m%d%H%M')}"
        create_notification(
            db=db,
            user_id=current_user.id,
            title="Deadline in 1 hour",
            message=f"Assignment '{assignment.title}' is due within one hour.",
            type="deadline",
            event_key=event_key,
            scheduled_for=assignment.deadline,
        )

    # Study session reminders
    sessions = db.query(StudySession).filter(
        (StudySession.user_id == current_user.id)
        & (StudySession.start_time > now)
        & (StudySession.start_time <= in_one_hour)
    ).all()

    for session in sessions:
        event_key = f"hour-study-session-{session.id}-{session.start_time.strftime('%Y%m%d%H%M')}"
        create_notification(
            db=db,
            user_id=current_user.id,
            title="Study session in 1 hour",
            message=f"Study session '{session.title}' starts within one hour.",
            type="calendar",
            event_key=event_key,
            scheduled_for=session.start_time,
        )

    # Course schedule session reminders (recurring slots)
    if current_user.role == UserRole.ADMIN:
        courses = db.query(Course).filter(Course.user_id == current_user.id).all()
    else:
        courses = db.query(Course).join(CourseMember, CourseMember.course_id == Course.id).filter(
            CourseMember.user_id == current_user.id
        ).all()

    for day_offset in (0, 1):
        target_day = (now + timedelta(days=day_offset)).date()
        weekday = target_day.weekday()

        for course in courses:
            for slot in course.schedules:
                if slot.day_of_week != weekday:
                    continue

                start_dt = _parse_hhmm_to_datetime(target_day, slot.start_time)
                if not (now < start_dt <= in_one_hour):
                    continue

                event_key = f"hour-course-slot-{course.id}-{slot.id}-{start_dt.strftime('%Y%m%d%H%M')}"
                create_notification(
                    db=db,
                    user_id=current_user.id,
                    title="Course session in 1 hour",
                    message=f"Course '{course.name}' starts at {slot.start_time}.",
                    type="calendar",
                    event_key=event_key,
                    scheduled_for=start_dt,
                )
