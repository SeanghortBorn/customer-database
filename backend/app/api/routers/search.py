from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import session as db_session, models
from app.api import deps

router = APIRouter()


@router.get('/')
def search(q: str, limit: int = 10, db: Session = Depends(db_session.get_db), org_id=Depends(deps.get_org_id)):
    results = {"people": [], "properties": []}
    if not q:
        return results
    pattern = f"%{q}%"
    people = db.query(models.Person).filter(models.Person.org_id == org_id).filter(
        (models.Person.first_name.ilike(pattern)) | (models.Person.last_name.ilike(pattern)) | (models.Person.email.ilike(pattern))
    ).limit(limit).all()
    props = db.query(models.Property).filter(models.Property.org_id == org_id).filter(
        (models.Property.name.ilike(pattern)) | (models.Property.address.ilike(pattern))
    ).limit(limit).all()
    results['people'] = people
    results['properties'] = props
    return results
