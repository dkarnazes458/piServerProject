from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from functools import wraps
from config import Config
from models import db, User, SystemModule, UserModulePermission, UserPreference, Boat, Equipment, MaintenanceRecord, Event, Trip

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({'message': 'Pi Server Project API is running!'})

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'pi-server-api'})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username, email, and password required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    })

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()})

# Admin authorization decorator
def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# Helper function to get current user
def get_current_user():
    user_id = int(get_jwt_identity())
    return User.query.get(user_id)

# ============================================================
# MODULE MANAGEMENT API ENDPOINTS
# ============================================================

@app.route('/api/admin/modules', methods=['GET'])
@admin_required
def get_all_modules():
    """Get all system modules (admin only)"""
    modules = SystemModule.query.order_by(SystemModule.sort_order).all()
    return jsonify({
        'modules': [module.to_dict() for module in modules],
        'count': len(modules)
    })

@app.route('/api/admin/modules', methods=['POST'])
@admin_required
def create_module():
    """Create a new system module (admin only)"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'display_name']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if module already exists
    if SystemModule.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Module name already exists'}), 409
    
    # Create new module
    module = SystemModule(
        name=data['name'],
        display_name=data['display_name'],
        description=data.get('description'),
        icon=data.get('icon'),
        is_active=data.get('is_active', True),
        requires_admin=data.get('requires_admin', False),
        sort_order=data.get('sort_order', 0)
    )
    
    db.session.add(module)
    db.session.commit()
    
    return jsonify({
        'message': 'Module created successfully',
        'module': module.to_dict()
    }), 201

@app.route('/api/admin/modules/<int:module_id>', methods=['PUT'])
@admin_required
def update_module(module_id):
    """Update a system module (admin only)"""
    module = SystemModule.query.get(module_id)
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update fields
    updateable_fields = ['display_name', 'description', 'icon', 'is_active', 'requires_admin', 'sort_order']
    for field in updateable_fields:
        if field in data:
            setattr(module, field, data[field])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Module updated successfully',
        'module': module.to_dict()
    })

@app.route('/api/admin/modules/<int:module_id>', methods=['DELETE'])
@admin_required
def delete_module(module_id):
    """Delete a system module (admin only)"""
    module = SystemModule.query.get(module_id)
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    
    # Don't allow deletion of core modules
    core_modules = ['dashboard', 'admin']
    if module.name in core_modules:
        return jsonify({'error': f'Cannot delete core module: {module.name}'}), 400
    
    # Delete related permissions first
    UserModulePermission.query.filter_by(module_id=module.id).delete()
    
    db.session.delete(module)
    db.session.commit()
    
    return jsonify({'message': 'Module deleted successfully'})

@app.route('/api/admin/users/<int:user_id>/modules', methods=['GET'])
@admin_required
def get_user_modules(user_id):
    """Get user's module permissions (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    permissions = UserModulePermission.query.filter_by(user_id=user_id).all()
    all_modules = SystemModule.query.order_by(SystemModule.sort_order).all()
    
    # Build response with permission status
    modules_data = []
    for module in all_modules:
        permission = next((p for p in permissions if p.module_id == module.id), None)
        modules_data.append({
            **module.to_dict(),
            'has_permission': permission is not None,
            'is_enabled': permission.is_enabled if permission else False,
            'granted_at': permission.granted_at.isoformat() if permission and permission.granted_at else None
        })
    
    return jsonify({
        'user': user.to_dict(),
        'modules': modules_data
    })

@app.route('/api/admin/users/<int:user_id>/modules', methods=['POST'])
@admin_required
def grant_user_module(user_id):
    """Grant module access to user (admin only)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('module_id'):
        return jsonify({'error': 'module_id is required'}), 400
    
    module = SystemModule.query.get(data['module_id'])
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    
    # Check if permission already exists
    existing = UserModulePermission.query.filter_by(
        user_id=user_id, module_id=module.id
    ).first()
    
    if existing:
        return jsonify({'error': 'User already has permission for this module'}), 409
    
    # Create permission
    current_admin = get_current_user()
    permission = UserModulePermission(
        user_id=user_id,
        module_id=module.id,
        is_enabled=True,
        granted_by=current_admin.id
    )
    
    db.session.add(permission)
    db.session.commit()
    
    return jsonify({
        'message': 'Module access granted successfully',
        'permission': permission.to_dict()
    }), 201

@app.route('/api/admin/users/<int:user_id>/modules/<int:module_id>', methods=['DELETE'])
@admin_required
def revoke_user_module(user_id, module_id):
    """Revoke module access from user (admin only)"""
    permission = UserModulePermission.query.filter_by(
        user_id=user_id, module_id=module_id
    ).first()
    
    if not permission:
        return jsonify({'error': 'Permission not found'}), 404
    
    # Don't allow revoking core modules
    module = SystemModule.query.get(module_id)
    if module and module.name in ['dashboard']:
        return jsonify({'error': f'Cannot revoke access to core module: {module.name}'}), 400
    
    db.session.delete(permission)
    db.session.commit()
    
    return jsonify({'message': 'Module access revoked successfully'})

# ============================================================
# USER MODULE PREFERENCE API ENDPOINTS
# ============================================================

@app.route('/api/user/modules', methods=['GET'])
@jwt_required()
def get_user_available_modules():
    """Get current user's available modules"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's module permissions
    permissions = UserModulePermission.query.filter_by(user_id=user.id).all()
    
    # Build list of available modules
    available_modules = []
    for permission in permissions:
        module = permission.module
        if module and module.is_active:
            # Check if user meets requirements
            if module.requires_admin and not user.is_admin:
                continue
            
            available_modules.append({
                **module.to_dict(),
                'is_enabled': permission.is_enabled
            })
    
    # Sort by sort_order
    available_modules.sort(key=lambda x: x['sort_order'])
    
    return jsonify({
        'modules': available_modules,
        'count': len(available_modules)
    })

