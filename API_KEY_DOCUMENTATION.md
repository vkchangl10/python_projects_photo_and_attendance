# API Key Authentication System

## Overview
This API Key system allows you to control access to FastAPI endpoints through Django Admin Panel. Superusers can create, update, and manage API keys without touching the code.

## Features
- ✅ Generate unique API keys automatically
- ✅ Manage API keys in Django Admin Panel
- ✅ Enable/disable keys on the fly
- ✅ Track API key usage (last used timestamp)
- ✅ Add descriptions and names to keys
- ✅ Required and optional API key validation

## Setup & Migrations

### 1. Apply Migrations
```bash
python manage.py migrate
```

This creates the `api_keys` table in the database.

### 2. Create Superuser (if not already created)
```bash
python manage.py createsuperuser
```

### 3. Access Django Admin
Navigate to: `http://localhost:8000/admin`

## Managing API Keys in Django Admin

### Create New API Key
1. Go to Django Admin → **API Keys**
2. Click **Add API Key**
3. Fill in:
   - **Name**: Descriptive name (e.g., "Mobile App", "Third Party Service")
   - **Description**: Optional additional info
   - **Is Active**: Check to enable this key
   - **Key**: Leave blank - auto-generated on save
4. Click **Save**

### Edit API Key
1. Select the key from the list
2. Modify the name, description, or is_active status
3. Click **Save**
- Note: You cannot edit the key value itself for security

### View Usage Metrics
- **Created At**: When the key was created
- **Updated At**: Last modification time
- **Last Used**: Last API call using this key

### Disable API Key
- Uncheck **Is Active** and save
- The key becomes invalid immediately for all future API calls

## Using API Keys in FastAPI Requests

### How to Send API Key
Include the API key in the `X-API-Key` header:

```bash
# Using curl
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/api/protected

# Using Python requests
import requests

headers = {
    "X-API-Key": "your_api_key_here"
}
response = requests.get("http://localhost:8000/api/protected", headers=headers)
print(response.json())

# Using JavaScript fetch
const response = await fetch('http://localhost:8000/api/protected', {
    headers: {
        'X-API-Key': 'your_api_key_here'
    }
});
const data = await response.json();
console.log(data);
```

## API Endpoints

### Protected Endpoints (Require API Key)

#### 1. `/api/protected`
Test endpoint to verify API key validity.

**Request:**
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/api/protected
```

**Response (Success):**
```json
{
    "status": "success",
    "message": "API Key is valid",
    "api_key_name": "Mobile App",
    "api_key_description": "API key for mobile application"
}
```

**Response (Error - Missing Key):**
```json
{
    "detail": "API Key is required. Please provide 'X-API-Key' header."
}
```

**Response (Error - Invalid Key):**
```json
{
    "detail": "Invalid or expired API Key"
}
```

#### 2. `/api/test-key`
Get detailed information about the API key being used.

**Request:**
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/api/test-key
```

**Response:**
```json
{
    "status": "success",
    "api_key": {
        "name": "Mobile App",
        "description": "API key for mobile application",
        "is_active": true,
        "created_at": "2024-03-11T10:30:00",
        "last_used": "2024-03-11T15:45:30"
    }
}
```

#### 3. `/api/users/`
List all users (requires API key).

**Request:**
```bash
curl -H "X-API-Key: your_api_key_here" http://localhost:8000/api/users/
```

**Response:**
```json
{
    "status": "success",
    "message": "Users endpoint",
    "users": [],
    "accessed_with_key": "Mobile App"
}
```

### Public Endpoints (No API Key Required)

#### 1. `/api`
Health check endpoint.

**Response:**
```json
{
    "message": "FastAPI is running on /api",
    "project": "idmitra_django",
    "debug": true
}
```

#### 2. `/health`
Database health check.

**Response:**
```json
{
    "status": "ok",
    "database": "mydb",
    "host": "localhost"
}
```

## Creating Protected Endpoints in Your Code

### Required API Key (with Depends)
```python
from fastapi import APIRouter, Depends
from .auth import verify_api_key
from core.models import APIKey

router = APIRouter(prefix="/api/myroute", tags=["my_route"])

@router.get("/get-data")
def get_data(api_key: APIKey = Depends(verify_api_key)):
    """This endpoint requires a valid API key."""
    return {
        "status": "success",
        "data": "Your data here",
        "accessed_with_key": api_key.name
    }
```

### Optional API Key (get key if provided)
```python
from fastapi import APIRouter, Depends
from .auth import get_optional_api_key
from core.models import APIKey
from typing import Optional

router = APIRouter(prefix="/api/myroute", tags=["my_route"])

@router.get("/public-data")
def get_public_data(api_key: Optional[APIKey] = Depends(get_optional_api_key)):
    """This endpoint works with or without API key."""
    if api_key:
        return {
            "status": "success",
            "data": "Premium data for authenticated users",
            "accessed_with_key": api_key.name
        }
    else:
        return {
            "status": "success",
            "data": "Free data for public access",
            "api_key": None
        }
```

## Error Handling

### Missing API Key
```json
{
    "detail": "API Key is required. Please provide 'X-API-Key' header."
}
```
- Status Code: `403 Forbidden`

### Invalid/Expired API Key
```json
{
    "detail": "Invalid or expired API Key"
}
```
- Status Code: `401 Unauthorized`

## Best Practices

1. **Keep Keys Secret**: Never commit API keys to git
2. **Rotate Keys**: Periodically create new keys and deactivate old ones
3. **Use Descriptions**: Always describe what each key is for
4. **Monitor Usage**: Check "Last Used" timestamps to identify unused keys
5. **Disable Unused Keys**: Deactivate keys that are no longer needed
6. **Environment Variables**: Store API keys in environment variables, not in code

## Files Modified/Created

- `core/models.py` - Added APIKey model
- `core/admin.py` - Registered APIKey in Django Admin
- `core/migrations/0002_apikey.py` - Database migration
- `fastapi_app/auth.py` - Created API key validation utilities
- `fastapi_app/main.py` - Added protected endpoints
- `fastapi_app/routers.py` - Updated example routes with API key requirement

## Troubleshooting

### "API Key is required" error
- Make sure you're sending the `X-API-Key` header correctly
- Check that the header name is exactly `X-API-Key` (case-sensitive)

### "Invalid or expired API Key" error
- Verify the key exists in Django Admin
- Check that the key's "Is Active" checkbox is checked
- Verify you're using the complete key value

### Key not showing up in last_used
- Run migrations: `python manage.py migrate`
- Ensure the SQLAlchemy session is being committed properly

