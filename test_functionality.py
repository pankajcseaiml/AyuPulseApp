#!/usr/bin/env python3
"""
Quick test of all main functionality
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_registration():
    """Test user registration"""
    print("1. Testing Registration...")
    data = {
        "name": "Test User",
        "username": "testuser2",
        "email": "testuser2@gmail.com",
        "password": "Test@1234"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=data)
    if response.status_code == 200:
        print(f"   [OK] Registration successful")
        return True
    else:
        print(f"   [FAIL] Registration failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_login():
    """Test user login"""
    print("2. Testing Login...")
    data = {
        "username": "testuser@gmail.com",
        "password": "Test@1234"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", data=data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"   [OK] Login successful")
        print(f"   Token: {token[:30]}...")
        return token
    else:
        print(f"   [FAIL] Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_user_info(token):
    """Test getting user info"""
    print("3. Testing User Info...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        print(f"   [OK] User info retrieved")
        print(f"   Name: {user_data.get('name', 'N/A')}")
        print(f"   Email: {user_data.get('email', 'N/A')}")
        return True
    else:
        print(f"   [FAIL] User info failed: {response.status_code}")
        return False

def test_prediction_creation(token):
    """Test creating a prediction"""
    print("4. Testing Prediction Creation...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Clinical data as JSON string
    clinical_data = {
        "age": 45,
        "gender": "M",
        "height": 175,
        "weight": 80,
        "CP": 1,
        "trestbps": 130,
        "chol": 220,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.2,
        "slope": 2,
        "ca": 0,
        "thal": 3
    }
    
    # Create form data with clinical_data as JSON string
    form_data = {
        "clinical_data": json.dumps(clinical_data)
    }
    
    # Add files (optional) - none for this test
    files = {}
    
    response = requests.post(
        f"{BASE_URL}/predictions",
        headers=headers,
        data=form_data,
        files=files
    )
    
    if response.status_code == 200:
        prediction = response.json()
        print(f"   [OK] Prediction created")
        print(f"   ID: {prediction.get('data', {}).get('id', 'N/A')}")
        print(f"   Risk Score: {prediction.get('data', {}).get('risk_score', 'N/A')}")
        return prediction.get('data', {}).get('id')
    else:
        print(f"   [FAIL] Prediction creation failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_prediction_listing(token):
    """Test listing predictions"""
    print("5. Testing Prediction Listing...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/predictions", headers=headers)
    if response.status_code == 200:
        predictions = response.json()
        count = len(predictions.get('data', []))
        print(f"   [OK] Predictions listed ({count} predictions)")
        return True
    else:
        print(f"   [FAIL] Prediction listing failed: {response.status_code}")
        return False

def test_health_endpoints():
    """Test health endpoints"""
    print("6. Testing Health Endpoints...")
    
    # Backend health
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print(f"   [OK] Backend health: OK")
    else:
        print(f"   [FAIL] Backend health: {response.status_code}")
    
    # Frontend (if available)
    try:
        response = requests.get("http://localhost:5173", timeout=2)
        if response.status_code == 200:
            print(f"   [OK] Frontend running: OK")
        else:
            print(f"   [FAIL] Frontend: {response.status_code}")
    except:
        print(f"   [FAIL] Frontend not reachable")

def main():
    print("=" * 60)
    print("Testing All Functionality")
    print("=" * 60)
    
    # Test registration
    test_registration()
    time.sleep(1)
    
    # Test login
    token = test_login()
    if not token:
        print("Login failed, skipping further tests")
        return
    
    time.sleep(1)
    
    # Test user info
    test_user_info(token)
    time.sleep(1)
    
    # Test prediction creation
    pred_id = test_prediction_creation(token)
    time.sleep(1)
    
    # Test prediction listing
    test_prediction_listing(token)
    time.sleep(1)
    
    # Test health endpoints
    test_health_endpoints()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()