# Architecture - Index

**Folder:** `02-architecture/`  
**Purpose:** System architecture, database design, and technical decisions

---

## 📚 Documents in This Folder

### [architecture.md](./architecture.md)
**Technical Architecture and System Design**
- Microservices architecture
- Hosting and platform (Vercel, Render, Supabase)
- Service decomposition (Gateway, domain services)
- Auth and authorization strategy
- Security, scalability, and observability
- **Read this if:** You want to understand the overall system design

### [database-design.md](./database-design.md)
**Complete Database Schema**
- Core tables (workspaces, lists, items, memberships)
- Enums and constraints
- Relationships and indexes
- Migration order
- Optional Row Level Security (RLS)
- **Read this if:** You need database schema details for implementation

### [data-model-migration.md](./data-model-migration.md)
**Data Model and Migration Strategy**
- Core entities and relationships
- Key constraints (unique, foreign keys)
- Indexing strategy
- Migration plan and order
- Seed data approach
- **Read this if:** You're setting up database migrations

---

## 🎯 Key Technical Decisions

### Tech Stack
- **Frontend:** Next.js 14 (Vercel)
- **Backend:** FastAPI + Python (Render)
- **Database:** Neon.tech PostgreSQL
- **Auth:** JWT Authentication (JWT)
- **Jobs:** Python-RQ + Redis
- **Storage:** Object Storage

### Architecture Pattern
- Single API Gateway for frontend
- Internal domain microservices
- Background workers for heavy tasks
- JSONB for flexible item values

### Scalability Targets
- 100k+ records per workspace
- Predictable performance with indexing
- Horizontal scaling for API and workers
- Connection pooling (PgBouncer)

---

## 🔗 Related Documentation

- **Planning:** See [01-planning](../01-planning/) for product requirements
- **Specifications:** See [03-specifications](../03-specifications/) for API details
- **Operations:** See [05-operations](../05-operations/) for DevOps and deployment

---

**Last Updated:** February 15, 2026
