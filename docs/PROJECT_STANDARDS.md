# Project Standards & Guidelines

**Last Updated:** February 15, 2026  
**Purpose:** Define standards for file organization, cleanup, and maintenance

---

## 📁 File Organization Structure

### Folder Hierarchy

```
docs/
├── 00-getting-started/      # Quick start guides and roadmaps
├── 01-planning/             # Product requirements and project plans
├── 02-architecture/         # System architecture and database design
├── 03-specifications/       # API, UX/UI, and permission specs
├── 04-development/          # Development guides and test plans
├── 05-operations/           # Operations, DevOps, and compliance
├── 99-history/              # Historical changes and modifications
└── PROJECT_STANDARDS.md     # This file
```

### Folder Purposes

| Folder | Purpose | File Types |
|--------|---------|------------|
| **00-getting-started** | Entry point for new developers | ACTION_PLAN, QUICK_START, IMPLEMENTATION_ROADMAP |
| **01-planning** | Product vision and requirements | PRD, inception reports, delivery plans |
| **02-architecture** | Technical design and data models | Architecture, database design, migrations |
| **03-specifications** | Detailed specifications | API specs, UX/UI specs, permissions |
| **04-development** | Development workflows | Feature breakdown, test plans |
| **05-operations** | Production operations | DevOps plans, legal compliance |
| **99-history** | Track all modifications | Changelogs, deprecated files, version history |

---

## 🧹 Cleanup Standards

### When to Clean Up

Perform cleanup:
- ✅ After completing a major feature
- ✅ Before creating a new release
- ✅ When files become outdated
- ✅ When merging duplicate content
- ✅ Weekly maintenance (recommended)

### Cleanup Checklist

#### 1. Identify Candidates for Cleanup

**Outdated Files:**
- [ ] Files referencing deprecated features
- [ ] Old architectural decisions that changed
- [ ] Superseded documentation

**Duplicate Files:**
- [ ] Files with overlapping content (>70% similarity)
- [ ] Multiple versions of the same document
- [ ] Redundant guides or plans

**Unused Files:**
- [ ] Files not referenced anywhere
- [ ] Temporary working documents
- [ ] Draft files marked "WIP" for >30 days

#### 2. Archive Before Deletion

**CRITICAL:** Never permanently delete. Always archive to `99-history/`.

```bash
# Archive process:
1. Move file to /docs/99-history/
2. Add date suffix: filename_YYYY-MM-DD.md
3. Update CHANGELOG.md with reason for archival
4. Remove from main documentation links
```

#### 3. Merge Duplicate Content

When files have similar content:

1. **Identify primary file** (most complete, most recent)
2. **Extract unique content** from duplicates
3. **Merge into primary file** with proper sections
4. **Archive old files** to 99-history/
5. **Update all references** to point to merged file

#### 4. Update References

After cleanup:
- [ ] Update README.md if structure changed
- [ ] Update all internal links to moved/merged files
- [ ] Update INDEX.md files in each folder
- [ ] Test all links work correctly

---

## 📝 Documentation Standards

### File Naming Conventions

**Format:** `kebab-case-descriptive-name.md`

**Examples:**
- ✅ `quick-start.md`
- ✅ `api-specification.md`
- ✅ `database-design.md`
- ❌ `QuickStart.md` (wrong case)
- ❌ `api_spec.md` (use hyphens, not underscores)
- ❌ `doc1.md` (not descriptive)

### File Headers

Every documentation file must include:

```markdown
# Document Title

**Project:** Customer Database System  
**Last Updated:** YYYY-MM-DD  
**Status:** Active | Deprecated | Archived  
**Owner:** [Team/Person responsible]

## Document Status
- Last synced: YYYY-MM-DD
- Next review: [date or trigger]
- Related docs: [list]

[Content here]
```

### Version Control

**Status Tags:**
- `Active` - Current, maintained documentation
- `Deprecated` - Outdated but kept for reference
- `Archived` - Historical, moved to 99-history/
- `Draft` - Work in progress, not official
- `Review` - Pending review/approval

---

## 🔄 Modification Tracking

### CHANGELOG.md Format

All changes must be logged in `docs/99-history/CHANGELOG.md`:

```markdown
## [Date] - [Type of Change]

### Added
- New file: [filename] - [purpose]

### Modified
- Updated [filename]: [what changed and why]

### Deprecated
- Marked [filename] as deprecated: [reason]

### Archived
- Moved [filename] to history: [reason]

### Merged
- Combined [file1] + [file2] → [new file]: [reason]
```

### Change Types

- **Added:** New documentation created
- **Modified:** Existing file updated
- **Deprecated:** File marked outdated but kept
- **Archived:** File moved to 99-history/
- **Merged:** Multiple files consolidated
- **Removed:** File reference removed (after archival)

---

## 🤖 AI Agent Guidelines

### For AI Assistants Working on This Project

When modifying this project:

