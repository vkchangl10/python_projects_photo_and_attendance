"""Example router for FastAPI."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@router.get("/")
def list_users(db: Session = Depends(get_db)):
    """List all users."""
    # Example: users = db.query(User).all()
    return {"message": "Users endpoint", "users": []}


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user."""
    # Example: user = db.query(User).filter(User.id == user_id).first()
    return {"user_id": user_id, "message": "User details"}
