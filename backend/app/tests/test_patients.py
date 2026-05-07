"""
Tests for patient management endpoints.
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


def test_create_patient():
    """Test creating a patient record."""
    token = get_auth_token()
    
    patient_data = {
        "full_name": "John Doe",
        "age": 45,
        "gender": "M",
        "phone": "+1234567890",
        "email": "johndoe@example.com",
        "address": "456 Oak St, City",
        "blood_group": "A+",
        "emergency_contact": "+0987654321",
        "medical_notes": "Patient has family history of heart disease."
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/patients", json=patient_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    patient = data["data"]
    assert patient["full_name"] == "John Doe"
    assert patient["age"] == 45
    assert patient["gender"] == "M"
    assert patient["email"] == "johndoe@example.com"
    assert "id" in patient
    assert "created_by" in patient


def test_list_patients():
    """Test listing patients."""
    token = get_auth_token()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/patients", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)


def test_get_patient_detail():
    """Test getting a specific patient detail."""
    token = get_auth_token()
    
    # First create a patient
    patient_data = {
        "full_name": "Jane Smith",
        "age": 52,
        "gender": "F",
        "phone": "+1122334455",
        "email": "janesmith@example.com",
        "blood_group": "B+"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/patients", json=patient_data, headers=headers)
    assert create_response.status_code == 200
    patient_id = create_response.json()["data"]["id"]
    
    # Now get the patient detail
    response = client.get(f"/patients/{patient_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    patient = data["data"]
    assert patient["id"] == patient_id
    assert patient["full_name"] == "Jane Smith"
    assert patient["age"] == 52
    assert patient["gender"] == "F"


def test_update_patient():
    """Test updating a patient record."""
    token = get_auth_token()
    
    # First create a patient
    patient_data = {
        "full_name": "Robert Johnson",
        "age": 38,
        "gender": "M",
        "phone": "+5566778899",
        "email": "robert@example.com",
        "blood_group": "O+"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/patients", json=patient_data, headers=headers)
    assert create_response.status_code == 200
    patient_id = create_response.json()["data"]["id"]
    
    # Update the patient
    update_data = {
        "age": 39,  # Updated age
        "phone": "+9988776655",  # Updated phone
        "medical_notes": "Updated medical notes after checkup."
    }
    
    response = client.put(f"/patients/{patient_id}", json=update_data, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    patient = data["data"]
    assert patient["age"] == 39
    assert patient["phone"] == "+9988776655"
    assert patient["medical_notes"] == "Updated medical notes after checkup."


def test_delete_patient():
    """Test deleting a patient record."""
    token = get_auth_token()
    
    # First create a patient
    patient_data = {
        "full_name": "Temporary Patient",
        "age": 25,
        "gender": "F",
        "phone": "+1112223333",
        "email": "temp@example.com",
        "blood_group": "AB+"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    create_response = client.post("/patients", json=patient_data, headers=headers)
    assert create_response.status_code == 200
    patient_id = create_response.json()["data"]["id"]
    
    # Delete the patient
    response = client.delete(f"/patients/{patient_id}", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    
    # Verify it's deleted
    get_response = client.get(f"/patients/{patient_id}", headers=headers)
    assert get_response.status_code == 404


def test_get_nonexistent_patient():
    """Test getting a patient that doesn't exist."""
    token = get_auth_token()
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/patients/507f1f77bcf86cd799439011", headers=headers)
    
    # Should return 404
    assert response.status_code == 404
    data = response.json()
    assert "success" in data
    assert data["success"] is False


def test_create_patient_with_invalid_data():
    """Test creating a patient with invalid data."""
    token = get_auth_token()
    
    # Missing required field
    patient_data = {
        "age": 45,
        "gender": "M",
        # Missing full_name
        "phone": "+1234567890"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/patients", json=patient_data, headers=headers)
    
    # Should return 422 validation error
    assert response.status_code == 422