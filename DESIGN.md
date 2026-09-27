---
name: Bauhaus Modernist 1919
colors:
  surface: '#FFFFFF'
  surface-dim: '#EFECE6'
  surface-bright: '#FFFFFF'
  surface-container-lowest: '#FFFFFF'
  surface-container-low: '#F7F5EE'
  surface-container: '#FAF8F2'
  surface-container-high: '#EFECE6'
  surface-container-highest: '#D8D4CA'
  on-surface: '#121212'
  on-surface-variant: '#495057'
  inverse-surface: '#18181D'
  inverse-on-surface: '#F4F4F0'
  outline: '#121212'
  outline-variant: '#383842'
  surface-tint: '#D92525'
  primary: '#D92525'
  on-primary: '#FFFFFF'
  primary-container: '#BE1E1E'
  on-primary-container: '#FFFFFF'
  inverse-primary: '#E63946'
  secondary: '#1A365D'
  on-secondary: '#FFFFFF'
  secondary-container: '#142742'
  on-secondary-container: '#FFFFFF'
  tertiary: '#F6AE2D'
  on-tertiary: '#121212'
  tertiary-container: '#FFBE0B'
  on-tertiary-container: '#121212'
  error: '#D92525'
  on-error: '#FFFFFF'
  error-container: '#FEE2E2'
  on-error-container: '#991B1B'
  background: '#F7F5EE'
  on-background: '#121212'
  surface-variant: '#FAF8F2'
typography:
  display-xl:
    fontFamily: Space Grotesk
    fontSize: 56px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.3'
  body-md:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '500'
    lineHeight: '1.5'
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1.4'
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1.0'
    letterSpacing: 0.08em
rounded:
  sm: 0px
  DEFAULT: 0px
  md: 0px
  lg: 0px
  xl: 0px
  full: 0px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 32px
  xl: 48px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

# 🎨 Bauhaus Modernist Design System (1919 Weimar)
### *Trekking Management Platform • Form Follows Function • Pure Constructivism*

## 1. Brand Philosophy & Aesthetic Identity

The design system for the **Alpine Trekking Management Platform** is rooted in the early 20th-century **Bauhaus movement (Weimar, 1919)** founded by Walter Gropius. In an era where modern software often relies on decorative glassmorphism, soft gradients, and arbitrary rounded cards, this design system establishes a bold, structural, constructivist counter-statement:

* **Form Follows Function**: Every line, border, color, and typographic hierarchy exists solely to convey operational utility and alpine safety.
* **The Zero-Radius Mandate (`0px`)**: Complete rejection of rounded corners (`border-radius: 0px !important`). All buttons, modals, input containers, badges, and cards maintain razor-sharp 90-degree corners.
* **Hard Offset Shadows**: Shadows use zero Gaussian blur (`box-shadow: 4px 4px 0px #121212`), creating tactile architectural depth reminiscent of letterpress printing and constructivist lithography.
* **Primary High-Contrast Palette**: Unapologetic use of saturated primary pigments—Carmine Red (`#D92525`), Cobalt Blue (`#1A365D`), and Chrome Yellow (`#F6AE2D`)—anchored by Stark Ink Black (`#121212`) and Unbleached Canvas Cream (`#F7F5EE`).

---

## 2. Color Palette & Thematic Matrix

The platform features full dual-mode parity with seamless synchronization across Light and Dark themes.

### Light Theme (Default Bauhaus Weimar)
| Token | Hex Value | Usage / Role |
| :--- | :--- | :--- |
| `--bh-canvas` | `#F7F5EE` | Primary application canvas (unbleached paper cream). |
| `--bh-surface` | `#FFFFFF` | Elevated cards, tables, navigation bars, and inputs. |
| `--bh-black` | `#121212` | High-contrast text, primary structural borders, and hard shadows. |
| `--bh-red` | `#D92525` | Carmine Red for primary calls-to-action, warnings, and deletions. |
| `--bh-blue` | `#1A365D` | Cobalt Blue for guide verification, credentials, and secondary links. |
| `--bh-yellow` | `#F6AE2D` | Chrome Yellow for hover states, expedition warnings, and highlights. |
| `--bh-green` | `#2D6A4F` | Alpine Pine Green for confirmed permits, active guides, and safety checks. |
| `--bh-border-color` | `#121212` | 2px to 3px solid ink boundaries on all interactive elements. |

