Playwright GA smoke test

Steps to run locally (requires Node.js and network access):

1. From the project root (seal-site/V1) install dependencies:

Run the following in PowerShell:

npm init -y
npm install -D playwright
npx playwright install

2. Run the smoke script from the project root:

node tests/ga-smoke.js

What it does:
- Opens Index.html as a local file in a headless Chromium instance.
- Prevents navigation on anchors with data-ga-* so clicks can be observed.
- Overrides dataLayer.push to log pushes to the test console.
- Clicks a small set of selectors and prints any DL_PUSH logs.

If installation requires admin privileges on your machine, install Node.js LTS manually from https://nodejs.org/ and then run the commands above.
