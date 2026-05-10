from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import Notification, User
from backend.notification_utils import ensure_one_hour_notifications
from backend.routers.auth import get_current_user
from backend.schemas import Notification as NotificationSchema, NotificationMarkReadRequest

router = APIRouter()


@router.get('/unread', response_model=list[NotificationSchema])
def get_unread_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Generate due one-hour reminders at read time to support "offline then login" scenario.
    ensure_one_hour_notifications(current_user, db)
    db.commit()

    notifications = db.query(Notification).filter(
        (Notification.user_id == current_user.id) & (Notification.is_read == False)  # noqa: E712
    ).order_by(Notification.created_at.asc()).all()
    return notifications


@router.post('/mark-read')
def mark_notifications_as_read(
    payload: NotificationMarkReadRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not payload.ids:
        return {'updated': 0}

    updated = db.query(Notification).filter(
        (Notification.user_id == current_user.id) & (Notification.id.in_(payload.ids))
    ).update({Notification.is_read: True}, synchronize_session=False)
    db.commit()
    return {'updated': updated}
