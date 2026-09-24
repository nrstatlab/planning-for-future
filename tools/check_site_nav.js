#!/usr/bin/env node
/*
 * Prove the site navigation is actually usable, on every kind of page.
 *
 *     python3 -m http.server 8812 &
 *     node tools/check_site_nav.js [http://127.0.0.1:8812]
 *
 * WHY A BROWSER. Everything else in tools/ reads the HTML, and the HTML was
 * right the whole time this check was being written. The two faults it found
 * were only visible once a browser had applied all five stylesheets together:
 *
 *   1. the subject sheets paint every <summary> #0f4c81, which is this bar's
 *      own background, so on 240 pages the four menu labels were dark blue on
 *      dark blue -- present in the DOM, present in the accessibility tree,
 *      correctly positioned, and invisible;
 *   2. those sheets also set details { overflow: hidden } to round the corners
 *      of a collapsible proof, which clipped the open menu to the height of
 *      its own summary -- the panel still measured 532px and reported itself
 *      visible.
 *
 * So geometry is not the test. This asks the browser what is painted at three
 * points inside the open panel, and compares each label's computed colour with
 * the bar's computed background.
 *
 * MUTATION TESTED, because a check that has never failed proves nothing:
 * putting overflow:hidden back fails 11 of 33; removing the colour reset fails
 * 12 of 33, naming 4 invisible labels on each subject page.
 *
 * It also runs every page a third time with JavaScript disabled, which is the
 * claim the whole <details> design rests on.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const BASE = process.argv[2] || 'http://127.0.0.1:8812';
const EXEC = process.env.CHROMIUM || '/opt/pw-browsers/chromium';

// One page of every kind: the two stylesheets, the two generated sections,
// the inline-styled maps, the three top-level pages and the error page.
const PAGES = [
  ['home',        '/index.html'],
  ['statistics',  '/statistics/bsc/theory-of-probability/unit1.html'],
  ['msc',         '/statistics/msc/probability-theory/unit1.html'],
  ['datascience', '/data-science/machine-learning/unit1.html'],
  ['exams-hub',   '/exams/index.html'],
  ['iss',         '/exams/iss/paper1.html'],
  ['ugcnet',      '/exams/ugc-net/unit3.html'],
  ['subjects',    '/subjects/economics/unit1.html'],
  ['guide',       '/guides/which-test.html'],
  ['topics',      '/topics.html'],
  ['notfound',    '/404.html'],
  ['about',       '/about.html'],
  // 404.html is served for a missing URL at ANY depth with that URL still in
  // the address bar, so it is also loaded two folders down (see below).
  ['notfound-deep', '/statistics/bsc/no-such-page.html'],
];

// The site lives under this path on its host; locally it is served from "/".
// Root-absolute links (only 404.html writes them) are mapped back here.
const SITE_BASE = 'https://nrstatlab.github.io/planning-for-future';
const BASE_PATH = new URL(SITE_BASE).pathname.replace(/\/?$/, '/');

const VIEWS = [
  [1180, 'wide',  true],
  [400,  'phone', true],
  [400,  'nojs',  false],   // the menu must work with no script at all
];

const MENUS = 4;            // Statistics, Data Science, Examinations, Subjects
const MIN_LINKS = 70;       // 78 today; a section lost would show up here
const MAX_PHONE_NAV = 96;   // the sticky row it replaced ate ~120px of 400px

(async () => {
  const browser = await chromium.launch({ executablePath: EXEC });
  let bad = 0, n = 0;

  for (const [width, tag, js] of VIEWS) {
    const ctx = await browser.newContext({
      viewport: { width, height: 900 }, javaScriptEnabled: js });
    for (const [name, url] of PAGES) {
      const page = await ctx.newPage();
      if (name === 'notfound-deep') {
        // What GitHub Pages does: answer a missing URL with 404.html's bytes.
        await page.route('**' + url, r => r.fulfill({ status: 404, path: '404.html', contentType: 'text/html' }));
      }
      await page.route('**' + BASE_PATH + '**', r =>
        r.continue({ url: r.request().url().replace(BASE_PATH, '/') }));
      const errs = [];
      page.on('pageerror', e => errs.push(String(e)));
      page.on('response', r => {
        if (r.status() >= 400 && !(name === 'notfound-deep' && r.url().endsWith(url)))
          errs.push(r.status() + ' ' + r.url());
      });
      await page.goto(BASE + url, { waitUntil: 'networkidle', timeout: 30000 });

      const m = await page.evaluate(() => ({
        navs: document.querySelectorAll('nav.sitenav').length,
        menus: document.querySelectorAll('details.sitenav-menu').length,
        links: document.querySelectorAll('.sitenav a').length,
        current: document.querySelectorAll('.sitenav [aria-current="page"]').length,
        skip: !!document.querySelector('.nav-skip'),
        target: !!document.querySelector('#nrstat-content'),
        navH: Math.round(document.querySelector('nav.sitenav').getBoundingClientRect().height),
        over: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        feet: document.querySelectorAll('footer.sitefoot').length,
        dated: /^\d{4}-\d{2}-\d{2}$/.test((document.querySelector('.sitefoot time') || {}).getAttribute?.('datetime') || ''),
        icon: (document.querySelector('link[rel="icon"][type="image/svg+xml"]') || {}).href || '',
        og: (document.querySelector('meta[property="og:image"]') || {}).content || '',
        navCss: [...document.styleSheets].some(ss => (ss.href || '').endsWith('site-nav.css') && ss.cssRules.length > 0),
      }));
      // Phase 1: the icon and the share card must actually be fetchable.
      const fetchOk = async u => {
        try { return (await page.request.get(u)).ok(); } catch (e) { return false; }
      };
      const iconOk = m.icon && await fetchOk(m.icon.replace(BASE_PATH, '/'));
      const ogOk = m.og.startsWith(SITE_BASE + '/') &&
        await fetchOk(BASE + '/' + m.og.slice(SITE_BASE.length + 1));

      // Open the widest menu and check it is really there, not merely present.
      const summaries = await page.$$('details.sitenav-menu > summary');
      await summaries[2].click();
      const o = await page.evaluate(() => {
        const d = document.querySelectorAll('details.sitenav-menu')[2];
        const pnl = d.querySelector('.sitenav-panel');
        const r = pnl.getBoundingClientRect();
        const pts = [[r.x + 20, r.y + 12],
                     [r.x + r.width / 2, r.y + Math.min(60, r.height - 6)],
                     [r.x + 20, r.y + Math.min(r.height - 6, innerHeight - 6)]];
        const painted = pts.every(([x, y]) => {
          if (x < 0 || y < 0 || x > innerWidth || y > innerHeight) return true;
          const e = document.elementFromPoint(x, y);
          return e && pnl.contains(e);
        });
        const barBg = getComputedStyle(document.querySelector('.sitenav')).backgroundColor;
        const invisible = [...document.querySelectorAll('.sitenav-menu > summary')]
          .filter(s => getComputedStyle(s).color === barBg).length;
        return { open: d.open, h: Math.round(r.height), w: Math.round(r.width),
                 offscreen: r.right > innerWidth + 1 || r.left < -1, painted, invisible };
      });

      const why = [];
      if (m.navs !== 1) why.push(`navs=${m.navs}`);
      if (m.menus !== MENUS) why.push(`menus=${m.menus}`);
      if (m.links < MIN_LINKS) why.push(`links=${m.links}`);
      if (!m.skip) why.push('no skip link');
      if (m.feet !== 1) why.push(`${m.feet} site footers`);
      if (!m.dated) why.push('footer has no content date');
      if (!iconOk) why.push('favicon does not resolve: ' + m.icon);
      if (!ogOk) why.push('share card does not resolve: ' + m.og);
      if (!m.navCss) why.push('the navigation stylesheet did not load');
      if (!m.target) why.push('skip link has no target');
      if (m.over > 2) why.push(`${m.over}px of horizontal scroll`);
      if (tag !== 'wide' && m.navH > MAX_PHONE_NAV) why.push(`bar is ${m.navH}px tall`);
      if (!o.open) why.push('menu did not open');
      if (o.h <= 40) why.push(`panel only ${o.h}px tall`);
      if (o.offscreen) why.push('panel runs off the screen');
      if (!o.painted) why.push('panel is CLIPPED or covered');
      if (o.invisible) why.push(`${o.invisible} label(s) the same colour as the bar`);
      for (const e of errs) why.push(e.slice(0, 100));

      n++;
      if (why.length) bad++;
      console.log(`${(why.length ? 'PROBLEM' : 'ok').padEnd(8)} ${tag.padEnd(5)} ` +
        `${name.padEnd(11)} nav=${m.navs} menus=${m.menus} links=${m.links} ` +
        `current=${m.current} navH=${m.navH}px panel=${o.h}x${o.w}` +
        (why.length ? '\n         ' + why.join('; ') : ''));
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  console.log(bad === 0
    ? `\n${n} page loads across ${VIEWS.length} viewports, all clean`
    : `\n${bad} of ${n} page loads have a problem`);
  process.exit(bad ? 1 : 0);
})();
