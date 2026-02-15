# Quick Start Guide - Customer Database System

## 🚀 Get Started in 30 Minutes

This guide will get your development environment running with the first deployable slice.

---

## Prerequisites

- **Conda:** Miniconda or Anaconda (for Python environment)
- **Python:** 3.11+ (managed by conda)
- **Node.js:** 20+
- **Docker:** For local database
- **Git:** Version control
- **Accounts:**
  - GitHub (for code + CI/CD)
  - Supabase (free tier)
  - Render (free tier for dev)
  - Vercel (free tier)

**⚠️ Important:** This project uses **Conda** for environment management, not venv. See [CONDA_SETUP.md](./CONDA_SETUP.md) for details.

---

## Step 1: Clone & Initialize (5 min)

```bash
# Create project structure
cd /home/seanghortborn/projects/customer-database

# Initialize Git if not already
git init
git add .
git commit -m "Initial project structure with documentation"

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
*.egg-info/
dist/
build/

# Conda
.conda/
environment.yml.bak

# Node
node_modules/
.next/
out/
.env*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Env files
.env
.env.local
.env.production

# Database
*.db
*.sqlite
EOF
```

---

## Step 2: Backend Setup (10 min)

### Create Backend Structure

```bash
mkdir -p backend/{api_gateway,services/workspace,shared/{models,schemas},alembic/versions,tests}
cd backend
```

### Setup Conda Environment

```bash
# Activate conda environment (from project root)
cd /home/seanghortborn/projects/customer-database
conda activate cds

# If environment doesn't exist, create it:
# conda env create -f environment.yml

# Go to backend folder
cd backend

# Create requirements.txt (for backend specific packages)
cat > requirements.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9
supabase==2.3.4
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
redis==5.0.1
rq==1.16.0
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0
python-dotenv==1.0.0
EOF

# Install
pip install -r requirements.txt
```

### Setup Database (Local Development)

```bash
# Create docker-compose.yml for local DB
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
EOF

# Start database
docker compose up -d
```

### Configure Alembic

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini - set database URL
# Or better, use env variable in alembic/env.py
```

**Edit `alembic/env.py`:**
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from shared.models import Base  # Import your models

# this is the Alembic Config object
config = context.config

# Set database URL from environment
config.set_main_option(
    'sqlalchemy.url',
    os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/customer_db')
)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Create Basic Files

**`backend/.env`** (local development):
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/customer_db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_JWT_SECRET=your-jwt-secret
REDIS_URL=redis://localhost:6379
```

**`backend/shared/database.py`:**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**`backend/shared/models/__init__.py`:**
```python
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from ..database import Base

class Workspace(Base):
    __tablename__ = 'workspaces'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    description = Column(Text)
    created_by = Column(UUID(as_uuid=True))
    settings = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class WorkspaceMembership(Base):
    __tablename__ = 'workspace_memberships'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(UUID(as_uuid=True))
    role = Column(Enum('owner', 'admin', 'editor', 'member', name='workspace_role'), nullable=False, default='member')
    status = Column(Enum('invited', 'accepted', 'revoked', name='invite_status'), nullable=False, default='invited')
    invite_token = Column(String)
    invite_email = Column(String)
    invited_by = Column(UUID(as_uuid=True))
    invited_at = Column(DateTime(timezone=True))
    accepted_at = Column(DateTime(timezone=True))
    revoked_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

**`backend/api_gateway/main.py`:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Customer Database API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Customer Database API v0.1.0"}

# Include routers as we build them
# from services.workspace.routes import router as workspace_router
# app.include_router(workspace_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Run Backend

```bash
# Make sure you're in backend/ and venv is activated
python -m api_gateway.main
```

Visit: http://localhost:8000/docs (FastAPI auto-docs)

---

## Step 3: Frontend Setup (10 min)

```bash
# Go back to project root
cd ..

# Create Next.js app
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*"

cd frontend

# Install dependencies
npm install @supabase/supabase-js zustand @tanstack/react-query @tanstack/react-table
npm install react-hook-form zod @hookform/resolvers
npm install lucide-react class-variance-authority clsx tailwind-merge

