#!/usr/bin/env python3
"""
Test authentication with enhanced User model
"""

from app import app
from models import db, User
from flask import json

def test_auth_functionality():
    """Test authentication functionality with enhanced models"""
    
    print("=== Authentication Tests ===\n")
    
    with app.test_client() as client:
        with app.app_context():
            
            # Test 1: Health endpoint
            print("1. Testing health endpoint...")
            response = client.get('/api/health')
            if response.status_code == 200:
                data = json.loads(response.data)
                print(f"   ✓ Health check: {data['status']}")
            else:
                print(f"   ✗ Health check failed: {response.status_code}")
                return False
            
            # Test 2: Login with admin user
            print("\n2. Testing login with enhanced User model...")
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            response = client.post('/api/auth/login', 
                                 data=json.dumps(login_data),
                                 content_type='application/json')
            
            if response.status_code == 200:
                login_result = json.loads(response.data)
                print("   ✓ Login successful")
                print(f"   ✓ User: {login_result['user']['full_name']}")
                print(f"   ✓ Admin: {login_result['user']['is_admin']}")
                print(f"   ✓ Experience: {login_result['user']['sailing_experience']}")
                print(f"   ✓ Certifications: {login_result['user']['certifications']}")
                access_token = login_result['access_token']
            else:
                print(f"   ✗ Login failed: {response.status_code}")
                print(f"   Response: {response.data.decode()}")
                return False
            
            # Test 3: Get current user
            print("\n3. Testing get current user...")
            headers = {"Authorization": f"Bearer {access_token}"}
            response = client.get('/api/auth/me', headers=headers)
            
            if response.status_code == 200:
                user_data = json.loads(response.data)['user']
                print("   ✓ Current user retrieved")
                print(f"   ✓ Enhanced fields working:")
                print(f"     - Full name: {user_data['full_name']}")
                print(f"     - Admin status: {user_data['is_admin']}")
                print(f"     - Sailing experience: {user_data['sailing_experience']}")
                print(f"     - Default module: {user_data['default_module']}")
                print(f"     - Timezone: {user_data['timezone']}")
            else:
                print(f"   ✗ Get user failed: {response.status_code}")
                return False
            
            # Test 4: Register new user
            print("\n4. Testing user registration...")
            register_data = {
                "username": "testuser",
                "email": "test@example.com",
                "password": "test123"
            }
            response = client.post('/api/auth/register',
                                 data=json.dumps(register_data),
                                 content_type='application/json')
            
            if response.status_code == 201:
                register_result = json.loads(response.data)
                print("   ✓ Registration successful")
                user = register_result['user']
                print(f"   ✓ New user defaults:")
                print(f"     - Admin: {user['is_admin']}")
                print(f"     - Experience: {user['sailing_experience']}")
                print(f"     - Default module: {user['default_module']}")
                print(f"     - Full name: {user['full_name']}")
            else:
                print(f"   ✗ Registration failed: {response.status_code}")
                print(f"   Response: {response.data.decode()}")
                return False
            
            print("\n=== All Authentication Tests Passed! ===")
            
            # Show final database state
            print(f"\nFinal Database State:")
            print(f"- Users: {User.query.count()}")
            print(f"- Admin users: {User.query.filter_by(is_admin=True).count()}")
            print(f"- Regular users: {User.query.filter_by(is_admin=False).count()}")
            
            return True

if __name__ == "__main__":
    success = test_auth_functionality()
    exit(0 if success else 1)