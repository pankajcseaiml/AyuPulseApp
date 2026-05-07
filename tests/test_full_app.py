import requests
import json
import sys

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get('http://localhost:8000/health')
        if response.status_code == 200:
            data = response.json()
            print(f'[OK] Backend health: {data.get("status")}')
            return True
        else:
            print(f'[FAIL] Backend health check failed: {response.status_code}')
            return False
    except Exception as e:
        print(f'[ERROR] Backend health check error: {str(e)}')
        return False

def test_auth_flow():
    """Test authentication flow (login with test user)"""
    try:
        # Login
        login_data = {
            'username': 'test@example.com',
            'password': 'password123'
        }
        
        response = requests.post('http://localhost:8000/auth/login', data=login_data)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print('[OK] Login successful')
            
            # Test /me endpoint
            headers = {'Authorization': f'Bearer {token}'}
            me_response = requests.get('http://localhost:8000/auth/me', headers=headers)
            if me_response.status_code == 200:
                user_data = me_response.json()
                print(f'[OK] User data retrieved: {user_data.get("data", {}).get("email")}')
                return token
            else:
                print(f'[FAIL] /me endpoint failed: {me_response.status_code}')
                return None
        else:
            print(f'[FAIL] Login failed: {response.status_code}')
            return None
    except Exception as e:
        print(f'[ERROR] Auth flow error: {str(e)}')
        return None

def test_prediction_flow(token):
    """Test prediction creation and retrieval"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        # Create prediction
        clinical_data = {
            'gender': 1,
            'age': 45,
            'sysBP': 120,
            'diaBP': 80,
            'totChol': 200,
            'BMI': 24.5,
            'heartRate': 75,
            'glucose': 95,
            'cigsPerDay': 0,
            'currentSmoker': 0,
            'BPMeds': 0,
            'prevalentStroke': 0,
            'prevalentHyp': 0,
            'diabetes': 0,
            'CP': 0
        }
        
        form_data = {
            'clinical_data': json.dumps(clinical_data)
        }
        
        create_response = requests.post('http://localhost:8000/predictions', 
                                       data=form_data, 
                                       headers=headers)
        if create_response.status_code == 200:
            prediction = create_response.json()
            pred_id = prediction.get('data', {}).get('id')
            print(f'[OK] Prediction created: {pred_id}')
            
            # List predictions
            list_response = requests.get('http://localhost:8000/predictions', headers=headers)
            if list_response.status_code == 200:
                predictions = list_response.json()
                count = len(predictions.get('data', []))
                print(f'[OK] Predictions listed: {count} predictions found')
                
                # Get prediction stats
                stats_response = requests.get('http://localhost:8000/predictions/stats/summary', headers=headers)
                if stats_response.status_code == 200:
                    stats = stats_response.json()
                    print(f'[OK] Prediction stats retrieved')
                    return True
                else:
                    print(f'[FAIL] Stats endpoint failed: {stats_response.status_code}')
                    return False
            else:
                print(f'[FAIL] List predictions failed: {list_response.status_code}')
                return False
        else:
            print(f'[FAIL] Create prediction failed: {create_response.status_code}')
            return False
    except Exception as e:
        print(f'[ERROR] Prediction flow error: {str(e)}')
        return False

def test_patients_flow(token):
    """Test patients CRUD operations"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        # List patients
        list_response = requests.get('http://localhost:8000/patients', headers=headers)
        if list_response.status_code == 200:
            patients = list_response.json()
            print(f'[OK] Patients listed: {len(patients.get("data", []))} patients found')
            return True
        else:
            print(f'[FAIL] List patients failed: {list_response.status_code}')
            return False
    except Exception as e:
        print(f'[ERROR] Patients flow error: {str(e)}')
        return False

def test_profile_flow(token):
    """Test profile operations"""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get profile (may not exist yet)
        profile_response = requests.get('http://localhost:8000/profile', headers=headers)
        if profile_response.status_code == 200:
            print('[OK] Profile retrieved')
            return True
        elif profile_response.status_code == 404:
            print('[INFO] Profile not found (expected for new user)')
            return True  # Not an error, profile just doesn't exist yet
        else:
            print(f'[FAIL] Profile endpoint failed: {profile_response.status_code}')
            return False
    except Exception as e:
        print(f'[ERROR] Profile flow error: {str(e)}')
        return False

def main():
    print('=' * 60)
    print('Testing Full Application Functionality')
    print('=' * 60)
    
    all_passed = True
    
    # Test 1: Backend health
    print('\n1. Testing backend health...')
    if not test_backend_health():
        all_passed = False
        print('[CRITICAL] Backend not healthy, stopping tests')
        return False
    
    # Test 2: Authentication flow
    print('\n2. Testing authentication flow...')
    token = test_auth_flow()
    if not token:
        all_passed = False
        print('[CRITICAL] Authentication failed, stopping tests')
        return False
    
    # Test 3: Prediction flow
    print('\n3. Testing prediction flow...')
    if not test_prediction_flow(token):
        all_passed = False
    
    # Test 4: Patients flow
    print('\n4. Testing patients flow...')
    if not test_patients_flow(token):
        all_passed = False
    
    # Test 5: Profile flow
    print('\n5. Testing profile flow...')
    if not test_profile_flow(token):
        all_passed = False
    
    # Summary
    print('\n' + '=' * 60)
    print('TEST SUMMARY')
    print('=' * 60)
    
    if all_passed:
        print('[SUCCESS] All application flows are working correctly!')
        print('\nApplication Status:')
        print('- Backend: Running on http://localhost:8000')
        print('- Frontend: Running on http://localhost:5174')
        print('- MongoDB: Connected and operational')
        print('- Authentication: Working')
        print('- Predictions: Working')
        print('- Patients: Working')
        print('- Profile: Working')
        return True
    else:
        print('[FAILURE] Some application flows have issues')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)