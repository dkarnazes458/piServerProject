#!/usr/bin/env python3
"""
Test script for Module Management API endpoints
"""

from app import app
from models import db, User, SystemModule, UserModulePermission, UserPreference
from flask import json

def test_module_management_apis():
    """Test all module management API endpoints"""
    
    print("=== Module Management API Tests ===\n")
    
    with app.test_client() as client:
        with app.app_context():
            
            # Create test users
            admin_user = User.query.filter_by(is_admin=True).first()
            if not admin_user:
                print("Creating test admin user...")
                admin_user = User(
                    username='testadmin',
                    email='admin@test.com',
                    is_admin=True,
                    sailing_experience='Professional'
                )
                admin_user.set_password('admin123')
                db.session.add(admin_user)
                db.session.commit()
            
            regular_user = User.query.filter_by(is_admin=False).first()
            if not regular_user:
                print("Creating test regular user...")
                regular_user = User(
                    username='testuser',
                    email='user@test.com',
                    is_admin=False,
                    sailing_experience='Intermediate'
                )
                regular_user.set_password('user123')
                db.session.add(regular_user)
                db.session.commit()
            
            # Login as admin
            print("1. Testing admin login...")
            admin_login = client.post('/api/auth/login', 
                                    data=json.dumps({
                                        'username': admin_user.username,
                                        'password': 'admin123'
                                    }),
                                    content_type='application/json')
            
            if admin_login.status_code == 200:
                admin_token = json.loads(admin_login.data)['access_token']
                admin_headers = {'Authorization': f'Bearer {admin_token}'}
                print("   ✓ Admin login successful")
            else:
                print(f"   ✗ Admin login failed: {admin_login.status_code}")
                return False
            
            # Login as regular user
            print("2. Testing regular user login...")
            user_login = client.post('/api/auth/login',
                                   data=json.dumps({
                                       'username': regular_user.username,
                                       'password': 'user123'
                                   }),
                                   content_type='application/json')
            
            if user_login.status_code == 200:
                user_token = json.loads(user_login.data)['access_token']
                user_headers = {'Authorization': f'Bearer {user_token}'}
                print("   ✓ Regular user login successful")
            else:
                print(f"   ✗ Regular user login failed: {user_login.status_code}")
                return False
            
            # Test 3: Admin - Get all modules
            print("\\n3. Testing admin get all modules...")
            response = client.get('/api/admin/modules', headers=admin_headers)
            if response.status_code == 200:
                modules_data = json.loads(response.data)
                print(f"   ✓ Found {modules_data['count']} modules")
                module_names = [m['name'] for m in modules_data['modules']]
                print(f"   ✓ Modules: {', '.join(module_names)}")
            else:
                print(f"   ✗ Get modules failed: {response.status_code}")
                return False
            
            # Test 4: Regular user tries admin endpoint (should fail)
            print("\\n4. Testing regular user access to admin endpoint...")
            response = client.get('/api/admin/modules', headers=user_headers)
            if response.status_code == 403:
                print("   ✓ Regular user correctly denied admin access")
            else:
                print(f"   ✗ Security issue: Regular user got {response.status_code}")
                return False
            
            # Test 5: Create new module (admin only)
            print("\\n5. Testing create new module...")
            new_module_data = {
                'name': 'test_module',
                'display_name': 'Test Module',
                'description': 'A test module for API testing',
                'icon': 'test',
                'sort_order': 50
            }
            response = client.post('/api/admin/modules',
                                 data=json.dumps(new_module_data),
                                 content_type='application/json',
                                 headers=admin_headers)
            
            if response.status_code == 201:
                created_module = json.loads(response.data)['module']
                print(f"   ✓ Created module: {created_module['display_name']}")
                test_module_id = created_module['id']
            else:
                print(f"   ✗ Create module failed: {response.status_code}")
                print(f"   Response: {response.data.decode()}")
                return False
            
            # Test 6: Update module
            print("\\n6. Testing update module...")
            update_data = {
                'description': 'Updated test module description',
                'is_active': True
            }
            response = client.put(f'/api/admin/modules/{test_module_id}',
                                data=json.dumps(update_data),
                                content_type='application/json',
                                headers=admin_headers)
            
            if response.status_code == 200:
                print("   ✓ Module updated successfully")
            else:
                print(f"   ✗ Update module failed: {response.status_code}")
                return False
            
            # Test 7: Grant module access to regular user
            print("\\n7. Testing grant module access...")
            grant_data = {'module_id': test_module_id}
            response = client.post(f'/api/admin/users/{regular_user.id}/modules',
                                 data=json.dumps(grant_data),
                                 content_type='application/json',
                                 headers=admin_headers)
            
            if response.status_code == 201:
                print("   ✓ Module access granted to user")
            else:
                print(f"   ✗ Grant access failed: {response.status_code}")
                print(f"   Response: {response.data.decode()}")
                return False
            
            # Test 8: Get user's available modules
            print("\\n8. Testing user get available modules...")
            response = client.get('/api/user/modules', headers=user_headers)
            if response.status_code == 200:
                user_modules = json.loads(response.data)
                print(f"   ✓ User has access to {user_modules['count']} modules")
                user_module_names = [m['name'] for m in user_modules['modules']]
                print(f"   ✓ User modules: {', '.join(user_module_names)}")
            else:
                print(f"   ✗ Get user modules failed: {response.status_code}")
                return False
            
            # Test 9: Toggle module enable/disable
            print("\\n9. Testing toggle module enable/disable...")
            response = client.put(f'/api/user/modules/{test_module_id}/toggle',
                                headers=user_headers)
            if response.status_code == 200:
                toggle_result = json.loads(response.data)
                print(f"   ✓ Module toggled: {toggle_result['message']}")
            else:
                print(f"   ✗ Toggle module failed: {response.status_code}")
                return False
            
            # Test 10: User preferences
            print("\\n10. Testing user preferences...")
            prefs_data = {
                'theme': 'dark',
                'notifications': True,
                'default_units': 'metric'
            }
            response = client.put('/api/user/preferences',
                                data=json.dumps(prefs_data),
                                content_type='application/json',
                                headers=user_headers)
            
            if response.status_code == 200:
                print("   ✓ User preferences updated")
                
                # Get preferences back
                response = client.get('/api/user/preferences', headers=user_headers)
                if response.status_code == 200:
                    prefs = json.loads(response.data)['preferences']
                    print(f"   ✓ Retrieved preferences: {prefs}")
                else:
                    print(f"   ✗ Get preferences failed: {response.status_code}")
                    return False
            else:
                print(f"   ✗ Update preferences failed: {response.status_code}")
                return False
            
            # Test 11: Get user module permissions (admin view)
            print("\\n11. Testing admin view of user permissions...")
            response = client.get(f'/api/admin/users/{regular_user.id}/modules',
                                headers=admin_headers)
            if response.status_code == 200:
                admin_view = json.loads(response.data)
                granted_modules = [m for m in admin_view['modules'] if m['has_permission']]
                print(f"   ✓ Admin sees user has {len(granted_modules)} module permissions")
            else:
                print(f"   ✗ Admin get user modules failed: {response.status_code}")
                return False
            
            # Test 12: Cleanup - Delete test module
            print("\\n12. Testing delete module...")
            response = client.delete(f'/api/admin/modules/{test_module_id}',
                                   headers=admin_headers)
            if response.status_code == 200:
                print("   ✓ Test module deleted successfully")
            else:
                print(f"   ✗ Delete module failed: {response.status_code}")
                return False
            
            print("\\n=== All Module Management API Tests Passed! ===")
            
            # Final summary
            print("\\nFinal System State:")
            print(f"- Users: {User.query.count()}")
            print(f"- Modules: {SystemModule.query.count()}")
            print(f"- Permissions: {UserModulePermission.query.count()}")
            print(f"- Preferences: {UserPreference.query.count()}")
            
            return True

if __name__ == "__main__":
    success = test_module_management_apis()
    exit(0 if success else 1)