from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from typing import Optional
from uuid import UUID

from .database import get_db
from .models import WorkspaceMembership, User
from .jwt_auth import decode_access_token

security = HTTPBearer()

class CurrentUser:
    def __init__(self, user_id: UUID, email: str):
        self.user_id = user_id
        self.email = email

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> CurrentUser:
    """
    Verify JWT token and extract user info
    """
    token = credentials.credentials
    
    try:
        # Decode and verify JWT token
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        if not user_id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user exists and is active
        user = db.query(User).filter(User.id == UUID(user_id), User.is_active == True).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return CurrentUser(user_id=UUID(user_id), email=email)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_workspace_membership(
    workspace_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> WorkspaceMembership:
    """
    Get the user's membership in a workspace
    """
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this workspace"
        )
    
    return membership

def require_role(allowed_roles: list[str]):
    """
    Dependency factory to require specific roles
    Usage: Depends(require_role(['owner', 'admin']))
    """
    async def role_checker(
        workspace_id: UUID,
        membership: WorkspaceMembership = Depends(get_workspace_membership)
    ):
        if membership.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {', '.join(allowed_roles)}"
            )
        return membership
    
    return role_checker
