---
name: Aura Luminary
colors:
  surface: '#131317'
  surface-dim: '#131317'
  surface-bright: '#39393e'
  surface-container-lowest: '#0e0e12'
  surface-container-low: '#1b1b20'
  surface-container: '#1f1f24'
  surface-container-high: '#2a292e'
  surface-container-highest: '#353439'
  on-surface: '#e4e1e8'
  on-surface-variant: '#d0c5b5'
  inverse-surface: '#e4e1e8'
  inverse-on-surface: '#303035'
  outline: '#998f81'
  outline-variant: '#4d463a'
  surface-tint: '#e4c284'
  primary: '#f6d393'
  on-primary: '#412d00'
  primary-container: '#d9b77a'
  on-primary-container: '#5f4715'
  inverse-primary: '#745a27'
  secondary: '#cac6bc'
  on-secondary: '#323029'
  secondary-container: '#49473f'
  on-secondary-container: '#b9b5ab'
  tertiary: '#d8d6e4'
  on-tertiary: '#302f3a'
  tertiary-container: '#bcbac8'
  on-tertiary-container: '#4b4a56'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdea6'
  primary-fixed-dim: '#e4c284'
  on-primary-fixed: '#271900'
  on-primary-fixed-variant: '#5a4311'
  secondary-fixed: '#e7e2d7'
  secondary-fixed-dim: '#cac6bc'
  on-secondary-fixed: '#1d1c15'
  on-secondary-fixed-variant: '#49473f'
  tertiary-fixed: '#e3e1ef'
  tertiary-fixed-dim: '#c7c5d3'
  on-tertiary-fixed: '#1b1b25'
  on-tertiary-fixed-variant: '#464651'
  background: '#131317'
  on-background: '#e4e1e8'
  surface-variant: '#353439'
typography:
  display:
    fontFamily: Newsreader
    fontSize: 56px
    fontWeight: '400'
    lineHeight: 64px
    letterSpacing: -0.02em
  display-mobile:
    fontFamily: Newsreader
    fontSize: 36px
    fontWeight: '400'
    lineHeight: 44px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Newsreader
    fontSize: 40px
    fontWeight: '400'
    lineHeight: 48px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Newsreader
    fontSize: 28px
    fontWeight: '400'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Newsreader
    fontSize: 28px
    fontWeight: '400'
    lineHeight: 36px
  headline-sm:
    fontFamily: Newsreader
    fontSize: 22px
    fontWeight: '400'
    lineHeight: 30px
  title:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 26px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.06em
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.08em
  metric-display:
    fontFamily: Newsreader
    fontSize: 48px
    fontWeight: '400'
    lineHeight: 52px
    letterSpacing: -0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 3rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style
This design system defines an ethereal, high-end aesthetic tailored for elite artificial intelligence interfaces. It fuses cinematic digital minimalism with haute-horlogerie editorial craft. The product conveys sovereign intelligence, quiet power, and bespoke precision. 

The emotional response should evoke entering a private salon after hours: calm, focused, supremely confident, and devoid of noisy tech tropes. The interface relies on dark obsidian grounds, soft luminescence, frosted crystal finishes, and surgical champagne gold accents to signify extreme value and calculated clarity.

## Colors
The system is strictly dark-mode-first, architected around low-light depth, high-contrast readability, and restrained warmth.

- **Obsidian Ground (`#07070B`):** The primary canvas base, grounding the UI in limitless void depth.
- **Champagne Gold (`#D9B77A`):** The solitary focal accent. Reserved strictly for primary callouts, verified AI states, key metrics, and high-tier activations. Avoid oversaturation; use it as a pinpoint of light.
- **Ivory Main Text (`#F4F1EA`):** High-luminosity text for maximum legibility and editorial warmth against the obsidian void.
- **Muted Alabaster Secondary (`#B8B4AA`):** Subdued supporting text, metadata, and structural outlines.
- **Surface Translucency (`rgba(255, 255, 255, 0.04)`): The primary glass plane.
- **Hairline Chrome Borders (`rgba(255, 255, 255, 0.09)`): Crisp micro-contrast barriers.
- **Functional Semantics:**
  - **Success / Equilibrium:** `#4ADE80` (Muted Emerald)
  - **Attention / Compute:** `#FBBF24` (Warm Amber)
  - **Critical / Interruption:** `#FB7185` (Soft Rose)
  Always accompany semantic signals with an icon and micro-label to preserve refined clarity without garish fills.

## Typography
The system balances literary elegance with technical precision.

- **Headlines & Display:** Set in Newsreader (italicized accents encouraged for prompts or generative outputs). It provides an authoritative, humanistic contrast to the AI substrate.
- **Body & Data:** Set in Inter with enabled tabular figures (`tnum`) and slashed zeros (`cv01`) for data visualization, tokens, latencies, and system analytics.
- **Labels & Microcopy:** Inter, uppercase with increased tracking (`letter-spacing: 0.06em` to `0.08em`), establishing crisp legibility at small optical sizes.

## Layout & Spacing
A fluid 12-column responsive grid on desktop with generous page margins, compressing to a 6-column grid on tablet, and a 4-column flow on mobile screens.

Generous spatial voids are treated as active elements. Avoid high-density dashboard packing. Large margins around glass containers reinforce the sense of luxury and curated exclusivity. Divider lines must be minimal, 1px hairlines (`rgba(255, 255, 255, 0.06)`), and used only when spatial separation alone is insufficient.

## Elevation & Depth
Depth is created through light refraction, glass translucency, and atmospheric gradient backdrops rather than traditional drop shadows.

- **Base Layer:** `#07070B` matte canvas.
- **Level 1 (Glass Panes):** `background: rgba(255, 255, 255, 0.04)`, `backdrop-filter: blur(16px)`, surrounded by a perimeter hairline stroke of `1px solid rgba(255, 255, 255, 0.09)`.
- **Level 2 (Hover / Elevated Popovers):** `background: rgba(255, 255, 255, 0.07)`, `backdrop-filter: blur(24px)`, with an ambient diffuse glow: `box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 20px 0 rgba(217, 183, 122, 0.05)`.
- **Level 3 (Modal / Overlays):** `background: #0E0E15`, `border: 1px solid rgba(255, 255, 255, 0.12)`, `box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.9)`.

## Shapes
Primary cards, content panes, and modal containers use an explicit 20px corner radius (`rounded-xl` token in this system), providing an organic, river-stone feel beneath the glass refraction.

Interactive secondary elements such as text fields, selection chips, and sub-panels use an 8px radius (`rounded`). Pill shapes are exclusively reserved for micro-status indicators, metadata badges, and floating action prompts.

## Components

### Buttons
- **Primary:** Background in solid Champagne Gold (`#D9B77A`), text in Obsidian (`#07070B`), font Inter 600. On hover, apply a soft radiant bloom: `box-shadow: 0 0 24px rgba(217, 183, 122, 0.35)`.
- **Secondary / Ghost:** Translucent background (`rgba(255, 255, 255, 0.04)`), text in Ivory (`#F4F1EA`), border `1px solid rgba(255, 255, 255, 0.12)`. On hover: `background: rgba(255, 255, 255, 0.08)`.

### Cards & Panels
- Constructed with `background: rgba(255, 255, 255, 0.04)`, `backdrop-filter: blur(16px)`, `border: 1px solid rgba(255, 255, 255, 0.09)`, and `border-radius: 20px`.
- Padding must default to generous scales (`space-lg` to `space-xl`).

### Input Fields
- Dark inset backgrounds (`rgba(0, 0, 0, 0.4)`), border `1px solid rgba(255, 255, 255, 0.1)`. Radius `8px`.
- Text in Ivory (`#F4F1EA`), placeholder in muted slate (`rgba(184, 180, 170, 0.4)`).
- Focus state: Border transitions to `#D9B77A` with a subtle inner glow: `box-shadow: 0 0 0 1px #D9B77A, 0 0 16px rgba(217, 183, 122, 0.15)`.

### Status Indicators & Chips
- Compact pills using `rgba(255, 255, 255, 0.03)` with `1px solid rgba(255, 255, 255, 0.08)`.
- Status indicators pair an 8px illuminated dot alongside a label in uppercase tracked Inter:
  - *Operational / Synced:* `#4ADE80` dot with matching 10% opacity glow ring.
  - *Calculating / Ingesting:* `#FBBF24` dot with gentle pulse animation.
  - *Anomaly / Suspended:* `#FB7185` dot.

### Lists & Dividers
- Lists omit alternating row colors. Separation is handled via generous vertical padding and razor-thin hairline borders (`1px solid rgba(255, 255, 255, 0.05)`).
- Metric lists display tabular numerals using `metric-display` typography, aligning values with absolute precision.

### AI Prompt & Command Bar
- A floating frosted glass pill or 20px rounded capsule (`backdrop-filter: blur(24px)`).
- Gold cursor indicator (`#D9B77A`) and whisper-quiet keyboard shortcut tags styled in micro-capsules (`rgba(255, 255, 255, 0.06)`).