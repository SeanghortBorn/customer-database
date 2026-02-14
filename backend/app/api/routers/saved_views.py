from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import session as db_session, models
from app.api import deps

router = APIRouter()


@router.post('/', response_model=dict)
def create_saved_view(name: str, resource_type: str, filters: dict = None, columns: dict = None, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.get_current_user)):
    sv = models.SavedView(org_id=current_user.org_id, user_id=current_user.id, name=name, resource_type=resource_type, filters=filters, columns=columns)
    db.add(sv)
    db.commit()
    db.refresh(sv)
    return {"id": str(sv.id), "name": sv.name}


@router.get('/', response_model=List[dict])
def list_saved_views(resource_type: str | None = None, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.get_current_user)):
    q = db.query(models.SavedView).filter(models.SavedView.org_id == current_user.org_id)
    if resource_type:
        q = q.filter(models.SavedView.resource_type == resource_type)
    return q.all()


@router.delete('/{view_id}')
def delete_saved_view(view_id: str, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    sv = db.query(models.SavedView).filter(models.SavedView.id == view_id, models.SavedView.org_id == current_user.org_id).first()
    if not sv:
        raise HTTPException(status_code=404, detail='Saved view not found')
    db.delete(sv)
    db.commit()
    return {"ok": True}
