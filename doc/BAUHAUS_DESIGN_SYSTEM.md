# 🎨 Bauhaus UI Design System Specification
## Project: Trekking Management Application
**Design Philosophy:** Bauhaus Modernism & Constructivist Functionalism  
**Keywords:** Geometric Purity • Form Follows Function • Primary Color Blocking • Stark Asymmetry • Razor Edges  

---

## 1. Design Philosophy & Historical Anchor

The Bauhaus school (Weimar, Dessau, Berlin, 1919–1933) founded by Walter Gropius championed the synthesis of fine art, craft, and functional technology.

For our Trekking Management Application, this means:
1. **Zero Frivolous Decoration:** Eliminate soft gradient blurs, faux 3D buttons, drop shadows with gaussian blurs, and curved rounded corners.
2. **Truth to Materials:** The digital canvas is flat, structured, and modular. We expose structural borders, grid lines, and data tables with pride.
3. **High Contrast for Outdoor Clarity:** High-contrast color relationships ensure mountain trekkers, guides in the field, and administrators can navigate swiftly under varying light conditions.
4. **Geometric Hierarchy:** Fundamental shapes—the circle, the triangle, and the rectangle—anchor visual grouping.

---

## 2. Color Palette & Design Tokens

Bauhaus aesthetics are instantly recognizable by their disciplined reliance on **Primary Colors** contrasted against **Stark Black, Slate Gray, and Off-White Raw Canvas**.

```
+-------------------------------------------------------------------------------+
| PRIMARY PALETTE                                                               |
|  [ #121212 ]      [ #F7F5EE ]      [ #D92525 ]      [ #1A365D ]   [ #F6AE2D ] |
|  Bauhaus Black   Raw Canvas Cream   Primary Red      Cobalt Blue   Warm Yellow|
+-------------------------------------------------------------------------------+
```

### 2.1. Color Tokens Table

| Token Name | Hex Code | Role & Usage | Text Contrast |
| :--- | :--- | :--- | :--- |
| `--bh-canvas` | `#F7F5EE` | Primary application background (unbleached warm paper). | Dark text (`#121212`) |
| `--bh-surface` | `#FFFFFF` | Card panels, table backgrounds, and input backgrounds. | Dark text (`#121212`) |
| `--bh-black` | `#121212` | Borders, typography, primary buttons, structural rules. | Light text (`#FFFFFF`) |
| `--bh-red` | `#D92525` | Primary action buttons, urgent notices, 'Hard' difficulty, delete. | White text (`#FFFFFF`) |
| `--bh-blue` | `#1A365D` | Secondary actions, navigation accents, admin badges, info. | White text (`#FFFFFF`) |
| `--bh-yellow` | `#F6AE2D` | Attention elements, warnings, 'Moderate' difficulty, highlights. | Black text (`#121212`) |
| `--bh-green` | `#2D6A4F` | 'Easy' difficulty, confirmed booking status, success badges. | White text (`#FFFFFF`) |
| `--bh-gray-light`| `#E5E2D9` | Dividers, secondary button background, table alternate row fill.| Black text (`#121212`) |
| `--bh-gray-dark` | `#495057` | Supporting meta labels, subtitles, monospace captions. | White / Light |

---

## 3. Typography & Typesetting Rules

### 3.1. Font Hierarchy
- **Primary Display & Headings:** `Space Grotesk`, `Archivo Black`, or `Inter` (geometric sans-serif with bold letterforms).
- **Body & Forms:** `Inter`, `Helvetica Neue`, `Arial`, sans-serif (legible, neutral, rational).
- **Data, IDs & Timestamps:** `JetBrains Mono`, `Consolas`, `Courier New`, monospace (utilitarian precision).

### 3.2. Typographic Scale

| Level | Size | Weight | Tracking (Letter-Spacing) | Transform | Usage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display H1** | `2.25rem (36px)` | 800 (Bold) | `-0.02em` | Normal / Title | Major page headlines |
| **Heading H2** | `1.75rem (28px)` | 700 (Bold) | `-0.01em` | Normal | Section containers & modal headers |
| **Heading H3** | `1.25rem (20px)` | 700 (Bold) | `0em` | Uppercase | Card headers, table headings |
| **Navigation** | `0.95rem (15px)` | 600 (Semibold)| `0.05em` | Uppercase | Sidebar tabs & navbar items |
| **Body Text**  | `1.00rem (16px)` | 400 (Regular) | `0em` | Normal | Narrative copy & table cells |
| **Technical**  | `0.85rem (13.5px)`| 500 (Medium) | `0.08em` | Uppercase Monospace | Slot counter, timestamps, status tags |

---

## 4. Geometric & Structural Tokens

### 4.1. The Zero-Radius Mandate
- **Border-Radius:** Strictly `0px` (or `2px` maximum for subtle tactile finish). No pill-shaped bubbles or rounded corners.
- **Borders:** Crisp, high-contrast borders:
  - Standard border: `2px solid var(--bh-black)`
  - Heavy structural rule: `3px solid var(--bh-black)`
  - Section separator: `1px solid var(--bh-black)`

### 4.2. Neo-Brutalist Bauhaus Drop Shadows
In lieu of blurry, realistic drop shadows, Bauhaus layouts leverage **flat, hard offset shadows**:
- **Standard Card Shadow:** `box-shadow: 4px 4px 0px #121212;`
- **Elevated Button Shadow:** `box-shadow: 3px 3px 0px #121212;`
- **Active / Pressed State:** `transform: translate(2px, 2px); box-shadow: 1px 1px 0px #121212;`

