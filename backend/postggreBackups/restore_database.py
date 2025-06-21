#!/usr/bin/env python3
"""
Database Restoration Script
Restores PostgreSQL database from backup file
"""

import os
import sys
import subprocess
from datetime import datetime
from urllib.parse import urlparse

def list_backup_files():
    """List available backup files"""
    backups_dir = os.path.dirname(__file__)
    
    if not os.path.exists(backups_dir):
        print("❌ No backups directory found.")
        return []
    
    backup_files = [f for f in os.listdir(backups_dir) if f.endswith('.sql')]
    
    if not backup_files:
        print("❌ No backup files found in current directory.")
        return []
    
    print("\n📁 Available backup files:")
    print("-" * 60)
    
    for i, backup_file in enumerate(sorted(backup_files, reverse=True), 1):
        backup_path = os.path.join(backups_dir, backup_file)
        size = os.path.getsize(backup_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        
        print(f"{i}. {backup_file}")
        print(f"   Size: {size:,} bytes")
        print(f"   Date: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    return backup_files

def restore_database(db_url, backup_file_path, target_db_name=None):
    """Restore database from backup file"""
    
    # Parse database URL
    parsed = urlparse(db_url)
    
    if target_db_name:
        # Use different target database name
        db_name = target_db_name
    else:
        # Use original database name
        db_name = parsed.path[1:]  # Remove leading slash
    
    print(f"🚀 Starting Database Restoration...")
    print("=" * 50)
    print(f"📍 Database Host: {parsed.hostname}:{parsed.port}")
    print(f"👤 Username: {parsed.username}")
    print(f"🗃️  Target Database: {db_name}")
    print(f"📄 Backup File: {backup_file_path}")
    print("=" * 50)
    
    try:
        # Set up environment
        env = os.environ.copy()
        if parsed.password:
            env['PGPASSWORD'] = parsed.password
        
        # Step 1: Test connection
        print("\n🔍 Testing database connection...")
        test_cmd = [
            'psql',
            '--host', parsed.hostname,
            '--port', str(parsed.port or 5432),
            '--username', parsed.username,
            '--dbname', 'postgres',  # Connect to postgres db first
            '--command', 'SELECT version();'
        ]
        
        result = subprocess.run(test_cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Database connection failed:")
            print(f"Error: {result.stderr}")
            return False
        
        print("✅ Database connection successful")
        
        # Step 2: Ask about dropping existing database
        if not target_db_name:
            print(f"\n⚠️  WARNING: This will COMPLETELY REPLACE the existing database '{db_name}'")
            print("All current data will be LOST!")
            response = input("Are you sure you want to continue? (yes/no): ").strip().lower()
            
            if response not in ['yes', 'y']:
                print("Restoration cancelled.")
                return False
            
            # Drop and recreate database
            print(f"\n🗑️  Dropping existing database '{db_name}'...")
            drop_cmd = [
                'psql',
                '--host', parsed.hostname,
                '--port', str(parsed.port or 5432),
                '--username', parsed.username,
                '--dbname', 'postgres',
                '--command', f'DROP DATABASE IF EXISTS "{db_name}";'
            ]
            
            result = subprocess.run(drop_cmd, env=env, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to drop database:")
                print(f"Error: {result.stderr}")
                return False
            
            print(f"✅ Database '{db_name}' dropped")
        
        # Step 3: Create database
        print(f"\n🔨 Creating database '{db_name}'...")
        create_cmd = [
            'psql',
            '--host', parsed.hostname,
            '--port', str(parsed.port or 5432),
            '--username', parsed.username,
            '--dbname', 'postgres',
            '--command', f'CREATE DATABASE "{db_name}";'
        ]
        
        result = subprocess.run(create_cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0 and "already exists" not in result.stderr:
            print(f"❌ Failed to create database:")
            print(f"Error: {result.stderr}")
            return False
        
        print(f"✅ Database '{db_name}' ready")
        
        # Step 4: Restore from backup
        print(f"\n📥 Restoring data from backup...")
        print("This may take a few minutes...")
        
        restore_cmd = [
            'psql',
            '--host', parsed.hostname,
            '--port', str(parsed.port or 5432),
            '--username', parsed.username,
            '--dbname', db_name,
            '--file', backup_file_path,
            '--verbose'
        ]
        
        result = subprocess.run(restore_cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Database restoration completed successfully!")
            
            # Step 5: Verify restoration
            print(f"\n🔍 Verifying restoration...")
            verify_cmd = [
                'psql',
                '--host', parsed.hostname,
                '--port', str(parsed.port or 5432),
                '--username', parsed.username,
                '--dbname', db_name,
                '--command', '''
                SELECT 
                    schemaname,
                    tablename,
                    n_tup_ins as "Rows"
                FROM pg_stat_user_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename;
                '''
            ]
            
            result = subprocess.run(verify_cmd, env=env, capture_output=True, text=True)
            if result.returncode == 0:
                print("📊 Database tables and row counts:")
                print(result.stdout)
            
            print("🎉 Restoration completed successfully!")
            return True
        else:
            print(f"\n❌ Restoration failed:")
            print(f"Return code: {result.returncode}")
            print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return False
            
    except FileNotFoundError:
        print(f"\n❌ PostgreSQL client tools not found!")
        print("Please install PostgreSQL client:")
        print("  macOS: brew install postgresql")
        print("  Ubuntu: sudo apt-get install postgresql-client")
        return False
    except Exception as e:
        print(f"\n❌ Restoration failed with error:")
        print(f"Error: {str(e)}")
        return False

def main():
    print("PostgreSQL Database Restoration Tool")
    print("=" * 50)
    
    # List available backups
    backup_files = list_backup_files()
    if not backup_files:
        return
    
    # Let user select backup file
    while True:
        try:
            choice = input(f"\nSelect backup file (1-{len(backup_files)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(backup_files):
                selected_backup = sorted(backup_files, reverse=True)[choice_num - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(backup_files)}")
        except ValueError:
            print("Please enter a valid number")
    
    backup_file_path = os.path.join(os.path.dirname(__file__), selected_backup)
    print(f"\n📄 Selected: {selected_backup}")
    
    # Ask for target database name
    print(f"\nRestore options:")
    print(f"1. Replace existing database (DESTRUCTIVE)")
    print(f"2. Restore to new database (SAFE)")
    
    while True:
        option = input("Choose option (1 or 2): ").strip()
        if option == '1':
            target_db = None
            break
        elif option == '2':
            target_db = input("Enter new database name: ").strip()
            if target_db:
                break
            print("Please enter a valid database name")
        else:
            print("Please enter 1 or 2")
    
    # Database URL
    db_url = "postgresql://pi_user:mypassword123@192.168.1.165:5432/pi_server_db"
    
    # Perform restoration
    success = restore_database(db_url, backup_file_path, target_db)
    
    if success:
        print(f"\n🎉 Database restoration completed!")
        if target_db:
            print(f"Database restored as: {target_db}")
            print(f"To switch your app to use this database, update DATABASE_URL to:")
            print(f"postgresql://pi_user:mypassword123@192.168.1.165:5432/{target_db}")
    else:
        print(f"\n❌ Database restoration failed!")

if __name__ == "__main__":
    main()