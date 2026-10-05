---
name: Orbital Telemetry & Vision-Language Operations
colors:
  surface: '#0e131e'
  surface-dim: '#0e131e'
  surface-bright: '#343946'
  surface-container-lowest: '#090e19'
  surface-container-low: '#171b27'
  surface-container: '#1b1f2b'
  surface-container-high: '#252a36'
  surface-container-highest: '#303541'
  on-surface: '#dee2f2'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dee2f2'
  inverse-on-surface: '#2b303c'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#48d7f9'
  on-secondary: '#003641'
  secondary-container: '#01b8d9'
  on-secondary-container: '#004451'
  tertiary: '#eef7ff'
  on-tertiary: '#00354a'
  tertiary-container: '#aee0ff'
  on-tertiary-container: '#00668b'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#afecff'
  secondary-fixed-dim: '#48d7f9'
  on-secondary-fixed: '#001f27'
  on-secondary-fixed-variant: '#004e5d'
  tertiary-fixed: '#c4e7ff'
  tertiary-fixed-dim: '#7bd0ff'
  on-tertiary-fixed: '#001e2c'
  on-tertiary-fixed-variant: '#004c69'
  background: '#0e131e'
  on-background: '#dee2f2'
  surface-variant: '#303541'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Space Grotesk
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: 0em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
  title-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.04em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.06em
  label-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-tablet: 1.5rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1.25rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes a high-density, mission-critical operational cockpit for orbital analytics, satellite ground-station telemetry, and real-time vision-language reasoning. The emotional core balances sovereign precision, deep-space focus, and instant situational awareness. 

The aesthetic synthesizes:
- **Orbital Glassmorphism & HUD Reticles:** High-translucency obsidian overlays, 1px photon edge-highlights, faint coordinate tracking lines, and radial sweep visual cues.
- **Deep Technical Minimalism:** Absolute contrast between black-void foundations and laser-calibrated luminescence, omitting ornamental clutter in favor of high-fidelity data density.
- **Optoelectronic Feedback:** Luminescent telemetry states (cyan lock, emerald nominal, amber divergence, crimson fault) paired with restrained photonic bloom shadows that indicate dynamic satellite tracking status and orbital pipeline activity.

## Colors

The chromatic architecture is engineered strictly for dark environments to preserve operator visual endurance over prolonged tactical observation:

- **Foundation Tiers:** Canvas base relies on Void Black (`#05070D`), stepping into Deep Orbit Navy (`#0B101B`) for module containers, and Sub-Orbital Slate (`#121B2A`) for elevated glass HUD panels. 
- **Luminescent Accents:** 
  - `primary` (`#00F0FF` - Electric Cyan): Active vector paths, focus reticles, conversational target locks, and AI query confirmation states.
  - `secondary` (`#00B8D9` - High-Velocity Cyan): Orbital pipeline tracks, secondary node connectors, and HUD grid dividers.
  - `tertiary` (`#38BDF8` - Sky Plasma): Interactive hover states, telemetry stream metadata, and tertiary icon strokes.
- **Telemetry Indicators:**
  - `Nominal Orbit` (`#10B981` / Emerald): Sensor synchronization, intact telemetry locks, and normal thermal baselines.
  - `Orbital Warning` (`#F59E0B` / Solar Amber): High solar flare flux, jitter drift, and tracking degredation.
  - `Critical Vector` (`#EF4444` / Supernova Crimson): Collision trajectory warning, sensor loss, and payload fault.
- **Contrasting Neutrals:** Deep space slate borders (`#1E293B` at 40-70% alpha) provide structural containment, while primary text utilizes Star White (`#F8FAFC`) down to Telemetry Muted (`#64748B`) for technical timestamps and azimuth labels.

## Typography

The typographic hierarchy couples geometric futurism with monospaced legibility:

- **Headlines & Mission Trackers (Space Grotesk):** Delivers clean aeronautical structure. Characterized by wide proportions and technical angles, applied to situational titles, mission identifiers, and major visual modals.
- **Conversational & Operations Body (Plus Jakarta Sans):** Provides maximum legibility for vision-language AI interactions, mission intelligence synthesis, and rapid descriptive reading under time-sensitive operations.
- **Telemetry & Spatial Coordinates (JetBrains Mono):** Dedicated to high-velocity numerical streams, ephemeris data, azimuth/elevation readouts, latitude/longitude matrices, and system diagnostic logs. All telemetry labels mandate tabular figures and uppercase tracking.

## Layout & Spacing

The layout is built upon a high-density, 12-column dynamic command matrix designed for seamless visual-language interaction and panoramic multispectral telemetry:

