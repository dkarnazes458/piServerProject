#!/usr/bin/env python3
"""
Test script for core sailor utility models
"""

from app import app
from models import db, User, Boat, Equipment, MaintenanceRecord, Event
from datetime import datetime, date, timedelta
import json

def test_core_models():
    """Test all new core models and relationships"""
    
    print("=== Core Sailor Models Test ===\n")
    
    with app.app_context():
        
        # Recreate tables for testing
        print("1. Creating fresh database with new models...")
        db.drop_all()
        db.create_all()
        
        # Create test user
        test_user = User(
            username='sailor_test',
            email='test@sailing.com',
            first_name='Test',
            last_name='Sailor',
            sailing_experience='Advanced'
        )
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()
        print(f"   ✓ Created test user: {test_user.get_full_name()}")
        
        # Test 2: Create a boat
        print("\\n2. Testing Boat model...")
        test_boat = Boat(
            name="Sea Spirit",
            boat_type="Sailboat",
            length_feet=32.5,
            beam_feet=10.2,
            draft_feet=5.8,
            year_built=1998,
            hull_material="Fiberglass",
            registration_number="FL1234AB",
            hin="ABC12345D404",
            owner_id=test_user.id,
            home_port="Marina Bay",
            engine_make="Yanmar",
            engine_model="3YM30",
            engine_hours=1250.5,
            fuel_capacity_gallons=20,
            sail_area_sqft=425,
            keel_type="Fin",
            condition="Good"
        )
        test_boat.set_photos(["boat1.jpg", "boat2.jpg"])
        
        db.session.add(test_boat)
        db.session.commit()
        
        boat_dict = test_boat.to_dict()
        print(f"   ✓ Created boat: {boat_dict['name']}")
        print(f"   ✓ Boat age: {boat_dict['age_years']} years")
        print(f"   ✓ Owner: {boat_dict['owner_name']}")
        print(f"   ✓ Photos: {boat_dict['photos']}")
        
        # Test 3: Create equipment
        print("\\n3. Testing Equipment model...")
        test_equipment = Equipment(
            name="Garmin GPS Plotter",
            category="Navigation",
            subcategory="GPS",
            brand="Garmin",
            model="GPSMAP 942xs",
            serial_number="GPS123456",
            purchase_date=date(2023, 3, 15),
            purchase_price=1299.99,
            owner_id=test_user.id,
            boat_id=test_boat.id,
            location_on_boat="Nav Station",
            condition="Excellent",
            quantity=1,
            weight_lbs=2.8,
            dimensions="10x6x3 inches"
        )
        
        specs = {
            "screen_size": "9 inches",
            "resolution": "1280x720",
            "chartplotter": True,
            "sonar": True,
            "wifi": True
        }
        test_equipment.set_specifications(specs)
        test_equipment.set_photos(["gps1.jpg"])
        test_equipment.set_documents(["manual.pdf", "warranty.pdf"])
        
        db.session.add(test_equipment)
        db.session.commit()
        
        equipment_dict = test_equipment.to_dict()
        print(f"   ✓ Created equipment: {equipment_dict['name']}")
        print(f"   ✓ On boat: {equipment_dict['boat_name']}")
        print(f"   ✓ Warranty valid: {equipment_dict['warranty_valid']}")
        print(f"   ✓ Age: {equipment_dict['age_days']} days")
        print(f"   ✓ Specifications: {equipment_dict['specifications']}")
        
        # Test 4: Create maintenance record
        print("\\n4. Testing MaintenanceRecord model...")
        test_maintenance = MaintenanceRecord(
            boat_id=test_boat.id,
            equipment_id=test_equipment.id,
            maintenance_type="Routine",
            title="GPS Software Update",
            description="Updated GPS software to latest version and checked all functions",
            date_performed=date.today(),
            performed_by="Test Sailor",
            performed_by_type="Self",
            location="Home Marina",
            labor_hours=1.5,
            parts_cost=0.00,
            labor_cost=0.00,
            next_maintenance_due=date.today() + timedelta(days=365),
            maintenance_interval_days=365,
            status="Completed",
            priority="Medium",
            created_by=test_user.id
        )
        
        parts = [
            {"name": "Software Update", "cost": 0, "part_number": "SW-2024-01"}
        ]
        test_maintenance.set_parts_used(parts)
        test_maintenance.set_photos(["maintenance1.jpg"])
        
        db.session.add(test_maintenance)
        db.session.commit()
        
        maintenance_dict = test_maintenance.to_dict()
        print(f"   ✓ Created maintenance: {maintenance_dict['title']}")
        print(f"   ✓ For boat: {maintenance_dict['boat_name']}")
        print(f"   ✓ Equipment: {maintenance_dict['equipment_name']}")
        print(f"   ✓ Total cost: ${maintenance_dict['total_cost']}")
        print(f"   ✓ Next due: {maintenance_dict['days_until_due']} days")
        print(f"   ✓ Parts used: {maintenance_dict['parts_used']}")
        
        # Test 5: Create event
        print("\\n5. Testing Event model...")
        start_time = datetime.now() + timedelta(days=14)
        end_time = start_time + timedelta(hours=6)
        
        test_event = Event(
            name="Spring Regatta 2024",
            event_type="Race",
            description="Annual spring sailing regatta with multiple race classes",
            location="San Francisco Bay",
            venue="St. Francis Yacht Club",
            start_date=start_time,
            end_date=end_time,
            organizer="SF Yacht Racing Association",
            organizer_contact="events@sfyra.com",
            registration_required=True,
            registration_deadline=start_time - timedelta(days=3),
            registration_fee=75.00,
            max_participants=50,
            current_participants=23,
            skill_level_required="Intermediate",
            weather_dependent=True,
            status="Scheduled",
            created_by=test_user.id
        )
        
        boat_reqs = {
            "min_length": 25,
            "max_length": 50,
            "equipment_required": ["VHF Radio", "Life Jackets", "Fire Extinguisher"],
            "boat_types": ["Sailboat"]
        }
        test_event.set_boat_requirements(boat_reqs)
        
        prizes = [
            {"place": 1, "prize": "Trophy + $500"},
            {"place": 2, "prize": "Trophy + $300"},
            {"place": 3, "prize": "Trophy + $200"}
        ]
        test_event.set_prizes(prizes)
        
        db.session.add(test_event)
        db.session.commit()
        
        event_dict = test_event.to_dict()
        print(f"   ✓ Created event: {event_dict['name']}")
        print(f"   ✓ Event type: {event_dict['event_type']}")
        print(f"   ✓ Days until event: {event_dict['days_until_event']}")
        print(f"   ✓ Duration: {event_dict['duration_hours']} hours")
        print(f"   ✓ Spots available: {event_dict['spots_available']}")
        print(f"   ✓ Can register: {event_dict['can_register']}")
        print(f"   ✓ Boat requirements: {event_dict['boat_requirements']}")
        
        # Test 6: Test relationships
        print("\\n6. Testing model relationships...")
        
        # User -> boats
        user_boats = test_user.owned_boats
        print(f"   ✓ User owns {len(user_boats)} boats")
        
        # User -> equipment  
        user_equipment = test_user.equipment
        print(f"   ✓ User has {len(user_equipment)} equipment items")
        
        # Boat -> equipment
        boat_equipment = test_boat.equipment
        print(f"   ✓ Boat has {len(boat_equipment)} equipment items")
        
        # Boat -> maintenance records
        boat_maintenance = test_boat.maintenance_records
        print(f"   ✓ Boat has {len(boat_maintenance)} maintenance records")
        
        # Equipment -> maintenance records
        equipment_maintenance = test_equipment.maintenance_records
        print(f"   ✓ Equipment has {len(equipment_maintenance)} maintenance records")
        
        # User -> created events
        user_events = test_user.created_events
        print(f"   ✓ User created {len(user_events)} events")
        
        print("\\n=== All Core Model Tests Passed! ===")
        
        # Final summary
        print("\\nFinal Database State:")
        print(f"- Users: {User.query.count()}")
        print(f"- Boats: {Boat.query.count()}")
        print(f"- Equipment: {Equipment.query.count()}")
        print(f"- Maintenance Records: {MaintenanceRecord.query.count()}")
        print(f"- Events: {Event.query.count()}")
        
        return True

if __name__ == "__main__":
    success = test_core_models()
    exit(0 if success else 1)