---

## 5. UI Component Specifications

### 5.1. Top Navigation Bar (`.bh-navbar`)
- **Structure:** Crisp white background with a bottom border of `3px solid #121212`.
- **Branding:** Bold graphic lockup:
  - Red square or yellow circle geometric accent mark beside the logo text.
  - "TREKKING MANAGEMENT" in all-caps heavy tracking.
- **Action Buttons:** Geometric black-bordered boxes with high-contrast text.

### 5.2. Sidebar Navigation (`.bh-sidebar`)
- **Structure:** Perpendicular vertical panel with a `3px solid #121212` right border.
- **Tab Items:**
  - Prefixed with numbered indices (`01 // BOOK TREKS`, `02 // PROFILE`, `03 // MY TREKS`).
  - Active Tab: Inverted stark block (Black background `#121212` with Yellow `#F6AE2D` text and a left red accent bar).
  - Hover Tab: High-contrast yellow or cream background with immediate feedback.

### 5.3. Metric & Stat Cards (`.bh-stat-card`)
- **Structure:** Heavy `2px solid #121212` border, `4px 4px 0px #121212` hard drop-shadow.
- **Header:** Top band filled with a primary color (Cobalt Blue for Treks, Yellow for Guides, Red for Pending, Green for Bookings).
- **Stat Metric:** Massive oversized monospace number (`2.5rem`, font-weight `800`).
- **Label:** Monospace uppercase label with high tracking.

### 5.4. Data Tables (`.bh-table`)
- **Frame:** Contained within a full black border (`2px solid #121212`).
- **Header (`thead`):** Solid `#121212` background with crisp white uppercase text and thin vertical white dividers.
- **Row Styling:** Alternate row striping using `--bh-canvas` (`#F7F5EE`) and `--bh-surface` (`#FFFFFF`).
- **Hover:** Active row highlighted with pale yellow tint (`#FFF8E7`).
- **Cell Dividers:** `1px solid #121212`.

### 5.5. Buttons & Controls (`.bh-btn`)
- `.bh-btn`: `display: inline-flex; align-items: center; justify-content: center; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; border: 2px solid #121212; border-radius: 0px; box-shadow: 3px 3px 0px #121212; transition: all 0.1s ease;`
- `.bh-btn-red`: Background `#D92525`, Color `#FFFFFF`.
- `.bh-btn-blue`: Background `#1A365D`, Color `#FFFFFF`.
- `.bh-btn-yellow`: Background `#F6AE2D`, Color `#121212`.
- `.bh-btn-black`: Background `#121212`, Color `#FFFFFF`.
- `.bh-btn-white`: Background `#FFFFFF`, Color `#121212`.

### 5.6. Status Badges & Stamps (`.bh-badge`)
- Solid rectangular tags, `border: 1.5px solid #121212`, `font-family: monospace`, `padding: 2px 8px`, `font-size: 0.75rem`, `font-weight: 700`, `letter-spacing: 0.06em`.
- `Easy`: Green background (`#2D6A4F`), white text.
- `Moderate`: Yellow background (`#F6AE2D`), black text.
- `Hard`: Red background (`#D92525`), white text.
- `Confirmed`: Crisp white background, black border, green dot.
- `Cancelled / Refunded`: Gray background (`#E5E2D9`), strike-through accent.

### 5.7. Forms, Inputs & Select Boxes (`.bh-form-control`)
- **Inputs:** Thick `2px solid #121212` border, white background, razor corners (`0px`).
- **Focus State:** Inset highlight or bold yellow underline outline (`box-shadow: 3px 3px 0px #F6AE2D; border-color: #121212; outline: none;`).
- **Labels:** Bold, uppercase, accompanied by a small geometric glyph (e.g., `■ EMAIL ADDRESS`).

---

## 6. CSS Engine Architecture (`static/css/style.css`)

```css
/* Core Bauhaus Design Tokens */
:root {
    --bh-canvas: #F7F5EE;
    --bh-surface: #FFFFFF;
    --bh-black: #121212;
    --bh-red: #D92525;
    --bh-blue: #1A365D;
    --bh-yellow: #F6AE2D;
    --bh-green: #2D6A4F;
    --bh-gray-light: #E5E2D9;
    --bh-gray-dark: #495057;

    --bh-border: 2px solid var(--bh-black);
    --bh-border-thick: 3px solid var(--bh-black);
    --bh-shadow: 4px 4px 0px var(--bh-black);
    --bh-shadow-sm: 2px 2px 0px var(--bh-black);
    --bh-shadow-lg: 6px 6px 0px var(--bh-black);

    --font-heading: 'Space Grotesk', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-body: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

body {
    background-color: var(--bh-canvas);
    color: var(--bh-black);
    font-family: var(--font-body);
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
}
```

---

## 7. Responsive & Print Considerations

- **Mobile Viewport (< 768px):** The rigid sidebar collapses cleanly into an accordion horizontal navigation bar with full-width primary buttons and compact hard shadows (`2px 2px 0px #121212`).
- **Print Optimization (`@media print`):** Background colors convert cleanly to high-contrast monochrome linework, ensuring digital trek passes can be printed on any thermal or home printer without wasting ink while retaining unmistakable Bauhaus linework.

