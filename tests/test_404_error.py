import requests
import json

# Test the 404 error response
BASE_URL = "http://localhost:8000"
NON_EXISTENT_PREDICTION_ID = "69f720df320421d3af9968d1"

def test_404_response():
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
        
        # Test prediction detail endpoint with non-existent ID
        headers = {"Authorization": f"Bearer {access_token}"}
        print(f"\nTesting 404 response for ID: {NON_EXISTENT_PREDICTION_ID}")
        pred_response = requests.get(f"{BASE_URL}/predictions/{NON_EXISTENT_PREDICTION_ID}", headers=headers)
        
        print(f"Status code: {pred_response.status_code}")
        print(f"Response headers: {dict(pred_response.headers)}")
        print(f"Response body: {pred_response.text}")
        
        # Try to parse JSON
        try:
            error_data = pred_response.json()
            print(f"\nParsed error JSON:")
            print(json.dumps(error_data, indent=2))
        except:
            print("\nResponse is not valid JSON")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_404_response()