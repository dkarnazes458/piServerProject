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


class Boat(db.Model):
    __tablename__ = 'boats'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    boat_type = db.Column(db.String(50))  # Sailboat, Motorboat, Catamaran, etc.
    
    # Physical specifications
    length_feet = db.Column(db.Float)
    beam_feet = db.Column(db.Float) 
    draft_feet = db.Column(db.Float)
    displacement_lbs = db.Column(db.Integer)
    year_built = db.Column(db.Integer)
    hull_material = db.Column(db.String(50))  # Fiberglass, Wood, Steel, Aluminum
    
    # Registration and documentation
    registration_number = db.Column(db.String(50), unique=True)
    hin = db.Column(db.String(20))  # Hull Identification Number
    documentation_number = db.Column(db.String(20))
    
    # Ownership and location
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    home_port = db.Column(db.String(100))
    current_location = db.Column(db.String(100))
    marina_berth = db.Column(db.String(50))
    
    # Insurance and legal
    insurance_company = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    insurance_expiry = db.Column(db.Date)
    
    # Technical specifications
    engine_make = db.Column(db.String(50))
    engine_model = db.Column(db.String(50))
    engine_year = db.Column(db.Integer)
    engine_hours = db.Column(db.Float)
    fuel_capacity_gallons = db.Column(db.Float)
    water_capacity_gallons = db.Column(db.Float)
    
    # Sailing specifications
    sail_area_sqft = db.Column(db.Float)
    mast_height_feet = db.Column(db.Float)
    keel_type = db.Column(db.String(50))  # Full, Fin, Wing, Centerboard
    
    # Status and condition
    is_active = db.Column(db.Boolean, default=True)
    condition = db.Column(db.String(20), default='Good')  # Excellent, Good, Fair, Poor
    last_survey_date = db.Column(db.Date)
    next_survey_due = db.Column(db.Date)
    
    # Additional information
    notes = db.Column(db.Text)
    photos = db.Column(db.Text)  # JSON array of photo URLs
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', backref='owned_boats')
    
    def get_photos(self):
        """Get photos as list"""
        if self.photos:
            try:
                return json.loads(self.photos)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_photos(self, photo_list):
        """Set photos from list"""
        self.photos = json.dumps(photo_list) if photo_list else None
    
    def calculate_age(self):
        """Calculate boat age in years"""
        if self.year_built:
            current_year = datetime.utcnow().year
            return current_year - self.year_built
        return None
    
    def to_dict(self):
        """Convert boat to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'boat_type': self.boat_type,
            'length_feet': self.length_feet,
            'beam_feet': self.beam_feet,
            'draft_feet': self.draft_feet,
            'displacement_lbs': self.displacement_lbs,
            'year_built': self.year_built,
            'age_years': self.calculate_age(),
            'hull_material': self.hull_material,
            'registration_number': self.registration_number,
            'hin': self.hin,
            'documentation_number': self.documentation_number,
            'owner_id': self.owner_id,
            'owner_name': self.owner.get_full_name() if self.owner else None,
            'home_port': self.home_port,
            'current_location': self.current_location,
            'marina_berth': self.marina_berth,
            'insurance_company': self.insurance_company,
            'insurance_policy_number': self.insurance_policy_number,
            'insurance_expiry': self.insurance_expiry.isoformat() if self.insurance_expiry else None,
            'engine_make': self.engine_make,
            'engine_model': self.engine_model,
            'engine_year': self.engine_year,
            'engine_hours': self.engine_hours,
            'fuel_capacity_gallons': self.fuel_capacity_gallons,
            'water_capacity_gallons': self.water_capacity_gallons,
            'sail_area_sqft': self.sail_area_sqft,
            'mast_height_feet': self.mast_height_feet,
            'keel_type': self.keel_type,
            'is_active': self.is_active,
            'condition': self.condition,
            'last_survey_date': self.last_survey_date.isoformat() if self.last_survey_date else None,
            'next_survey_due': self.next_survey_due.isoformat() if self.next_survey_due else None,
            'notes': self.notes,
            'photos': self.get_photos(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # Safety, Navigation, Maintenance, Sail, Electronics, etc.
    subcategory = db.Column(db.String(50))  # Life Jacket, GPS, Wrench Set, Jib, VHF Radio
    
    # Product information
    brand = db.Column(db.String(50))
    model = db.Column(db.String(100))
    part_number = db.Column(db.String(50))
    serial_number = db.Column(db.String(100))
    
    # Purchase information
    purchase_date = db.Column(db.Date)
    purchase_price = db.Column(db.Numeric(10, 2))
    purchase_location = db.Column(db.String(100))
    warranty_period_months = db.Column(db.Integer)
    warranty_expiry = db.Column(db.Date)
    
    # Ownership and location
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'))  # Optional - may be portable
    location_on_boat = db.Column(db.String(100))  # "Port Locker", "Nav Station", "Engine Compartment"
    current_location = db.Column(db.String(100))  # If not on boat
    
    # Condition and status
    condition = db.Column(db.String(20), default='Good')  # Excellent, Good, Fair, Poor, Needs Repair
    is_operational = db.Column(db.Boolean, default=True)
    last_inspection_date = db.Column(db.Date)
    next_inspection_due = db.Column(db.Date)
    
    # Specifications and details
    specifications = db.Column(db.Text)  # JSON string for flexible specs
    quantity = db.Column(db.Integer, default=1)
    weight_lbs = db.Column(db.Float)
    dimensions = db.Column(db.String(100))  # "12x8x3 inches"
    
    # Documentation
    manual_url = db.Column(db.String(255))
    photos = db.Column(db.Text)  # JSON array of photo URLs
    documents = db.Column(db.Text)  # JSON array of document URLs
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', backref='equipment')
    boat = db.relationship('Boat', backref='equipment')
    
    def get_specifications(self):
        """Get specifications as dictionary"""
        if self.specifications:
            try:
                return json.loads(self.specifications)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_specifications(self, specs_dict):
        """Set specifications from dictionary"""
        self.specifications = json.dumps(specs_dict) if specs_dict else None
    
    def get_photos(self):
        """Get photos as list"""
        if self.photos:
            try:
                return json.loads(self.photos)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_photos(self, photo_list):
        """Set photos from list"""
        self.photos = json.dumps(photo_list) if photo_list else None
    
    def get_documents(self):
        """Get documents as list"""
        if self.documents:
            try:
                return json.loads(self.documents)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_documents(self, doc_list):
        """Set documents from list"""
        self.documents = json.dumps(doc_list) if doc_list else None
    
    def is_warranty_valid(self):
        """Check if warranty is still valid"""
        if self.warranty_expiry:
            from datetime import date
            return date.today() <= self.warranty_expiry
        return False
    
    def calculate_age_days(self):
        """Calculate equipment age in days"""
        if self.purchase_date:
            from datetime import date
            return (date.today() - self.purchase_date).days
        return None
    
    def to_dict(self):
        """Convert equipment to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'subcategory': self.subcategory,
            'brand': self.brand,
            'model': self.model,
            'part_number': self.part_number,
            'serial_number': self.serial_number,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'purchase_price': float(self.purchase_price) if self.purchase_price else None,
            'purchase_location': self.purchase_location,
            'warranty_period_months': self.warranty_period_months,
            'warranty_expiry': self.warranty_expiry.isoformat() if self.warranty_expiry else None,
            'warranty_valid': self.is_warranty_valid(),
            'owner_id': self.owner_id,
            'owner_name': self.owner.get_full_name() if self.owner else None,
            'boat_id': self.boat_id,
            'boat_name': self.boat.name if self.boat else None,
            'location_on_boat': self.location_on_boat,
            'current_location': self.current_location,
            'condition': self.condition,
            'is_operational': self.is_operational,
            'last_inspection_date': self.last_inspection_date.isoformat() if self.last_inspection_date else None,
            'next_inspection_due': self.next_inspection_due.isoformat() if self.next_inspection_due else None,
            'specifications': self.get_specifications(),
            'quantity': self.quantity,
            'weight_lbs': self.weight_lbs,
            'dimensions': self.dimensions,
            'manual_url': self.manual_url,
            'photos': self.get_photos(),
            'documents': self.get_documents(),
            'notes': self.notes,
            'age_days': self.calculate_age_days(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class MaintenanceRecord(db.Model):
    __tablename__ = 'maintenance_records'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # What was maintained
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))  # Optional - general boat maintenance
    
    # Maintenance details
    maintenance_type = db.Column(db.String(50), nullable=False)  # Routine, Repair, Replacement, Inspection, Upgrade
    title = db.Column(db.String(200), nullable=False)  # "Oil Change", "Sail Repair", "Engine Service"
    description = db.Column(db.Text, nullable=False)
    
    # When and who
    date_performed = db.Column(db.Date, nullable=False)
    performed_by = db.Column(db.String(100))  # Name of person/service who did the work
    performed_by_type = db.Column(db.String(50), default='Self')  # Self, Professional, Friend, Yard
    location = db.Column(db.String(100))  # Marina, Home, Boatyard, etc.
    
    # Cost and time
    cost = db.Column(db.Numeric(10, 2))
    labor_hours = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    
    # Parts and materials
    parts_used = db.Column(db.Text)  # JSON array of parts
    parts_cost = db.Column(db.Numeric(10, 2))
    labor_cost = db.Column(db.Numeric(10, 2))
    
    # Scheduling
    next_maintenance_due = db.Column(db.Date)
    next_maintenance_hours = db.Column(db.Float)  # Engine hours when next service due
    maintenance_interval_days = db.Column(db.Integer)  # How often this should be done
    maintenance_interval_hours = db.Column(db.Float)  # Engine hour intervals
    
    # Documentation
    photos = db.Column(db.Text)  # JSON array of photo URLs
    documents = db.Column(db.Text)  # JSON array of document URLs (receipts, invoices)
    notes = db.Column(db.Text)
    
    # Status and tracking
    status = db.Column(db.String(20), default='Completed')  # Planned, In Progress, Completed, Cancelled
    priority = db.Column(db.String(10), default='Medium')  # Low, Medium, High, Critical
    warranty_work = db.Column(db.Boolean, default=False)
    
    # Relationships and tracking
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    boat = db.relationship('Boat', backref='maintenance_records')
    equipment = db.relationship('Equipment', backref='maintenance_records')
    creator = db.relationship('User', backref='created_maintenance_records')
    
    def get_parts_used(self):
        """Get parts used as list"""
        if self.parts_used:
            try:
                return json.loads(self.parts_used)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_parts_used(self, parts_list):
        """Set parts used from list"""
        self.parts_used = json.dumps(parts_list) if parts_list else None
    
    def get_photos(self):
        """Get photos as list"""
        if self.photos:
            try:
                return json.loads(self.photos)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_photos(self, photo_list):
        """Set photos from list"""
        self.photos = json.dumps(photo_list) if photo_list else None
    
    def get_documents(self):
        """Get documents as list"""
        if self.documents:
            try:
                return json.loads(self.documents)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_documents(self, doc_list):
        """Set documents from list"""
        self.documents = json.dumps(doc_list) if doc_list else None
    
    def calculate_total_cost(self):
        """Calculate total maintenance cost"""
        total = 0
        if self.parts_cost:
            total += float(self.parts_cost)
        if self.labor_cost:
            total += float(self.labor_cost)
        if not total and self.cost:
            total = float(self.cost)
        return total
    
    def is_overdue(self):
        """Check if next maintenance is overdue"""
        if self.next_maintenance_due:
            from datetime import date
            return date.today() > self.next_maintenance_due
        return False
    
    def days_until_due(self):
        """Calculate days until next maintenance is due"""
        if self.next_maintenance_due:
            from datetime import date
            delta = self.next_maintenance_due - date.today()
            return delta.days
        return None
    
    def to_dict(self):
        """Convert maintenance record to dictionary for JSON response"""
        return {
            'id': self.id,
            'boat_id': self.boat_id,
            'boat_name': self.boat.name if self.boat else None,
            'equipment_id': self.equipment_id,
            'equipment_name': self.equipment.name if self.equipment else None,
            'maintenance_type': self.maintenance_type,
            'title': self.title,
            'description': self.description,
            'date_performed': self.date_performed.isoformat(),
            'performed_by': self.performed_by,
            'performed_by_type': self.performed_by_type,
            'location': self.location,
            'cost': float(self.cost) if self.cost else None,
            'labor_hours': self.labor_hours,
            'currency': self.currency,
            'parts_used': self.get_parts_used(),
            'parts_cost': float(self.parts_cost) if self.parts_cost else None,
            'labor_cost': float(self.labor_cost) if self.labor_cost else None,
            'total_cost': self.calculate_total_cost(),
            'next_maintenance_due': self.next_maintenance_due.isoformat() if self.next_maintenance_due else None,
            'next_maintenance_hours': self.next_maintenance_hours,
            'maintenance_interval_days': self.maintenance_interval_days,
            'maintenance_interval_hours': self.maintenance_interval_hours,
            'photos': self.get_photos(),
            'documents': self.get_documents(),
            'notes': self.notes,
            'status': self.status,
            'priority': self.priority,
            'warranty_work': self.warranty_work,
            'is_overdue': self.is_overdue(),
            'days_until_due': self.days_until_due(),
            'created_by': self.created_by,
            'creator_name': self.creator.get_full_name() if self.creator else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    event_type = db.Column(db.String(50))  # Race, Regatta, Social, Training, Maintenance, Trip
    
    # Event details
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    venue = db.Column(db.String(100))  # Marina, yacht club, etc.
    
    # Timing
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    all_day = db.Column(db.Boolean, default=False)
    timezone = db.Column(db.String(50), default='UTC')
    
    # Organization
    organizer = db.Column(db.String(100))
    organizer_contact = db.Column(db.String(200))  # Email or phone
    website = db.Column(db.String(255))
    
    # Registration and participation
    registration_required = db.Column(db.Boolean, default=False)
    registration_deadline = db.Column(db.DateTime)
    registration_fee = db.Column(db.Numeric(10, 2))
    max_participants = db.Column(db.Integer)
    current_participants = db.Column(db.Integer, default=0)
    
    # Requirements and restrictions
    boat_requirements = db.Column(db.Text)  # JSON - length, type, equipment requirements
    skill_level_required = db.Column(db.String(50))  # Beginner, Intermediate, Advanced, Professional
    age_restrictions = db.Column(db.String(100))
    
    # Additional information
    weather_dependent = db.Column(db.Boolean, default=True)
    backup_date = db.Column(db.DateTime)
    prizes = db.Column(db.Text)  # JSON array of prizes/awards
    notes = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Cancelled, Postponed, Completed
    is_public = db.Column(db.Boolean, default=True)
    
    # Creation tracking
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='created_events')
    
    def get_boat_requirements(self):
        """Get boat requirements as dictionary"""
        if self.boat_requirements:
            try:
                return json.loads(self.boat_requirements)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_boat_requirements(self, requirements_dict):
        """Set boat requirements from dictionary"""
        self.boat_requirements = json.dumps(requirements_dict) if requirements_dict else None
    
    def get_prizes(self):
        """Get prizes as list"""
        if self.prizes:
            try:
                return json.loads(self.prizes)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_prizes(self, prizes_list):
        """Set prizes from list"""
        self.prizes = json.dumps(prizes_list) if prizes_list else None
    
    def is_registration_open(self):
        """Check if registration is still open"""
        if not self.registration_required:
            return True
        if self.registration_deadline:
            return datetime.utcnow() <= self.registration_deadline
        return True
    
    def is_full(self):
        """Check if event is at capacity"""
        if self.max_participants:
            return self.current_participants >= self.max_participants
        return False
    
    def can_register(self):
        """Check if new registrations are possible"""
        return self.is_registration_open() and not self.is_full() and self.status == 'Scheduled'
    
    def days_until_event(self):
        """Calculate days until event starts"""
        if self.start_date:
            delta = self.start_date - datetime.utcnow()
            return delta.days
        return None
    
    def duration_hours(self):
        """Calculate event duration in hours"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return delta.total_seconds() / 3600
        return None
    
    def to_dict(self):
        """Convert event to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'event_type': self.event_type,
            'description': self.description,
            'location': self.location,
            'venue': self.venue,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'all_day': self.all_day,
            'timezone': self.timezone,
            'organizer': self.organizer,
            'organizer_contact': self.organizer_contact,
            'website': self.website,
            'registration_required': self.registration_required,
            'registration_deadline': self.registration_deadline.isoformat() if self.registration_deadline else None,
            'registration_fee': float(self.registration_fee) if self.registration_fee else None,
            'max_participants': self.max_participants,
            'current_participants': self.current_participants,
            'spots_available': (self.max_participants - self.current_participants) if self.max_participants else None,
            'boat_requirements': self.get_boat_requirements(),
            'skill_level_required': self.skill_level_required,
            'age_restrictions': self.age_restrictions,
            'weather_dependent': self.weather_dependent,
            'backup_date': self.backup_date.isoformat() if self.backup_date else None,
            'prizes': self.get_prizes(),
            'notes': self.notes,
            'status': self.status,
            'is_public': self.is_public,
            'registration_open': self.is_registration_open(),
            'is_full': self.is_full(),
            'can_register': self.can_register(),
            'days_until_event': self.days_until_event(),
            'duration_hours': self.duration_hours(),
            'created_by': self.created_by,
            'creator_name': self.creator.get_full_name() if self.creator else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Trip(db.Model):
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic trip information
    name = db.Column(db.String(200), nullable=False)  # "Weekend Cruise", "Catalina Island Trip"
    description = db.Column(db.Text)
    trip_type = db.Column(db.String(50), default='Leisure')  # Leisure, Racing, Training, Delivery, Charter
    
    # Boat and crew
    boat_id = db.Column(db.Integer, db.ForeignKey('boats.id'), nullable=False)
    captain_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crew_size = db.Column(db.Integer, default=1)
    
    # Timing
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    planned_duration_hours = db.Column(db.Float)
    actual_duration_hours = db.Column(db.Float)
    
    # Locations
    start_location = db.Column(db.String(200))  # Port/Marina name
    end_location = db.Column(db.String(200))
    start_latitude = db.Column(db.Numeric(10, 8))  # GPS coordinates
    start_longitude = db.Column(db.Numeric(11, 8))
    end_latitude = db.Column(db.Numeric(10, 8))
    end_longitude = db.Column(db.Numeric(11, 8))
    
    # Trip metrics
    distance_miles = db.Column(db.Float)  # Nautical miles
    distance_calculated = db.Column(db.Float)  # Auto-calculated from GPS track
    max_speed_knots = db.Column(db.Float)
    avg_speed_knots = db.Column(db.Float)
    max_wind_speed_knots = db.Column(db.Float)
    avg_wind_speed_knots = db.Column(db.Float)
    wind_direction = db.Column(db.String(50))
    
    # Conditions and notes
    weather_conditions = db.Column(db.Text)  # JSON or text description
    sea_conditions = db.Column(db.Text)
    visibility = db.Column(db.String(50))  # Excellent, Good, Fair, Poor
    tide_conditions = db.Column(db.Text)
    fuel_used_gallons = db.Column(db.Float)
    fuel_cost = db.Column(db.Numeric(8, 2))
    
    # GPS and route data
    gps_file_path = db.Column(db.String(500))  # Path to uploaded GPS file
    gps_file_name = db.Column(db.String(255))  # Original filename
    gps_file_size = db.Column(db.Integer)  # File size in bytes
    gps_file_type = db.Column(db.String(10))  # gpx, kml, nmea, csv
    route_processed = db.Column(db.Boolean, default=False)  # Whether GPS data has been processed
    total_route_points = db.Column(db.Integer, default=0)
    
    # Trip status and logistics
    status = db.Column(db.String(50), default='Planned')  # Planned, In Progress, Completed, Cancelled
    purpose = db.Column(db.String(100))  # Business, Pleasure, Training, Racing, etc.
    difficulty_level = db.Column(db.String(20), default='Moderate')  # Easy, Moderate, Challenging, Expert
    
    # Safety and emergency
    emergency_contact = db.Column(db.String(200))
    float_plan_filed = db.Column(db.Boolean, default=False)
    float_plan_with = db.Column(db.String(200))  # Who has the float plan
    safety_equipment_check = db.Column(db.Boolean, default=False)
    
    # Costs and expenses
    total_cost = db.Column(db.Numeric(10, 2))
    cost_breakdown = db.Column(db.Text)  # JSON of expense categories
    
    # Experience and learning
    lessons_learned = db.Column(db.Text)
    highlights = db.Column(db.Text)
    challenges_faced = db.Column(db.Text)
    overall_rating = db.Column(db.Integer)  # 1-5 star rating
    would_repeat = db.Column(db.Boolean)
    
    # Documentation
    photos = db.Column(db.Text)  # JSON array of photo paths
    documents = db.Column(db.Text)  # JSON array of document paths
    logbook_entries = db.Column(db.Text)  # JSON array of detailed log entries
    
    # Metadata
    is_public = db.Column(db.Boolean, default=False)  # Share with community
    is_favorite = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)  # JSON array of tags
    
    # Relationships
    boat = db.relationship('Boat', backref='trips')
    captain = db.relationship('User', foreign_keys=[captain_id], backref='captained_trips')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_weather_conditions(self):
        """Get weather conditions as dict"""
        if self.weather_conditions:
            try:
                return json.loads(self.weather_conditions)
            except json.JSONDecodeError:
                return {'description': self.weather_conditions}
        return {}
    
    def set_weather_conditions(self, conditions_dict):
        """Set weather conditions from dict"""
        self.weather_conditions = json.dumps(conditions_dict) if conditions_dict else None
    
    def get_cost_breakdown(self):
        """Get cost breakdown as dict"""
        if self.cost_breakdown:
            try:
                return json.loads(self.cost_breakdown)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_cost_breakdown(self, costs_dict):
        """Set cost breakdown from dict"""
        self.cost_breakdown = json.dumps(costs_dict) if costs_dict else None
    
    def get_photos(self):
        """Get photos as list"""
        if self.photos:
            try:
                return json.loads(self.photos)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_photos(self, photo_list):
        """Set photos from list"""
        self.photos = json.dumps(photo_list) if photo_list else None
    
    def get_documents(self):
        """Get documents as list"""
        if self.documents:
            try:
                return json.loads(self.documents)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_documents(self, doc_list):
        """Set documents from list"""
        self.documents = json.dumps(doc_list) if doc_list else None
    
    def get_logbook_entries(self):
        """Get logbook entries as list"""
        if self.logbook_entries:
            try:
                return json.loads(self.logbook_entries)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_logbook_entries(self, entries_list):
        """Set logbook entries from list"""
        self.logbook_entries = json.dumps(entries_list) if entries_list else None
    
    def get_tags(self):
        """Get tags as list"""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_tags(self, tag_list):
        """Set tags from list"""
        self.tags = json.dumps(tag_list) if tag_list else None
    
    def calculate_actual_duration(self):
        """Calculate actual trip duration in hours"""
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            return delta.total_seconds() / 3600
        return None
    
    def calculate_average_speed(self):
        """Calculate average speed based on distance and duration"""
        duration = self.actual_duration_hours or self.calculate_actual_duration()
        if duration and duration > 0 and self.distance_miles:
            return self.distance_miles / duration
        return None
    
    def is_completed(self):
        """Check if trip is completed"""
        return self.status == 'Completed'
    
    def is_in_progress(self):
        """Check if trip is currently in progress"""
        return self.status == 'In Progress'
    
    def days_since_trip(self):
        """Calculate days since trip ended"""
        if self.end_date:
            delta = datetime.utcnow() - self.end_date
            return delta.days
        return None
    
    def to_dict(self):
        """Convert trip to dictionary for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'trip_type': self.trip_type,
            'boat_id': self.boat_id,
            'boat_name': self.boat.name if self.boat else None,
            'captain_id': self.captain_id,
            'captain_name': self.captain.get_full_name() if self.captain else None,
            'crew_size': self.crew_size,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'planned_duration_hours': self.planned_duration_hours,
            'actual_duration_hours': self.actual_duration_hours or self.calculate_actual_duration(),
            'start_location': self.start_location,
            'end_location': self.end_location,
            'start_latitude': float(self.start_latitude) if self.start_latitude else None,
            'start_longitude': float(self.start_longitude) if self.start_longitude else None,
            'end_latitude': float(self.end_latitude) if self.end_latitude else None,
            'end_longitude': float(self.end_longitude) if self.end_longitude else None,
            'distance_miles': self.distance_miles,
            'distance_calculated': self.distance_calculated,
            'max_speed_knots': self.max_speed_knots,
            'avg_speed_knots': self.avg_speed_knots or self.calculate_average_speed(),
            'max_wind_speed_knots': self.max_wind_speed_knots,
            'avg_wind_speed_knots': self.avg_wind_speed_knots,
            'wind_direction': self.wind_direction,
            'weather_conditions': self.get_weather_conditions(),
            'sea_conditions': self.sea_conditions,
            'visibility': self.visibility,
            'tide_conditions': self.tide_conditions,
            'fuel_used_gallons': self.fuel_used_gallons,
            'fuel_cost': float(self.fuel_cost) if self.fuel_cost else None,
            'gps_file_name': self.gps_file_name,
            'gps_file_size': self.gps_file_size,
            'gps_file_type': self.gps_file_type,
            'route_processed': self.route_processed,
            'total_route_points': self.total_route_points,
            'status': self.status,
            'purpose': self.purpose,
            'difficulty_level': self.difficulty_level,
            'emergency_contact': self.emergency_contact,
            'float_plan_filed': self.float_plan_filed,
            'float_plan_with': self.float_plan_with,
            'safety_equipment_check': self.safety_equipment_check,
            'total_cost': float(self.total_cost) if self.total_cost else None,
            'cost_breakdown': self.get_cost_breakdown(),
            'lessons_learned': self.lessons_learned,
            'highlights': self.highlights,
            'challenges_faced': self.challenges_faced,
            'overall_rating': self.overall_rating,
            'would_repeat': self.would_repeat,
            'photos': self.get_photos(),
            'documents': self.get_documents(),
            'logbook_entries': self.get_logbook_entries(),
            'is_public': self.is_public,
            'is_favorite': self.is_favorite,
            'notes': self.notes,
            'tags': self.get_tags(),
            'is_completed': self.is_completed(),
            'is_in_progress': self.is_in_progress(),
            'days_since_trip': self.days_since_trip(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class GPSRoutePoint(db.Model):
    __tablename__ = 'gps_route_points'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    
    # GPS coordinates
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    altitude = db.Column(db.Float)  # In meters above sea level
    
    # Timing
    timestamp = db.Column(db.DateTime, nullable=False)
    elapsed_time_seconds = db.Column(db.Integer)  # Seconds since trip start
    
    # Movement data
    speed_knots = db.Column(db.Float)
    speed_over_ground = db.Column(db.Float)  # GPS calculated speed
    course_over_ground = db.Column(db.Float)  # GPS calculated heading (degrees)
    heading = db.Column(db.Float)  # Compass heading (degrees from north)
    
    # GPS quality and accuracy
    accuracy = db.Column(db.Float)  # GPS accuracy in meters
    satellites_used = db.Column(db.Integer)  # Number of GPS satellites
    hdop = db.Column(db.Float)  # Horizontal Dilution of Precision
    signal_quality = db.Column(db.String(20))  # Excellent, Good, Fair, Poor
    
    # Point classification
    point_type = db.Column(db.String(20), default='track')  # track, waypoint, anchor, mooring, mark
    point_name = db.Column(db.String(100))  # Name for waypoints/marks
    
    # Environmental data (if available)
    water_depth = db.Column(db.Float)  # Depth in feet or meters
    water_temperature = db.Column(db.Float)
    air_temperature = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    wind_direction = db.Column(db.Float)
    barometric_pressure = db.Column(db.Float)
    
    # Distance calculations
    distance_from_previous = db.Column(db.Float)  # Nautical miles from previous point
    cumulative_distance = db.Column(db.Float)  # Total distance from trip start
    
    # Engine and sail data
    engine_rpm = db.Column(db.Integer)
    engine_temperature = db.Column(db.Float)
    fuel_flow_rate = db.Column(db.Float)
    sail_configuration = db.Column(db.String(100))  # "Main + Jib", "Spinnaker", etc.
    
    # Additional data
    notes = db.Column(db.Text)  # Any notes about this specific point
    is_significant = db.Column(db.Boolean, default=False)  # Mark important points
    
    # Relationships
    trip = db.relationship('Trip', backref='route_points')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def distance_to_point(self, other_point):
        """Calculate distance to another GPS point using Haversine formula"""
        # Convert latitude and longitude to radians
        lat1 = math.radians(float(self.latitude))
        lon1 = math.radians(float(self.longitude))
        lat2 = math.radians(float(other_point.latitude))
        lon2 = math.radians(float(other_point.longitude))
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in nautical miles
        r = 3440.065
        
        return c * r
    
    def bearing_to_point(self, other_point):
        """Calculate bearing to another GPS point"""
        lat1 = math.radians(float(self.latitude))
        lon1 = math.radians(float(self.longitude))
        lat2 = math.radians(float(other_point.latitude))
        lon2 = math.radians(float(other_point.longitude))
        
        dlon = lon2 - lon1
        
        y = math.sin(dlon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
        
        bearing = math.degrees(math.atan2(y, x))
        
        # Normalize to 0-360 degrees
        return (bearing + 360) % 360
    
    def time_since_previous(self, previous_point):
        """Calculate time elapsed since previous point"""
        if previous_point and previous_point.timestamp:
            delta = self.timestamp - previous_point.timestamp
            return delta.total_seconds()
        return None
    
    def to_dict(self):
        """Convert GPS point to dictionary for JSON response"""
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'altitude': self.altitude,
            'timestamp': self.timestamp.isoformat(),
            'elapsed_time_seconds': self.elapsed_time_seconds,
            'speed_knots': self.speed_knots,
            'speed_over_ground': self.speed_over_ground,
            'course_over_ground': self.course_over_ground,
            'heading': self.heading,
            'accuracy': self.accuracy,
            'satellites_used': self.satellites_used,
            'hdop': self.hdop,
            'signal_quality': self.signal_quality,
            'point_type': self.point_type,
            'point_name': self.point_name,
            'water_depth': self.water_depth,
            'water_temperature': self.water_temperature,
            'air_temperature': self.air_temperature,
            'wind_speed': self.wind_speed,
            'wind_direction': self.wind_direction,
            'barometric_pressure': self.barometric_pressure,
            'distance_from_previous': self.distance_from_previous,
            'cumulative_distance': self.cumulative_distance,
            'engine_rpm': self.engine_rpm,
            'engine_temperature': self.engine_temperature,
            'fuel_flow_rate': self.fuel_flow_rate,
            'sail_configuration': self.sail_configuration,
            'notes': self.notes,
            'is_significant': self.is_significant,
            'created_at': self.created_at.isoformat()
        }


# Relationship tables for many-to-many relationships

class TripParticipant(db.Model):
    __tablename__ = 'trip_participants'
    
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Role and participation details
    role = db.Column(db.String(50), default='Crew')  # Captain, Crew, Guest, Observer, Instructor
    is_confirmed = db.Column(db.Boolean, default=True)
    experience_level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    
    # Participation tracking
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    left_at = db.Column(db.DateTime)  # If they left early
    hours_participated = db.Column(db.Float)
    
    # Emergency and contact info
    emergency_contact = db.Column(db.String(200))
    medical_notes = db.Column(db.Text)
    dietary_restrictions = db.Column(db.Text)
    
    # Cost sharing
    cost_share = db.Column(db.Numeric(8, 2))  # Amount this person paid
    cost_share_percentage = db.Column(db.Float)  # Percentage of total cost
    
    # Performance and feedback
    performance_rating = db.Column(db.Integer)  # 1-5 rating of their contribution
    notes = db.Column(db.Text)  # Notes about this person's participation
    
    # Relationships
    trip = db.relationship('Trip', backref='participants')
    user = db.relationship('User', backref='trip_participations')
    
    # Unique constraint to prevent duplicate participant entries
    __table_args__ = (db.UniqueConstraint('trip_id', 'user_id', name='_trip_user_uc'),)
    
    def to_dict(self):
        """Convert trip participant to dictionary for JSON response"""
        return {
            'id': self.id,
            'trip_id': self.trip_id,
            'trip_name': self.trip.name if self.trip else None,
            'user_id': self.user_id,
            'user_name': self.user.get_full_name() if self.user else None,
            'username': self.user.username if self.user else None,
            'role': self.role,
            'is_confirmed': self.is_confirmed,
            'experience_level': self.experience_level,
            'joined_at': self.joined_at.isoformat(),
            'left_at': self.left_at.isoformat() if self.left_at else None,
            'hours_participated': self.hours_participated,
            'emergency_contact': self.emergency_contact,
            'medical_notes': self.medical_notes,
            'dietary_restrictions': self.dietary_restrictions,
            'cost_share': float(self.cost_share) if self.cost_share else None,
            'cost_share_percentage': self.cost_share_percentage,
            'performance_rating': self.performance_rating,
            'notes': self.notes
        }