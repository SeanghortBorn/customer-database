from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import session as db_session
from app.db import models
from app.schemas import UserCreate, UserOut, Token, RegisterResponse
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(payload: UserCreate, invite_token: str | None = None, db: Session = Depends(db_session.get_db)):
    # If a user exists with a password, block register; if exists without password, set password (invite flow)
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing and existing.hashed_password:
        raise HTTPException(status_code=400, detail="User already exists")

    # Check for invite by token or by email
    invite = None
    if invite_token:
        invite = db.query(models.Invite).filter(models.Invite.token == invite_token).first()
    if not invite:
        invite = db.query(models.Invite).filter(models.Invite.email == payload.email).first()

    if existing and not existing.hashed_password:
        # user created via invite earlier - set password and return
        existing.hashed_password = get_password_hash(payload.password)
        if payload.name:
            existing.name = payload.name
        db.add(existing)
        db.commit()
        db.refresh(existing)
        access_token = create_access_token(subject=str(existing.id))
        return {"access_token": access_token, "token_type": "bearer", "user": existing}

    if invite:
        # respect invite org and role
        org_id = invite.org_id
        role = invite.role or 'editor'
        user = models.User(org_id=org_id, email=payload.email, name=payload.name, role=role, hashed_password=get_password_hash(payload.password))
        db.add(user)
        db.commit()
        db.refresh(user)
        invite.accepted_by = user.id
        db.add(invite)
        db.commit()
        access_token = create_access_token(subject=str(user.id))
        return {"access_token": access_token, "token_type": "bearer", "user": user}

    # No invite: create personal org
    org_name = payload.dict().get('org_name') or f"{payload.email} (org)"
    org = models.Organization(name=org_name)
    db.add(org)
    db.commit()
    db.refresh(org)

    user = models.User(org_id=org.id, email=payload.email, name=payload.name, role='owner', hashed_password=get_password_hash(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer", "user": user}



@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not user.hashed_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60 * 24 * 7)
    access_token = create_access_token(subject=str(user.id), expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


from app.api import deps


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: models.User = Depends(deps.get_current_user)):
    return current_user


# NOTE: OAuth providers (Google/Microsoft) should be implemented with proper verification.
# For MVP we accept a dev-only "oauth" flow that upserts by email.
@router.post("/oauth/dev", response_model=Token)
def oauth_dev_login(email: str, name: str = None, db: Session = Depends(db_session.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        org = models.Organization(name=f"{email} (org)")
        db.add(org)
        db.commit()
        db.refresh(org)
        user = models.User(org_id=org.id, email=email, name=name, role='editor')
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token(subject=str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}


# --- OAuth (Google / Microsoft) using Authlib (server-side redirect flow) ---
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

oauth = OAuth()
if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )

if settings.MICROSOFT_CLIENT_ID and settings.MICROSOFT_CLIENT_SECRET:
    oauth.register(
        name='microsoft',
        client_id=settings.MICROSOFT_CLIENT_ID,
        client_secret=settings.MICROSOFT_CLIENT_SECRET,
        server_metadata_url='https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )


@router.get('/login/{provider}')
async def oauth_login(request: Request, provider: str):
    if provider not in oauth._registry:
        raise HTTPException(status_code=400, detail='Unsupported provider')
    redirect_uri = request.url_for('oauth_callback', provider=provider)
    return await oauth.create_client(provider).authorize_redirect(request, redirect_uri)


@router.get('/auth/{provider}/callback')
async def oauth_callback(request: Request, provider: str, db: Session = Depends(db_session.get_db)):
    if provider not in oauth._registry:
        raise HTTPException(status_code=400, detail='Unsupported provider')
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    userinfo = await client.parse_id_token(request, token)
    email = userinfo.get('email') or userinfo.get('preferred_username')
    name = userinfo.get('name')
    # upsert user
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # create user in a new org for simplicity or reuse an org mapping strategy
        org = models.Organization(name=f"{email} (org)")
        db.add(org)
        db.commit()
        db.refresh(org)
        user = models.User(org_id=org.id, email=email, name=name, role='editor')
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token(subject=str(user.id))
    frontend = settings.FRONTEND_URL or 'http://localhost:3000'
    # redirect user back to frontend with token in query string (MVP)
    from starlette.responses import RedirectResponse
    return RedirectResponse(url=f"{frontend}/?token={access_token}")
