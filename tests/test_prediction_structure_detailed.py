import requests
import json

def test_prediction_structure_detailed():
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
        
        # Get first prediction
        headers = {'Authorization': f'Bearer {token}'}
        list_response = requests.get('http://localhost:8000/predictions', headers=headers)
        
        if list_response.status_code != 200:
            print(f'List failed: {list_response.text}')
            return
            
        predictions = list_response.json()
        data = predictions.get('data', [])
        if not data:
            print('No predictions found')
            return
            
        first_id = data[0].get('id')
        print(f'\nFetching prediction {first_id}...')
        detail_response = requests.get(f'http://localhost:8000/predictions/{first_id}', headers=headers)
        
        if detail_response.status_code != 200:
            print(f'Detail failed: {detail_response.text}')
            return
            
        prediction = detail_response.json()
        pred_data = prediction.get('data', {})
        
        print('\n=== clinical_reference_ranges detailed structure ===')
        ref_ranges = pred_data.get('clinical_reference_ranges', [])
        print(f'Type: {type(ref_ranges)}')
        print(f'Length: {len(ref_ranges)}')
        
        if ref_ranges and len(ref_ranges) > 0:
            print('\nFirst item:')
            first_item = ref_ranges[0]
            print(json.dumps(first_item, indent=2))
            
            # Check required fields
            required_fields = ['parameter', 'value', 'unit', 'reference_range', 'status']
            missing = [f for f in required_fields if f not in first_item]
            if missing:
                print(f'\n[ERROR] Missing fields: {missing}')
            else:
                print(f'\n[OK] All required fields present')
                
            # Check all items
            print(f'\nAll parameters:')
            for i, item in enumerate(ref_ranges):
                print(f'  {i+1}. {item.get("parameter")}: {item.get("value")} {item.get("unit")} - {item.get("status")}')
        
        # Check if frontend will be able to render
        print('\n=== Frontend compatibility check ===')
        issues = []
        
        # Check that clinical_reference_ranges is a list (not dict)
        if not isinstance(ref_ranges, list):
            issues.append(f'clinical_reference_ranges is {type(ref_ranges)}, expected list')
        
        # Check that each item has the required fields
        for i, item in enumerate(ref_ranges):
            if not isinstance(item, dict):
                issues.append(f'Item {i} is {type(item)}, expected dict')
                continue
                
            for field in ['parameter', 'value', 'unit', 'reference_range', 'status']:
                if field not in item:
                    issues.append(f'Item {i} missing field: {field}')
        
        if issues:
            print(f'[FAIL] Issues found:')
            for issue in issues:
                print(f'  - {issue}')
        else:
            print('[OK] Frontend should be able to render this data')
            
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    test_prediction_structure_detailed()