# Phase 1 Data Model: Restaurant Menu Website

Derived from the spec's Key Entities and Functional Requirements. All models live in Django
apps per Constitution IV: `Category`/`MenuItem` in the `menu` app, `ContactMessage` in the
`pages` app.

## Category (`menu` app)

Grouping for menu items; a filter option on the Menu page (FR-003).

| Field | Type | Rules |
|---|---|---|
| `id` | `AutoField` (PK) | implicit |
| `name` | `CharField(max_length=100)` | required; `unique=False` — duplicate names allowed per spec Edge Cases ("two categories ... share the same name? Allowed") |
| `slug` | `SlugField(max_length=110, unique=True)` | auto-generated from `name` on save if blank (`django.utils.text.slugify`); used in the Menu page's `?category=` filter URL and must be unique for unambiguous lookup even when names repeat |

**Relationships**: one `Category` → many `MenuItem` (`MenuItem.category` FK). A category may
have zero items (Edge Cases: "category has zero menu items ... still appears as a filter
option").

**Ordering**: `Meta.ordering = ['name']` for a stable, predictable filter list.

**`__str__`**: returns `name`.

## MenuItem (`menu` app)

A single dish or drink (FR-002, FR-004, FR-009, FR-011).

| Field | Type | Rules |
|---|---|---|
| `id` | `AutoField` (PK) | implicit |
| `name` | `CharField(max_length=150)` | required; duplicates allowed (Edge Cases) |
| `description` | `TextField` | required |
| `price` | `DecimalField(max_digits=6, decimal_places=2)` | required; `MinValueValidator(0)`; single currency, fixed 2 decimals per clarification |
| `image` | `ImageField(upload_to='menu_items/', blank=True, null=True)` | optional; validators: `FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])` + custom `validate_image_size` (≤ 5MB) per FR-009a |
| `category` | `ForeignKey(Category, on_delete=models.CASCADE, related_name='items')` | required |
| `is_featured` | `BooleanField(default=False)` | drives Home page featured-dishes section (FR-011); cap of 6 displayed is enforced in the view/query (`order_by(...)[:6]`), not on the model |
| `created_at` | `DateTimeField(auto_now_add=True)` | for stable default ordering |

**Relationships**: belongs to one `Category`. `on_delete=CASCADE` — deleting a `Category`
removes its items; acceptable since content is fully admin-managed and this is the simplest
behavior consistent with "no orphaned items" (no spec requirement contradicts this; staff can
recreate items if a category is deleted by mistake, which Admin's delete-confirmation page
guards against).

**Ordering**: `Meta.ordering = ['category__name', 'name']`.

**`__str__`**: returns `name`.

**Validation notes**:
- `validate_image_size(file)`: raises `ValidationError` if `file.size > 5 * 1024 * 1024`.
- Missing image → templates fall back to the static placeholder (FR-013); this is a template
  concern, not a model constraint (`blank=True, null=True` is correct as-is).

## ContactMessage (`pages` app)

A visitor inquiry submitted through the Contact page (FR-005, FR-006, FR-007).

| Field | Type | Rules |
|---|---|---|
| `id` | `AutoField` (PK) | implicit |
| `name` | `CharField(max_length=150)` | required |
| `contact_info` | `CharField(max_length=254)` | required; holds an email or phone (spec says "sender contact info (e.g. email)" — kept as a general string rather than `EmailField` so a phone number is also valid; format is still validated as "well-formed" per FR-006 via form-level validation, e.g. non-empty and matching a light email-or-phone pattern) |
| `message` | `TextField(max_length=2000)` | required; capped at 2000 characters per clarification/FR-006 |
| `submitted_at` | `DateTimeField(auto_now_add=True)` | timestamp for staff review, immutable |

**Relationships**: none — a standalone record, not editable by the visitor after submission
(spec: "not editable by the visitor after submission" — enforced simply by not exposing any
edit view for it; Admin retains standard edit capability for staff).

**Ordering**: `Meta.ordering = ['-submitted_at']` (newest first for staff review in Admin).

**`__str__`**: returns `f"{self.name} ({self.submitted_at:%Y-%m-%d %H:%M})"`.

## State / lifecycle notes

- No entity in this feature has a state machine. `MenuItem.is_featured` is a simple boolean
  toggle, and per clarification there is deliberately **no** "currently unavailable" state —
  temporary removal is done by editing/deleting the item (spec Assumption).
- `ContactMessage` is create-only from the public site; staff may still edit/delete via Admin
  as a standard Django Admin capability, but no public-facing edit/delete path exists.

## Admin registration summary (Constitution II)

| Model | `list_display` | `list_filter` | `search_fields` |
|---|---|---|---|
| `Category` | `name`, `slug` | — | `name` |
| `MenuItem` | `name`, `category`, `price`, `is_featured` | `category`, `is_featured` | `name`, `description` |
| `ContactMessage` | `name`, `contact_info`, `submitted_at` | `submitted_at` | `name`, `contact_info`, `message` |

`MenuItem` and `Category` admin are further detailed in `contracts/web-routes.md` alongside
the public routes they back.
