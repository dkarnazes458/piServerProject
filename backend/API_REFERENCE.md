# Sailor Utility API Reference

## Current Status
✅ **Completed APIs**: Module Management, Authentication, Boats, Trips, Equipment, Maintenance, Events  
🚧 **In Development**: GPS Processing, Advanced Search, File Upload  
📅 **Planned**: Navigation, Social, Event Registration  

## Authentication
All endpoints require JWT token in header: `Authorization: Bearer <token>`

## Admin Authorization
Endpoints marked with 🔒 require admin privileges (`is_admin: true`)

## Table of Contents
- [Module Management APIs](#module-management-apis)
- [User Module APIs](#user-module-apis)
- [User Preferences APIs](#user-preferences-apis)
- [Enhanced Authentication APIs](#enhanced-authentication-apis)
- [Entity CRUD APIs](#entity-crud-apis)
  - [Boats API](#boats-api)
  - [Trips API](#trips-api)
  - [Equipment API](#equipment-api)
  - [Maintenance API](#maintenance-api)
  - [Events API](#events-api)
- [Error Responses](#error-responses)
- [Module System Architecture](#module-system-architecture)

---

## Module Management APIs

### 🔒 System Module Administration

#### GET `/api/admin/modules`
Get all system modules (admin only)
```json
Response: {
  "modules": [
    {
      "id": 1,
      "name": "dashboard",
      "display_name": "Dashboard",
      "description": "Main dashboard",
      "icon": "dashboard",
      "is_active": true,
      "requires_admin": false,
      "sort_order": 1
    }
  ],
  "count": 9
}
```

#### POST `/api/admin/modules`
Create new system module (admin only)
```json
Request: {
  "name": "weather",
  "display_name": "Weather Tracker",
  "description": "Track weather conditions",
  "icon": "cloud",
  "is_active": true,
  "requires_admin": false,
  "sort_order": 10
}
```

#### PUT `/api/admin/modules/{module_id}`
Update system module (admin only)
```json
Request: {
  "display_name": "Updated Name",
  "description": "Updated description",
  "is_active": false
}
```

#### DELETE `/api/admin/modules/{module_id}`
Delete system module (admin only)
- Cannot delete core modules: `dashboard`, `admin`

### 🔒 User Permission Management

#### GET `/api/admin/users/{user_id}/modules`
Get user's module permissions (admin only)
```json
Response: {
  "user": { ... },
  "modules": [
    {
      "id": 1,
      "name": "dashboard",
      "display_name": "Dashboard",
      "has_permission": true,
      "is_enabled": true,
      "granted_at": "2024-01-01T12:00:00"
    }
  ]
}
```

#### POST `/api/admin/users/{user_id}/modules`
Grant module access to user (admin only)
```json
Request: {
  "module_id": 3
}
```

#### DELETE `/api/admin/users/{user_id}/modules/{module_id}`
Revoke module access from user (admin only)
- Cannot revoke core modules: `dashboard`

---

## User Module APIs

#### GET `/api/user/modules`
Get current user's available modules
```json
Response: {
  "modules": [
    {
      "id": 1,
      "name": "dashboard",
      "display_name": "Dashboard",
      "is_enabled": true,
      "sort_order": 1
    }
  ],
  "count": 5
}
```

#### PUT `/api/user/modules/{module_id}/toggle`
Enable/disable module for current user
```json
Response: {
  "message": "Module enabled successfully",
  "module": {
    "id": 3,
    "name": "trips",
    "display_name": "Trip Logbook",
    "is_enabled": true
  }
}
```

---

## User Preferences APIs

#### GET `/api/user/preferences`
Get current user's preferences
```json
Response: {
  "preferences": {
    "theme": "dark",
    "notifications": true,
    "default_units": "metric",
    "default_module": "dashboard"
  },
  "count": 4
}
```

#### PUT `/api/user/preferences`
Update current user's preferences
```json
Request: {
  "theme": "light",
  "notifications": false,
  "default_units": "imperial",
  "language": "en"
}
```

---

## Enhanced Authentication APIs

#### POST `/api/auth/login`
Enhanced login with sailor-specific fields
```json
Request: {
  "username": "sailor1",
  "password": "password123"
}

Response: {
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "sailor1",
    "email": "sailor1@example.com",
    "full_name": "John Sailor",
    "is_admin": false,
    "sailing_experience": "Intermediate",
    "certifications": ["Basic Sailing", "VHF Radio"],
    "default_module": "dashboard",
    "timezone": "UTC"
  },
  "access_token": "eyJ..."
}
```

#### GET `/api/auth/me`
Get current user with enhanced fields
```json
Response: {
  "user": {
    "id": 1,
    "username": "sailor1",
    "full_name": "John Sailor",
    "is_admin": false,
    "sailing_experience": "Intermediate",
    "certifications": ["Basic Sailing"],
    "default_module": "dashboard",
    "timezone": "UTC",
    "phone": "+1234567890",
    "emergency_contact": "Jane Doe - +0987654321"
  }
}
```

---

## Entity CRUD APIs

### Boats API

#### GET `/api/boats`
Get all boats for current user
```json
Response: {
  "boats": [
    {
      "id": 1,
      "name": "Sea Wanderer",
      "boat_type": "Sailboat",
      "length_feet": 35.0,
      "beam_feet": 12.0,
      "draft_feet": 5.5,
      "year_built": 2015,
      "hull_material": "Fiberglass",
      "registration_number": "NY123456",
      "home_port": "New York Harbor",
      "owner_id": 1,
      "is_active": true,
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ],
  "count": 1
}
```

#### POST `/api/boats`
Create a new boat
```json
Request: {
  "name": "Sea Wanderer",
  "boat_type": "Sailboat",
  "length_feet": 35.0,
  "beam_feet": 12.0,
  "draft_feet": 5.5,
  "year_built": 2015,
  "hull_material": "Fiberglass",
  "registration_number": "NY123456",
  "home_port": "New York Harbor"
}

Response: {
  "message": "Boat created successfully",
  "boat": { ... }
}
```

#### GET `/api/boats/{boat_id}`
Get specific boat details

#### PUT `/api/boats/{boat_id}`
Update boat (owner only)

#### DELETE `/api/boats/{boat_id}`
Delete boat (owner only)

---

### Trips API

#### GET `/api/trips`
Get all trips for current user
```json
Response: {
  "trips": [
    {
      "id": 1,
      "name": "Weekend Sailing",
      "boat_id": 1,
      "boat_name": "Sea Wanderer",
      "captain_id": 1,
      "captain_name": "John Sailor",
      "start_date": "2024-06-15T09:00:00",
      "end_date": "2024-06-15T17:00:00",
      "start_location": "Marina Bay",
      "end_location": "Sunset Cove",
      "distance_miles": 25.5,
      "duration_hours": 8.0,
      "status": "Completed",
      "weather_conditions": "Clear skies, 10-15 kt winds",
      "notes": "Perfect sailing conditions"
    }
  ],
  "count": 1
}
```

#### POST `/api/trips`
Create a new trip
```json
Request: {
  "name": "Weekend Sailing",
  "boat_id": 1,
  "start_date": "2024-06-15T09:00:00",
  "end_date": "2024-06-15T17:00:00",
  "start_location": "Marina Bay",
  "end_location": "Sunset Cove",
  "weather_conditions": "Clear skies, 10-15 kt winds"
}
```

#### GET `/api/trips/{trip_id}`
Get specific trip details

#### PUT `/api/trips/{trip_id}`
Update trip (captain/creator only)

#### DELETE `/api/trips/{trip_id}`
Delete trip (captain/creator only)

---

### Equipment API

#### GET `/api/equipment`
Get all equipment for current user
```json
Response: {
  "equipment": [
    {
      "id": 1,
      "name": "VHF Radio",
      "category": "Electronics",
      "subcategory": "Communication",
      "brand": "Standard Horizon",
      "model": "GX2200",
      "serial_number": "SH123456",
      "purchase_date": "2023-05-15",
      "purchase_price": 249.99,
      "warranty_expiry": "2025-05-15",
      "warranty_valid": true,
      "boat_id": 1,
      "boat_name": "Sea Wanderer",
      "location_on_boat": "Nav Station",
      "condition": "Excellent",
      "is_operational": true,
      "quantity": 1,
      "age_days": 425
    }
  ],
  "count": 1
}
```

#### POST `/api/equipment`
Create a new equipment item
```json
Request: {
  "name": "VHF Radio",
  "category": "Electronics",
  "brand": "Standard Horizon",
  "model": "GX2200",
  "purchase_date": "2023-05-15",
  "purchase_price": 249.99,
  "boat_id": 1,
  "location_on_boat": "Nav Station"
}
```

#### GET `/api/equipment/{equipment_id}`
Get specific equipment details

#### PUT `/api/equipment/{equipment_id}`
Update equipment (owner only)

#### DELETE `/api/equipment/{equipment_id}`
Delete equipment (owner only)

---

### Maintenance API

#### GET `/api/maintenance`
Get all maintenance records for current user's boats and equipment
```json
Response: {
  "maintenance_records": [
    {
      "id": 1,
      "boat_id": 1,
      "boat_name": "Sea Wanderer",
      "equipment_id": null,
      "maintenance_type": "Routine",
      "title": "Engine Oil Change",
      "description": "Changed engine oil and filter",
      "date_performed": "2024-06-01",
      "performed_by": "Marina Service",
      "performed_by_type": "Professional",
      "cost": 150.00,
      "labor_hours": 2.0,
      "currency": "USD",
      "parts_cost": 75.00,
      "labor_cost": 75.00,
      "total_cost": 150.00,
      "next_maintenance_due": "2024-12-01",
      "status": "Completed",
      "priority": "Medium",
      "is_overdue": false,
      "days_until_due": 120
    }
  ],
  "count": 1
}
```

#### POST `/api/maintenance`
Create a new maintenance record
```json
Request: {
  "boat_id": 1,
  "title": "Engine Oil Change",
  "description": "Changed engine oil and filter",
  "maintenance_type": "Routine",
  "date_performed": "2024-06-01",
  "cost": 150.00,
  "labor_hours": 2.0
}
```

#### GET `/api/maintenance/{maintenance_id}`
Get specific maintenance record

#### PUT `/api/maintenance/{maintenance_id}`
Update maintenance record (accessible via boat/equipment ownership)

#### DELETE `/api/maintenance/{maintenance_id}`
Delete maintenance record (accessible via boat/equipment ownership)

---

### Events API

#### GET `/api/events`
Get all events (public events + events created by user)
```json
Response: {
  "events": [
    {
      "id": 1,
      "name": "Annual Regatta",
      "event_type": "Race",
      "description": "Annual sailing regatta with multiple classes",
      "location": "Chesapeake Bay",
      "venue": "Annapolis Yacht Club",
      "start_date": "2024-07-15T10:00:00",
      "end_date": "2024-07-15T18:00:00",
      "all_day": false,
      "organizer": "Annapolis Yacht Club",
      "registration_required": true,
      "registration_deadline": "2024-07-10T23:59:59",
      "registration_fee": 50.00,
      "max_participants": 100,
      "current_participants": 45,
      "spots_available": 55,
      "skill_level_required": "Intermediate",
      "status": "Scheduled",
      "is_public": true,
      "registration_open": true,
      "can_register": true,
      "days_until_event": 25
    }
  ],
  "count": 1
}
```

#### POST `/api/events`
Create a new event
```json
Request: {
  "name": "Annual Regatta",
  "event_type": "Race",
  "description": "Annual sailing regatta",
  "start_date": "2024-07-15T10:00:00",
  "end_date": "2024-07-15T18:00:00",
  "location": "Chesapeake Bay",
  "registration_required": true,
  "registration_fee": 50.00,
  "max_participants": 100
}
```

#### GET `/api/events/{event_id}`
Get specific event details (public events or user's events)

#### PUT `/api/events/{event_id}`
Update event (creator only)

#### DELETE `/api/events/{event_id}`
Delete event (creator only)

---

## Error Responses

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid/missing token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `409` - Conflict (duplicate data)

### Error Response Format
```json
{
  "error": "Descriptive error message"
}
```

---

## Module System Architecture

### Core Modules (Cannot be deleted)
- `dashboard` - Main dashboard (cannot be disabled by users)
- `admin` - Admin panel (admin users only)

### Standard Modules
- `boats` - Fleet Management ✅ (Full CRUD API)
- `trips` - Trip Logbook with GPS support ✅ (Full CRUD API)
- `equipment` - Equipment Tracker ✅ (Full CRUD API)
- `maintenance` - Maintenance Log ✅ (Full CRUD API)
- `events` - Events Calendar ✅ (Full CRUD API)
- `navigation` - Weather & Routes
- `social` - Crew Network

### Module States
- **Active/Inactive** - Admin controlled, system-wide
- **Enabled/Disabled** - User controlled, personal preference
- **Permission Required** - Admin grants access per user
- **Admin Only** - Only admin users can access

### Security Model
1. **System Level** - Admin enables/disables modules globally
2. **Permission Level** - Admin grants module access to users
3. **User Level** - Users enable/disable their granted modules
4. **Admin Level** - Some modules require admin privileges