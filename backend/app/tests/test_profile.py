"""
Tests for profile endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_token(email="testpatient@example.com", password="securepassword123"):
    """Helper to get auth token."""
    login_data = {
        "username": email,
        "password": password
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


def test_create_profile():
    """Test creating a user profile."""
    token = get_auth_token()
    
    profile_data = {
        "age": 35,
        "gender": "M",
        "height": 175,
        "weight": 70,
        "blood_group": "O+",
        "phone": "+1234567890",
        "address": "123 Main St, City",
        "emergency_contact": "+0987654321",
        "lifestyle": {
            "exercise_frequency": "moderate",
            "diet_type": "balanced",
            "smoking": False,
            "alcohol": "occasional",
            "sleep_hours": 7,
            "stress_level": "medium"
        },
        "medical_history": {
            "diabetes": False,
            "hypertension": False,
            "cholesterol": False,
            "family_history": True,
            "previous_heart_issues": False,
            "medications": ["Aspirin"],
            "allergies": ["Penicillin"]
        }
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/profile", json=profile_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    profile = data["data"]
    assert profile["age"] == 35
    assert profile["gender"] == "M"
    assert profile["height"] == 175
    assert profile["weight"] == 70
    assert profile["blood_group"] == "O+"
    assert "bmi" in profile
    assert profile["bmi"] == round(70 / ((175/100) ** 2), 1)


def test_get_profile():
    """Test getting user profile."""
    token = get_auth_token()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/profile", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    profile = data["data"]
    assert "age" in profile
    assert "gender" in profile
    assert "height" in profile
    assert "weight" in profile
    assert "bmi" in profile


def test_update_profile():
    """Test updating user profile."""
    token = get_auth_token()
    
    # First get current profile
    headers = {"Authorization": f"Bearer {token}"}
    get_response = client.get("/profile", headers=headers)
    assert get_response.status_code == 200
    
    # Update with new data
    update_data = {
        "age": 36,  # Updated age
        "weight": 72,  # Updated weight
        "lifestyle": {
            "exercise_frequency": "high",
            "diet_type": "vegetarian",
            "smoking": False,
            "alcohol": "none",
            "sleep_hours": 8,
            "stress_level": "low"
        }
    }
    
    response = client.put("/profile", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    profile = data["data"]
    assert profile["age"] == 36
    assert profile["weight"] == 72
    assert profile["lifestyle"]["exercise_frequency"] == "high"
    assert profile["lifestyle"]["diet_type"] == "vegetarian"


def test_profile_with_invalid_data():
    """Test creating profile with invalid data."""
    token = get_auth_token()
    
    # Invalid gender
    profile_data = {
        "age": 35,
        "gender": "X",  # Invalid gender
        "height": 175,
        "weight": 70
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/profile", json=profile_data, headers=headers)
    
    # Should return 422 validation error
    assert response.status_code == 422


def test_profile_bmi_calculation():
    """Test that BMI is calculated correctly."""
    token = get_auth_token()
    
    profile_data = {
        "age": 30,
        "gender": "F",
        "height": 165,
        "weight": 60,
        "blood_group": "A+"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/profile", json=profile_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    profile = data["data"]
    
    # Calculate expected BMI: weight(kg) / (height(m) ^ 2)
    expected_bmi = round(60 / ((165/100) ** 2), 1)
    assert profile["bmi"] == expected_bmi


def test_profile_without_auth():
    """Test accessing profile without authentication."""
    response = client.get("/profile")
    
    # Should return 401 unauthorized
    assert response.status_code == 401
    data = response.json()
    assert "success" in data
    assert data["success"] is False