from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import schemas, db
from app.db import models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UnitOut])
def list_units(property_id: str = None, skip: int = 0, limit: int = 50, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    q = db.query(models.Unit).join(models.Property).filter(models.Property.org_id == org_id)
    if property_id:
        q = q.filter(models.Unit.property_id == property_id)
    return q.offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.UnitOut)
def create_unit(payload: schemas.UnitCreate, request: Request, property_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    prop = db.query(models.Property).filter(models.Property.id == property_id, models.Property.org_id == org_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    unit = models.Unit(**payload.dict(), property_id=property_id)
    db.add(unit)
    prop.unit_count = len(prop.units) + 1
    db.add(prop)
    db.commit()
    db.refresh(unit)
    # broadcast event
    try:
        request.app.state.broadcast('unit.created', {"id": str(unit.id), "unit_no": unit.unit_no, "property_id": str(property_id)})
    except Exception:
        pass
    return unit


@router.get("/{unit_id}", response_model=schemas.UnitOut)
def get_unit(unit_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    unit = db.query(models.Unit).join(models.Property).filter(models.Unit.id == unit_id, models.Property.org_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.patch("/{unit_id}", response_model=schemas.UnitOut)
def update_unit(unit_id: str, payload: schemas.UnitCreate, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    unit = db.query(models.Unit).join(models.Property).filter(models.Unit.id == unit_id, models.Property.org_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(unit, k, v)
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


@router.delete("/{unit_id}")
def delete_unit(unit_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    unit = db.query(models.Unit).join(models.Property).filter(models.Unit.id == unit_id, models.Property.org_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    prop = unit.property
    db.delete(unit)
    prop.unit_count = max(0, prop.unit_count - 1)
    db.add(prop)
    db.commit()
    return {"ok": True}

@router.get("/{unit_id}/history")
def list_unit_history(unit_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    # ensure unit belongs to org
    unit = db.query(models.Unit).join(models.Property).filter(models.Unit.id == unit_id, models.Property.org_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return db.query(models.UnitPriceHistory).filter(models.UnitPriceHistory.unit_id == unit_id).order_by(models.UnitPriceHistory.effective_date.desc()).all()


@router.post("/{unit_id}/history")
def create_unit_history(unit_id: str, price: float, currency: str = 'USD', effective_date: str | None = None, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    unit = db.query(models.Unit).join(models.Property).filter(models.Unit.id == unit_id, models.Property.org_id == org_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    from datetime import datetime
    eff = datetime.fromisoformat(effective_date) if effective_date else None
    hist = models.UnitPriceHistory(unit_id=unit_id, price=price, currency=currency, effective_date=eff, created_by=current_user.id)
    db.add(hist)
    db.commit()
    db.refresh(hist)
    return hist
