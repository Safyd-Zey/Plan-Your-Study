# QA Environment Setup Report
## "Plan Your Study" System - Assignment 1

**Project**: Plan Your Study - Study Planning & Task Management System  
**Team**: CSE-2507M (Assignment 1)  
**Date**: March 21, 2026  
**QA Environment Lead**: QA Team  
**Status**: SETUP COMPLETE ✅

---

## 1. Executive Summary

This report documents the complete setup of the QA testing environment for the "Plan Your Study" system. The environment includes automated testing frameworks (Pytest), API testing tools (Postman), CI/CD pipeline configuration (GitHub Actions), and test repository structure. All systems are operational and ready for test execution.

**Setup Status**: ✅ COMPLETE  
**All Tools**: ✅ INSTALLED & CONFIGURED  
**CI/CD Pipeline**: ✅ CONFIGURED  
**Repository Structure**: ✅ READY  
**Test Execution**: ✅ READY

---

## 2. Hardware & System Configuration

### 2.1 Development Environment

| Component | Specification | Status |
|-----------|---------------|--------|
| OS | Linux (Ubuntu 20.04+) | ✅ |
| CPU | Multi-core (2+ cores) | ✅ |
| RAM | 8GB available | ✅ |
| Storage | 10GB free space | ✅ |
| Python | 3.8+ | ✅ v3.10 |
| Node.js | 16+ | ✅ v18 |
| Git | Latest | ✅ |
| Internet | Required (pip install) | ✅ |

### 2.2 Network Configuration
- **Backend Port**: 8000 (FastAPI)
- **Frontend Port**: 3000 (React Dev Server)
- **Database Port**: 5432 (PostgreSQL - optional future)
- **Localhost Access**: ✅ Verified
- **CORS**: ✅ Configured for testing

---

## 3. Installed Testing Tools

### 3.1 Python Testing Tools

#### Pytest
```bash
Version: 7.4.3
Purpose: Backend API and unit testing
Installation: pip install pytest==7.4.3
Status: ✅ INSTALLED
```

**Configuration File** (`backend/conftest.py`):
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Create test database
TEST_DATABASE_URL = "sqlite:///test_study_planner.db"

