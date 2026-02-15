from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List, Optional

from shared.models import Relationship, RelationshipLink, AuditLog, List as ListModel
from shared.schemas import (
    RelationshipCreate, RelationshipResponse,
    RelationshipLinkCreate, RelationshipLinkResponse
)

# Relationship operations
def create_relationship(
    db: Session, list_id: UUID, relationship_data: RelationshipCreate, user_id: UUID
) -> Relationship:
    """Create a new relationship between lists"""
    # Get the list to find workspace_id for audit
    db_list = db.query(ListModel).filter(ListModel.id == list_id).first()
    
    db_relationship = Relationship(
        list_id=list_id,
        name=relationship_data.name,
        target_list_id=relationship_data.target_list_id,
        relationship_type=relationship_data.relationship_type
    )
    db.add(db_relationship)
    db.flush()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='relationship.create',
        entity_type='relationship',
        entity_id=db_relationship.id,
        details={
            'name': relationship_data.name,
            'target_list_id': str(relationship_data.target_list_id),
            'type': relationship_data.relationship_type
        }
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_relationship)
    return db_relationship

def get_list_relationships(db: Session, list_id: UUID) -> List[Relationship]:
    """Get all relationships for a list"""
    return db.query(Relationship).filter(
        Relationship.list_id == list_id
    ).all()

def get_relationship(db: Session, relationship_id: UUID) -> Optional[Relationship]:
    """Get a specific relationship"""
    return db.query(Relationship).filter(Relationship.id == relationship_id).first()

def delete_relationship(db: Session, relationship_id: UUID, user_id: UUID) -> None:
    """Delete a relationship"""
    db_relationship = db.query(Relationship).filter(Relationship.id == relationship_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_relationship.list_id).first()
    
    # Add audit log before deletion
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='relationship.delete',
        entity_type='relationship',
        entity_id=relationship_id,
        details={'name': db_relationship.name}
    )
    db.add(audit)
    db.commit()
    
    db.query(Relationship).filter(Relationship.id == relationship_id).delete()
    db.commit()

# Relationship link operations
def create_link(
    db: Session, relationship_id: UUID, link_data: RelationshipLinkCreate, user_id: UUID
) -> RelationshipLink:
    """Create a link between two items"""
    db_relationship = db.query(Relationship).filter(Relationship.id == relationship_id).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_relationship.list_id).first()
    
    # Check if link already exists
    existing = db.query(RelationshipLink).filter(
        RelationshipLink.relationship_id == relationship_id,
        RelationshipLink.source_item_id == link_data.source_item_id,
        RelationshipLink.target_item_id == link_data.target_item_id
    ).first()
    
    if existing:
        raise ValueError("Link already exists")
    
    db_link = RelationshipLink(
        relationship_id=relationship_id,
        source_item_id=link_data.source_item_id,
        target_item_id=link_data.target_item_id
    )
    db.add(db_link)
    db.flush()
    
    # Add audit log
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='relationship.link',
        entity_type='relationship_link',
        entity_id=db_link.id,
        details={
            'relationship_id': str(relationship_id),
            'source_item_id': str(link_data.source_item_id),
            'target_item_id': str(link_data.target_item_id)
        }
    )
    db.add(audit)
    
    db.commit()
    db.refresh(db_link)
    return db_link

def get_relationship_links(db: Session, relationship_id: UUID) -> List[RelationshipLink]:
    """Get all links for a relationship"""
    return db.query(RelationshipLink).filter(
        RelationshipLink.relationship_id == relationship_id
    ).all()

def delete_link(db: Session, link_id: UUID, user_id: UUID) -> None:
    """Delete a relationship link"""
    db_link = db.query(RelationshipLink).filter(RelationshipLink.id == link_id).first()
    db_relationship = db.query(Relationship).filter(
        Relationship.id == db_link.relationship_id
    ).first()
    db_list = db.query(ListModel).filter(ListModel.id == db_relationship.list_id).first()
    
    # Add audit log before deletion
    audit = AuditLog(
        workspace_id=db_list.workspace_id,
        user_id=user_id,
        action='relationship.unlink',
        entity_type='relationship_link',
        entity_id=link_id,
        details={
            'relationship_id': str(db_link.relationship_id),
            'source_item_id': str(db_link.source_item_id),
            'target_item_id': str(db_link.target_item_id)
        }
    )
    db.add(audit)
    db.commit()
    
    db.query(RelationshipLink).filter(RelationshipLink.id == link_id).delete()
    db.commit()
