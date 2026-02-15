from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional
import secrets

from shared.models import Workspace, WorkspaceMembership, AuditLog
from shared.schemas import (
    WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse,
    InviteCreate, MembershipResponse, RoleUpdate
)

def create_workspace(db: Session, workspace: WorkspaceCreate, user_id: UUID) -> Workspace:
    """Create a new workspace and automatically add creator as owner"""
    db_workspace = Workspace(
        name=workspace.name,
        description=workspace.description,
        created_by=user_id,
        settings=workspace.settings or {}
    )
    db.add(db_workspace)
    db.flush()
    
    # Create owner membership
    membership = WorkspaceMembership(
        workspace_id=db_workspace.id,
        user_id=user_id,
        role='owner',
        status='accepted',
        accepted_at=datetime.utcnow()
    )
    db.add(membership)
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_workspace.id,
        user_id=user_id,
        action='workspace.create',
        entity_type='workspace',
        entity_id=db_workspace.id,
        details={'workspace_name': workspace.name}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

def get_user_workspaces(db: Session, user_id: UUID) -> List[Workspace]:
    """Get all workspaces where user is a member"""
    memberships = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.user_id == user_id,
        WorkspaceMembership.status == 'accepted'
    ).all()
    
    workspace_ids = [m.workspace_id for m in memberships]
    return db.query(Workspace).filter(Workspace.id.in_(workspace_ids)).all()

def get_workspace(db: Session, workspace_id: UUID) -> Optional[Workspace]:
    """Get a single workspace by ID"""
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()

def update_workspace(
    db: Session, workspace_id: UUID, workspace_update: WorkspaceUpdate, user_id: UUID
) -> Workspace:
    """Update workspace details"""
    db_workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    
    update_data = workspace_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_workspace, field, value)
    
    db_workspace.updated_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=workspace_id,
        user_id=user_id,
        action='workspace.update',
        entity_type='workspace',
        entity_id=workspace_id,
        metadata=update_data
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

def delete_workspace(db: Session, workspace_id: UUID, user_id: UUID) -> None:
    """Delete a workspace (only owners can do this)"""
    # Add audit log before deletion
    audit = AuditLog(
        workspace_id=workspace_id,
        user_id=user_id,
        action='workspace.delete',
        entity_type='workspace',
        entity_id=workspace_id,
        details={}
    )
    db.add(audit)
    db.commit()
    
    db.query(Workspace).filter(Workspace.id == workspace_id).delete()
    db.commit()

def invite_member(
    db: Session, workspace_id: UUID, invite: InviteCreate, inviter_id: UUID
) -> WorkspaceMembership:
    """Invite a user to the workspace"""
    # Check if already invited or member
    existing = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == workspace_id,
        WorkspaceMembership.invite_email == invite.email.lower()
    ).first()
    
    if existing and existing.status == 'accepted':
        raise ValueError("User is already a member of this workspace")
    
    if existing and existing.status == 'invited':
        raise ValueError("User has already been invited")
    
    # Create invitation
    invite_token = secrets.token_urlsafe(32)
    membership = WorkspaceMembership(
        workspace_id=workspace_id,
        invite_email=invite.email.lower(),
        role=invite.role,
        status='invited',
        invite_token=invite_token,
        invited_by=inviter_id,
        invited_at=datetime.utcnow()
    )
    db.add(membership)
    
    # Add audit log
    audit = AuditLog(
        workspace_id=workspace_id,
        user_id=inviter_id,
        action='membership.invite',
        entity_type='membership',
        entity_id=membership.id,
        details={'email': invite.email, 'role': invite.role}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(membership)
    return membership

def accept_invite(db: Session, invite_token: str, user_id: UUID) -> WorkspaceMembership:
    """Accept a workspace invitation"""
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.invite_token == invite_token,
        WorkspaceMembership.status == 'invited'
    ).first()
    
    if not membership:
        raise ValueError("Invalid or expired invitation")
    
    membership.user_id = user_id
    membership.status = 'accepted'
    membership.accepted_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=membership.workspace_id,
        user_id=user_id,
        action='membership.accept',
        entity_type='membership',
        entity_id=membership.id,
        details={'email': membership.invite_email}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(membership)
    return membership

def get_workspace_members(db: Session, workspace_id: UUID) -> List[WorkspaceMembership]:
    """Get all members of a workspace"""
    return db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == workspace_id
    ).all()

def update_member_role(
    db: Session, membership_id: UUID, role_update: RoleUpdate, updater_id: UUID
) -> WorkspaceMembership:
    """Update a member's role"""
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.id == membership_id
    ).first()
    
    # Check last owner protection
    if membership.role == 'owner' and role_update.role != 'owner':
        owner_count = db.query(WorkspaceMembership).filter(
            WorkspaceMembership.workspace_id == membership.workspace_id,
            WorkspaceMembership.role == 'owner',
            WorkspaceMembership.status == 'accepted'
        ).count()
        
        if owner_count <= 1:
            raise ValueError("Cannot remove or demote the last owner")
    
    old_role = membership.role
    membership.role = role_update.role
    membership.updated_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=membership.workspace_id,
        user_id=updater_id,
        action='membership.role_change',
        entity_type='membership',
        entity_id=membership_id,
        details={'old_role': old_role, 'new_role': role_update.role}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(membership)
    return membership

def remove_member(db: Session, membership_id: UUID, remover_id: UUID) -> None:
    """Remove a member from workspace"""
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.id == membership_id
    ).first()
    
    # Check last owner protection
    if membership.role == 'owner':
        owner_count = db.query(WorkspaceMembership).filter(
            WorkspaceMembership.workspace_id == membership.workspace_id,
            WorkspaceMembership.role == 'owner',
            WorkspaceMembership.status == 'accepted'
        ).count()
        
        if owner_count <= 1:
            raise ValueError("Cannot remove the last owner")
    
    # Add audit log before deletion
    audit = AuditLog(
        workspace_id=membership.workspace_id,
        user_id=remover_id,
        action='membership.remove',
        entity_type='membership',
        entity_id=membership_id,
        details={'user_id': str(membership.user_id), 'role': membership.role}
    )
    db.add(audit)
    db.commit()
    
    db.query(WorkspaceMembership).filter(WorkspaceMembership.id == membership_id).delete()
    db.commit()
