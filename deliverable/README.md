Deliverable: SEAL Enterprises — Design Notes & Prototype

Contents:

- `design_notes.md` — concise findings and token suggestions.
- `implementation_plan.md` — assets list, integration steps, QA checklist.
- `prototype/` — working one-page prototype (`index.html`, `styles.css`).
- `capture_playwright.js` — headless capture script for blocked sites (saves into `inspiration_pages`).

How to preview the prototype locally:

1. Install dependencies (if not already):

```
npm install
```

2. Serve the folder and open the prototype:

```
npm run serve
```

Then open `http://localhost:8000/prototype/index.html` in your browser.

3. To run the headless captures (creates screenshots and rendered HTML in `inspiration_pages`):

```
npm run capture:blocked
```

Notes:
- The Playwright capture may still encounter anti-bot overlays; results are saved even if overlay content is present.
- I can also export a `deliverable/assets` folder with ready-to-use hero images if you approve the selected imagery.
