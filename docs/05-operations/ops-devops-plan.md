# Ops and DevOps Plan

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Goals
- Reliable, predictable deployments with fast rollback.
- Clear separation of environments with minimal config drift.
- Strong observability to detect issues before users do.
- Efficient developer workflow with guardrails and automation.

## 2) Environments
- dev: local + shared dev services for feature work.
- staging: production-like environment for integration and E2E.
- production: user-facing environment.
- Separate Supabase projects per environment.
- Render services per environment (gateway, domain services, workers, Redis).
- Vercel projects: staging + production; previews for PRs.

## 3) Source Control and Workflow
- Trunk-based with short-lived feature branches.
- PR required for all changes to main.
- Required checks: lint, unit, integration, type checks, and migrations dry-run.
- Conventional labels for releases and hotfixes.

## 4) CI/CD
- CI on every PR: build, lint, unit tests, integration tests, and security checks.
- CD to staging on merge to main.
- Manual promotion to production with a release checklist gate.
- Frontend: Vercel preview deploys on PR; promote on merge.
- Backend: Render deploys from main; workers deployed with services.
- Database migrations run as a dedicated step with preflight checks.

## 5) Configuration and Secrets
- Environment variables stored in Render and Vercel; no secrets in repo.
- Supabase service keys stored in Render only (never in frontend).
- Rotate service keys and invite token salts quarterly or on incident.
- Use separate credentials for background workers and API gateway.

## 6) Infrastructure as Code
- Use Terraform to define Render services, Vercel projects, and Supabase config.
- Store IaC in a separate `infra/` folder with a minimal README.
- Run `terraform plan` in CI for PRs; apply on merge with approvals.

## 7) Observability
- Stack: Sentry for application errors + OpenTelemetry for traces.
- Logs and metrics: use Render and Vercel managed logging/metrics initially.
- Structured JSON logs with request IDs and workspace IDs.
- Metrics: latency, error rate, queue depth, job duration, DB query time.
- Dashboards for API, worker, and DB health.
- Alerts: error rate, latency p95, queue backlog, worker failures, DB saturation.

## 8) Performance and Scaling
- Connection pooling for Neon.tech PostgreSQL (PgBouncer).
- Horizontal scaling for API gateway and workers.
- Rate limits at the gateway per user and per IP.
- Cache list schemas and workspace metadata where safe.
- Background jobs for imports/exports and large writes.

## 9) Backups and Recovery
- Supabase PITR enabled with 30 days retention.
- Daily logical exports for critical tables.
- Recovery targets: RPO 1 hour, RTO 4 hours.
- Weekly restore test to staging; record RPO/RTO results.
- Documented recovery runbook and owner.

## 10) Security
- TLS everywhere; HSTS on frontend.
- Least-privilege service roles and DB policies.
- SAST and dependency scanning in CI.
- Rate-limit invites and sensitive endpoints.
- Audit log retention aligned with compliance requirements.

## 11) Incident Response
- On-call rotation with escalation rules.
- Incident severity levels and response targets.
- Post-incident review within 5 business days.
- Runbooks: import/export failures, auth outages, DB saturation, queue backlog.

## 12) Release Checklist (Production)
- All CI checks green and staging smoke tests passed.
- Migration plan reviewed and tested on staging.
- Dashboards verified; alerts enabled.
- Backup/restore last run within 7 days.
- Rollback plan documented (code + migrations).
