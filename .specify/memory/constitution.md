<!--
Sync Impact Report
- Version change: (unratified template) → 1.0.0
- Modified principles: n/a (initial ratification)
- Added principles: I. Django-Only, Server-Rendered Stack; II. Admin-Managed Content;
  III. Responsive Bootstrap UI; IV. Clean App Separation; V. Ship-Ready Deliverable
- Added sections: Technology Constraints; Development Workflow & Quality Gates; Governance
- Removed sections: none
- Templates requiring follow-up: none — plan/spec/tasks templates consume this file at
  runtime and contain no project-specific stack references to reconcile.
- Deferred placeholders: none
-->
# Restaurant Menu Website Constitution

## Core Principles

### I. Django-Only, Server-Rendered Stack (NON-NEGOTIABLE)
This project MUST be built with Python, Django, Django Templates, Django ORM, and Django
Admin. HTML, CSS, and Bootstrap render the UI server-side. React, Vue, Angular, Django REST
Framework, GraphQL, and calls to any external/third-party API MUST NOT be introduced.
Rationale: `requirement.md` explicitly scopes the tech stack and explicitly excludes these
options; keeping the stack minimal keeps the project dependency-free and easy to hand off.

### II. Admin-Managed Content
`Category` and `MenuItem` records MUST be fully creatable, editable, and deletable through
Django Admin without touching code. Every content model MUST be registered in `admin.py`
with sensible `list_display`/`list_filter`/`search_fields` so a non-developer can manage the
menu. Rationale: the restaurant owner is the primary content editor; `requirement.md` requires
Django Admin CRUD for categories and menu items.

### III. Responsive Bootstrap UI
All templates MUST use Bootstrap's grid and components and MUST render correctly at mobile,
tablet, and desktop breakpoints. A single `base.html` MUST define the shared navbar/footer
that every page extends. Rationale: `requirement.md` mandates a responsive design using
Bootstrap across the Home, Menu, Item Detail, and Contact pages.

### IV. Clean App Separation
The project MUST be organized into focused Django apps (e.g., a `menu` app owning
`Category`/`MenuItem`, filtering, and item detail; a `pages`/`core` app owning Home, Contact,
and `ContactMessage`) rather than one monolithic app. Each app MUST own its own models,
views, URLs, and templates directory. Rationale: keeps the codebase navigable and testable as
it grows, and matches conventional Django project structure.

### V. Ship-Ready Deliverable
Every change MUST leave the project in a runnable state: migrations committed alongside
model changes, no broken imports, and setup instructions (README) MUST stay current
(virtualenv, dependencies, `migrate`, `createsuperuser`, `runserver`). Rationale:
`requirement.md` lists a complete Django project, migrations, and setup instructions as
required deliverables — the project must always be handoff-ready.

## Technology Constraints

- **Backend**: Python + Django — Django Templates for rendering, Django ORM for persistence,
  Django Admin for content management.
- **Frontend**: HTML, CSS, Bootstrap (CDN or vendored static files) — no client-side
  framework and no JS build step (webpack/vite/npm) required to run the site.
- **Forbidden**: React, Vue, Angular, Django REST Framework, GraphQL, and any external or
  third-party API integration.
- **Data**: SQLite is acceptable for development; `requirement.md` does not mandate a
  specific production database.

## Development Workflow & Quality Gates

- Follow the spec-kit pipeline for this feature — constitution → specify → clarify (optional)
  → plan → tasks → implement → converge — as tracked in `phase.md`.
- Before `/speckit-implement` runs, `spec.md`, `plan.md`, and `tasks.md` MUST be reviewed
  against the Core Principles above.
- After implementation, manually verify: Admin CRUD works for `Category`/`MenuItem`; Home,
  Menu, Item Detail, and Contact pages render and are responsive; the contact form validates
  and persists a `ContactMessage`; `python manage.py migrate` runs clean from a fresh
  database.

## Governance

This constitution supersedes ad-hoc practices for this project. Any change to the Core
Principles requires updating this file with a version bump and a Sync Impact Report entry.
Proposals that violate Technology Constraints (e.g., introducing DRF or a JS framework)
MUST be rejected unless this constitution is amended first. Versioning follows semantic
versioning: MAJOR for backward-incompatible principle removals/redefinitions, MINOR for new
principles or materially expanded guidance, PATCH for clarifications and wording fixes. Use
`phase.md` for day-to-day workflow tracking; this document governs scope and technology
boundaries.

**Version**: 1.0.0 | **Ratified**: 2026-08-27 | **Last Amended**: 2026-08-27
