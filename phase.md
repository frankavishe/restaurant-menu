# Phases — Restaurant Menu Website (spec-kit workflow)

Tracks progress through the [spec-kit](https://github.com/github/spec-kit) spec-driven workflow for this project. Source requirements: `requirement.md`. Each phase below maps to a spec-kit skill (invoked as `/speckit-<name>` in Claude Code).

## Phase 0 — Environment setup ✅ done
- [x] Install `uv` and the `specify` CLI
- [x] Scaffold spec-kit into the project (`.specify/`, `.claude/skills/speckit-*`)
- [x] Initialize git, commit scaffold
- [x] Add GitHub remote (`frankavishe/restaurant-menu`), push `main`

## Phase 1 — Constitution ✅ done
**Skill:** `/speckit-constitution`
Establish the non-negotiable project principles so every later phase stays in scope:
- Stack is Python/Django, Django Templates, Django ORM, Django Admin, Bootstrap only
- No React/Vue/Angular, no Django REST Framework, no external APIs
- Content (categories, menu items) managed entirely through Django Admin
- Responsive UI required (Bootstrap grid/components)
- Clean, conventional Django project layout
**Output:** `.specify/memory/constitution.md`

## Phase 2 — Specify ✅ done
**Skill:** `/speckit-specify`
Turn `requirement.md` into a formal feature spec: user-facing behavior for Home, Menu (with category filter), Item detail, Contact page + form, Admin-managed Category/MenuItem/ContactMessage data, without prescribing implementation details yet.
**Output:** `spec.md` (new feature branch/dir per spec-kit convention)

## Phase 3 — Clarify (optional but recommended) ✅ done
**Skill:** `/speckit-clarify`
Resolve ambiguities spec-kit flags before planning. Session 2026-08-27 resolved:
- Menu item images: JPEG/PNG/WebP, max 5MB
- Prices: single currency, fixed 2 decimals, symbol shown (e.g. "$12.99")
- Contact message: max 2000 characters
- No "currently unavailable" state — staff delete/edit instead
- Featured dishes on Home: capped at 6 items
**Output:** clarifications encoded back into `spec.md` (uncommitted — commit alongside Phase 4 output)

## Phase 4 — Plan ✅ done
**Skill:** `/speckit-plan`
Produced the technical implementation plan:
- Django 5.1 / Python 3.12; `menu` app (Category/MenuItem, filtering, detail) + `pages` app (Home/Contact, ContactMessage)
- Model fields for `Category`, `MenuItem`, `ContactMessage` (incl. image validators, price as Decimal, message length cap)
- URL structure and views: `/`, `/menu/` (+`?category=slug`), `/menu/<pk>/`, `/contact/`
- Template inheritance (`base.html` with Bootstrap 5 navbar/footer)
- Static files: Bootstrap via CDN; placeholder image as static asset; media via `MEDIA_ROOT` in dev
- Admin registration summary for all three models
**Output:** `plan.md`, `research.md`, `data-model.md`, `contracts/web-routes.md`, `quickstart.md` (all uncommitted)

## Phase 5 — Tasks ✅ done
**Skill:** `/speckit-tasks`
Broke the plan into an ordered, dependency-aware task list organized by user story
(US1 Menu browse/filter → US2 Admin management → US3 Home → US4 Item detail → US5 Contact),
plus Setup and Foundational phases and a final Polish phase — 37 tasks (T001–T037) total.
**Output:** `specs/001-restaurant-menu-site/tasks.md` (uncommitted — commit alongside prior
phase outputs)

## Phase 6 — Quality gates (optional) ✅ done
- `/speckit-checklist` — skipped (optional; not requested)
- `/speckit-analyze` — cross-checked `constitution.md` / `spec.md` / `plan.md` / `tasks.md`; found 1 HIGH inconsistency (FR-014 vs. category-filter fallback behavior) and 2 MEDIUM underspecifications (contact-info format validation; Bootstrap-class coverage on content templates). All three fixed:
  - `spec.md` FR-014 narrowed to menu items only + new Edge Case documenting unmatched-category fallback
  - `tasks.md` T030 now calls for a `clean_contact_info` validator
  - `tasks.md` T017/T022/T025/T033 now call out Bootstrap grid/card/form classes explicitly

## Phase 7 — Implement ✅ done
**Skill:** `/speckit-implement`
Executed `tasks.md` end-to-end (T001–T037, all complete): Django project scaffold
(`restaurant_site`), `menu` app (`Category`/`MenuItem` models, validators, admin, views,
templates) and `pages` app (`ContactMessage` model, form, admin, views, templates), shared
`base.html`/Bootstrap layout, static/media wiring, migrations applied, `README.md` setup
instructions.
- Environment: Python 3.14.5 (only interpreter available) + Django 5.2.17 (satisfies
  `Django~=5.1`) + Pillow 12.3.0, isolated in a project-local `.venv`
- Verified via browser: Home (featured cap 6/7 confirmed), Menu (list + category filter +
  empty-state), Item detail, Contact (validation errors, valid submit → PRG redirect →
  confirmation, `ContactMessage` persisted, visible in Admin), Admin CRUD login
- `/menu/999999/` → 404 confirmed; `manage.py check` and `makemigrations --check` clean
- Fixed `Category` admin plural label ("Categorys" → "Categories") during verification
**Output:** full Django project at repo root (all files from `plan.md`'s Project Structure);
`tasks.md` checkboxes all `[X]`; uncommitted — commit alongside Phase 8 verification.

## Phase 8 — Converge & verify
**Skill:** `/speckit-converge`
- Assess the built codebase against spec/plan/tasks; append any remaining/missed work as new tasks
- Run migrations, start the dev server, manually walk through Home → Menu → filter → item detail → Contact → Admin CRUD
- Confirm responsive behavior (mobile/tablet/desktop breakpoints)
- Commit + push final implementation

---
**Status:** Phase 7 complete (full implementation done and manually verified, uncommitted). Next: Phase 8 (`/speckit-converge`).
