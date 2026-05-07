import requests
import json

# Test the prediction detail endpoint
BASE_URL = "http://localhost:8000"
PREDICTION_ID = "69f720df320421d3af9968d1"  # The ID user mentioned

def test_prediction_detail():
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
        print(f"\nTesting prediction detail for ID: {PREDICTION_ID}")
        pred_response = requests.get(f"{BASE_URL}/predictions/{PREDICTION_ID}", headers=headers)
        
        print(f"Status code: {pred_response.status_code}")
        if pred_response.status_code == 200:
            prediction = pred_response.json()
            print(f"Prediction found!")
            print(f"Data structure: {json.dumps(prediction, indent=2)[:500]}...")
            
            # Check clinical_reference_ranges type
            if "data" in prediction and "clinical_reference_ranges" in prediction["data"]:
                ref_ranges = prediction["data"]["clinical_reference_ranges"]
                print(f"\nclinical_reference_ranges type: {type(ref_ranges)}")
                if isinstance(ref_ranges, list):
                    print(f"Length: {len(ref_ranges)}")
                    if len(ref_ranges) > 0:
                        print(f"First item: {ref_ranges[0]}")
                else:
                    print(f"Value: {ref_ranges}")
        elif pred_response.status_code == 404:
            print("Prediction not found (404)")
            
            # List all predictions to see what exists
            print("\nListing all predictions...")
            list_response = requests.get(f"{BASE_URL}/predictions", headers=headers)
            if list_response.status_code == 200:
                predictions = list_response.json()
                if "data" in predictions:
                    pred_list = predictions["data"]
                    print(f"Total predictions: {len(pred_list)}")
                    for i, p in enumerate(pred_list[:5]):
                        print(f"  {i+1}. ID: {p.get('id')}, Risk: {p.get('risk_category', 'N/A')}")
        else:
            print(f"Error: {pred_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_prediction_detail()