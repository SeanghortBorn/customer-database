# Implementation Roadmap - Customer Database System

**Project:** Customer Database System (Real Estate)  
**Date:** February 15, 2026  
**Approach:** Micro-development with continuous deployment

---

## Technology Stack (Recommended)

### Backend (Python)
- **API Framework:** FastAPI (modern, fast, auto-docs, async support)
- **ORM:** SQLAlchemy 2.0 with Alembic for migrations
- **Auth Integration:** Supabase Python Client + JWT validation
- **Background Jobs:** Python-RQ (Redis Queue) - simple, Python-native
- **Testing:** pytest + pytest-asyncio + httpx for API tests
- **Validation:** Pydantic (built into FastAPI)

### Frontend
- **Framework:** Next.js 14+ (App Router) - SSR, API routes, excellent DX
- **Styling:** Tailwind CSS + shadcn/ui components (high-quality, accessible)
- **State Management:** Zustand (lightweight) + TanStack Query (server state)
- **Table Component:** TanStack Table (formerly React Table) - powerful, flexible
- **Forms:** React Hook Form + Zod validation
- **Auth:** Supabase JavaScript client

### Infrastructure
- **Database:** Supabase Postgres (managed)
- **Storage:** Supabase Storage (for files)
- **Backend Hosting:** Render (Web Services + Background Workers)
- **Frontend Hosting:** Vercel (auto-preview, edge, great Next.js integration)
- **Cache/Queue:** Redis (Render managed or Upstash)

### DevOps & CI/CD
- **Version Control:** Git + GitHub
- **CI/CD:** GitHub Actions
- **Container:** Docker (for backend services)
- **IaC:** Terraform (optional, can start manual)
- **Monitoring:** Sentry (errors) + Render/Vercel built-in metrics

---

## Micro-Development Strategy

### Core Principle
Release **vertical slices** - each feature is end-to-end functional (database → API → UI) but limited in scope. This allows continuous deployment while building incrementally.

### Release Stages
1. **Foundation** - Auth & Infrastructure (1 deployable slice)
2. **Workspaces** - Multi-tenant basics (2 slices)
3. **Lists & Items** - Core data management (3 slices)
4. **Collaboration** - Sharing & permissions (2 slices)
5. **Advanced Features** - Relationships, import/export (3 slices)

Each slice is fully tested and production-ready before moving to the next.

---

## Phase 0: Project Setup & Foundation (Week 1)

### Slice 0.1: Project Structure & CI/CD Pipeline
**Goal:** Set up monorepo structure with working CI/CD

#### Backend Setup
```bash
mkdir -p backend/{api_gateway,services,shared,tests}
cd backend
```

**File Structure:**
```
backend/
├── api_gateway/           # Main API entry point
│   ├── main.py
│   ├── dependencies.py    # Auth, DB session
│   └── middleware.py
├── services/
│   ├── auth/             # Auth service
│   ├── workspace/        # Workspace service
│   ├── list_item/        # Lists & Items service
│   └── shared/           # Shared utilities
├── shared/
│   ├── database.py       # SQLAlchemy setup
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── auth.py          # JWT verification
├── alembic/             # Database migrations
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

**Key Files to Create:**

`requirements.txt`:
```txt
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
```

#### Frontend Setup
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir
cd frontend
```

**Install Key Dependencies:**
```bash
npm install @supabase/supabase-js zustand @tanstack/react-query @tanstack/react-table
npm install react-hook-form zod @hookform/resolvers
npm install -D @shadcn/ui
npx shadcn-ui@latest init
```

**File Structure:**
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── signup/
│   ├── (dashboard)/
│   │   ├── workspaces/
│   │   └── layout.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/              # shadcn components
│   └── features/        # Feature components
├── lib/
│   ├── supabase.ts     # Supabase client
│   ├── api.ts          # API client
│   └── hooks/
├── stores/             # Zustand stores
└── types/
```

#### CI/CD Setup

Create `.github/workflows/backend-ci.yml`:
```yaml
name: Backend CI

on:
  pull_request:
    paths:
      - 'backend/**'
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v
          
      - name: Lint
        run: |
          cd backend
          pip install ruff
          ruff check .

  deploy-staging:
    if: github.ref == 'refs/heads/main'
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK_STAGING }}
```

Create `.github/workflows/frontend-ci.yml`:
```yaml
name: Frontend CI

