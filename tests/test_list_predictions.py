import requests
import json

def test_list_predictions():
    # First login to get token
    login_data = {
        'username': 'test@example.com',
        'password': 'password123'
    }
    
    try:
        print('Logging in...')
        response = requests.post('http://localhost:8000/auth/login', data=login_data)
        if response.status_code != 200:
            print(f'Login failed: {response.status_code}')
            return
        
        token = response.json().get('access_token')
        print('Login successful')
        
        # List all predictions
        headers = {'Authorization': f'Bearer {token}'}
        
        print('\nListing all predictions...')
        list_response = requests.get('http://localhost:8000/predictions', headers=headers)
        
        print(f'Response Status: {list_response.status_code}')
        if list_response.status_code == 200:
            predictions = list_response.json()
            data = predictions.get('data', [])
            print(f'Found {len(data)} predictions:')
            
            for i, pred in enumerate(data):
                print(f'\n[{i+1}] ID: {pred.get("id")}')
                print(f'    Risk Score: {pred.get("risk_score")}')
                print(f'    Risk Category: {pred.get("risk_category")}')
                print(f'    Created At: {pred.get("created_at")}')
                print(f'    Subject Name: {pred.get("subject_name")}')
                
            if data:
                # Test the first prediction
                first_id = data[0].get('id')
                print(f'\nTesting detail endpoint for first prediction ({first_id})...')
                detail_response = requests.get(f'http://localhost:8000/predictions/{first_id}', headers=headers)
                print(f'Detail Response Status: {detail_response.status_code}')
                if detail_response.status_code == 200:
                    detail = detail_response.json()
                    print('Detail endpoint works!')
                    print(f'Data keys: {list(detail.get("data", {}).keys())}')
                else:
                    print(f'Detail error: {detail_response.text}')
        else:
            print(f'Error: {list_response.text}')
            
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    test_list_predictions()