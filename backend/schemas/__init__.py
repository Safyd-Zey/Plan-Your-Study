from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from backend.models import PriorityLevel, TaskStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
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
