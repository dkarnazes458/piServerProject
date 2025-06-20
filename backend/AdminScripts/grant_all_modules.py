#!/usr/bin/env python3
"""
Grant All Modules Script

This script grants access to all available modules for a specified user.
Useful for testing the modular frontend or setting up admin users.

Usage:
  python grant_all_modules.py <username_or_email>
  python grant_all_modules.py --admin <username_or_email>  # Also make user admin
"""

import sys
import os
from flask import Flask
from config import Config
from models import db, User, SystemModule, UserModulePermission

def create_app_for_command():
    """Create Flask app configured for database access"""
    app = Flask(__name__)
    
    # Use development config for SQLite by default
    app.config.from_object(Config)
    
    # Override with production database if specified
    if 'DATABASE_URL' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    
    db.init_app(app)
    return app

def find_user(identifier):
    """Find user by username or email"""
    user = User.query.filter_by(username=identifier).first()
    if not user:
        user = User.query.filter_by(email=identifier).first()
    return user

def grant_all_modules(username_or_email, make_admin=False):
    """Grant all module permissions to a user"""
    app = create_app_for_command()
    
    with app.app_context():
        print(f"🔍 Looking for user: {username_or_email}")
        
        # Find the user
        user = find_user(username_or_email)
        if not user:
            print(f"❌ User '{username_or_email}' not found!")
            print("Available users:")
            users = User.query.all()
            for u in users:
                print(f"  - {u.username} ({u.email})")
            return False
        
        print(f"✅ Found user: {user.username} ({user.email})")
        
        # Make admin if requested
        if make_admin and not user.is_admin:
            user.is_admin = True
            print(f"🛡️  Granted admin privileges to {user.username}")
        
        # Get all available modules
        modules = SystemModule.query.filter_by(is_active=True).all()
        if not modules:
            print("⚠️  No active modules found! Creating default modules...")
            create_default_modules()
            modules = SystemModule.query.filter_by(is_active=True).all()
        
        print(f"📦 Found {len(modules)} active modules:")
        for module in modules:
            print(f"  - {module.name} ({module.display_name})")
        
        # Grant permissions for all modules
        granted_count = 0
        updated_count = 0
        
        for module in modules:
            # Check if permission already exists
            existing_permission = UserModulePermission.query.filter_by(
                user_id=user.id,
                module_id=module.id
            ).first()
            
            if existing_permission:
                if not existing_permission.is_enabled:
                    existing_permission.is_enabled = True
                    updated_count += 1
                    print(f"  ✓ Re-enabled {module.name}")
                else:
                    print(f"  → Already has {module.name}")
            else:
                # Create new permission
                permission = UserModulePermission(
                    user_id=user.id,
                    module_id=module.id,
                    is_enabled=True,
                    granted_by=user.id  # Self-granted for this script
                )
                db.session.add(permission)
                granted_count += 1
                print(f"  ✅ Granted {module.name}")
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n🎉 Success!")
            print(f"   - Granted {granted_count} new module permissions")
            print(f"   - Updated {updated_count} existing permissions")
            if make_admin:
                print(f"   - Admin privileges: {'✅' if user.is_admin else '❌'}")
            
            print(f"\n📊 Final status for {user.username}:")
            print(f"   - Admin: {'Yes' if user.is_admin else 'No'}")
            print(f"   - Total modules: {len(modules)}")
            
            # Show current permissions
            current_permissions = UserModulePermission.query.filter_by(
                user_id=user.id,
                is_enabled=True
            ).join(SystemModule).all()
            
            print(f"   - Enabled modules: {len(current_permissions)}")
            for perm in current_permissions:
                print(f"     • {perm.module.name}")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error saving changes: {e}")
            return False

def create_default_modules():
    """Create default system modules if they don't exist"""
    default_modules = [
        {
            'name': 'dashboard',
            'display_name': 'Dashboard',
            'description': 'Main dashboard with overview and statistics',
            'icon': 'dashboard',
            'sort_order': 1
        },
        {
            'name': 'boats',
            'display_name': 'Fleet Management',
            'description': 'Manage your boats and fleet information',
            'icon': 'boat',
            'sort_order': 2
        },
        {
            'name': 'trips',
            'display_name': 'Trip Logbook',
            'description': 'Log and track your sailing trips with GPS support',
            'icon': 'map',
            'sort_order': 3
        },
        {
            'name': 'equipment',
            'display_name': 'Equipment Tracker',
            'description': 'Manage your sailing equipment and inventory',
            'icon': 'tools',
            'sort_order': 4
        },
        {
            'name': 'maintenance',
            'display_name': 'Maintenance Log',
            'description': 'Track maintenance records and schedules',
            'icon': 'wrench',
            'sort_order': 5
        },
        {
            'name': 'events',
            'display_name': 'Events Calendar',
            'description': 'Manage sailing events, races, and gatherings',
            'icon': 'calendar',
            'sort_order': 6
        },
        {
            'name': 'navigation',
            'display_name': 'Weather & Routes',
            'description': 'Weather information and route planning tools',
            'icon': 'compass',
            'sort_order': 7
        },
        {
            'name': 'social',
            'display_name': 'Crew Network',
            'description': 'Connect with other sailors and crew members',
            'icon': 'users',
            'sort_order': 8
        },
        {
            'name': 'admin',
            'display_name': 'Admin Panel',
            'description': 'System administration and user management',
            'icon': 'settings',
            'requires_admin': True,
            'sort_order': 9
        }
    ]
    
    for module_data in default_modules:
        existing = SystemModule.query.filter_by(name=module_data['name']).first()
        if not existing:
            module = SystemModule(**module_data)
            db.session.add(module)
    
    db.session.commit()

def show_usage():
    """Show usage information"""
    print("Grant All Modules Script")
    print("=" * 30)
    print()
    print("Usage:")
    print("  python grant_all_modules.py <username_or_email>")
    print("  python grant_all_modules.py --admin <username_or_email>")
    print()
    print("Examples:")
    print("  python grant_all_modules.py john_doe")
    print("  python grant_all_modules.py john@example.com")
    print("  python grant_all_modules.py --admin admin@example.com")
    print()
    print("Options:")
    print("  --admin    Also grant admin privileges to the user")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    make_admin = False
    user_identifier = None
    
    # Parse arguments
    if len(sys.argv) == 2:
        user_identifier = sys.argv[1]
    elif len(sys.argv) == 3 and sys.argv[1] == '--admin':
        make_admin = True
        user_identifier = sys.argv[2]
    else:
        show_usage()
        sys.exit(1)
    
    # Run the grant process
    success = grant_all_modules(user_identifier, make_admin)
    sys.exit(0 if success else 1)