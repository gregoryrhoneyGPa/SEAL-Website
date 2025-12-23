**Implementation Plan — SEAL Enterprises Redesign**

1) Assets to prepare
  - Hero photography: 3 optimized variants (desktop 1920×1080, tablet 1200×675, mobile 800×450) exported as WebP + fallback JPG.
  - Logo SVG and 2 raster sizes (retina & standard).
  - CTA icon set (SVGs): arrow, phone, envelope.
  - Sample card imagery (3 landscape crops) optimized for 400×250.

2) CSS variables (starter)
  - `--color-primary: #1668E3`
  - `--color-accent: #FFB800`
  - `--color-bg: #0f1724`
  - `--color-muted: #94A3B8`
  - `--max-width: 1100px`
  - `--radius: 20px`

3) Integration steps (Wix)
  - Header: replace current header with a slim sticky header. In Wix editor, use site header strip, add text element for logo and add menu element aligned right.
  - Hero: add a full-width strip section at top. Set background to chosen hero image and add overlay using color + transparency. Add text elements (H1/H2) and a button element for CTAs.
  - Lead capture/search: add a single-line input and button below hero text. On submit, route to contact page or open a lightbox form using Wix built-in lightbox.
  - Cards: use a repeater element for deals; bind images + text and a CTA.
  - Mobile: ensure mobile layout stacks; hide wide search form and show compact input + CTA.

4) Performance & accessibility
  - Image formats: WebP/AVIF first, fall back to JPEG. Add width/hint attributes and lazy-loading for below‑the‑fold images.
  - Fonts: prefer system stack for speed; if using web fonts, preload the most-critical font variants.
  - Contrast: verify CTAs meet WCAG AA (use contrast-checker during QA).

5) Deployment checklist
  - QA the prototype locally: `npm run serve` then open `/prototype/index.html`.
  - Replace hero assets in Wix site manager and update CSS tokens in the editor (use theme colors).
  - Test on mobile devices and run Lighthouse to confirm accessibility and performance.

6) Notes
  - If you want, I can export the hero image variants and provide downloadable assets in a `deliverable/assets` folder.
