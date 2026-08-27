# Web Route Contracts: Restaurant Menu Website

This project exposes no JSON/REST API (forbidden by Constitution I). Its "contract" surface
is the set of server-rendered routes visitors and staff interact with. Each route below
documents method, inputs, template rendered, and status codes — the equivalent of an API
contract for a Django template-driven app.

## Public routes

### `GET /` — Home

- **View**: `pages.views.home`
- **Inputs**: none
- **Behavior**: Renders restaurant info/logo (from `settings`/template constants — no
  dedicated model, per spec this is static site content) and the featured-dishes section:
  `MenuItem.objects.filter(is_featured=True)[:6]` (FR-001 cap).
- **Template**: `pages/home.html` (extends `base.html`)
- **Status codes**: `200` always (no failure mode — an empty featured list renders an empty
  section, not an error).

### `GET /menu/` — Menu list (+ optional category filter)

- **View**: `menu.views.menu_list`
- **Inputs**: optional query param `?category=<slug>`
- **Behavior**:
  - No `category` param → all `MenuItem`s, `select_related('category')`, per FR-002.
  - `category=<slug>` matches an existing `Category.slug` → items filtered to that category
    (FR-003, Acceptance Scenario 2).
  - `category=<slug>` matches no `Category` → treated as "no filter"/falls back to full list
    rather than erroring (consistent with Edge Cases' error-avoidance stance); the filter UI
    highlights "All" in this case.
  - Every existing `Category` is listed as a filter link regardless of whether it currently
    has items (Edge Cases: zero-item category still appears as a filter option).
  - Zero items total → template renders an empty/"coming soon" state (Edge Cases).
- **Template**: `menu/menu_list.html`
- **Status codes**: `200` always.

### `GET /menu/<int:pk>/` — Menu item detail

- **View**: `menu.views.menu_item_detail`
- **Inputs**: `pk` path segment
- **Behavior**: Looks up `MenuItem` by `pk` via `get_object_or_404` (FR-004, User Story 4
  Acceptance Scenario 2 — "not found" response for a deleted/nonexistent item).
- **Template**: `menu/menu_item_detail.html`
- **Status codes**: `200` on found; `404` (Django's standard not-found page/template) when
  the item doesn't exist — satisfies FR-014.

### `GET|POST /contact/` — Contact page + form

- **View**: `pages.views.contact`
- **Inputs (POST)**: `name`, `contact_info`, `message` (form fields backing
  `ContactMessage`)
- **Behavior**:
  - `GET` → renders a blank `ContactForm`.
  - `POST` with valid data → saves a `ContactMessage`, then redirects (Post/Redirect/Get) to
    `GET /contact/?sent=1` (or a session/message-framework flash) so a confirmation renders
    without resubmission risk (FR-006, FR-007, User Story 5 Scenario 1).
  - `POST` with invalid data (missing required field, message > 2000 chars, malformed
    `contact_info`) → re-renders `contact.html` with the bound form and field errors, `200`;
    **no** `ContactMessage` row is created (User Story 5 Scenario 2, SC-004).
- **Template**: `pages/contact.html`
- **Status codes**: `200` (GET, POST-invalid, and the post-redirect confirmation GET);
  `302` (POST-valid → redirect).

## Admin routes (Django Admin — Constitution II)

All under `/admin/`, provided by `django.contrib.admin` with the three models registered:

| Model | Admin capabilities |
|---|---|
| `Category` | create, edit, delete; list shows `name`, `slug` |
| `MenuItem` | create, edit, delete; assign `category`, `price`, `description`, `image`, `is_featured`; list filterable by `category`/`is_featured`; image validators (FR-009a) enforced on save, surfaced as standard Django Admin form errors |
| `ContactMessage` | read (list + detail) for staff review (FR-010); standard Admin edit/delete available but no public-facing equivalent |

No custom admin views are needed — `ModelAdmin` registrations with the `list_display`/
`list_filter`/`search_fields` from `data-model.md` are sufficient.

## Not-found / error handling

- Django's default `404`/`500` handling applies project-wide; no custom error views are
  required by the spec. `DEBUG=False` in any non-dev settings would use Django's standard
  `templates/404.html`/`500.html` if added later — out of scope for this feature unless
  requested.

## Static & media

- `GET /static/...` — Bootstrap CSS/JS (CDN, not locally served — see `research.md`), plus
  `static/css/custom.css` and `static/img/placeholder.png`.
- `GET /media/...` — uploaded `MenuItem.image` files, served via Django's dev static helper
  (`django.conf.urls.static.static`) when `DEBUG=True`. Production media serving is out of
  scope for this feature.
