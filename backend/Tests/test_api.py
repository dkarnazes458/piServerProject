#!/usr/bin/env python3
"""
Test script for API endpoints with enhanced models
"""

import requests
import json
import time
import threading
from app import app

def start_server():
    """Start the Flask server in a thread"""
    app.run(host='127.0.0.1', port=5001, debug=False)

def test_api_endpoints():
    """Test API endpoints with our enhanced models"""
    base_url = "http://127.0.0.1:5001"
    
    print("=== API Endpoint Tests ===\n")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    try:
        # Test 1: Health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ Health check passed: {response.json()}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            return False
        
        # Test 2: Login with admin user
        print("\n2. Testing login with admin user...")
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/api/auth/login", 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            login_result = response.json()
            print("   ✓ Login successful")
            print(f"   ✓ User: {login_result['user']['full_name']}")
            print(f"   ✓ Admin: {login_result['user']['is_admin']}")
            print(f"   ✓ Experience: {login_result['user']['sailing_experience']}")
            access_token = login_result['access_token']
        else:
            print(f"   ✗ Login failed: {response.status_code} - {response.text}")
            return False
        
        # Test 3: Get current user with enhanced fields
        print("\n3. Testing get current user...")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{base_url}/api/auth/me", 
                              headers=headers, timeout=5)
        
        if response.status_code == 200:
            user_data = response.json()['user']
            print("   ✓ Current user data retrieved")
            print(f"   ✓ Full name: {user_data['full_name']}")
            print(f"   ✓ Default module: {user_data['default_module']}")
            print(f"   ✓ Timezone: {user_data['timezone']}")
            print(f"   ✓ Certifications: {user_data['certifications']}")
        else:
            print(f"   ✗ Get user failed: {response.status_code}")
            return False
        
        # Test 4: Register a new user (test enhanced registration)
        print("\n4. Testing user registration with enhanced fields...")
        register_data = {
            "username": "sailor1",
            "email": "sailor1@example.com",
            "password": "sailor123"
        }
        response = requests.post(f"{base_url}/api/auth/register", 
                               json=register_data, timeout=5)
        
        if response.status_code == 201:
            register_result = response.json()
            print("   ✓ User registration successful")
            print(f"   ✓ New user: {register_result['user']['username']}")
            print(f"   ✓ Admin status: {register_result['user']['is_admin']}")
            print(f"   ✓ Default experience: {register_result['user']['sailing_experience']}")
        else:
            print(f"   ✗ Registration failed: {response.status_code} - {response.text}")
            return False
        
        print("\n=== All API Tests Passed! ===")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request error: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    # Start server in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run tests
    success = test_api_endpoints()
    exit(0 if success else 1)