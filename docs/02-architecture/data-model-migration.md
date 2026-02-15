# Data Model and Migration Plan

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Core Entities
- users
- workspaces
- workspace_memberships
- lists
- columns
- items
- relationships
- relationship_links
- files
- comments
- audit_logs
- import_jobs
- export_jobs

## 2) Relationships
- user -> workspace_memberships (1:N)
- workspace -> lists (1:N)
- list -> columns (1:N)
- list -> items (1:N)
- list -> relationships (1:N)
- relationship -> relationship_links (1:N)
- workspace_membership -> workspace (N:1)

## 3) Key Constraints
- Unique workspace membership per user: UNIQUE(workspace_id, user_id)
- Roles enum: owner, admin, editor, member
- At least one owner per workspace (enforced in app logic)
- Column keys unique per list: UNIQUE(list_id, key)
- Relationship links unique per pair: UNIQUE(relationship_id, from_item_id, to_item_id)

## 4) Indexing
- workspace_memberships(user_id)
- workspace_memberships(workspace_id, role)
- lists(workspace_id)
- columns(list_id)
- items(list_id)
- items(list_id, updated_at)
- relationships(list_id)
- relationship_links(relationship_id, from_item_id)
- audit_logs(workspace_id, created_at)

## 5) Migration Plan
1. Create role enum and workspaces.
2. Create workspace_memberships with invite fields.
3. Create lists and columns.
4. Create items with JSONB values.
5. Add relationships and relationship_links.
6. Add files, comments, and audit logs.
7. Add import/export job tables.

## 6) Data Retention
- Soft delete for lists and items (optional).
- Log deletion events in audit_logs.
- Store file metadata in DB; blobs live in Supabase Storage.

## 7) Seed Data
- Create one workspace and owner user for dev.

## 8) Backfill Plan
- If migrating from existing data, map old lists to lists table.
- Import row data into items table.
