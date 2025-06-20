from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Enhanced sailor-specific fields
    is_admin = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    emergency_contact = db.Column(db.String(200))
    sailing_experience = db.Column(db.String(20), default='Beginner')  # Beginner, Intermediate, Advanced, Professional
    certifications = db.Column(db.Text)  # JSON array of certifications
    default_module = db.Column(db.String(50), default='dashboard')
    profile_image_path = db.Column(db.String(255))
    last_login = db.Column(db.DateTime)
    timezone = db.Column(db.String(50), default='UTC')

    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def get_certifications(self):
        """Get certifications as list"""
        if self.certifications:
            try:
                return json.loads(self.certifications)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_certifications(self, cert_list):
        """Set certifications from list"""
        self.certifications = json.dumps(cert_list) if cert_list else None
    
    def get_full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username

    def to_dict(self):
        """Convert user to dictionary for JSON response"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'phone': self.phone,
            'emergency_contact': self.emergency_contact,
            'sailing_experience': self.sailing_experience,
            'certifications': self.get_certifications(),
            'default_module': self.default_module,
            'profile_image_path': self.profile_image_path,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'timezone': self.timezone
        }


class SystemModule(db.Model):
    __tablename__ = 'system_modules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., "boats", "trips"
    display_name = db.Column(db.String(100), nullable=False)  # e.g., "Fleet Management"
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Icon class/name for UI
    is_active = db.Column(db.Boolean, default=True)  # Admin can disable modules globally
    requires_admin = db.Column(db.Boolean, default=False)  # Admin-only modules
    sort_order = db.Column(db.Integer, default=0)  # Navigation display order
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert module to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'icon': self.icon,
            'is_active': self.is_active,
            'requires_admin': self.requires_admin,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UserModulePermission(db.Model):
    __tablename__ = 'user_module_permissions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('system_modules.id'), nullable=False)
    is_enabled = db.Column(db.Boolean, default=True)  # User preference
    granted_at = db.Column(db.DateTime, default=datetime.utcnow)
    granted_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # Admin who granted access
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='module_permissions')
    module = db.relationship('SystemModule', backref='user_permissions')
    granted_by_user = db.relationship('User', foreign_keys=[granted_by])
    
    # Unique constraint to prevent duplicate permissions
    __table_args__ = (db.UniqueConstraint('user_id', 'module_id', name='_user_module_uc'),)
    
    def to_dict(self):
        """Convert permission to dictionary for JSON response"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'module_id': self.module_id,
            'module_name': self.module.name if self.module else None,
            'module_display_name': self.module.display_name if self.module else None,
            'is_enabled': self.is_enabled,
            'granted_at': self.granted_at.isoformat(),
            'granted_by': self.granted_by,
            'granted_by_username': self.granted_by_user.username if self.granted_by_user else None
        }


class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    preference_key = db.Column(db.String(100), nullable=False)  # e.g., "theme", "notifications", "units"
    preference_value = db.Column(db.Text)  # JSON string for complex preferences
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='preferences')
    
    # Unique constraint to prevent duplicate preference keys per user
    __table_args__ = (db.UniqueConstraint('user_id', 'preference_key', name='_user_preference_uc'),)
    
    def get_value(self):
        """Get preference value, attempting to parse as JSON first"""
        if self.preference_value:
            try:
                return json.loads(self.preference_value)
            except json.JSONDecodeError:
                return self.preference_value
        return None
    
    def set_value(self, value):
        """Set preference value, converting to JSON if not string"""
        if isinstance(value, str):
            self.preference_value = value
        else:
            self.preference_value = json.dumps(value)
    
    def to_dict(self):
        """Convert preference to dictionary for JSON response"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'preference_key': self.preference_key,
            'preference_value': self.get_value(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }