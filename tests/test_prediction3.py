import requests
import json
import sys

def test_login(email, password):
    """Test login with given credentials"""
    login_data = {
        'username': email,
        'password': password
    }
    
    try:
        response = requests.post('http://localhost:8000/auth/login', data=login_data)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f'[OK] Login successful for {email}')
            return token
        else:
            print(f'[FAIL] Login failed for {email}: {response.status_code} - {response.text}')
            return None
    except Exception as e:
        print(f'[ERROR] Error logging in {email}: {str(e)}')
        return None

def test_prediction_with_token(token):
    """Test prediction endpoint with valid token"""
    headers = {'Authorization': f'Bearer {token}'}
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
    
    try:
        print('\nTesting prediction endpoint...')
        pred_response = requests.post('http://localhost:8000/predictions', 
                                     data=form_data, 
                                     headers=headers)
        print(f'Prediction Response Status: {pred_response.status_code}')
        if pred_response.status_code == 200:
            print('[OK] SUCCESS: Prediction created!')
            result = pred_response.json()
            print(f'  Prediction ID: {result.get("data", {}).get("id")}')
            print(f'  Risk Score: {result.get("data", {}).get("risk_score")}')
            print(f'  Risk Category: {result.get("data", {}).get("risk_category")}')
            return True
        else:
            print(f'[FAIL] Prediction failed: {pred_response.text}')
            return False
    except Exception as e:
        print(f'[ERROR] Error testing prediction: {str(e)}')
        return False

def main():
    # Test with known users from database
    test_cases = [
        # (email, password_to_try)
        ('test@example.com', 'password123'),
        ('test@example.com', 'Password123'),
        ('test@example.com', 'test123'),
        ('testuser@example.com', 'password123'),
        ('testuser@example.com', 'Password123'),
        ('testuser@example.com', 'test123'),
        ('panjob@gmail.com', 'password123'),
        ('panjob@gmail.com', 'Password123'),
        ('panjob@gmail.com', 'panjob123'),
        ('rajsharma@gmail.com', 'password123'),
        ('rajsharma@gmail.com', 'Password123'),
        ('rajsharma@gmail.com', 'raj123'),
    ]
    
    successful_login = None
    token = None
    
    print('Testing login with various credentials...')
    for email, password in test_cases:
        token = test_login(email, password)
        if token:
            successful_login = (email, password)
            break
    
    if not token:
        print('\n[FAIL] No successful login. Cannot test prediction.')
        return False
    
    print(f'\n[OK] Using user: {successful_login[0]}')
    
    # Test prediction
    success = test_prediction_with_token(token)
    
    if success:
        print('\n[OK] Prediction functionality is working!')
        return True
    else:
        print('\n[FAIL] Prediction functionality test failed.')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)