# Technical Architecture

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Architecture Goals
- Microservices aligned to domain boundaries, but practical to run on Render.
- Single public API surface for the frontend, with internal service isolation.
- Strong workspace-level access control with auditability.
- Scales to 100k+ records per workspace with predictable performance.
- Consistent design system in the frontend with strong table performance.

## 2) Hosting and Platform (Chosen)
- Frontend: Vercel (Next.js or similar SPA)
- Backend: Render (Python services + background workers)
- Database: Supabase Postgres
- Object storage: Supabase Storage (for file columns)

## 3) High-Level System Context
- Clients: Web app (desktop, tablet, mobile)
- API Edge: API Gateway (Python, FastAPI)
- Backend: Domain microservices (Python, FastAPI)
- Data: Supabase Postgres + Storage
- Async: Background worker service + Redis queue

## 4) Service Decomposition (Microservices)
Public-facing:
- API Gateway: auth verification, request routing, rate limits, response shaping

Domain services (internal):
- Auth and Session Service: Supabase Auth JWT verification and session rules
- Workspace and Membership Service: workspaces, invites, roles, permissions
- List and Item Service: lists, columns, items, item values
- Relationship Service: cross-list linking, lookups, and integrity checks
- Import/Export Service: CSV/Excel/JSON parsing, validation, batch writes
- Audit Log Service: append-only audit events, query API
- Notification Service (optional phase 2): email invites, system alerts

## 5) API Design and Communication
- Single public API base: /api/v1 on the Gateway
- Gateway to services: internal HTTP (FastAPI) with service-to-service auth
- Async jobs: Redis queue (RQ/Celery) for imports, exports, and large batch ops
- Frontend never calls internal services directly

## 6) Auth and Authorization
- Primary auth: Supabase Auth (email/password, magic link, or SSO later)
- Gateway validates JWT and attaches user context to downstream calls
- RBAC enforced in services using workspace membership rules
- Enforce "last owner" rule at the service layer and cover with tests

## 7) Data Storage and Schema Strategy
- Supabase Postgres for core data (workspaces, memberships, lists, items)
- Column definitions in a dedicated table; item values stored in JSONB per item
- Relationships stored in a junction table with indexes for fast linking
- Supabase Storage for file columns and attachments

## 8) Data Flow (Typical)
1. User signs in via Supabase Auth.
2. Client calls API Gateway with JWT.
3. Gateway verifies JWT, routes to Workspace service.
4. Workspace service checks roles and returns workspace data.
5. List/Item service handles CRUD with role checks and audit events.
6. Audit service stores append-only events for compliance and troubleshooting.
7. Import/Export jobs run in background and notify user when done.

## 9) Security
- TLS in transit, encryption at rest (Supabase managed)
- Role checks on every write endpoint and sensitive read
- Invite tokens are single-use with expiry and audit logging
- Rate-limiting at the Gateway (per user and per IP)

## 10) Scalability and Performance
- Index on workspace_id, list_id, relationship link keys
- Cursor pagination for large lists and audit logs
- Background jobs for heavy imports/exports
- Optional caching for list schemas and workspace metadata

## 11) Observability
- Structured logs with request IDs across services
- Metrics: latency, error rate, queue depth, DB query time
- Alerts for error spikes, queue failures, and slow queries

## 12) Environments and Deployment
- Environments: dev, staging, production
- CI: build, lint, tests on PR
- CD: auto deploy to staging, manual promotion to production

## 13) Resolved Decisions
- Auth provider: Supabase Auth (JWT)
- Hosting: Vercel (frontend), Render (backend), Supabase (DB/storage)
- API pattern: single Gateway with internal microservices
