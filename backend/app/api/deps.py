from typing import Generator, Callable, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.db.session import get_db
from app.db import models
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_org_id(current_user: models.User = Depends(get_current_user)):
    return current_user.org_id


# Set session variable for RLS (must be used as a dependency on endpoints)
def set_db_org(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # set per-session variable so Postgres RLS policies can use current_setting('zoneer.org')
    try:
        if current_user and current_user.org_id:
            db.execute("SELECT set_config('zoneer.org', :org, true)", {"org": str(current_user.org_id)})
    except Exception:
        # ignore for sqlite/dev environment
        pass
    return None


# simple role guard generator
def require_role(*allowed_roles: str) -> Callable[..., Any]:
    def _require(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return current_user
    return _require
