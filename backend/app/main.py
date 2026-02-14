from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import asyncio

from app.api.routers import people, properties, units, auth, shares
from app.api import deps
from app.core.config import settings

app = FastAPI(title="Zoneer — Customer DB (backend)")

# CORS middleware must be added FIRST so it executes LAST (middleware runs in reverse order)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware required by OAuth (Authlib) to store state
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# simple in-memory WebSocket connection registry and broadcast helper (MVP)
app.state.ws_connections = set()

async def _ws_send(ws, data):
    try:
        await ws.send_json(data)
    except Exception:
        app.state.ws_connections.discard(ws)

def broadcast(event: str, payload: dict):
    payload_obj = {"event": event, "payload": payload}
    for ws in list(app.state.ws_connections):
        asyncio.create_task(_ws_send(ws, payload_obj))

# expose broadcast on app.state so routers can call it without circular imports
app.state.broadcast = broadcast


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    app.state.ws_connections.add(websocket)
    try:
        while True:
            # keep connection alive; server pushes messages via `broadcast`
            await websocket.receive_text()
    except WebSocketDisconnect:
        app.state.ws_connections.discard(websocket)

# auth router exposes /api/auth endpoints
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Backward-compatible route (convenience)
app.include_router(auth.router, prefix="/api", tags=["auth-compat"], include_in_schema=False)

# core CRUD routers (RLS session var set on these routes)
app.include_router(people.router, prefix="/api/people", tags=["people"], dependencies=[Depends(deps.set_db_org)])
app.include_router(properties.router, prefix="/api/properties", tags=["properties"], dependencies=[Depends(deps.set_db_org)])
app.include_router(units.router, prefix="/api/units", tags=["units"], dependencies=[Depends(deps.set_db_org)])

# sharing / permissions
app.include_router(shares.router, prefix="/api/shares", tags=["shares"], dependencies=[Depends(deps.set_db_org)])

# invites / teams (admin)
from app.api.routers import invites, teams, saved_views, search
app.include_router(invites.router, prefix="/api/invites", tags=["invites"])
app.include_router(teams.router, prefix="/api/teams", tags=["teams"], dependencies=[Depends(deps.set_db_org)])
# saved views & search
app.include_router(saved_views.router, prefix="/api/saved-views", tags=["saved_views"], dependencies=[Depends(deps.set_db_org)])
app.include_router(search.router, prefix="/api/search", tags=["search"], dependencies=[Depends(deps.set_db_org)])


# public link resolver (used by share-by-link)
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import session as db_session, models


@app.get('/s/{token}')
def shared_by_token(token: str, db: Session = Depends(db_session.get_db)):
    from datetime import datetime
    share = db.query(models.ResourceShare).filter(models.ResourceShare.link_token == token).first()
    if not share:
        raise HTTPException(status_code=404, detail='Shared link not found')
    # check expiry and max views
    if share.expires_at and share.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail='Link expired')
    if share.max_views and (share.view_count or 0) >= share.max_views:
        raise HTTPException(status_code=410, detail='Link expired (max views)')
    # increment view count and record activity
    share.view_count = (share.view_count or 0) + 1
    db.add(share)
    db.commit()
    try:
        log = models.ActivityLog(org_id=share.org_id, actor_id=None, action='share.link.view', resource_type=share.resource_type, resource_id=share.resource_id, diff={"token": token, "view_count": share.view_count})
        db.add(log)
        db.commit()
    except Exception:
        pass
    if share.resource_type == 'person':
        return db.query(models.Person).filter(models.Person.id == share.resource_id, models.Person.org_id == share.org_id).first()
    if share.resource_type == 'property':
        return db.query(models.Property).filter(models.Property.id == share.resource_id, models.Property.org_id == share.org_id).first()
    raise HTTPException(status_code=400, detail='Unsupported resource')


@app.get("/health")
def health():
    return {"status": "ok"}
