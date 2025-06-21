#!/usr/bin/env python3
"""
Database Permissions Diagnostic Script
Checks PostgreSQL users, permissions, and database access
"""

import os
import sys
import subprocess
from urllib.parse import urlparse

def run_psql_command(host, port, username, database, command, password=None):
    """Run a psql command and return the result"""
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password
    
    cmd = [
        'psql',
        '--host', host,
        '--port', str(port),
        '--username', username,
        '--dbname', database,
        '--command', command,
        '--tuples-only',
        '--no-align'
    ]
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Connection timeout"
    except Exception as e:
        return False, "", str(e)

def check_database_access():
    """Check database access and permissions"""
    
    # Database connection details
    host = "192.168.1.165"
    port = 5432
    username = "pi_user"
    password = "mypassword123"
    database = "pi_server_db"
    
    print("🔍 PostgreSQL Database Permissions Diagnostic")
    print("=" * 50)
    print(f"Host: {host}:{port}")
    print(f"Username: {username}")
    print(f"Database: {database}")
    print("=" * 50)
    
    # Test 1: Basic connection
    print("\n1. Testing basic database connection...")
    success, output, error = run_psql_command(
        host, port, username, "postgres", "SELECT version();", password
    )
    
    if success:
        print("✅ Can connect to PostgreSQL server")
        print(f"   Version: {output.split(',')[0] if output else 'Unknown'}")
    else:
        print("❌ Cannot connect to PostgreSQL server")
        print(f"   Error: {error}")
        return False
    
    # Test 2: Check user privileges
    print("\n2. Checking user privileges...")
    success, output, error = run_psql_command(
        host, port, username, "postgres", 
        f"SELECT usename, usesuper, usecreatedb, usecreaterole FROM pg_user WHERE usename = '{username}';",
        password
    )
    
    if success and output:
        parts = output.split('|')
        if len(parts) >= 4:
            print(f"✅ User '{username}' exists")
            print(f"   Superuser: {'Yes' if parts[1] == 't' else 'No'}")
            print(f"   Create DB: {'Yes' if parts[2] == 't' else 'No'}")
            print(f"   Create Role: {'Yes' if parts[3] == 't' else 'No'}")
        else:
            print(f"⚠️  User '{username}' found but details unclear")
    else:
        print(f"❌ User '{username}' not found or no access")
        print(f"   Error: {error}")
    
    # Test 3: List all databases
    print("\n3. Checking database access...")
    success, output, error = run_psql_command(
        host, port, username, "postgres",
        "SELECT datname FROM pg_database WHERE datistemplate = false;",
        password
    )
    
    if success:
        databases = output.split('\n') if output else []
        print(f"✅ Can list databases: {', '.join(databases)}")
        
        if database in databases:
            print(f"✅ Target database '{database}' exists")
        else:
            print(f"❌ Target database '{database}' not found")
            return False
    else:
        print("❌ Cannot list databases")
        print(f"   Error: {error}")
    
    # Test 4: Connect to target database
    print(f"\n4. Testing connection to target database '{database}'...")
    success, output, error = run_psql_command(
        host, port, username, database, "SELECT current_user, current_database();", password
    )
    
    if success:
        print(f"✅ Can connect to database '{database}'")
        print(f"   Current user: {output.split('|')[0] if '|' in output else output}")
    else:
        print(f"❌ Cannot connect to database '{database}'")
        print(f"   Error: {error}")
        return False
    
    # Test 5: Check table permissions
    print(f"\n5. Checking table access in '{database}'...")
    success, output, error = run_psql_command(
        host, port, username, database,
        "SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;",
        password
    )
    
    if success:
        tables = output.split('\n') if output else []
        if tables and tables[0]:
            print(f"✅ Can list tables: {', '.join(tables)}")
            
            # Test table permissions
            test_table = tables[0]
            success, output, error = run_psql_command(
                host, port, username, database,
                f"SELECT COUNT(*) FROM {test_table};",
                password
            )
            
            if success:
                print(f"✅ Can read from table '{test_table}'")
            else:
                print(f"❌ Cannot read from table '{test_table}'")
                print(f"   Error: {error}")
        else:
            print("⚠️  No tables found in database")
    else:
        print("❌ Cannot list tables")
        print(f"   Error: {error}")
    
    # Test 6: Check schema permissions
    print(f"\n6. Checking schema permissions...")
    success, output, error = run_psql_command(
        host, port, username, database,
        f"""
        SELECT 
            has_database_privilege('{username}', '{database}', 'CONNECT') as can_connect,
            has_database_privilege('{username}', '{database}', 'CREATE') as can_create,
            has_schema_privilege('{username}', 'public', 'CREATE') as can_create_schema,
            has_schema_privilege('{username}', 'public', 'USAGE') as can_use_schema;
        """,
        password
    )
    
    if success and output:
        parts = output.split('|')
        if len(parts) >= 4:
            print(f"✅ Database privileges:")
            print(f"   Connect: {'Yes' if parts[0] == 't' else 'No'}")
            print(f"   Create: {'Yes' if parts[1] == 't' else 'No'}")
            print(f"   Schema Create: {'Yes' if parts[2] == 't' else 'No'}")
            print(f"   Schema Usage: {'Yes' if parts[3] == 't' else 'No'}")
    
    print("\n" + "=" * 50)
    print("🎉 Diagnostic completed!")
    
    return True

def suggest_fixes():
    """Suggest fixes for common permission issues"""
    print("\n🔧 Common Permission Fixes:")
    print("-" * 30)
    print("If you're having permission issues, try these commands on the Raspberry Pi:")
    print()
    print("1. Connect as postgres superuser:")
    print("   sudo -u postgres psql")
    print()
    print("2. Grant superuser privileges:")
    print("   ALTER USER pi_user WITH SUPERUSER;")
    print()
    print("3. Grant database ownership:")
    print("   ALTER DATABASE pi_server_db OWNER TO pi_user;")
    print()
    print("4. Grant all privileges:")
    print("   GRANT ALL PRIVILEGES ON DATABASE pi_server_db TO pi_user;")
    print()
    print("5. For existing tables:")
    print("   \\c pi_server_db;")
    print("   GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO pi_user;")
    print("   GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pi_user;")

if __name__ == "__main__":
    try:
        success = check_database_access()
        if not success:
            suggest_fixes()
    except KeyboardInterrupt:
        print("\n\nDiagnostic cancelled by user.")
    except Exception as e:
        print(f"\n❌ Diagnostic failed with error: {str(e)}")
        suggest_fixes()