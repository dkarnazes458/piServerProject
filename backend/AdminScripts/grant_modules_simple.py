#!/usr/bin/env python3
"""
Simple Module Grant Script

This script grants access to all available modules for a specified user.
Uses direct SQLite commands instead of Flask for simplicity.

Usage:
  python3 grant_modules_simple.py <username_or_email>
  python3 grant_modules_simple.py --admin <username_or_email>
"""

import sys
import sqlite3
import os
from datetime import datetime

def connect_to_db():
    """Connect to the SQLite database"""
    db_path = os.path.join(os.path.dirname(__file__), 'app.db')
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        print("Make sure you're running this from the backend directory and the database exists.")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def find_user(conn, identifier):
    """Find user by username or email"""
    cursor = conn.cursor()
    
    # Try username first
    cursor.execute("SELECT * FROM user WHERE username = ?", (identifier,))
    user = cursor.fetchone()
    
    if not user:
        # Try email
        cursor.execute("SELECT * FROM user WHERE email = ?", (identifier,))
        user = cursor.fetchone()
    
    return user

def get_all_modules(conn):
    """Get all active system modules"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM system_modules WHERE is_active = 1 ORDER BY sort_order")
    return cursor.fetchall()

def create_default_modules(conn):
    """Create default system modules if they don't exist"""
    default_modules = [
        ('dashboard', 'Dashboard', 'Main dashboard with overview and statistics', 'dashboard', 1, 0),
        ('boats', 'Fleet Management', 'Manage your boats and fleet information', 'boat', 2, 0),
        ('trips', 'Trip Logbook', 'Log and track your sailing trips with GPS support', 'map', 3, 0),
        ('equipment', 'Equipment Tracker', 'Manage your sailing equipment and inventory', 'tools', 4, 0),
        ('maintenance', 'Maintenance Log', 'Track maintenance records and schedules', 'wrench', 5, 0),
        ('events', 'Events Calendar', 'Manage sailing events, races, and gatherings', 'calendar', 6, 0),
        ('navigation', 'Weather & Routes', 'Weather information and route planning tools', 'compass', 7, 0),
        ('social', 'Crew Network', 'Connect with other sailors and crew members', 'users', 8, 0),
        ('admin', 'Admin Panel', 'System administration and user management', 'settings', 9, 1)
    ]
    
    cursor = conn.cursor()
    now = datetime.utcnow().isoformat()
    
    for name, display_name, description, icon, sort_order, requires_admin in default_modules:
        # Check if module already exists
        cursor.execute("SELECT id FROM system_modules WHERE name = ?", (name,))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO system_modules 
                (name, display_name, description, icon, is_active, requires_admin, sort_order, created_at, updated_at)
                VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?)
            """, (name, display_name, description, icon, requires_admin, sort_order, now, now))
    
    conn.commit()

def grant_all_modules(identifier, make_admin=False):
    """Grant all module permissions to a user"""
    conn = connect_to_db()
    if not conn:
        return False
    
    try:
        print(f"🔍 Looking for user: {identifier}")
        
        # Find the user
        user = find_user(conn, identifier)
        if not user:
            print(f"❌ User '{identifier}' not found!")
            
            # Show available users
            cursor = conn.cursor()
            cursor.execute("SELECT username, email FROM user")
            users = cursor.fetchall()
            if users:
                print("Available users:")
                for u in users:
                    print(f"  - {u['username']} ({u['email']})")
            return False
        
        print(f"✅ Found user: {user['username']} ({user['email']})")
        
        # Make admin if requested
        if make_admin and not user['is_admin']:
            cursor = conn.cursor()
            cursor.execute("UPDATE user SET is_admin = 1 WHERE id = ?", (user['id'],))
            print(f"🛡️  Granted admin privileges to {user['username']}")
        
        # Get or create modules
        modules = get_all_modules(conn)
        if not modules:
            print("⚠️  No active modules found! Creating default modules...")
            create_default_modules(conn)
            modules = get_all_modules(conn)
        
        print(f"📦 Found {len(modules)} active modules:")
        for module in modules:
            print(f"  - {module['name']} ({module['display_name']})")
        
        # Grant permissions for all modules
        cursor = conn.cursor()
        granted_count = 0
        updated_count = 0
        now = datetime.utcnow().isoformat()
        
        for module in modules:
            # Check if permission already exists
            cursor.execute("""
                SELECT id, is_enabled FROM user_module_permissions 
                WHERE user_id = ? AND module_id = ?
            """, (user['id'], module['id']))
            
            existing = cursor.fetchone()
            
            if existing:
                if not existing['is_enabled']:
                    cursor.execute("""
                        UPDATE user_module_permissions 
                        SET is_enabled = 1 
                        WHERE id = ?
                    """, (existing['id'],))
                    updated_count += 1
                    print(f"  ✓ Re-enabled {module['name']}")
                else:
                    print(f"  → Already has {module['name']}")
            else:
                # Create new permission
                cursor.execute("""
                    INSERT INTO user_module_permissions 
                    (user_id, module_id, is_enabled, granted_at, granted_by)
                    VALUES (?, ?, 1, ?, ?)
                """, (user['id'], module['id'], now, user['id']))
                granted_count += 1
                print(f"  ✅ Granted {module['name']}")
        
        # Commit all changes
        conn.commit()
        
        print(f"\n🎉 Success!")
        print(f"   - Granted {granted_count} new module permissions")
        print(f"   - Updated {updated_count} existing permissions")
        
        # Check final admin status
        cursor.execute("SELECT is_admin FROM user WHERE id = ?", (user['id'],))
        is_admin = cursor.fetchone()['is_admin']
        if make_admin:
            print(f"   - Admin privileges: {'✅' if is_admin else '❌'}")
        
        print(f"\n📊 Final status for {user['username']}:")
        print(f"   - Admin: {'Yes' if is_admin else 'No'}")
        print(f"   - Total modules: {len(modules)}")
        
        # Show current permissions
        cursor.execute("""
            SELECT sm.name 
            FROM user_module_permissions ump
            JOIN system_modules sm ON ump.module_id = sm.id
            WHERE ump.user_id = ? AND ump.is_enabled = 1
            ORDER BY sm.sort_order
        """, (user['id'],))
        
        enabled_modules = cursor.fetchall()
        print(f"   - Enabled modules: {len(enabled_modules)}")
        for mod in enabled_modules:
            print(f"     • {mod['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

def show_usage():
    """Show usage information"""
    print("Grant All Modules Script (Simple)")
    print("=" * 35)
    print()
    print("Usage:")
    print("  python3 grant_modules_simple.py <username_or_email>")
    print("  python3 grant_modules_simple.py --admin <username_or_email>")
    print()
    print("Examples:")
    print("  python3 grant_modules_simple.py john_doe")
    print("  python3 grant_modules_simple.py john@example.com")
    print("  python3 grant_modules_simple.py --admin admin@example.com")
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