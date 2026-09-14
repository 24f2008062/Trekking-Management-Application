# 🗺️ Bauhaus UI Implementation & Migration Plan
## Project: Trekking Management Application
**Objective:** Transform existing Bootstrap views into an authentic Bauhaus design system while preserving 100% of underlying business logic and routes.

---

## 1. Implementation Phasing Overview

```
+---------------------------------------------------------------------------------------+
| PHASE 1A: Core Foundation & Global Bauhaus Shell                                      |
|  - Google Fonts (Space Grotesk + Inter)                                               |
|  - Overhaul static/css/style.css (Tokens, Buttons, Tables, Cards, Badges)             |
|  - Overhaul templates/base.html (Navbar, Flash alerts, Bauhaus container framing)     |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 1B: High-Velocity Redis & Zero-Trust Security Foundation                        |
|  - Redis 7.x multi-tier caching (Catalog, Lookups, Search) with Cache-Aside pattern   |
|  - Server-side Redis session storage (Flask-Session) & instant user revocation        |
|  - Concurrency control: Atomic Redis distributed lock on slot reservation             |
|  - Distributed sliding-window rate limiting (Flask-Limiter) & HTTP security headers   |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 2: Authentication & Onboarding                                                  |
|  - templates/login.html & index.html (Bauhaus Constructivist Poster Layout)           |
|  - templates/register.html (High-contrast role picker & form controls)                |
|  - templates/staff_details.html (Guide credentialing form)                            |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 3: Trekker Experience & Booking Flow                                            |
|  - templates/trekker_dashboard.html (Numbered tabs, catalog table, card layout)       |
|  - templates/book_trek.html (Emergency declaration, pricing card, confirm button)     |
|  - templates/update_trekker_profile.html                                              |
|  - [NEW] templates/trek_pass.html (Printable Bauhaus Digital Trek Pass)               |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 4: Staff / Guide Operations Portal                                              |
|  - templates/staff_dashboard.html (Assigned treks table, trekker roster)              |
|  - templates/edit_staff_trek.html & update_profile.html                                |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 5: Admin Command Center & Management Views                                      |
|  - templates/admin_dashboard.html (Color-blocked KPI metrics, 6 management tabs)      |
|  - templates/add_trek.html, edit_trek.html, assign_staff.html                         |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
| PHASE 6: End-to-End Verification & Non-Regression Audit                               |
|  - RBAC verification (Admin, Staff, Trekker, Blacklisted, Pending)                    |
|  - Slot reservation atomic math check                                                 |
|  - Responsive mobile testing & print styling check                                    |
+---------------------------------------------------------------------------------------+
```

---

## 2. Detailed Phase Breakdown

### Phase 1: Core Foundation & Global Shell

#### 1.1. CSS Architecture (`static/css/style.css`)
- **Reset & Root Tokens:** Define `--bh-canvas`, `--bh-black`, `--bh-red`, `--bh-blue`, `--bh-yellow`, `--bh-green`.
- **Typography Integration:**
  - `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Space+Grotesk:wght@500;700;800&display=swap');`
- **Global Reset:** Set body background to warm canvas `#F7F5EE`, font-family to `Inter`, heading typography to `Space Grotesk`.
- **Button System:**
  - `.bh-btn`: 2px black border, 0px border-radius, hard shadow `3px 3px 0px #121212`, active push effect `translate(2px, 2px)`.
  - Color modifiers: `.bh-btn-primary` (Red), `.bh-btn-secondary` (White/Cream), `.bh-btn-accent` (Yellow), `.bh-btn-dark` (Solid Black).
- **Cards & Containers:**
  - `.bh-card`: White surface, 2px black border, 4px hard shadow.
  - `.bh-card-header`: Solid primary color banner with crisp white or black uppercase title.
- **Table Modernization:**
  - `.bh-table`: Thick outer border, inverted black headers, monospace ID/slot columns, hover highlights.
