# Feature Specification: Restaurant Menu Website

**Feature Branch**: `001-restaurant-menu-site`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "A responsive Django restaurant menu website with a home page (restaurant info, logo, featured dishes, navbar, footer), a menu page (name, description, price, image, category, with category filtering), an item detail page, a contact page with a contact form, Django Admin management of Categories and MenuItems, and data models for Category, MenuItem, and ContactMessage. Built with Django + Bootstrap only — no JS frameworks, no DRF, no external APIs. See requirement.md."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse the Menu by Category (Priority: P1)

A visitor opens the site to see what food is on offer, and narrows the list down to a
category they care about (e.g. "Starters", "Drinks") to decide what to order.

**Why this priority**: This is the core value of the site — without a browsable, filterable
menu there is no product. It is the single feature that must work for the site to be useful.

**Independent Test**: Load the menu page with at least two categories and several items
seeded; verify all items display with name, description, price, image, and category; select a
category filter and verify only that category's items remain visible.

**Acceptance Scenarios**:

1. **Given** the menu has items across multiple categories, **When** a visitor opens the Menu
   page, **Then** every menu item is listed with its name, description, price, image, and
   category.
2. **Given** the visitor is on the Menu page, **When** they select a specific category,
   **Then** only items belonging to that category are shown.
3. **Given** the visitor has filtered to a category, **When** they choose "All" (or clear the
   filter), **Then** the full menu is shown again.

---

### User Story 2 - Manage Menu Content via Admin (Priority: P2)

Restaurant staff sign in to Django Admin to add new categories and dishes, correct prices or
descriptions, and remove discontinued items — without needing a developer.

**Why this priority**: The menu is only ever as good as the content behind it. Staff must be
able to keep it current on their own for the site to stay useful over time.

**Independent Test**: Log into `/admin/` as a staff user; create a Category; create a
MenuItem assigned to it with name/description/price/image; edit and then delete a MenuItem;
confirm each change is immediately reflected on the public Menu page.

**Acceptance Scenarios**:

1. **Given** a staff user is logged into Django Admin, **When** they create a new Category,
   **Then** it becomes available for assignment to menu items and appears as a filter option
   on the Menu page.
2. **Given** a staff user is on the MenuItem admin form, **When** they save a new item with
   name, description, price, image, and category, **Then** the item appears on the public
   Menu page under its category.
3. **Given** an existing MenuItem, **When** a staff user edits or deletes it in Admin,
   **Then** the public Menu page reflects the update or removal without further action.

---

### User Story 3 - View the Home Page (Priority: P3)

A first-time visitor lands on the home page and immediately understands what restaurant this
is, sees a few standout dishes, and can navigate to the rest of the site.

**Why this priority**: The home page is the entry point for most visitors and drives them
toward the Menu and Contact pages; it doesn't carry unique data of its own beyond what P1/P2
already provide.

**Independent Test**: Load the home page with restaurant info configured and at least one
item marked as featured; verify restaurant name/logo, a featured-dishes section, and a navbar
and footer with links to Home, Menu, and Contact are all present.

**Acceptance Scenarios**:

1. **Given** the site is configured with restaurant info and a logo, **When** a visitor loads
   the home page, **Then** the restaurant name, logo, and general info are displayed.
2. **Given** one or more menu items are marked as featured, **When** a visitor loads the home
   page, **Then** those items are displayed in a featured-dishes section.
3. **Given** a visitor is on any page, **When** they use the navbar or footer, **Then** they
   can reach Home, Menu, and Contact.

---

### User Story 4 - View Menu Item Details (Priority: P4)

A visitor who is interested in a specific dish opens its detail page to see the full
description and any other information before deciding to order.

**Why this priority**: Useful, but the item summary already shown on the Menu page (P1)
covers most decision-making needs; the dedicated detail page is a refinement, not the core
loop.

**Independent Test**: From the Menu page, click through to a single item; verify its detail
page shows the same name, description, price, image, and category as the menu listing.

**Acceptance Scenarios**:

1. **Given** a visitor is viewing the Menu page, **When** they select a specific item,
   **Then** they are taken to a detail page showing that item's full name, description,
   price, image, and category.
2. **Given** a visitor navigates directly to an item detail URL that doesn't exist (e.g. it
   was deleted), **When** the page loads, **Then** a clear "not found" response is shown
   instead of an error page.

---

### User Story 5 - Contact the Restaurant (Priority: P5)

A visitor with a question (reservation, catering, feedback) fills out the contact form so the
restaurant can follow up.

**Why this priority**: Valuable for conversions but not required for the site's core purpose
of presenting the menu; it's the last mile of the visitor journey.

**Independent Test**: Submit the contact form with valid data and confirm a success message
appears and the submission is retrievable by staff; submit with missing/invalid data and
confirm validation errors are shown and nothing is saved.

