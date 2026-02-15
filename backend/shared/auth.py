from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from supabase import create_client, Client
import os
from typing import Optional
from uuid import UUID

from .database import get_db
from .models import WorkspaceMembership

# Supabase client
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_ANON_KEY", "")
supabase: Client = create_client(supabase_url, supabase_key)

security = HTTPBearer()

class CurrentUser:
    def __init__(self, user_id: UUID, email: str):
        self.user_id = user_id
        self.email = email

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Verify JWT token from Supabase Auth and extract user info
    """
    token = credentials.credentials
    
    try:
        # Verify the JWT with Supabase
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = user_response.user
        return CurrentUser(user_id=UUID(user.id), email=user.email or "")
        
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
