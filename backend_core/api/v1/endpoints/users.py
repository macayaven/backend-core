"""User endpoints."""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend_core.core.deps import get_current_user
from backend_core.core.security import get_password_hash
from backend_core.db.session import get_db
from backend_core.models.user import User
from backend_core.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> User:
    """Create new user."""
    # Check if user exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    now = datetime.now(timezone.utc)
    user = User()
    user.email = user_in.email
    user.hashed_password = get_password_hash(user_in.password)
    user.first_name = user_in.first_name
    user.last_name = user_in.last_name
    user.created_at = now
    user.updated_at = now

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UserRead)
def read_user_me(current_user: User = Depends(get_current_user)) -> User:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Update current user."""
    if user_in.password is not None:
        current_user.hashed_password = get_password_hash(user_in.password)
    if user_in.email is not None:
        current_user.email = user_in.email
    if user_in.first_name is not None:
        current_user.first_name = user_in.first_name
    if user_in.last_name is not None:
        current_user.last_name = user_in.last_name

    current_user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(current_user)
    return current_user
