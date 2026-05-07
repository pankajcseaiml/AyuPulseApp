import requests
import json

def test_prediction_structure():
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
        
        print('\n=== Checking ResultsPage required fields ===')
        
        # Fields accessed in ResultsPage
        fields_to_check = [
            ('risk_category', 'string', 'Line 38-44, 74, 86-87'),
            ('risk_score', 'number', 'Line 115, 117'),
            ('subject_name', 'string', 'Line 79'),
            ('confidence', 'number', 'Line 99'),
            ('explanation_text', 'string', 'Line 92'),
            ('modalities_used', 'list', 'Line 104-106'),
            ('recommendations', 'list', 'Line 177-182'),
            ('shap_features', 'list', 'Line 132'),
            ('clinical_reference_ranges', 'list', 'Line 149-163'),
            ('created_at', 'string', 'Line 80'),
        ]
        
        all_present = True
        for field, expected_type, location in fields_to_check:
            value = pred_data.get(field)
            if value is None:
                print(f'[MISSING] {field} (used at {location})')
                all_present = False
            else:
                actual_type = type(value).__name__
                if expected_type == 'list' and isinstance(value, list):
                    print(f'[OK] {field}: list with {len(value)} items')
                elif expected_type == 'number' and isinstance(value, (int, float)):
                    print(f'[OK] {field}: {value} (number)')
                elif expected_type == 'string' and isinstance(value, str):
                    print(f'[OK] {field}: "{value[:50]}{"..." if len(value) > 50 else ""}"')
                else:
                    print(f'[WARN] {field}: type {actual_type}, expected {expected_type}')
        
        # Check specific structures
        print('\n=== Checking nested structures ===')
        
        # Check shap_features structure
        shap_features = pred_data.get('shap_features', [])
        if shap_features:
            print(f'shap_features: {len(shap_features)} items')
            if shap_features and isinstance(shap_features[0], dict):
                print(f'  First item keys: {list(shap_features[0].keys())}')
        else:
            print('[MISSING] shap_features is empty or missing')
            
        # Check clinical_reference_ranges structure
        ref_ranges = pred_data.get('clinical_reference_ranges', [])
        if ref_ranges:
            print(f'clinical_reference_ranges: {len(ref_ranges)} items')
            if ref_ranges and isinstance(ref_ranges[0], dict):
                print(f'  First item keys: {list(ref_ranges[0].keys())}')
                
                # Check for required fields in reference ranges
                required_ref_fields = ['parameter', 'value', 'unit', 'reference_range', 'status']
                first_ref = ref_ranges[0]
                missing = [f for f in required_ref_fields if f not in first_ref]
                if missing:
                    print(f'  [MISSING] Missing fields in reference range: {missing}')
                else:
                    print(f'  [OK] All required fields present')
        else:
            print('[MISSING] clinical_reference_ranges is empty or missing')
            
        # Check recommendations
        recommendations = pred_data.get('recommendations', [])
        if recommendations:
            print(f'recommendations: {len(recommendations)} items')
            print(f'  First: "{recommendations[0][:80]}{"..." if len(recommendations[0]) > 80 else ""}"')
        else:
            print('[MISSING] recommendations is empty or missing')
            
        # Check modalities_used
        modalities = pred_data.get('modalities_used', [])
        if modalities:
            print(f'modalities_used: {modalities}')
        else:
            print('[MISSING] modalities_used is empty or missing')
            
        print('\n=== Summary ===')
        if all_present:
            print('[OK] All required fields are present for ResultsPage')
        else:
            print('[FAIL] Some required fields are missing')
            
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    test_prediction_structure()