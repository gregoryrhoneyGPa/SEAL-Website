const fs = require("fs");
const playwright = require("playwright");
(async() => {
  const sites = ["https://www.expedia.com","https://www.priceline.com","https://www.cruisedirect.com","https://www.audleytravel.com"];
  for (const url of sites) {
    try {
      const browser = await playwright.chromium.launch({headless:true});
      const context = await browser.newContext({viewport:{width:1280,height:800}});
      const page = await context.newPage();
      await page.goto(url, {waitUntil:'networkidle', timeout:60000});
      const safe = url.replace(/https?:\/\//,'').replace(/[^\w.-]/g,'_');
      const outdir = 'inspiration_pages';
      await page.screenshot({path:`${outdir}/${safe}.png`, fullPage:true});
      const html = await page.content();
      fs.writeFileSync(`${outdir}/${safe}.rendered.html`, html);
      await browser.close();
    } catch (e) {
      console.error('ERROR for', url, e && (e.stack || e.toString()));
    }
  }
})();
