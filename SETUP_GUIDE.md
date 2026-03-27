# Plan Your Study - Setup & Installation Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Node.js 16 or higher
- npm (comes with Node.js)
- Git (for version control)

### Operating System Support
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

## Complete Installation Steps

### Step 1: Clone or Extract Project

```bash
cd "Plan Your Study"
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Configure Environment

```bash
# Copy example env file
cp .env.example .env

# On Windows: copy .env.example .env
```

Edit `.env` if needed (defaults should work for development):
- `DATABASE_URL=sqlite:///study_planner.db`
- `SECRET_KEY=your-secret-key-here-change-in-production`

#### 2.4 Start Backend Server

```bash
python main.py
```

✅ Backend is running at `http://localhost:8000`

Visit `http://localhost:8000/docs` to see API documentation

### Step 3: Frontend Setup

#### 3.1 Install Node Modules

**Open a NEW terminal window/tab** (keep backend running)

```bash
cd frontend

# Install dependencies
npm install
```

#### 3.2 Configure Environment

```bash
# Copy example env file
cp .env.example .env.local

# On Windows: copy .env.example .env.local
```

No changes needed for development (defaults are correct)

#### 3.3 Start Frontend Development Server

```bash
npm run dev
```

✅ Frontend is running at `http://localhost:3000`

## Verification Checklist

After starting both servers, verify everything works:

- [ ] Backend running at `http://localhost:8000`
- [ ] API docs accessible at `http://localhost:8000/docs`
- [ ] Frontend running at `http://localhost:3000`
- [ ] Can access login page at `http://localhost:3000/login`
- [ ] No console errors in browser

## First Time Usage

### 1. Create User Account

1. Go to `http://localhost:3000`
2. Click "Register here" link
3. Fill in:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: (any password)
4. Click "Create Account"

### 2. Create First Course

1. Click "Courses" in navigation
2. Click "New Course" button
3. Fill in course details:
   - Name: `Mathematics 101`
   - Description: (optional)
   - Instructor: (optional)
4. Click "Add Course"

### 3. Create Assignment

1. Click "Assignments" in navigation
2. Click "New Assignment" button
3. Fill in fields:
   - Course: Select your course
   - Title: `Chapter 5 Exercises`
   - Deadline: Set a date/time
   - Priority: Select level
4. Click "Create"

### 4. Add Subtasks

1. In Assignments page, expand your new assignment
2. In "Subtasks" section, enter a subtask title
3. Click "Add"
4. Check boxes to mark subtasks complete

### 5. View Schedule & Progress

- Click "Schedule" to see weekly calendar
- Click "Progress" to see completion stats
- Click "Dashboard" to see overview

## Troubleshooting

### Backend Issues

**"Port 8000 already in use"**
```bash
# Find and kill process using port 8000
# Windows:
netstat -ano | findstr :8000

# macOS/Linux:
lsof -ti:8000 | xargs kill
```

**"ModuleNotFoundError"**
```bash
# Make sure virtual environment is activated
# Then reinstall requirements
pip install -r requirements.txt
```

**"Database error"**
```bash
# Delete the database and restart
rm study_planner.db
python main.py
```

### Frontend Issues

**"Port 3000 already in use"**
```bash
# Kill process using port 3000
# Windows:
netstat -ano | findstr :3000

# macOS/Linux:
lsof -ti:3000 | xargs kill
```

**"npm: command not found"**
- Install Node.js from https://nodejs.org/
- Restart terminal after installation

**"Dependencies not installing"**
```bash
# Clear npm cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**"Blank page or API errors"**
- Verify backend is running at `http://localhost:8000`
- Check browser console for errors (F12)
- Clear browser cache

### General Issues

**"Cannot connect to backend"**
1. Check backend is running: `http://localhost:8000/docs`
2. Check firewall settings
3. Verify API_URL in frontend `.env.local`

**"Login not working"**
1. Verify user exists (check registration worked)
2. Check email/password combination
3. Clear browser localStorage

## Common Commands

### Backend

```bash
# Activate virtual environment
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows

# Run server
python main.py

# Deactivate virtual environment
deactivate
```

### Frontend

```bash
# Start development
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check

# Clear cache
npm cache clean --force
```

## Development Workflow

### Terminal Setup (Recommended)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Optional:**
```bash
# For running additional commands
cd "Plan Your Study"
```

### Making Changes

**Backend Changes:**
- Edit files in `backend/routers/`, `backend/models.py`, etc.
- Server auto-reloads with `--reload`
- Check `http://localhost:8000/docs` for updated API

**Frontend Changes:**
- Edit files in `frontend/src/`
- Browser auto-refreshes with dev server
- Check browser console for errors

## Database Reset

To start fresh with a clean database:

```bash
# Stop the backend server (Ctrl+C)

# Navigate to backend
cd backend

# Delete database
rm study_planner.db

# Restart server
python main.py
```

## Production Deployment

### Backend Production Build

```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

### Frontend Production Build

```bash
# Build optimized bundle
npm run build

# Output in dist/ folder ready for deployment
# Deploy dist/ folder to static host (Netlify, Vercel, etc.)
```

## Environment Variables Reference

### Backend (.env)

| Variable | Default | Notes |
|----------|---------|-------|
| DATABASE_URL | sqlite:///study_planner.db | SQLite for dev, PostgreSQL recommended for production |
| SECRET_KEY | your-secret-key-here | **Change in production** |
| ALGORITHM | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Token expiration time |

### Frontend (.env.local)

| Variable | Default | Notes |
|----------|---------|-------|
| VITE_API_URL | http://localhost:8000/api | Backend API endpoint |

## Getting Help

- Check the README.md files in `backend/` and `frontend/` directories
- Review API documentation at `http://localhost:8000/docs`
- Check browser console (F12) for frontend errors
- Check terminal output for backend errors

## Next Steps

1. ✅ Complete this setup guide
2. ✅ Create test user and data
3. ✅ Explore all features
4. ✅ Read API documentation
5. ✅ Start developing

## Quick Reference

```bash
# Backend Commands
cd backend && source venv/bin/activate && python main.py

# Frontend Commands
cd frontend && npm run dev

# Reset Everything
cd backend && rm study_planner.db
cd frontend && rm -rf node_modules && npm install
```

---

**Happy planning! 📚✨**

If you encounter any issues, refer to the Troubleshooting section above or check the individual README files.
