from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from shared.database import get_db
from shared.auth import get_current_user, get_workspace_membership, CurrentUser
from shared.models import AuditLog
from shared.schemas import AuditLogResponse

router = APIRouter()

@router.get("/workspaces/{workspace_id}/audit", response_model=List[AuditLogResponse])
async def get_audit_logs(
    workspace_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    membership = Depends(get_workspace_membership),
    db: Session = Depends(get_db)
):
    """Get audit logs for a workspace"""
    logs = db.query(AuditLog).filter(
        AuditLog.workspace_id == workspace_id
    ).order_by(AuditLog.created_at.desc()).limit(limit).offset(offset).all()
    
    return logs
