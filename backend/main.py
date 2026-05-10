from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import Base, engine
from backend.routers import auth, courses, assignments, subtasks, progress, schedule, notifications
import os
from sqlalchemy import inspect, text

def _run_legacy_migrations():
    inspector = inspect(engine)
    if "users" in inspector.get_table_names():
        user_columns = {col["name"] for col in inspector.get_columns("users")}
        if "role" not in user_columns:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(10) DEFAULT 'user'"))
                conn.execute(text("UPDATE users SET role = 'user' WHERE role IS NULL"))
        else:
            with engine.begin() as conn:
                # Normalize legacy values from previous enum storage format.
                conn.execute(text("UPDATE users SET role = 'user' WHERE role IN ('USER', 'user') OR role IS NULL"))
                conn.execute(text("UPDATE users SET role = 'admin' WHERE role IN ('ADMIN', 'admin')"))

# Create tables
Base.metadata.create_all(bind=engine)
_run_legacy_migrations()

app = FastAPI(
    title="Plan Your Study API",
    description="API for study planning and task management system",
    version="1.0.0"
)

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(assignments.router, prefix="/api/assignments", tags=["Assignments"])
app.include_router(subtasks.router, prefix="/api/subtasks", tags=["Subtasks"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(schedule.router, prefix="/api/schedule", tags=["Schedule"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Plan Your Study API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
