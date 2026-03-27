"""
Unit tests for authentication module
"""
import pytest
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_password_hashing():
    """Test password hashing works correctly"""
    password = "TestPassword123!"
    hashed = pwd_context.hash(password)
    
    # Verify hashed password is different from original
    assert hashed != password
    
    # Verify password can be verified
    assert pwd_context.verify(password, hashed)


def test_password_verification_fails_with_wrong_password():
    """Test that wrong password doesn't verify"""
    password = "TestPassword123!"
    wrong_password = "WrongPassword123!"
    
    hashed = pwd_context.hash(password)
    
    # Wrong password should fail verification
    assert not pwd_context.verify(wrong_password, hashed)


def test_user_registration_payload(test_user_data):
    """Test user registration data structure"""
    assert "email" in test_user_data
    assert "username" in test_user_data
    assert "password" in test_user_data
    
    # Validate email
    assert "@" in test_user_data["email"]
    
    # Validate password strength
    assert len(test_user_data["password"]) >= 8


def test_course_data_validation(test_course_data):
    """Test course data structure"""
    assert "name" in test_course_data
    assert "description" in test_course_data
    assert "instructor" in test_course_data
    
    assert len(test_course_data["name"]) > 0


def test_assignment_data_validation(test_assignment_data):
    """Test assignment data structure"""
    assert "title" in test_assignment_data
    assert "description" in test_assignment_data
    assert "deadline" in test_assignment_data
    assert "priority" in test_assignment_data
    
    # Validate priority is valid
    assert test_assignment_data["priority"] in ["low", "medium", "high"]
