from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets
from datetime import datetime, timedelta

from app.db import session as db_session, models
from app.schemas import UserOut
from app.api import deps
from app.emails import send_email
from app.core.config import settings

router = APIRouter()


@router.post('/', dependencies=[Depends(deps.set_db_org)])
def create_invite(email: str, role: str = 'editor', expires_in_days: int = 7, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    token = secrets.token_urlsafe(24)
    invite = models.Invite(org_id=current_user.org_id, email=email, role=role, token=token, expires_at=(datetime.utcnow() + timedelta(days=expires_in_days)))
    db.add(invite)
    db.commit()
    db.refresh(invite)
    # Prepare accept URL for frontend (if configured) or API accept endpoint
    frontend = settings.FRONTEND_URL or ''
    accept_url = f"{frontend}/accept-invite?token={token}" if frontend else f"/api/invites/accept?token={token}"

    # send invite email when SMTP is configured (falls back to console)
    subject = f"You're invited to join {current_user.org.name if hasattr(current_user, 'org') else 'Zoneer'}"
    body = f"You have been invited as {role}. Click to accept: {accept_url}\n\nOr use this token: {token}"
    send_email(subject, email, body)

    return {"token": token, "accept_url": accept_url}


@router.get('/accept')
def accept_invite(token: str, name: str = None, db: Session = Depends(db_session.get_db)):
    invite = db.query(models.Invite).filter(models.Invite.token == token).first()
    if not invite or (invite.expires_at and invite.expires_at < datetime.utcnow()):
        raise HTTPException(status_code=404, detail='Invite expired or not found')
    # create user in org and mark accepted
    existing = db.query(models.User).filter(models.User.email == invite.email).first()
    if existing:
        invite.accepted_by = existing.id
        db.add(invite)
        db.commit()
        return {"ok": True, "user_id": str(existing.id), "email": invite.email}
    # create a placeholder user (passwordless) — user should complete registration
    user = models.User(org_id=invite.org_id, email=invite.email, name=name or invite.email.split('@')[0], role=invite.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    invite.accepted_by = user.id
    db.add(invite)
    db.commit()
    return {"ok": True, "user_id": str(user.id), "email": invite.email}
