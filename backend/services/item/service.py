from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from shared.models import Item, AuditLog, List as ListModel, Comment
from shared.schemas import (
    ItemCreate, ItemUpdate, ItemResponse,
    CommentCreate, CommentResponse
)

# Item operations
def create_item(db: Session, list_id: UUID, item_data: ItemCreate, user_id: UUID) -> Item:
    """Create a new item in a list"""
    # Get the list to find workspace_id for audit
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    
    db_item = Item(
        list_id=list_id,
        title=item_data.title,
        values=item_data.values or {},
        created_by=user_id,
        updated_by=user_id
    )
    db.add(db_item)
    db.flush()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='item.create',
        entity_type='item',
        entity_id=db_item.id,
        details={'list_id': str(list_id), 'title': item_data.title}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def get_list_items(
    db: Session, 
    list_id: UUID, 
    limit: int = 100, 
    offset: int = 0
) -> List[Item]:
    """Get all items in a list with pagination"""
    return db.query(Item).filter(
        Item.list_id == list_id,
        Item.archived_at.is_(None)
    ).order_by(Item.position, Item.created_at).limit(limit).offset(offset).all()

def get_item(db: Session, item_id: UUID) -> Optional[Item]:
    """Get a specific item"""
    return db.query(Item).filter(Item.id == item_id).first()

def update_item(db: Session, item_id: UUID, item_update: ItemUpdate, user_id: UUID) -> Item:
    """Update item details"""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_item.list_id).first()
    
    update_data = item_update.model_dump(exclude_unset=True)
    
    # Handle values update - merge with existing values
    if 'values' in update_data and update_data['values'] is not None:
        existing_values = db_item.values or {}
        existing_values.update(update_data['values'])
        db_item.values = existing_values
        del update_data['values']
    
    # Update other fields
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db_item.updated_by = user_id
    db_item.updated_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='item.update',
        entity_type='item',
        entity_id=item_id,
        metadata=item_update.model_dump(exclude_unset=True)
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_item)
    return db_item

def archive_item(db: Session, item_id: UUID, user_id: UUID) -> Item:
    """Archive an item (soft delete)"""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_item.list_id).first()
    
    db_item.archived_at = datetime.utcnow()
    db_item.updated_at = datetime.utcnow()
    db_item.updated_by = user_id
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='item.delete',
        entity_type='item',
        entity_id=item_id,
        details={'title': db_item.title}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_item)
    return db_item

# Comment operations
def create_comment(db: Session, item_id: UUID, comment_data: CommentCreate, user_id: UUID) -> Comment:
    """Create a comment on an item"""
    db_item = db.query(Item).filter(Item.id == item_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_item.list_id).first()
    
    db_comment = Comment(
        item_id=item_id,
        user_id=user_id,
        content=comment_data.content
    )
    db.add(db_comment)
    db.flush()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='comment.create',
        entity_type='comment',
        entity_id=db_comment.id,
        details={'item_id': str(item_id)}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_item_comments(db: Session, item_id: UUID) -> List[Comment]:
    """Get all comments for an item"""
    return db.query(Comment).filter(
        Comment.item_id == item_id
    ).order_by(Comment.created_at.desc()).all()

def delete_comment(db: Session, comment_id: UUID, user_id: UUID) -> None:
    """Delete a comment"""
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    db_item = db.query(Item).filter(Item.id == db_comment.item_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_item.list_id).first()
    
    # Add audit log before deletion
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='comment.delete',
        entity_type='comment',
        entity_id=comment_id,
        details={'item_id': str(db_comment.item_id)}
    )
    db.add(audit)
    db.commit()
    
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
