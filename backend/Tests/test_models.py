#!/usr/bin/env python3
"""
Test script for Sailor Utility models and basic functionality
"""

from app import app
from models import db, User, SystemModule, UserModulePermission, UserPreference
import json

def test_models():
    """Test all our new models and functionality"""
    
    with app.app_context():
        print("=== Sailor Utility Model Tests ===\n")
        
        # Test 1: Database connection and table creation
        print("1. Testing database connection and tables...")
        try:
            tables = list(db.metadata.tables.keys())
            print(f"   ✓ Found {len(tables)} tables: {', '.join(tables)}")
        except Exception as e:
            print(f"   ✗ Database error: {e}")
            return False
        
        # Test 2: User model with enhanced fields
        print("\n2. Testing enhanced User model...")
        try:
            user_count = User.query.count()
            print(f"   ✓ Current users: {user_count}")
            
            if user_count > 0:
                admin_user = User.query.filter_by(is_admin=True).first()
                if admin_user:
                    print(f"   ✓ Admin user found: {admin_user.get_full_name()}")
                    print(f"   ✓ Sailing experience: {admin_user.sailing_experience}")
                    print(f"   ✓ Default module: {admin_user.default_module}")
                else:
                    print("   ! No admin user found")
        except Exception as e:
            print(f"   ✗ User model error: {e}")
            return False
        
        # Test 3: SystemModule model
        print("\n3. Testing SystemModule model...")
        try:
            modules = SystemModule.query.order_by(SystemModule.sort_order).all()
            print(f"   ✓ Found {len(modules)} system modules:")
            for module in modules:
                admin_only = " (Admin Only)" if module.requires_admin else ""
                active = "✓" if module.is_active else "✗"
                print(f"     {active} {module.display_name} ({module.name}){admin_only}")
        except Exception as e:
            print(f"   ✗ SystemModule error: {e}")
            return False
        
        # Test 4: UserModulePermission model
        print("\n4. Testing UserModulePermission model...")
        try:
            permissions = UserModulePermission.query.all()
            print(f"   ✓ Found {len(permissions)} user permissions")
            
            if permissions:
                # Group permissions by user
                user_perms = {}
                for perm in permissions:
                    user_id = perm.user_id
                    if user_id not in user_perms:
                        user_perms[user_id] = []
                    user_perms[user_id].append(perm.module.name)
                
                for user_id, module_names in user_perms.items():
                    user = User.query.get(user_id)
                    print(f"     {user.username}: {', '.join(module_names)}")
        except Exception as e:
            print(f"   ✗ UserModulePermission error: {e}")
            return False
        
        # Test 5: UserPreference model (create a test preference)
        print("\n5. Testing UserPreference model...")
        try:
            # Create a test preference if we have users
            if user_count > 0:
                admin_user = User.query.filter_by(is_admin=True).first()
                
                # Check if preference already exists
                existing_pref = UserPreference.query.filter_by(
                    user_id=admin_user.id, 
                    preference_key='test_preference'
                ).first()
                
                if not existing_pref:
                    test_pref = UserPreference(
                        user_id=admin_user.id,
                        preference_key='test_preference'
                    )
                    test_pref.set_value({'theme': 'dark', 'notifications': True})
                    db.session.add(test_pref)
                    db.session.commit()
                    print("   ✓ Created test preference")
                else:
                    print("   ✓ Test preference already exists")
                
                # Test retrieving preferences
                prefs = UserPreference.query.filter_by(user_id=admin_user.id).all()
                print(f"   ✓ User has {len(prefs)} preferences")
                for pref in prefs:
                    print(f"     {pref.preference_key}: {pref.get_value()}")
        except Exception as e:
            print(f"   ✗ UserPreference error: {e}")
            return False
        
        # Test 6: Model relationships
        print("\n6. Testing model relationships...")
        try:
            if user_count > 0:
                admin_user = User.query.filter_by(is_admin=True).first()
                
                # Test user -> module permissions relationship
                user_permissions = admin_user.module_permissions
                print(f"   ✓ Admin user has {len(user_permissions)} module permissions")
                
                # Test user -> preferences relationship
                user_prefs = admin_user.preferences
                print(f"   ✓ Admin user has {len(user_prefs)} preferences")
                
                # Test module -> user permissions relationship
                dashboard_module = SystemModule.query.filter_by(name='dashboard').first()
                if dashboard_module:
                    module_perms = dashboard_module.user_permissions
                    print(f"   ✓ Dashboard module has {len(module_perms)} user permissions")
        except Exception as e:
            print(f"   ✗ Relationship error: {e}")
            return False
        
        # Test 7: JSON serialization
        print("\n7. Testing JSON serialization...")
        try:
            if user_count > 0:
                admin_user = User.query.filter_by(is_admin=True).first()
                user_dict = admin_user.to_dict()
                
                # Test that we can serialize to JSON
                json_str = json.dumps(user_dict, indent=2)
                print("   ✓ User model serializes to JSON correctly")
                print(f"   ✓ JSON contains {len(user_dict)} fields")
                
                # Test module serialization
                module = SystemModule.query.first()
                if module:
                    module_dict = module.to_dict()
                    json.dumps(module_dict)
                    print("   ✓ Module model serializes to JSON correctly")
        except Exception as e:
            print(f"   ✗ JSON serialization error: {e}")
            return False
        
        print("\n=== All Tests Passed! ===")
        print("\nDatabase Summary:")
        print(f"- Users: {User.query.count()}")
        print(f"- Modules: {SystemModule.query.count()}")
        print(f"- Permissions: {UserModulePermission.query.count()}")
        print(f"- Preferences: {UserPreference.query.count()}")
        
        return True

if __name__ == "__main__":
    success = test_models()
    exit(0 if success else 1)