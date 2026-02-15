# API Specification (Draft)

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Conventions
- Base path: /api/v1
- Auth: JWT Authentication JWT (Bearer token)
- Pagination: limit, cursor
- Errors: JSON with code and message
- Async jobs: POST starts job, GET checks status

## 2) Workspace Endpoints
- POST /workspaces
- GET /workspaces
- GET /workspaces/:id
- PATCH /workspaces/:id
- DELETE /workspaces/:id

## 3) Membership Endpoints
- POST /workspaces/:id/invite
- GET /workspaces/:id/members
- POST /workspaces/:id/members/:memberId/role
- DELETE /workspaces/:id/members/:memberId
- POST /workspaces/:id/invites/:token/accept

## 4) List Endpoints
- POST /workspaces/:id/lists
- GET /workspaces/:id/lists
- GET /lists/:listId
- PATCH /lists/:listId
- DELETE /lists/:listId

## 5) Column Endpoints
- POST /lists/:listId/columns
- GET /lists/:listId/columns
- PATCH /columns/:columnId
- DELETE /columns/:columnId

## 6) Item Endpoints
- POST /lists/:listId/items
- GET /lists/:listId/items
- PATCH /items/:itemId
- DELETE /items/:itemId

## 7) Relationship Endpoints
- POST /lists/:listId/relationships
- GET /lists/:listId/relationships
- POST /relationships/:relationshipId/links
- DELETE /relationships/:relationshipId/links/:linkId

## 8) Import/Export Endpoints
- POST /lists/:listId/imports
- GET /imports/:importId
- POST /lists/:listId/exports
- GET /exports/:exportId

## 9) Files
- POST /files/presign
- POST /items/:itemId/files
- DELETE /items/:itemId/files/:fileId

## 10) Comments and Audit
- POST /items/:itemId/comments
- GET /items/:itemId/comments
- GET /workspaces/:id/audit

## 11) Error Codes
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict (duplicate, invalid role change)
- 422 Validation Error
- 429 Too Many Requests

## 12) Role Rules
- Only owners can promote to owner.
- Do not remove or demote the last owner.
