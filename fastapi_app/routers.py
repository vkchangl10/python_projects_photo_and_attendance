"""Example router for FastAPI using Django ORM models with async support."""
from fastapi import APIRouter, Depends
from asgiref.sync import sync_to_async

from .auth import verify_api_key, get_optional_api_key
from .models import APIKey, User

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@sync_to_async
def _get_all_users():
    """Internal function to query all users from database."""
    return list(User.objects.all().values('id', 'username', 'email', 'first_name', 'last_name'))


@router.get("/")
async def list_users(api_key: APIKey = Depends(verify_api_key)):
    """
    List all users asynchronously.
    Requires a valid API key in the 'X-API-Key' header.
    """
    # Query all users using Django ORM asynchronously
    users = await _get_all_users()
    
    return {
        "status": "success",
        "message": "Users endpoint",
        "count": len(users),
        "users": users,
        "accessed_with_key": api_key.name
    }


@sync_to_async
def _get_user_by_id(user_id: int):
    """Internal function to query a specific user from database."""
    try:
        user = User.objects.get(id=user_id)
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_active': user.is_active,
            'created_at': user.date_joined.isoformat() if hasattr(user, 'date_joined') else None,
        }
    except User.DoesNotExist:
        return None


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    api_key: APIKey = Depends(verify_api_key)
):
    """
    Get a specific user asynchronously.
    Requires a valid API key in the 'X-API-Key' header.
    """
    # Query specific user using Django ORM asynchronously
    user_data = await _get_user_by_id(user_id)
    
    if user_data:
        return {
            "status": "success",
            "user_id": user_id,
            "message": "User details",
            "user": user_data,
            "accessed_with_key": api_key.name
        }
    else:
        return {
            "status": "error",
            "message": f"User with id {user_id} not found",
            "user_id": user_id
        }

