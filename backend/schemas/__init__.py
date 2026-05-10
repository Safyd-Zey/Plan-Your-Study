from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from backend.models import PriorityLevel, TaskStatus, UserRole

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Course Schedule Schemas
class CourseScheduleBase(BaseModel):
    day_of_week: int  # 0=Monday, ..., 6=Sunday
    start_time: str   # "HH:MM"
    end_time: str     # "HH:MM"
    room: Optional[str] = None

class CourseScheduleCreate(CourseScheduleBase):
    pass

class CourseSchedule(CourseScheduleBase):
    id: int
    course_id: int

    class Config:
        from_attributes = True

class CourseScheduleWithCourse(CourseSchedule):
    course_name: str

class CourseMemberCreate(BaseModel):
    user_id: int

class CourseMember(BaseModel):
    id: int
    course_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Course Schemas
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructor: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    schedules: List[CourseSchedule] = []
    
    class Config:
        from_attributes = True

# Subtask Schemas
class SubtaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.NOT_STARTED

class SubtaskCreate(SubtaskBase):
    pass

class SubtaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class SubtaskStatusUpdate(BaseModel):
    status: TaskStatus

class Subtask(SubtaskBase):
    id: int
    assignment_id: int
    order: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime
    priority: PriorityLevel = PriorityLevel.MEDIUM
    status: TaskStatus = TaskStatus.NOT_STARTED

class AssignmentCreate(AssignmentBase):
    course_id: int

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[PriorityLevel] = None
    status: Optional[TaskStatus] = None
    course_id: Optional[int] = None

class AssignmentStatusUpdate(BaseModel):
    status: TaskStatus

class Assignment(AssignmentBase):
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    updated_at: datetime
    subtasks: List[Subtask] = []
    
    class Config:
        from_attributes = True

class AssignmentWithCourse(Assignment):
    course: Course
    user: User

class AssignmentBroadcastResult(BaseModel):
    created_count: int
    assignment_ids: List[int]

# Study Session Schemas
class StudySessionBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class StudySessionCreate(StudySessionBase):
    pass

class StudySession(StudySessionBase):
    id: int
    user_id: int
    reminder_sent: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenWithUser(Token):
    id: int
    email: EmailStr
    username: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Progress Schemas
class ProgressStats(BaseModel):
    total_assignments: int
    completed_assignments: int
    in_progress_assignments: int
    not_started_assignments: int
    completion_percentage: float
    upcoming_deadlines: List[Assignment]


# Notification Schemas
class Notification(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    scheduled_for: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationMarkReadRequest(BaseModel):
    ids: List[int]