### Dark Theme (Bauhaus Obsidian)
| Token | Hex Value | Usage / Role |
| :--- | :--- | :--- |
| `--bh-canvas` | `#0F0F12` | Deep obsidian background. |
| `--bh-surface` | `#18181D` | Surface containers and card bodies. |
| `--bh-black` | `#F4F4F0` | Primary foreground text (chalk white). |
| `--bh-border-color` | `#383842` | Crisp charcoal architectural border lines. |
| `--bh-red` | `#E63946` | High-visibility neon signal red. |
| `--bh-blue` | `#3A86FF` | Electric cobalt for secondary actions. |
| `--bh-yellow` | `#FFBE0B` | Signal amber for alerts and active buttons. |
| `--bh-green` | `#06D6A0` | Neon mint green for verified status. |

---

## 3. Typographic Hierarchy

Typography is structured into three specialized typographic voices:

| Family | Classification | Usage |
| :--- | :--- | :--- |
| **Space Grotesk** | Geometric Display | Section headers, brand identity, navigation titles, and KPI values. |
| **Inter** | Neutral Humanist | Form inputs, data tables, administrative labels, and body descriptions. |
| **JetBrains Mono** | Industrial Monospace | Cryptographic hashes, permit booking codes, telemetry data, and dates. |

### Scale Matrix
* **Display XL (`56px / 800`)**: Hero landings, trek title headers. Letter spacing: `-0.02em`.
* **Headline LG (`32px / 700`)**: Dashboard section headers, administrative portals.
* **Headline MD (`24px / 700`)**: Card headers, expedition detail view headers.
* **Body MD (`15px / 500`)**: Standard content paragraphs, descriptions. Line height: `1.5`.
* **Code / Telemetry (`13px / 600`)**: Permit codes (`TRK-2026-X99`), SHA-256 signatures, slots.
* **Label Caps (`12px / 700`)**: Form field labels (`■ EMAIL ADDRESS`), difficulty badges, table headers (`UPPERCASE`).

---

## 4. Spacing, Elevation & Shadows

### Structural Spacing System
Built on a 4px base increment (`4px`, `8px`, `16px`, `24px`, `32px`, `48px`).
* **Desktop Content Margin**: Generous padding (`2.75rem 3.5rem`) on dashboard workspaces.
* **Inner Container Max-Width**: `1500px` centered to maintain readability on ultra-wide screens.
* **Card Bottom Margin**: `2.25rem` consistent rhythm across all views.

### Hard Offset Shadows (Zero Blur)
* **Shadow XS**: `1px 1px 0px var(--bh-shadow-color)` — small badges, chips.
* **Shadow SM**: `2px 2px 0px var(--bh-shadow-color)` — secondary buttons, form controls.
* **Shadow Default**: `4px 4px 0px var(--bh-shadow-color)` — cards, hero widgets, primary buttons.
* **Shadow LG**: `6px 6px 0px var(--bh-shadow-color)` — authentication containers, modal windows.

---

## 5. Component Library & Patterns

### 1. Navigation Monolith (`.bh-navbar`, `.sidebar-nav`)
* Fixed at top with `z-index: 1050`, 3px bottom border, and hard shadow.
* Numbered section items (`01 // EXPEDITIONS`, `02 // GUIDES`, `03 // PERMITS`).
* Integrated Theme Switcher with stabilized width (`122px`) preventing horizontal layout shift during toggle.

### 2. Buttons (`.bh-btn`)
* Bold uppercase lettering with `0.06em` letter spacing.
* Primary button fills with Carmine Red (`#D92525`); on hover, shifts `translate(-1px, -1px)` with elevated 3px shadow.
* Active press transitions to `translate(2px, 2px)` with shadow compression.
* Scoped `transform` and `box-shadow` transitions only, preventing color fade lag during theme switching.

### 3. Stat & KPI Blocks (`.bh-stat-card`)
* Top 6px color-accent stripe (Carmine Red, Cobalt Blue, or Chrome Yellow).
* Massive geometric numbers in Space Grotesk.
* Monospace sub-labels with uppercase descriptions.

### 4. Digital Trekking Permit Pass (`.bh-pass-container`)
* Architectural industrial pass format engineered for both screen and `@media print` DIN A4 voucher printing.
* Built-in interactive 3D holographic seal powered by Three.js WebGL.
* Cryptographic SHA-256 verification string and QR layout block.

### 5. Interactive Three.js 3D Topographic Radar
* Real-time low-poly wireframe mountain mesh responding to mouse orbit and theme shifts.
* Multi-mode difficulty morphing between Easy, Moderate, and Alpine Hard elevation contours.