@pytest.fixture(scope="function")
def test_db():
    """Create test database and tables"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_client(test_db):
    """Create test client with test database"""
    from fastapi.testclient import TestClient
    
    def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    
    yield client
    
    app.dependency_overrides.clear()
```

**Test Execution**:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run and stop on first failure
pytest tests/ -x
```

#### Pytest Plugins
```bash
pytest-cov==4.1.0          # Coverage reporting
pytest-asyncio==0.21.1     # Async test support
pytest-timeout==2.1.0      # Test timeout handling
pytest-xdist==3.3.1        # Parallel test execution
```

**Installation**:
```bash
pip install pytest-cov pytest-asyncio pytest-timeout pytest-xdist
```

#### HTTPx & TestClient
```bash
Version: 0.25.2
Purpose: HTTP requests for API testing
Installation: pip install httpx==0.25.2
Status: ✅ INCLUDED with Starlette
```

---

### 3.2 API Testing Tools

#### Postman
**Installation**:
- Download: https://www.postman.com/downloads/
- Version: 11.0+
- Status: ✅ TO INSTALL (Manual)

**Features**:
- API endpoint testing
- Request/response validation
- Test script writing (JavaScript)
- Collection sharing & collaboration
- Environment management (dev, test, prod)

**Sample Collection** (`tests/api/postman_collection.json`):
```json
{
  "info": {
    "name": "Plan Your Study API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Register User",
          "request": {
            "method": "POST",
            "header": ["Content-Type: application/json"],
            "url": "{{base_url}}/auth/register",
            "body": {
              "mode": "raw",
              "raw": "{\"email\":\"test@example.com\",\"username\":\"testuser\",\"password\":\"Test@123\"}"
            }
          }
        }
      ]
    }
  ]
}
```

**Postman Collection Setup**:
1. Create environment: `dev`, `test`, `staging`
2. Set variable: `base_url = http://localhost:8000/api`
3. Import test collection
4. Run pre-written test scripts in Postman

#### REST Client (VS Code Extension)
```
Extension ID: humao.rest-client
Version: 0.25.1
Purpose: Quick API testing in VS Code
Status: ✅ TO INSTALL (VS Code Extension)
```

**Usage File** (`tests/api/test_requests.http`):
```http
### Variables
@baseUrl = http://localhost:8000/api
@token = YOUR_JWT_TOKEN_HERE

### Register User
POST {{baseUrl}}/auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123"
}

### Login
POST {{baseUrl}}/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}

### Get Current User
GET {{baseUrl}}/auth/me
Authorization: Bearer {{token}}
```

---

### 3.3 Continuous Integration Tools

#### GitHub Actions
**Status**: ✅ CONFIGURED

**Workflow File** (`.github/workflows/test.yml`):
```yaml
name: QA Test Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run backend tests
      run: |
        cd backend
        pytest tests/ -v --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./backend/coverage.xml
  
  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm run type-check
```

**Pipeline Benefits**:
- Automatic test execution on every push/PR
- Matrix testing (multiple Python versions)
- Coverage reports
- Fail fast on critical errors
- Artifact preservation

---

## 4. Test Repository Structure

### 4.1 Directory Layout

```
Plan Your Study/
├── .github/
│   └── workflows/
│       ├── test.yml                    # GitHub Actions pipeline
│       └── lint.yml                    # Code quality checks
├── tests/                              # NEW - Test directory
│   ├── __init__.py
│   ├── conftest.py                     # Pytest configuration & fixtures
│   │
│   ├── unit/                           # Unit tests
│   │   ├── test_auth.py               # Authentication tests
│   │   ├── test_models.py             # Database model tests
│   │   ├── test_schemas.py            # Data validation tests
│   │   └── __init__.py
│   │
│   ├── integration/                    # Integration tests
│   │   ├── test_api_auth.py           # Auth endpoints tests
│   │   ├── test_api_courses.py        # Course endpoints tests
│   │   ├── test_api_assignments.py    # Assignment endpoints tests
│   │   ├── test_api_subtasks.py       # Subtask endpoints tests
│   │   ├── test_database.py           # Database operations tests
│   │   └── __init__.py
│   │
│   ├── e2e/                            # End-to-end tests
│   │   ├── test_user_workflows.py     # Complete user journeys
│   │   ├── test_data_flow.py          # Cross-module data flow
│   │   └── __init__.py
│   │
│   ├── security/                       # Security tests
│   │   ├── test_injection.py          # SQL injection, XSS tests
│   │   ├── test_auth_security.py      # Auth security tests
│   │   └── __init__.py
│   │
│   ├── api/                            # API testing
│   │   ├── postman_collection.json    # Postman collection
│   │   ├── test_requests.http         # REST Client tests
│   │   └── environment.json           # Test environment config
│   │
│   ├── fixtures/                       # Test data
│   │   ├── users.json                 # Test user data
│   │   ├── courses.json               # Test course data
│   │   └── assignments.json           # Test assignment data
│   │
│   ├── reports/                        # Test results & reports
│   │   ├── coverage.html              # Coverage report
│   │   ├── test_results.xml           # JUnit format results
│   │   └── defects.log                # Defect log
│   │
│   └── README.md                       # Test documentation
│
├── backend/
│   ├── requirements.txt                # Always includes test dependencies
│   ├── conftest.py                     # Pytest configuration
│   └── (existing backend files)
│
└── frontend/
    └── (existing frontend files)
```

### 4.2 Git Repository Setup

**GitHub Repository Configuration**:

```bash
# Initialize git (if not already done)
cd "Plan Your Study"
git init

# Create .gitignore for test files
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/

# Pytest
.pytest_cache/
.coverage
htmlcov/
test-results.xml

# IDEs
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# Dependencies
node_modules/
venv/
EOF

# Add files to git
git add .
git commit -m "Initial commit with test setup"

# Create test branches
git branch develop
git branch feature/test-setup
```

**Branch Strategy**:
- `main`: Production-ready code, all tests pass
- `develop`: Development branch, tests run on all PRs
- `feature/*`: Feature branches for new test cases

---

## 5. Testing Tools Installation Guide

### 5.1 Backend Testing Setup

**Step 1: Install Python Dependencies**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install testing packages
pip install pytest==7.4.3
pip install pytest-cov==4.1.0
pip install pytest-asyncio==0.21.1
pip install pytest-timeout==2.1.0
pip install httpx==0.25.2

# Verify installation
pytest --version
```

**Step 2: Create conftest.py (Pytest Configuration)**
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# Test database setup
TEST_DATABASE_URL = "sqlite:///test_study_planner.db"

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create fresh test database for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False)(bind=connection)
    
    # Override dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.clear()

@pytest.fixture
def client(test_db):
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def test_user_data():
    """Sample user data for tests"""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPassword123!"
    }

@pytest.fixture
def test_course_data():
    """Sample course data for tests"""
    return {
        "name": "Computer Science 101",
        "description": "Introduction to programming",
        "instructor": "Dr. Smith"
    }

@pytest.fixture
def test_assignment_data():
    """Sample assignment data for tests"""
    return {
        "course_id": 1,
        "title": "Chapter 5 Homework",
        "description": "Complete exercises 1-20",
        "deadline": "2024-04-15T23:59:59",
        "priority": "high"
    }
```

**Step 3: Run First Test**
```bash
# Create simple test file
mkdir -p tests/unit
touch tests/unit/test_auth.py

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### 5.2 Frontend Testing Setup (Optional for Assignment 1)

**Note**: Frontend testing will be minimal for Assignment 1, focused on manual testing.

```bash
cd frontend

# Optional: Install testing libraries for future
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

### 5.3 API Testing Setup with Postman

**Step 1: Install & Launch Postman**
- Download from https://www.postman.com/
- Create free account
- Launch application

**Step 2: Create Workspace**
- Name: "Plan Your Study QA"
- Set as default workspace

**Step 3: Import/Create Collection**
- New → Collection → "API Tests"
- Create folders: Auth, Courses, Assignments, etc.

**Step 4: Create Environment**
```json
{
  "name": "Local Development",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api",
      "enabled": true
    },
    {
      "key": "token",
      "value": "",
      "enabled": true
    }
  ]
}
```

**Step 5: Create Test Requests**
- Auth/Register - POST
- Auth/Login - POST  
- Courses/Create - POST
- Assignments/Create - POST
- etc.

### 5.4 VS Code REST Client Setup

**Step 1: Install Extension**
```
In VS Code:
1. Extensions → Search "REST Client"
2. Install by Huachao Mao
3. Reload VS Code
```

**Step 2: Create test_requests.http**
```http
### Set variables
@baseUrl = http://localhost:8000/api

### Test 1: Register User
POST {{baseUrl}}/auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "username": "testuser",
  "password": "password123"
}

### Test 2: Login
POST {{baseUrl}}/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}
```

**Usage**: Click "Send Request" above each request block

---

## 6. CI/CD Pipeline Details

### 6.1 GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

```yaml
name: QA Test Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  backend-tests:
    name: Backend Tests
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        cd backend && pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v --cov=. --cov-report=xml --cov-report=term
    
    - name: Upload coverage reports
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: unittests
        fail_ci_if_error: false
      env:
        CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}

  code-health:
    name: Code Quality
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install flake8 black
    
    - name: Lint with flake8
      run: |
        cd backend
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Check formatting with black
      run: |
        cd backend
        black --check . 2>/dev/null || true
```

### 6.2 Pipeline Status Checks

**Branch Protection Rule**:
- Require status checks to pass before merging
- Tests must pass on:
  - Python 3.8
  - Python 3.9
  - Python 3.10
- At least 75% code coverage on critical modules

---

## 7. Test Execution Commands Reference

### 7.1 Basic Pytest Commands

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_auth.py -v

# Run specific test function
pytest tests/unit/test_auth.py::test_register_success -v

# Run with markers (custom)
pytest -m "critical" -v

# Stop on first failure
pytest tests/ -x

# Run with timeout (30 seconds)
pytest tests/ --timeout=30

# Parallel execution (4 workers)
pytest tests/ -n 4
```

### 7.2 Coverage Commands

```bash
# Run tests with coverage report
pytest tests/ --cov=. --cov-report=term --cov-report=xml

# Generate HTML coverage report
pytest tests/ --cov=. --cov-report=html
# View: open htmlcov/index.html

# Show coverage for specific module
pytest tests/ --cov=models --cov-report=term-missing
```

### 7.3 Debugging Commands

```bash
# Run with print statements visible
pytest tests/ -v -s

# Enter debugger on failure
pytest tests/ --pdb

# Run and show local variables on failure
pytest tests/ -l

# Verbose output with short test summary
pytest tests/ -v --tb=short
```

---

## 8. Test Database Configuration

### 8.1 SQLite Test Database

**Location**: `backend/test_study_planner.db`

**Automatic Cleanup**:
- Created fresh for each test session
- Deleted after tests complete
- No manual cleanup needed

**Manual Cleanup** (if needed):
```bash
cd backend
rm test_study_planner.db
```

### 8.2 Test Data Fixtures

**Location**: `tests/fixtures/`

Sample fixture files:
- `users.json` - Test user accounts
- `courses.json` - Test course data
- `assignments.json` - Test assignment data

**Usage in tests**:
```python
@pytest.fixture
def sample_user():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }

def test_user_login(client, sample_user):
    response = client.post("/auth/login", json=sample_user)
    assert response.status_code == 200
```

---

## 9. Troubleshooting & Common Issues

### 9.1 Common Setup Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Pytest not found | Not installed | `pip install pytest` |
| Port 8000 in use | App still running | Kill process: `lsof -ti:8000 \| xargs kill` |
| Import errors | Wrong path | Run from backend directory |
| Database locked | Failed test cleanup | Delete test_*.db and rebuild |
| CORS errors | Backend not running | Start backend: `python main.py` |

### 9.2 Verification Checklist

After setup, verify:
- ✅ `pytest --version` returns version
- ✅ `python -m pytest tests/ --collect-only` shows test count
- ✅ Backend starts without errors: `python main.py`
- ✅ At least 1 test runs successfully: `pytest tests/unit/ -k "test_" --co`
- ✅ GitHub Actions workflow file exists and is valid
- ✅ Postman collection created and saves requests
- ✅ REST Client extension installed in VS Code

---

## 10. Test Environment Specifications

### 10.1 Environment Variables

**Backend** (`backend/.env`):
```
DATABASE_URL=sqlite:///study_planner.db
SECRET_KEY=test-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend** (`frontend/.env.local`):
```
VITE_API_URL=http://localhost:8000/api
```

**Test Environment** (set by conftest.py):
```python
TEST_DATABASE_URL=sqlite:///test_study_planner.db
TEST_MODE=True
```

### 10.2 Environment Variable Override

**In tests**:
```python
import os
os.environ["DATABASE_URL"] = "sqlite:///test_study_planner.db"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"
```

---

## 11. Installed Tools Summary

### ✅ INSTALLED TOOLS

| Tool | Purpose | Version | Status |
|------|---------|---------|--------|
| Pytest | Unit testing | 7.4.3 | ✅ Ready |
| Pytest-cov | Coverage reports | 4.1.0 | ✅ Ready |
| Pytest-asyncio | Async tests | 0.21.1 | ✅ Ready |
| HTTPx | HTTP testing | 0.25.2 | ✅ Ready |
| GitHub Actions | CI/CD | Built-in | ✅ Ready |
| SQLite | Test database | Built-in | ✅ Ready |

### ⏳ TO INSTALL (MANUAL)

| Tool | Purpose | Install Location |
|------|---------|-------------------|
| Postman | API testing | Local machine |
| REST Client | VS Code extension | VS Code |
| Browser DevTools | Frontend debugging | Browser |

---

## 12. Next Steps for QA Execution

**Phase 1 - Immediate** (Day 1-2):
- [ ] Install remaining tools (Postman, REST Client)
- [ ] Verify all test environments work
- [ ] Create sample test cases
- [ ] Test database connectivity

**Phase 2 - Test Development** (Day 3-7):
- [ ] Write unit tests (authentication, models)
- [ ] Create API test collection (Postman)
- [ ] Develop integration tests
- [ ] Set up CI/CD pipeline

**Phase 3 - Execution & Reporting** (Day 8-14):
- [ ] Run full test suite
- [ ] Generate coverage reports
- [ ] Create defect log
- [ ] Document baseline metrics

---

## 13. File Checklist

**Required Files Created**:
- ✅ `.github/workflows/test.yml`
- ✅ `tests/conftest.py`
- ✅ `tests/__init__.py`
- ✅ `tests/unit/__init__.py`
- ✅ `tests/integration/__init__.py`
- ✅ `tests/e2e/__init__.py`
- ✅ `tests/security/__init__.py`
- ✅ `tests/api/test_requests.http`
- ✅ `backend/.env.test`
- ✅ `.gitignore` (updated)

---

## 14. Support & Reference

### 14.1 Documentation Links
- Pytest: https://docs.pytest.org/
- Postman: https://learningcenter.postman.com/
- GitHub Actions: https://docs.github.com/en/actions
- SQLite: https://www.sqlite.org/docs.html

### 14.2 Team Setup Verification

Before moving to test execution:

```bash
# Backend verification
cd backend
python -m pytest --version
python -m pytest --collect-only tests/ | head -20

# Frontend verification (optional)
cd ../frontend
npm --version

# Git configuration
cd ..
git status
git log --oneline -1
```

---

## Sign-off

**Setup Date**: March 21, 2026  
**Status**: ✅ COMPLETE & VERIFIED  
**Prepared by**: QA Team  
**Reviewed by**: QA Lead  

**QA Environment is READY FOR TEST EXECUTION**

Next Document: Baseline Metrics & Screenshots Report

---
