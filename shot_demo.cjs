// Capture 3 demo states from 车记得 demo v4.1 via playwright (run from no-Chinese path)
const { pathToFileURL } = require('url');
const pw = require('C:/Users/Su/.workbuddy/plugins/cache/experts/ppt-implement/1.0.13/skills/ppt-implement/scripts/export/node_modules/playwright');

(async () => {
  const browser = await pw.chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 760, height: 920 },
    deviceScaleFactor: 2,
  });
  const demoUrl = pathToFileURL('C:/ppt-ws/shot_tmp/demo.html').href;
  await page.goto(demoUrl);
  await page.waitForTimeout(1000);

  // 1) home screen with AI entry card
  await page.locator('.phone').screenshot({ path: 'C:/ppt-ws/shot_tmp/demo_home.png' });

  // 2) AI parse modal
  await page.click('.ai-home-entry');
  await page.waitForTimeout(700);
  await page.fill('#aiInput', '去海底捞，要充电');
  await page.click('#destSheet button.ai-btn');
  await page.waitForTimeout(1900);
  await page.locator('.phone').screenshot({ path: 'C:/ppt-ws/shot_tmp/demo_parse.png' });

  // 3) recommendation card with AI constraints applied
  await page.click('#aiParseBody button.ai-btn');
  await page.waitForTimeout(1000);
  await page.locator('.phone').screenshot({ path: 'C:/ppt-ws/shot_tmp/demo_reco.png' });

  await browser.close();
  console.log('SHOTS_DONE');
})().catch((e) => { console.error('ERR', e && e.message ? e.message : e); process.exit(1); });
