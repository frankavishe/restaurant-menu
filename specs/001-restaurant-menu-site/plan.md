# Implementation Plan: Restaurant Menu Website

**Branch**: `001-restaurant-menu-site` | **Date**: 2026-08-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-restaurant-menu-site/spec.md`

## Summary

A responsive, server-rendered Django site presenting a restaurant's menu: a Home page
(info + featured dishes), a filterable Menu page, per-item detail pages, a Contact page with
a persisted contact form, and full Category/MenuItem/ContactMessage management via Django
Admin. Two focused apps (`menu`, `pages`) share a single Bootstrap-based `base.html`; no JS
framework, no DRF, no external APIs — all filtering and form handling is standard Django
request/response with template rendering.

## Technical Context

**Language/Version**: Python 3.12, Django 5.1 (LTS-track latest stable)

**Primary Dependencies**: Django, Pillow (required by `ImageField` for image validation/
processing). No DRF, no JS framework, no build tooling.

**Storage**: SQLite (`db.sqlite3`) via Django ORM — sufficient for dev/handoff per
constitution; no specific production DB mandated.

**Testing**: Django's built-in test framework (`django.test.TestCase` + `Client`), run via
`python manage.py test`. Covers model validation, view responses, category filtering, and
contact form validation/persistence.

**Target Platform**: Cross-platform WSGI app; run locally via `manage.py runserver` for dev/
handoff. No OS-specific dependencies.

**Project Type**: Web application — single Django project, multiple apps, server-rendered
templates (no separate frontend).

**Performance Goals**: No hard throughput target; standard server-rendered page loads (SC-002
requires category filtering to feel like a normal page navigation, not a special perf budget).

**Constraints**: No React/Vue/Angular, no DRF/GraphQL, no external/third-party API calls; all
UI responsive via Bootstrap grid/components; image uploads restricted to JPEG/PNG/WebP ≤ 5MB
(FR-009a); contact message body capped at 2000 characters (FR-006); prices in a single
currency, fixed 2 decimals (FR-002).

**Scale/Scope**: Single restaurant, single language, single currency. Expected data volume:
tens of categories, low hundreds of menu items, growing list of contact messages — no scale
engineering required.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Check | Status |
|---|---|---|
| I. Django-Only, Server-Rendered Stack | Django Templates + ORM + Admin only; Bootstrap via CDN; no React/Vue/Angular, no DRF, no GraphQL, no external API calls anywhere in the design. | PASS |
| II. Admin-Managed Content | `Category`, `MenuItem`, and `ContactMessage` all registered in `admin.py` with `list_display`/`list_filter`/`search_fields`; no code changes needed to manage content. | PASS |
| III. Responsive Bootstrap UI | Single `templates/base.html` defines navbar/footer via Bootstrap; every page template extends it; Bootstrap grid used throughout. | PASS |
| IV. Clean App Separation | `menu` app owns `Category`/`MenuItem`, filtering, item detail; `pages` app owns Home, Contact, `ContactMessage`. Each app owns its own models/views/urls/templates. | PASS |
| V. Ship-Ready Deliverable | Migrations committed with model changes; `requirements.txt` + `README.md` setup instructions (venv, install, migrate, createsuperuser, runserver) kept current. | PASS |

No violations — Complexity Tracking is not needed.

## Project Structure

### Documentation (this feature)

```text
specs/001-restaurant-menu-site/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output (/speckit-plan command)
├── data-model.md        # Phase 1 output (/speckit-plan command)
├── quickstart.md        # Phase 1 output (/speckit-plan command)
├── contracts/           # Phase 1 output (/speckit-plan command)
│   └── web-routes.md
└── tasks.md             # Phase 2 output (/speckit-tasks command - NOT created here)
```

### Source Code (repository root)

```text
manage.py
requirements.txt
README.md

restaurant_site/            # Django project package
├── __init__.py
├── settings.py
├── urls.py                 # includes menu.urls, pages.urls; serves MEDIA in DEBUG
├── wsgi.py
└── asgi.py

menu/                        # app: Category, MenuItem, listing, filter, detail
├── __init__.py
├── models.py                # Category, MenuItem
├── admin.py
├── views.py                 # menu_list (with ?category= filter), menu_item_detail
├── urls.py
├── migrations/
└── templates/menu/
    ├── menu_list.html
    └── menu_item_detail.html

pages/                        # app: Home, Contact, ContactMessage
├── __init__.py
├── models.py                # ContactMessage
├── admin.py
├── forms.py                  # ContactForm (ModelForm)
├── views.py                  # home, contact (GET/POST)
├── urls.py
├── migrations/
└── templates/pages/
    ├── home.html
    └── contact.html

templates/
└── base.html                 # shared navbar/footer, Bootstrap CDN include

static/
├── css/custom.css             # small overrides only
└── img/placeholder.png        # placeholder for missing MenuItem images

media/                         # MEDIA_ROOT (dev) — uploaded MenuItem images
```

**Structure Decision**: Standard Django multi-app layout (Option "web application", adapted
for server-rendered Django rather than a separate frontend/backend split). Two content apps
(`menu`, `pages`) as required by Constitution IV, a project-level `templates/` for the shared
`base.html`, and a project-level `static/` for the placeholder image and any custom CSS.

## Complexity Tracking

*No Constitution Check violations — table intentionally omitted.*
