from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import schemas, db
from app.db import models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.PersonOut])
def list_people(skip: int = 0, limit: int = 50, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    return db.query(models.Person).filter(models.Person.org_id == org_id).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.PersonOut)
def create_person(payload: schemas.PersonCreate, request: Request, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    person = models.Person(**payload.dict(), org_id=org_id, created_by=current_user.id)
    db.add(person)
    db.commit()
    db.refresh(person)
    # broadcast real-time event (MVP)
    try:
        request.app.state.broadcast('person.created', {"id": str(person.id), "first_name": person.first_name, "last_name": person.last_name})
    except Exception:
        pass
    return person


@router.get("/{person_id}", response_model=schemas.PersonOut)
def get_person(person_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id)):
    person = db.query(models.Person).filter(models.Person.id == person_id, models.Person.org_id == org_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.patch("/{person_id}", response_model=schemas.PersonOut)
def update_person(person_id: str, payload: schemas.PersonCreate, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    person = db.query(models.Person).filter(models.Person.id == person_id, models.Person.org_id == org_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(person, k, v)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.delete("/{person_id}")
def delete_person(person_id: str, db: Session = Depends(db.session.get_db), org_id=Depends(deps.get_org_id), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    person = db.query(models.Person).filter(models.Person.id == person_id, models.Person.org_id == org_id).first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    db.delete(person)
    db.commit()
    return {"ok": True}
