# UX and UI Specification (Comprehensive)

Project: Customer Database System (Real Estate)
Date: 2026-02-15

## Document Status
- Last synced: 2026-02-15
- Consistency check: aligned across requirements, architecture, and data model
- Next review: update on major scope or schema change

## 1) Product Intent and UX Principles
This system is a modern, minimalist data workspace for real estate teams. The UI should feel like a purpose-built spreadsheet: fast, confident, and calm under heavy data entry.

Principles:
- Minimalist, not sparse: reduce chrome, elevate content density.
- One action, one surface: avoid stacked modals and layered dialogs.
- Predictable interactions: inline edit everywhere, with visible save states.
- Progressive disclosure: reveal power features only when needed.
- Trust and clarity: permissions are visible and explainable.

## 2) Information Architecture
Primary entities and surfaces:
- Workspaces: tenant boundary, access control.
- Lists: schema definitions and views.
- Items: rows in lists with inline editing.
- Relationships: link panels and lookup columns.
- Members and permissions: workspace-level management.
- Audit and comments: transparency and history.

Navigation hierarchy:
1) Global (top bar)
	- Workspace switcher
	- Global search
	- Notifications (optional phase 2)
	- User menu
2) Workspace (left sidebar)
	- Lists
	- Views (future: saved filters)
	- Members
	- Audit log
3) List (main)
	- Table view
	- Toolbar (view options, filters, import/export)
4) Item (side panel)
	- Details, relationships, files, comments

## 3) Core Screens
1) Auth
	- Sign in / Sign up with minimal fields
	- Social or magic link optional (future)
	- Focused, quiet layout with a single CTA

2) Workspace List
	- Cards or compact rows (density toggle)
	- Create workspace CTA top-right
	- Recent activity or last opened

3) Workspace Overview
	- Lists grid and quick actions
	- Search lists, create list
	- Empty state: create a list, import data

4) List Detail (Table)
	- Spreadsheet-like grid with inline edit
	- Column headers with type icons
	- Sticky header and first column
	- Row actions at right: open, duplicate, archive

5) Item Detail (Side Panel)
	- Title and key fields
	- Related records
	- Files and comments
	- Audit trail snippet

6) Members and Sharing
	- Role table with inline role change
	- Invite form with email + role
	- Permission rules visible with tooltips

7) Import/Export
	- Multi-step import wizard with mapping
	- Progress state and error summary
	- Export format selection with job status

8) Audit Log
	- Filter by actor, action, list
	- Infinite scroll or cursor paging

## 4) Key Flows
### 4.1 Create Workspace
1. Click create workspace.
2. Name and description.
3. Create and land in workspace overview.
4. Offer next actions: create list, import data, invite members.

### 4.2 Invite Member and Set Role
1. Open Members.
2. Input email and role.
3. Confirm invite; show pending state.
4. On accept, status becomes active; audit log entry created.

### 4.3 Create List and Columns
1. Create list name.
2. Starter schema template (optional) or blank.
3. Add columns with type and validations.

### 4.4 Add and Edit Items
1. Inline edit cells with auto-save.
2. Batch paste support.
3. Multi-select for bulk edit.

### 4.5 Link Records Across Lists
1. Add relationship column.
2. Search and select items from linked list.
3. Create new related item inline if permitted.

### 4.6 Import Data
1. Select file type (CSV/Excel/JSON).
2. Map columns.
3. Validation preview with errors.
4. Start import (background job).
5. Status and summary on completion.

### 4.7 Export Data
1. Choose list and format.
2. Background job with notification.
3. Download from export history.

## 5) Design System
### 5.1 Typography
- Primary: a geometric sans for clean data density.
- Secondary: a neutral serif for subtle emphasis (section headers).

### 5.2 Color
- Base: warm white and charcoal.
- Accent: muted teal for primary actions.
- Status: green (success), amber (warning), red (error), blue (info).

### 5.3 Spacing and Density
- 4px grid.
- Table density toggle: compact, standard.
- Input heights: 32px compact, 40px standard.

### 5.4 Elevation and Borders
- Minimal elevation; use thin borders and soft shadows for panels.
- Keep modals rare; prefer side panels and inline.

### 5.5 Motion
- Subtle fade and slide for side panel.
- Row highlight on update.
- Progress bars for import/export jobs.

## 6) Core Components
### 6.1 Data Table
- Sticky header
- Column resize and reorder
- Inline edit with validation
- Column type icon + name
- Row selection checkbox

### 6.2 Column Builder
- Type selector
- Required, unique toggles
- Type-specific config (select options, formats)

### 6.3 Search and Filters
- Global search (across lists)
- List-level filter bar
- Saved filters (future)

### 6.4 Relationship Picker
- Search within linked list
- Multi-select for many-to-many
- Create related item inline if allowed

### 6.5 File Upload
- Drag and drop
- Progress indicator
- Preview for images and PDFs

### 6.6 Comments
- Inline thread view
- Mentions (future)

### 6.7 Role Manager
- Role dropdown with restrictions
- Inline warnings for last owner rule

## 7) Permissions and UI Behavior
- Hide actions users cannot perform, but show reasons where relevant.
- On forbidden action attempts, show an inline banner with the rule.
- Owner-only actions have a lock icon and tooltip.

Permission rules to reflect in UI:
- Only owner can promote to owner.
- Last owner cannot be removed or demoted.
- Members can add items but cannot delete lists.

