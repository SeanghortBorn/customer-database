from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import session as db_session, models
from app.api import deps

router = APIRouter()


@router.post('/')
def create_team(name: str, db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    team = models.Team(org_id=current_user.org_id, name=name)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get('/')
def list_teams(db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.get_current_user)):
    return db.query(models.Team).filter(models.Team.org_id == current_user.org_id).all()


@router.post('/{team_id}/members')
def add_member(team_id: str, user_email: str, role: str = 'member', db: Session = Depends(db_session.get_db), current_user: models.User = Depends(deps.require_role('owner','admin'))):
    team = db.query(models.Team).filter(models.Team.id == team_id, models.Team.org_id == current_user.org_id).first()
    if not team:
        raise HTTPException(status_code=404, detail='Team not found')
    user = db.query(models.User).filter(models.User.email == user_email, models.User.org_id == current_user.org_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    member = models.TeamMember(team_id=team.id, user_id=user.id, role=role)
    db.add(member)
    db.commit()
    return member
