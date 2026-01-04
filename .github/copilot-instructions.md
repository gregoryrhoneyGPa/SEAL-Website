# Copilot Instructions for SEAL Website Codebase

## Project Overview
- This codebase is a hybrid static/dynamic website for SEAL Enterprises, with automation scripts for content, PDF, and image processing.
- Major components: HTML pages (site content), Python/PowerShell/JS automation scripts, and supporting assets (images, CSVs, configs).
- No central build system; workflows are script-driven and file-based.

## Key Workflows
- **Accessibility Check:**
  - Run `.\scripts\check-a11y.ps1` (PowerShell) or `.\scripts\check-a11y.bat` (CMD) to invoke `tools/basic_a11y_check.py`.
- **Social Links Update:**
  - Use `.\scripts\set-social-links.ps1` to interactively update social icons in `Index.html`.
- **Image Optimization:**
  - From repo root: `npm install` then `npm run optimize` (see `tools/README.md`).
  - Reads from `images/canva/originals`, writes to `images/canva/optimized`, outputs `report.json`.
- **Lighthouse Audits:**
  - Use `.\tools\run-lighthouse.ps1` (PowerShell) to run audits; see `tools/README.md` for options (e.g., `-TargetHost`, `-ChromePath`).
- **Prototype Preview:**
  - In `deliverable/`, run `npm install` then `npm run serve` to preview `prototype/index.html`.
  - Capture blocked sites: `npm run capture:blocked` (uses Playwright, outputs to `inspiration_pages`).

## Conventions & Patterns
- Scripts are intended for local use; always back up before running automation.
- HTML files are often duplicated for backup/versioning (e.g., `about.html`, `about.html.bak`).
- Configs and credentials use `.template` suffix for safe sharing (e.g., `email_config.txt.template`).
- Python scripts are used for PDF, CSV, and Google Sheets automation (see files like `fora_automation.py`, `generate_fora_section.py`).
- PowerShell is preferred for Windows automation; some scripts have `.bat` wrappers for CMD.
- Node.js tools are used for image and Lighthouse workflows; ensure Node/npm are installed.

## Integration Points
- Google Sheets/Drive APIs (see `fora_google_sheets_automation.py`).
- Playwright for headless browser automation (`capture_playwright.js`).
- Image processing via Node.js (`sharp` dependency).

## Examples
- To optimize images:
  ```
  npm install
  npm run optimize
  ```
- To run a Lighthouse audit:
  ```
  .\tools\run-lighthouse.ps1 -TargetHost "http://localhost:8000" -OutDir "." -Desktop
  ```
- To update social links:
  ```
  .\scripts\set-social-links.ps1
  ```

## References
- See `tools/README.md`, `scripts/README.md`, and `deliverable/README.md` for more details and usage examples.
- Key automation scripts: `fora_automation.py`, `generate_fora_section.py`, `convert_fora_pdfs.ps1`, `capture_playwright.js`.

---

If you add new workflows or conventions, update this file to keep AI agents productive.
