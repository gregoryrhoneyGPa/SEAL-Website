Deployment checklist — SEAL Enterprises

Purpose
- Final checklist to safely merge local improvements (accessibility, structured data, scripts) with the live Canva site and push updates to production.

Pre-merge steps (local)
1. Backup current live files
- Export and keep a copy of the current live homepage and assets (FTP/SFTP or hosting control panel). Save as `Index.live-backup.html` and copy current `images/` folder.

2. Prepare local working copy
- Ensure `V1/Index.html` is the working file. Create `Index.before-merge.html` as a backup of the local copy before merging.

3. Gather Canva assets
- Export hero, feature and thumbnail images from Canva following `V2/instructions/CANVA_GUIDE.md`.
- Place optimized images into `V1/images/` with clear filenames.

Merge steps
1. Replace visuals and copy
- Swap hero and feature images in `V1/Index.html` to the new exported filenames; update `alt` text.
- Copy preferred headlines, CTAs, and short content blocks from the live site into `V1/Index.html` sections.

2. Preserve SEO & structured data
- Keep the JSON-LD block in `V1/Index.html` and confirm `@id`, `url` and canonical link point to `https://sealenterprise.net/`.
- Verify `<title>` and `<meta name="description">` reflect the chosen copy.

3. Update links and contact details
- Confirm phone, email, address on `V1/Index.html` match the authoritative live details.
- Confirm social icons point to real profiles (Facebook, Instagram, LinkedIn, Pinterest).

Quality assurance
1. Local preview
- Start local server: `.\scripts\start-server.ps1` (or `python -m http.server 8000` in `V1`). Open `http://localhost:8000/Index.html`.

2. Accessibility checks
- Run quick check: `.\scripts\check-a11y.ps1`.
- For deeper tests, run Playwright + axe locally (Node required). See `tools/run_axe_playwright.js` and the README for instructions.

3. Structured-data validation
- Run `python tools/check_structured_data.py` to ensure JSON-LD is valid.

4. Visual QA
- Test on desktop and mobile widths, confirm images load, navigation works, and CTAs are actionable.

Deployment
1. Final backups
- Save `Index.final-backup.html` (copy of the live file just before upload) and create a tagged release or timestamped folder on the server.

2. Upload files
- Upload changed files (`Index.html`, updated `images/`, `css/`, `js/`) via your standard deployment method (SFTP/hosting panel/Git). Keep permissions the same.

3. Post-deploy checks
- Visit `https://sealenterprise.net/` and confirm the site loads and links are correct.
- Run `python tools/check_structured_data.py` against the live page (or paste the live HTML) to revalidate JSON-LD.
- Use the quick a11y script locally against the live HTML if you can fetch it.

Rollback plan
- If issues are found, restore the previously saved live backup files to revert quickly.

Optional tasks (recommended)
- Add `sitemap.xml` and submit to Google Search Console.
- Add robots rules if necessary and verify `rel=canonical` across pages.
- Schedule a regular (weekly or after content changes) run of `.\scripts\check-a11y.ps1` on your laptop.

Contacts & notes
- Keep a copy of this `V1/V2/instructions/DEPLOY.md` with your project notes.
- If you want, I can prepare a deploy script or an FTP upload helper for your hosting setup.
