# Development Index

**Folder:** `04-development/`  
**Purpose:** Development workflows, feature tracking, and testing

---

## 📚 Documents in This Folder

### [FEATURE_BREAKDOWN.md](./FEATURE_BREAKDOWN.md)
**Feature Priorities and Release Tracking**
- All features broken into deployable slices
- Priority levels (P0/P1/P2/P3)
- Effort estimates for each feature
- Visual architecture diagram
- Progress tracker with checkboxes
- MVP vs post-MVP features
- **Read this if:** You want to track development progress and priorities

### [test-plan.md](./test-plan.md)
**Testing Strategy and Coverage**
- Test types (unit, integration, E2E, load, accessibility)
- Coverage goals
- Test data and environments
- Entry and exit criteria
- **Read this if:** You're writing tests or setting up CI

### [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)
**Implementation Status**
- Current progress on each feature
- Dependencies and blockers
- Milestones and deadlines
- **Read this if:** You want to track implementation progress and dependencies

---

## 🎯 Development Approach

### Micro-Development Strategy
- **Vertical slices:** Each feature is end-to-end (DB → API → UI)
- **Independently deployable:** No broken intermediate states
- **Fully tested:** Comprehensive test coverage
- **Production-ready:** Each slice ships to production

### Release Cadence
- **Sprint length:** 1 week
- **Releases:** 1-2 features per week
- **Environments:** dev → staging (auto) → production (manual)

### Testing Coverage Goals
- Unit tests for role checks and validations
- Integration tests for all API endpoints
- E2E tests for critical user flows
- Load tests for 100k-record workspaces
- Accessibility tests (WCAG AA) for core screens

---

## 📊 Feature Status Tracking

Track feature completion in [FEATURE_BREAKDOWN.md](./FEATURE_BREAKDOWN.md):

- 🔴 **Todo:** Not started
- 🟡 **In Progress:** Currently being developed
- 🟢 **Completed:** Tested and deployed

### MVP Features (Phase 1-4)
- All P0 (must-have) features
- Most P1 (should-have) features
- Target: 8-10 weeks

### Post-MVP Features
- P2 (nice-to-have) features
- P3 (future) enhancements

---

## 🔗 Related Documentation

- **Getting Started:** See [00-getting-started](../00-getting-started/) for implementation guides
- **Specifications:** See [03-specifications](../03-specifications/) for API and UX specs
- **Operations:** See [05-operations](../05-operations/) for deployment

---

**Last Updated:** February 15, 2026
