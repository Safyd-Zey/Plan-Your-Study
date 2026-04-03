"""
Pytest configuration and fixtures for Plan Your Study application
"""
import pytest
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


# Test database configuration
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine for the session"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables after session
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db(test_engine):
    """Create a fresh test database for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    
    session = sessionmaker(autocommit=False, autoflush=False)(bind=connection)

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
    """Create FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def test_user_data():
    """Sample user data for tests"""
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "TestPassword123!"
    }


@pytest.fixture
def test_user_data_2():
    """Another test user"""
    return {
        "email": "testuser2@example.com",
        "username": "testuser2",
        "password": "TestPassword456!"
    }


@pytest.fixture
def test_course_data():
    """Sample course data for tests"""
    return {
        "name": "Introduction to Python",
        "description": "Learn Python basics",
        "instructor": "Dr. Smith"
    }


@pytest.fixture
def test_assignment_data():
    """Sample assignment data for tests"""
    return {
        "title": "Chapter 5 Exercises",
        "description": "Complete all exercises from chapter 5",
        "deadline": "2024-04-15T23:59:59",
        "priority": "high"
    }


@pytest.fixture
def test_subtask_data():
    """Sample subtask data for tests"""
    return {
        "title": "Read Chapter 5",
        "description": "Read chapter 5 thoroughly",
        "status": "not_started"
    }


@pytest.fixture
def authenticated_user(client, test_user_data):
    """Create and authenticate a user, return client with token"""
    # Register user
    client.post("/api/auth/register", json=test_user_data)
    
    # Login user
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Add token to client headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client, token


@pytest.fixture
def authenticated_user_2(test_db, test_user_data_2):
    """Create and authenticate a second user"""
    client = TestClient(app)

    # Register user
    client.post("/api/auth/register", json=test_user_data_2)
    
    # Login user
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": test_user_data_2["email"],
            "password": test_user_data_2["password"]
        }
    )
    
    token = login_response.json()["access_token"]
    
    # Add token to client headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    
    return client, token
