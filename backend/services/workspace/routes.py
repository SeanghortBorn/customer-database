from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from shared.database import get_db
from shared.auth import get_current_user, get_workspace_membership, require_role, CurrentUser
from shared.schemas import (
    WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse,
    InviteCreate, MembershipResponse, RoleUpdate
)
from services.workspace.service import (
    create_workspace, get_user_workspaces, get_workspace, 
    update_workspace, delete_workspace,
    invite_member, accept_invite, get_workspace_members,
    update_member_role, remove_member
)

router = APIRouter()

@router.post("/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace_endpoint(
    workspace: WorkspaceCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new workspace"""
    return create_workspace(db, workspace, current_user.user_id)

@router.get("/workspaces", response_model=List[WorkspaceResponse])
async def list_workspaces(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all workspaces for current user"""
    return get_user_workspaces(db, current_user.user_id)

@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace_endpoint(
    workspace_id: UUID,
    membership = Depends(get_workspace_membership),
    db: Session = Depends(get_db)
):
    """Get a specific workspace"""
    workspace = get_workspace(db, workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.patch("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace_endpoint(
    workspace_id: UUID,
    workspace_update: WorkspaceUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    membership = Depends(require_role(['owner', 'admin'])),
    db: Session = Depends(get_db)
):
    """Update workspace details"""
    return update_workspace(db, workspace_id, workspace_update, current_user.user_id)

@router.delete("/workspaces/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace_endpoint(
    workspace_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    membership = Depends(require_role(['owner'])),
    db: Session = Depends(get_db)
):
    """Delete a workspace"""
    delete_workspace(db, workspace_id, current_user.user_id)
    return None

@router.post("/workspaces/{workspace_id}/invite", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
async def invite_member_endpoint(
    workspace_id: UUID,
    invite: InviteCreate,
    current_user: CurrentUser = Depends(get_current_user),
    membership = Depends(require_role(['owner', 'admin'])),
    db: Session = Depends(get_db)
):
    """Invite a user to the workspace"""
    try:
        return invite_member(db, workspace_id, invite, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/invites/{invite_token}/accept", response_model=MembershipResponse)
async def accept_invite_endpoint(
    invite_token: str,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a workspace invitation"""
    try:
        return accept_invite(db, invite_token, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/workspaces/{workspace_id}/members", response_model=List[MembershipResponse])
async def list_members(
    workspace_id: UUID,
    membership = Depends(get_workspace_membership),
    db: Session = Depends(get_db)
):
    """Get all members of a workspace"""
    return get_workspace_members(db, workspace_id)

@router.patch("/workspaces/{workspace_id}/members/{membership_id}/role", response_model=MembershipResponse)
async def update_role_endpoint(
    workspace_id: UUID,
    membership_id: UUID,
    role_update: RoleUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    membership = Depends(require_role(['owner', 'admin'])),
    db: Session = Depends(get_db)
):
    """Update a member's role"""
    try:
        return update_member_role(db, membership_id, role_update, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.delete("/workspaces/{workspace_id}/members/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member_endpoint(
    workspace_id: UUID,
    membership_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    membership = Depends(require_role(['owner', 'admin'])),
    db: Session = Depends(get_db)
):
    """Remove a member from workspace"""
    try:
        remove_member(db, membership_id, current_user.user_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