- **Status Badges:**
  - Distinct rectangular stamps: `[ EASY ]`, `[ MODERATE ]`, `[ HARD ]`, `[ OPEN ]`, `[ CLOSED ]`.

#### 1.2. Base Template Overhaul (`templates/base.html`)
- Insert Google Fonts in `<head>`.
- Replace default navbar with `.bh-navbar`:
  - Geometric accent icon (e.g. Red square + Black triangle mountain silhouette).
  - High-contrast branding: **TREK // MGMT**.
  - All-caps session status and login/logout action buttons.
- Implement Bauhaus flash messages: Solid yellow alert banner with black border and bold monospace text.
- Footer: Industrial footer block with bold uppercase copyright and version stamp.

---

### Phase 2: Authentication & Onboarding Views

#### 2.1. Login View (`templates/login.html` & `templates/index.html`)
- Convert into a Constructivist poster aesthetic:
  - Asymmetric split-screen or framed focal card with a thick 3px black border and yellow corner accent.
  - Form fields styled with `.bh-form-control` (thick black borders, crisp focus ring).
  - Submit button: Heavy `.bh-btn-primary` spanning full card width.
  - Error messages in stark black-on-yellow alert box.

#### 2.2. Register View (`templates/register.html`)
- Role selection presented as two distinct geometric blocks:
  - `[ 🥾 TREKKER ]` vs `[ 🧢 STAFF GUIDE ]` with visual radio selection.
  - Clear password requirement indicators and validation feedback.

#### 2.3. Staff Profile Completion (`templates/staff_details.html`)
- Guide certification step styled as an "Official Alpine Guide Dossier" with emergency contact and phone inputs.

---

### Phase 3: Trekker Experience & Booking Flow

#### 3.1. Trekker Dashboard (`templates/trekker_dashboard.html`)
- **Sidebar Overhaul:**
  - Replace soft pills with numbered tabs:
    - `01 // DISCOVER TREKS`
    - `02 // PROFILE DOSSIER`
    - `03 // ACTIVE EXPEDITIONS`
    - `04 // SUMMIT HISTORY`
    - `05 // TRAIL SEARCH`
  - Active tab rendered with solid black fill, yellow label, and red left indicator block.
- **Available Treks Catalog:**
  - Render as high-contrast tabular roster with columns: `INDEX`, `EXPEDITION NAME`, `TERRAIN/DIFFICULTY`, `DURATION`, `REMAINING SLOTS`, `STATUS`, `ACTIONS`.
  - Immediate visual feedback on full/sold out treks (`0 SLOTS LEFT` badge in red).
- **My Treks & History:**
  - Active bookings display a "View Trek Pass" button leading to the printable ticket.
  - Completed treks display a summit completion stamp.

#### 3.2. Booking Form (`templates/book_trek.html`)
- Transform from basic inputs into an Expedition Registration Manifest:
  - Left panel: Trek summary (Name, Duration, Altitude, Guide Name, Price).
  - Right panel: Participant details, emergency contact name, emergency phone, blood group dropdown, and confirmation button.

#### 3.3. [NEW] Digital Trek Pass (`templates/trek_pass.html`)
- Standalone printable boarding pass / trail permit:
  - Top header: Black banner with "OFFICIAL TREK PERMIT // VALIDATED".
  - Two-column layout: Route details on the left, barcode/simulated QR and booking ID on the right.
  - Print stylesheet `@media print` ensuring clean 1-page paper printout.

---

### Phase 4: Staff / Guide Operations Portal

#### 4.1. Staff Dashboard (`templates/staff_dashboard.html`)
- **Assigned Treks Summary:**
  - Top metric blocks displaying Total Assigned Expeditions and Total Guided Trekkers.
  - High-contrast list of assigned treks with a direct "Update Slots & Status" button.
- **Participant Manifest:**
  - Roster of all booked participants grouped by trek.
  - Displays participant name, email, booking date, and emergency contact details.
