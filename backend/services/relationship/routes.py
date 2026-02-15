from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from shared.database import get_db
from shared.auth import get_current_user, CurrentUser
from shared.schemas import (
    RelationshipCreate, RelationshipResponse,
    RelationshipLinkCreate, RelationshipLinkResponse
)
from services.relationship.service import (
    create_relationship, get_list_relationships, get_relationship, delete_relationship,
    create_link, get_relationship_links, delete_link
)

router = APIRouter()

# Relationship endpoints
@router.post("/lists/{list_id}/relationships", response_model=RelationshipResponse, status_code=status.HTTP_201_CREATED)
async def create_relationship_endpoint(
    list_id: UUID,
    relationship_data: RelationshipCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new relationship"""
    return create_relationship(db, list_id, relationship_data, current_user.user_id)

@router.get("/lists/{list_id}/relationships", response_model=List[RelationshipResponse])
async def list_relationships(
    list_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all relationships for a list"""
    return get_list_relationships(db, list_id)

@router.delete("/relationships/{relationship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_relationship_endpoint(
    relationship_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a relationship"""
    db_relationship = get_relationship(db, relationship_id)
    if not db_relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    delete_relationship(db, relationship_id, current_user.user_id)
    return None

# Relationship link endpoints
@router.post("/relationships/{relationship_id}/links", response_model=RelationshipLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link_endpoint(
    relationship_id: UUID,
    link_data: RelationshipLinkCreate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new link between items"""
    try:
        return create_link(db, relationship_id, link_data, current_user.user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/relationships/{relationship_id}/links", response_model=List[RelationshipLinkResponse])
async def list_links(
    relationship_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all links for a relationship"""
    return get_relationship_links(db, relationship_id)

@router.delete("/links/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link_endpoint(
    link_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a relationship link"""
    delete_link(db, link_id, current_user.user_id)
    return None
