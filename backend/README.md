Backend (FastAPI)

Commands (development):

- Build & run with docker-compose (root): `docker-compose up --build`
- Start local server: `uvicorn app.main:app --reload --port 8000`
- Run migrations: `alembic upgrade head`
- Seed development user: `python backend/scripts/seed.py`

Notes:
- DB URL configured with `DATABASE_URL` environment variable.
- Auth is scaffolded as a simple stub; replace `app.api.deps.get_current_user` with a real auth flow (OAuth/JWT) for production.
