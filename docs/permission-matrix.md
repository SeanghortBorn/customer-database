# Permission Matrix

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## Roles
- owner, admin, editor, member
- viewer/commenter are future-phase roles

## Core Rules
- Only owners can promote to owner.
- Last owner cannot be removed or demoted.
- All permissions are enforced on the server.

## Actions by Role
| Action | Owner | Admin | Editor | Member |
| --- | --- | --- | --- | --- |
| Create workspace | Yes | No | No | No |
| Delete workspace | Yes | No | No | No |
| Invite members | Yes | Yes | No | No |
| Remove members | Yes | Yes | No | No |
| Change member roles | Yes | Yes (not to owner) | No | No |
| Create lists | Yes | Yes | Yes | No |
| Edit lists | Yes | Yes | Yes | No |
| Delete lists | Yes | Yes | Yes | No |
| Create items | Yes | Yes | Yes | Yes |
| Edit items | Yes | Yes | Yes | Yes |
| Delete items | Yes | Yes | Yes | No |
| Comment on items | Yes | Yes | Yes | Yes |
| View audit log | Yes | Yes | No | No |
