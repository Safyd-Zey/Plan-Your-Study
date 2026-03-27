# Project Testing Guide

## API Testing

### Using Swagger UI (Recommended for Beginners)

1. Start the backend server
2. Visit `http://localhost:8000/docs`
3. All endpoints listed with interactive testing

### Manual API Testing

Use tools like Postman, cURL, or VS Code REST Client

#### Authentication Endpoints

**Register User:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Get Current User:**
```bash
curl "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### Course Endpoints

**Create Course:**
```bash
curl -X POST "http://localhost:8000/api/courses/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mathematics 101",
    "description": "Basics of calculus",
    "instructor": "Dr. Smith"
  }'
```

**Get All Courses:**
```bash
curl "http://localhost:8000/api/courses/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Assignment Endpoints

**Create Assignment:**
```bash
curl -X POST "http://localhost:8000/api/assignments/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "title": "Chapter 5 Homework",
    "description": "Complete exercises 1-20",
    "deadline": "2024-04-15T23:59:59",
    "priority": "high",
    "status": "not_started"
  }'
```

**Get All Assignments:**
```bash
curl "http://localhost:8000/api/assignments/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Progress Endpoints

**Get Progress Stats:**
```bash
curl "http://localhost:8000/api/progress/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Schedule Endpoints

**Get Weekly Schedule:**
```bash
curl "http://localhost:8000/api/schedule/weekly?start_date=2024-04-01" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Frontend Testing

### Test User Flow

1. **Registration**
   - Go to `http://localhost:3000/register`
   - Create new account
   - Verify redirected to dashboard

2. **Dashboard**
   - View overall statistics
   - Check upcoming assignments
   - Verify progress percentage

3. **Courses**
   - Create new course
   - Add multiple courses
   - Edit course details
   - Delete course

4. **Assignments**
   - Create assignment for each course
   - Set different priorities
   - Add subtasks
   - Mark subtasks as complete
   - Update assignment status

5. **Schedule**
   - View weekly calendar
   - Navigate between weeks
   - See all assignments and sessions

6. **Progress**
   - Check completion stats
   - Review upcoming deadlines
   - Verify percentages

## Automated Testing

### Backend Tests (Optional)

Create `test_main.py`:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login():
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200

def test_get_courses():
    response = client.get("/api/courses/")
    assert response.status_code == 401  # Without token
```

Run tests:
```bash
pytest test_main.py -v
```

## Performance Testing

### Load Testing with Apache Bench

```bash
# Test API response time
ab -n 100 -c 10 -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/progress/stats
```

### Response Time Checks

- API endpoints should respond in <1 second
- Frontend should load in <2 seconds
- Database queries should complete in <100ms

## Browser Testing

### Browsers to Test
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Responsive Design Testing

1. Desktop (1920x1080)
2. Tablet (768x1024)
3. Mobile (375x667)

Use Chrome DevTools:
- F12 → Device Toolbar → Test different devices

### Browser Console

Check for errors:
- F12 → Console tab
- Verify no red error messages
- Check network tab for API calls

## Security Testing

### Password Requirements
- Accept any password for now
- Test with special characters
- Test with long passwords

### Token Validation
- Invalid token should return 401
- Expired token should return 401
- No token should return 401

### Data Isolation
- User A should not see User B's data
- Delete User A's data, User B's data remains
- Verify user_id in all database queries

## Known Test Cases

### Happy Path

1. Register → Login → Dashboard → Create Course → Create Assignment with Subtasks → View Schedule → Check Progress

2. Multiple courses with mixed priority assignments

3. All subtasks marked complete → Assignment status complete

### Edge Cases

1. Empty database (no courses/assignments)
2. Very long assignment titles
3. Deadline in past
4. Multiple subtasks on one assignment
5. Rapid API calls

## Debugging

### Browser DevTools

**Network Tab:**
- Monitor all API requests
- Check response status codes
- View response payloads
- Identify slow requests

**Console Tab:**
- Check for JavaScript errors
- Use `console.log()` for debugging
- Check Redux/Zustand store state

**Storage Tab:**
- View localStorage (token, user data)
- Verify session data

### Backend Debugging

**Add Print Statements:**
```python
@router.get("/")
def get_items():
    print("Getting items...")
    items = db.query(Item).all()
    print(f"Found {len(items)} items")
    return items
```

**Check Database:**
```bash
# View SQLite database
sqlite3 study_planner.db

# View tables
.tables

# Query data
SELECT * FROM users;
SELECT * FROM assignments WHERE user_id=1;
```

## Test Data

### Sample User Account
- Email: `test@example.com`
- Username: `testuser`
- Password: `password123`

### Sample Course
- Name: `Computer Science 101`
- Instructor: `Prof. Johnson`
- Description: `Introduction to programming`

### Sample Assignments
1. Lists and Arrays - High Priority - Due Today
2. Functions - Medium Priority - Due Tomorrow
3. OOP Concepts - Low Priority - Due Next Week

## Checklist Before Deployment

- [ ] All CRUD operations working
- [ ] Authentication working (register, login, logout)
- [ ] User data isolation verified
- [ ] No console errors in browser
- [ ] API responses within 1 second
- [ ] Frontend loads within 2 seconds
- [ ] Responsive design tested on 3+ devices
- [ ] Database resets properly
- [ ] All features from requirements working

## Test Results Template

```
Testing Session: [Date]
Tester: [Name]
Environment: Windows/Mac/Linux | Chrome 120

Test Cases Passed: 25/25
Test Cases Failed: 0/25
Blockers: None
Issues Found: None

Sign off: ___________
```

## Common Test Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Cannot connect to API" | Check backend is running on 8000 |
| "Token invalid" | Register new user and login fresh |
| "Data not saving" | Check backend console for errors |
| "UI not responsive" | Clear browser cache, reload |
| "API slow" | Check database, optimize queries |

## Performance Benchmarks

Target metrics:
- API response: <1000ms (target: <200ms)
- Page load: <2000ms (target: <1000ms)
- Database query: <100ms
- Screenshot on mobile: <3000ms
- Build time: <1 minute

---

**Run tests regularly during development to catch issues early!**