**Acceptance Scenarios**:

1. **Given** a visitor is on the Contact page, **When** they submit the form with valid name,
   contact info, and message, **Then** they see a confirmation and the message is saved for
   staff to review.
2. **Given** a visitor submits the contact form with a required field missing or invalid,
   **When** they submit, **Then** the form redisplays with clear validation errors and no
   message is saved.
3. **Given** staff want to review inquiries, **When** they open Django Admin, **Then** they
   can see all submitted contact messages with sender info and timestamp.

---

### Edge Cases

- What happens when a category has zero menu items? The category still appears as a filter
  option; selecting it shows an empty state rather than an error.
- What happens when a menu item has no image uploaded? The page renders a placeholder image
  instead of a broken image link.
- What happens when the menu has no items at all yet (fresh install)? The Menu page renders
  with an empty/"coming soon" state rather than erroring.
- How does the system handle a contact form submission with an excessively long message or
  invalid characters? Server-side validation rejects it with a clear error; no partial data is
  saved.
- What happens when two categories or two menu items share the same name? Allowed — items are
  distinguished internally by ID, not by uniqueness of name.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST display a Home page with restaurant name/info, logo, a
  featured-dishes section, a navbar, and a footer.
- **FR-002**: The system MUST display a Menu page listing every menu item with its name,
  description, price, image, and category.
- **FR-003**: The system MUST let visitors filter the Menu page by category, including an
  option to view all categories at once.
- **FR-004**: The system MUST provide a detail page for each menu item showing its full name,
  description, price, image, and category.
- **FR-005**: The system MUST display a Contact page with restaurant contact information and
  a contact form.
- **FR-006**: The system MUST validate contact form submissions (required fields, well-formed
  contact info) before saving them, and MUST show the visitor a confirmation on success and
  clear errors on failure.
- **FR-007**: The system MUST persist every valid contact form submission for staff to review.
- **FR-008**: The system MUST let staff create, edit, and delete Categories through Django
  Admin.
- **FR-009**: The system MUST let staff create, edit, and delete MenuItems (including
  assigning a category, price, description, and image) through Django Admin.
- **FR-010**: The system MUST let staff view submitted contact messages through Django Admin.
- **FR-011**: The system MUST let staff mark a MenuItem as "featured" so it can appear in the
  Home page's featured-dishes section.
- **FR-012**: The system MUST render all pages responsively, remaining usable and legible on
  mobile, tablet, and desktop screen widths.
- **FR-013**: The system MUST show a placeholder image for any menu item that has no image
  uploaded.
- **FR-014**: The system MUST return a clear "not found" result when a visitor requests a
  menu item or category that does not exist.

### Key Entities

- **Category**: A grouping for menu items (e.g. "Starters", "Main Course", "Beverages").
  Attributes: name, and enough identifying info to be selected as a Menu page filter. A
  category can have zero or many menu items.
- **MenuItem**: A single dish or drink offered by the restaurant. Attributes: name,
  description, price, image, category (belongs to one Category), and a flag for whether it is
  featured on the Home page.
- **ContactMessage**: A message submitted through the Contact page. Attributes: sender name,
  sender contact info (e.g. email), message body, and submission timestamp. Reviewed by staff
  in Django Admin; not editable by the visitor after submission.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time visitor can find the price and description of a specific dish in
  under 30 seconds from landing on the Home page.
- **SC-002**: Filtering the Menu page to a single category updates the visible items with no
  full-page reload delay perceptible as more than a normal page navigation (i.e. behaves like
  any standard link/page load).
- **SC-003**: Staff can add a brand-new menu item (with image) and see it live on the public
  Menu page within 2 minutes, with zero code changes or developer involvement.
- **SC-004**: 100% of valid contact form submissions are retrievable by staff afterward; 0% of
  invalid submissions (missing/malformed required fields) are saved.
- **SC-005**: All pages remain fully usable (no overlapping content, no horizontal scrolling,
  all actions reachable) at common mobile, tablet, and desktop widths.

## Assumptions

- Menu item images are uploaded files managed through Django Admin (not external image URLs),
  matching the "no external APIs" constraint.
- The contact form's only required delivery mechanism is persisting `ContactMessage` records
  for staff to review in Django Admin; outbound email notification is out of scope for this
  feature unless requested later.
- "Featured dishes" on the Home page are chosen explicitly by staff (a flag on MenuItem) rather
  than computed automatically (e.g. by popularity), since no ordering data source exists yet.
- Category filtering on the Menu page is a standard server-rendered page navigation (query
  parameter or route per category), consistent with the "no JS framework" constraint — it is
  not a client-side/AJAX filter.
- No user accounts or authentication are required for visitors; only staff (Django Admin
  superuser/staff accounts) authenticate, using Django's built-in auth.
- Single restaurant, single language, single currency — multi-location/multi-language support
  is out of scope.
