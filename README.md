# Customer Database System

> A modern, collaborative spreadsheet-like customer database for real estate teams with workspace organization, role-based access control, and powerful cross-list relationships.

[![Status](https://img.shields.io/badge/status-in%20development-yellow)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)]()
[![Next.js](https://img.shields.io/badge/Next.js-14-black)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)
- [Current Status](#current-status)
- [Contributing](#contributing)

---

## 🎯 Overview

The Customer Database System is a web-based collaborative platform designed specifically for real estate teams to manage customer data with spreadsheet-like flexibility but with stronger:

- **Collaboration**: Role-based access control (Owner, Admin, Editor, Member)
- **Structure**: Define custom schemas with relationships across lists
- **Scalability**: Handle 100k+ records per workspace with predictable performance
- **Security**: JWT authentication, server-side permission enforcement, audit logging

### Problem We're Solving

Generic spreadsheet tools lack:
- Structured relationships between data (e.g., Properties ↔ Owners ↔ Managers)
- Granular permission control for teams
- Audit trails for compliance
- Purpose-built UX for real estate workflows

### Our Solution

A modern web app that combines the flexibility of spreadsheets with the power of relational databases, packaged in a beautiful, fast interface.

---

## ✨ Key Features

### Phase 1: Core Platform (MVP)
- ✅ **Multi-workspace organization**: One user → many workspaces
- ✅ **Team collaboration**: Invite members with roles (owner, admin, editor, member)
- ✅ **Dynamic lists**: Create unlimited lists with custom columns
- ✅ **Flexible schema**: 10+ column types (text, number, date, select, currency, etc.)
- ✅ **Spreadsheet UI**: Fast inline editing with keyboard navigation
- ✅ **Relationships**: Link records across lists (Properties ↔ People)
- ✅ **Comments**: Discuss items with your team
- ✅ **Audit log**: Track who changed what and when
- ✅ **Import/Export**: CSV, Excel, JSON support

### Phase 2: Future Enhancements
- 🔜 Advanced search and filters
- 🔜 File attachments
- 🔜 Saved views
- 🔜 Real-time collaboration
- 🔜 Mobile app
- 🔜 API access for integrations
- 🔜 AI-powered data enrichment

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL (via Supabase)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Auth**: Supabase Auth (JWT)
- **Background Jobs**: Python-RQ + Redis
- **Testing**: pytest

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State**: Zustand + TanStack Query
- **Tables**: TanStack Table
- **Forms**: React Hook Form + Zod

### Infrastructure
- **Hosting**: 
  - Backend: Render
  - Frontend: Vercel
  - Database: Supabase Postgres
  - Storage: Supabase Storage
  - Cache/Queue: Redis (Render/Upstash)
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry (errors) + platform metrics

### Architecture Pattern
- **Style**: Microservices (practical for Render)
- **API**: Single gateway with domain services
- **Auth**: JWT with role-based access control
- **Jobs**: Background workers for imports/exports

---

## 📁 Project Structure

```
customer-database/
├── backend/                         # Python backend (to be created)
│   ├── api_gateway/                # Main API entry point
│   ├── services/                   # Domain microservices
│   ├── shared/                     # Shared code
│   ├── alembic/                    # Database migrations
│   └── tests/                      # Test suite
│
├── frontend/                        # Next.js frontend (to be created)
│   ├── app/                        # App Router pages
│   ├── components/                 # React components
│   ├── lib/                        # Utilities
│   └── stores/                     # State management
│
├── docs/                            # 📚 All Project Documentation
│   ├── 00-getting-started/         # 🚀 Start here!
│   │   ├── ACTION_PLAN.md         # Week-by-week action guide
│   │   ├── QUICK_START.md         # 30-minute setup
│   │   ├── IMPLEMENTATION_ROADMAP.md  # Detailed implementation
│   │   └── INDEX.md               # Folder navigation
│   │
│   ├── 01-planning/                # 📋 Product & Planning
│   │   ├── prd.md                 # Product requirements
│   │   ├── inception-report.md    # Project background
│   │   ├── delivery-plan.md       # Milestones & timeline
│   │   └── INDEX.md               # Folder navigation
│   │
│   ├── 02-architecture/            # 🏗️ Technical Design
│   │   ├── architecture.md        # System architecture
│   │   ├── database-design.md     # Complete schema
│   │   ├── data-model-migration.md  # Migration strategy
│   │   └── INDEX.md               # Folder navigation
│   │
│   ├── 03-specifications/          # 📐 Detailed Specs
│   │   ├── api-spec.md           # API endpoints
│   │   ├── ux-ui-spec.md         # Design system
│   │   ├── permission-matrix.md   # RBAC rules
│   │   └── INDEX.md               # Folder navigation
│   │
│   ├── 04-development/             # 💻 Dev Workflows
│   │   ├── FEATURE_BREAKDOWN.md   # Feature tracking
│   │   ├── test-plan.md          # Testing strategy
│   │   └── INDEX.md               # Folder navigation
│   │
│   ├── 05-operations/              # 🚢 DevOps & Production
│   │   ├── ops-devops-plan.md    # Deployment guide
│   │   ├── legal-compliance.md    # Legal requirements
│   │   └── INDEX.md               # Folder navigation
│   │
│   ├── 99-history/                 # 📜 Change History
│   │   ├── CHANGELOG.md          # All modifications tracked
│   │   └── INDEX.md               # Folder navigation
│   │
│   └── PROJECT_STANDARDS.md        # 📏 Organization guidelines
│
├── .github/workflows/              # CI/CD pipelines (to be created)
│
└── README.md                        # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 20 or higher
- **Docker**: For local database
- **Git**: Version control

### Quick Setup (30 minutes)

**Detailed instructions**: See [QUICK_START.md](./QUICK_START.md)

```bash
# 1. Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d
alembic upgrade head
python -m api_gateway.main

# 2. Frontend setup
cd frontend
npm install
npm run dev

# Visit http://localhost:3000
```

### Accounts Needed

- **Supabase**: https://supabase.com (free tier)
- **Render**: https://render.com (free tier)
- **Vercel**: https://vercel.com (free tier)

---

## 📚 Documentation

### 🎯 Quick Navigation

All documentation is organized in `/docs` by topic:

| Folder | Purpose | Start Here |
|--------|---------|------------|
| [00-getting-started](./docs/00-getting-started/) | **Start here!** Setup guides and roadmaps | [QUICK_START.md](./docs/00-getting-started/QUICK_START.md) |
| [01-planning](./docs/01-planning/) | Product requirements and vision | [prd.md](./docs/01-planning/prd.md) |
| [02-architecture](./docs/02-architecture/) | System design and database | [architecture.md](./docs/02-architecture/architecture.md) |
| [03-specifications](./docs/03-specifications/) | API, UX/UI, permissions | [api-spec.md](./docs/03-specifications/api-spec.md) |
| [04-development](./docs/04-development/) | Feature tracking and testing | [FEATURE_BREAKDOWN.md](./docs/04-development/FEATURE_BREAKDOWN.md) |
| [05-operations](./docs/05-operations/) | DevOps and compliance | [ops-devops-plan.md](./docs/05-operations/ops-devops-plan.md) |
| [99-history](./docs/99-history/) | Change tracking | [CHANGELOG.md](./docs/99-history/CHANGELOG.md) |

💡 **Tip:** Each folder contains an `INDEX.md` file for easy navigation!

### 📋 Essential Documents

**For Developers:**
- [Quick Start Guide](./docs/00-getting-started/QUICK_START.md) - Get running in 30 minutes
- [Implementation Roadmap](./docs/00-getting-started/IMPLEMENTATION_ROADMAP.md) - Detailed code examples
- [Action Plan](./docs/00-getting-started/ACTION_PLAN.md) - Week-by-week tasks

**For Product Team:**
- [Product Requirements](./docs/01-planning/prd.md) - What we're building
- [Feature Breakdown](./docs/04-development/FEATURE_BREAKDOWN.md) - Feature priorities and status

**For DevOps:**
- [Architecture](./docs/02-architecture/architecture.md) - System design
- [Ops/DevOps Plan](./docs/05-operations/ops-devops-plan.md) - Deployment strategy

**For Project Management:**
- [Delivery Plan](./docs/01-planning/delivery-plan.md) - Milestones and timeline
- [Project Standards](./docs/PROJECT_STANDARDS.md) - Organization guidelines

---

## 💻 Development Workflow

### Micro-Development Approach

We follow a **vertical slice** approach where each feature is:
- End-to-end (database → API → UI)
- Independently deployable
- Fully tested
- Production-ready

### Development Cycle

1. Pick feature from [FEATURE_BREAKDOWN.md](./FEATURE_BREAKDOWN.md)
2. Create feature branch
3. Implement (DB → API → UI → tests)
4. Open PR (CI runs automatically)
5. Code review
6. Merge to main → auto-deploy to staging
7. QA on staging
8. Manual deploy to production
9. Monitor and iterate

---

## 🚢 Deployment

### Environments

- **Development**: Local (Docker Compose)
- **Staging**: Auto-deploy from `main` branch
- **Production**: Manual promotion with approval

### CI/CD Pipeline

- **PR**: Lint + Tests + Build check
- **Main**: Auto-deploy to staging
- **Production**: Manual deploy with checklist

See [ops-devops-plan.md](./docs/ops-devops-plan.md) for details.

---

## 🎯 Current Status

### ✅ Completed
- [x] Project planning and documentation
- [x] Architecture design
- [x] Database schema design
- [x] API specification
- [x] UX/UI design system
- [x] Implementation roadmap

### 🏗️ Next Steps
- [ ] Project setup (Week 1) - See [QUICK_START.md](./QUICK_START.md)
- [ ] Phase 1: Workspaces (Week 2)
- [ ] Phase 2: Lists & Items (Week 3-4)
- [ ] Phase 3: Collaboration (Week 5)
- [ ] Phase 4: Advanced Features (Week 6-8)

Track detailed progress in [FEATURE_BREAKDOWN.md](./FEATURE_BREAKDOWN.md).

---

## 🤝 Contributing

### For Developers

1. **Setup:** Follow [QUICK_START.md](./docs/00-getting-started/QUICK_START.md)
2. **Standards:** Read [PROJECT_STANDARDS.md](./docs/PROJECT_STANDARDS.md)
3. **Branch:** Create feature branch
4. **Implement:** Follow coding standards below
5. **Test:** Write tests (80%+ coverage)
6. **Document:** Update relevant docs
7. **PR:** Submit pull request

### Coding Standards

- **Python:** PEP 8, type hints, docstrings
- **TypeScript:** Strict mode, functional components
- **Commits:** Conventional commits (`feat:`, `fix:`, `docs:`, etc.)
- **Tests:** 80%+ coverage required
- **Documentation:** Update CHANGELOG.md for all changes

### File Organization

- **Always check** [PROJECT_STANDARDS.md](./docs/PROJECT_STANDARDS.md) before adding files
- **Update CHANGELOG.md** when modifying documentation
- **Archive old files** to `docs/99-history/` instead of deleting
- **Use INDEX.md** files for navigation within folders

---

## 🗺️ Architecture Overview

```
Client (Browser)
       ↓
Next.js Frontend (Vercel)
       ↓
API Gateway (FastAPI on Render)
       ↓
   ┌───┴────┐
   ↓        ↓
Domain   Background
Services   Workers
   ↓        ↓
   └───┬────┘
       ↓
PostgreSQL + Redis (Supabase)
```

---

## 🎬 Next Steps

**Ready to start building?**

### New to the Project?
1. **Setup:** Follow [QUICK_START.md](./docs/00-getting-started/QUICK_START.md) (30 min)
2. **Plan:** Review [ACTION_PLAN.md](./docs/00-getting-started/ACTION_PLAN.md) (15 min)
3. **Build:** Use [IMPLEMENTATION_ROADMAP.md](./docs/00-getting-started/IMPLEMENTATION_ROADMAP.md)

### Contributing to Documentation?
1. **Read:** [PROJECT_STANDARDS.md](./docs/PROJECT_STANDARDS.md) - Organization guidelines
2. **Navigate:** Use `INDEX.md` files in each folder
3. **Track:** Update [CHANGELOG.md](./docs/99-history/CHANGELOG.md) with all changes
4. **Archive:** Move old files to `docs/99-history/` instead of deleting

### Need Specific Information?

| I want to... | Go to... |
|--------------|----------|
| Get started quickly | [00-getting-started/QUICK_START.md](./docs/00-getting-started/QUICK_START.md) |
| Understand the product | [01-planning/prd.md](./docs/01-planning/prd.md) |
| Learn the architecture | [02-architecture/architecture.md](./docs/02-architecture/architecture.md) |
| Implement an API | [03-specifications/api-spec.md](./docs/03-specifications/api-spec.md) |
| Track feature progress | [04-development/FEATURE_BREAKDOWN.md](./docs/04-development/FEATURE_BREAKDOWN.md) |
| Deploy to production | [05-operations/ops-devops-plan.md](./docs/05-operations/ops-devops-plan.md) |
| See what changed | [99-history/CHANGELOG.md](./docs/99-history/CHANGELOG.md) |

**Let's build something amazing! 🚀**

---

## 📄 License

This project is proprietary. All rights reserved. © 2026

---

**⭐ If you find this helpful, please star the repository!**
