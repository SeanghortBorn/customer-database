from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.db import session as db_session
from app.db import models
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.ShareCreate)
def create_share(payload: schemas.ShareCreate, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    # find grantee user by email (must be in same org in this MVP)
    grantee = db.query(models.User).filter(models.User.email == payload.grantee_email, models.User.org_id == current_user.org_id).first()
    if not grantee:
        raise HTTPException(status_code=404, detail='Grantee not found')
    share = models.ResourceShare(org_id=current_user.org_id, resource_type=payload.resource_type, resource_id=payload.resource_id, grantee_type='user', grantee_id=grantee.id, role=payload.role)
    db.add(share)
    db.commit()
    db.refresh(share)
    # activity log
    log = models.ActivityLog(org_id=current_user.org_id, actor_id=current_user.id, action='share.create', resource_type=payload.resource_type, resource_id=payload.resource_id, diff={"grantee": grantee.email, "role": payload.role})
    db.add(log)
    db.commit()
    return payload


@router.post('/link')
def create_link_share(resource_type: str, resource_id: str, role: str = 'viewer', expires_in_days: int = 30, max_views: int | None = None, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin','editor'))):
    import uuid
    from datetime import datetime, timedelta
    token = uuid.uuid4().hex
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days) if expires_in_days else None
    share = models.ResourceShare(org_id=current_user.org_id, resource_type=resource_type, resource_id=resource_id, grantee_type='link', role=role, link_token=token, expires_at=expires_at, max_views=max_views, view_count=0)
    db.add(share)
    db.commit()
    db.refresh(share)
    # activity log
    log = models.ActivityLog(org_id=current_user.org_id, actor_id=current_user.id, action='share.link.create', resource_type=resource_type, resource_id=resource_id, diff={"token": token, "expires_at": str(expires_at), "max_views": max_views})
    db.add(log)
    db.commit()
    # return token which the frontend can convert to a shareable URL
    return {"token": token, "url": f"/s/{token}", "expires_at": expires_at.isoformat() if expires_at else None, "max_views": max_views}


@router.get('/resolve/{token}')
def resolve_link(token: str, db: Session = Depends(db_session.get_db)):
    from datetime import datetime
    share = db.query(models.ResourceShare).filter(models.ResourceShare.link_token == token).first()
    if not share:
        raise HTTPException(status_code=404, detail='Link not found or expired')
    # check expiry and max views
    if share.expires_at and share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail='Link expired')
    if share.max_views and share.view_count >= share.max_views:
        raise HTTPException(status_code=410, detail='Link expired (max views)')

    # increment view count and record activity
    share.view_count = (share.view_count or 0) + 1
    db.add(share)
    db.commit()
    log = models.ActivityLog(org_id=share.org_id, actor_id=None, action='share.link.view', resource_type=share.resource_type, resource_id=share.resource_id, diff={"token": token, "view_count": share.view_count})
    db.add(log)
    db.commit()

    # load the resource and return it (basic MVP)
    if share.resource_type == 'person':
        return db.query(models.Person).filter(models.Person.id == share.resource_id, models.Person.org_id == share.org_id).first()
    if share.resource_type == 'property':
        return db.query(models.Property).filter(models.Property.id == share.resource_id, models.Property.org_id == share.org_id).first()
    raise HTTPException(status_code=400, detail='Unsupported resource type')


@router.get("/", response_model=List[dict])
def list_shares(resource_type: str = None, resource_id: str = None, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.get_current_user)):
    q = db.query(models.ResourceShare).filter(models.ResourceShare.org_id == current_user.org_id)
    if resource_type:
        q = q.filter(models.ResourceShare.resource_type == resource_type)
    if resource_id:
        q = q.filter(models.ResourceShare.resource_id == resource_id)
    return q.all()


@router.delete("/{share_id}")
def delete_share(share_id: str, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    share = db.query(models.ResourceShare).filter(models.ResourceShare.id == share_id, models.ResourceShare.org_id == current_user.org_id).first()
    if not share:
        raise HTTPException(status_code=404, detail='Share not found')
    db.delete(share)
    db.commit()
    return {"ok": True}