on:
  pull_request:
    paths:
      - 'frontend/**'
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
          
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          
      - name: Lint
        run: |
          cd frontend
          npm run lint
          
      - name: Type check
        run: |
          cd frontend
          npx tsc --noEmit
          
      - name: Build
        run: |
          cd frontend
          npm run build
```

#### Deliverables
- ✅ Monorepo with backend/frontend structure
- ✅ CI pipeline running on PRs
- ✅ Auto-deploy to staging on main merge
- ✅ Development environment with Docker Compose

**Time:** 2-3 days

---

### Slice 0.2: Database Setup & Auth Integration
**Goal:** Supabase project configured, auth working end-to-end

#### Supabase Setup
1. Create Supabase project (staging + production)
2. Enable Email Auth
3. Note credentials: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`

#### Database Schema - Initial Migration

Create `backend/alembic/versions/001_initial_schema.py`:
```python
"""Initial schema

Revision ID: 001
Create Date: 2026-02-15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

def upgrade():
    # Enums
    op.execute("""
        CREATE TYPE workspace_role AS ENUM ('owner','admin','editor','member');
        CREATE TYPE invite_status AS ENUM ('invited','accepted','revoked');
    """)
    
    # User profiles
    op.create_table(
        'user_profiles',
        sa.Column('user_id', UUID, primary_key=True),
        sa.Column('full_name', sa.Text),
        sa.Column('avatar_url', sa.Text),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    
    # Workspaces
    op.create_table(
        'workspaces',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('created_by', UUID),
        sa.Column('settings', JSONB, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_index('idx_workspaces_created_by', 'workspaces', ['created_by'])

def downgrade():
    op.drop_table('workspaces')
    op.drop_table('user_profiles')
    op.execute('DROP TYPE workspace_role, invite_status')
```

#### Backend Auth Module

`backend/shared/auth.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from supabase import create_client, Client
import os

security = HTTPBearer()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
JWT_SECRET = os.getenv('SUPABASE_JWT_SECRET')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Validate JWT and return user info"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail='Invalid token')
        return {'user_id': user_id, 'email': payload.get('email')}
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')
```

#### Frontend Auth Setup