#### Before Making Changes

1. **Read this file** to understand structure
2. **Check CHANGELOG.md** for recent changes
3. **Identify file location** using folder purposes above
4. **Verify no duplicates** exist elsewhere

#### During Changes

1. **Update existing files** rather than creating new ones when possible
2. **Follow naming conventions** strictly
3. **Include proper headers** in all new files
4. **Update INDEX.md** if adding/moving files

#### After Changes

1. **Log change** in CHANGELOG.md with date and description
2. **Update README.md** if structure changed
3. **Archive old versions** if replacing files
4. **Verify all links** still work
5. **Run cleanup check** using checklist above

#### File Creation Decision Tree

```
Need to add content?
├─ Does similar file exist?
│  ├─ YES → Update existing file
│  └─ NO → Continue
├─ Is content <500 words?
│  ├─ YES → Add to existing related file
│  └─ NO → Continue
└─ Create new file with proper naming + header
```

---

## 🔍 Cleanup Commands

### Automated Checks

```bash
# Find files not modified in 90 days
find docs/ -name "*.md" -mtime +90 -not -path "*/99-history/*"

# Find duplicate filenames
find docs/ -name "*.md" -not -path "*/99-history/*" | \
  rev | cut -d'/' -f1 | rev | sort | uniq -d

# Find files not referenced in any other file
# (Manual review recommended)
for file in docs/**/*.md; do
  name=$(basename "$file" .md)
  count=$(grep -r "$name" docs/ --exclude-dir=99-history | wc -l)
  if [ $count -eq 1 ]; then
    echo "Possibly unused: $file"
  fi
done

# Verify all markdown links work
# (Use a tool like markdown-link-check)
npx markdown-link-check README.md
npx markdown-link-check docs/**/*.md
```

### Manual Review Schedule

- **Daily:** Check for WIP files older than 3 days
- **Weekly:** Review 99-history/ size (should be <10 files)
- **Monthly:** Full cleanup audit using checklist above
- **Quarterly:** Review and merge related documentation

---

## 📊 Quality Metrics

### Documentation Health Indicators

**Healthy Project:**
- No files >180 days without update (except archived)
- No duplicate files outside 99-history/
- All links functional (0 broken links)
- <5 files marked "Draft" or "WIP"
- CHANGELOG.md updated within last 7 days

**Needs Attention:**
- >10 files not updated in 90 days
- >3 files marked "Deprecated"
- >5 broken links
- CHANGELOG.md not updated in 30 days

---

## 🎯 Best Practices

### DO

✅ Update existing files rather than creating duplicates  
✅ Use descriptive, searchable file names  
✅ Include proper headers with dates and status  
✅ Log all changes in CHANGELOG.md  
✅ Archive before deleting  
✅ Keep folder structure flat (max 2 levels deep)  
✅ Reference other docs with relative links  
✅ Review and cleanup weekly  

### DON'T

❌ Create files with vague names (doc1.md, notes.md)  
❌ Leave WIP files uncommitted for >7 days  
❌ Delete files without archiving  
❌ Duplicate content across multiple files  
❌ Skip updating CHANGELOG.md  
❌ Create deep nested folder structures  
❌ Use absolute paths in internal links  
❌ Leave broken links in documentation  

---

## 🔄 Migration Process

### When Reorganizing Existing Files

1. **Create new structure** first (folders)
2. **Copy (don't move)** files to new locations
3. **Update all references** to new paths
4. **Test all links** work correctly
5. **Archive old files** (don't delete)
6. **Update README.md** with new structure
7. **Log migration** in CHANGELOG.md
8. **Keep old structure** for 30 days before cleanup

---

## 📚 Quick Reference

### Common Tasks

| Task | Command/Action |
|------|----------------|
| Create new doc | Use template, proper naming, log in CHANGELOG |
| Update existing | Edit file, update "Last Updated" date |
| Archive file | Move to 99-history/, add date suffix, log change |
| Find outdated | Run: `find docs/ -name "*.md" -mtime +90` |
| Check links | Run: `npx markdown-link-check docs/**/*.md` |
| Review cleanup | Use "Cleanup Checklist" above quarterly |

### File Templates

Located in `docs/99-history/templates/` (create as needed):
- `document-template.md` - Standard doc header
- `api-endpoint-template.md` - API documentation
- `feature-spec-template.md` - Feature specifications

---

## 🎓 Training Resources

For new team members:
1. Read this document first
2. Review README.md for project overview
3. Explore folder structure in order (00 → 05)
4. Check CHANGELOG.md for recent changes
5. Follow AI Agent Guidelines above

---

## 📞 Questions?

If this document doesn't answer your question:
1. Check related documentation in folder INDEX.md files
2. Review CHANGELOG.md for similar past situations
3. Create a GitHub Issue with label `documentation`
4. Update this file with answer once resolved

---

**Remember:** Clean documentation = Happy developers = Better product! 🚀
