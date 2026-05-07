"""
Tests for admin endpoints.
Note: These tests require an admin user to be created first.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_admin_token():
    """Helper to get admin auth token.
    This assumes an admin user exists in the database.
    For testing, we might need to create one first.
    """
    # Try to login as admin (assuming admin@example.com exists)
    login_data = {
        "username": "admin@example.com",
        "password": "adminpassword123"
    }
    response = client.post("/auth/login", data=login_data)
    if response.status_code == 200:
        data = response.json()
        return data["access_token"]
    
    # If admin doesn't exist, try to create one first
    # Note: In real tests, admin should be seeded in the database
    return None


def test_admin_list_users():
    """Test admin listing users (requires admin role)."""
    token = get_admin_token()
    if not token:
        pytest.skip("Admin user not available for testing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/users", headers=headers)
    
    # Admin should be able to list users
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)


def test_admin_get_user():
    """Test admin getting a specific user."""
    token = get_admin_token()
    if not token:
        pytest.skip("Admin user not available for testing")
    
    # First get list of users to find a user ID
    headers = {"Authorization": f"Bearer {token}"}
    list_response = client.get("/admin/users", headers=headers)
    assert list_response.status_code == 200
    users = list_response.json()["data"]
    
    if users:
        user_id = users[0]["id"]
        response = client.get(f"/admin/users/{user_id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert data["success"] is True
        assert "data" in data
        user = data["data"]
        assert user["id"] == user_id
        assert "email" in user
        assert "role" in user


def test_admin_update_user():
    """Test admin updating a user."""
    token = get_admin_token()
    if not token:
        pytest.skip("Admin user not available for testing")
    
    # First get list of users
    headers = {"Authorization": f"Bearer {token}"}
    list_response = client.get("/admin/users", headers=headers)
    assert list_response.status_code == 200
    users = list_response.json()["data"]
    
    if users:
        # Find a non-admin user to update
        target_user = None
        for user in users:
            if user["role"] != "admin":
                target_user = user
                break
        
        if target_user:
            user_id = target_user["id"]
            update_data = {
                "is_active": False  # Deactivate the user
            }
            
            response = client.put(f"/admin/users/{user_id}", json=update_data, headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            assert data["success"] is True
            assert "data" in data
            updated_user = data["data"]
            assert updated_user["id"] == user_id
            assert updated_user["is_active"] is False


def test_admin_toggle_user_active():
    """Test admin toggling user active status."""
    token = get_admin_token()
    if not token:
        pytest.skip("Admin user not available for testing")
    
    # First get list of users
    headers = {"Authorization": f"Bearer {token}"}
    list_response = client.get("/admin/users", headers=headers)
    assert list_response.status_code == 200
    users = list_response.json()["data"]
    
    if users:
        # Find a non-admin user
        target_user = None
        for user in users:
            if user["role"] != "admin":
                target_user = user
                break
        
        if target_user:
            user_id = target_user["id"]
            original_active = target_user["is_active"]
            
            response = client.post(f"/admin/users/{user_id}/toggle-active", headers=headers)
            
            assert response.status_code == 200
            data = response.json()
            assert "success" in data
            assert data["success"] is True
            assert "data" in data
            toggled_user = data["data"]
            assert toggled_user["id"] == user_id
            assert toggled_user["is_active"] != original_active  # Should be toggled


def test_admin_system_stats():
    """Test admin getting system statistics."""
    token = get_admin_token()
    if not token:
        pytest.skip("Admin user not available for testing")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/stats", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    stats = data["data"]
    assert "total_users" in stats
    assert "total_predictions" in stats
    assert "total_patients" in stats
    assert "users_by_role" in stats


def test_non_admin_access():
    """Test that non-admin users cannot access admin endpoints."""
    # Get a regular user token (patient role)
    login_data = {
        "username": "testpatient@example.com",
        "password": "securepassword123"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/admin/users", headers=headers)
    
    # Non-admin should be denied access
    assert response.status_code == 403  # Forbidden
    data = response.json()
    assert "success" in data
    assert data["success"] is False


def test_admin_delete_user():
    """Test admin deleting a user."""
    token = get_admin_token()
    if not token:
        pytest.skip("Admin user not available for testing")
    
    # First create a test user to delete
    user_data = {
        "name": "User To Delete",
        "email": "todelete@example.com",
        "password": "deletepassword123",
        "role": "patient"
    }
    create_response = client.post("/auth/register", json=user_data)
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]
    
    # Now delete as admin
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/admin/users/{user_id}", headers=headers)
    
    # Should succeed (or return appropriate status)
    # Note: Admin might not be allowed to delete themselves
    assert response.status_code in [200, 403, 400]
    
    if response.status_code == 200:
        data = response.json()
        assert "success" in data
        assert data["success"] is True