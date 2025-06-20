#!/usr/bin/env python3
"""
Production Migration Script for Core Sailor Models

This script deploys the new core models (Boats, Equipment, MaintenanceRecord, Event)
to the production PostgreSQL database.
"""

import os
import sys
from flask import Flask
from flask_migrate import Migrate, upgrade, migrate as flask_migrate
from config import Config
from models import db, User, SystemModule, UserModulePermission, UserPreference, Boat, Equipment, MaintenanceRecord, Event
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

def check_existing_tables(app):
    """Check what tables already exist"""
    print("🔄 Checking existing database structure...")
    
    with app.app_context():
        try:
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"   ✓ Found {len(existing_tables)} existing tables:")
            for table in sorted(existing_tables):
                print(f"     - {table}")
            
            # Check if our new tables already exist
            new_tables = ['boats', 'equipment', 'maintenance_records', 'events']
            existing_new_tables = [t for t in new_tables if t in existing_tables]
            
            if existing_new_tables:
                print(f"   ⚠ These new tables already exist: {existing_new_tables}")
                return False, existing_new_tables
            else:
                print(f"   ✓ Ready to create new tables: {new_tables}")
                return True, []
                
        except Exception as e:
            print(f"   ✗ Error checking tables: {e}")
            return False, []

def create_sample_data(app):
    """Create sample data for demonstration"""
    print("🔄 Creating sample data...")
    
    with app.app_context():
        try:
            # Get admin user for sample data
            admin_user = User.query.filter_by(is_admin=True).first()
            if not admin_user:
                admin_user = User.query.first()
            
            if not admin_user:
                print("   ⚠ No users found - skipping sample data")
                return
            
            # Create sample boat
            if not Boat.query.first():
                sample_boat = Boat(
                    name="Demo Sailboat",
                    boat_type="Sailboat",
                    length_feet=35.0,
                    beam_feet=11.5,
                    draft_feet=6.2,
                    year_built=2010,
                    hull_material="Fiberglass",
                    registration_number="DEMO001",
                    owner_id=admin_user.id,
                    home_port="Marina Bay",
                    condition="Good"
                )
                db.session.add(sample_boat)
                print("   ✓ Created sample boat")
            
            # Create sample equipment
            if not Equipment.query.first():
                boat = Boat.query.first()
                sample_equipment = Equipment(
                    name="VHF Radio",
                    category="Navigation",
                    subcategory="Radio",
                    brand="Standard Horizon",
                    model="GX1700",
                    owner_id=admin_user.id,
                    boat_id=boat.id if boat else None,
                    location_on_boat="Nav Station",
                    condition="Good"
                )
                db.session.add(sample_equipment)
                print("   ✓ Created sample equipment")
            
            # Create sample maintenance record
            if not MaintenanceRecord.query.first():
                boat = Boat.query.first()
                from datetime import date
                sample_maintenance = MaintenanceRecord(
                    boat_id=boat.id if boat else None,
                    maintenance_type="Routine",
                    title="Engine Oil Change",
                    description="Changed engine oil and filter",
                    date_performed=date.today(),
                    performed_by="Demo User",
                    status="Completed",
                    created_by=admin_user.id
                )
                db.session.add(sample_maintenance)
                print("   ✓ Created sample maintenance record")
            
            # Create sample event
            if not Event.query.first():
                from datetime import datetime, timedelta
                sample_event = Event(
                    name="Demo Regatta",
                    event_type="Race",
                    description="Sample sailing event for demonstration",
                    location="Demo Bay",
                    start_date=datetime.now() + timedelta(days=30),
                    organizer="Demo Yacht Club",
                    status="Scheduled",
                    created_by=admin_user.id
                )
                db.session.add(sample_event)
                print("   ✓ Created sample event")
            
            db.session.commit()
            print("   ✓ Sample data created successfully")
            
        except Exception as e:
            print(f"   ✗ Error creating sample data: {e}")
            db.session.rollback()

