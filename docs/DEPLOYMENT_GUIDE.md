# Sailor Utility Deployment Guide

## Database Migration for Production PostgreSQL

### Prerequisites
- PostgreSQL database running
- Database credentials configured in environment variables
- Backup of existing database (CRITICAL!)

### Environment Variables Required
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name
# OR individual components:
DB_HOST=your_postgres_host
DB_PORT=5432
DB_NAME=sailor_utility
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

### Migration Process

#### 1. Backup Current Database
```bash
# Create a full backup before migration
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql
```

#### 2. Run Migration Script
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Run production migration
python migrate_production.py --confirm-production
```

#### 3. Verify Migration
The migration script will:
- ✅ Backup existing user data
- ✅ Apply database schema changes
- ✅ Create default system modules
- ✅ Migrate existing users to enhanced model
- ✅ Grant default module permissions
- ✅ Verify final state

### Manual Migration (Alternative)

If the automated script fails, you can run migrations manually:

```bash
# Initialize migration (if first time)
flask db init

# Create migration
flask db migrate -m "Enhanced user model and modular system"

# Apply migration
flask db upgrade
```

### Post-Migration Tasks

#### 1. Assign Admin Privileges
```sql
-- Connect to PostgreSQL and assign admin to specific users
UPDATE "user" SET is_admin = true WHERE username = 'your_admin_username';
```

#### 2. Create Default Data
Run the following script to ensure default modules exist:

```bash
python -c "
from app import app
from models import db, SystemModule
from migrate_production import create_default_modules

with app.app_context():
    create_default_modules(app)
"
```

#### 3. Test Application
- ✅ Verify login works with existing users
- ✅ Check that enhanced user fields are populated
- ✅ Confirm module system is functional
- ✅ Test admin panel access for admin users

### Rollback Procedure

If migration fails and you need to rollback:

```bash
# Restore from backup
psql $DATABASE_URL < backup_YYYYMMDD_HHMMSS.sql

# Or use Flask-Migrate downgrade
flask db downgrade
```

### Schema Changes Summary

#### Enhanced User Table
- ➕ `is_admin` (BOOLEAN)
- ➕ `first_name` (VARCHAR(50))
- ➕ `last_name` (VARCHAR(50))
- ➕ `phone` (VARCHAR(20))
- ➕ `emergency_contact` (VARCHAR(200))
- ➕ `sailing_experience` (VARCHAR(20))
- ➕ `certifications` (TEXT - JSON)
- ➕ `default_module` (VARCHAR(50))
- ➕ `profile_image_path` (VARCHAR(255))
- ➕ `last_login` (DATETIME)
- ➕ `timezone` (VARCHAR(50))

#### New Tables
- ➕ `system_modules` - Module definitions
- ➕ `user_module_permissions` - User access control
- ➕ `user_preferences` - User customization

### Troubleshooting

#### Common Issues

**1. Connection Error**
```
Error: could not connect to server
```
Solution: Verify DATABASE_URL and network connectivity

**2. Permission Denied**
```
Error: permission denied for table user
```
Solution: Ensure database user has DDL privileges

**3. Column Already Exists**
```
Error: column "is_admin" of relation "user" already exists
```
Solution: Migration already applied or partial completion. Check current schema.

**4. Foreign Key Violations**
```
Error: violates foreign key constraint
```
Solution: Ensure referential integrity. May need to clean orphaned data.

#### Getting Help

1. Check migration logs in detail
2. Verify database connection
3. Ensure all dependencies are installed
4. Review the migration script output
5. Check PostgreSQL logs for detailed errors

### Development vs Production

#### Development (SQLite)
```bash
# Simple migration for development
flask db upgrade
```

#### Production (PostgreSQL)
```bash
# Use the comprehensive migration script
python migrate_production.py --confirm-production
```

### Security Considerations

- 🔒 Always backup before migration
- 🔒 Run migrations in maintenance window
- 🔒 Verify user permissions after migration
- 🔒 Test thoroughly in staging environment first
- 🔒 Monitor application logs after deployment

---

**⚠️ IMPORTANT**: Always test migrations on a staging environment that matches production before applying to live data!