import requests
import json

print("Checking prediction ID 69f720df320421d3af9968d1...")

# First login
login_data = {'username': 'test@example.com', 'password': 'password123'}
print("Logging in...")
try:
    response = requests.post('http://localhost:8000/auth/login', data=login_data)
    print(f"Login response status: {response.status_code}")
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        exit()
    
    token = response.json().get('access_token')
    headers = {'Authorization': f'Bearer {token}'}
    print("Login successful")
    
    # Check the specific ID the user mentioned
    prediction_id = '69f720df320421d3af9968d1'
    print(f"\nChecking prediction ID: {prediction_id}")
    detail_response = requests.get(f'http://localhost:8000/predictions/{prediction_id}', headers=headers)
    
    print(f"Status code: {detail_response.status_code}")
    if detail_response.status_code == 200:
        print("Prediction found!")
        data = detail_response.json().get('data', {})
        print(f"Risk category: {data.get('risk_category')}")
        print(f"Subject name: {data.get('subject_name')}")
        print(f"Clinical reference ranges: {len(data.get('clinical_reference_ranges', []))} items")
    elif detail_response.status_code == 404:
        print("Prediction not found (404) - This explains why frontend shows white screen")
        print("\nAvailable predictions:")
        list_response = requests.get('http://localhost:8000/predictions', headers=headers)
        if list_response.status_code == 200:
            predictions = list_response.json().get('data', [])
            print(f"Total predictions: {len(predictions)}")
            for p in predictions:
                print(f"  - {p['id']}: {p['subject_name']} ({p['risk_category']})")
        else:
            print(f"Failed to list predictions: {list_response.status_code}")
    else:
        print(f"Error: {detail_response.status_code}")
        print(detail_response.text)
        
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()