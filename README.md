# Plan Your Study - Complete System

Plan Your Study is a full-stack study planning application for course-based learning. It supports role-based workflows (admin and user), per-student assignment tracking, schedule management, subtasks, progress analytics, and in-app notifications.

## Project Overview

The system helps students and course admins to:
- organize courses and members,
- manage assignments with deadlines and priorities,
- track status and subtasks,
- view weekly/monthly schedule context,
- monitor completion progress,
- receive in-app reminders.

## System Architecture

### Backend
- Framework: FastAPI
- Database: SQLite (default local runtime), SQLAlchemy ORM
- Authentication: JWT in httpOnly cookie
- API style: REST

### Frontend
- Framework: React 18 + TypeScript
- State: Zustand
- Styling: Tailwind CSS
- Routing: React Router v6
- Build: Vite

## Quick Start (Local Development)

Run both services from two terminals.

### 1) Backend

From project root:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend:
- API base: http://127.0.0.1:8000/api
- Swagger: http://127.0.0.1:8000/docs

### 2) Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:
- App URL: http://localhost:3000

## Quick Start (Docker)

```bash
docker-compose up --build
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Features

### 1. Authentication
- User registration and login
- Role-aware accounts (user/admin)
- JWT session via httpOnly cookie
- Password hashing with bcrypt

### 2. Course Management
- Admin course CRUD
- Add course details (name, description, instructor)
- Enroll users to courses
- Manage recurring course schedule slots

### 3. Assignment Management
- Create assignments with deadlines
- Set priority (low/medium/high)
- Track status (not_started/in_progress/completed)
- Admin broadcast assignment to all enrolled users
- Admin grouped view by shared assignment template

### 4. Subtask Management
- Break down complex assignments
- Track subtask completion
- Visual progress indicators

### 5. Schedule & Calendar
- Weekly and calendar views
- Deadlines + study sessions + course sessions
- Click assignment in schedule to open assignment details
- 24-hour time format

### 6. Progress Tracking
- Completion percentage
- Status distribution
- Upcoming deadlines

### 7. Notifications
- In-app notifications for:
	- added to course,
	- new assignment,
	- one-hour reminders before deadline/session
- Unread notifications persist and are shown after reconnect/login

## Project Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py              # Configuration
│   ├── database.py            # Database setup
│   ├── models.py              # SQLAlchemy models
│   ├── schemas/__init__.py    # Pydantic schemas
│   ├── routers/               # API route handlers
│   │   ├── auth.py            # Authentication
│   │   ├── courses.py         # Course management
│   │   ├── assignments.py     # Assignment management
│   │   ├── subtasks.py        # Subtask management
│   │   ├── progress.py        # Progress tracking
│   │   ├── schedule.py        # Schedule management
│   │   └── notifications.py   # Notification API
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── README.md             # Backend documentation
│
├── frontend/
│   ├── src/
│   │   ├── pages/            # Page components
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── CoursesPage.tsx
│   │   │   ├── AssignmentsPage.tsx
│   │   │   ├── SchedulePage.tsx
│   │   │   └── ProgressPage.tsx
│   │   ├── components/       # Reusable components
│   │   │   └── Navigation.tsx
│   │   ├── api.ts           # API client
│   │   ├── store.ts         # Zustand store
│   │   ├── App.tsx          # Main app
│   │   ├── main.tsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── .env.example
│   ├── README.md            # Frontend documentation
│   └── index.html
│
└── README.md (this file)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/logout` | Logout and clear cookie |
| GET | `/api/auth/users` | List users (admin) |
| POST | `/api/courses/` | Create course |
| GET | `/api/courses/` | Get all courses |
| PUT | `/api/courses/{id}` | Update course |
| DELETE | `/api/courses/{id}` | Delete course |
| POST | `/api/assignments/` | Create assignment |
| GET | `/api/assignments/` | Get all assignments |
| PUT | `/api/assignments/{id}` | Update assignment |
| DELETE | `/api/assignments/{id}` | Delete assignment |
| POST | `/api/subtasks/{assignment_id}` | Create subtask |
| GET | `/api/subtasks/{assignment_id}` | Get subtasks |
| PUT | `/api/subtasks/{subtask_id}` | Update subtask |
| DELETE | `/api/subtasks/{subtask_id}` | Delete subtask |
| GET | `/api/progress/stats` | Get progress statistics |
| GET | `/api/schedule/daily` | Get daily schedule |
| GET | `/api/schedule/weekly` | Get weekly schedule |
| GET | `/api/schedule/calendar` | Get monthly calendar |
| GET | `/api/notifications/unread` | Get unread notifications |
| POST | `/api/notifications/mark-read` | Mark notifications as read |

## Security Notes

- JWT session in httpOnly cookie
- Bcrypt password hashing
- Server-side role and ownership checks
- Per-user data isolation
- Input validation with Pydantic

## Database Entities

### Users
Stores user account information with secure password hashing

### CourseMembers
Maps users to courses for enrollment access

### Assignments
Stores assignments with deadlines, priorities, and status

### Subtasks
Breakdown of complex assignments for better management

### StudySessions
Planned study sessions and events

### Notifications
Persistent in-app reminders and unread delivery

## 🎨 UI/UX Features

- Clean, intuitive interface
- Responsive design for all devices
- Color-coded priorities and statuses
- Smooth animations and transitions
- Accessibility-friendly components
- Dark/light ready styling

## Running Tests

From project root:

```bash
pytest
```

Optional suites are available under the tests directory:
- integration
- e2e
- performance
- mutation
- chaos

## 🛠️ Technology Decisions

**Why FastAPI?**
- Fast performance
- Automatic API documentation
- Strong typing with Python
- Easy to learn and use

**Why React?**
- Component reusability
- Large ecosystem
- Developer experience
- TypeScript support

**Why Tailwind CSS?**
- Utility-first approach
- Rapid development
- Consistent styling
- Small production bundle

**Why Zustand?**
- Minimal boilerplate
- Simple API
- No prop drilling
- DevTools support

## Development Notes

- Frontend and backend run independently during development.
- Backend OpenAPI docs are available at /docs.
- Frontend uses cookie-based requests with credentials enabled.
- Both services support hot reload.

## 🐛 Troubleshooting

**Backend Issues:**
- Ensure Python 3.8+ is installed
- Check all dependencies: `pip list`
- Reset database: delete `study_planner.db`

**Frontend Issues:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `npm cache clean --force`
- Check Node version: `node --version`

## Deployment

### Backend (Example with Gunicorn)
```bash
pip install gunicorn
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

### Frontend (Example with Netlify)
```bash
npm run build
# Deploy dist folder to static hosting
```

## 📚 API Documentation

Once the backend is running, access interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## User Manual

### Getting Started
1. Register a new account
2. Create your first course
3. Add assignments to courses
4. Break down assignments into subtasks
5. Track progress on the dashboard

### Best Practices
- Organize assignments by course
- Set realistic deadlines
- Use priority levels effectively
- Regular progress review
- Break large tasks into subtasks

## 📄 Sample Test Data

Test user credentials will be created when you register. Use the registration page to create a test account.

## 🔄 Data Flow

1. User logs in.
2. Backend sets JWT in httpOnly cookie.
3. Frontend calls protected API routes with credentials.
4. Backend validates cookie token and access scope.
5. Data is stored in Zustand and rendered in UI.

## 📞 Support

For issues, questions, or feature requests, refer to the individual README files in backend and frontend directories.

## 📜 License

This project is part of CSE-2507M course assignment.

---

**Last Updated**: May 2026
**Version**: 1.0.0
