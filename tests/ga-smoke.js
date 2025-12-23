const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  page.on('console', msg => console.log('PAGE:', msg.text()));

  // Pages to test and the selectors to click on each
  const pagesToTest = [
    { url: 'Index.html', selectors: ['[data-ga-label="Pickleball Spotlight Card"]', '[data-ga-label="Pickleball Link"]'] },
    { url: 'index-modern.html', selectors: ['[data-ga-label="Pickleball Link"]'] },
    { url: 'Index.merged.html', selectors: ['[data-ga-label="Pickleball Link"]'] },
    { url: 'components.html', selectors: ['[data-ga-label="Components Plan My Journey"]', '[data-ga-label="Components Homepage Link"]'] },
    { url: 'contact.html', selectors: ['[data-ga-label="Contact Submit Request"]', '[data-ga-label="Contact Schedule Consultation"]'] },
    { url: 'pickleball-passport.html', selectors: ['[data-ga-label="Schedule Partner Overview"]', '[data-ga-label="Program Overview"]', '[data-ga-label="Start Planning Contact"]'] },
    { url: 'scaffold-pages/pickleball-passport.html', selectors: ['[data-ga-label="Scaffold Pickleball Book Call"]', '[data-ga-label="Scaffold Pickleball Browse Resources"]'] }
  ];

  for (const p of pagesToTest) {
    const fileUrl = 'file://' + path.resolve(p.url);
    console.log('\n--- Loading', fileUrl);
    try {
      await page.goto(fileUrl);
    } catch (e) {
      console.log('PAGE LOAD ERROR', e.message);
      continue;
    }

    await page.evaluate(() => {
      // prevent navigation so clicks are observable in headless run
      document.querySelectorAll('a[data-ga-category], button[data-ga-category]').forEach(el=>{
        el.addEventListener('click', e=>{ e.preventDefault(); }, {passive:false});
      });
      // capture dataLayer pushes
      window.dataLayer = window.dataLayer || [];
      const orig = window.dataLayer.push.bind(window.dataLayer);
      window.dataLayer.push = function(obj){
        console.log('DL_PUSH', JSON.stringify(obj));
        return orig(obj);
      };
    });

    for (const sel of p.selectors) {
      try {
        const found = await page.$(sel);
        if (!found) { console.log('NOT FOUND:', sel); continue; }
        console.log('CLICKING:', sel);
        await found.click();
        await page.waitForTimeout(300);
      } catch (e) {
        console.log('ERROR clicking', sel, e.message);
      }
    }
  }

  await browser.close();
  console.log('\nSmoke test complete');
})();
