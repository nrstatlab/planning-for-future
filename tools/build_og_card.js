#!/usr/bin/env node
/*
 * Draw assets/og-card.jpg, the 1200x630 image a link preview shows.
 *
 * JPEG, not PNG: the PNG was 393 KB, and WhatsApp -- the main way this material
 * travels -- is commonly reported to drop preview images above about 300 KB.
 *
 *     node tools/build_og_card.js
 *
 * Before this, not one of the 691 pages carried og:image, so a link shared in
 * WhatsApp, Telegram or LinkedIn -- which is how this material actually travels
 * between students -- arrived as a grey box with a URL in it.
 *
 * Drawn by a browser rather than by an image library because there is no image
 * library in this repository's toolchain, and Chromium is already here for
 * check_site_nav.js. The words are the home page's own: nothing on the card is
 * a claim the site does not already make.
 *
 * The mark is the favicon's -- three ascending bars -- so the tab icon and the
 * share card read as the same brand.
 */
const path = require('path');
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const OUT = path.join(__dirname, '..', 'assets', 'og-card.jpg');
const EXEC = process.env.CHROMIUM || '/opt/pw-browsers/chromium';

const HTML = `<!DOCTYPE html><html><head><meta charset="utf-8"><style>
  * { box-sizing: border-box; margin: 0; }
  body { width: 1200px; height: 630px; overflow: hidden;
    font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: #fff;
    background:
      radial-gradient(900px 420px at 85% -10%, rgba(255,255,255,.18), transparent 60%),
      linear-gradient(135deg, #0a3763 0%, #0f4c81 48%, #1e7fbf 100%); }
  .in { position: absolute; inset: 0; padding: 78px 86px; display: flex;
        flex-direction: column; justify-content: space-between; }
  .top { display: flex; align-items: center; gap: 26px; }
  .mark { width: 96px; height: 96px; border-radius: 20px; background: rgba(255,255,255,.14);
          display: flex; align-items: flex-end; justify-content: center; gap: 9px; padding: 0 0 20px; }
  .mark i { display: block; width: 17px; background: #fff; border-radius: 3px; }
  .brand { font-size: 62px; font-weight: 800; letter-spacing: .05em; }
  h1 { font-size: 58px; line-height: 1.12; font-weight: 700; max-width: 960px; }
  .foot { display: flex; gap: 16px; flex-wrap: wrap; }
  .foot span { font-size: 27px; padding: 10px 20px; border-radius: 999px;
               background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.28); }
</style></head><body><div class="in">
  <div class="top">
    <div class="mark"><i style="height:30px"></i><i style="height:46px"></i><i style="height:62px"></i></div>
    <div class="brand">NRSTATLAB</div>
  </div>
  <h1>Statistics, Data Science and Machine Learning &mdash; written to teach.</h1>
  <div class="foot"><span>Every step shown</span><span>Code that runs</span><span>Free to read, no sign-in</span></div>
</div></body></html>`;

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
  await page.setContent(HTML);
  await page.screenshot({ path: OUT, type: 'jpeg', quality: 88 });
  await browser.close();
  console.log('wrote', OUT);
})();
