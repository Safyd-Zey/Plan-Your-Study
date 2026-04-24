"""
Integration tests for API authentication endpoints
"""
import pytest


def test_user_registration_success(client, test_user_data):
    """Test successful user registration"""
    response = client.post("/api/auth/register", json=test_user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]


def test_user_registration_duplicate_email(client, test_user_data):
    """Test registration fails with duplicate email"""
    # Register first user
    client.post("/api/auth/register", json=test_user_data)
    
    # Try to register with same email
    response = client.post("/api/auth/register", json=test_user_data)
    
    # Should fail
    assert response.status_code >= 400


def test_user_login_success(client, test_user_data):
    """Test successful user login"""
    # Register user first
    client.post("/api/auth/register", json=test_user_data)
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_user_login_wrong_password(client, test_user_data):
    """Test login fails with wrong password"""
    # Register user first
    client.post("/api/auth/register", json=test_user_data)
    
    # Login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data["email"],
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401


def test_user_login_nonexistent_email(client):
    """Test login fails with nonexistent email"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password"
        }
    )
    
    assert response.status_code == 401


def test_create_course_authenticated(authenticated_user, test_course_data):
    """Test course creation requires authentication"""
    client, token = authenticated_user
    
    response = client.post('/api/courses', json=test_course_data)
    assert response.status_code == 201
    assert response.json()['name'] == test_course_data['name']


def test_create_course_unauthenticated(client, test_course_data):
    """Test course creation fails without authentication"""
    response = client.post('/api/courses', json=test_course_data)
    assert response.status_code == 401


def test_list_courses_authenticated(authenticated_user, test_course_data):
    """Test listing courses for authenticated user"""
    client, token = authenticated_user
    
    # Create a course
    client.post('/api/courses', json=test_course_data)
    
    response = client.get('/api/courses')
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_list_courses_isolation(authenticated_user, test_course_data):
    """Test courses are isolated between users"""
    client1, token1 = authenticated_user
    # Simulate another user by creating another client (simplified)
    # In real scenario, would need separate authenticated clients
    
    # Create course for user1
    client1.post('/api/courses', json=test_course_data)
    
    response = client1.get('/api/courses')
    assert response.status_code == 200
    # Should only see their own courses
    """Test login fails with wrong password"""
    # Register user
    client.post("/api/auth/register", json=test_user_data)
    
    # Try login with wrong password
    response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data["email"],
            "password": "WrongPassword123!"
        }
    )
    
    assert response.status_code >= 400


def test_get_current_user_authenticated(authenticated_user):
    """Test getting current user when authenticated"""
    client, token = authenticated_user
    
    response = client.get("/api/auth/me")
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data


def test_get_current_user_unauthenticated(client):
    """Test getting current user without authentication"""
    response = client.get("/api/auth/me")
    
    assert response.status_code == 401


def test_create_course_authenticated(authenticated_user, test_course_data):
    """Test creating course as authenticated user"""
    client, token = authenticated_user
    
    response = client.post("/api/courses", json=test_course_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == test_course_data["name"]
    assert "id" in data


def test_create_course_unauthenticated(client, test_course_data):
    """Test creating course without authentication"""
    response = client.post("/api/courses", json=test_course_data)
    
    assert response.status_code == 401


def test_list_courses_authenticated(authenticated_user, test_course_data):
    """Test listing courses as authenticated user"""
    client, token = authenticated_user
    
    # Create a course first
    client.post("/api/courses", json=test_course_data)
    
    # List courses
    response = client.get("/api/courses")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["name"] == test_course_data["name"]


def test_list_courses_isolation(authenticated_user, authenticated_user_2, test_course_data):
    """Test that users only see their own courses"""
    client1, token1 = authenticated_user
    client2, token2 = authenticated_user_2
    
    # User 1 creates a course
    client1.post("/api/courses", json=test_course_data)
    
    # User 2 lists courses (should be empty)
    response = client2.get("/api/courses")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # User 2 shouldn't see User 1's course
