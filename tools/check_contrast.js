#!/usr/bin/env node
/*
 * Measure text contrast the way a reader meets it: in a browser, against the
 * background actually painted behind each piece of text.
 *
 *     python3 -m http.server 8812 &
 *     node tools/check_contrast.js [http://127.0.0.1:8812] [--scheme=dark|light|both]
 *
 * Every visible element that directly holds text is measured: its computed
 * colour against the first opaque background found by walking up its
 * ancestors (alpha is composited, and a gradient counts by its colour stops --
 * the lightest one for dark text, the darkest for light text, whichever is
 * worse). WCAG 2 AA: 4.5:1, or 3:1 for large text (24px, or 18.66px bold).
 *
 * Written for the dark theme, which is GENERATED (tools/build_dark_theme.py)
 * and so is only trustworthy if something measures it. It runs on the light
 * theme too, because nothing had measured that either.
 *
 * Not measured: text inside SVG (the diagrams keep a light panel of their
 * own), visually-hidden screen-reader text, and anything not rendered.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const args = process.argv.slice(2);
const BASE = args.find(a => a.startsWith('http')) || 'http://127.0.0.1:8812';
const SCHEME = (args.find(a => a.startsWith('--scheme=')) || '--scheme=both').split('=')[1];
const EXEC = process.env.CHROMIUM || '/opt/pw-browsers/chromium';

// One page of every layout the site has, and the ones with the most colour.
const PAGES = [
  '/index.html', '/about.html', '/topics.html', '/guides/which-test.html', '/404.html',
  '/statistics/index.html', '/statistics/sampling-techniques/index.html',
  '/statistics/sampling-techniques/unit2.html', '/statistics/sampling-techniques/practical.html',
  '/statistics/probability-theory/unit1.html', '/statistics/probability-theory/index.html',
  '/data-science/index.html', '/data-science/data-mining/index.html',
  '/data-science/data-mining/unit2.html', '/data-science/data-mining/lab.html',
  '/data-science/data-mining/practice.html', '/data-science/machine-learning/self-study-notes/index.html',
  '/exams/index.html', '/exams/iss/paper1.html', '/exams/asrb-net/index.html',
  '/exams/ugc-net/index.html', '/exams/ugc-net/unit5.html', '/exams/ugc-net/mcqs.html',
  '/statistics/economics/index.html', '/statistics/economics/unit1.html', '/statistics/financial-accounting/unit3.html',
];

async function measure(page) {
  return page.evaluate(() => {
    const parse = s => {
      const m = s && s.match(/rgba?\(([^)]+)\)/);
      if (!m) return null;
      const p = m[1].split(/[\s,\/]+/).filter(Boolean).map(Number);
      return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
    };
    const lum = c => {
      const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4; };
      return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]);
    };
    const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
    const over = (top, under) => {           // composite top (with alpha) over an opaque colour
      const a = top[3];
      return [0, 1, 2].map(i => top[i] * a + under[i] * (1 - a)).concat(1);
    };
    const stops = img => (img.match(/rgba?\([^)]+\)/g) || []).map(parse);

    // Every background colour that could be behind el, from nearest ancestor out.
    function behind(el, fgLight) {
      const layers = [];
      for (let e = el; e; e = e.parentElement) {
        const cs = getComputedStyle(e);
        const img = cs.backgroundImage;
        if (img && img !== 'none' && /gradient/.test(img)) {
          const ss = stops(img).filter(c => c && c[3] > 0.5);
          if (ss.length) {
            // the worst stop for this text: lightest behind dark text, darkest behind light text
            ss.sort((a, b) => lum(a) - lum(b));
            layers.push(fgLight ? ss[ss.length - 1] : ss[0]);
            if (ss[0][3] >= 0.99) break;
          }
        }
        const bg = parse(cs.backgroundColor);
        if (bg && bg[3] > 0) {
          layers.push(bg);
          if (bg[3] >= 0.99) break;
        }
      }
      let c = [255, 255, 255, 1];                 // the canvas, if nothing is opaque
      const rootBg = parse(getComputedStyle(document.documentElement).backgroundColor);
      if (matchMedia('(prefers-color-scheme: dark)').matches) c = [18, 18, 18, 1];
      if (rootBg && rootBg[3] > 0) c = over(rootBg, c);
      for (let i = layers.length - 1; i >= 0; i--) c = over(layers[i], c);
      return c;
    }

    const fails = [];
    let n = 0;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    while (walker.nextNode()) {
      const t = walker.currentNode;
      if (!t.nodeValue.trim()) continue;
      const el = t.parentElement;
      if (!el || seen.has(el)) continue;
      seen.add(el);
      if (el.closest('svg, .sr-head, script, style, noscript, [hidden]')) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      if (cs.clip && cs.clip !== 'auto' && /rect\(0/.test(cs.clip)) continue;
      let op = 1;
      for (let e = el; e; e = e.parentElement) op *= Number(getComputedStyle(e).opacity);
      if (op < 0.1) continue;
      const fg0 = parse(cs.color);
      if (!fg0) continue;
      const fgLight = lum(fg0) > 0.4;
      const bg = behind(el, fgLight);
      const fg = over([fg0[0], fg0[1], fg0[2], fg0[3] * op], bg);
      const px = parseFloat(cs.fontSize), bold = Number(cs.fontWeight) >= 700;
      const need = (px >= 24 || (bold && px >= 18.66)) ? 3 : 4.5;
      const cr = ratio(fg, bg);
      n++;
      if (cr < need) {
        let path = el.tagName.toLowerCase() + (el.className && typeof el.className === 'string'
          ? '.' + el.className.trim().split(/\s+/).join('.') : '');
        const p = el.parentElement;
        if (p) path = (p.className && typeof p.className === 'string' ? '.' + p.className.trim().split(/\s+/)[0] : p.tagName.toLowerCase()) + ' > ' + path;
        fails.push({ path, cr: Math.round(cr * 100) / 100, need,
                     fg: cs.color, bg: `rgb(${bg.slice(0, 3).map(Math.round).join(', ')})`,
                     text: t.nodeValue.trim().slice(0, 40) });
      }
    }
    return { n, fails };
  });
}

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC });
  const schemes = SCHEME === 'both' ? ['light', 'dark'] : [SCHEME];
  let total = 0, bad = 0;
  for (const scheme of schemes) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: scheme });
    for (const url of PAGES) {
      const page = await ctx.newPage();
      // 404.html writes root-absolute paths for the host it is served from;
      // locally the site is at "/", so map them back (as check_site_nav.js does).
      await page.route('**/planning-for-future/**', r =>
        r.continue({ url: r.request().url().replace('/planning-for-future/', '/') }));
      await page.goto(BASE + url, { waitUntil: 'networkidle', timeout: 30000 });
      // open every closed <details> so answers and proofs are measured too
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => {
        if (!d.closest('.sitenav')) d.open = true;
      }));
      // and every folded topic section (assets/sections.js) on a long page
      await page.evaluate(() => {
        const all = Array.from(document.querySelectorAll('.sec-bar button')).find(b => /Open all/.test(b.textContent));
        if (all) all.click();
      });
      const { n, fails } = await measure(page);
      total += n; bad += fails.length;
      // group identical failures (same selector, same colours) to keep the report readable
      const groups = {};
      for (const f of fails) {
        const k = `${f.path} | ${f.cr}:1 < ${f.need} | ${f.fg} on ${f.bg}`;
        (groups[k] = groups[k] || { k, n: 0, text: f.text }).n++;
      }
      const g = Object.values(groups).sort((a, b) => b.n - a.n);
      console.log(`${fails.length ? 'FAIL' : 'ok  '} ${scheme.padEnd(5)} ${url.padEnd(62)} ${n} text elements, ${fails.length} below AA`);
      for (const x of g.slice(0, 6)) console.log(`        ${x.n}x  ${x.k}   "${x.text}"`);
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  console.log(`\n${total} text elements measured, ${bad} below WCAG AA`);
  process.exit(bad ? 1 : 0);
})();
