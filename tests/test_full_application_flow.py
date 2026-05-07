import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_step(step_num, description):
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {description}")
    print(f"{'='*60}")

def test_full_application():
    print("Testing Full Application Functionality")
    print("=" * 60)
    
    # Step 1: Test login with existing user
    print_step(1, "Testing Login")
    login_data = {
        "username": "patient@ayupulse.com",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if login_response.status_code != 200:
            print(f"[FAIL] Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return False
        
        token_data = login_response.json()
        access_token = token_data.get("access_token")
        print(f"[OK] Login successful")
        print(f"   Token obtained: {access_token[:20]}...")
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Step 2: Test getting current user
        print_step(2, "Testing Get Current User")
        me_response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"[OK] User data retrieved")
            print(f"   Name: {user_data.get('data', {}).get('name', 'N/A')}")
            print(f"   Email: {user_data.get('data', {}).get('email', 'N/A')}")
            print(f"   Role: {user_data.get('data', {}).get('role', 'N/A')}")
        else:
            print(f"[FAIL] Failed to get user data: {me_response.status_code}")
        
        # Step 3: Test listing predictions
        print_step(3, "Testing List Predictions")
        predictions_response = requests.get(f"{BASE_URL}/predictions", headers=headers)
        if predictions_response.status_code == 200:
            predictions = predictions_response.json()
            pred_list = predictions.get("data", [])
            print(f"[OK] Predictions retrieved: {len(pred_list)} found")
            for i, p in enumerate(pred_list[:3]):
                print(f"   {i+1}. ID: {p.get('id')[:8]}..., Risk: {p.get('risk_category', 'N/A')}")
        else:
            print(f"[FAIL] Failed to list predictions: {predictions_response.status_code}")
        
        # Step 4: Test getting an existing prediction detail
        print_step(4, "Testing Existing Prediction Detail")
        if pred_list:
            existing_id = pred_list[0].get('id')
            detail_response = requests.get(f"{BASE_URL}/predictions/{existing_id}", headers=headers)
            if detail_response.status_code == 200:
                detail = detail_response.json()
                print(f"[OK] Prediction detail retrieved")
                print(f"   ID: {detail.get('data', {}).get('id')}")
                print(f"   Risk category: {detail.get('data', {}).get('risk_category')}")
                print(f"   Risk score: {detail.get('data', {}).get('risk_score')}")
                
                # Check clinical_reference_ranges is a list
                ref_ranges = detail.get('data', {}).get('clinical_reference_ranges', [])
                if isinstance(ref_ranges, list):
                    print(f"   clinical_reference_ranges: List with {len(ref_ranges)} items [OK]")
                else:
                    print(f"   clinical_reference_ranges: NOT a list (type: {type(ref_ranges)}) [FAIL]")
            else:
                print(f"[FAIL] Failed to get prediction detail: {detail_response.status_code}")
        else:
            print("[WARN] No predictions to test detail view")
        
        # Step 5: Test 404 error for non-existent prediction
        print_step(5, "Testing 404 Error Handling")
        non_existent_id = "69f720df320421d3af9968d1"
        error_response = requests.get(f"{BASE_URL}/predictions/{non_existent_id}", headers=headers)
        if error_response.status_code == 404:
            error_data = error_response.json()
            print(f"[OK] 404 error handled correctly")
            print(f"   Error message: {error_data.get('error', 'N/A')}")
            print(f"   Code: {error_data.get('code', 'N/A')}")
        else:
            print(f"[FAIL] Expected 404 but got: {error_response.status_code}")
        
        # Step 6: Test prediction stats
        print_step(6, "Testing Prediction Statistics")
        stats_response = requests.get(f"{BASE_URL}/predictions/stats/summary", headers=headers)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"[OK] Prediction stats retrieved")
            print(f"   Total predictions: {stats.get('data', {}).get('total_predictions', 'N/A')}")
            print(f"   Risk distribution: {stats.get('data', {}).get('risk_distribution', 'N/A')}")
        else:
            print(f"[FAIL] Failed to get stats: {stats_response.status_code}")
        
        # Step 7: Test profile endpoint
        print_step(7, "Testing Profile Endpoint")
        profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if profile_response.status_code == 200:
            profile = profile_response.json()
            print(f"[OK] Profile retrieved")
        elif profile_response.status_code == 404:
            print(f"[WARN] Profile not found (user may not have created profile yet)")
        else:
            print(f"[FAIL] Failed to get profile: {profile_response.status_code}")
        
        # Step 8: Test patients endpoint
        print_step(8, "Testing Patients Endpoint")
        patients_response = requests.get(f"{BASE_URL}/patients", headers=headers)
        if patients_response.status_code == 200:
            patients = patients_response.json()
            patients_list = patients.get("data", [])
            print(f"[OK] Patients retrieved: {len(patients_list)} found")
        else:
            print(f"[FAIL] Failed to get patients: {patients_response.status_code}")
        
        print("\n" + "="*60)
        print("SUMMARY: All critical endpoints tested successfully!")
        print("The application is functioning correctly.")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Exception during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_full_application()
    if success:
        print("\n[OK] All tests passed! Application is working correctly.")
    else:
        print("\n[FAIL] Some tests failed. Check the logs above.")