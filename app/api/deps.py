from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.http import HTTPKey2FA
from app.db.session import SessionLocal

auth_scheme = HTTPBearer()
auth_scheme_2fa = HTTPKey2FA(name="X-Auth-Token-2fa")
api_key_header = APIKeyHeader(name="X-Api-Key", auto_error=False)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
) -> models.Admin:
    try:
        payload = jwt.decode(
            token.credentials,
            settings.secret_key,
            algorithms=[security.ALGORITHM],
        )
        token_data = schemas.AuthTokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    admin = crud.admin.get(db, id=token_data.sub)
    if not admin:
        raise HTTPException(status_code=404, detail="User not found")
    return admin


def get_current_user_2fa(
    current_user: models.Admin = Depends(get_current_user),
    auth_key: str = Depends(auth_scheme_2fa),
) -> models.Admin:
    if not crud.admin.totp_verify(current_user, auth_key):
        raise HTTPException(
            status_code=403,
            detail="Invalid authentication credentials",
        )
    return current_user


def get_api_key(api_key_header: str = Depends(api_key_header)):
    """Retrieve & validate an API key from HTTP header"""
    if api_key_header == settings.api_key:
        return api_key_header

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
