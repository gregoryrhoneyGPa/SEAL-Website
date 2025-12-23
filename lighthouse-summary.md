# Lighthouse Summary — http://localhost:8000/

## Snapshot
- Fetch time: 2025-12-19 (report)
- Lighthouse version: 13.0.1

## Scores
- Performance: 1.00 — Excellent. Key metrics (report):
  - First Contentful Paint (FCP): ~750 ms (0.8 s)
  - Largest Contentful Paint (LCP): ~757 ms (0.8 s)
  - Speed Index: ~750 ms (0.8 s)
- Accessibility: 0.86 — Good but has actionable issues.
- Best Practices: 0.96 — Mostly fine; minor items to check.

## Top Opportunities / Findings
- Performance
  - Overall score is strong; keep monitoring Core Web Vitals.
  - Typical opportunities to inspect (even with a 1.0 score): image delivery (responsive/formats), caching/HTTP cache headers, render-blocking JS/CSS, and unused JS/CSS.
- Accessibility (score 0.86)
  - Relevant checks with non-zero weight in the report: `color-contrast`, `document-title`, `html-has-lang`, `html-lang-valid`, `link-name`, `list` / `listitem`, `target-size`, `heading-order`, `landmark-one-main`.
  - Actionable next steps: ensure page `lang` attribute is set and valid; verify document title and descriptive link text; fix color contrast failures; ensure touch target sizes and provide a single `<main>` landmark and correct heading semantics; follow up with manual accessibility testing.
- Best Practices (score 0.96)
  - `is-on-https` passes. Review minor flagged items such as console errors, deprecations, third-party cookie usage, and paste-preventing-inputs if relevant.

## Recommended Next Steps
1. Run a focused accessibility sweep (axe/pa11y + manual testing) and fix prioritized a11y failures.
2. Maintain current performance settings; periodically re-run Lighthouse when deploying content changes.
3. Review best-practices flagged audits (console errors, third-party cookies, deprecated APIs) and remediate as needed.

## Artifacts
- Extracted category files added:
  - `lighthouse-performance.json`
  - `lighthouse-accessibility.json`
  - `lighthouse-best-practices.json`

(If you want, I can open the specific audit results and extract the top failing audit details for each category.)