# Initialize shadcn/ui
npx shadcn-ui@latest init
# Choose: Default style, Slate color, CSS variables: yes
```

### Configure Environment

**`frontend/.env.local`:**
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Create Basic Layout

**`frontend/lib/supabase.ts`:**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

**`frontend/app/page.tsx`:**
```typescript
import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-8">Customer Database</h1>
      <div className="flex gap-4">
        <Link 
          href="/login" 
          className="rounded bg-blue-600 px-6 py-3 text-white hover:bg-blue-700"
        >
          Sign In
        </Link>
        <Link 
          href="/signup" 
          className="rounded border px-6 py-3 hover:bg-gray-100"
        >
          Sign Up
        </Link>
      </div>
    </div>
  )
}
```

### Run Frontend

```bash
npm run dev
```

Visit: http://localhost:3000

---

## Step 4: Supabase Setup (5 min)

1. **Create Project:**
   - Go to https://supabase.com
   - Create new project (choose region close to you)
   - Wait for provisioning (~2 min)

2. **Get Credentials:**
   - Project Settings → API
   - Copy:
     - URL
     - `anon` public key
     - `service_role` key (keep secret!)
     - JWT Secret (Settings → API → JWT Settings)

3. **Enable Email Auth:**
   - Authentication → Providers
   - Enable Email provider
   - Configure email templates (optional)

4. **Update `.env` files:**
   - Update `backend/.env` with Supabase credentials
   - Update `frontend/.env.local` with Supabase credentials

---

## Step 5: First Migration & Test

```bash
cd backend

# Create first migration
alembic revision --autogenerate -m "Initial schema"

# Review the migration file in alembic/versions/

# Run migration
alembic upgrade head

# Verify tables created
psql postgresql://postgres:postgres@localhost:5432/customer_db -c "\dt"
```

---

## Step 6: Run Tests

```bash
# In backend/
pytest tests/ -v

# Expected: Pass (or skip if no tests yet)
```

---

## Step 7: Deploy to Staging (Optional)

### Backend on Render

1. Create account at https://render.com
2. New Web Service
3. Connect GitHub repo
4. Configure:
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn api_gateway.main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:** Add all from `.env`
5. Deploy

### Frontend on Vercel

1. Create account at https://vercel.com
2. Import Git Repository
3. Framework: Next.js (auto-detected)
4. Root Directory: `frontend`
5. Environment Variables: Add from `.env.local`
6. Deploy

---

## Verification Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] Database accessible (postgres + redis)
- [ ] Supabase project created
- [ ] Can see API docs at http://localhost:8000/docs
- [ ] Frontend loads without errors
- [ ] Environment variables configured

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check if database is running
docker compose ps

# Check database connection
psql postgresql://postgres:postgres@localhost:5432/customer_db -c "SELECT 1"
```

### Frontend build errors
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run dev
```

### Database migration errors
```bash
# Reset database (DEV ONLY!)
alembic downgrade base
docker compose down -v
docker compose up -d
alembic upgrade head
```

---

## Next Steps

Now you're ready to implement your first feature! 

**Recommended first slice:** Workspace Creation

See [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) → **Phase 1: Slice 1.1**

### Quick Implementation Order

1. ✅ Setup complete (you are here)
2. → Implement auth pages (signup/login)
3. → Create workspace CRUD endpoints
4. → Build workspace list UI
5. → Add workspace invites
6. → Deploy to staging
7. → Continue with Lists & Items

---

## Helpful Commands

```bash
# Backend
cd backend
source .venv/bin/activate
python -m api_gateway.main          # Run server
alembic upgrade head                # Run migrations
pytest tests/ -v                    # Run tests

# Frontend
cd frontend
npm run dev                         # Development server
npm run build                       # Production build
npm run lint                        # Lint code

# Database
docker compose up -d                # Start DB
docker compose down                 # Stop DB
docker compose logs -f postgres     # View logs

# Git
git add .
git commit -m "feat: implement workspace creation"
git push origin main
```

---

## Resources

- **Docs:** See `/docs` folder for full specs
- **Roadmap:** See `IMPLEMENTATION_ROADMAP.md`
- **Architecture:** See `docs/architecture.md`
- **API Spec:** See `docs/api-spec.md`

**Happy coding! 🚀**