## 8) Empty States
- Workspace empty: "Create your first list" and "Import data".
- List empty: "Add your first row" and "Paste from clipboard".
- Relationships empty: "Link records".
- Audit empty: "No activity yet".

## 9) Error and Validation
- Inline cell errors for validation failures.
- Form-level summary on save errors.
- Import mapping errors grouped by column.
- Network failures show retry option.

## 10) Accessibility
- Keyboard navigation for table (arrows, enter to edit, esc to cancel).
- Focus visible for all interactive elements.
- Color contrast meets WCAG AA.
- Screen reader labels for role and status badges.

## 11) Responsive Behavior
- Desktop: full table with sidebar.
- Tablet: collapsible sidebar and sticky toolbar.
- Mobile: list view and item detail drawer; quick edit in vertical cards.

## 12) Content and Microcopy
- Use clear verbs: Create, Add, Invite, Export.
- Confirm destructive actions with concise language.
- Error copy includes next step and permission hints.

## 13) Performance UX
- Skeleton rows during load.
- Virtualized table for large datasets.
- Optimistic updates for inline edits.

## 14) Analytics and Telemetry (optional)
- Track time to create list and first row.
- Invite acceptance rate.
- Import success rate and average duration.

## 15) UX QA Checklist
- All permissions tested across roles.
- No blocked actions without explanation.
- Table keyboard navigation complete.
- Import/export flow clear and recoverable.
- Mobile list and detail usable without horizontal scroll.

## 16) Visual Style Guide and Tokens
This section provides concrete tokens for implementation and design tooling.

### 16.1 Typography
- Primary: "Sora" (headings, UI labels)
- Secondary: "IBM Plex Sans" (data table, body)
- Numeric: "IBM Plex Mono" (IDs, timestamps)
- Scale (px): 12, 13, 14, 16, 18, 22, 28, 36
- Line height: 1.4 for body, 1.2 for headings

### 16.2 Color Tokens
Base:
- --color-bg: #F7F5F1
- --color-surface: #FFFFFF
- --color-ink: #1F2527
- --color-ink-muted: #5C666A

Accent:
- --color-accent: #2A7F78
- --color-accent-hover: #21645E
- --color-accent-soft: #DCEFEA

Status:
- --color-success: #2E7D32
- --color-warning: #C07A00
- --color-error: #C62828
- --color-info: #1E5FA6

Borders and focus:
- --color-border: #E5E1DA
- --color-border-strong: #C9C3B8
- --color-focus: #1E5FA6

### 16.3 Spacing and Radius
- Spacing scale (px): 4, 8, 12, 16, 20, 24, 32, 40
- Radius: 6 (inputs), 10 (panels), 14 (cards)
- Shadow: 0 2px 8px rgba(0,0,0,0.08)

### 16.4 Table Density Tokens
- --row-height-compact: 32px
- --row-height-standard: 40px
- --row-height-comfy: 48px

## 17) Wireframes (Text-Only)
These are layout blueprints for quick alignment before hi-fi design.

### 17.1 Workspace List
------------------------------------------------------------
Top Bar: [Workspace Switcher] [Global Search] [User Menu]
------------------------------------------------------------
Workspace List
	[Create Workspace]
	--------------------------------------------------------
	| Workspace Name | Members | Last Opened | Role        |
	--------------------------------------------------------
	| Acme Realty    | 12      | Today       | Owner       |
	| North Region   | 5       | Yesterday   | Admin       |
	--------------------------------------------------------

### 17.2 Workspace Overview
------------------------------------------------------------
Sidebar: Lists / Members / Audit
------------------------------------------------------------
Main
	[Create List] [Import]
	--------------------------------------------------------
	| List Cards / Rows with quick actions                 |
	--------------------------------------------------------

### 17.3 List Table View
------------------------------------------------------------
Toolbar: [List Name] [Filter] [Sort] [View] [Import/Export]
------------------------------------------------------------
Table
	| Name | Type | Status | Owner | Updated | ... |
	--------------------------------------------------------
	| ... inline editable rows ...                         |
------------------------------------------------------------
Right Side Panel (Item Detail)
	Title, fields, relationships, files, comments

### 17.4 Members and Roles
------------------------------------------------------------
Members
	Invite: [Email] [Role] [Send]
	--------------------------------------------------------
	| Name | Email | Role | Status | Actions              |
	--------------------------------------------------------
	| ...                                                 |
------------------------------------------------------------

### 17.5 Import Flow
------------------------------------------------------------
Step 1: Upload
Step 2: Map Columns
Step 3: Validate
Step 4: Import (job status)
------------------------------------------------------------

## 18) UI Copy Bank
Use these strings for consistent, minimal copy.

### 18.1 Workspace
- "Create workspace"
- "Workspace name"
- "Invite members"
- "You are the last owner. Add another owner before leaving."

### 18.2 Lists and Items
- "Create list"
- "Add column"
- "Add row"
- "Paste to add rows"
- "No rows yet. Add your first row."

### 18.3 Permissions
- "You do not have permission to do that."
- "Only owners can promote to owner."
- "This action is restricted by workspace role."

### 18.4 Import and Export
- "Import file"
- "Map columns"
- "Review errors"
- "Import started. We will notify you when it is done."
- "Export ready to download"

### 18.5 Errors and Empty States
- "We could not save your changes. Try again."
- "No activity yet"
- "Nothing to show here"