- **Desktop & Multi-Monitor Operations (≥ 1440px):** 12-column layout with 2rem margins and 1.5rem gutters. Rigid 3-tier partitioning: Left module (Telemetry & Ephemeris Tree, 3 cols), Center module (Main Optical/SAR Sensor Viewport & Bounding Box HUD, 6 cols), Right module (Vision-Language AI Prompt & Query Response Console, 3 cols).
- **Tablet Tactical Cockpit (768px - 1439px):** 8-column layout with 1.5rem margins and 1rem gutters. Viewport pins to the top; Telemetry and AI Query tools split dynamically via docked bottom drawers or side-by-side tabs.
- **Mobile Handheld Relay (< 768px):** 4-column layout with 1rem margins. Collapses into single-stream situational tabs: (1) Target Visual, (2) Direct Query AI, (3) Telemetry Status.
- **Rhythm & Padding:** Component internal spacing uses a tight 4px base increment (`space-xs` to `space-xl`) to maximize data density while preserving distinct cognitive boundaries.

## Elevation & Depth

Visual depth is achieved through layered translucent plates and photon-emissive glow states rather than traditional ambient shadows:

- **Surface Layers:**
  - **Base Canvas:** Solid Void Black (`#05070D`).
  - **Level 1 (Docked Consoles & Grids):** `#0B101B` with 80% opacity and `backdrop-filter: blur(12px)`. Outlined with 1px solid `rgba(56, 189, 248, 0.12)`.
  - **Level 2 (Active HUD Cards & Modals):** `#121B2A` with 70% opacity and `backdrop-filter: blur(20px)`. Outlined with 1px solid `rgba(0, 240, 255, 0.25)`.
- **Electroluminescent Glows (Drop Shadows):**
  - **Target Focus & Active Locks:** `0 0 16px rgba(0, 240, 255, 0.35), 0 0 2px #00F0FF`.
  - **Telemetry Nominal State:** `0 0 10px rgba(16, 185, 129, 0.3)`.
  - **Warning / Fault State:** `0 0 14px rgba(239, 68, 68, 0.4)`.
- **Pipeline & Tracking Dividers:** Rendered via 1px linear gradients running horizontally or vertically: `linear-gradient(90deg, transparent, rgba(0, 240, 255, 0.4) 50%, transparent)`.

## Shapes

The interface embraces a chamfered, precision-cut aerospace posture:

- **Corners (`roundedness: 1`):** Base components utilize an exact 0.25rem (4px) curvature, preventing the soft, consumer-grade appearance of high radii while eliminating raw harshness. Larger container cards scale to 0.5rem (`rounded-lg`).
- **HUD Reticles & Cut Corners:** Tactical modules and telemetry badges feature subtle 45-degree corner chamfers (clip-paths) or corner crosshair marks (`+` indices) at panel vertices to maintain an authentic flight-deck instrumentation feel.
- **Pipeline Nodes:** Sensor tracks and pipeline nodes utilize pure circular or 45-degree diamond glyphs for state progression.

## Components

### Buttons & Interactive Triggers
- **Primary Operational Button:** Electric Cyan background (`#00F0FF`) with Void Black text (`#05070D`), bold Space Grotesk typography, 4px corner radius, and an active outer cyan glow (`0 0 12px rgba(0, 240, 255, 0.4)`).
- **Secondary / HUD Button:** Translucent `#0B101B` background, 1px border of `rgba(0, 240, 255, 0.4)`, cyan text. On hover, background shifts to `rgba(0, 240, 255, 0.1)` with 100% border opacity.
- **Critical Action Button:** Deep dark crimson background with neon red border (`#EF4444`) and subtle red photonic halo.

### Telemetry Badges & Chips
- Monospace JetBrains Mono tracking indicators, padded tightly (`0.25rem 0.5rem`).
- Enclosed in a 1px border with a matching pulsing neon status dot (e.g., `#10B981` Emerald for `AOS: LOCKED`, `#F59E0B` Amber for `DOPPLER DRIFT`).

### Vision-Language Input Fields
- Chat and reasoning query bars sit inside a glassmorphic container (`#0B101B` at 85% opacity, blur 16px).
- Input field displays prompt cursor with cyan tint, surrounded by 1px ghost boundary `rgba(56, 189, 248, 0.2)`.
- Active focus expands a dual glow ring (`0 0 0 1px #00F0FF, 0 0 8px rgba(0, 240, 255, 0.25)`). Includes shortcut token tags (e.g., `[TARGET: SAT-4A]`, `[BAND: SAR]`).

### Cards & Telemetry Containers
- Double-lined corner accents on top-left and bottom-right edges to mimic tactical reticle displays.
- Header bands formatted in JetBrains Mono uppercase labels, separated from container body by a glowing laser divider.

### Checkboxes & Radios
- Sharp, square components (2px corner radius) with micro crosshair checkmarks.
- Radio buttons feature dual concentric rings: an outer translucent cyan rim with an inner solid photon core when selected.

### Satellite-Specific Modules
- **Optical/SAR Viewport Bounding HUD:** Highlighting boxes overlaying imagery in 1px dashed or solid electric cyan with pinpoint coordinates displayed on the top edge in `label-sm`.
- **Pipeline Track Lines:** Dynamic SVG connective rails with animated glowing dashes indicating real-time neural inference streaming between ground terminal, edge processor, and orbit payload.