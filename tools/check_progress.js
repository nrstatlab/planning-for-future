// Prove that reader progress (assets/progress.js) works, and stays out of the way.
//
//     python3 -m http.server 8812 --bind 127.0.0.1 &      # from the repository root
//     node tools/check_progress.js [http://127.0.0.1:8812]
//
// What a reader would do, in one browser profile, then the two ways it must
// fail quietly:
//
//   1. mark a unit done; both toggles on the page agree, storage holds it
//   2. its course home says "1 of N done" and ticks that unit's card
//   3. the Statistics hub card and the exam hub's course row carry "1/N"
//   4. the home page offers "Continue where you left off" to that unit
//   5. UGC NET counts as a course of its own
//   6. "Clear my progress" on About empties it, and the home strip goes
//   7. with JavaScript off: no toggle, no strip -- the page as published
//   8. with storage throwing (a private window): no toggle, no error
//
// N is read from assets/progress-index.json, never written here.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://127.0.0.1:8812';
const EXEC = process.env.CHROMIUM || '/opt/pw-browsers/chromium';
const INDEX = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'assets', 'progress-index.json')));
const COURSE = 'statistics/sampling-theory';
const UNIT = COURSE + '/unit2.html';
const N = INDEX.courses[COURSE].length;
const UGC_N = INDEX.courses['exams/ugc-net'].length;

let bad = 0;
function check(ok, what, detail) {
  console.log((ok ? 'ok  ' : 'FAIL') + ' ' + what + (ok || !detail ? '' : '  -- ' + detail));
  if (!ok) bad += 1;
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC });
  const errors = [];
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon|net::ERR/.test(m.text())) errors.push(m.text()); });
  const go = async p => { await page.goto(BASE + '/' + p, { waitUntil: 'networkidle' }); await page.waitForTimeout(150); };

  // 1
  await go(UNIT);
  let toggles = page.locator('.progress-toggle button');
  check(await toggles.count() === 2, 'unit page has a toggle at the top and at the foot', 'count=' + await toggles.count());
  await toggles.first().click();
  const pressed = await toggles.evaluateAll(bs => bs.map(b => b.getAttribute('aria-pressed')));
  check(pressed.every(v => v === 'true'), 'both toggles read done after one click', pressed.join(','));
  const stored = await page.evaluate(() => localStorage.getItem('nrstatlab.progress.v1'));
  check(!!stored && JSON.parse(stored).done[UNIT] !== undefined, 'storage holds the unit id', stored);

  // 2
  await go(COURSE + '/index.html');
  const line = await page.locator('.progress-line').textContent().catch(() => '');
  check(line.startsWith('1 of ' + N + ' done'), 'course home says 1 of ' + N, line);
  const tick = await page.locator("a[href='unit2.html'] .progress-tick").count();
  check(tick >= 1, 'the done unit\'s card is ticked', 'ticks=' + tick);

  // 3
  await go('statistics/index.html');
  const card = await page.locator("a.course[href='sampling-theory/index.html'] .progress-badge").textContent().catch(() => '');
  check(card === '1/' + N, 'Statistics hub card shows 1/' + N, card);
  await go('exams/asrb-net/index.html');
  const row = await page.locator(".exam-courses a[href$='sampling-theory/index.html'] .progress-badge").textContent().catch(() => '');
  check(row === '1/' + N, 'exam hub course row shows 1/' + N, row);

  // 4
  await go('index.html');
  const strip = page.locator('.progress-continue');
  const href = await strip.locator('a').getAttribute('href').catch(() => '');
  check(href && href.endsWith('/' + UNIT), 'home offers to continue at the unit', href);
  const stripText = await strip.textContent().catch(() => '');
  check(/1 unit done/.test(stripText), 'home counts 1 unit done', stripText);

  // 5
  await go('exams/ugc-net/unit1.html');
  await page.locator('.progress-toggle button').first().click();
  await go('exams/ugc-net/index.html');
  const ugc = await page.locator('.progress-line').textContent().catch(() => '');
  check(ugc.startsWith('1 of ' + UGC_N + ' done'), 'UGC NET counts as a course: 1 of ' + UGC_N, ugc);

  // 6
  await go('about.html');
  page.once('dialog', d => d.accept());
  await page.locator('.progress-clear').click();
  const after = await page.evaluate(() => localStorage.getItem('nrstatlab.progress.v1'));
  check(after === null, 'Clear my progress empties storage', after);
  await go('index.html');
  check(await page.locator('.progress-continue').count() === 0, 'home strip gone after clearing');

  check(errors.length === 0, 'no script errors while doing all of that', errors.join(' | '));
  await ctx.close();

  // 7
  const off = await browser.newContext({ javaScriptEnabled: false });
  const p2 = await off.newPage();
  await p2.goto(BASE + '/' + UNIT, { waitUntil: 'load' });
  check(await p2.locator('.progress-toggle').count() === 0, 'JavaScript off: no toggle on a unit page');
  await p2.goto(BASE + '/about.html', { waitUntil: 'load' });
  check(await p2.locator('#progress-controls').isHidden(), 'JavaScript off: About shows no controls');
  await off.close();

  // 8
  const blocked = await browser.newContext();
  await blocked.addInitScript(() => {
    const deny = () => { throw new DOMException('blocked', 'SecurityError'); };
    Storage.prototype.setItem = deny; Storage.prototype.getItem = deny;
  });
  const p3 = await blocked.newPage();
  const errs3 = [];
  p3.on('pageerror', e => errs3.push(e.message));
  await p3.goto(BASE + '/' + UNIT, { waitUntil: 'networkidle' });
  check(await p3.locator('.progress-toggle').count() === 0, 'storage blocked: no toggle');
  await p3.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
  check(errs3.length === 0, 'storage blocked: no script errors', errs3.join(' | '));
  await blocked.close();

  await browser.close();
  console.log(bad ? `\n${bad} failure(s)` : '\nall progress checks pass');
  process.exit(bad ? 1 : 0);
})();