@app.route('/api/user/modules/<int:module_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_user_module(module_id):
    """Enable/disable module for current user"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    permission = UserModulePermission.query.filter_by(
        user_id=user.id, module_id=module_id
    ).first()
    
    if not permission:
        return jsonify({'error': 'You do not have permission for this module'}), 403
    
    # Don't allow disabling core modules
    module = SystemModule.query.get(module_id)
    if module and module.name in ['dashboard']:
        return jsonify({'error': f'Cannot disable core module: {module.name}'}), 400
    
    # Toggle the enabled state
    permission.is_enabled = not permission.is_enabled
    db.session.commit()
    
    return jsonify({
        'message': f'Module {"enabled" if permission.is_enabled else "disabled"} successfully',
        'module': {
            **module.to_dict(),
            'is_enabled': permission.is_enabled
        }
    })

# ============================================================
# USER PREFERENCES API ENDPOINTS
# ============================================================

@app.route('/api/user/preferences', methods=['GET'])
@jwt_required()
def get_user_preferences():
    """Get current user's preferences"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    preferences = UserPreference.query.filter_by(user_id=user.id).all()
    
    # Convert to dictionary format
    prefs_dict = {}
    for pref in preferences:
        prefs_dict[pref.preference_key] = pref.get_value()
    
    return jsonify({
        'preferences': prefs_dict,
        'count': len(preferences)
    })

@app.route('/api/user/preferences', methods=['PUT'])
@jwt_required()
def update_user_preferences():
    """Update current user's preferences"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No preferences provided'}), 400
    
    updated_prefs = []
    
    for key, value in data.items():
        # Find or create preference
        pref = UserPreference.query.filter_by(
            user_id=user.id, preference_key=key
        ).first()
        
        if not pref:
            pref = UserPreference(user_id=user.id, preference_key=key)
            db.session.add(pref)
        
        pref.set_value(value)
        updated_prefs.append(key)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Preferences updated successfully',
        'updated_keys': updated_prefs
    })

# ============================================================
# BOATS CRUD API ENDPOINTS
# ============================================================

@app.route('/api/boats', methods=['GET'])
@jwt_required()
def get_boats():
    """Get all boats for current user"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get boats owned by user
    boats = Boat.query.filter_by(owner_id=user.id, is_active=True).all()
    
    return jsonify({
        'boats': [boat.to_dict() for boat in boats],
        'count': len(boats)
    })

@app.route('/api/boats', methods=['POST'])
@jwt_required()
def create_boat():
    """Create a new boat"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Boat name is required'}), 400
    
    # Check for duplicate registration number if provided
    if data.get('registration_number'):
        existing = Boat.query.filter_by(registration_number=data['registration_number']).first()
        if existing:
            return jsonify({'error': 'Registration number already exists'}), 409
    
    # Create new boat
    boat = Boat(
        name=data['name'],
        boat_type=data.get('boat_type'),
        length_feet=data.get('length_feet'),
        beam_feet=data.get('beam_feet'),
        draft_feet=data.get('draft_feet'),
        displacement_lbs=data.get('displacement_lbs'),
        year_built=data.get('year_built'),
        hull_material=data.get('hull_material'),
        registration_number=data.get('registration_number'),
        hin=data.get('hin'),
        documentation_number=data.get('documentation_number'),
        owner_id=user.id,
        home_port=data.get('home_port'),
        current_location=data.get('current_location'),
        marina_berth=data.get('marina_berth'),
        insurance_company=data.get('insurance_company'),
        insurance_policy_number=data.get('insurance_policy_number'),
        engine_make=data.get('engine_make'),
        engine_model=data.get('engine_model'),
        engine_year=data.get('engine_year'),
        engine_hours=data.get('engine_hours'),
        fuel_capacity_gallons=data.get('fuel_capacity_gallons'),
        water_capacity_gallons=data.get('water_capacity_gallons'),
        sail_area_sqft=data.get('sail_area_sqft'),
        mast_height_feet=data.get('mast_height_feet'),
        keel_type=data.get('keel_type'),
        condition=data.get('condition', 'Good'),
        notes=data.get('notes')
    )
    
    # Handle dates
    from datetime import datetime
    if data.get('insurance_expiry'):
        try:
            boat.insurance_expiry = datetime.strptime(data['insurance_expiry'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if data.get('last_survey_date'):
        try:
            boat.last_survey_date = datetime.strptime(data['last_survey_date'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if data.get('next_survey_due'):
        try:
            boat.next_survey_due = datetime.strptime(data['next_survey_due'], '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Handle photos
    if data.get('photos'):
        boat.set_photos(data['photos'])
    
    db.session.add(boat)
    db.session.commit()
    
    return jsonify({
        'message': 'Boat created successfully',
        'boat': boat.to_dict()
    }), 201

@app.route('/api/boats/<int:boat_id>', methods=['GET'])
@jwt_required()
def get_boat(boat_id):
    """Get specific boat details"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    boat = Boat.query.filter_by(id=boat_id, owner_id=user.id).first()
    if not boat:
        return jsonify({'error': 'Boat not found'}), 404
    
    return jsonify({'boat': boat.to_dict()})

@app.route('/api/boats/<int:boat_id>', methods=['PUT'])
@jwt_required()
def update_boat(boat_id):
    """Update boat details"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    boat = Boat.query.filter_by(id=boat_id, owner_id=user.id).first()
    if not boat:
        return jsonify({'error': 'Boat not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Check for duplicate registration number if changed
    if data.get('registration_number') and data['registration_number'] != boat.registration_number:
        existing = Boat.query.filter_by(registration_number=data['registration_number']).first()
        if existing:
            return jsonify({'error': 'Registration number already exists'}), 409
    
    # Update fields
    updateable_fields = [
        'name', 'boat_type', 'length_feet', 'beam_feet', 'draft_feet', 'displacement_lbs',
        'year_built', 'hull_material', 'registration_number', 'hin', 'documentation_number',
        'home_port', 'current_location', 'marina_berth', 'insurance_company', 
        'insurance_policy_number', 'engine_make', 'engine_model', 'engine_year', 
        'engine_hours', 'fuel_capacity_gallons', 'water_capacity_gallons', 'sail_area_sqft',
        'mast_height_feet', 'keel_type', 'condition', 'notes'
    ]
    
    for field in updateable_fields:
        if field in data:
            setattr(boat, field, data[field])
    
    # Handle date fields
    from datetime import datetime
    date_fields = ['insurance_expiry', 'last_survey_date', 'next_survey_due']
    for field in date_fields:
        if field in data and data[field]:
            try:
                setattr(boat, field, datetime.strptime(data[field], '%Y-%m-%d').date())
            except ValueError:
                pass
        elif field in data and data[field] is None:
            setattr(boat, field, None)
    
    # Handle photos
    if 'photos' in data:
        boat.set_photos(data['photos'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Boat updated successfully',
        'boat': boat.to_dict()
    })

@app.route('/api/boats/<int:boat_id>', methods=['DELETE'])
@jwt_required()
def delete_boat(boat_id):
    """Delete boat (soft delete by setting is_active=False)"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    boat = Boat.query.filter_by(id=boat_id, owner_id=user.id).first()
    if not boat:
        return jsonify({'error': 'Boat not found'}), 404
    
    # Soft delete
    boat.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Boat deleted successfully'})

# ============================================================
# TRIPS CRUD API ENDPOINTS
# ============================================================

@app.route('/api/trips', methods=['GET'])
@jwt_required()
def get_trips():
    """Get all trips for current user"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get trips where user is captain or participant
    trips = Trip.query.filter_by(captain_id=user.id).all()
    
    return jsonify({
        'trips': [trip.to_dict() for trip in trips],
        'count': len(trips)
    })

@app.route('/api/trips', methods=['POST'])
@jwt_required()
def create_trip():
    """Create a new trip"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('name') or not data.get('boat_id') or not data.get('start_date'):
        return jsonify({'error': 'Trip name, boat ID, and start date are required'}), 400
    
    # Verify boat ownership
    boat = Boat.query.filter_by(id=data['boat_id'], owner_id=user.id).first()
    if not boat:
        return jsonify({'error': 'Boat not found or not owned by user'}), 404
    
    # Create new trip
    from datetime import datetime
    try:
        start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({'error': 'Invalid start date format'}), 400
    
    trip = Trip(
        name=data['name'],
        description=data.get('description'),
        trip_type=data.get('trip_type', 'Leisure'),
        boat_id=data['boat_id'],
        captain_id=user.id,
        crew_size=data.get('crew_size', 1),
        start_date=start_date,
        planned_duration_hours=data.get('planned_duration_hours'),
        start_location=data.get('start_location'),
        end_location=data.get('end_location'),
        start_latitude=data.get('start_latitude'),
        start_longitude=data.get('start_longitude'),
        end_latitude=data.get('end_latitude'),
        end_longitude=data.get('end_longitude'),
        status=data.get('status', 'Planned'),
        purpose=data.get('purpose'),
        difficulty_level=data.get('difficulty_level', 'Moderate'),
        emergency_contact=data.get('emergency_contact'),
        float_plan_filed=data.get('float_plan_filed', False),
        float_plan_with=data.get('float_plan_with'),
        safety_equipment_check=data.get('safety_equipment_check', False),
        notes=data.get('notes')
    )
    
    # Handle end date
    if data.get('end_date'):
        try:
            trip.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except ValueError:
            pass
    
    # Handle complex fields
    if data.get('weather_conditions'):
        trip.set_weather_conditions(data['weather_conditions'])
    
    if data.get('cost_breakdown'):
        trip.set_cost_breakdown(data['cost_breakdown'])
    
    if data.get('photos'):
        trip.set_photos(data['photos'])
    
    if data.get('documents'):
        trip.set_documents(data['documents'])
    
    if data.get('logbook_entries'):
        trip.set_logbook_entries(data['logbook_entries'])
    
    if data.get('tags'):
        trip.set_tags(data['tags'])
    
    db.session.add(trip)
    db.session.commit()
    
    return jsonify({
        'message': 'Trip created successfully',
        'trip': trip.to_dict()
    }), 201

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    """Get specific trip details"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    trip = Trip.query.filter_by(id=trip_id, captain_id=user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    return jsonify({'trip': trip.to_dict()})

@app.route('/api/trips/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    """Update trip details"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    trip = Trip.query.filter_by(id=trip_id, captain_id=user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update basic fields
    basic_fields = [
        'name', 'description', 'trip_type', 'crew_size', 'planned_duration_hours',
        'actual_duration_hours', 'start_location', 'end_location', 'start_latitude',
        'start_longitude', 'end_latitude', 'end_longitude', 'distance_miles',
        'max_speed_knots', 'avg_speed_knots', 'max_wind_speed_knots', 'avg_wind_speed_knots',
        'wind_direction', 'sea_conditions', 'visibility', 'tide_conditions',
        'fuel_used_gallons', 'fuel_cost', 'status', 'purpose', 'difficulty_level',
        'emergency_contact', 'float_plan_filed', 'float_plan_with', 'safety_equipment_check',
        'total_cost', 'lessons_learned', 'highlights', 'challenges_faced',
        'overall_rating', 'would_repeat', 'is_public', 'is_favorite', 'notes'
    ]
    
    for field in basic_fields:
        if field in data:
            setattr(trip, field, data[field])
    
    # Handle date fields
    from datetime import datetime
    if 'start_date' in data and data['start_date']:
        try:
            trip.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        except ValueError:
            pass
    
    if 'end_date' in data:
        if data['end_date']:
            try:
                trip.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
            except ValueError:
                pass
        else:
            trip.end_date = None
    
    # Handle complex fields
    if 'weather_conditions' in data:
        trip.set_weather_conditions(data['weather_conditions'])
    
    if 'cost_breakdown' in data:
        trip.set_cost_breakdown(data['cost_breakdown'])
    
    if 'photos' in data:
        trip.set_photos(data['photos'])
    
    if 'documents' in data:
        trip.set_documents(data['documents'])
    
    if 'logbook_entries' in data:
        trip.set_logbook_entries(data['logbook_entries'])
    
    if 'tags' in data:
        trip.set_tags(data['tags'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Trip updated successfully',
        'trip': trip.to_dict()
    })

@app.route('/api/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    """Delete trip"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    trip = Trip.query.filter_by(id=trip_id, captain_id=user.id).first()
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
    
    # Hard delete trip and related GPS points
    from models import GPSRoutePoint
    GPSRoutePoint.query.filter_by(trip_id=trip.id).delete()
    
    db.session.delete(trip)
    db.session.commit()
    
    return jsonify({'message': 'Trip deleted successfully'})

# ============================================================
# EQUIPMENT CRUD API ENDPOINTS
# ============================================================

@app.route('/api/equipment', methods=['GET'])
@jwt_required()
def get_equipment():
    """Get all equipment for current user"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get equipment owned by user
    equipment = Equipment.query.filter_by(owner_id=user.id).all()
    
    return jsonify({
        'equipment': [item.to_dict() for item in equipment],
        'count': len(equipment)
    })

@app.route('/api/equipment', methods=['POST'])
@jwt_required()
def create_equipment():
    """Create a new equipment item"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Equipment name is required'}), 400
    
    try:
        # Create new equipment
        equipment = Equipment(
            name=data['name'],
            category=data.get('category'),
            subcategory=data.get('subcategory'),
            brand=data.get('brand'),
            model=data.get('model'),
            part_number=data.get('part_number'),
            serial_number=data.get('serial_number'),
            purchase_location=data.get('purchase_location'),
            warranty_period_months=data.get('warranty_period_months'),
            boat_id=data.get('boat_id') if data.get('boat_id') else None,
            location_on_boat=data.get('location_on_boat'),
            current_location=data.get('current_location'),
            condition=data.get('condition', 'Good'),
            is_operational=data.get('is_operational', True),
            quantity=data.get('quantity', 1),
            weight_lbs=data.get('weight_lbs'),
            dimensions=data.get('dimensions'),
            manual_url=data.get('manual_url'),
            notes=data.get('notes'),
            owner_id=user.id
        )
        
        # Handle date fields
        if data.get('purchase_date'):
            from datetime import datetime
            equipment.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
        
        if data.get('warranty_expiry'):
            from datetime import datetime
            equipment.warranty_expiry = datetime.strptime(data['warranty_expiry'], '%Y-%m-%d').date()
        
        if data.get('last_inspection_date'):
            from datetime import datetime
            equipment.last_inspection_date = datetime.strptime(data['last_inspection_date'], '%Y-%m-%d').date()
        
        if data.get('next_inspection_due'):
            from datetime import datetime
            equipment.next_inspection_due = datetime.strptime(data['next_inspection_due'], '%Y-%m-%d').date()
        
        # Handle numeric fields
        if data.get('purchase_price'):
            equipment.purchase_price = float(data['purchase_price'])
        
        # Handle JSON fields
        if data.get('specifications'):
            equipment.set_specifications(data['specifications'])
        
        if data.get('photos'):
            equipment.set_photos(data['photos'])
        
        if data.get('documents'):
            equipment.set_documents(data['documents'])
        
        # Validate boat ownership if boat_id provided
        if equipment.boat_id:
            boat = Boat.query.filter_by(id=equipment.boat_id, owner_id=user.id).first()
            if not boat:
                return jsonify({'error': 'Boat not found or not owned by user'}), 404
        
        db.session.add(equipment)
        db.session.commit()
        
        return jsonify({
            'message': 'Equipment created successfully',
            'equipment': equipment.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create equipment: {str(e)}'}), 500

@app.route('/api/equipment/<int:equipment_id>', methods=['GET'])
@jwt_required()
def get_equipment_by_id(equipment_id):
    """Get specific equipment by ID"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    equipment = Equipment.query.filter_by(id=equipment_id, owner_id=user.id).first()
    if not equipment:
        return jsonify({'error': 'Equipment not found'}), 404
    
    return jsonify(equipment.to_dict())

@app.route('/api/equipment/<int:equipment_id>', methods=['PUT'])
@jwt_required()
def update_equipment(equipment_id):
    """Update equipment"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    equipment = Equipment.query.filter_by(id=equipment_id, owner_id=user.id).first()
    if not equipment:
        return jsonify({'error': 'Equipment not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update basic fields
        if 'name' in data:
            equipment.name = data['name']
        if 'category' in data:
            equipment.category = data['category']
        if 'subcategory' in data:
            equipment.subcategory = data['subcategory']
        if 'brand' in data:
            equipment.brand = data['brand']
        if 'model' in data:
            equipment.model = data['model']
        if 'part_number' in data:
            equipment.part_number = data['part_number']
        if 'serial_number' in data:
            equipment.serial_number = data['serial_number']
        if 'purchase_location' in data:
            equipment.purchase_location = data['purchase_location']
        if 'warranty_period_months' in data:
            equipment.warranty_period_months = data['warranty_period_months']
        if 'location_on_boat' in data:
            equipment.location_on_boat = data['location_on_boat']
        if 'current_location' in data:
            equipment.current_location = data['current_location']
        if 'condition' in data:
            equipment.condition = data['condition']
        if 'is_operational' in data:
            equipment.is_operational = data['is_operational']
        if 'quantity' in data:
            equipment.quantity = data['quantity']
        if 'weight_lbs' in data:
            equipment.weight_lbs = data['weight_lbs']
        if 'dimensions' in data:
            equipment.dimensions = data['dimensions']
        if 'manual_url' in data:
            equipment.manual_url = data['manual_url']
        if 'notes' in data:
            equipment.notes = data['notes']
        
        # Handle boat_id change with validation
        if 'boat_id' in data:
            if data['boat_id']:
                boat = Boat.query.filter_by(id=data['boat_id'], owner_id=user.id).first()
                if not boat:
                    return jsonify({'error': 'Boat not found or not owned by user'}), 404
                equipment.boat_id = data['boat_id']
            else:
                equipment.boat_id = None
        
        # Handle date fields
        if 'purchase_date' in data:
            if data['purchase_date']:
                from datetime import datetime
                equipment.purchase_date = datetime.strptime(data['purchase_date'], '%Y-%m-%d').date()
            else:
                equipment.purchase_date = None
        
        if 'warranty_expiry' in data:
            if data['warranty_expiry']:
                from datetime import datetime
                equipment.warranty_expiry = datetime.strptime(data['warranty_expiry'], '%Y-%m-%d').date()
            else:
                equipment.warranty_expiry = None
        
        if 'last_inspection_date' in data:
            if data['last_inspection_date']:
                from datetime import datetime
                equipment.last_inspection_date = datetime.strptime(data['last_inspection_date'], '%Y-%m-%d').date()
            else:
                equipment.last_inspection_date = None
        
        if 'next_inspection_due' in data:
            if data['next_inspection_due']:
                from datetime import datetime
                equipment.next_inspection_due = datetime.strptime(data['next_inspection_due'], '%Y-%m-%d').date()
            else:
                equipment.next_inspection_due = None
        
        # Handle numeric fields
        if 'purchase_price' in data:
            equipment.purchase_price = float(data['purchase_price']) if data['purchase_price'] else None
        
        # Handle JSON fields
        if 'specifications' in data:
            equipment.set_specifications(data['specifications'])
        
        if 'photos' in data:
            equipment.set_photos(data['photos'])
        
        if 'documents' in data:
            equipment.set_documents(data['documents'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Equipment updated successfully',
            'equipment': equipment.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update equipment: {str(e)}'}), 500

@app.route('/api/equipment/<int:equipment_id>', methods=['DELETE'])
@jwt_required()
def delete_equipment(equipment_id):
    """Delete equipment"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    equipment = Equipment.query.filter_by(id=equipment_id, owner_id=user.id).first()
    if not equipment:
        return jsonify({'error': 'Equipment not found'}), 404
    
    db.session.delete(equipment)
    db.session.commit()
    
    return jsonify({'message': 'Equipment deleted successfully'})

# ============================================================
# MAINTENANCE CRUD API ENDPOINTS
# ============================================================

@app.route('/api/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance_records():
    """Get all maintenance records for current user's boats and equipment"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get maintenance records for user's boats and equipment
    user_boat_ids = [boat.id for boat in Boat.query.filter_by(owner_id=user.id).all()]
    user_equipment_ids = [eq.id for eq in Equipment.query.filter_by(owner_id=user.id).all()]
    
    # Query maintenance records for user's boats or equipment
    maintenance_records = MaintenanceRecord.query.filter(
        db.or_(
            MaintenanceRecord.boat_id.in_(user_boat_ids),
            MaintenanceRecord.equipment_id.in_(user_equipment_ids),
            MaintenanceRecord.created_by == user.id
        )
    ).all()
    
    return jsonify({
        'maintenance_records': [record.to_dict() for record in maintenance_records],
        'count': len(maintenance_records)
    })

@app.route('/api/maintenance', methods=['POST'])
@jwt_required()
def create_maintenance_record():
    """Create a new maintenance record"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Title and description are required'}), 400
    
    try:
        # Create new maintenance record
        maintenance = MaintenanceRecord(
            title=data['title'],
            description=data['description'],
            maintenance_type=data.get('maintenance_type', 'Routine'),
            performed_by=data.get('performed_by'),
            performed_by_type=data.get('performed_by_type', 'Self'),
            location=data.get('location'),
            currency=data.get('currency', 'USD'),
            status=data.get('status', 'Completed'),
            priority=data.get('priority', 'Medium'),
            warranty_work=data.get('warranty_work', False),
            notes=data.get('notes'),
            created_by=user.id
        )
        
        # Handle optional boat_id and equipment_id
        if data.get('boat_id'):
            boat = Boat.query.filter_by(id=data['boat_id'], owner_id=user.id).first()
            if not boat:
                return jsonify({'error': 'Boat not found or not owned by user'}), 404
            maintenance.boat_id = data['boat_id']
        
        if data.get('equipment_id'):
            equipment = Equipment.query.filter_by(id=data['equipment_id'], owner_id=user.id).first()
            if not equipment:
                return jsonify({'error': 'Equipment not found or not owned by user'}), 404
            maintenance.equipment_id = data['equipment_id']
        
        # Require at least boat_id or equipment_id
        if not maintenance.boat_id and not maintenance.equipment_id:
            return jsonify({'error': 'Either boat_id or equipment_id is required'}), 400
        
        # Handle date fields
        if data.get('date_performed'):
            from datetime import datetime
            maintenance.date_performed = datetime.strptime(data['date_performed'], '%Y-%m-%d').date()
        else:
            from datetime import date
            maintenance.date_performed = date.today()
        
        if data.get('next_maintenance_due'):
            from datetime import datetime
            maintenance.next_maintenance_due = datetime.strptime(data['next_maintenance_due'], '%Y-%m-%d').date()
        
        # Handle numeric fields
        if data.get('cost'):
            maintenance.cost = float(data['cost'])
        if data.get('labor_hours'):
            maintenance.labor_hours = float(data['labor_hours'])
        if data.get('parts_cost'):
            maintenance.parts_cost = float(data['parts_cost'])
        if data.get('labor_cost'):
            maintenance.labor_cost = float(data['labor_cost'])
        if data.get('next_maintenance_hours'):
            maintenance.next_maintenance_hours = float(data['next_maintenance_hours'])
        if data.get('maintenance_interval_days'):
            maintenance.maintenance_interval_days = int(data['maintenance_interval_days'])
        if data.get('maintenance_interval_hours'):
            maintenance.maintenance_interval_hours = float(data['maintenance_interval_hours'])
        
        # Handle JSON fields
        if data.get('parts_used'):
            maintenance.set_parts_used(data['parts_used'])
        
        if data.get('photos'):
            maintenance.set_photos(data['photos'])
        
        if data.get('documents'):
            maintenance.set_documents(data['documents'])
        
        db.session.add(maintenance)
        db.session.commit()
        
        return jsonify({
            'message': 'Maintenance record created successfully',
            'maintenance_record': maintenance.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create maintenance record: {str(e)}'}), 500

@app.route('/api/maintenance/<int:maintenance_id>', methods=['GET'])
@jwt_required()
def get_maintenance_record_by_id(maintenance_id):
    """Get specific maintenance record by ID"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's boat and equipment IDs for access control
    user_boat_ids = [boat.id for boat in Boat.query.filter_by(owner_id=user.id).all()]
    user_equipment_ids = [eq.id for eq in Equipment.query.filter_by(owner_id=user.id).all()]
    
    maintenance = MaintenanceRecord.query.filter(
        MaintenanceRecord.id == maintenance_id,
        db.or_(
            MaintenanceRecord.boat_id.in_(user_boat_ids),
            MaintenanceRecord.equipment_id.in_(user_equipment_ids),
            MaintenanceRecord.created_by == user.id
        )
    ).first()
    
    if not maintenance:
        return jsonify({'error': 'Maintenance record not found'}), 404
    
    return jsonify(maintenance.to_dict())

@app.route('/api/maintenance/<int:maintenance_id>', methods=['PUT'])
@jwt_required()
def update_maintenance_record(maintenance_id):
    """Update maintenance record"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's boat and equipment IDs for access control
    user_boat_ids = [boat.id for boat in Boat.query.filter_by(owner_id=user.id).all()]
    user_equipment_ids = [eq.id for eq in Equipment.query.filter_by(owner_id=user.id).all()]
    
    maintenance = MaintenanceRecord.query.filter(
        MaintenanceRecord.id == maintenance_id,
        db.or_(
            MaintenanceRecord.boat_id.in_(user_boat_ids),
            MaintenanceRecord.equipment_id.in_(user_equipment_ids),
            MaintenanceRecord.created_by == user.id
        )
    ).first()
    
    if not maintenance:
        return jsonify({'error': 'Maintenance record not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update basic fields
        if 'title' in data:
            maintenance.title = data['title']
        if 'description' in data:
            maintenance.description = data['description']
        if 'maintenance_type' in data:
            maintenance.maintenance_type = data['maintenance_type']
        if 'performed_by' in data:
            maintenance.performed_by = data['performed_by']
        if 'performed_by_type' in data:
            maintenance.performed_by_type = data['performed_by_type']
        if 'location' in data:
            maintenance.location = data['location']
        if 'currency' in data:
            maintenance.currency = data['currency']
        if 'status' in data:
            maintenance.status = data['status']
        if 'priority' in data:
            maintenance.priority = data['priority']
        if 'warranty_work' in data:
            maintenance.warranty_work = data['warranty_work']
        if 'notes' in data:
            maintenance.notes = data['notes']
        
        # Handle boat_id and equipment_id changes with validation
        if 'boat_id' in data:
            if data['boat_id']:
                boat = Boat.query.filter_by(id=data['boat_id'], owner_id=user.id).first()
                if not boat:
                    return jsonify({'error': 'Boat not found or not owned by user'}), 404
                maintenance.boat_id = data['boat_id']
            else:
                maintenance.boat_id = None
        
        if 'equipment_id' in data:
            if data['equipment_id']:
                equipment = Equipment.query.filter_by(id=data['equipment_id'], owner_id=user.id).first()
                if not equipment:
                    return jsonify({'error': 'Equipment not found or not owned by user'}), 404
                maintenance.equipment_id = data['equipment_id']
            else:
                maintenance.equipment_id = None
        
        # Handle date fields
        if 'date_performed' in data:
            if data['date_performed']:
                from datetime import datetime
                maintenance.date_performed = datetime.strptime(data['date_performed'], '%Y-%m-%d').date()
        
        if 'next_maintenance_due' in data:
            if data['next_maintenance_due']:
                from datetime import datetime
                maintenance.next_maintenance_due = datetime.strptime(data['next_maintenance_due'], '%Y-%m-%d').date()
            else:
                maintenance.next_maintenance_due = None
        
        # Handle numeric fields
        if 'cost' in data:
            maintenance.cost = float(data['cost']) if data['cost'] else None
        if 'labor_hours' in data:
            maintenance.labor_hours = float(data['labor_hours']) if data['labor_hours'] else None
        if 'parts_cost' in data:
            maintenance.parts_cost = float(data['parts_cost']) if data['parts_cost'] else None
        if 'labor_cost' in data:
            maintenance.labor_cost = float(data['labor_cost']) if data['labor_cost'] else None
        if 'next_maintenance_hours' in data:
            maintenance.next_maintenance_hours = float(data['next_maintenance_hours']) if data['next_maintenance_hours'] else None
        if 'maintenance_interval_days' in data:
            maintenance.maintenance_interval_days = int(data['maintenance_interval_days']) if data['maintenance_interval_days'] else None
        if 'maintenance_interval_hours' in data:
            maintenance.maintenance_interval_hours = float(data['maintenance_interval_hours']) if data['maintenance_interval_hours'] else None
        
        # Handle JSON fields
        if 'parts_used' in data:
            maintenance.set_parts_used(data['parts_used'])
        
        if 'photos' in data:
            maintenance.set_photos(data['photos'])
        
        if 'documents' in data:
            maintenance.set_documents(data['documents'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Maintenance record updated successfully',
            'maintenance_record': maintenance.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update maintenance record: {str(e)}'}), 500

@app.route('/api/maintenance/<int:maintenance_id>', methods=['DELETE'])
@jwt_required()
def delete_maintenance_record(maintenance_id):
    """Delete maintenance record"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's boat and equipment IDs for access control
    user_boat_ids = [boat.id for boat in Boat.query.filter_by(owner_id=user.id).all()]
    user_equipment_ids = [eq.id for eq in Equipment.query.filter_by(owner_id=user.id).all()]
    
    maintenance = MaintenanceRecord.query.filter(
        MaintenanceRecord.id == maintenance_id,
        db.or_(
            MaintenanceRecord.boat_id.in_(user_boat_ids),
            MaintenanceRecord.equipment_id.in_(user_equipment_ids),
            MaintenanceRecord.created_by == user.id
        )
    ).first()
    
    if not maintenance:
        return jsonify({'error': 'Maintenance record not found'}), 404
    
    db.session.delete(maintenance)
    db.session.commit()
    
    return jsonify({'message': 'Maintenance record deleted successfully'})

# ============================================================
# EVENTS CRUD API ENDPOINTS
# ============================================================

@app.route('/api/events', methods=['GET'])
@jwt_required()
def get_events():
    """Get all events (public events + events created by user)"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get public events and events created by user
    events = Event.query.filter(
        db.or_(
            Event.is_public == True,
            Event.created_by == user.id
        )
    ).all()
    
    return jsonify({
        'events': [event.to_dict() for event in events],
        'count': len(events)
    })

@app.route('/api/events', methods=['POST'])
@jwt_required()
def create_event():
    """Create a new event"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data or not data.get('name') or not data.get('start_date'):
        return jsonify({'error': 'Event name and start date are required'}), 400
    
    try:
        # Create new event
        event = Event(
            name=data['name'],
            event_type=data.get('event_type'),
            description=data.get('description'),
            location=data.get('location'),
            venue=data.get('venue'),
            all_day=data.get('all_day', False),
            timezone=data.get('timezone', 'UTC'),
            organizer=data.get('organizer'),
            organizer_contact=data.get('organizer_contact'),
            website=data.get('website'),
            registration_required=data.get('registration_required', False),
            max_participants=data.get('max_participants'),
            current_participants=data.get('current_participants', 0),
            skill_level_required=data.get('skill_level_required'),
            age_restrictions=data.get('age_restrictions'),
            weather_dependent=data.get('weather_dependent', True),
            notes=data.get('notes'),
            status=data.get('status', 'Scheduled'),
            is_public=data.get('is_public', True),
            created_by=user.id
        )
        
        # Handle datetime fields
        from datetime import datetime
        event.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        
        if data.get('end_date'):
            event.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        if data.get('registration_deadline'):
            event.registration_deadline = datetime.fromisoformat(data['registration_deadline'].replace('Z', '+00:00'))
        
        if data.get('backup_date'):
            event.backup_date = datetime.fromisoformat(data['backup_date'].replace('Z', '+00:00'))
        
        # Handle numeric fields
        if data.get('registration_fee'):
            event.registration_fee = float(data['registration_fee'])
        
        # Handle JSON fields
        if data.get('boat_requirements'):
            event.set_boat_requirements(data['boat_requirements'])
        
        if data.get('prizes'):
            event.set_prizes(data['prizes'])
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'message': 'Event created successfully',
            'event': event.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create event: {str(e)}'}), 500

@app.route('/api/events/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event_by_id(event_id):
    """Get specific event by ID"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get public events or events created by user
    event = Event.query.filter(
        Event.id == event_id,
        db.or_(
            Event.is_public == True,
            Event.created_by == user.id
        )
    ).first()
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    return jsonify(event.to_dict())

@app.route('/api/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    """Update event (only creator can edit)"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    event = Event.query.filter_by(id=event_id, created_by=user.id).first()
    if not event:
        return jsonify({'error': 'Event not found or not owned by user'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        # Update basic fields
        if 'name' in data:
            event.name = data['name']
        if 'event_type' in data:
            event.event_type = data['event_type']
        if 'description' in data:
            event.description = data['description']
        if 'location' in data:
            event.location = data['location']
        if 'venue' in data:
            event.venue = data['venue']
        if 'all_day' in data:
            event.all_day = data['all_day']
        if 'timezone' in data:
            event.timezone = data['timezone']
        if 'organizer' in data:
            event.organizer = data['organizer']
        if 'organizer_contact' in data:
            event.organizer_contact = data['organizer_contact']
        if 'website' in data:
            event.website = data['website']
        if 'registration_required' in data:
            event.registration_required = data['registration_required']
        if 'max_participants' in data:
            event.max_participants = data['max_participants']
        if 'current_participants' in data:
            event.current_participants = data['current_participants']
        if 'skill_level_required' in data:
            event.skill_level_required = data['skill_level_required']
        if 'age_restrictions' in data:
            event.age_restrictions = data['age_restrictions']
        if 'weather_dependent' in data:
            event.weather_dependent = data['weather_dependent']
        if 'notes' in data:
            event.notes = data['notes']
        if 'status' in data:
            event.status = data['status']
        if 'is_public' in data:
            event.is_public = data['is_public']
        
        # Handle datetime fields
        if 'start_date' in data:
            from datetime import datetime
            event.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        
        if 'end_date' in data:
            if data['end_date']:
                from datetime import datetime
                event.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
            else:
                event.end_date = None
        
        if 'registration_deadline' in data:
            if data['registration_deadline']:
                from datetime import datetime
                event.registration_deadline = datetime.fromisoformat(data['registration_deadline'].replace('Z', '+00:00'))
            else:
                event.registration_deadline = None
        
        if 'backup_date' in data:
            if data['backup_date']:
                from datetime import datetime
                event.backup_date = datetime.fromisoformat(data['backup_date'].replace('Z', '+00:00'))
            else:
                event.backup_date = None
        
        # Handle numeric fields
        if 'registration_fee' in data:
            event.registration_fee = float(data['registration_fee']) if data['registration_fee'] else None
        
        # Handle JSON fields
        if 'boat_requirements' in data:
            event.set_boat_requirements(data['boat_requirements'])
        
        if 'prizes' in data:
            event.set_prizes(data['prizes'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Event updated successfully',
            'event': event.to_dict()
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update event: {str(e)}'}), 500

@app.route('/api/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    """Delete event (only creator can delete)"""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    event = Event.query.filter_by(id=event_id, created_by=user.id).first()
    if not event:
        return jsonify({'error': 'Event not found or not owned by user'}), 404
    
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({'message': 'Event deleted successfully'})

if __name__ == '__main__':
    import sys
    
    # Get port from command line argument or use default
    port = 5001  # Changed default port to avoid AirPlay conflict
    if len(sys.argv) > 1 and sys.argv[1].startswith('--port='):
        port = int(sys.argv[1].split('=')[1])
    elif len(sys.argv) > 2 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    
    with app.app_context():
        db.create_all()
    
    print(f"Starting Flask app on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)