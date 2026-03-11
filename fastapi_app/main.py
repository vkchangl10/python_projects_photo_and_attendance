"""FastAPI application entry point with async endpoints."""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .auth import verify_api_key, get_optional_api_key
from .models import APIKey
from .routers import router

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
async def read_root():
    """Health check endpoint."""
    return {
        "message": "FastAPI is running on /api",
        "project": settings.PROJECT_NAME,
        "debug": settings.DEBUG,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "database": settings.DB_NAME,
        "host": settings.DB_HOST,
    }


@app.get("/protected")
async def protected_endpoint(api_key: APIKey = Depends(verify_api_key)):
    """
    Example of a protected endpoint that requires a valid API key.
    
    Pass your API key in the 'X-API-Key' header:
    curl -H "X-API-Key: your_api_key_here" http://localhost:8000/api/protected
    """
    return {
        "status": "success",
        "message": "API Key is valid",
        "api_key_name": api_key.name,
        "api_key_description": api_key.description
    }


@app.get("/test-key")
async def test_key_endpoint(api_key: APIKey = Depends(verify_api_key)):
    """
    Test endpoint to verify API key and get key details.
    """
    return {
        "status": "success",
        "api_key": {
            "name": api_key.name,
            "description": api_key.description,
            "is_active": api_key.is_active,
            "created_at": api_key.created_at.isoformat() if api_key.created_at else None,
            "last_used": api_key.last_used.isoformat() if api_key.last_used else None
        }
    }




