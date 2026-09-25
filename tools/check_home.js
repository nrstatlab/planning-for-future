// Prove the home page's three columns, and that the A-Z column answers in
// the column itself.
//
//     python3 -m http.server 8812 --bind 127.0.0.1 &      # from the repository root
//     node tools/check_home.js [http://127.0.0.1:8812]
//
//   1. at 1280px: Examinations left, Topics A-Z middle, Study material right,
//      side by side
//   2. at 900px: Topics A-Z across the top, the other two side by side below
//   3. at 390px: one column, in the order Examinations, Topics A-Z, Study
//   4. typing "chi square" lists results INSIDE the middle column, and the
//      letter view gives way to them
//   5. clicking elsewhere on the page leaves those results where they are
//   6. Escape clears the box and brings the letters back
//   7. a letter lists its topics in the column -- as many as
//      assets/topics-index.json holds for it -- and its links open real pages
//   8. picking a letter clears a search in progress
//   9. with the data unreachable, a letter still goes to topics.html#letter-x
//  10. with JavaScript off, the letters are links to topics.html and there is
//      no search box to mislead anyone
//  11. no script errors
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://127.0.0.1:8812';
const EXEC = process.env.CHROMIUM || '/opt/pw-browsers/chromium';
const AZ = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'assets', 'topics-index.json')));
const B_TOPICS = AZ.letters.find(l => l[0] === 'B')[1].length;

let bad = 0;
function check(ok, what, detail) {
  console.log((ok ? 'ok  ' : 'FAIL') + ' ' + what + (ok || detail === undefined ? '' : '  -- ' + detail));
  if (!ok) bad += 1;
}

