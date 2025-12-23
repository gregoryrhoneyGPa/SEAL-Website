# capture_blocked_sites.ps1
$sites = @(
  'https://www.expedia.com',
  'https://www.priceline.com',
  'https://www.cruisedirect.com',
  'https://www.audleytravel.com'
)

$cwd = Get-Location
$out = Join-Path $cwd 'inspiration_pages'
New-Item -Path $out -ItemType Directory -Force | Out-Null

# Ensure Node is installed (try winget)
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
  Write-Output 'Node not found. Attempting to install Node LTS via winget (may prompt for elevation).'
  if (Get-Command winget -ErrorAction SilentlyContinue) {
    winget install -e --id OpenJS.NodeJS.LTS
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
      Write-Error 'Node installation failed or not in PATH. Install Node.js manually from https://nodejs.org/ and re-run this script.'; exit 1
    }
  } else {
    Write-Error 'winget not available. Please install Node.js manually from https://nodejs.org/ and re-run this script.'; exit 1
  }
}

# Write Node script that uses Playwright
$nodeScript = @'
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

(async () => {
  const sites = ["https://www.expedia.com","https://www.priceline.com","https://www.cruisedirect.com","https://www.audleytravel.com"];
  const outDir = path.resolve(process.cwd(), "inspiration_pages");
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  for (const url of sites) {
    const safe = url.replace(/^https?:\/\//, "").replace(/[^a-z0-9._-]/gi, "_");
    const png = path.join(outDir, `${safe}.png`);
    const htmlFile = path.join(outDir, `${safe}.rendered.html`);
    try {
      const browser = await chromium.launch({ headless: true });
      const context = await browser.newContext({
        viewport: { width: 1280, height: 900 },
        userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
      });
      const page = await context.newPage();
      page.setDefaultNavigationTimeout(60000);
      try {
        await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
      } catch (e) {
        console.error("Navigation issue for", url, e && e.message ? e.message : e);
      }
      await page.waitForTimeout(2000);
      try {
        await page.screenshot({ path: png, fullPage: true });
      } catch (e) {
        console.error("Screenshot failed for", url, e && e.message ? e.message : e);
      }
      try {
        const html = await page.content();
        fs.writeFileSync(htmlFile, html, "utf8");
      } catch (e) {
        console.error("Saving HTML failed for", url, e && e.message ? e.message : e);
      }
      await browser.close();
      console.log("Saved:", png, htmlFile);
    } catch (err) {
      console.error("ERROR processing", url, err && err.stack ? err.stack : err);
    }
  }
  process.exit(0);
})();
'@

Set-Content -Path .\capture_playwright.js -Value $nodeScript -Encoding UTF8

# Init npm if needed, install playwright and browsers
if (-not (Test-Path package.json)) {
  npm init -y | Out-Null
}
npm install playwright --no-audit --no-fund
# Ensure the browser binaries are installed
npx playwright install chromium

# Run the capture script
node .\capture_playwright.js

Write-Output "Finished. Check the `inspiration_pages` folder for .png and .rendered.html files."