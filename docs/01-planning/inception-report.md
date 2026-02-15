# Inception Report - Customer Database System (Real Estate)

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Project Overview

### Vision
Build a modern, dynamic customer database that feels like a beautiful, purpose-built spreadsheet with stronger collaboration, UX, and cross-list relationships. The system focuses on real estate customer data (properties, units, owners, landlords, managers) to enable effective follow-up and communication.

### Problem Statement
Generic spreadsheet tools are flexible but lack structured relationships, permission control, and task-specific UX for real estate data capture and collaboration.

### Outcome (updated)
A responsive web application that lets teams and individuals create multiple workspaces, build unlimited lists and items, relate records across lists, and collaborate securely with role-based access and a transparent invite/permissions model.

### Platform decisions (updated)
- Frontend: Vercel
- Backend: Render (Python microservices + worker)
- Database and storage: Neon.tech PostgreSQL + Object Storage
- Auth: JWT Authentication (JWT)

## 2) Goals and Success Criteria

### Goals
- Fast and flexible data entry with a clean, modern UI.
- Real-time collaboration with granular permissions and role hierarchy.
- Strong relationship linking between lists (e.g., People <-> Properties).
- Responsive design across desktop, tablet, and mobile screens.
- Minimalist, attractive interface with a consistent design system.

### Success Criteria
- Create a list with custom columns in under 60 seconds.
- Add 100+ rows with low latency and no UI lag.
- Invite and grant workspace access with a role in under 30 seconds.
- Link records across lists with search/autocomplete in under 5 seconds.
- Core screens pass WCAG AA checks.

## 3) Scope

### In Scope (MVP)
- One user → many workspaces; workspace → many lists; list → unlimited items.
- Shareable workspaces with invite flow and role-based permissions.
- Dynamic lists with unlimited rows/columns.
- Custom column types and validations.
- Relationships between lists with lookup and linking.
- Comments on rows or items and activity history/audit log.
- Import/export: Excel, CSV, JSON.

### Out of Scope (Phase 1)
- Native mobile app.
- Advanced analytics dashboards.
- Marketing automation or messaging campaigns.
- AI enrichment (consider for Phase 3).

## 4) Key Users & Personas (updated)
- Owner — full control (workspace lifecycle, members, and role management).
- Admin — manage members and workspace settings (cannot delete workspace).
- Editor — create and modify lists/items.
- Member — view and contribute within limits (create items, comment).
- Viewer/Commenter — read-only or comment-only affordances (future phase).

> Decision: support multiple simultaneous owners (co-owners). At least one owner must remain.

## 5) Core Features (MVP)

### List and Data Management
- Create, rename, duplicate, archive lists.
- Add/edit/delete rows and columns.
- Column types: text, number, date, currency, phone, email, URL, single select, multi select, boolean, file, location.
- Validations: required fields, unique fields, format checks (email, phone).

### Relationships
- Link records between lists (e.g., Properties <-> Owners, Properties <-> People).
- Support one-to-many and many-to-many links.
- Search and create related records inline.

### Sharing and Collaboration (updated)
- Workspace-level invites with role assignment: `owner`, `admin`, `editor`, `member`.
- Invite by email with acceptance token; unregistered emails create pending invitations.
- Prevent removing or demoting the last remaining `owner`.
- Per-list and per-item sharing controls (for advanced ACLs in later phases).

### Comments and History
- Comment on rows or items.
- Change history for critical fields with actor & timestamp.

### Import and Export
- Import: Excel, CSV, JSON.
- Export: Excel, CSV, JSON.
- Suggested additional format: TSV.

## 6) Collaboration & Permissions — design details

### Permission model (brief)
- `owner`: full workspace control (manage members, promote to owner, delete workspace).
- `admin`: manage members (invite/remove, cannot delete workspace or transfer ownership to self), manage lists/items.
- `editor`: create/edit lists & items.
- `member`: contribute (create items, comment), limited admin actions.

