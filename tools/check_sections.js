// Prove that the collapsible topic sections (assets/sections.js) work, and
// lose nothing.
//
//     python3 -m http.server 8812 --bind 127.0.0.1 &      # from the repository root
//     node tools/check_sections.js [http://127.0.0.1:8812]
//
// On four long pages of different make (a Statistics unit, a Data Science
// unit, a UGC NET unit whose headings sit inside a <section>, a practical):
//
//   1. the first section is open, every other one closed
//   2. a heading click opens its section, a second click closes it
//   3. "Open all" and "Close all" do what they say
//   4. a link to a heading (page.html#id) opens that section
//   5. a link to something INSIDE a closed section opens it too
//   6. a contents-list link opens the section it points at
//   7. the unit toggle and the prev/next links stay outside every section
//   8. printed, every section's text is on the page
//   9. no text is lost: the column's words with every section open are the
//      words of the page as published
//  10. with JavaScript off there is nothing: no bar, no buttons
//  11. no script errors on any of it
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const BASE = process.argv[2] || 'http://127.0.0.1:8812';
const EXEC = process.env.CHROMIUM || '/opt/pw-browsers/chromium';
const PAGES = [
  'statistics/inferential-statistics/unit3.html',
  'data-science/data-mining/unit4.html',
  'exams/ugc-net/unit3.html',
  'statistics/data-science-using-python/practical.html',
];

let bad = 0;
function check(ok, what, detail) {
  console.log((ok ? 'ok  ' : 'FAIL') + ' ' + what + (ok || detail === undefined ? '' : '  -- ' + detail));
  if (!ok) bad += 1;
}

const state = () => Array.from(document.querySelectorAll('.sec-toggle'))
  .map(b => b.getAttribute('aria-expanded') === 'true' &&
            !document.getElementById(b.getAttribute('aria-controls')).hidden ? 1 : 0).join('');
