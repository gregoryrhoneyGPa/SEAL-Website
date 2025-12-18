Scripts

`check-a11y.bat` / `check-a11y.ps1`
- Runs the project's basic Python accessibility checker (`tools/basic_a11y_check.py`).
- Usage (PowerShell):

  .\scripts\check-a11y.ps1

- Usage (double-click or CMD):

  .\scripts\check-a11y.bat

`set-social-links.ps1`
- Interactive script to update the social icon links in `Index.html`.
- It prompts for Facebook, Instagram and LinkedIn URLs. Use local mock pages or real profile URLs.
- Usage (PowerShell):

  .\scripts\set-social-links.ps1

`start-server.ps1` / `start-server.bat`
- Starts a local HTTP server (Python's `http.server`) in a new PowerShell window and opens the site homepage.
- Usage (PowerShell):

  .\scripts\start-server.ps1

- Usage (double-click / cmd):

  .\scripts\start-server.bat

Notes
- These scripts are for local use on your laptop. Keep the repo working copy backed up before running.

Recent edits (2025-12-17):
- Updated hero image handling to improve Largest Contentful Paint (LCP):
  - Added a preload link for the hero image in `V1/Index.html`:
    `<link rel="preload" href="images/canva/hero-home.webp" as="image" />`
  - Switched the hero background reference in `V1/css/styles.css` to the optimized WebP at `../images/canva/hero-home.webp`.
  - These are safe, non-destructive changes intended to make the hero image discoverable earlier and improve LCP. Backups of edited pages were preserved as `.original.html` during earlier edits.

If you'd like, I can also:
- Add `fetchpriority="high"` and `loading="eager"` to inlined `<img>` hero markup where applicable.
- Add a short note about cache recommendations (long cache TTLs for images + filename-based cache-busting).
