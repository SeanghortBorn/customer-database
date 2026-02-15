# Specifications - Index

**Folder:** `03-specifications/`  
**Purpose:** Detailed API, UX/UI, and permission specifications

---

## 📚 Documents in This Folder

### [api-spec.md](./api-spec.md)
**API Endpoint Specifications**
- API conventions and auth
- All endpoints organized by domain:
  - Workspace endpoints
  - Membership and invite endpoints
  - List and column endpoints
  - Item endpoints
  - Relationship endpoints
  - Import/Export endpoints
- Error codes and role rules
- **Read this if:** You're implementing backend API endpoints

### [ux-ui-spec.md](./ux-ui-spec.md)
**UX and UI Design System**
- Product intent and UX principles
- Information architecture
- Core screens and flows
- Design system (typography, color, spacing)
- Core components (table, forms, pickers)
- Permissions reflected in UI
- **Read this if:** You're implementing frontend components

### [permission-matrix.md](./permission-matrix.md)
**Role-Based Access Control Rules**
- Role definitions (Owner, Admin, Editor, Member)
- Core permission rules
- Actions by role (matrix table)
- "Last owner" protection rule
- **Read this if:** You need to implement permission checks

---

## 🎯 Key Specifications

### API Base Path
`/api/v1`

### Authentication
- Supabase Auth JWT (Bearer token)
- Gateway validates JWT and attaches user context
- All endpoints require authentication

### Core Permission Rules
- Only owners can promote to owner
- Last owner cannot be removed or demoted
- All permissions enforced server-side

### UX Principles
- Minimalist, not sparse
- One action, one surface (avoid stacked modals)
- Predictable interactions (inline edit everywhere)
- Progressive disclosure (reveal power features when needed)
- Trust and clarity (permissions visible and explainable)

---

## 🔗 Related Documentation

- **Architecture:** See [02-architecture](../02-architecture/) for system design
- **Development:** See [04-development](../04-development/) for feature implementation
- **Planning:** See [01-planning](../01-planning/) for product context

---

**Last Updated:** February 15, 2026
