from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import Base, engine
from backend.routers import auth, courses, assignments, subtasks, progress, schedule
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Plan Your Study API",
    description="API for study planning and task management system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
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
