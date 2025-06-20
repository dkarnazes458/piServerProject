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