"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user():
    """Test user registration."""
    # Test with valid data - registration now only creates "patient" role
    user_data = {
        "name": "Test Patient",
        "email": "testpatient@example.com",
        "password": "securepassword123",
        "role": "patient"  # Only patient role allowed in registration
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert data["role"] == "patient"  # Should always be patient
    assert "is_active" in data
    assert data["is_active"] is True


def test_register_duplicate_email():
    """Test registration with duplicate email."""
    user_data = {
        "name": "Another Patient",
        "email": "testpatient@example.com",  # Same email as above
        "password": "anotherpassword",
        "role": "patient"
    }
    response = client.post("/auth/register", json=user_data)
    # Should return 400 error
    assert response.status_code == 400
    data = response.json()
    assert "success" in data
    assert data["success"] is False
    assert "error" in data


def test_login_success():
    """Test successful login."""
    login_data = {
        "username": "testpatient@example.com",
        "password": "securepassword123"
    }
    # Note: OAuth2PasswordRequestForm expects form data, not JSON
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    """Test login with wrong password."""
    login_data = {
        "username": "testdoctor@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert "success" in data
    assert data["success"] is False
    assert "error" in data


def test_login_nonexistent_user():
    """Test login with non-existent user."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "somepassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert "success" in data
    assert data["success"] is False
    assert "error" in data


def test_get_current_user_without_token():
    """Test accessing protected endpoint without token."""
    response = client.get("/auth/me")
    assert response.status_code == 401
    data = response.json()
    assert "success" in data
    assert data["success"] is False
    assert "error" in data