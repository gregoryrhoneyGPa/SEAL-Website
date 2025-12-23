const { chromium } = require('playwright');
const axe = require('axe-core');

(async () => {
  const url = process.argv[2] || 'http://localhost:8000/';
  console.log('Running axe-core audit on', url);
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });

  // Inject axe-core source
  await page.addScriptTag({ content: axe.source });

  // Run axe in the page context
  const results = await page.evaluate(async () => {
    return await axe.run();
  });

  // Print summary
  console.log('\nAxe results summary:');
  console.log('Violations:', results.violations.length);
  console.log('Incomplete:', results.incomplete.length);
  console.log('Inapplicable:', results.inapplicable.length);

  // Save full JSON to file
  const fs = require('fs');
  const out = 'tools/axe-report.json';
  fs.writeFileSync(out, JSON.stringify(results, null, 2), 'utf8');
  console.log('\nFull report written to', out);

  // Print top 5 violations with selectors
  if (results.violations.length) {
    console.log('\nTop violations:');
    results.violations.slice(0,5).forEach((v, i) => {
      console.log(`\n${i+1}. ${v.id} — ${v.description} (impact: ${v.impact})`);
      v.nodes.slice(0,3).forEach((n,j)=>{
        console.log(`  - Target: ${n.target.join(' , ')}`);
      });
    });
  }

  await browser.close();
  process.exit(results.violations.length ? 1 : 0);
})();
