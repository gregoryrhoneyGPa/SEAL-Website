**Design Notes — SEAL Enterprises redesign**

- **Purpose:** modernize `sealenterprises.net` with a travel‑market look: large immersive hero, clear search/CTA, high‑contrast primary CTA, and streamlined nav.

- **Sources reviewed:** Travelzoo, Kayak, Expedia (rendered), Abercrombie & Kent, Vacationstogo, SealEnterprises (current).

- **Hero treatments (recommended):**
  - Full‑bleed background (photo or gradient with subtle texture). Prefer a soft dark overlay for readable text.
  - Large, bold headline (approx 40–56px desktop), compact subhead (16–20px), and a single primary CTA + secondary link.
  - Optional search bar or single-line lead capture centered under headline for conversions.

- **Typography:**
  - Use a geometric/modern heading face (e.g., Centra-like or system Inter stack: `Inter, system-ui, -apple-system, 'Segoe UI'`).
  - Body: neutral sans (system stack or Google Open Sans/Inter). Maintain strong contrast and 1.4 line-height.

- **Color tokens (proposal):**
  - `--color-primary`: #1668E3 (deep travel blue)
  - `--color-accent`: #FFB800 (warm yellow accent)
  - `--color-bg`: #0f1724 (dark hero background) / white for content background
  - `--color-muted`: #94A3B8 (muted text)

- **CTA style:** pill / rounded rectangle (24–28px radius), bold text, clear hover state (slightly darker primary). Primary CTA filled, secondary outlined or ghost.

- **Layout & spacing:** centered content, max-width 1100px, generous vertical padding for hero (min 80–120px desktop). Use CSS variables for spacing scale.

- **Imagery & assets:** large hero images (16:9 or 3:2), photography with people/landscapes, optimized to WebP/AVIF where possible. Provide fallback color gradient.

- **Components to build:**
  - Hero (desktop + mobile)
  - Global header (logo left, links right, mobile hamburger)
  - Primary CTA component (filled/ghost)
  - Search / quick lead capture block
  - Card grid for featured deals (image + headline + price)

- **Accessibility notes:**
  - CTAs must have >= 4.5:1 contrast on normal text; larger text AB 3:1 allowed for ≥18px.
  - Headings use semantic tags (h1 → h2). Navigation uses landmark elements and skip link.
  - Forms should include visible labels and focus outlines.

- **Next steps:**
  1. Review these tokens and confirm brand color preference.
  2. Integrate `prototype/index.html` into a staging folder and iterate assets.
  3. Optionally run Playwright captures for remaining blocked sites and add screenshots to `inspiration_pages`.

---

Files added:

- [prototype/index.html](prototype/index.html)
- [prototype/styles.css](prototype/styles.css)

If you want, I can also create a small exported image asset and a ready-to-paste snippet for your Wix templates.