Rules:
- Only an `owner` may promote another user to `owner`.
- Membership is unique per user + workspace.
- Audit all role changes (who, when, previous role).
- Server-side enforcement for every sensitive action.

### Invite flow
1. Owner/Admin sends invite to an email + role.
2. System stores a pending `workspace_membership` with `invite_token`.
3. Invitee clicks link — signs in / registers — token accepted → role becomes `accepted`.
4. Unaccepted invites can be revoked by Owner/Admin.

### Edge cases to enforce
- Disallow demoting/removing the last owner.
- Rate-limit invites and verify email ownership.
- If a workspace owner account is deleted, ensure ownership transfer or fail-safe owner assignment.

## 7) Data model & example SQL (Postgres)

- Enforce referential integrity and UNIQUE(workspace_id, user_id).
- Use an enum for roles and status for clarity and performance.

```sql
-- roles
CREATE TYPE workspace_role AS ENUM ('owner','admin','editor','member');
CREATE TYPE invite_status AS ENUM ('invited','accepted','revoked');

-- workspaces
CREATE TABLE workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  created_by UUID REFERENCES auth.users(id),
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- memberships
CREATE TABLE workspace_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id),
  role workspace_role NOT NULL DEFAULT 'member',
  status invite_status NOT NULL DEFAULT 'invited',
  invite_token TEXT,
  invited_by UUID REFERENCES auth.users(id),
  invited_at TIMESTAMPTZ,
  accepted_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  UNIQUE(workspace_id, user_id)
);
CREATE INDEX idx_wm_user ON workspace_memberships(user_id);
CREATE INDEX idx_wm_workspace_role ON workspace_memberships(workspace_id, role);

-- lists and items
CREATE TABLE lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID REFERENCES workspaces(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  position INT,
  created_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  list_id UUID REFERENCES lists(id) ON DELETE CASCADE,
  title TEXT,
  values JSONB NOT NULL DEFAULT '{}',
  position INT,
  created_by UUID REFERENCES auth.users(id),
  updated_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

## 8) API surface (examples)
- POST /workspaces — create workspace (creator -> owner)
- GET /workspaces — list user workspaces
- GET /workspaces/:id — workspace details + members
- POST /workspaces/:id/invite — invite email + role (owner/admin)
- POST /workspaces/:id/members/:memberId/role — change role (enforce owner rules)
- DELETE /workspaces/:id/members/:memberId — remove member (respect owner rules)
- CRUD lists: /workspaces/:id/lists
- CRUD items: /lists/:listId/items

Security: always validate membership and role on the server — never rely on client-side checks.

## 9) Tests & QA (recommended)
- Unit tests: role transitions, prevent demoting last owner, invite token acceptance.
- Integration tests: invite → accept flow, role-based access checks per endpoint.
- E2E/UI: share modal, members list, role change flows, blocked UI actions for insufficient roles.
- Acceptance tests: invitee receives email, accepts, and sees workspace per role.

## 10) Next steps (priority)
1. Add DB migration (create `workspace_memberships` + role enum). ✅
2. Implement membership APIs + server-side checks.
3. Add unit & integration tests for membership and role rules.
4. Add UI: share modal, members list, promote/demote controls.

## 11) Project Phases (status)
- Phase 1: MVP with workspace sharing & role-based permissions (updated scope).
- Phase 2: Templates, smart views, bulk operations.
- Phase 3: Automation, AI enrichment, analytics.

## 12) Open Decisions (updated)
- Billing model (per workspace, per seat, or tiered) — still open.
- Data retention policy for deleted lists — still open.
- Ownership model — decided: multiple simultaneous owners allowed.
- Email service for invites and notifications — still open.

---

### Appendix — Acceptance criteria for collaboration feature
- A user can create multiple workspaces and invite other users.
- Invited users receive an email with a token and gain access after accepting.
- Roles control API/UX access; attempts to perform forbidden actions return 403.
- The system prevents removing or demoting the final `owner`.


<!-- End of updated inception report -->
