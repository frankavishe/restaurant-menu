# Quickstart: Restaurant Menu Website

Validation guide for this feature once implemented (Phase 7). Not implementation code — see
`data-model.md` for fields and `contracts/web-routes.md` for routes.

## Prerequisites

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

## Seed content (via Admin)

1. Open `http://127.0.0.1:8000/admin/`, log in as the superuser created above.
2. Create at least two `Category` rows (e.g. "Starters", "Drinks").
3. Create several `MenuItem` rows across those categories, with name/description/price and an
   uploaded image on at least one; mark one or two as `is_featured`.

## Validation scenarios

Each maps to an Independent Test / Acceptance Scenario from `spec.md`.

### 1. Browse & filter the Menu (User Story 1)

- Visit `/menu/` → every seeded item appears with name, description, price (e.g. `$12.99`),
  image (or placeholder), and category. See `contracts/web-routes.md#get-menu--menu-list--optional-category-filter`.
- Click a category filter link → only that category's items remain.
- Click "All" → the full list returns.

### 2. Manage content via Admin (User Story 2)

- In `/admin/`, edit a `MenuItem`'s price or description → reload `/menu/` → change is
  reflected immediately.
- Delete a `MenuItem` → it disappears from `/menu/` and its old detail URL now 404s.

### 3. Home page (User Story 3)

- Visit `/` → restaurant name/logo/info render, plus a featured-dishes section listing the
  `is_featured` items (capped at 6 even if more are marked — seed 7+ to verify the cap).
- Navbar/footer links reach Home, Menu, and Contact from any page.

### 4. Item detail (User Story 4)

- From `/menu/`, click into an item → detail page shows the same name/description/price/
  image/category.
- Visit `/menu/999999/` (a nonexistent id) → a `404` response, not a server error.

### 5. Contact form (User Story 5)

- Visit `/contact/`, submit valid name/contact info/message → confirmation shown; the row is
  visible under `ContactMessage` in `/admin/`.
- Submit with a required field blank, or a message over 2000 characters → form re-renders
  with validation errors; no new `ContactMessage` row is created (verify count in Admin
  unchanged).

## Automated checks

```powershell
python manage.py test
```

Should cover: model validation (price precision, image type/size validators, message length
cap), `menu` view responses (list/filter/detail/404), and `pages` view responses (home
featured cap, contact GET/POST valid+invalid) — see `research.md#testing-approach`.

## Responsive check (FR-012, SC-005)

Using browser dev tools, verify Home/Menu/Item Detail/Contact at common mobile (~375px),
tablet (~768px), and desktop (~1280px) widths: no horizontal scrolling, no overlapping
content, navbar collapses to a Bootstrap toggler on narrow widths, all links/buttons remain
reachable.
