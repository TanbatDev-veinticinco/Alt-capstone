from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import user_service
from app.services.auth_service import get_current_active_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user_data)


@router.post("/login")
def login(
    login_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    token_data = user_service.login_user(db, login_data)

    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 30,
    )

    return {
        "message": "Login successful",
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"]
    }


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    return current_user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")

    return {"message": "Logged out successfully"}
