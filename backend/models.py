from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime
import enum

class PriorityLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    courses = relationship("Course", back_populates="user", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="user", cascade="all, delete-orphan")
    study_sessions = relationship("StudySession", back_populates="user", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    instructor = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="courses")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

class Assignment(Base):
    __tablename__ = "assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime)
    priority = Column(Enum(PriorityLevel), default=PriorityLevel.MEDIUM)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="assignments")
    course = relationship("Course", back_populates="assignments")
    subtasks = relationship("Subtask", back_populates="assignment", cascade="all, delete-orphan")

class Subtask(Base):
    __tablename__ = "subtasks"
    
    id = Column(Integer, primary_key=True, index=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignment = relationship("Assignment", back_populates="subtasks")

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="study_sessions")
