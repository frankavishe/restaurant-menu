# Restaurant Menu Website

A responsive, server-rendered Django site for a restaurant: a Home page with featured
dishes, a filterable Menu page, per-item detail pages, and a Contact page with a persisted
contact form. All content (categories, menu items, contact messages) is managed through
Django Admin.

Built with Django Templates, the Django ORM, and Django Admin only — no REST framework, no
JS framework, no external APIs. UI is responsive via Bootstrap 5 (CDN).

## Requirements

- Python 3.12+
- pip / venv

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit:

- `http://127.0.0.1:8000/` — Home
- `http://127.0.0.1:8000/menu/` — Menu (with category filter)
- `http://127.0.0.1:8000/contact/` — Contact
- `http://127.0.0.1:8000/admin/` — Admin (log in with the superuser created above)

## Managing content

All content is managed via Django Admin (`/admin/`):

- **Categories** — create/edit/delete menu categories (e.g. "Starters", "Drinks").
- **Menu Items** — create/edit/delete dishes: name, description, price, image (JPEG/PNG/
  WebP, max 5MB), category, and a "featured" flag (featured items appear on Home, capped at
  the first 6).
- **Contact Messages** — read-only-in-spirit list of messages submitted via the Contact page
  (standard Admin edit/delete is still available to staff).

## Project layout

```text
manage.py
requirements.txt
restaurant_site/     # Django project settings/urls
menu/                 # Category, MenuItem models; menu list/filter/detail views
pages/                # Home, Contact views; ContactMessage model + form
templates/base.html  # shared navbar/footer (Bootstrap)
static/               # custom.css, placeholder image
media/                 # uploaded MenuItem images (dev)
```

## Running tests

```powershell
python manage.py test
```

See `specs/001-restaurant-menu-site/quickstart.md` for full validation scenarios.
