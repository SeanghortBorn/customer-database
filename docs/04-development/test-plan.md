# Test Plan

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Test Types
- Unit tests for role rules and validations
- Integration tests for API endpoints
- End-to-end tests for core flows
- Load tests for 100k-record workspaces
- Accessibility tests for core screens (WCAG AA)
- UX QA for table editing, permissions, and import flows
- Backup/restore drill tests (staging)
- Security checks in CI (SAST and dependency scan)

## 2) Coverage Goals
- Role checks for all write endpoints
- Invite flow: send, accept, revoke
- Last owner protection
- Import/export basic flows
- JWT verification at API Gateway
- Background worker retries and failure handling
- File upload and download flows (Object Storage)
- Rate limit behavior (429)
- Keyboard navigation for table editing
- Screen reader labels for role/status and inputs
- Error and empty state messaging clarity
- Observability: request IDs present in logs and trace propagation
- Backup restore success within target RPO/RTO

## 3) Test Data
- Seed users with different roles
- Sample workspaces with 10k items

## 4) Environments
- CI: run unit and integration tests
- Staging: run E2E nightly
- Render staging mirrors production service topology

## 5) Entry and Exit Criteria
- All tests pass in CI
- No P1 bugs in release candidate
- Performance targets met
