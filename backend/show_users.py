#!/usr/bin/env python3
"""
Show Users Script

Displays all users and their current module permissions.
Useful for checking current access levels.

Usage:
  python show_users.py
"""

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

def show_users():
    """Display all users and their permissions"""
    app = create_app_for_command()
    
    with app.app_context():
        print("=" * 70)
        print("SAILOR UTILITY - USER PERMISSIONS")
        print("=" * 70)
        
        # Get all users
        users = User.query.all()
        if not users:
            print("No users found in the database.")
            return
        
        # Get all modules
        modules = SystemModule.query.filter_by(is_active=True).all()
        module_names = [m.name for m in modules]
        
        print(f"Found {len(users)} users and {len(modules)} active modules")
        print()
        
        for user in users:
            print(f"👤 {user.username} ({user.email})")
            print(f"   Name: {user.get_full_name()}")
            print(f"   Admin: {'✅ Yes' if user.is_admin else '❌ No'}")
            print(f"   Active: {'✅ Yes' if user.is_active else '❌ No'}")
            print(f"   Created: {user.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            # Get user's module permissions
            permissions = UserModulePermission.query.filter_by(
                user_id=user.id
            ).join(SystemModule).all()
            
            enabled_modules = [p.module.name for p in permissions if p.is_enabled]
            disabled_modules = [p.module.name for p in permissions if not p.is_enabled]
            
            print(f"   Modules ({len(enabled_modules)}/{ len(modules)}):")
            
            if enabled_modules:
                print(f"     ✅ Enabled: {', '.join(enabled_modules)}")
            else:
                print(f"     ❌ No modules enabled")
            
            if disabled_modules:
                print(f"     ⏸️  Disabled: {', '.join(disabled_modules)}")
            
            # Show missing modules
            missing_modules = [m for m in module_names if m not in enabled_modules and m not in disabled_modules]
            if missing_modules:
                print(f"     ⚠️  No permission: {', '.join(missing_modules)}")
            
            print()
        
        print("=" * 70)
        print("AVAILABLE MODULES")
        print("=" * 70)
        
        for module in modules:
            admin_req = " (Admin Only)" if module.requires_admin else ""
            print(f"📦 {module.name} - {module.display_name}{admin_req}")
            print(f"   {module.description}")
            print()

if __name__ == "__main__":
    show_users()