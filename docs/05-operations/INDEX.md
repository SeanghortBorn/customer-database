# Operations - Index

**Folder:** `05-operations/`  
**Purpose:** Operations, DevOps, deployment, and compliance

---

## 📚 Documents in This Folder

### [ops-devops-plan.md](./ops-devops-plan.md)
**Operations and DevOps Strategy**
- Deployment environments (dev, staging, production)
- CI/CD pipeline (GitHub Actions)
- Configuration and secrets management
- Infrastructure as Code (Terraform)
- Observability (logs, metrics, alerts)
- Performance and scaling
- Backups and recovery
- Security practices
- Incident response
- **Read this if:** You're setting up deployment or production operations

### [legal-compliance.md](./legal-compliance.md)
**Legal and Compliance Requirements**
- Privacy and data handling
- Security baseline
- Compliance targets (GDPR/CCPA)
- Terms and policies needed
- Subprocessor documentation
- **Read this if:** You need to understand legal/compliance requirements

---

## 🎯 Key Operations Info

### Environments
- **Development:** Local (Docker Compose)
- **Staging:** Auto-deploy from `main` branch
- **Production:** Manual promotion with checklist

### CI/CD Pipeline
- **PR:** Lint → Tests → Build check
- **Main merge:** Auto-deploy to staging
- **Production:** Manual deploy with approval

### Observability Stack
- **Errors:** Sentry
- **Logs:** Structured JSON with request IDs
- **Metrics:** Render/Vercel dashboards
- **Alerts:** Error rate, latency, queue depth

### Backup & Recovery
- **PITR:** 30 days retention (Supabase)
- **RPO:** 1 hour (Recovery Point Objective)
- **RTO:** 4 hours (Recovery Time Objective)
- **Testing:** Weekly restore test to staging

---

## 🔐 Security Checklist

- [ ] TLS everywhere, HSTS enabled
- [ ] Least-privilege service roles
- [ ] SAST and dependency scanning in CI
- [ ] Rate-limiting on sensitive endpoints
- [ ] Audit log retention policy
- [ ] Quarterly credential rotation

---

## 📋 Release Checklist

Before deploying to production:

- [ ] All CI checks green
- [ ] Staging smoke tests passed
- [ ] Migration tested on staging
- [ ] Dashboards verified, alerts enabled
- [ ] Backup tested within 7 days
- [ ] Rollback plan documented

---

## 🔗 Related Documentation

- **Architecture:** See [02-architecture](../02-architecture/) for system design
- **Development:** See [04-development](../04-development/) for testing strategy
- **Getting Started:** See [00-getting-started](../00-getting-started/) for setup

---

**Last Updated:** February 15, 2026
