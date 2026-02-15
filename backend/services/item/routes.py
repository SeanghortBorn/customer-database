from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from ..shared.database import get_db
from ..shared.auth import get_current_user, CurrentUser
from ..shared.models import WorkspaceMembership, List as ListModel
from ..shared.schemas import (
    ItemCreate, ItemUpdate, ItemResponse,
    CommentCreate, CommentResponse
)
from .service import (
    create_item, get_list_items, get_item, update_item, archive_item,
    create_comment, get_item_comments, delete_comment
)

router = APIRouter()

# Item endpoints
@router.post("/lists/{list_id}/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item_endpoint(
    list_id: UUID,
    item_data: ItemCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new item"""
    # Verify user has access
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")
    
    membership = db.query(WorkspaceMembership).filter(
        WorkspaceMembership.workspace_id == db_list.workspace_id,
        WorkspaceMembership.user_id == current_user.user_id,
        WorkspaceMembership.status == 'accepted'
    ).first()
    
    if not membership:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return create_item(db, list_id, item_data, current_user.user_id)

@router.get("/lists/{list_id}/items", response_model=List[ItemResponse])
async def list_items(
    list_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all items in a list"""
    return get_list_items(db, list_id, limit, offset)

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item_endpoint(
    item_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific item"""
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return db_item

@router.patch("/items/{item_id}", response_model=ItemResponse)
async def update_item_endpoint(
    item_id: UUID,
    item_update: ItemUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update item details"""
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return update_item(db, item_id, item_update, current_user.user_id)

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_item_endpoint(
    item_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Archive an item"""
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    archive_item(db, item_id, current_user.user_id)
    return None

# Comment endpoints
@router.post("/items/{item_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment_endpoint(
    item_id: UUID,
    comment_data: CommentCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a comment on an item"""
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return create_comment(db, item_id, comment_data, current_user.user_id)

@router.get("/items/{item_id}/comments", response_model=List[CommentResponse])
async def list_comments(
    item_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all comments for an item"""
    return get_item_comments(db, item_id)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_endpoint(
    comment_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a comment"""
    # TODO: Verify user owns the comment or is admin
    delete_comment(db, comment_id, current_user.user_id)
    return None
