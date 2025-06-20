from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from functools import wraps
from config import Config
from models import db, User, SystemModule, UserModulePermission, UserPreference, Boat, Equipment, MaintenanceRecord, Event

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)