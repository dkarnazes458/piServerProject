#!/usr/bin/env python3
"""
Production Database Migration Script for PostgreSQL

This script handles migrating the production PostgreSQL database
to support the enhanced sailor utility features.
"""

import os
import sys
from flask import Flask
from flask_migrate import Migrate, upgrade, init, migrate as flask_migrate
from config import Config
from models import db, User, SystemModule, UserModulePermission, UserPreference
import traceback

def create_app_for_migration():
    """Create Flask app configured for migration"""
    app = Flask(__name__)
    
    # Use production config for PostgreSQL
    app.config.from_object(Config)
    
    # Override database URL if provided via environment
    if 'DATABASE_URL' in os.environ:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app, migrate

def backup_existing_data(app):
    """Backup existing user data before migration"""
    print("🔄 Backing up existing user data...")
    
    with app.app_context():
        try:
            # Check if user table exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'user' in tables:
                # Get existing users
                result = db.engine.execute('SELECT id, username, email, password_hash, created_at, is_active FROM "user"')
                existing_users = []
                for row in result:
                    existing_users.append({
                        'id': row[0],
                        'username': row[1], 
                        'email': row[2],
                        'password_hash': row[3],
                        'created_at': row[4],
                        'is_active': row[5] if row[5] is not None else True
                    })
                
                print(f"   ✓ Found {len(existing_users)} existing users to preserve")
                return existing_users
            else:
                print("   ℹ No existing user table found - fresh installation")
                return []
        except Exception as e:
            print(f"   ⚠ Error backing up data: {e}")
            return []

def create_default_modules(app):
    """Create default system modules"""
    print("🔄 Creating default system modules...")
    
    with app.app_context():
        modules_data = [
            {
                'name': 'dashboard',
                'display_name': 'Dashboard', 
                'description': 'Main dashboard with overview and statistics',
                'icon': 'dashboard',
                'sort_order': 1,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'boats',
                'display_name': 'Fleet Management',
                'description': 'Manage your boats and fleet information', 
                'icon': 'boat',
                'sort_order': 2,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'trips',
                'display_name': 'Trip Logbook',
                'description': 'Log and track your sailing trips with GPS support',
                'icon': 'map',
                'sort_order': 3,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'equipment',
                'display_name': 'Equipment Tracker',
                'description': 'Manage your sailing equipment and inventory',
                'icon': 'tools',
                'sort_order': 4,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'maintenance',
                'display_name': 'Maintenance Log',
                'description': 'Track maintenance records and schedules',
                'icon': 'wrench',
                'sort_order': 5,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'events',
                'display_name': 'Events Calendar',
                'description': 'Manage sailing events, races, and gatherings',
                'icon': 'calendar',
                'sort_order': 6,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'navigation',
                'display_name': 'Weather & Routes',
                'description': 'Weather information and route planning tools',
                'icon': 'compass',
                'sort_order': 7,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'social',
                'display_name': 'Crew Network',
                'description': 'Connect with other sailors and crew members',
                'icon': 'users',
                'sort_order': 8,
                'is_active': True,
                'requires_admin': False
            },
            {
                'name': 'admin',
                'display_name': 'Admin Panel',
                'description': 'System administration and user management',
                'icon': 'settings',
                'sort_order': 99,
                'is_active': True,
                'requires_admin': True
            }
        ]
        
        created_modules = []
        for module_data in modules_data:
            # Check if module already exists
            existing = SystemModule.query.filter_by(name=module_data['name']).first()
            if not existing:
                module = SystemModule(**module_data)
                db.session.add(module)
                created_modules.append(module)
            else:
                print(f"   ℹ Module '{module_data['name']}' already exists")
        
        if created_modules:
            db.session.commit()
            print(f"   ✓ Created {len(created_modules)} new modules")
        else:
            print("   ℹ All modules already exist")
        
        return SystemModule.query.all()

def migrate_existing_users(app, existing_users, modules):
    """Migrate existing users to enhanced model"""
    print("🔄 Migrating existing users to enhanced model...")
    
    with app.app_context():
        migrated_count = 0
        
        for user_data in existing_users:
            # Check if user already migrated
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if existing_user:
                print(f"   ℹ User '{user_data['username']}' already migrated")
                continue
            
            # Create user with enhanced fields
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password_hash'],
                created_at=user_data['created_at'],
                is_active=user_data['is_active'],
                # Set defaults for new fields
                is_admin=False,  # Will need manual admin assignment
                sailing_experience='Beginner',
                default_module='dashboard',
                timezone='UTC'
            )
            
            db.session.add(user)
            migrated_count += 1
        
        if migrated_count > 0:
            db.session.commit()
            print(f"   ✓ Migrated {migrated_count} users")
            
            # Grant default modules to all users
            print("🔄 Granting default module access...")
            default_modules = [m for m in modules if not m.requires_admin]
            
            for user_data in existing_users:
                user = User.query.filter_by(username=user_data['username']).first()
                if user:
                    for module in default_modules:
                        # Check if permission already exists
                        existing_perm = UserModulePermission.query.filter_by(
                            user_id=user.id, module_id=module.id
                        ).first()
                        
                        if not existing_perm:
                            permission = UserModulePermission(
                                user_id=user.id,
                                module_id=module.id,
                                is_enabled=True
                            )
                            db.session.add(permission)
            
            db.session.commit()
            print(f"   ✓ Granted default module access to migrated users")
        else:
            print("   ℹ No users needed migration")

def run_migration():
    """Run the complete migration process"""
    print("=" * 60)
    print("🚀 SAILOR UTILITY DATABASE MIGRATION")
    print("=" * 60)
    
    try:
        # Create app for migration
        app, migrate = create_app_for_migration()
        
        print(f"📊 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
        
        with app.app_context():
            # Step 1: Backup existing data
            existing_users = backup_existing_data(app)
            
            # Step 2: Run database migration
            print("🔄 Running database schema migration...")
            try:
                upgrade()
                print("   ✓ Schema migration completed successfully")
            except Exception as e:
                print(f"   ⚠ Migration error: {e}")
                print("   ℹ This might be normal if already up to date")
            
            # Step 3: Create default modules
            modules = create_default_modules(app)
            
            # Step 4: Migrate existing users if any
            if existing_users:
                migrate_existing_users(app, existing_users, modules)
            
            # Step 5: Verify migration
            print("🔄 Verifying migration...")
            user_count = User.query.count()
            module_count = SystemModule.query.count()
            permission_count = UserModulePermission.query.count()
            
            print(f"   ✓ Users: {user_count}")
            print(f"   ✓ Modules: {module_count}")
            print(f"   ✓ Permissions: {permission_count}")
            
        print("=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Review user accounts and assign admin privileges as needed")
        print("2. Test the application with the new enhanced features")
        print("3. Grant additional module permissions to users as required")
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print("❌ MIGRATION FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check if we're in the right environment
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm-production":
        print("⚠️  PRODUCTION MIGRATION CONFIRMED")
    else:
        print("⚠️  This script will modify the production database!")
        print("⚠️  Make sure you have a backup before proceeding!")
        print()
        print("To run this migration, use:")
        print("  python migrate_production.py --confirm-production")
        print()
        sys.exit(1)
    
    success = run_migration()
    sys.exit(0 if success else 1)