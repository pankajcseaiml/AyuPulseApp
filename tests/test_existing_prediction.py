import requests
import json

# Test the prediction detail endpoint
BASE_URL = "http://localhost:8000"
EXISTING_PREDICTION_ID = "69f72025320421d3af9968d0"  # One of the existing IDs

def test_existing_prediction():
    # First login to get token
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    try:
        # Login
        print("Logging in...")
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print(login_response.text)
            return
        
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        print(f"Login successful, token obtained")
        
        # Test prediction detail endpoint
        headers = {"Authorization": f"Bearer {access_token}"}
        print(f"\nTesting prediction detail for ID: {EXISTING_PREDICTION_ID}")
        pred_response = requests.get(f"{BASE_URL}/predictions/{EXISTING_PREDICTION_ID}", headers=headers)
        
        print(f"Status code: {pred_response.status_code}")
        if pred_response.status_code == 200:
            prediction = pred_response.json()
            print(f"Prediction found!")
            
            # Check the full structure
            data = prediction.get("data", {})
            print(f"\n=== PREDICTION DATA STRUCTURE ===")
            print(f"ID: {data.get('id')}")
            print(f"Risk category: {data.get('risk_category')}")
            print(f"Risk score: {data.get('risk_score')}")
            print(f"Created at: {data.get('created_at')}")
            
            # Check clinical_reference_ranges
            ref_ranges = data.get("clinical_reference_ranges")
            print(f"\nclinical_reference_ranges type: {type(ref_ranges)}")
            if ref_ranges is not None:
                if isinstance(ref_ranges, list):
                    print(f"Length: {len(ref_ranges)}")
                    if len(ref_ranges) > 0:
                        print(f"First item structure: {json.dumps(ref_ranges[0], indent=2)}")
                else:
                    print(f"Value (not a list): {ref_ranges}")
                    print(f"Keys if dict: {list(ref_ranges.keys()) if isinstance(ref_ranges, dict) else 'N/A'}")
            
            # Check other important fields
            print(f"\nOther fields:")
            print(f"  - recommendations: {type(data.get('recommendations'))}, value: {data.get('recommendations')}")
            print(f"  - shap_features: {type(data.get('shap_features'))}")
            print(f"  - modalities_used: {data.get('modalities_used')}")
            print(f"  - clinical_data: {data.get('clinical_data')}")
            
        else:
            print(f"Error: {pred_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_existing_prediction()