- **Profile Management (`templates/update_profile.html`):**
  - Guide phone number, physical address, and certifications.

#### 4.2. Edit Trek Status (`templates/edit_staff_trek.html`)
- Clean form allowing guide to alter available slots and flip status (`Open` -> `In Progress` -> `Completed` -> `Closed`).

---

### Phase 5: Admin Command Center

#### 5.1. Admin Dashboard (`templates/admin_dashboard.html`)
- **Overview Metric Grid:**
  - Five Bauhaus color-blocked stat cards:
    1. Total Treks (Cobalt Blue `#1A365D`)
    2. Certified Guides (Warm Yellow `#F6AE2D`)
    3. Pending Guide Approvals (Primary Red `#D92525`)
    4. Active Bookings (Deep Forest Green `#2D6A4F`)
    5. Blacklisted Users (Charcoal Black `#121212`)
- **Management Tabs:**
  - `01 // SYSTEM OVERVIEW`
  - `02 // TREK CATALOG (CRUD)`
  - `03 // GUIDE ROSTER & ASSIGNMENTS`
  - `04 // PENDING APPLICANTS`
  - `05 // GLOBAL BOOKINGS`
  - `06 // ACCESS CONTROL & BLACKLIST`
  - `07 // MASTER SEARCH`

#### 5.2. Admin Action Templates
- `templates/add_trek.html`: Add trek with duration, difficulty, slots, and guide assignment.
- `templates/edit_trek.html`: Modify existing catalog entries.
- `templates/assign_staff.html`: Direct guide assignment matrix.

---

## 3. Template-by-Template Migration Matrix

| Template File | Current Visual Pattern | Target Bauhaus Visual Pattern | Risk / Data Preservation |
| :--- | :--- | :--- | :--- |
| `base.html` | Default Bootstrap 5 navbar, soft gray footer | Geometric `#121212` 3px border, high-contrast typography, flash banner | Zero risk; retains `{% block content %}` and `session` checks |
| `login.html` | Centered Bootstrap card | Constructivist graphic block, 3px border, 4px hard shadow, uppercase inputs | Zero risk; maintains POST to `/login` |
| `register.html` | Standard form | Geometric role-selection toggle, bold input frames | Zero risk; preserves role assignment logic |
| `trekker_dashboard.html` | Bootstrap nav-pills, standard table | Numbered black/yellow tabs, high-contrast catalog, printable pass trigger | High attention; ensure all 5 tab targets match JS pills |
| `staff_dashboard.html` | Standard cards & simple tables | Guide manifest layout, emergency badges, status toggle buttons | Zero risk; preserves guide query filters |
| `admin_dashboard.html` | Standard Bootstrap tabs | Color-blocked metric grid, stark tabular CRUD views, danger action buttons | High attention; preserve all URL parameter tab switching |
| `book_trek.html` | Basic form | Expedition reservation dossier with emergency details | Low risk; preserves booking creation logic |

---

## 4. Verification & Testing Protocol

1. **RBAC Security Pass:**
   - Attempt accessing `/admin-dashboard` as a trekker -> Confirm redirect to `/login`.
   - Attempt accessing `/staff-dashboard` as a trekker -> Confirm redirect to `/login`.
   - Attempt accessing protected routes while blacklisted -> Confirm denied.
2. **Booking & Slot Math Invariance:**
   - Book a trek with 5 available slots -> Verify slots decrement to 4 immediately.
   - Cancel the booking -> Verify slots increment back to 5.
   - Attempt booking a trek with 0 slots -> Verify warning alert and prevented submission.
3. **Bauhaus Design System Consistency:**
   - Verify zero rounded corners (`border-radius: 0px`).
   - Verify all buttons display the `3px 3px 0px #121212` hard drop-shadow.
   - Verify all table headers are rendered with solid black inverted style.
   - Test responsive layout on 375px (mobile), 768px (tablet), and 1440px (desktop).

