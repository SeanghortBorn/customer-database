# Database Design

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Overview
This design targets Supabase Postgres with a multi-tenant, workspace-first model. It supports dynamic lists, flexible column definitions, item values stored in JSONB, relationship links across lists, invites, role enforcement, audit logs, and import/export jobs. The schema is optimized for 100k+ records per workspace with predictable query performance.

## 2) Core Principles
- Workspace is the primary tenant boundary.
- Role enforcement is application-layer with optional RLS for defense in depth.
- Lists define schema via columns; items store values in JSONB.
- Relationships are explicit and indexed for fast linking.
- Audit is append-only.

## 3) Enums
```sql
CREATE TYPE workspace_role AS ENUM ('owner','admin','editor','member');
CREATE TYPE invite_status AS ENUM ('invited','accepted','revoked');
CREATE TYPE job_status AS ENUM ('pending','running','failed','completed');
CREATE TYPE audit_action AS ENUM (
  'workspace.create','workspace.update','workspace.delete',
  'membership.invite','membership.accept','membership.role_change','membership.remove',
  'list.create','list.update','list.delete',
  'column.create','column.update','column.delete',
  'item.create','item.update','item.delete',
  'relationship.create','relationship.delete','relationship.link','relationship.unlink',
  'comment.create','comment.delete',
  'file.attach','file.detach',
  'import.start','import.complete','export.start','export.complete'
);
```

## 4) Tables (Core)
### 4.1 users
Supabase Auth provides `auth.users`. Use `auth.users.id` as the canonical user id. Create a profile table for display info.

```sql
CREATE TABLE user_profiles (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### 4.2 workspaces
```sql
CREATE TABLE workspaces (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  created_by UUID REFERENCES auth.users(id),
  settings JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_workspaces_created_by ON workspaces(created_by);
```

### 4.3 workspace_memberships
```sql
CREATE TABLE workspace_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id),
  role workspace_role NOT NULL DEFAULT 'member',
  status invite_status NOT NULL DEFAULT 'invited',
  invite_token TEXT,
  invite_email CITEXT,
  invited_by UUID REFERENCES auth.users(id),
  invited_at TIMESTAMPTZ,
  accepted_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(workspace_id, user_id)
);
CREATE INDEX idx_wm_user ON workspace_memberships(user_id);
CREATE INDEX idx_wm_workspace_role ON workspace_memberships(workspace_id, role);
CREATE INDEX idx_wm_invite_token ON workspace_memberships(invite_token);
CREATE UNIQUE INDEX idx_wm_invite_email ON workspace_memberships(workspace_id, invite_email) WHERE user_id IS NULL AND status = 'invited';
```

### 4.4 lists
```sql
CREATE TABLE lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  position INT,
  created_by UUID REFERENCES auth.users(id),
  archived_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_lists_workspace ON lists(workspace_id);
CREATE INDEX idx_lists_workspace_archived ON lists(workspace_id, archived_at);
```

### 4.5 columns
```sql
CREATE TABLE columns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  list_id UUID NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
  key TEXT NOT NULL,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  position INT,
  is_required BOOLEAN NOT NULL DEFAULT false,
  is_unique BOOLEAN NOT NULL DEFAULT false,
  config JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(list_id, key)
);
CREATE INDEX idx_columns_list ON columns(list_id);
```

### 4.6 items
```sql
CREATE TABLE items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  list_id UUID NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
  title TEXT,
  values JSONB NOT NULL DEFAULT '{}',
  position INT,
  created_by UUID REFERENCES auth.users(id),
  updated_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  archived_at TIMESTAMPTZ
);
CREATE INDEX idx_items_list ON items(list_id);
CREATE INDEX idx_items_list_updated ON items(list_id, updated_at DESC);
CREATE INDEX idx_items_values_gin ON items USING GIN (values);
```

### 4.7 relationships
```sql
CREATE TABLE relationships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  list_id UUID NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  from_list_id UUID NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
  to_list_id UUID NOT NULL REFERENCES lists(id) ON DELETE CASCADE,
  cardinality TEXT NOT NULL DEFAULT 'many_to_many',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_relationships_list ON relationships(list_id);
