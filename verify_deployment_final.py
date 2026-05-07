#!/usr/bin/env python3
"""
Deployment Verification Script for AyuPulseApp
This script verifies that all deployment components are properly configured.
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and is readable."""
    path = Path(filepath)
    if path.exists() and path.is_file():
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[FAIL] {description}: {filepath} NOT FOUND")
        return False

def check_env_file(filepath, required_vars=None):
    """Check if environment file exists and has required variables."""
    path = Path(filepath)
    if not path.exists():
        print(f"[FAIL] Environment file not found: {filepath}")
        return False
    
    print(f"[OK] Environment file exists: {filepath}")
    
    if required_vars:
        content = path.read_text()
        missing = []
        for var in required_vars:
            if f"{var}=" in content:
                print(f"  [OK] Contains {var}")
            else:
                print(f"  [FAIL] Missing {var}")
                missing.append(var)
        
        if missing:
            print(f"  Warning: Missing required variables: {missing}")
            return False
    
    return True

def check_backend_health(url):
    """Check if backend API is healthy."""
    try:
        response = requests.get(f"{url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] Backend health check: {url}/health")
            print(f"  Status: {data.get('status', 'unknown')}")
            print(f"  Version: {data.get('version', 'unknown')}")
            return True
        else:
            print(f"[FAIL] Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] Backend health check error: {e}")
        return False

def check_frontend_build():
    """Check if frontend build directory exists."""
    frontend_dist = Path("frontend/dist")
    if frontend_dist.exists() and any(frontend_dist.iterdir()):
        print(f"[OK] Frontend build exists: {frontend_dist}")
        return True
    else:
        print(f"[FAIL] Frontend build not found or empty: {frontend_dist}")
        return False

def check_railway_config():
    """Check Railway configuration file."""
    railway_json = Path("backend/railway.json")
    if not railway_json.exists():
        print("[FAIL] Railway configuration not found: backend/railway.json")
        return False
    
    try:
        with open(railway_json, 'r') as f:
            config = json.load(f)
        
        print("[OK] Railway configuration found:")
        print(f"  Start command: {config.get('deploy', {}).get('startCommand', 'NOT SET')}")
        print(f"  Health check: {config.get('deploy', {}).get('healthcheckPath', 'NOT SET')}")
        
        # Check if start command is correct
        start_cmd = config.get('deploy', {}).get('startCommand', '')
        if 'uvicorn app.main:app' in start_cmd:
            print("  [OK] Start command looks correct")
            return True
        else:
            print("  [FAIL] Start command may be incorrect")
            return False
    except Exception as e:
        print(f"[FAIL] Error reading railway.json: {e}")
        return False

def check_vercel_config():
    """Check Vercel configuration file."""
    vercel_json = Path("frontend/vercel.json")
    if not vercel_json.exists():
        print("[FAIL] Vercel configuration not found: frontend/vercel.json")
        return False
    
    try:
        with open(vercel_json, 'r') as f:
            config = json.load(f)
        
        print("[OK] Vercel configuration found:")
        
        # Check rewrites for SPA
        rewrites = config.get('rewrites', [])
        if rewrites:
            print(f"  [OK] SPA rewrites configured ({len(rewrites)} rules)")
        else:
            print("  [FAIL] No SPA rewrites configured")
        
        # Check headers
        headers = config.get('headers', [])
        if headers:
            print(f"  [OK] Security headers configured ({len(headers)} rules)")
        else:
            print("  [FAIL] No security headers configured")
        
        return True
    except Exception as e:
        print(f"[FAIL] Error reading vercel.json: {e}")
        return False