const boxes = () => ['.col-exams', '.col-az', '.col-study'].map(s => {
  const r = document.querySelector(s).getBoundingClientRect();
  return { x: Math.round(r.left), y: Math.round(r.top + window.scrollY), w: Math.round(r.width) };
});

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC });
  const errors = [];
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
  const page = await ctx.newPage();
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon|net::ERR/.test(m.text())) errors.push(m.text()); });
  const go = async () => { await page.goto(BASE + '/index.html', { waitUntil: 'networkidle' }); await page.waitForTimeout(150); };

  // 1
  await go();
  let [e, a, s] = await page.evaluate(boxes);
  check(e.x < a.x && a.x < s.x && Math.abs(e.y - s.y) < 40 && a.y - e.y < 200,
        '1280px: exams left, A-Z middle, study right', JSON.stringify([e, a, s]));

  // 2
  await page.setViewportSize({ width: 900, height: 1000 });
  [e, a, s] = await page.evaluate(boxes);
  check(a.y < e.y && Math.abs(e.y - s.y) < 40 && e.x < s.x && a.w > e.w * 1.6,
        '900px: A-Z across the top, exams and study below', JSON.stringify([e, a, s]));

  // 3
  await page.setViewportSize({ width: 390, height: 844 });
  [e, a, s] = await page.evaluate(boxes);
  check(e.y < a.y && a.y < s.y && e.x === a.x && a.x === s.x,
        '390px: one column, exams then A-Z then study', JSON.stringify([e, a, s]));
  await page.setViewportSize({ width: 1280, height: 1000 });

  // 4
  await page.fill('#q', 'chi square');
  await page.waitForFunction(() => document.querySelectorAll('#results li[role=option]').length > 0, null, { timeout: 5000 }).catch(() => {});
  const r = await page.evaluate(() => {
    const col = document.querySelector('.col-az').getBoundingClientRect();
    const items = Array.from(document.querySelectorAll('#results li[role=option]'));
    const outside = items.filter(li => {
      const b = li.getBoundingClientRect();
      return b.left < col.left - 1 || b.right > col.right + 1;
    }).length;
    const letters = getComputedStyle(document.querySelector('.az-letters')).display;
    const pos = getComputedStyle(document.getElementById('results')).position;
    return { n: items.length, outside, letters, pos, chi: items.some(li => /chi/i.test(li.textContent)) };
  });
  check(r.n >= 3 && r.chi, '"chi square" lists results', JSON.stringify(r));
  check(r.outside === 0 && r.pos === 'static', 'the results sit inside the middle column', JSON.stringify(r));
  check(r.letters === 'none', 'the letter view gives way to the results', r.letters);

  // 5
  await page.mouse.click(40, 600);
  check(await page.evaluate(() => !document.getElementById('results').hidden),
        'clicking elsewhere leaves the results in place');

  // 6
  await page.focus('#q');
  await page.keyboard.press('Escape');
  const after = await page.evaluate(() => ({
    v: document.getElementById('q').value, hidden: document.getElementById('results').hidden,
    letters: getComputedStyle(document.querySelector('.az-letters')).display }));
  check(after.v === '' && after.hidden && after.letters !== 'none', 'Escape clears the box and brings the letters back', JSON.stringify(after));

  // 7
  await page.locator(".az-letters a[data-letter='B']").click();
  await page.waitForSelector('.az-list', { timeout: 5000 }).catch(() => {});
  const panel = await page.evaluate(() => ({
    head: (document.querySelector('.az-head') || {}).textContent || '',
    dts: document.querySelectorAll('.az-list dt').length,
    href: (document.querySelector('.az-list dd a') || {}).href || '',
    current: (document.querySelector('.az-letters a[aria-current]') || {}).textContent }));
  check(panel.dts === B_TOPICS && panel.head.indexOf(String(B_TOPICS)) !== -1,
        'B lists its ' + B_TOPICS + ' topics in the column', JSON.stringify(panel));
  check(panel.current === 'B', 'B is marked as the current letter', panel.current);
  const status = panel.href ? (await page.request.get(panel.href)).status() : 0;
  check(status === 200, 'a topic link opens a real page', panel.href + ' -> ' + status);
  check(page.url().endsWith('/index.html'), 'picking a letter stays on the home page', page.url());

  // 8 -- words in the box, but not yet searched on (the letters still
  // show): picking a letter must empty the box so the two never disagree
  await page.evaluate(() => { document.getElementById('q').value = 'anova'; });
  await page.locator(".az-letters a[data-letter='C']").click();
  await page.waitForTimeout(300);
  const box8 = await page.evaluate(() => ({ v: document.getElementById('q').value,
    head: (document.querySelector('.az-head') || {}).textContent || '' }));
  check(box8.v === '' && /^C /.test(box8.head), 'a letter clears a search in progress', JSON.stringify(box8));

  // 9
  const ctx2 = await browser.newContext();
  await ctx2.route('**/assets/topics-index.json', rt => rt.abort());
  const p2 = await ctx2.newPage();
  await p2.goto(BASE + '/index.html', { waitUntil: 'networkidle' });
  await Promise.all([p2.waitForURL('**/topics.html#letter-b', { timeout: 5000 }).catch(() => {}),
                     p2.locator(".az-letters a[data-letter='B']").click()]);
  check(/topics\.html#letter-b$/.test(p2.url()), 'data unreachable: a letter still goes to topics.html', p2.url());
  await ctx2.close();

  // 10
  const off = await browser.newContext({ javaScriptEnabled: false });
  const p3 = await off.newPage();
  await p3.goto(BASE + '/index.html', { waitUntil: 'load' });
  const plain = await p3.evaluate(() => ({
    search: getComputedStyle(document.querySelector('.col-az .search')).display,
    b: document.querySelector(".az-letters a[data-letter='B']").getAttribute('href'),
    all: !!document.querySelector(".az-panel a.azlink[href='topics.html']") }));
  check(plain.search === 'none' && plain.b === 'topics.html#letter-b' && plain.all,
        'scripts off: no search box, letters link to topics.html', JSON.stringify(plain));
  await off.close();

  // 11
  check(errors.length === 0, 'no script errors', errors.slice(0, 3).join(' | '));
  await browser.close();
  console.log(bad ? '\n' + bad + ' failure(s)' : '\nall home checks pass');
  process.exit(bad ? 1 : 0);
})();
