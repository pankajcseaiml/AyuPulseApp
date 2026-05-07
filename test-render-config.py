#!/usr/bin/env python3
"""
Test Render configuration for AyuPulseApp backend.
This script validates the render.yaml configuration and checks if the backend
is ready for deployment to Render.
"""

import os
import sys
import yaml
import requests

def check_render_yaml():
    """Check if render.yaml exists and is valid."""
    print("1. Checking render.yaml configuration...")
    
    render_yaml_path = "backend/render.yaml"
    if not os.path.exists(render_yaml_path):
        print(f"  [FAIL] render.yaml not found at {render_yaml_path}")
        return False
    
    try:
        with open(render_yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"  [OK] render.yaml found and valid YAML")
        
        # Check required fields
        if 'services' not in config:
            print(f"  [FAIL] 'services' section missing in render.yaml")
            return False
        
        services = config['services']
        if not services:
            print(f"  [FAIL] No services defined in render.yaml")
            return False
        
        web_service = services[0]
        print(f"  [OK] Service name: {web_service.get('name', 'N/A')}")
        print(f"  [OK] Build command: {web_service.get('buildCommand', 'N/A')}")
        print(f"  [OK] Start command: {web_service.get('startCommand', 'N/A')}")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"  [FAIL] Invalid YAML: {e}")
        return False
    except Exception as e:
        print(f"  [FAIL] Error reading render.yaml: {e}")
        return False

def check_requirements():
    """Check if requirements.txt exists."""
    print("\n2. Checking requirements.txt...")
    
    req_path = "backend/requirements.txt"
    if not os.path.exists(req_path):
        print(f"  [FAIL] requirements.txt not found at {req_path}")
        return False
    
    print(f"  [OK] requirements.txt found")
    
    # Check for essential packages
    try:
        with open(req_path, 'r') as f:
            content = f.read()
        
        essential_packages = ['fastapi', 'uvicorn', 'pymongo', 'motor']
        missing = []
        for pkg in essential_packages:
            if pkg not in content.lower():
                missing.append(pkg)
        
        if missing:
            print(f"  [WARNING] Some packages may be missing: {missing}")
        else:
            print(f"  [OK] Essential packages found")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Error reading requirements.txt: {e}")
        return False

def check_main_app():
    """Check if main FastAPI app exists."""
    print("\n3. Checking main application...")
    
    main_app_path = "backend/app/main.py"
    if not os.path.exists(main_app_path):
        print(f"  [FAIL] main.py not found at {main_app_path}")
        return False
    
    print(f"  [OK] main.py found")
    
    # Check if it contains FastAPI app
    try:
        with open(main_app_path, 'r') as f:
            content = f.read()
        
        if 'FastAPI' in content or 'app = FastAPI()' in content:
            print(f"  [OK] FastAPI application detected")
        else:
            print(f"  [WARNING] FastAPI app may not be properly defined")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Error reading main.py: {e}")
        return False

def check_health_endpoint():
    """Test health endpoint locally."""
    print("\n4. Testing health endpoint locally...")
    
    try:
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  [OK] Health endpoint: {data.get('status')}")
            return True
        else:
            print(f"  [WARNING] Health endpoint returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  [INFO] Backend not running locally (expected for Render test)")
        return True  # Not a failure for this test
    except Exception as e:
        print(f"  [INFO] Could not connect to local backend: {e}")
        return True  # Not a failure for this test

def check_env_example():
    """Check environment example files."""
    print("\n5. Checking environment configuration...")
    
    env_example_path = "backend/.env.example"
    if not os.path.exists(env_example_path):
        print(f"  [WARNING] .env.example not found at {env_example_path}")
    else:
        print(f"  [OK] .env.example found")
    
    env_production_path = "backend/.env.production"
    if not os.path.exists(env_production_path):
        print(f"  [INFO] .env.production not found (will use Render env vars)")
    else:
        print(f"  [OK] .env.production found")
    
    return True

def main():
    print("=" * 60)
    print("Render Deployment Configuration Test")
    print("=" * 60)
    
    tests = [
        check_render_yaml,
        check_requirements,
        check_main_app,
        check_env_example,
        check_health_endpoint,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  [ERROR] Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("\n[SUCCESS] Render configuration is ready for deployment!")
        print("\nNext steps:")
        print("1. Push changes to GitHub")
        print("2. Go to https://render.com")
        print("3. Create new Web Service")
        print("4. Connect your GitHub repository")
        print("5. Configure with render.yaml settings")
        print("6. Add environment variables (MONGODB_URL, SECRET_KEY, etc.)")
        print("7. Deploy!")
        return 0
    elif passed >= total - 1:
        print("\n[WARNING] Render configuration has minor issues")
        print("Check the warnings above before deploying.")
        return 1
    else:
        print("\n[FAILURE] Render configuration has significant issues")
        print("Fix the failures above before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())