`frontend/lib/supabase.ts`:
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
```

`frontend/app/(auth)/login/page.tsx`:
```typescript
'use client'
import { useState } from 'react'
import { supabase } from '@/lib/supabase'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) {
      alert(error.message)
    } else {
      router.push('/workspaces')
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <form onSubmit={handleLogin} className="w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold">Sign In</h1>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded border px-4 py-2"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded border px-4 py-2"
        />
        <button
          type="submit"
          className="w-full rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Sign In
        </button>
      </form>
    </div>
  )
}
```

#### Deliverables
- ✅ Supabase configured (staging + production)
- ✅ Initial database schema migrated
- ✅ Auth working: signup/login on frontend
- ✅ Backend JWT validation working
- ✅ Protected route example

**Time:** 2-3 days

---

## Phase 1: Workspaces Foundation (Week 2)

### Slice 1.1: Create & List Workspaces
**Goal:** Users can create workspaces and see their workspace list

#### Database Migration

`backend/alembic/versions/002_workspace_memberships.py`:
```python
"""Add workspace memberships

Revision ID: 002
"""
def upgrade():
    op.create_table(
        'workspace_memberships',
        sa.Column('id', UUID, primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('workspace_id', UUID, sa.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', UUID),
        sa.Column('role', sa.Enum('owner','admin','editor','member', name='workspace_role'), nullable=False, server_default='member'),
        sa.Column('status', sa.Enum('invited','accepted','revoked', name='invite_status'), nullable=False, server_default='invited'),
        sa.Column('invite_token', sa.Text),
        sa.Column('invite_email', sa.Text),
        sa.Column('invited_by', UUID),
        sa.Column('invited_at', sa.DateTime(timezone=True)),
        sa.Column('accepted_at', sa.DateTime(timezone=True)),
        sa.Column('revoked_at', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('workspace_id', 'user_id', name='uq_workspace_user')
    )
    op.create_index('idx_wm_user', 'workspace_memberships', ['user_id'])
    op.create_index('idx_wm_workspace_role', 'workspace_memberships', ['workspace_id', 'role'])
```

#### Backend API

`backend/services/workspace/routes.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from ...shared.auth import get_current_user
from ...shared.database import get_db
from .schemas import WorkspaceCreate, WorkspaceResponse
from .service import WorkspaceService

router = APIRouter(prefix='/workspaces', tags=['workspaces'])

@router.post('/', response_model=WorkspaceResponse)
async def create_workspace(
    workspace: WorkspaceCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new workspace (creator becomes owner)"""
    service = WorkspaceService(db)
    return service.create_workspace(
        name=workspace.name,
        description=workspace.description,
        created_by=UUID(current_user['user_id'])
    )

@router.get('/', response_model=list[WorkspaceResponse])
async def list_workspaces(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all workspaces the user is a member of"""
    service = WorkspaceService(db)
    return service.list_user_workspaces(user_id=UUID(current_user['user_id']))
```

`backend/services/workspace/service.py`:
```python
from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from ...shared.models import Workspace, WorkspaceMembership

class WorkspaceService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_workspace(self, name: str, description: str | None, created_by: UUID):
        # Create workspace
        workspace = Workspace(
            id=uuid4(),
            name=name,
            description=description,
            created_by=created_by
        )
        self.db.add(workspace)
        
        # Add creator as owner
        membership = WorkspaceMembership(
            workspace_id=workspace.id,
            user_id=created_by,
            role='owner',
            status='accepted',
            accepted_at=datetime.utcnow()
        )
        self.db.add(membership)
        self.db.commit()
        self.db.refresh(workspace)
        return workspace
    
    def list_user_workspaces(self, user_id: UUID):
        return self.db.query(Workspace).join(
            WorkspaceMembership,
            Workspace.id == WorkspaceMembership.workspace_id
        ).filter(
            WorkspaceMembership.user_id == user_id,
            WorkspaceMembership.status == 'accepted'
        ).all()
```

#### Frontend UI

`frontend/app/(dashboard)/workspaces/page.tsx`:
```typescript
'use client'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { supabase } from '@/lib/supabase'

export default function WorkspacesPage() {
  const [isCreating, setIsCreating] = useState(false)
  const [name, setName] = useState('')
  const queryClient = useQueryClient()

  const { data: workspaces, isLoading } = useQuery({
    queryKey: ['workspaces'],
    queryFn: async () => {
      const token = (await supabase.auth.getSession()).data.session?.access_token
      const res = await fetch('/api/v1/workspaces', {
        headers: { Authorization: `Bearer ${token}` }
      })
      return res.json()
    }
  })

  const createMutation = useMutation({
    mutationFn: async (workspaceName: string) => {
      const token = (await supabase.auth.getSession()).data.session?.access_token
      const res = await fetch('/api/v1/workspaces', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: workspaceName })
      })
      return res.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['workspaces'] })
      setIsCreating(false)
      setName('')
    }
  })

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Workspaces</h1>
        <button
          onClick={() => setIsCreating(true)}
          className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Create Workspace
        </button>
      </div>

      {isCreating && (
        <div className="mb-6 rounded border p-4">
          <input
            type="text"
            placeholder="Workspace name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full rounded border px-4 py-2 mb-2"
          />
          <div className="flex gap-2">
            <button
              onClick={() => createMutation.mutate(name)}
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            >
              Create
            </button>
            <button
              onClick={() => setIsCreating(false)}
              className="rounded border px-4 py-2 hover:bg-gray-100"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {workspaces?.map((ws: any) => (
          <div key={ws.id} className="rounded border p-6 hover:shadow-lg transition">
            <h3 className="text-xl font-semibold mb-2">{ws.name}</h3>
            <p className="text-gray-600">{ws.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
```

#### Tests

`backend/tests/test_workspace.py`:
```python
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

def test_create_workspace(client: TestClient, auth_headers):
    response = client.post(
        '/api/v1/workspaces',
        json={'name': 'Test Workspace', 'description': 'Test'},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'Test Workspace'
    assert 'id' in data

def test_list_workspaces(client: TestClient, auth_headers):
    response = client.get('/api/v1/workspaces', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

#### Deliverables
- ✅ Create workspace endpoint
- ✅ List workspaces endpoint
- ✅ Frontend: workspace list page with create
- ✅ Auto-create owner membership
- ✅ Tests passing

**Time:** 3-4 days  
**Deploy:** Staging → Production

---

### Slice 1.2: Workspace Members & Invitations
**Goal:** Invite users to workspace with roles

*(Continue with detailed implementation for invite flow, role management, etc.)*

---

## Phase 2: Lists & Items (Week 3-4)

### Slice 2.1: Create Lists with Basic Columns
### Slice 2.2: Add & Edit Items (Spreadsheet View)
### Slice 2.3: Column Types & Validations

---

## Phase 3: Collaboration Features (Week 5)

### Slice 3.1: Comments on Items
### Slice 3.2: Audit Log & Activity History

---

## Phase 4: Advanced Features (Week 6-8)

### Slice 4.1: Relationships Between Lists
### Slice 4.2: Import CSV/Excel
### Slice 4.3: Export & File Attachments

---

## Deployment Checklist (Per Release)

### Pre-Deploy
- [ ] All tests passing (unit + integration + E2E)
- [ ] Migrations tested on staging
- [ ] Manual QA completed
- [ ] Performance check (no regressions)
- [ ] Security scan clean

### Deploy
- [ ] Merge to main → auto-deploy staging
- [ ] Smoke test staging
- [ ] Run migration on production DB (with backup)
- [ ] Deploy backend services
- [ ] Deploy frontend
- [ ] Verify health checks

### Post-Deploy
- [ ] Monitor error rates (< 1%)
- [ ] Check key metrics (latency, DB queries)
- [ ] User acceptance test
- [ ] Document any issues

---

## Development Workflow

### Daily Flow
1. Pick next micro-feature from roadmap
2. Create feature branch: `feature/workspace-creation`
3. Implement: database → backend → frontend → tests
4. Open PR (CI runs automatically)
5. Code review + approval
6. Merge to main (auto-deploy to staging)
7. QA on staging
8. Manual promote to production

### Testing Strategy
- **Unit tests:** Business logic, role checks, validators
- **Integration tests:** API endpoints with real DB (test container)
- **E2E tests:** Critical user flows (Playwright)
- **Manual QA:** UX, edge cases, cross-browser

### Git Strategy
- Main branch: always deployable
- Feature branches: short-lived (1-3 days)
- Hotfix branches: for production issues
- Tags: release versions (`v0.1.0`, `v0.2.0`)

---

## Monitoring & Observability

### Metrics to Track
- API latency (p50, p95, p99)
- Error rate by endpoint
- Database query time
- Background job success rate
- User signup/login rate

### Alerts
- Error rate > 1%
- API latency > 2s (p95)
- Database connection pool exhausted
- Background job failures
- Disk/memory usage > 80%

### Tools
- **Sentry:** Error tracking
- **Render Metrics:** CPU, memory, requests
- **Vercel Analytics:** Frontend performance
- **Supabase Dashboard:** Database stats

---

## Next Steps

### Week 1: Foundation
1. Set up project structure (backend + frontend)
2. Configure CI/CD pipelines
3. Set up Supabase + run initial migrations
4. Implement auth (signup/login)
5. Deploy to staging

### Week 2: Workspaces
1. Implement workspace CRUD
2. Add workspace memberships
3. Build workspace list UI
4. Implement invite flow
5. Deploy to production (Slice 1.1 + 1.2)

### Week 3-4: Lists & Items
*(Continue with incremental releases)*

---

## Questions for You

1. **Team size:** Are you solo or do you have a team?
2. **Timeline:** What's your target for MVP release?
3. **Hosting budget:** Comfortable with Supabase/Render/Vercel pricing?
4. **Design:** Do you have designs or should I recommend UI kit?
5. **First feature priority:** Which slice should we build first?

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Supabase Docs](https://supabase.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com/)

### Example Repos
- FastAPI + SQLAlchemy: [full-stack-fastapi-template](https://github.com/tiangolo/full-stack-fastapi-template)
- Next.js + Supabase: [nextjs-supabase-auth](https://github.com/vercel/next.js/tree/canary/examples/with-supabase)

Let me know which slice you'd like to start with, and I'll provide detailed code for that feature!
