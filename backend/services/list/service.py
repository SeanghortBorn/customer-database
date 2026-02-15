from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from ..shared.models import List as ListModel, Column_, Item, AuditLog
from ..shared.schemas import (
    ListCreate, ListUpdate, ListResponse,
    ColumnCreate, ColumnUpdate, ColumnResponse
)

# List operations
def create_list(db: Session, workspace_id: UUID, list_data: ListCreate, user_id: UUID) -> ListModel:
    """Create a new list in a workspace"""
    db_list = ListModel(
        workspace_id=workspace_id,
        name=list_data.name,
        description=list_data.description,
        created_by=user_id
    )
    db.add(db_list)
    db.flush()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=workspace_id,
        user_id=user_id,
        action='list.create',
        entity_type='list',
        entity_id=db_list.id,
        metadata={'list_name': list_data.name}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_list)
    return db_list

def get_workspace_lists(db: Session, workspace_id: UUID) -> List[ListModel]:
    """Get all lists in a workspace"""
    return db.query(ListModel).filter(
        ListModel.workspace_id == workspace_id,
        ListModel.archived_at.is_(None)
    ).order_by(ListModel.position, ListModel.created_at).all()

def get_list(db: Session, list_id: UUID) -> Optional[ListModel]:
    """Get a specific list"""
    return db.query(ListModel).filter(ListModel.id == list_id).first()

def update_list(db: Session, list_id: UUID, list_update: ListUpdate, user_id: UUID) -> ListModel:
    """Update list details"""
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    
    update_data = list_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_list, field, value)
    
    db_list.updated_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='list.update',
        entity_type='list',
        entity_id=list_id,
        metadata=update_data
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_list)
    return db_list

def archive_list(db: Session, list_id: UUID, user_id: UUID) -> ListModel:
    """Archive a list (soft delete)"""
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    db_list.archived_at = datetime.utcnow()
    db_list.updated_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='list.delete',
        entity_type='list',
        entity_id=list_id,
        metadata={'list_name': db_list.name}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_list)
    return db_list

# Column operations
def create_column(db: Session, list_id: UUID, column_data: ColumnCreate, user_id: UUID) -> Column_:
    """Create a new column in a list"""
    # Get the list to find workspace_id for audit
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    
    db_column = Column_(
        list_id=list_id,
        key=column_data.key,
        name=column_data.name,
        type=column_data.type,
        position=column_data.position,
        is_required=column_data.is_required,
        is_unique=column_data.is_unique,
        config=column_data.config or {}
    )
    db.add(db_column)
    db.flush()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='column.create',
        entity_type='column',
        entity_id=db_column.id,
        metadata={'list_id': str(list_id), 'column_name': column_data.name, 'column_type': column_data.type}
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_column)
    return db_column

def get_list_columns(db: Session, list_id: UUID) -> List[Column_]:
    """Get all columns for a list"""
    return db.query(Column_).filter(
        Column_.list_id == list_id
    ).order_by(Column_.position, Column_.created_at).all()

def get_column(db: Session, column_id: UUID) -> Optional[Column_]:
    """Get a specific column"""
    return db.query(Column_).filter(Column_.id == column_id).first()

def update_column(db: Session, column_id: UUID, column_update: ColumnUpdate, user_id: UUID) -> Column_:
    """Update column details"""
    db_column = db.query(Column_).filter(Column_.id == column_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_column.list_id).first()
    
    update_data = column_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_column, field, value)
    
    db_column.updated_at = datetime.utcnow()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='column.update',
        entity_type='column',
        entity_id=column_id,
        metadata=update_data
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_column)
    return db_column

def delete_column(db: Session, column_id: UUID, user_id: UUID) -> None:
    """Delete a column"""
    db_column = db.query(Column_).filter(Column_.id == column_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_column.list_id).first()
    
    # Add audit log before deletion
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='column.delete',
        entity_type='column',
        entity_id=column_id,
        metadata={'column_name': db_column.name}
    )
    db.add(audit)
    db.commit()
    
    db.query(Column_).filter(Column_.id == column_id).delete()
    db.commit()
