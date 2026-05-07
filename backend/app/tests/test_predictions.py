"""
Tests for prediction endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import json

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


def test_create_prediction_with_clinical_data():
    """Test creating a prediction with only clinical data."""
    token = get_auth_token()
    
    clinical_data = {
        "age": 45,
        "gender": "M",
        "CP": 2,
        "trestbps": 130,
        "chol": 240,
        "fbs": 1,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 1,
        "thal": 3
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/predictions", json=clinical_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    prediction = data["data"]
    assert "id" in prediction
    assert "risk_score" in prediction
    assert "risk_category" in prediction
    assert "modalities_used" in prediction
    assert "clinical" in prediction["modalities_used"]
    assert prediction["risk_score"] >= 0
    assert prediction["risk_score"] <= 1


def test_create_prediction_with_invalid_data():
    """Test creating a prediction with invalid clinical data."""
    token = get_auth_token()
    
    # Missing required field
    clinical_data = {
        "age": 45,
        "gender": "M",
        # Missing CP field
        "trestbps": 130,
        "chol": 240
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/predictions", json=clinical_data, headers=headers)
    
    # Should return 422 validation error
    assert response.status_code == 422


def test_list_predictions():
    """Test listing user's predictions."""
    token = get_auth_token()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/predictions", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)


def test_get_prediction_detail():
    """Test getting a specific prediction detail."""
    token = get_auth_token()
    
    # First create a prediction
    clinical_data = {
        "age": 50,
        "gender": "F",
        "CP": 1,
        "trestbps": 120,
        "chol": 200,
        "fbs": 0,
        "restecg": 0,
        "thalach": 160,
        "exang": 0,
        "oldpeak": 0.8,
        "slope": 1,
        "ca": 0,
        "thal": 2
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/predictions", json=clinical_data, headers=headers)
    assert create_response.status_code == 200
    prediction_id = create_response.json()["data"]["id"]
    
    # Now get the prediction detail
    response = client.get(f"/predictions/{prediction_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    prediction = data["data"]
    assert prediction["id"] == prediction_id
    assert "clinical_reference_ranges" in prediction
    assert "shap_values" in prediction
    assert "recommendations" in prediction


def test_get_nonexistent_prediction():
    """Test getting a prediction that doesn't exist."""
    token = get_auth_token()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/predictions/507f1f77bcf86cd799439011", headers=headers)
    
    # Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "success" in data
    assert data["success"] is False


def test_delete_prediction():
    """Test deleting a prediction."""
    token = get_auth_token()
    
    # First create a prediction
    clinical_data = {
        "age": 55,
        "gender": "M",
        "CP": 3,
        "trestbps": 140,
        "chol": 260,
        "fbs": 1,
        "restecg": 1,
        "thalach": 140,
        "exang": 1,
        "oldpeak": 2.5,
        "slope": 3,
        "ca": 2,
        "thal": 3
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/predictions", json=clinical_data, headers=headers)
    assert create_response.status_code == 200
    prediction_id = create_response.json()["data"]["id"]
    
    # Now delete the prediction
    response = client.delete(f"/predictions/{prediction_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    
    # Verify it's deleted
    get_response = client.get(f"/predictions/{prediction_id}", headers=headers)
    assert get_response.status_code == 404


def test_prediction_stats():
    """Test getting prediction statistics."""
    token = get_auth_token()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/predictions/stats/summary", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    stats = data["data"]
    assert "total_predictions" in stats
    assert "average_risk" in stats
    assert "risk_distribution" in stats