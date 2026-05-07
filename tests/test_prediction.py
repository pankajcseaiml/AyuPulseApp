import requests
import json
import sys

def test_prediction():
    # First login to get token
    login_data = {
        'username': 'rajsharma@gmail.com',
        'password': 'password123'
    }
    
    try:
        print('Testing login...')
        response = requests.post('http://localhost:8000/auth/login', data=login_data)
        print(f'Login Response Status: {response.status_code}')
        if response.status_code != 200:
            print(f'Login failed: {response.text}')
            return False
        
        token = response.json().get('access_token')
        print('Token obtained successfully')
        
        # Now test prediction endpoint
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
        
        print('\nTesting prediction endpoint...')
        pred_response = requests.post('http://localhost:8000/predictions', 
                                     data=form_data, 
                                     headers=headers)
        print(f'Prediction Response Status: {pred_response.status_code}')
        if pred_response.status_code == 200:
            print('SUCCESS: Prediction created!')
            result = pred_response.json()
            print(f'Prediction ID: {result.get("data", {}).get("id")}')
            print(f'Risk Score: {result.get("data", {}).get("risk_score")}')
            print(f'Risk Category: {result.get("data", {}).get("risk_category")}')
            return True
        else:
            print(f'Prediction failed: {pred_response.text}')
            return False
            
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

if __name__ == '__main__':
    success = test_prediction()
    sys.exit(0 if success else 1)