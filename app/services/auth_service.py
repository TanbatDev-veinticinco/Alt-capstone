from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User, UserRole
from app.repositories import user_repository
from app.schemas.user import TokenData


bearer_scheme = HTTPBearer(auto_error=False)


def get_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    if credentials:
        return credentials.credentials

    token = request.cookies.get("access_token")

    if token:
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def get_current_user(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = user_repository.get_user_by_email(db, token_data.email)

    if user is None:
        raise credentials_exception

    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )

    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required"
        )

    return current_user


def require_student(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != UserRole.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can perform this action"
        )

    return current_user
