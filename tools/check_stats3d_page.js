#!/usr/bin/env node
/* Drive the 3D Statistics page in a browser and check every panel and test.

     node tools/check_stats3d_page.js http://127.0.0.1:8813 [--shots=DIR]

   Serve the site first (python3 -m http.server 8813). If MATHJAX_DIR points
   at a local copy of MathJax 3's es5 folder, formulas are typeset from it
   and checked for errors; otherwise MathJax is blocked and only the page's
   own behaviour is checked. For every width (390, 800, 1280 px) and scheme
   (light, dark) it:
     - loads the example, opens each panel, runs all 23 tests and the
       distribution comparison, and the "specify a distribution" test;
     - loads the unequal-sizes example and finds the course's ANOVA F;
     - sets five variables of 50 through the size form, pastes them and runs
       every test;
     - pastes five columns of unequal sizes and requires the paired tests to
       refuse (naming the sizes) and every other test to give a decision;
     - requires no script error, no MathJax error, no sideways scroll, a 3-D
       plot that turns when dragged, and every course link to resolve. */
'use strict';
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const BASE = args.find((a) => a.startsWith('http')) || 'http://127.0.0.1:8813';
const SHOTS = (args.find((a) => a.startsWith('--shots=')) || '').split('=')[1];
const MJ = process.env.MATHJAX_DIR;
const ROOT = path.resolve(__dirname, '..');
const ref = require(path.join(__dirname, 'stats3d_reference.json'));

const NUMS = { mu0: '15', sigma: '5', sigma2: '4', s0sq: '60', d0: '0', rho0: '0.5', m0: '15' };
const BIG_NUMS = { mu0: '48', sigma: '10', sigma2: '9', s0sq: '90', d0: '0', rho0: '0.5', m0: '48' };

// Tests that need equal sample sizes; with unequal sizes they must refuse.
const PAIRED = ['tpaired', 'rZero', 'rFisher', 'partial', 'multiple', 'reg1', 'reg2', 'sign2', 'wil2'];

async function runAllTests(page, nums, refused) {
  const ids = await page.$$eval('#s3-test option', (o) => o.map((x) => x.value));
  const bad = [];
  for (const id of ids) {
    await page.selectOption('#s3-test', id);
    for (const [k, v] of Object.entries(nums)) {
      const sel = '#s3-test-params input[data-p="' + k + '"]';
      if (await page.$(sel)) await page.fill(sel, v);
    }
    await page.click('#s3-test-go');
    const out = await page.$eval('#s3-test-out', (e) => ({
      decision: !!e.querySelector('.s3-decision'), note: (e.querySelector('.s3-note') || {}).textContent || '' }));
    if (refused && refused.includes(id)) {
      if (out.decision || !/equal sample sizes/.test(out.note)) bad.push(id + ' should refuse unequal sizes: ' + (out.note || 'ran'));
    } else if (!out.decision) bad.push(id + ': ' + (out.note || 'no result'));
  }
  return { n: ids.length, bad };
}