const columnWords = () => {
  const col = document.querySelector('main') || document.querySelector('.wrapper, .container');
  const c = col.cloneNode(true);
  c.querySelectorAll('.sec-bar, .progress-toggle, .progress-line, script, style, mjx-container, mjx-assistive-mml')
    .forEach(n => n.remove());
  return c.textContent.replace(/\s+/g, ' ').trim();
};

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC });
  const errors = [];
  const off = await browser.newContext({ javaScriptEnabled: false });
  const plain = await off.newPage();

  // Twice: as Chrome and Edge run it, where closed sections are
  // hidden="until-found" and the browser itself opens one a #link lands in;
  // and as Firefox and Safari run it, with no until-found, where only the
  // script's own link handling can. Without the second pass that handling
  // could be deleted and every check here would still pass in Chromium.
  for (const mode of ['until-found', 'plain hidden']) {
  const ctx = await browser.newContext();
  if (mode === 'plain hidden') {
    await ctx.addInitScript(() => { delete HTMLElement.prototype.onbeforematch; });
  }
  const page = await ctx.newPage();
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/favicon|net::ERR/.test(m.text())) errors.push(m.text()); });
  const go = async p => { await page.goto(BASE + '/' + p, { waitUntil: 'networkidle' }); await page.waitForTimeout(200); };

  for (const p of PAGES) {
    console.log('-- ' + p + '  [' + mode + ']');
    const usesUntil = await (async () => { await go(p); return page.evaluate(() =>
      Array.from(document.querySelectorAll('.sec-body[hidden]')).every(b => b.getAttribute('hidden') === 'until-found')); })();
    check(usesUntil === (mode === 'until-found'), 'closed sections are hidden as ' + mode);
    await go(p);
    const s = await page.evaluate(state);
    const n = s.length;
    // 1
    check(n >= 4 && s === '1' + '0'.repeat(n - 1), 'first open, the rest closed (' + n + ' sections)', s);

    // 2
    const third = page.locator('.sec-toggle').nth(2);
    await third.click();
    check((await page.evaluate(state))[2] === '1', 'a heading click opens its section');
    await third.click();
    check((await page.evaluate(state))[2] === '0', 'a second click closes it');

    // 3
    await page.locator('.sec-bar button', { hasText: 'Open all' }).click();
    check(!(await page.evaluate(state)).includes('0'), '"Open all" opens every section');
    // 9 -- measured here, with everything open
    const words = await page.evaluate(columnWords);
    await page.locator('.sec-bar button', { hasText: 'Close all' }).click();
    check(!(await page.evaluate(state)).includes('1'), '"Close all" closes every section');

    // 4
    const id3 = await page.evaluate(() => document.querySelectorAll('h2.sec-head')[3].id);
    // A fresh load, not a same-page hash change: arriving from another page
    // (a syllabus map, a search result) fires no hashchange.
    await page.goto('about:blank');
    await go(p + '#' + encodeURIComponent(id3));
    check((await page.evaluate(state))[3] === '1', 'page.html#' + id3.slice(0, 30) + ' opens that section');
    const inView = await page.evaluate(i => {
      const r = document.getElementById(i).getBoundingClientRect();
      return r.top >= -2 && r.top < window.innerHeight;
    }, id3);
    check(inView, '... and scrolls to it');

    // 5 -- a target inside a later section (an h3 id, or any id) opens it
    const inner = await page.evaluate(() => {
      const bodies = Array.from(document.querySelectorAll('.sec-body'));
      for (let i = bodies.length - 1; i > 0; i--) {
        const t = bodies[i].querySelector('[id]');
        if (t) return { id: t.id, i };
      }
      return null;
    });
    if (inner) {
      await page.goto('about:blank');
      await go(p + '#' + encodeURIComponent(inner.id));
      check((await page.evaluate(state))[inner.i] === '1', 'a link inside section ' + (inner.i + 1) + ' opens it');
    }

    // 6
    await go(p);
    const tocHref = await page.evaluate(() => {
      const heads = Array.from(document.querySelectorAll('h2.sec-head')).map(h => '#' + h.id);
      const a = Array.from(document.querySelectorAll('details.toc a[href^="#"], .toc a[href^="#"]'))
        .find(x => heads.indexOf(decodeURIComponent(x.getAttribute('href'))) > 0);
      return a ? a.getAttribute('href') : null;
    });
    if (tocHref) {
      const idx = await page.evaluate(h => Array.from(document.querySelectorAll('h2.sec-head'))
        .map(x => '#' + x.id).indexOf(decodeURIComponent(h)), tocHref);
      await page.evaluate(() => { const d = document.querySelector('details.toc'); if (d) d.open = true; });
      await page.locator(".toc a[href='" + tocHref + "']").first().click();
      await page.waitForTimeout(150);
      check((await page.evaluate(state))[idx] === '1', 'a contents-list link opens section ' + (idx + 1));
    } else {
      console.log('     (no contents list on this page)');
    }

    // 7
    const inside = await page.evaluate(() =>
      document.querySelectorAll('.sec-body .progress-toggle, .sec-body .pagination, .sec-body .page-nav, ' +
                                '.sec-body p.next-course, .sec-body section.exam-courses').length);
    check(inside === 0, 'unit toggle and prev/next stay outside every section', inside);

    // 8
    await page.emulateMedia({ media: 'print' });
    const hiddenInPrint = await page.evaluate(() => Array.from(document.querySelectorAll('.sec-body'))
      .filter(b => b.getBoundingClientRect().height === 0).length);
    check(hiddenInPrint === 0, 'printed, every section is on the page', hiddenInPrint + ' empty');
    await page.emulateMedia({ media: 'screen' });

    // 9 and 10
    await plain.goto(BASE + '/' + p, { waitUntil: 'load' });
    const plainWords = await plain.evaluate(columnWords);
    check(words === plainWords, 'no text lost or added by folding',
          words.length + ' vs ' + plainWords.length + ' chars');
    const chrome = await plain.evaluate(() => document.querySelectorAll('.sec-bar, .sec-toggle, .sec-body').length);
    check(chrome === 0, 'with JavaScript off, nothing is folded', chrome);
  }
  await ctx.close();
  }

  // 11
  check(errors.length === 0, 'no script errors', errors.slice(0, 3).join(' | '));
  await browser.close();
  console.log(bad ? '\n' + bad + ' failure(s)' : '\nall section checks pass');
  process.exit(bad ? 1 : 0);
})();
