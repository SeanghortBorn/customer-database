from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session, joinedload

from app import schemas, db
from app.db import models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.PropertyOut])
def list_properties(skip: int = 0, limit: int = 50, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    return db.query(models.Property).options(joinedload(models.Property.owner)).filter(models.Property.org_id == org_id).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.PropertyOut)
def create_property(payload: schemas.PropertyCreate, request: Request, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    prop = models.Property(**payload.dict(), org_id=org_id, created_by=current_user.id)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    # reload with owner relationship for proper response serialization
    db.expire(prop)
    prop = db.query(models.Property).options(joinedload(models.Property.owner)).filter(models.Property.id == prop.id).first()
    # broadcast event
    try:
        request.app.state.broadcast('property.created', {"id": str(prop.id), "name": prop.name})
    except Exception:
        pass
    return prop


@router.get("/{property_id}", response_model=schemas.PropertyOut)
def get_property(property_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    prop = db.query(models.Property).options(joinedload(models.Property.owner)).filter(models.Property.id == property_id, models.Property.org_id == org_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


@router.patch("/{property_id}", response_model=schemas.PropertyOut)
def update_property(property_id: str, payload: schemas.PropertyCreate, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    prop = db.query(models.Property).filter(models.Property.id == property_id, models.Property.org_id == org_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(prop, k, v)
    db.add(prop)
    db.commit()
    db.refresh(prop)
    # Eager load owner relationship for response
    db.expire(prop)
    prop = db.query(models.Property).options(joinedload(models.Property.owner)).filter(models.Property.id == property_id).first()
    return prop


@router.delete("/{property_id}")
def delete_property(property_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    prop = db.query(models.Property).filter(models.Property.id == property_id, models.Property.org_id == org_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    db.delete(prop)
    db.commit()
    return {"ok": True}