CREATE INDEX idx_relationships_from_to ON relationships(from_list_id, to_list_id);
```

### 4.8 relationship_links
```sql
CREATE TABLE relationship_links (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  relationship_id UUID NOT NULL REFERENCES relationships(id) ON DELETE CASCADE,
  from_item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  to_item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(relationship_id, from_item_id, to_item_id)
);
CREATE INDEX idx_rl_relationship ON relationship_links(relationship_id);
CREATE INDEX idx_rl_from_item ON relationship_links(from_item_id);
CREATE INDEX idx_rl_to_item ON relationship_links(to_item_id);
```

### 4.9 files (metadata)
```sql
CREATE TABLE files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  storage_bucket TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  filename TEXT NOT NULL,
  content_type TEXT,
  size_bytes BIGINT,
  uploaded_by UUID REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(item_id, storage_path)
);
CREATE INDEX idx_files_item ON files(item_id);
```

### 4.10 comments
```sql
CREATE TABLE comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  item_id UUID NOT NULL REFERENCES items(id) ON DELETE CASCADE,
  author_id UUID REFERENCES auth.users(id),
  body TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  deleted_at TIMESTAMPTZ
);
CREATE INDEX idx_comments_item ON comments(item_id);
CREATE INDEX idx_comments_created ON comments(created_at DESC);
```

### 4.11 audit_logs
```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  actor_id UUID REFERENCES auth.users(id),
  action audit_action NOT NULL,
  entity_type TEXT,
  entity_id UUID,
  details JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_audit_workspace_time ON audit_logs(workspace_id, created_at DESC);
CREATE INDEX idx_audit_actor ON audit_logs(actor_id);
```

### 4.12 import_jobs / export_jobs
```sql
CREATE TABLE import_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  list_id UUID REFERENCES lists(id) ON DELETE SET NULL,
  created_by UUID REFERENCES auth.users(id),
  status job_status NOT NULL DEFAULT 'pending',
  source_type TEXT NOT NULL,
  source_path TEXT,
  stats JSONB NOT NULL DEFAULT '{}',
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_import_jobs_workspace ON import_jobs(workspace_id, created_at DESC);

CREATE TABLE export_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  list_id UUID REFERENCES lists(id) ON DELETE SET NULL,
  created_by UUID REFERENCES auth.users(id),
  status job_status NOT NULL DEFAULT 'pending',
  format TEXT NOT NULL,
  result_path TEXT,
  stats JSONB NOT NULL DEFAULT '{}',
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_export_jobs_workspace ON export_jobs(workspace_id, created_at DESC);
```

## 5) Constraints and Integrity
- Enforce unique membership per user + workspace.
- Ensure `columns.key` uniqueness per list.
- Enforce unique relationship links by `(relationship_id, from_item_id, to_item_id)`.
- Prevent removing or demoting the last owner in application logic; audit every role change.
- Soft delete where appropriate (`archived_at`, `deleted_at`) to preserve history.

## 6) Performance and Indexing
- Multi-tenant access patterns are indexed by `workspace_id` and `list_id`.
- JSONB GIN index supports ad-hoc value filters; for heavy filtering on a field, promote it to a generated column or add a functional index.
- Cursor pagination uses `(list_id, updated_at, id)` ordering for stable pages.
- Audit and job tables are time-indexed per workspace.

## 7) Optional Row Level Security (RLS)
RLS can be enabled for defense in depth. Policies should reference `auth.uid()` and `workspace_memberships`.

Example policy for lists:
```sql
ALTER TABLE lists ENABLE ROW LEVEL SECURITY;
CREATE POLICY lists_select ON lists
  FOR SELECT USING (
    EXISTS (
      SELECT 1 FROM workspace_memberships wm
      WHERE wm.workspace_id = lists.workspace_id
        AND wm.user_id = auth.uid()
        AND wm.status = 'accepted'
    )
  );
```

## 8) Data Lifecycle
- Soft delete for lists, items, comments to support recovery.
- Audit all destructive events with actor, timestamp, and entity details.
- Files are stored in Supabase Storage; DB stores metadata only.

## 9) Migration Order
1. Create enums.
2. Create workspaces and memberships.
3. Create lists, columns, items.
4. Create relationships and relationship_links.
5. Create files, comments, audit_logs.
6. Create import_jobs and export_jobs.

## 10) Alignment to Requirements
- Multi-workspace, role-based sharing: `workspaces`, `workspace_memberships`.
- Dynamic schema: `lists` + `columns` + `items.values` JSONB.
- Relationships across lists: `relationships` + `relationship_links`.
- Comments and audit log: `comments` + `audit_logs`.
- Import/export: `import_jobs`, `export_jobs`.
- Scale to 100k+ records: indexing, pagination, JSONB GIN.