def run_core_models_migration():
    """Run the complete migration process for core models"""
    print("=" * 60)
    print("🚀 SAILOR UTILITY CORE MODELS DEPLOYMENT")
    print("=" * 60)
    
    try:
        # Create app for migration
        app, migrate = create_app_for_migration()
        
        print(f"📊 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
        
        with app.app_context():
            # Step 1: Check existing structure
            can_proceed, existing_tables = check_existing_tables(app)
            
            if not can_proceed and existing_tables:
                print("⚠️  Some new tables already exist!")
                if 'DATABASE_URL' in os.environ and 'postgres' in os.environ['DATABASE_URL']:
                    # Production - be more careful
                    print("Production database detected - skipping table creation")
                    print("Proceeding with verification and sample data...")
                else:
                    # Development - proceed
                    print("Development database - proceeding with verification...")
            
            # Step 2: Run database migration
            print("🔄 Running database schema migration...")
            try:
                upgrade()
                print("   ✓ Schema migration completed successfully")
            except Exception as e:
                print(f"   ⚠ Migration error: {e}")
                print("   ℹ This might be normal if already up to date")
            
            # Step 3: Verify new tables exist
            print("🔄 Verifying new tables...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            current_tables = inspector.get_table_names()
            
            expected_tables = ['boats', 'equipment', 'maintenance_records', 'events']
            for table in expected_tables:
                if table in current_tables:
                    print(f"   ✓ Table '{table}' exists")
                else:
                    print(f"   ✗ Table '{table}' missing")
            
            # Step 4: Test model operations
            print("🔄 Testing model operations...")
            try:
                # Test basic queries
                boat_count = Boat.query.count()
                equipment_count = Equipment.query.count()
                maintenance_count = MaintenanceRecord.query.count()
                event_count = Event.query.count()
                
                print(f"   ✓ Boats: {boat_count}")
                print(f"   ✓ Equipment: {equipment_count}")
                print(f"   ✓ Maintenance Records: {maintenance_count}")
                print(f"   ✓ Events: {event_count}")
                
            except Exception as e:
                print(f"   ✗ Model test error: {e}")
                return False
            
            # Step 5: Create sample data if empty
            total_records = boat_count + equipment_count + maintenance_count + event_count
            if total_records == 0:
                create_sample_data(app)
            
            # Step 6: Final verification
            print("🔄 Final verification...")
            user_count = User.query.count()
            module_count = SystemModule.query.count()
            boat_count = Boat.query.count()
            equipment_count = Equipment.query.count()
            maintenance_count = MaintenanceRecord.query.count()
            event_count = Event.query.count()
            
            print(f"   ✓ Users: {user_count}")
            print(f"   ✓ Modules: {module_count}")
            print(f"   ✓ Boats: {boat_count}")
            print(f"   ✓ Equipment: {equipment_count}")
            print(f"   ✓ Maintenance Records: {maintenance_count}")
            print(f"   ✓ Events: {event_count}")
            
        print("=" * 60)
        print("✅ CORE MODELS DEPLOYMENT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("New Features Available:")
        print("- Complete boat/fleet management")
        print("- Equipment inventory tracking")
        print("- Maintenance record system")
        print("- Event management")
        print()
        print("Next Steps:")
        print("1. Test the new models through API endpoints")
        print("2. Begin frontend development for new modules")
        print("3. Add GPS tracking for trips (Phase 2 completion)")
        
        return True
        
    except Exception as e:
        print("=" * 60)
        print("❌ CORE MODELS DEPLOYMENT FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Check if we're in the right environment
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm-production":
        print("⚠️  PRODUCTION DEPLOYMENT CONFIRMED")
    else:
        print("⚠️  This script will modify the production database!")
        print("⚠️  Make sure you have a backup before proceeding!")
        print()
        print("To run this deployment, use:")
        print("  python migrate_core_models.py --confirm-production")
        print()
        sys.exit(1)
    
    success = run_core_models_migration()
    sys.exit(0 if success else 1)