async function mathjaxDone(page) {
  if (!MJ) return 0;
  await page.waitForFunction(() => window.MathJax && MathJax.startup && MathJax.startup.promise, null, { timeout: 30000 });
  await page.evaluate(() => MathJax.startup.promise);
  await page.waitForTimeout(400);
  await page.evaluate(() => MathJax.typesetPromise ? MathJax.typesetPromise() : null);
  return page.evaluate(() => document.querySelectorAll('mjx-merror').length);
}
async function overflow(page) {
  return page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium' });
  let problems = 0;
  const big = ref.data.big, rows = [];
  for (let i = 0; i < 50; i++) {
    rows.push([big.y[i], big.x1[i], big.x2[i], big.y[50 + i], big.x1[50 + i]].join('\t'));
  }
  const paste = rows.join('\n');
  const five = ref.data.five, g = ['g1', 'g2', 'g3', 'g4', 'g5'], ragged = [g.join('\t')];
  const longest = Math.max(...g.map((k) => five[k].length));
  for (let i = 0; i < longest; i++) ragged.push(g.map((k) => (i < five[k].length ? five[k][i] : '')).join('\t'));
  const pasteRagged = ragged.join('\n');
  const links = new Set();

  for (const scheme of ['light', 'dark']) {
    for (const width of [390, 800, 1280]) {
      const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme });
      await ctx.route('**/*', (r) => {
        const u = r.request().url();
        if (u.includes('cdn.jsdelivr.net/npm/mathjax@3/es5/')) {
          if (!MJ) return r.abort();
          return r.fulfill({ path: path.join(MJ, u.split('/es5/')[1].split('?')[0]) });
        }
        return u.startsWith(BASE) ? r.continue() : r.abort();
      });
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', (e) => errors.push(String(e)));
      page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push(m.text()); });
      await page.goto(BASE + '/3d-statistics/index.html');
      const why = [];
      try { await page.evaluate(() => localStorage.clear()); } catch (e) { /* none */ }

      // 1. the example is there on a first visit
      const cells = await page.$$eval('#s3-grid input', (i) => i.filter((x) => x.value !== '').length);
      if (cells !== 15) why.push('example cells=' + cells);

      // 2. descriptive: the worked course values appear
      await page.click('#tab-descriptive');
      await page.waitForSelector('#s3-three canvas');
      const text = await page.textContent('#s3-desc');
      for (const v of ['0.9882', '0.9875', '0.997']) if (!text.includes(v)) why.push('descriptive lacks ' + v);
      // the 3-D plot turns when dragged
      const canvas = await page.$('#s3-3d-host canvas');
      const before = await canvas.screenshot();
      const box = await canvas.boundingBox();
      await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
      await page.mouse.down();
      await page.mouse.move(box.x + box.width / 2 + 80, box.y + box.height / 2 + 30, { steps: 5 });
      await page.mouse.up();
      const after = await canvas.screenshot();
      if (before.equals(after)) why.push('3-D plot did not turn');
      await page.$$eval('#s3-desc details', (d) => d.forEach((x) => { x.open = true; }));
      const mjErr1 = await mathjaxDone(page);
      if (mjErr1) why.push('MathJax errors (descriptive): ' + mjErr1);
      if (await overflow(page) > 0) why.push('sideways scroll on descriptive');
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `desc-${width}-${scheme}.png`), fullPage: true });

      // 3. every test on the example
      await page.click('#tab-inferential');
      let r = await runAllTests(page, NUMS);
      if (r.bad.length) why.push('example tests: ' + r.bad.join('; '));
      const mjErr2 = await mathjaxDone(page);
      if (mjErr2) why.push('MathJax errors (tests): ' + mjErr2);
      if (await overflow(page) > 0) why.push('sideways scroll on tests');

      // 4. distributions, then a specified one
      await page.click('#tab-distributions');
      await page.click('#s3-dist-go');
      await page.waitForSelector('#s3-dist-out .s3-card');
      await page.$$eval('#s3-dist-out details', (d) => d.forEach((x) => { x.open = true; }));
      await page.selectOption('#s3-spec-dist', 'normal');
      await page.fill('#s3-spec-params [data-sp="mu"]', '20');
      await page.fill('#s3-spec-params [data-sp="sigma"]', '8');
      await page.click('#s3-spec-go');
      if (!(await page.$('#s3-spec-out .s3-decision'))) why.push('specified distribution: ' + (await page.textContent('#s3-spec-out')));
      const mjErr3 = await mathjaxDone(page);
      if (mjErr3) why.push('MathJax errors (distributions): ' + mjErr3);
      if (await overflow(page) > 0) why.push('sideways scroll on distributions');
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `dist-${width}-${scheme}.png`), fullPage: true });

      // 5. the unequal-sizes example reproduces the course's ANOVA
      await page.click('#tab-data');
      await page.click('#s3-example2');
      await page.click('#tab-inferential');
      await page.selectOption('#s3-test', 'anova');
      await page.click('#s3-test-go');
      if (!(await page.textContent('#s3-test-out')).includes('4.8848')) why.push('machines ANOVA F not 4.8848');

      // 6. five variables of 50 through the size form, then typed by paste
      await page.click('#tab-data');
      await page.selectOption('#s3-k', '5');
      await page.fill('#s3-size-all', '50');
      await page.click('#s3-size-same');
      if (!/Balanced design/.test(await page.textContent('#s3-balance'))) why.push('size form: not balanced');
      const cellCount = (await page.$$('#s3-grid input')).length;
      if (cellCount !== 250) why.push('grid cells=' + cellCount);
      await page.fill('#s3-size-0', '70');
      await page.dispatchEvent('#s3-size-0', 'change');
      if ((await page.inputValue('#s3-size-0')) !== '50') why.push('size above 50 accepted');
      await page.click('.s3-paste summary');
      await page.fill('#s3-paste-text', paste);
      await page.click('#s3-paste-go');
      const status = await page.textContent('#s3-status');
      if ((status.match(/: 50 of 50/g) || []).length !== 5) why.push('paste status: ' + status);
      if (await overflow(page) > 0) why.push('sideways scroll on the data grid');
      await page.click('#tab-inferential');
      r = await runAllTests(page, BIG_NUMS);
      if (r.bad.length) why.push('5 x 50 tests: ' + r.bad.join('; '));

      // 7. five columns of unequal sizes: paired tests refuse, the rest run
      await page.click('#tab-data');
      await page.click('.s3-paste summary');
      await page.fill('#s3-paste-text', pasteRagged);
      await page.click('#s3-paste-go');
      const sizes = [];
      for (let i = 0; i < 5; i++) sizes.push(await page.inputValue('#s3-size-' + i));
      if (sizes.join(',') !== '12,15,10,8,20') why.push('ragged sizes ' + sizes.join(','));
      if (!/Unbalanced/.test(await page.textContent('#s3-balance'))) why.push('ragged: not unbalanced');
      await page.click('#tab-inferential');
      r = await runAllTests(page, { mu0: '21', sigma: '3', sigma2: '4', s0sq: '10', d0: '0', rho0: '0.5', m0: '21' }, PAIRED);
      if (r.bad.length) why.push('unequal-size tests: ' + r.bad.join('; '));
      await page.click('#tab-descriptive');
      await page.waitForSelector('#s3-box svg');
      if (!/equal sample sizes/.test(await page.textContent('#s3-pair-out'))) why.push('pair panel did not refuse unequal sizes');
      if (SHOTS) await page.screenshot({ path: path.join(SHOTS, `unequal-${width}-${scheme}.png`), fullPage: true });

      // back to the balanced five variables for the distribution and 3-D checks
      await page.click('#tab-data');
      await page.click('.s3-paste summary');
      await page.fill('#s3-paste-text', paste);
      await page.click('#s3-paste-go');
      await page.click('#tab-distributions');
      for (const v of ['0', '2']) {
        await page.selectOption('#s3-dist-var', v);
        await page.click('#s3-dist-go');
        await page.waitForSelector('#s3-dist-out .s3-card');
      }
      await page.click('#tab-descriptive');
      await page.waitForSelector('#s3-three canvas');
      const mjErr4 = await mathjaxDone(page);
      if (mjErr4) why.push('MathJax errors (100 rows): ' + mjErr4);
      if (await overflow(page) > 0) why.push('sideways scroll with 100 rows');

      (await page.$$eval('a[href]', (a) => a.map((x) => x.getAttribute('href'))))
        .filter((h) => h.startsWith('../statistics/')).forEach((h) => links.add(h));
      if (errors.length) why.push('script errors: ' + errors.slice(0, 3).join(' | '));
      console.log((why.length ? 'PROBLEM ' : 'ok      ') + scheme.padEnd(6) + String(width).padEnd(5) +
        (why.length ? why.join(' / ') : 'example, machines ANOVA, 23 tests on 5 x 50 and on unequal sizes, distributions'));
      problems += why.length ? 1 : 0;
      await ctx.close();
    }
  }
  await browser.close();

  // every course link and its section exist
  const missing = [];
  for (const h of links) {
    const [file, anchor] = h.split('#');
    const p = path.join(ROOT, '3d-statistics', file);
    if (!fs.existsSync(p)) { missing.push(h); continue; }
    if (anchor && !fs.readFileSync(p, 'utf8').includes('id="' + decodeURIComponent(anchor) + '"')) missing.push(h);
  }
  if (missing.length) { console.log('PROBLEM links: ' + missing.join(', ')); problems++; }
  else console.log('ok      ' + links.size + ' course links and their sections exist');
  if (!MJ) console.log('note    MathJax was not loaded (set MATHJAX_DIR to check formulas)');
  process.exit(problems ? 1 : 0);
})();
