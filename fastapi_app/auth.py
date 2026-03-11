"""API Key authentication utilities for FastAPI using Django ORM with async support."""
from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from django.utils import timezone
from asgiref.sync import sync_to_async

from .models import APIKey

# Create an APIKeyHeader security scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@sync_to_async
def _verify_api_key_db(api_key: str) -> APIKey:
    """Internal function to query and update API key in database."""
    try:
        db_api_key = APIKey.objects.get(key=api_key, is_active=True)
        # Update last_used timestamp
        db_api_key.last_used = timezone.now()
        db_api_key.save(update_fields=['last_used'])
        return db_api_key
    except APIKey.DoesNotExist:
        return None


async def verify_api_key(api_key: str = Depends(api_key_header)) -> APIKey:
    """
    Verify if the provided API key is valid and active.
    FastAPI dependency for required API key (asynchronous).
    
    Args:
        api_key: The API key from the request header
        
    Returns:
        APIKey object if valid
        
    Raises:
        HTTPException: If API key is missing, invalid, or inactive
    """
    # Get API key from header
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key is required. Please provide 'X-API-Key' header."
        )
    
    # Query Django ORM for the API key asynchronously
    db_api_key = await _verify_api_key_db(api_key)
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API Key"
        )
    
    return db_api_key


@sync_to_async
def _get_optional_api_key_db(api_key: str) -> APIKey | None:
    """Internal function to query optional API key from database."""
    try:
        db_api_key = APIKey.objects.get(key=api_key, is_active=True)
        # Update last_used timestamp
        db_api_key.last_used = timezone.now()
        db_api_key.save(update_fields=['last_used'])
        return db_api_key
    except APIKey.DoesNotExist:
        return None


async def get_optional_api_key(api_key: str = Depends(api_key_header)) -> APIKey | None:
    """
    Get API key if provided, but don't require it.
    FastAPI dependency for optional API key (asynchronous).
    
    Returns:
        APIKey object if valid key is provided, None otherwise
    """
    if not api_key:
        return None
    
    return await _get_optional_api_key_db(api_key)


