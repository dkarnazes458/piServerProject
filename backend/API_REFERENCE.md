# Sailor Utility API Reference

## Authentication
All endpoints require JWT token in header: `Authorization: Bearer <token>`

## Admin Authorization
Endpoints marked with 🔒 require admin privileges (`is_admin: true`)

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
- `boats` - Fleet Management
- `trips` - Trip Logbook with GPS support
- `equipment` - Equipment Tracker
- `maintenance` - Maintenance Log
- `events` - Events Calendar
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