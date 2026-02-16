from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from shared.database import get_db
from shared.auth import get_current_user, get_workspace_membership, require_role, CurrentUser
from shared.models import WorkspaceMembership
from shared.schemas import (
    ListCreate, ListUpdate, ListResponse,
    ColumnCreate, ColumnUpdate, ColumnResponse
)
from services.list.service import (
    create_list, get_workspace_lists, get_list, update_list, archive_list,
    create_column, get_list_columns, get_column, update_column, delete_column
)

router = APIRouter()

# List endpoints
@router.post("/workspaces/{workspace_id}/lists", response_model=ListResponse, status_code=status.HTTP_201_CREATED)
async def create_list_endpoint(
    workspace_id: UUID,
    list_data: ListCreate,
    current_user: CurrentUser = Depends(get_current_user),
    membership = Depends(require_role(['owner', 'admin', 'editor'])),
    db: Session = Depends(get_db)
):
    """Create a new list"""
    return create_list(db, workspace_id, list_data, current_user.user_id)

@router.get("/workspaces/{workspace_id}/lists", response_model=List[ListResponse])
async def list_lists(
    workspace_id: UUID,
    membership = Depends(get_workspace_membership),
    db: Session = Depends(get_db)
):
    """Get all lists in a workspace"""
    return get_workspace_lists(db, workspace_id)

@router.get("/lists/{list_id}", response_model=ListResponse)
async def get_list_endpoint(
    list_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific list"""
    db_list = get_list(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    
    # Verify user has access to this workspace
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return db_list

@router.patch("/lists/{list_id}", response_model=ListResponse)
async def update_list_endpoint(
    list_id: UUID,
    list_update: ListUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update list details"""
    db_list = get_list(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    
    # Verify user has editor+ role
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin', 'editor']:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return update_list(db, list_id, list_update, current_user.user_id)

@router.delete("/lists/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_list_endpoint(
    list_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Archive a list"""
    db_list = get_list(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    
    # Verify user has editor+ role
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin', 'editor']:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    archive_list(db, list_id, current_user.user_id)
    return None

# Column endpoints
@router.post("/lists/{list_id}/columns", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
async def create_column_endpoint(
    list_id: UUID,
    column_data: ColumnCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new column"""
    db_list = get_list(db, list_id)
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    
    # Verify user has editor+ role
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin', 'editor']:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return create_column(db, list_id, column_data, current_user.user_id)

@router.get("/lists/{list_id}/columns", response_model=List[ColumnResponse])
async def list_columns(
    list_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all columns for a list"""
    return get_list_columns(db, list_id)

@router.patch("/columns/{column_id}", response_model=ColumnResponse)
async def update_column_endpoint(
    column_id: UUID,
    column_update: ColumnUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update column details"""
    db_column = get_column(db, column_id)
    if not db_column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    # Verify user has editor+ role
    from shared.models import List as ListModel
    db_list = db.query(ListModel).filter(ListModel.id == db_column.list_id).first()
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin', 'editor']:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return update_column(db, column_id, column_update, current_user.user_id)

@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_column_endpoint(
    column_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a column"""
    db_column = get_column(db, column_id)
    if not db_column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    # Verify user has editor+ role
    from shared.models import List as ListModel
    db_list = db.query(ListModel).filter(ListModel.id == db_column.list_id).first()
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership or membership.role not in ['owner', 'admin', 'editor']:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    delete_column(db, column_id, current_user.user_id)
    return None
