# Auto-Improve Worklog — bibletracker2
Branch: `auto-improve/2026-06-28`

---

### chore: remove unused generate_csrf import

**What:** Deleted `from flask_wtf.csrf import generate_csrf` from `app/readings/routes.py` line 10. The import had a misleading comment ("Needed for CSRF token in the template") but `generate_csrf` was never called in the file or any template.

**Why:** Dead import adds confusion and an unnecessary dependency on the internal `flask_wtf.csrf` API. Removing it keeps the import block honest.

**Files:** `app/readings/routes.py`

**Gate:**
- Baseline: `python3 -m py_compile app/**/*.py` → PASS
- Post-edit: same → PASS

**Commit:** 67e712a
