Zoneer — Customer & Property Manager (scaffold)

This repository contains an MVP scaffold for a customer/property management application (Zoneer):

- Backend: FastAPI + SQLAlchemy + Alembic (Postgres)
- Frontend: Next.js (TypeScript)
- DB: PostgreSQL (docker-compose)

What I scaffolded:
- Full DB schema (organizations, users, people, properties, units, shares, comments, activity)
- FastAPI backend with CRUD endpoints for People / Properties / Units
- Alembic initial migration + helper scripts
- Next.js responsive UI (list pages) and simple components
- Dockerfile + docker-compose for local dev

Quick start — development (recommended)

1) Copy env files:
   - `cp backend/.env.example backend/.env`
   - `cp frontend/.env.local.example frontend/.env.local`

2) Start services with Docker Compose:
   - `docker-compose up --build`

3) Create DB schema and seed demo user:
   - `docker compose exec backend alembic upgrade head`
   - `docker compose exec backend python backend/scripts/seed.py` (creates `admin@example.com` / `password`)
   - (or: `python -m app.db.create_all` for a quick create — requires local libpq / DB)

4) Open the frontend:
   - http://localhost:3000 — People & Properties list pages (supports sign in / register)
   - Backend API: http://localhost:8000/docs (OpenAPI)

Completed features:
- Authentication: Email + OAuth (Google/Microsoft) + RBAC (Owner/Admin/Editor/Commenter/Viewer).
- Invites & Teams: send invites, accept invite flow, team management.
- Sharing: resource-level sharing and share-by-link (with expiry and max‑views), plus audit logs.
- Units & Pricing: per-unit records + unit price history and unit history UI.
- Search & Saved Views: simple full-text search endpoint and saved view storage.
- Realtime: WebSocket endpoint `/ws` with frontend notifications for create events.
- RLS & Performance: Postgres RLS policies (migration) + GIN/trigram indexes for search.
- Tests & CI: pytest tests and GitHub Actions workflow (`.github/workflows/ci.yml`).

Quick feature notes:
- OAuth: server-side Google / Microsoft routes are scaffolded (set CLIENT_ID/SECRET in `backend/.env`). After provider callback you will be redirected to the frontend with a token in the URL.
- Invites & Teams: admin endpoints (`/api/invites`, `/api/teams`) let Owners/Admins invite users and manage teams; invite emails are sent when SMTP is configured in `backend/.env`.
- Share-by-link: `POST /api/shares/link` supports `expires_in_days` and `max_views`; public resolver at `/s/{token}` enforces expiry and view limits and creates activity logs.
- Saved views: create/list/delete saved views via `/api/saved-views`.
- Realtime: frontend connects to `/ws` and shows brief notifications when people/properties/units are created.
- CI: backend unit tests run on push/PR via GitHub Actions (see `.github/workflows/ci.yml`).

Files to look at first:
- `backend/app/db/models.py` (schema)
- `backend/app/api/routers` (API endpoints)
- `frontend/pages` and `frontend/components` (UI)

Testing
- Unit tests (backend): from the project root run `PYTHONPATH=backend .venv/bin/pytest backend/tests`.
  - Tests now use isolated per-test SQLite DB files (fast, hermetic).
- End-to-end (E2E) tests (frontend): Playwright is configured under `frontend/e2e`.
  - Start backend on port `8000` and run `cd frontend && npm ci && npx playwright install --with-deps && npm run test:e2e`.
  - CI will automatically run E2E on push/PR.

