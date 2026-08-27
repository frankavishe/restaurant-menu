# Phase 0 Research: Restaurant Menu Website

The constitution and spec already fix most technical decisions (Django-only stack, Bootstrap
UI, admin-managed content), so no items were left as `NEEDS CLARIFICATION` in the Technical
Context. This document records the remaining implementation-approach decisions.

## Django & dependency versions

- **Decision**: Django 5.1, Python 3.12, `Pillow` as the only extra runtime dependency.
- **Rationale**: Django 5.1 is the current stable release with long community support;
  `ImageField` requires Pillow to validate and process uploaded images (needed for FR-009a).
  No other third-party packages are needed — DRF, `django-crispy-forms`, etc. are avoidable
  with plain Django forms + Bootstrap classes in templates.
- **Alternatives considered**: Django REST Framework for API-driven rendering — rejected,
  forbidden by Constitution I. `django-crispy-forms` for form styling — rejected as an
  unnecessary dependency; Bootstrap form classes can be applied directly in the template/form
  widgets.

## Category filtering mechanism

- **Decision**: Server-rendered query-parameter filtering — `GET /menu/?category=<slug>`.
  The view reads the optional `category` query param, filters the `MenuItem` queryset by the
  matching `Category`, and re-renders the same template with the active filter highlighted.
  "All categories" is simply the URL with no `category` param.
- **Rationale**: Matches the spec's Assumption that filtering is "a standard server-rendered
  page navigation ... not a client-side/AJAX filter," and Constitution I's ban on JS
  frameworks. A plain `<a>`/link-based filter satisfies SC-002 (feels like a normal page
  navigation).
- **Alternatives considered**: Separate URL per category (`/menu/<slug>/`) — viable, but a
  single query-param view is simpler to implement and test while still giving each filtered
  view a shareable/bookmarkable URL; POST-based filter forms — rejected, filtering is not a
  mutation and should be a plain GET link.

## Price representation

- **Decision**: `MenuItem.price` is a `DecimalField(max_digits=6, decimal_places=2)`.
  Templates render it as `${{ item.price|floatformat:2 }}` (a fixed `$` prefix, since the spec
  clarifies single-currency/fixed-2-decimals with a shown symbol).
- **Rationale**: `DecimalField` avoids floating-point rounding issues for money. A fixed `$`
  prefix in the template satisfies FR-002 without adding a currency/locale library, which
  would be over-engineering for a single-currency site.
- **Alternatives considered**: `django.contrib.humanize` currency filters — unnecessary since
  only one currency/format is required; storing currency as a per-item field — rejected, out
  of scope (Assumption: "single currency ... multi-language support is out of scope").

## Image upload validation (type + size)

- **Decision**: `MenuItem.image` is an `ImageField(upload_to=..., blank=True, null=True)`
  with two validators: Django's built-in `FileExtensionValidator(['jpg', 'jpeg', 'png',
  'webp'])` for extension, plus a small custom validator function checking
  `file.size <= 5 * 1024 * 1024` and raising `ValidationError` otherwise. Both run in
  `full_clean()`, so Django Admin surfaces clear errors (FR-009a) without extra JS.
- **Rationale**: Built-in validators keep this dependency-free and enforce the rule at the
  model layer, so it applies uniformly whether the item is created via Admin or (in the
  future) any other form.
- **Alternatives considered**: Validating `content_type` via a JS/browser `accept` attribute
  only — rejected, purely client-side and not authoritative; a dedicated image-processing
  library (e.g. `django-imagekit`) — unnecessary for simple validation, adds a dependency.

## Placeholder image for missing MenuItem images

- **Decision**: A single static file `static/img/placeholder.png` referenced in templates via
  `{% if item.image %}{{ item.image.url }}{% else %}{% static 'img/placeholder.png' %}{% endif %}`.
- **Rationale**: Satisfies FR-013 with zero extra logic — a static asset, not a generated
  image or external placeholder service (which would violate the no-external-API rule).

## Contact form handling

- **Decision**: A `ModelForm` (`pages.forms.ContactForm`) bound to `ContactMessage`, with
  `message` using `forms.Textarea` and `MaxLengthValidator(2000)` (matching the model's
  `max_length=2000`) so both client-rendered `maxlength` and server-side validation agree.
  The `contact` view handles GET (blank form) and POST (validate → save → show a success
  message, or re-render with field errors) — a standard Post/Redirect/Get is used on success
  to avoid resubmission on refresh.
- **Rationale**: Matches FR-006/FR-007 and Acceptance Scenarios for User Story 5 without any
  AJAX or client-side framework; `ModelForm` keeps validation rules defined once, on the
  model.
- **Alternatives considered**: Sending an email notification on submit — explicitly out of
  scope per spec Assumptions (no email/external service requirement).

## Testing approach

- **Decision**: Django's built-in `TestCase` + `Client`, run with `python manage.py test`.
  Covers: model field validation (price precision, image validators, message length),
  `menu` view responses (list, category filter, detail 404 on missing item), and `pages`
  view responses (home renders featured items capped at 6, contact GET/POST valid+invalid).
- **Rationale**: No extra test dependency needed; Django's test runner is sufficient for a
  project this size and keeps the dependency list minimal per Constitution I's spirit.
- **Alternatives considered**: `pytest-django` — nicer fixtures/output but an extra
  dependency not justified for this project's size; can be revisited later without changing
  test intent.

## Bootstrap delivery

- **Decision**: Bootstrap 5 via CDN `<link>`/`<script>` tags in `templates/base.html`.
- **Rationale**: Constitution's Technology Constraints explicitly allow "CDN or vendored
  static files" for Bootstrap; CDN avoids adding a build step or vendoring binary/minified
  assets into the repo, keeping the project simplest to hand off.
- **Alternatives considered**: Vendoring Bootstrap into `static/`— viable fallback if the
  deployment environment has no internet access; noted here so it can be swapped later
  without any template restructuring (only the `<link>`/`<script>` src changes).

All Technical Context items are resolved; no open `NEEDS CLARIFICATION` markers remain.
