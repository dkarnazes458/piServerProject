#!/usr/bin/env python3
"""
Comprehensive Production Database Backup Script
Creates a full backup of PostgreSQL database including users, roles, and permissions
"""

import os
import sys
import subprocess
from datetime import datetime
from urllib.parse import urlparse

def backup_database_with_permissions(db_url, backup_dir=None):
    """Create comprehensive backup including users and permissions"""
    
    # Use script directory if no backup_dir specified
    if backup_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_dir = script_dir
    
    print("💾 Starting Comprehensive PostgreSQL Backup...")
    print("=" * 60)
    
    if not db_url or not db_url.startswith('postgresql'):
        print("❌ ERROR: Must be PostgreSQL database")
        return False
    
    # Parse database URL
    parsed = urlparse(db_url)
    
    # Generate backup filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create backups directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # File paths
    database_backup = os.path.join(backup_dir, f"database_full_{timestamp}.sql")
    globals_backup = os.path.join(backup_dir, f"globals_roles_{timestamp}.sql")
    combined_backup = os.path.join(backup_dir, f"complete_backup_{timestamp}.sql")
    
    print(f"📍 Database: {parsed.hostname}:{parsed.port}/{parsed.path[1:]}")
    print(f"💾 Database backup: {database_backup}")
    print(f"👥 Globals backup: {globals_backup}")
    print(f"📦 Combined backup: {combined_backup}")
    
    try:
        # Set up environment
        env = os.environ.copy()
        if parsed.password:
            env['PGPASSWORD'] = parsed.password
        
        # Step 1: Backup global objects (users, roles, tablespaces)
        print(f"\n🔄 Step 1: Backing up global objects (users, roles)...")
        globals_cmd = [
            'pg_dumpall',
            '--host', parsed.hostname,
            '--port', str(parsed.port or 5432),
            '--username', parsed.username,
            '--globals-only',  # Only dump roles, users, tablespaces
            '--verbose',
            '--file', globals_backup
        ]
        
        result = subprocess.run(globals_cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Global objects backup failed:")
            print(f"Error: {result.stderr}")
            return False
        
        print(f"✅ Global objects backup completed")
        
        # Step 2: Backup database with permissions
        print(f"\n🔄 Step 2: Backing up database with permissions...")
        database_cmd = [
            'pg_dump',
            '--host', parsed.hostname,
            '--port', str(parsed.port or 5432),
            '--username', parsed.username,
            '--dbname', parsed.path[1:],  # Remove leading slash
            '--verbose',
            '--clean',
            '--create',  # Include CREATE DATABASE statement
            '--schema-only',  # First get schema with permissions
            '--file', f"{database_backup}.schema"
        ]
        
        result = subprocess.run(database_cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Database schema backup failed:")
            print(f"Error: {result.stderr}")
            return False
        
        # Step 3: Backup database data
        print(f"\n🔄 Step 3: Backing up database data...")
        data_cmd = [
            'pg_dump',
            '--host', parsed.hostname,
            '--port', str(parsed.port or 5432),
            '--username', parsed.username,
            '--dbname', parsed.path[1:],
            '--verbose',
            '--data-only',  # Only data
            '--file', f"{database_backup}.data"
        ]
        
        result = subprocess.run(data_cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Database data backup failed:")
            print(f"Error: {result.stderr}")
            return False
        
        # Step 4: Create combined backup file
        print(f"\n🔄 Step 4: Creating combined backup file...")
        
        with open(combined_backup, 'w') as combined:
            combined.write("-- ========================================\n")
            combined.write("-- COMPLETE POSTGRESQL BACKUP\n")
            combined.write(f"-- Created: {datetime.now().isoformat()}\n")
            combined.write(f"-- Database: {parsed.path[1:]}\n")
            combined.write(f"-- Host: {parsed.hostname}:{parsed.port}\n")
            combined.write("-- ========================================\n\n")
            
            # Add global objects (users, roles)
            combined.write("-- ========================================\n")
            combined.write("-- GLOBAL OBJECTS (Users, Roles, etc.)\n")
            combined.write("-- ========================================\n\n")
            
            with open(globals_backup, 'r') as f:
                combined.write(f.read())
            
            combined.write("\n\n")
            
            # Add database schema with permissions
            combined.write("-- ========================================\n")
            combined.write("-- DATABASE SCHEMA WITH PERMISSIONS\n")
            combined.write("-- ========================================\n\n")
            
            with open(f"{database_backup}.schema", 'r') as f:
                combined.write(f.read())
            
            combined.write("\n\n")
            
            # Add database data
            combined.write("-- ========================================\n")
            combined.write("-- DATABASE DATA\n")
            combined.write("-- ========================================\n\n")
            
            with open(f"{database_backup}.data", 'r') as f:
                combined.write(f.read())
        
        # Clean up temporary files
        os.remove(f"{database_backup}.schema")
        os.remove(f"{database_backup}.data")
        
        # Check file sizes
        globals_size = os.path.getsize(globals_backup)
        combined_size = os.path.getsize(combined_backup)
        
        print(f"\n✅ Comprehensive backup completed successfully!")
        print(f"📦 Globals backup: {globals_size:,} bytes")
        print(f"📦 Combined backup: {combined_size:,} bytes")
        
        return True
        
    except FileNotFoundError:
        print(f"\n❌ PostgreSQL client tools not found!")
        print("Please install PostgreSQL client:")
        print("  macOS: brew install postgresql")
        print("  Ubuntu: sudo apt-get install postgresql-client")
        return False
    except Exception as e:
        print(f"\n❌ Backup failed with error:")
        print(f"Error: {str(e)}")
        return False

def create_restore_instructions(backup_file):
    """Create restoration instructions"""
    instructions_file = backup_file.replace('.sql', '_RESTORE_INSTRUCTIONS.txt')
    
    with open(instructions_file, 'w') as f:
        f.write("COMPLETE DATABASE RESTORATION INSTRUCTIONS\n")
        f.write("=" * 50 + "\n\n")
        f.write("This backup includes users, roles, permissions, schema, and data.\n\n")
        f.write("RESTORATION STEPS:\n")
        f.write("-" * 20 + "\n\n")
        f.write("1. Stop the application to prevent connections:\n")
        f.write("   sudo systemctl stop your-app-service\n\n")
        f.write("2. Connect as postgres superuser:\n")
        f.write("   sudo -u postgres psql\n\n")
        f.write("3. Drop existing database (CAREFUL!):\n")
        f.write("   DROP DATABASE IF EXISTS pi_server_db;\n\n")
        f.write("4. Exit psql and restore:\n")
        f.write("   \\q\n")
        f.write(f"   psql -U postgres < {os.path.basename(backup_file)}\n\n")
        f.write("5. Restart application:\n")
        f.write("   sudo systemctl start your-app-service\n\n")
        f.write("ALTERNATIVE - Restore to new database:\n")
        f.write("-" * 40 + "\n")
        f.write("To restore to a different database name, edit the backup file\n")
        f.write("and change 'CREATE DATABASE pi_server_db' to your desired name.\n\n")
        f.write("VERIFICATION:\n")
        f.write("-" * 15 + "\n")
        f.write("After restoration, verify:\n")
        f.write("1. Users exist: \\du\n")
        f.write("2. Database exists: \\l\n")
        f.write("3. Tables exist: \\dt\n")
        f.write("4. Permissions work: SELECT count(*) FROM \"user\";\n")
    
    return instructions_file

def main():
    print("Comprehensive PostgreSQL Database Backup Tool")
    print("=" * 50)
    print("This creates a complete backup including:")
    print("• Database schema with permissions")
    print("• All data")
    print("• Users and roles")
    print("• Tablespaces and global objects")
    print()
    
    # Database URL
    db_url = "postgresql://admin_user:Trinitron$9d2@192.168.1.165:5432/pi_server_db"
    
    # Confirm before proceeding
    response = input("Create comprehensive backup? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Backup cancelled.")
        return
    
    # Create backup
    success = backup_database_with_permissions(db_url)
    
    if success:
        # Find the most recent combined backup in script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backup_files = [f for f in os.listdir(script_dir) if f.startswith("complete_backup_") and f.endswith(".sql")]
        if backup_files:
            latest_backup = os.path.join(script_dir, sorted(backup_files)[-1])
            instructions_file = create_restore_instructions(latest_backup)
            
            print(f"\n📋 Restoration instructions created: {instructions_file}")
            print(f"\n🎉 Complete backup ready!")
            print(f"📁 Backup file: {latest_backup}")
            print(f"💡 This backup includes everything needed for full restoration")
    else:
        print(f"\n❌ Backup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()