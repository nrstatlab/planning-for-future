#!/usr/bin/env node
/* Check the 3D Statistics library against independent reference values.

     node tools/check_stats3d.js

   tools/stats3d_reference.json holds fixed data sets and, for each function
   of assets/stats3d-lib.js, the value scipy/statsmodels give for them
   (tools/stats3d_reference.py). Every number must agree to 1e-9 relative
   (1e-7 for p-values and quantiles, which go through series and
   continued fractions; 1e-6 for the few maximum-likelihood estimates a case
   marks). No server is needed. */
'use strict';
const path = require('path');
const S = require(path.join(__dirname, '..', 'assets', 'stats3d-lib.js'));
const ref = require(path.join(__dirname, 'stats3d_reference.json'));

function arg(a) {
  if (a && typeof a === 'object' && !Array.isArray(a) && a.data) {
    const v = ref.data[a.data][a.var];
    return a.len ? v.slice(0, a.len) : v.slice();
  }
  if (Array.isArray(a)) return a.map(arg);
  return a;
}
function get(obj, key) {
  if (key === '') return obj;
  return key.split('.').reduce((o, k) => (o == null ? undefined : o[k]), obj);
}
const LOOSE = /(^|\.)(p|pB|pA|pF|ci|chi|ks)\b|Inv$|Cdf$|Sf$/;

let checked = 0;
const fails = [];
for (const c of ref.cases) {
  const args = c.args.map(arg);
  let out;
  if (c.fn === 'fit') out = S.fit(args[0], args[1], args[2]);
  else out = S[c.fn].apply(null, args);
  for (const [k, want] of Object.entries(c.expect)) {
    const got = get(out, k);
    const tol = c.tol || (LOOSE.test(k) || LOOSE.test(c.fn) ? 1e-7 : 1e-9);
    const ok = typeof got === 'number' && Math.abs(got - want) <= tol * Math.max(1, Math.abs(want));
    checked++;
    if (!ok) fails.push(`${c.fn}(${JSON.stringify(c.args).slice(0, 90)}) ${k}: got ${got}, want ${want}`);
  }
}
if (fails.length) {
  fails.slice(0, 60).forEach(f => console.log('FAIL', f));
  console.log(`${fails.length} of ${checked} values differ`);
  process.exit(1);
}
console.log(`3D Statistics library: ${checked} values agree with the reference (${ref.cases.length} cases)`);
