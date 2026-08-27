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

## Phase 2 — Specify
**Skill:** `/speckit-specify`
Turn `requirement.md` into a formal feature spec: user-facing behavior for Home, Menu (with category filter), Item detail, Contact page + form, Admin-managed Category/MenuItem/ContactMessage data, without prescribing implementation details yet.
**Output:** `spec.md` (new feature branch/dir per spec-kit convention)

## Phase 3 — Clarify (optional but recommended)
**Skill:** `/speckit-clarify`
Resolve ambiguities spec-kit flags before planning, e.g.:
- Menu item images: uploaded files vs. URL field?
- Contact form: saved to DB only, or also emailed?
- Featured dishes on Home: manually flagged field, or auto-picked?
- Category filter: query param page reload, or client-side?
**Output:** clarifications encoded back into `spec.md`

## Phase 4 — Plan
**Skill:** `/speckit-plan`
Produce the technical implementation plan:
- Django project + app layout (e.g. `menu` app for Category/MenuItem, `pages`/`core` app for Home/Contact)
- Model fields for `Category`, `MenuItem`, `ContactMessage`
- URL structure and views (function- or class-based)
- Template inheritance (`base.html` with navbar/footer via Bootstrap)
- Static files strategy (Bootstrap via CDN vs. vendored) and media handling for images
- Admin registration (`admin.py` customizations for list display/filtering)
**Output:** `plan.md` + supporting design docs

## Phase 5 — Tasks
**Skill:** `/speckit-tasks`
Break the plan into an ordered, dependency-aware task list, roughly:
1. Project scaffold (`django-admin startproject`, apps)
2. Models + migrations
3. Admin registration
4. Views + URLs (Home, Menu list, Category filter, Item detail, Contact)
5. Templates + Bootstrap layout (base, navbar, footer, pages)
6. Contact form (Django form + validation + save)
7. Static/media configuration
8. Responsive polish + manual QA pass
**Output:** `tasks.md`

## Phase 6 — Quality gates (optional)
- `/speckit-checklist` — generate a requirements-completeness checklist
- `/speckit-analyze` — cross-check `constitution.md` / `spec.md` / `plan.md` / `tasks.md` for consistency gaps before writing code

## Phase 7 — Implement
**Skill:** `/speckit-implement`
Execute `tasks.md` end-to-end: generates the actual Django project, models, admin, views, templates, static/media wiring, migrations, and setup instructions per the Deliverables in `requirement.md`.
**Gate:** only run after reviewing `spec.md` / `plan.md` / `tasks.md`.

## Phase 8 — Converge & verify
**Skill:** `/speckit-converge`
- Assess the built codebase against spec/plan/tasks; append any remaining/missed work as new tasks
- Run migrations, start the dev server, manually walk through Home → Menu → filter → item detail → Contact → Admin CRUD
- Confirm responsive behavior (mobile/tablet/desktop breakpoints)
- Commit + push final implementation

---
**Status:** Phase 1 complete. Next: Phase 2 (`/speckit-specify`).
