#!/bin/bash
# Comprehensive PostgreSQL Backup Script
# Creates backup with users, roles, and permissions

set -e  # Exit on any error

# Configuration
DB_HOST="127.0.0.1"
DB_PORT="5432"
DB_NAME="pi_server_db"
DB_USER="admin_user"
BACKUP_DIR="$(dirname "$0")"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory
mkdir -p "$BACKUP_DIR"

# File names
GLOBALS_BACKUP="$BACKUP_DIR/globals_${TIMESTAMP}.sql"
DATABASE_BACKUP="$BACKUP_DIR/database_${TIMESTAMP}.sql"
COMBINED_BACKUP="$BACKUP_DIR/complete_backup_${TIMESTAMP}.sql"

echo "🚀 Starting Comprehensive PostgreSQL Backup..."
echo "=" * 60
echo "📍 Database: $DB_HOST:$DB_PORT/$DB_NAME"
echo "💾 Backup directory: $BACKUP_DIR"

# Step 1: Backup global objects (users, roles)
echo ""
echo "🔄 Step 1: Backing up users and roles..."
PGPASSWORD="Trinitron\$9d2" pg_dumpall \
  --host="$DB_HOST" \
  --port="$DB_PORT" \
  --username="$DB_USER" \
  --globals-only \
  --verbose \
  --file="$GLOBALS_BACKUP"

echo "✅ Global objects backup completed"

# Step 2: Backup database with schema and data
echo ""
echo "🔄 Step 2: Backing up database with permissions..."
PGPASSWORD="Trinitron\$9d2" pg_dump \
  --host="$DB_HOST" \
  --port="$DB_PORT" \
  --username="$DB_USER" \
  --dbname="$DB_NAME" \
  --verbose \
  --clean \
  --create \
  --file="$DATABASE_BACKUP"

echo "✅ Database backup completed"

# Step 3: Create combined backup
echo ""
echo "🔄 Step 3: Creating combined backup file..."

cat > "$COMBINED_BACKUP" << EOF
-- ========================================
-- COMPLETE POSTGRESQL BACKUP
-- Created: $(date --iso-8601=seconds)
-- Database: $DB_NAME
-- Host: $DB_HOST:$DB_PORT
-- ========================================

-- ========================================
-- GLOBAL OBJECTS (Users, Roles, etc.)
-- ========================================

EOF

cat "$GLOBALS_BACKUP" >> "$COMBINED_BACKUP"

cat >> "$COMBINED_BACKUP" << EOF

-- ========================================
-- DATABASE WITH SCHEMA AND DATA
-- ========================================

EOF

cat "$DATABASE_BACKUP" >> "$COMBINED_BACKUP"

# Get file sizes
GLOBALS_SIZE=$(stat -c%s "$GLOBALS_BACKUP" 2>/dev/null || stat -f%z "$GLOBALS_BACKUP" 2>/dev/null || echo "unknown")
DATABASE_SIZE=$(stat -c%s "$DATABASE_BACKUP" 2>/dev/null || stat -f%z "$DATABASE_BACKUP" 2>/dev/null || echo "unknown")
COMBINED_SIZE=$(stat -c%s "$COMBINED_BACKUP" 2>/dev/null || stat -f%z "$COMBINED_BACKUP" 2>/dev/null || echo "unknown")

echo "✅ Combined backup created"
echo ""
echo "📊 Backup Summary:"
echo "   • Globals: $GLOBALS_SIZE bytes"
echo "   • Database: $DATABASE_SIZE bytes"
echo "   • Combined: $COMBINED_SIZE bytes"
echo ""

# Create restoration instructions
INSTRUCTIONS_FILE="${COMBINED_BACKUP%.*}_RESTORE_INSTRUCTIONS.txt"
cat > "$INSTRUCTIONS_FILE" << EOF
COMPLETE DATABASE RESTORATION INSTRUCTIONS
==================================================

This backup includes users, roles, permissions, schema, and data.

RESTORATION STEPS:
------------------

1. Stop the application to prevent connections:
   sudo pkill -f "python.*app.py"
   sudo pkill -f "npm.*dev"

2. Connect as postgres superuser:
   sudo -u postgres psql

3. Drop existing database (CAREFUL!):
   DROP DATABASE IF EXISTS $DB_NAME;

4. Exit psql and restore:
   \q
   sudo -u postgres psql < $(basename "$COMBINED_BACKUP")

5. Restart application:
   cd ~/code/piServerProject/backend
   source venv/bin/activate
   python app.py &
   
   cd ../frontend
   npm run dev &

VERIFICATION:
-------------
After restoration, verify:
1. Users exist: \du
2. Database exists: \l
3. Tables exist: \dt
4. Permissions work: SELECT count(*) FROM "user";

BACKUP CREATED: $(date)
BACKUP FILE: $(basename "$COMBINED_BACKUP")
EOF

echo "📋 Restoration instructions: $INSTRUCTIONS_FILE"
echo ""
echo "🎉 Comprehensive backup completed successfully!"
echo "📁 Main backup file: $COMBINED_BACKUP"
echo ""
echo "💡 This backup includes everything needed for complete restoration"
echo "   including users, roles, permissions, schema, and all data."