def check_cors_config():
    """Check CORS configuration in backend."""
    config_py = Path("backend/app/core/config.py")
    if not config_py.exists():
        print("[FAIL] Backend config.py not found")
        return False
    
    try:
        content = config_py.read_text()
        
        # Check for CORS origins configuration
        if 'BACKEND_CORS_ORIGINS' in content:
            print("[OK] CORS configuration found in config.py")
            
            # Check if Vercel domains are included
            vercel_domains = ['vercel.app', 'ayu-pulse-app.vercel.app']
            found = any(domain in content for domain in vercel_domains)
            
            if found:
                print("  [OK] Vercel domains detected in CORS configuration")
            else:
                print("  [WARN] Vercel domains not found in CORS configuration")
                print("    Note: Add your Vercel domain to BACKEND_CORS_ORIGINS")
            
            return True
        else:
            print("[FAIL] BACKEND_CORS_ORIGINS not found in config.py")
            return False
    except Exception as e:
        print(f"[FAIL] Error reading config.py: {e}")
        return False

def main():
    print("=" * 70)
    print("AyuPulseApp Deployment Verification")
    print("=" * 70)
    
    print("\n1. Checking file structure...")
    print("-" * 40)
    
    files_to_check = [
        ("backend/requirements.txt", "Backend dependencies"),
        ("backend/app/main.py", "Backend main application"),
        ("frontend/package.json", "Frontend dependencies"),
        ("frontend/vite.config.ts", "Frontend build configuration"),
        ("README.md", "Main documentation"),
        ("DEPLOYMENT.md", "Deployment guide"),
        ("DEPLOY_VERCEL.md", "Vercel deployment guide"),
    ]
    
    all_files_ok = True
    for filepath, description in files_to_check:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    print("\n2. Checking environment configuration...")
    print("-" * 40)
    
    # Check frontend .env.example
    frontend_env_ok = check_env_file(
        "frontend/.env.example",
        ["VITE_API_URL", "VITE_APP_NAME"]
    )
    
    # Check backend .env.example
    backend_env_ok = check_env_file(
        "backend/.env.example",
        ["MONGODB_URL", "SECRET_KEY", "BACKEND_CORS_ORIGINS"]
    )
    
    print("\n3. Checking deployment configurations...")
    print("-" * 40)
    
    railway_ok = check_railway_config()
    vercel_ok = check_vercel_config()
    cors_ok = check_cors_config()
    
    print("\n4. Checking build status...")
    print("-" * 40)
    
    frontend_build_ok = check_frontend_build()
    
    print("\n5. Testing backend connectivity (optional)...")
    print("-" * 40)
    
    backend_urls = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    
    backend_healthy = False
    for url in backend_urls:
        print(f"\nTrying backend at {url}...")
        if check_backend_health(url):
            backend_healthy = True
            break
    
    if not backend_healthy:
        print("⚠ Backend not reachable locally (may be expected if not running)")
    
    print("\n" + "=" * 70)
    print("DEPLOYMENT READINESS SUMMARY")
    print("=" * 70)
    
    summary = {
        "File Structure": all_files_ok,
        "Frontend Environment": frontend_env_ok,
        "Backend Environment": backend_env_ok,
        "Railway Configuration": railway_ok,
        "Vercel Configuration": vercel_ok,
        "CORS Configuration": cors_ok,
        "Frontend Build": frontend_build_ok,
        "Backend Health": backend_healthy,
    }
    
    all_passed = True
    for item, status in summary.items():
        status_symbol = "[OK]" if status else "[FAIL]"
        print(f"{status_symbol} {item}")
        if not status:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("[SUCCESS] DEPLOYMENT READY: All checks passed!")
        print("\nNext steps:")
        print("1. Deploy backend to Railway: Follow instructions in DEPLOYMENT.md")
        print("2. Set VITE_API_URL in Vercel to your Railway backend URL")
        print("3. Update CORS in backend to include your Vercel domain")
        print("4. Test the complete application at your Vercel URL")
    else:
        print("[WARNING] DEPLOYMENT NOT READY: Some checks failed.")
        print("\nPlease fix the issues marked with [FAIL] above.")
        print("Refer to DEPLOYMENT.md and DEPLOY_VERCEL.md for guidance.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())