# Plan Your Study - Backend README

## Overview
FastAPI backend for the "Plan Your Study" application - a comprehensive study planning and task management system for students.

## Features
- User authentication with JWT tokens
- Course management (CRUD operations)
- Assignment management with priorities and deadlines
- Subtask management for breaking down complex assignments
- Study schedule management
- Progress tracking and statistics
- Daily and weekly schedule views

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: JWT with bcrypt
- **Validation**: Pydantic
- **Server**: Uvicorn

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Important Notes
- **Run from project root**: All commands must be run from the project root directory, not from the backend folder, due to absolute import paths
- **Virtual environment**: Ensure the virtual environment is activated before running commands

### Setup Steps

1. **Navigate to project root**
   ```bash
   cd path/to/Plan-Your-Study  # Project root, not backend folder
   ```

2. **Create virtual environment** (if not already created)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the server**
   ```bash
   # From PROJECT ROOT (not from backend directory!)
   cd ..
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Courses
- `POST /api/courses/` - Create course
- `GET /api/courses/` - Get all courses
- `GET /api/courses/{id}` - Get specific course
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

### Assignments
- `POST /api/assignments/` - Create assignment
- `GET /api/assignments/` - Get all assignments
- `GET /api/assignments/{id}` - Get specific assignment
- `PUT /api/assignments/{id}` - Update assignment
- `DELETE /api/assignments/{id}` - Delete assignment
- `GET /api/assignments/course/{course_id}` - Get assignments for a course

### Subtasks
- `POST /api/subtasks/` - Create subtask
- `GET /api/subtasks/{assignment_id}` - Get subtasks for assignment
- `PUT /api/subtasks/{id}` - Update subtask
- `DELETE /api/subtasks/{id}` - Delete subtask

### Progress
- `GET /api/progress/stats` - Get progress statistics

### Schedule
- `GET /api/schedule/daily` - Get daily schedule
- `GET /api/schedule/weekly` - Get weekly schedule
- `POST /api/schedule/study-sessions` - Create study session
- `GET /api/schedule/study-sessions` - Get all study sessions

## Database Models

### User
- id (Primary Key)
- email (Unique)
- username (Unique)
- hashed_password
- created_at
- updated_at

### Course
- id (Primary Key)
- user_id (Foreign Key)
- name
- description
- instructor
- created_at
- updated_at

### Assignment
- id (Primary Key)
- user_id (Foreign Key)
- course_id (Foreign Key)
- title
- description
- deadline
- priority (low, medium, high)
- status (not_started, in_progress, completed)
- created_at
- updated_at

### Subtask
- id (Primary Key)
- assignment_id (Foreign Key)
- title
- description
- status
- order
- created_at
- updated_at

### StudySession
- id (Primary Key)
- user_id (Foreign Key)
- title
- description
- start_time
- end_time
- reminder_sent
- created_at

## Configuration

Key configuration options in `config.py`:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT encoding (change in production!)
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: 30 minutes)

## Security Notes

- Always change `SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting for production
- Set up proper CORS policies
- Use environment variables for sensitive data

## Testing

Run tests with:
```bash
pytest
```

## Development

For development with auto-reload:
```bash
uvicorn main:app --reload
```

## Deployment

For production deployment:
1. Use a production WSGI server (e.g., Gunicorn)
2. Set up proper environment variables
3. Use a production database (PostgreSQL recommended)
4. Enable HTTPS
5. Set up proper logging and monitoring

Example production command:
```bash
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

## Troubleshooting

**Port already in use**: Change the port in `main.py` or use `lsof -ti:8000 | xargs kill`

**Database errors**: Delete `study_planner.db` to reset the database

**CORS errors**: Check CORS configuration in `main.py`

## Support & Contact

For issues or questions, please refer to the project documentation or create an issue in the repository.
