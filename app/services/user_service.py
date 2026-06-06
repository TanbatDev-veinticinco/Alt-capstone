from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import user_repository
from app.schemas.user import UserCreate, UserLogin
from app.services.auth_service import create_access_token
from app.models.user import User


def register_user(db: Session, user_data: UserCreate) -> User:
    existing_user = user_repository.get_user_by_email(db, user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    return user_repository.create_user(db, user_data)


def login_user(db: Session, login_data: UserLogin) -> dict:
    user = user_repository.get_user_by_email(db, login_data.email)

    if not user or not user_repository.verify_password(
        login_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is deactivated"
        )

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }