---

description: "Task list template for feature implementation"
---

# Tasks: Restaurant Menu Website

**Input**: Design documents from `/specs/001-restaurant-menu-site/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/web-routes.md, quickstart.md (all present)

**Tests**: Not requested in the spec/plan — no test tasks are included. `python manage.py test` is referenced only as an optional automated check in quickstart.md.

**Organization**: Tasks are grouped by user story (priority order from spec.md: US1 → US5) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Include exact file paths in descriptions

## Path Conventions

Standard Django multi-app layout at the repository root (per `plan.md` Project Structure):
`manage.py`, `requirements.txt`, `README.md`, `restaurant_site/`, `menu/`, `pages/`, `templates/`, `static/`, `media/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create Django project scaffold at the repo root: `django-admin startproject restaurant_site .` (creates `manage.py` and `restaurant_site/{settings.py,urls.py,wsgi.py,asgi.py}`)
- [ ] T002 [P] Create `requirements.txt` at the repo root listing `Django~=5.1` and `Pillow`
- [ ] T003 [P] Create the `menu` app: `python manage.py startapp menu`, then add `menu/urls.py` with `urlpatterns = []`
- [ ] T004 [P] Create the `pages` app: `python manage.py startapp pages`, then add `pages/urls.py` with `urlpatterns = []`
- [ ] T005 Configure `restaurant_site/settings.py` (depends on T001): add `'menu'` and `'pages'` to `INSTALLED_APPS`; set `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']`; set `STATICFILES_DIRS = [BASE_DIR / 'static']`; add `MEDIA_URL = '/media/'` and `MEDIA_ROOT = BASE_DIR / 'media'`
- [ ] T006 [P] Create `templates/`, `static/css/`, and `static/img/` directories at the repo root; add a placeholder image at `static/img/placeholder.png`
- [ ] T007 Wire `restaurant_site/urls.py` (depends on T003, T004, T005): `path('admin/', admin.site.urls)`, `path('', include('pages.urls'))`, `path('menu/', include('menu.urls'))`, plus `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` appended when `settings.DEBUG` is `True`

**Checkpoint**: `python manage.py runserver` boots with no errors (empty pages/routes still to come).

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models, migrations, and shared template/static infrastructure that every user story depends on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create `Category` model in `menu/models.py`: `name` `CharField(max_length=100)`, `slug` `SlugField(max_length=110, unique=True)` auto-populated from `name` via `slugify()` in `save()` when blank, `Meta.ordering = ['name']`, `__str__` returns `name`
- [ ] T009 [P] Create `validate_image_size` validator function in `menu/validators.py`: raises `ValidationError` if `file.size > 5 * 1024 * 1024`
- [ ] T010 Create `MenuItem` model in `menu/models.py` (depends on T008, T009): `name` `CharField(150)`, `description` `TextField`, `price` `DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])`, `image` `ImageField(upload_to='menu_items/', blank=True, null=True, validators=[FileExtensionValidator(['jpg','jpeg','png','webp']), validate_image_size])`, `category` `ForeignKey(Category, on_delete=models.CASCADE, related_name='items')`, `is_featured` `BooleanField(default=False)`, `created_at` `DateTimeField(auto_now_add=True)`, `Meta.ordering = ['category__name', 'name']`, `__str__` returns `name`
- [ ] T011 Generate `menu` app migration (depends on T008, T010): `python manage.py makemigrations menu`
- [ ] T012 Apply migrations (depends on T011): `python manage.py migrate`
- [ ] T013 [P] Create `templates/base.html`: Bootstrap 5 CDN `<link>`/`<script>` tags, responsive navbar with hardcoded links to `/` (Home), `/menu/` (Menu), `/contact/` (Contact) plus a collapsible toggler, a footer, and `{% block content %}{% endblock %}` — hardcoded hrefs (matching the fixed paths in `contracts/web-routes.md`) are used deliberately so the shared navbar renders correctly regardless of which story phases below are implemented yet
- [ ] T014 [P] Create `static/css/custom.css` with minimal Bootstrap override rules, linked from `base.html`

**Checkpoint**: Foundation ready — models migrated, shared layout in place, user story implementation can now begin.

---

## Phase 3: User Story 1 - Browse the Menu by Category (Priority: P1) 🎯 MVP

**Goal**: A filterable Menu page listing every item with name, description, price, image, and category.

**Independent Test**: Load `/menu/` with ≥2 categories and several items seeded; verify all items display with name/description/price/image/category; select a category filter and verify only that category's items remain; clear the filter and verify the full list returns.

- [ ] T015 [US1] Implement `menu_list` view in `menu/views.py`: read optional `?category=<slug>` query param; base queryset `MenuItem.objects.select_related('category')`; if the slug matches an existing `Category`, filter to it, else use the full queryset (unmatched/absent slug → "no filter", per `contracts/web-routes.md`); fetch `Category.objects.all()` for the filter nav; pass `menu_items`, `categories`, `active_category` to context
- [ ] T016 [US1] Register the list route in `menu/urls.py` (depends on T015): `path('', views.menu_list, name='menu_list')`
- [ ] T017 [P] [US1] Create `menu/templates/menu/menu_list.html` (depends on T015) extending `base.html`, using Bootstrap grid/card classes throughout for responsive layout (FR-012): category filter nav (a link per `Category` plus an "All" link that clears `?category`, highlighting `active_category`), an item list showing name, description, price as `${{ item.price|floatformat:2 }}`, image or `{% static 'img/placeholder.png' %}` fallback, category name, and a link to `/menu/{{ item.pk }}/`; an empty-state message when `menu_items` is empty

**Checkpoint**: Menu browsing and category filtering fully functional and independently testable — MVP deliverable.

---

## Phase 4: User Story 2 - Manage Menu Content via Admin (Priority: P2)

**Goal**: Staff can create/edit/delete Categories and MenuItems through Django Admin, reflected immediately on the public Menu page.

**Independent Test**: Log into `/admin/`; create a Category; create a MenuItem assigned to it with name/description/price/image; edit then delete a MenuItem; confirm each change is reflected on `/menu/`.

- [ ] T018 [US2] Register `CategoryAdmin` in `menu/admin.py`: `list_display=('name', 'slug')`, `search_fields=('name',)`, `prepopulated_fields={'slug': ('name',)}`
- [ ] T019 [US2] Register `MenuItemAdmin` in `menu/admin.py` (depends on T018, same file): `list_display=('name', 'category', 'price', 'is_featured')`, `list_filter=('category', 'is_featured')`, `search_fields=('name', 'description')`

**Checkpoint**: Staff can fully manage Category/MenuItem content via Admin; changes appear on `/menu/` (US1) without further action.

---

## Phase 5: User Story 3 - View the Home Page (Priority: P3)

**Goal**: Home page shows restaurant info/logo and a featured-dishes section (capped at 6), reachable from a shared navbar/footer.

**Independent Test**: Load `/` with restaurant info configured and ≥1 item marked featured; verify name/logo/info, a featured-dishes section, and navbar/footer links to Home, Menu, and Contact.

- [ ] T020 [US3] Implement `home` view in `pages/views.py`: query `MenuItem.objects.filter(is_featured=True).select_related('category')[:6]` (FR-001 cap), pass as `featured_items` to context
- [ ] T021 [US3] Register the home route in `pages/urls.py` (depends on T020): `path('', views.home, name='home')`
- [ ] T022 [P] [US3] Create `pages/templates/pages/home.html` (depends on T020) extending `base.html`, using Bootstrap grid/card classes throughout for responsive layout (FR-012): restaurant name/logo/info block (static template content), a featured-dishes section iterating `featured_items` (name/price/image-or-placeholder, each linking to `/menu/{{ item.pk }}/`), and a fallback message when `featured_items` is empty

**Checkpoint**: Home page functional; navbar/footer (from Foundational T013) already links Home/Menu/Contact.

---

## Phase 6: User Story 4 - View Menu Item Details (Priority: P4)

**Goal**: A dedicated detail page per menu item, with a clear 404 for missing items.

**Independent Test**: From `/menu/`, open an item's detail link; verify it shows the same name/description/price/image/category as the listing; visit a nonexistent item id and confirm a 404.

- [ ] T023 [US4] Implement `menu_item_detail` view in `menu/views.py`: `get_object_or_404(MenuItem.objects.select_related('category'), pk=pk)`, pass `item` to context (FR-014)
- [ ] T024 [US4] Register the detail route in `menu/urls.py` (depends on T023): `path('<int:pk>/', views.menu_item_detail, name='menu_item_detail')`
- [ ] T025 [P] [US4] Create `menu/templates/menu/menu_item_detail.html` (depends on T023) extending `base.html`, using Bootstrap grid/card classes for responsive layout (FR-012): full name, description, price (`${{ item.price|floatformat:2 }}`), image or placeholder fallback, category name

**Checkpoint**: Item detail pages reachable from the Menu page (link already added in T017) and 404 correctly for missing items.

---

## Phase 7: User Story 5 - Contact the Restaurant (Priority: P5)

**Goal**: A Contact page with a validated, persisted contact form.

**Independent Test**: Submit `/contact/` with valid data → confirmation shown, message retrievable in Admin; submit with missing/invalid data → validation errors shown, nothing saved.

- [ ] T026 [US5] Create `ContactMessage` model in `pages/models.py`: `name` `CharField(150)`, `contact_info` `CharField(254)`, `message` `TextField(max_length=2000)`, `submitted_at` `DateTimeField(auto_now_add=True)`, `Meta.ordering = ['-submitted_at']`, `__str__` returns `f"{self.name} ({self.submitted_at:%Y-%m-%d %H:%M})"`
- [ ] T027 [US5] Generate `pages` app migration (depends on T026): `python manage.py makemigrations pages`
- [ ] T028 [US5] Apply migration (depends on T027): `python manage.py migrate`
- [ ] T029 [P] [US5] Register `ContactMessageAdmin` in `pages/admin.py` (depends on T026): `list_display=('name', 'contact_info', 'submitted_at')`, `list_filter=('submitted_at',)`, `search_fields=('name', 'contact_info', 'message')`
- [ ] T030 [P] [US5] Create `ContactForm` (`ModelForm`) in `pages/forms.py` (depends on T026), bound to `ContactMessage` fields `name`, `contact_info`, `message`; `message` widget `forms.Textarea` with `maxlength=2000`; apply Bootstrap `form-control` classes to all widgets; add a `clean_contact_info` method enforcing FR-006's "well-formed contact info" rule via a light email-or-phone pattern check (reject anything matching neither), raising `forms.ValidationError` on failure
- [ ] T031 [US5] Implement `contact` view in `pages/views.py` (depends on T030): `GET` renders a blank `ContactForm`; valid `POST` saves the `ContactMessage` and redirects to `contact` with `?sent=1` (Post/Redirect/Get); invalid `POST` re-renders `contact.html` with the bound form and field errors, no row saved (FR-006, FR-007)
- [ ] T032 [US5] Register the contact route in `pages/urls.py` (depends on T031): `path('contact/', views.contact, name='contact')`
- [ ] T033 [P] [US5] Create `pages/templates/pages/contact.html` (depends on T031) extending `base.html`, using Bootstrap grid/form classes for responsive layout (FR-012): restaurant contact info block, rendered `ContactForm` with Bootstrap markup (form-control/form-group) and field errors, a success confirmation shown when `request.GET.get('sent') == '1'`

**Checkpoint**: All five user stories independently functional.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Handoff readiness across all stories

- [ ] T034 [P] Create `README.md` at the repo root with setup instructions (venv creation/activation, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py createsuperuser`, `python manage.py runserver`) per `quickstart.md`
- [ ] T035 [P] Verify Django's default 404 response renders for `/menu/999999/` (nonexistent `MenuItem`) and confirm no custom error template is needed for this feature (FR-014)
- [ ] T036 Manual responsive check of Home/Menu/Item Detail/Contact at ~375px, ~768px, ~1280px widths per `quickstart.md` (FR-012, SC-005): no horizontal scrolling, no overlapping content, navbar collapses to a toggler on narrow widths
- [ ] T037 Execute all `quickstart.md` validation scenarios end-to-end (seed ≥2 categories and several items incl. 7+ featured via Admin, walk through the US1–US5 Independent Tests, confirm SC-001–SC-005)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories.
- **User Stories (Phase 3–7)**: All depend on Foundational completion.
  - US1 (Menu browse) has no dependency on other stories — true MVP.
  - US2 (Admin) depends only on the models from Foundational (T008/T010), not on US1's view/template.
  - US3 (Home) depends only on Foundational's `MenuItem` model.
  - US4 (Item detail) depends only on Foundational's `MenuItem` model; its link is added to US1's template in T017 using a hardcoded path, so US4 does not need to precede US1.
  - US5 (Contact) is fully self-contained (own model, form, view, template).
  - Stories can therefore proceed in parallel after Foundational, or sequentially in priority order (P1 → P5) as written.
- **Polish (Phase 8)**: Depends on all desired user stories being complete.

### Within Each User Story

- Model changes (if any) before views.
- Views before URL registration (route references the view function).
- URL registration and templates can proceed in parallel once the view exists.

### Parallel Opportunities

- Setup: T002, T003, T004, T006 can run in parallel.
- Foundational: T009, T013, T014 can run in parallel (T009 before T010 as an import dependency, but authoring itself is independent of T008).
- US1: T017 in parallel with T016 (both depend only on T015).
- US3: T022 in parallel with T021 (both depend only on T020).
- US4: T025 in parallel with T024 (both depend only on T023).
- US5: T029 and T030 in parallel (both depend only on T026); T033 in parallel with T032 (both depend only on T031).
- Different user stories (US1–US5) can be worked on in parallel by different developers once Foundational is done.

---

## Parallel Example: User Story 1

```bash
# After T015 (menu_list view) is done, launch together:
Task: "Register the list route in menu/urls.py"
Task: "Create menu/templates/menu/menu_list.html"
```

## Parallel Example: User Story 5

```bash
# After T026 (ContactMessage model) is done, launch together:
Task: "Register ContactMessageAdmin in pages/admin.py"
Task: "Create ContactForm in pages/forms.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Load `/menu/`, seed via `python manage.py shell` or Admin (US2 not yet built — shell/fixtures work fine for this checkpoint), verify listing + category filter
5. Demo if ready

### Incremental Delivery

1. Setup + Foundational → foundation ready (models migrated, shared layout in place)
2. Add US1 → test independently → MVP demo (Menu browse + filter)
3. Add US2 → test independently → staff can now manage content without a developer
4. Add US3 → test independently → Home page live
5. Add US4 → test independently → item detail pages live
6. Add US5 → test independently → Contact form live
7. Polish → README, 404 check, responsive check, full quickstart walkthrough

### Suggested Team Split

With multiple developers, after Foundational: Developer A takes US1 → US4 (both `menu` app), Developer B takes US3 → US5 (both `pages` app), Developer C takes US2 (Admin, `menu/admin.py`) once T008/T010 land — each story's independence (see Dependencies above) means little coordination is needed beyond the shared `templates/base.html` from Foundational.

---

## Notes

- [P] tasks = different files, no dependency on an incomplete task
- [Story] label maps task to a specific user story for traceability
- No test tasks are included — not requested in spec.md/plan.md; `python manage.py test` remains available as an optional manual check (see `research.md#testing-approach`)
- Commit after each task or logical group
- Stop at any checkpoint to validate a story independently
