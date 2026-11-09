/* StatsTricks360 — the 3D Statistics page (3d-statistics/index.html).

   Data entry, the four panels, the worked steps and the charts. All the
   mathematics is in assets/stats3d-lib.js (window.Stats3D), which
   tools/check_stats3d.js tests against scipy; this file only reads the
   grid, calls it and writes the results. Nothing is sent anywhere. */
(function () {
  'use strict';
  const S = window.Stats3D;
  const page = document.getElementById('s3');
  if (!S || !page) return;
  const $ = (id) => document.getElementById(id);
  const MAXN = 50;
  const STORE = 'statstricks360.stats3d.v2';

  /* ---------------------------------------------------------------- links */
  const C = '../statistics/';
  const LEARN = {
    mean: [C + 'descriptive-statistics/unit3.html#2-arithmetic-mean-am', 'Arithmetic mean'],
    median: [C + 'descriptive-statistics/unit3.html#3-median', 'Median'],
    mode: [C + 'descriptive-statistics/unit3.html#4-mode', 'Mode'],
    gm: [C + 'descriptive-statistics/unit3.html#6-geometric-mean-gm', 'Geometric mean'],
    hm: [C + 'descriptive-statistics/unit3.html#7-harmonic-mean-hm', 'Harmonic mean'],
    range: [C + 'descriptive-statistics/unit4.html#2-range', 'Range'],
    qd: [C + 'descriptive-statistics/unit4.html#3-quartile-deviation-qd-semi-inter-quartile-range', 'Quartiles and quartile deviation'],
    md: [C + 'descriptive-statistics/unit4.html#4-mean-deviation-md', 'Mean deviation'],
    sd: [C + 'descriptive-statistics/unit4.html#5-standard-deviation-sd-and-variance', 'Standard deviation and variance'],
    moments: [C + 'descriptive-statistics/unit5.html#3-central-moments', 'Central moments'],
    skew: [C + 'descriptive-statistics/unit5.html#6-skewness', 'Skewness'],
    kurt: [C + 'descriptive-statistics/unit5.html#7-kurtosis', 'Kurtosis'],
    freq: [C + 'descriptive-statistics/unit2.html#2-frequency-distribution', 'Frequency distribution'],
    graphs: [C + 'descriptive-statistics/unit2.html#4-graphical-representation', 'Graphs of a frequency distribution'],
    pearson: [C + 'statistical-methods/unit2.html#4-karl-pearsons-coefficient-of-correlation', "Karl Pearson's correlation coefficient"],
    spearman: [C + 'statistical-methods/unit2.html#5-spearmans-rank-correlation-coefficient', "Spearman's rank correlation"],
    regression: [C + 'statistical-methods/unit4.html#3-two-lines-of-regression', 'The two lines of regression'],
    partial: [C + 'statistical-methods/unit3.html#5-partial-correlation-coefficient', 'Partial correlation'],
    multiple: [C + 'statistical-methods/unit3.html#4-multiple-correlation-coefficient-three-variables', 'Multiple correlation'],
    plane: [C + 'econometrics/unit2.html#5-the-general-linear-multiple-regression-model', 'Multiple regression'],
    z1: [C + 'inferential-statistics/unit3.html#2-z-test-for-single-mean', 'z test for a single mean'],
    z2: [C + 'inferential-statistics/unit3.html#3-z-test-for-difference-of-two-means', 'z test for two means'],
    t1: [C + 'inferential-statistics/unit4.html#2-t-test-for-single-mean', 't test for a single mean'],
    t2: [C + 'inferential-statistics/unit4.html#3-t-test-for-difference-of-two-means-independent-samples', 't test for two means'],
    tp: [C + 'inferential-statistics/unit4.html#4-paired-t-test-dependent-samples', 'Paired t test'],
    chiVar: [C + 'inferential-statistics/unit4.html#7-%CF%87%C2%B2-test-for-single-variance', '\u03c7\u00b2 test for a variance'],
    fVar: [C + 'inferential-statistics/unit4.html#8-f-test-for-equality-of-two-variances', 'F test for two variances'],
    ci: [C + 'inferential-statistics/unit1.html#5-confidence-intervals-cis', 'Confidence intervals'],
    anova: [C + 'design-and-analysis-of-experiments/unit1.html#2-one-way-anova', 'One-way analysis of variance'],
    cd: [C + 'design-and-analysis-of-experiments/unit1.html#critical-difference', 'Critical difference'],
    bartlett: [C + 'design-and-analysis-of-experiments/unit1.html#assumptions-of-anova', 'Assumptions of ANOVA'],
    rZero: [C + 'inferential-statistics/unit4.html#t-test-for-a-correlation-coefficient', 't test for a correlation coefficient'],
    rFisher: [C + 'inferential-statistics/unit3.html#fishers-z-transformation-for-rho-rho-0-ne-0', "Fisher's z transformation"],
    partialTest: [C + 'multivariate-analysis/unit2.html#4-multiple-and-partial-correlation-coefficients', 'Tests of partial and multiple correlation'],
    regT: [C + 'econometrics/unit3.html#11-t-test-for-an-individual-coefficient', 't test for a regression coefficient'],
    regF: [C + 'econometrics/unit3.html#22-anova-table-for-regression', 'ANOVA table for regression'],
    sign: [C + 'inferential-statistics/unit5.html#3-sign-test', 'Sign test'],
    wilcoxon: [C + 'inferential-statistics/unit5.html#4-wilcoxon-signed-rank-test', 'Wilcoxon signed-rank test'],
    mw: [C + 'inferential-statistics/unit5.html#6-wilcoxonmannwhitney-u-test', 'Mann\u2013Whitney U test'],
    kw: [C + 'inferential-statistics/unit5.html#8-kruskalwallis-test-non-parametric-one-way-anova', 'Kruskal\u2013Wallis test'],
    runs: [C + 'inferential-statistics/unit5.html#2-one-sample-runs-test-test-for-randomness', 'Runs test for randomness'],
    ks: [C + 'inferential-statistics/unit5.html#9-kolmogorovsmirnov-ks-test', 'Kolmogorov\u2013Smirnov test'],
    gof: [C + 'inferential-statistics/unit4.html#5-%CF%87%C2%B2-test-for-goodness-of-fit', '\u03c7\u00b2 test of goodness of fit'],
    mom: [C + 'inferential-statistics/unit1.html#31-method-of-moments-mom', 'Method of moments'],
    mle: [C + 'inferential-statistics/unit1.html#32-method-of-maximum-likelihood-mle', 'Maximum likelihood'],
    degenerate: [C + 'theoretical-discrete-distributions/unit1.html#2-bernoulli-distribution', 'Discrete distributions'],
    bernoulli: [C + 'theoretical-discrete-distributions/unit1.html#2-bernoulli-distribution', 'Bernoulli distribution'],
    binomial: [C + 'theoretical-discrete-distributions/unit1.html#3-binomial-distribution', 'Binomial distribution'],
    poisson: [C + 'theoretical-discrete-distributions/unit2.html#1-definition-pmf', 'Poisson distribution'],
    negbinomial: [C + 'theoretical-discrete-distributions/unit3.html#1-definition-pmf', 'Negative binomial distribution'],
    geometric: [C + 'theoretical-discrete-distributions/unit4.html#1-definition-pmf', 'Geometric distribution'],
    hypergeometric: [C + 'theoretical-discrete-distributions/unit5.html#1-definition-pmf', 'Hypergeometric distribution'],
    duniform: [C + 'theoretical-discrete-distributions/unit1.html#1-discrete-uniform-distribution', 'Discrete uniform distribution'],
    uniform: [C + 'theoretical-continuous-distributions/unit1.html#1-definition-pdf', 'Uniform distribution'],
    exponential: [C + 'theoretical-continuous-distributions/unit2.html#1-definition-pdf', 'Exponential distribution'],
    weibull: [C + 'theoretical-continuous-distributions/unit2.html#7-weibull-distribution', 'Weibull distribution'],
    laplace: [C + 'theoretical-continuous-distributions/unit2.html#8-laplace-double-exponential-distribution', 'Laplace distribution'],
    gamma: [C + 'theoretical-continuous-distributions/unit3.html#2-gamma-distribution', 'Gamma distribution'],
    beta1: [C + 'theoretical-continuous-distributions/unit3.html#3-beta-distribution-of-first-kind', 'Beta distribution of the first kind'],
    beta2: [C + 'theoretical-continuous-distributions/unit3.html#4-beta-distribution-of-second-kind', 'Beta distribution of the second kind'],
    normal: [C + 'theoretical-continuous-distributions/unit4.html#1-definition-pdf', 'Normal distribution'],
    cauchy: [C + 'theoretical-continuous-distributions/unit4.html#11-cauchy-distribution', 'Cauchy distribution'],
    lognormal: [C + 'theoretical-continuous-distributions/unit4.html#12-lognormal-distribution', 'Lognormal distribution'],
    pareto: [C + 'distribution-theory/unit1.html#4-the-pareto-distribution', 'Pareto distribution'],
    logistic: null
  };
  function learn(key, text) {
    const l = LEARN[key];
    if (!l) return '';
    return '<a href="' + l[0] + '">' + esc(text || l[1]) + '</a>';
  }
  function learnLine(keys) {
    const links = keys.map((k) => learn(k)).filter(Boolean);
    return links.length ? '<p class="s3-learn">Learn this: ' + links.join(' &middot; ') + '</p>' : '';
  }

  /* ---------------------------------------------------------------- formatting */
  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  /* A number for a table: four decimals, trimmed; scientific when tiny or huge. */
  function f(v, dp) {
    if (v === null || v === undefined || Number.isNaN(v)) return '&ndash;';
    if (!isFinite(v)) return v > 0 ? '&infin;' : '&minus;&infin;';
    dp = dp === undefined ? 4 : dp;
    const a = Math.abs(v);
    if (a !== 0 && (a < Math.pow(10, -dp) || a >= 1e9)) {
      const [m, e] = v.toExponential(3).split('e');
      return m.replace('-', '&minus;') + ' &times; 10<sup>' + e.replace('+', '').replace('-', '&minus;') + '</sup>';
    }
    let s = (+v.toFixed(dp)).toString();
    if (s === '-0') s = '0';
    return s.replace('-', '&minus;');
  }
  /* The same number in TeX. */
  function t(v, dp) {
    if (v === null || v === undefined || Number.isNaN(v)) return '\\text{--}';
    if (!isFinite(v)) return v > 0 ? '\\infty' : '-\\infty';
    dp = dp === undefined ? 4 : dp;
    const a = Math.abs(v);
    if (a !== 0 && (a < Math.pow(10, -dp) || a >= 1e9)) {
      const [m, e] = v.toExponential(3).split('e');
      return m + ' \\times 10^{' + (+e) + '}';
    }
    let s = (+v.toFixed(dp)).toString();
    return s === '-0' ? '0' : s;
  }
  /* A value subtracted in a formula: (-3) rather than --3. */
  function tp(v, dp) { return v < 0 ? '(' + t(v, dp) + ')' : t(v, dp); }
  function pv(p) {
    if (p === null || p === undefined || Number.isNaN(p)) return '&ndash;';
    return p < 0.0001 ? '&lt; 0.0001' : f(p, 4);
  }
  function tpv(p) { return p < 0.0001 ? '< 0.0001' : t(p, 4); }
  /* "p = 0.0123" in TeX, or "p < 0.0001" when it is that small. */
  function pEq(p) { return 'p ' + (p < 0.0001 ? '< 0.0001' : '= ' + t(p, 4)); }
  function pct(a) { return (+(a * 100).toFixed(2)) + '%'; }
  function tex(s) { return '\\(' + s + '\\)'; }
  function disp(s) { return '\\[' + s + '\\]'; }
  function nameT(i) { return '\\text{' + texText(names()[i]) + '}'; }
  /* A variable name inside TeX: TeX's special characters and anything HTML
     could read as markup are dropped, since the TeX goes into innerHTML. */
  function texText(s) { return String(s).replace(/[\\{}$&#^_%~<>"']/g, ''); }
  function tn(s) { return '\\text{' + texText(s) + '}'; }

  function typeset(el) {
    let tries = 0;
    (function go() {
      if (window.MathJax && window.MathJax.typesetPromise && window.MathJax.startup) {
        window.MathJax.startup.promise.then(() => window.MathJax.typesetPromise([el])).catch(() => {});
      } else if (tries++ < 100) setTimeout(go, 150);
    })();
  }

  /* ---------------------------------------------------------------- data */
  /* Up to MAXK variables, each with its own sample size n_j (2 to MAXN),
     chosen before the values are typed: equal sizes make a balanced design. */
  const MAXK = 5;
  const DEFAULT_NAMES = ['X1', 'X2', 'X3', 'X4', 'X5'];
  const state = { k: 3, sizes: [10, 10, 10, 10, 10], names: DEFAULT_NAMES.slice(), values: [] };
  for (let c = 0; c < MAXK; c++) state.values[c] = new Array(MAXN).fill('');

  function names() { return state.names.map((s, i) => (s && s.trim()) || DEFAULT_NAMES[i]); }
  function sizes() { return state.sizes.slice(0, state.k); }
  function maxRows() { return Math.max.apply(null, sizes()); }

  function parseNum(s) {
    s = String(s).trim().replace(/−/g, '-');
    if (s === '') return null;
    if (!/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(s)) return NaN;
    return Number(s);
  }

  /* Each column's numbers, and a list of what is wrong: a cell inside the
     declared size that is empty or not a number. */
  function readData() {
    const cols = [], errors = [], nm = names();
    for (let c = 0; c < state.k; c++) {
      const col = [];
      for (let r = 0; r < state.sizes[c]; r++) {
        const v = parseNum(state.values[c][r]);
        if (v === null) errors.push(nm[c] + ', row ' + (r + 1) + ' is empty.');
        else if (Number.isNaN(v)) errors.push(nm[c] + ', row ' + (r + 1) + ' (“' + state.values[c][r] + '”) is not a number.');
        else col.push(v);
      }
      cols.push(col);
    }
    return { cols, errors, sizes: sizes() };
  }
  /* The columns a paired calculation uses; they must be of equal size. */
  function paired(data, idx) {
    const n = idx.map((c) => data.sizes[c]);
    if (n.some((v) => v !== n[0])) throw new Error(equalSizes(idx));
    return idx.map((c) => data.cols[c]);
  }
  function equalSizes(idx) {
    const nm = names();
    return 'This needs equal sample sizes (a balanced design): ' +
      idx.map((c) => nm[c] + ' has n = ' + state.sizes[c]).join(', ') +
      '. Make the sizes equal on the Enter data tab, or choose a test for independent samples.';
  }

  /* ---------------------------------------------------------------- the form */
  const grid = $('s3-grid');
  function buildSizes() {
    for (let c = 0; c < MAXK; c++) {
      $('s3-name-' + c).parentNode.hidden = c >= state.k;
      $('s3-size-' + c).parentNode.hidden = c >= state.k;
      $('s3-size-' + c).value = String(state.sizes[c]);
      const lab = $('s3-size-' + c).parentNode.querySelector('.s3-size-name');
      if (lab) lab.textContent = names()[c];
    }
    balanceLine();
  }
  function balanceLine() {
    const s = sizes(), el = $('s3-balance');
    if (state.k === 1) { el.textContent = 'One variable: n = ' + s[0] + '.'; return; }
    el.innerHTML = s.every((v) => v === s[0])
      ? '<strong>Balanced design:</strong> every n = ' + s[0] + '. Paired tests, correlation and regression are available.'
      : '<strong>Unbalanced:</strong> ' + s.map((v, i) => 'n<sub>' + (i + 1) + '</sub> = ' + v).join(', ') +
        '. Tests for independent samples (two-sample t, F, ANOVA, Mann&ndash;Whitney, Kruskal&ndash;Wallis) work with these sizes; paired tests, correlation and regression need equal sizes.';
  }
  function buildGrid() {
    const nm = names(), rows = maxRows();
    let h = '<thead><tr><th class="s3-row" scope="col">#</th>';
    for (let c = 0; c < state.k; c++) h += '<th scope="col">' + esc(nm[c]) + '<br><span class="s3-sub">n = ' + state.sizes[c] + '</span></th>';
    h += '</tr></thead><tbody>';
    for (let r = 0; r < rows; r++) {
      h += '<tr><th class="s3-row" scope="row">' + (r + 1) + '</th>';
      for (let c = 0; c < state.k; c++) {
        if (r >= state.sizes[c]) { h += '<td class="s3-off" aria-hidden="true"></td>'; continue; }
        const bad = Number.isNaN(parseNum(state.values[c][r]));
        h += '<td><input type="text" inputmode="decimal" autocomplete="off" spellcheck="false" data-c="' + c +
             '" data-r="' + r + '" aria-label="' + esc(nm[c]) + ', row ' + (r + 1) + '" value="' + esc(state.values[c][r]) + '"' +
             (bad ? ' class="s3-bad"' : '') + '></td>';
      }
      h += '</tr>';
    }
    grid.innerHTML = h + '</tbody>';
    status();
  }
  grid.addEventListener('input', (e) => {
    const el = e.target;
    if (!el.dataset || el.dataset.c === undefined) return;
    state.values[+el.dataset.c][+el.dataset.r] = el.value;
    el.classList.toggle('s3-bad', Number.isNaN(parseNum(el.value)));
    changed();
  });
  grid.addEventListener('keydown', (e) => {
    const el = e.target;
    if (e.key !== 'Enter' || el.dataset.c === undefined) return;
    e.preventDefault();
    const next = grid.querySelector('input[data-c="' + el.dataset.c + '"][data-r="' + (+el.dataset.r + 1) + '"]');
    if (next) next.focus();
  });
  /* Pasting several values into one cell spreads them from that cell; a
     column grows to hold what is pasted into it (up to MAXN). */
  grid.addEventListener('paste', (e) => {
    const el = e.target;
    if (el.dataset.c === undefined) return;
    const text = (e.clipboardData || window.clipboardData).getData('text');
    if (!/[\t\n,;]/.test(text.trim())) return;
    e.preventDefault();
    const lines = splitLines(text);
    const c0 = +el.dataset.c, r0 = +el.dataset.r;
    lines.forEach((cells, i) => cells.forEach((v, j) => {
      const c = c0 + j, r = r0 + i;
      if (c < MAXK && r < MAXN && v !== '') {
        state.values[c][r] = v;
        state.k = Math.max(state.k, c + 1);
        state.sizes[c] = Math.max(state.sizes[c], r + 1);
      }
    }));
    if (r0 + lines.length > MAXN || c0 + Math.max.apply(null, lines.map((l) => l.length)) > MAXK) flash = 'Only the first ' + MAXK + ' columns and ' + MAXN + ' rows are used.';
    syncControls(); buildSizes(); buildGrid(); changed();
  });

  function splitLines(text) {
    return text.replace(/\r/g, '').split('\n').filter((l) => l.trim() !== '')
      .map((l) => (/[\t;,]/.test(l) ? l.split(/\t|;|,(?=\s*[-+.\d−]|\s*$)|,\s+/) : l.trim().split(/\s+/)).map((v) => v.trim()));
  }

  let flash = '';
  function status() {
    const d = readData(), nm = names(), el = $('s3-status');
    const counts = d.cols.map((c, i) => esc(nm[i]) + ': ' + c.length + ' of ' + state.sizes[i]).join(' &middot; ');
    el.innerHTML = (flash ? esc(flash) + ' ' : '') + 'Filled: ' + counts +
      (d.errors.length ? '<br><span class="s3-err">' + esc(d.errors.slice(0, 3).join(' ')) +
        (d.errors.length > 3 ? ' (and ' + (d.errors.length - 3) + ' more)' : '') + '</span>' : '');
    flash = '';
  }
  function syncControls() {
    $('s3-k').value = String(state.k);
    for (let c = 0; c < MAXK; c++) $('s3-name-' + c).value = state.names[c];
  }

  let saveTimer = null;
  function changed() {
    status();
    clearOutputs();
    if ($('s3-remember').checked) {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(save, 300);
    }
  }
  function save() {
    try {
      localStorage.setItem(STORE, JSON.stringify({ k: state.k, sizes: state.sizes, names: state.names,
        values: state.values.map((col, c) => col.slice(0, state.sizes[c])) }));
    } catch (e) { /* storage unavailable: nothing is kept */ }
  }
  function load() {
    try {
      const raw = localStorage.getItem(STORE);
      if (!raw) return false;
      const o = JSON.parse(raw);
      state.k = Math.min(MAXK, Math.max(1, o.k | 0));
      for (let c = 0; c < MAXK; c++) {
        state.sizes[c] = Math.min(MAXN, Math.max(2, (o.sizes && o.sizes[c]) | 0));
        state.names[c] = String((o.names && o.names[c]) || DEFAULT_NAMES[c]).slice(0, 20);
        for (let r = 0; r < MAXN; r++) state.values[c][r] = (o.values && o.values[c] && o.values[c][r]) || '';
      }
      return true;
    } catch (e) { return false; }
  }
  function setSize(c, v) {
    let n = Math.round(+v);
    if (!(n >= 2)) { n = 2; flash = 'Each sample needs at least 2 observations.'; }
    if (n > MAXN) { n = MAXN; flash = 'At most ' + MAXN + ' observations per variable.'; }
    state.sizes[c] = n;
  }

  $('s3-k').addEventListener('change', () => { state.k = +$('s3-k').value; buildSizes(); buildGrid(); changed(); });
  for (let c = 0; c < MAXK; c++) {
    $('s3-name-' + c).addEventListener('input', () => {
      state.names[c] = $('s3-name-' + c).value;
      buildSizes(); buildGrid(); changed();
    });
    $('s3-size-' + c).addEventListener('change', () => {
      setSize(c, $('s3-size-' + c).value);
      buildSizes(); buildGrid(); changed();
    });
  }
  $('s3-size-same').addEventListener('click', () => {
    const v = $('s3-size-all').value;
    for (let c = 0; c < MAXK; c++) setSize(c, v);
    buildSizes(); buildGrid(); changed();
  });

  const EXAMPLES = {
    // Linear Algebra & Linear Models, Practical 13
    corr: { names: ['Y', 'X1', 'X2'], data: [[12, 18, 20, 28, 32], [2, 4, 6, 8, 10], [1, 3, 2, 5, 4]], note: 's3-example-note' },
    // Design & Analysis of Experiments, Unit 1, Worked Problem 1
    machines: { names: ['Machine A', 'Machine B', 'Machine C'],
      data: [[22, 25, 24, 21, 26, 23, 24], [20, 23, 22, 21, 24], [25, 23, 27, 26, 24, 25]], note: 's3-example2-note' }
  };
  function loadExample(key) {
    const ex = EXAMPLES[key];
    state.k = ex.data.length;
    for (let c = 0; c < MAXK; c++) {
      state.names[c] = ex.names[c] || DEFAULT_NAMES[c];
      state.sizes[c] = ex.data[c] ? ex.data[c].length : 10;
      for (let r = 0; r < MAXN; r++) state.values[c][r] = ex.data[c] && r < ex.data[c].length ? String(ex.data[c][r]) : '';
    }
    ['s3-example-note', 's3-example2-note'].forEach((id) => { $(id).hidden = id !== ex.note; });
    typeset($(ex.note));
    syncControls(); buildSizes(); buildGrid(); changed();
  }
  $('s3-example').addEventListener('click', () => loadExample('corr'));
  $('s3-example2').addEventListener('click', () => loadExample('machines'));
  $('s3-clear').addEventListener('click', () => {
    for (let c = 0; c < MAXK; c++) state.values[c].fill('');
    $('s3-example-note').hidden = true; $('s3-example2-note').hidden = true;
    buildGrid(); changed();
  });
  $('s3-remember').addEventListener('change', () => {
    if ($('s3-remember').checked) save();
    else { try { localStorage.removeItem(STORE); } catch (e) { /* nothing kept */ } }
  });
  /* A pasted block: each column's size is the position of its last value, so
     columns of different lengths give an unbalanced design. */
  $('s3-paste-go').addEventListener('click', () => {
    const lines = splitLines($('s3-paste-text').value);
    if (!lines.length) { flash = 'Nothing to paste.'; status(); return; }
    let header = null;
    if (lines[0].some((v) => v !== '' && Number.isNaN(parseNum(v)))) header = lines.shift();
    const width = Math.max.apply(null, lines.map((l) => l.length).concat(header ? [header.length] : [0]));
    if (width > MAXK) flash = 'At most ' + MAXK + ' columns: the first ' + MAXK + ' are used.';
    if (lines.length > MAXN) flash = 'At most ' + MAXN + ' rows: only the first ' + MAXN + ' are used.';
    const k = Math.min(MAXK, Math.max(1, width)), body = lines.slice(0, MAXN), sz = [];
    for (let c = 0; c < k; c++) {
      let last = -1;
      body.forEach((l, r) => { if (l[c] !== undefined && l[c] !== '') last = r; });
      sz.push(last + 1);
    }
    if (sz.some((v) => v < 2)) { flash = 'Each column needs at least two values.'; status(); return; }
    state.k = k;
    for (let c = 0; c < MAXK; c++) {
      if (c < k) state.sizes[c] = sz[c];
      for (let r = 0; r < MAXN; r++) state.values[c][r] = c < k && body[r] && body[r][c] !== undefined ? body[r][c] : '';
      state.names[c] = header && header[c] ? header[c].slice(0, 20) : (c < k && header ? DEFAULT_NAMES[c] : state.names[c]);
    }
    $('s3-example-note').hidden = true; $('s3-example2-note').hidden = true;
    syncControls(); buildSizes(); buildGrid(); changed();
    $('s3-paste-text').closest('details').open = false;
  });

  /* ---------------------------------------------------------------- tabs */
  const PANELS = ['data', 'descriptive', 'inferential', 'distributions'];
  const tabs = page.querySelector('.s3-tabs');
  tabs.hidden = false;
  function show(id, scroll) {
    if (PANELS.indexOf(id) < 0) id = 'data';
    PANELS.forEach((p) => {
      $(p).hidden = p !== id;
      const tab = $('tab-' + p);
      tab.setAttribute('aria-selected', p === id ? 'true' : 'false');
    });
    if (id === 'descriptive') renderDescriptive();
    if (id === 'inferential') renderTestForm();
    if (id === 'distributions') renderDistForm();
    if (scroll) tabs.scrollIntoView({ block: 'start' });
  }
  window.addEventListener('hashchange', () => show(location.hash.slice(1), true));
  page.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute('href').slice(1);
    if (PANELS.indexOf(id) < 0) return;
    e.preventDefault();
    if (location.hash !== '#' + id) history.pushState(null, '', '#' + id);
    show(id, true);
  });
  function clearOutputs() {
    ['s3-test-out', 's3-dist-out', 's3-spec-out'].forEach((id) => { $(id).innerHTML = ''; });
    if (!$('descriptive').hidden) renderDescriptive();
  }

  /* ---------------------------------------------------------------- SVG helpers */
  const NS = 'http://www.w3.org/2000/svg';
  function niceTicks(lo, hi, count) {
    if (!(hi > lo)) { hi = lo + 1; lo = lo - 1; }
    const step = S.niceStep((hi - lo) / (count || 5));
    const out = [];
    for (let v = Math.ceil(lo / step - 1e-9) * step; v <= hi + step * 1e-9; v += step) out.push(+v.toPrecision(12));
    return out;
  }
  function tickText(v) { return (+v.toPrecision(6)).toString().replace('-', '\u2212'); }
  function chart(w, h, label) {
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', label);
    return svg;
  }
  function el(svg, tag, attrs, text) {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    if (text !== undefined) e.textContent = text;
    svg.appendChild(e);
    return e;
  }
  /* Axes with ticks; returns the two scale functions. */
  function axes(svg, box, xr, yr, xLabel, yLabel, opt) {
    opt = opt || {};
    const [x0, y0, x1, y1] = box;
    const sx = (v) => x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0);
    const sy = (v) => y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0);
    (opt.noY ? [] : niceTicks(yr[0], yr[1], 5)).forEach((v) => {
      if (v < yr[0] - 1e-12 || v > yr[1] + 1e-12) return;
      if (opt.yInt && v !== Math.round(v)) return;
      el(svg, 'line', { x1: x0, x2: x1, y1: sy(v), y2: sy(v), class: 's3-gridline' });
      el(svg, 'text', { x: x0 - 6, y: sy(v) + 4, 'text-anchor': 'end' }, tickText(v));
    });
    niceTicks(xr[0], xr[1], Math.max(3, Math.round((x1 - x0) / 110))).forEach((v) => {
      if (v < xr[0] - 1e-12 || v > xr[1] + 1e-12) return;
      el(svg, 'line', { x1: sx(v), x2: sx(v), y1: y1, y2: y1 + 5, class: 's3-axis' });
      el(svg, 'text', { x: sx(v), y: y1 + 18, 'text-anchor': 'middle' }, tickText(v));
    });
    el(svg, 'line', { x1: x0, x2: x1, y1: y1, y2: y1, class: 's3-axis' });
    if (!opt.noY) el(svg, 'line', { x1: x0, x2: x0, y1: y0, y2: y1, class: 's3-axis' });
    if (xLabel) el(svg, 'text', { x: (x0 + x1) / 2, y: y1 + 36, 'text-anchor': 'middle' }, xLabel);
    if (yLabel) el(svg, 'text', { x: 14, y: (y0 + y1) / 2, 'text-anchor': 'middle', transform: 'rotate(-90 14 ' + (y0 + y1) / 2 + ')' }, yLabel);
    return [sx, sy];
  }
  function figure(svg, caption) {
    const fig = document.createElement('figure');
    fig.className = 's3-chart';
    fig.appendChild(svg);
    if (caption) { const fc = document.createElement('figcaption'); fc.innerHTML = caption; fig.appendChild(fc); }
    return fig;
  }
  /* Fitted-curve styles: colour and dash differ, so they read without colour too. */
  const CURVE_CLASSES = ['s3-ov0', 's3-ov1', 's3-ov2', 's3-ov3'];
  /* Chart width in SVG units: the column's own width, so text stays legible on a phone. */
  function chartWidth() { return Math.round(Math.min(720, Math.max(330, ((page.clientWidth || 720) - 40)))); }
  function colorVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || '#0f6cbd'; }

  /* Histogram (classes or, for whole numbers with few values, one bar per
     value) with optional fitted curves drawn over it as expected frequencies. */
  function histogram(x, overlays, title, byValue) {
    const W = chartWidth(), H = Math.round(W * 0.46) + 40, box = [56, 16, W - 16, H - 52];
    const svg = chart(W, H, title);
    const d = S.describe(x), allInt = byValue && x.every((v) => Number.isInteger(v)) && d.max - d.min <= 40;
    let bars, xr, width;
    if (allInt) {
      bars = [];
      for (let v = d.min; v <= d.max; v++) bars.push({ lo: v - 0.5, hi: v + 0.5, f: x.filter((u) => u === v).length });
      xr = [d.min - 0.5, d.max + 0.5]; width = 1;
    } else {
      const ft = S.freqTable(x);
      bars = ft.classes; width = ft.width;
      xr = [bars[0].lo, bars[bars.length - 1].hi];
    }
    let ymax = Math.max.apply(null, bars.map((b) => b.f));
    const curves = (overlays || []).map((o) => {
      const pts = [];
      if (o.discrete) {
        for (let v = Math.ceil(xr[0]); v <= Math.floor(xr[1]); v++) pts.push([v, x.length * o.density(v)]);
      } else {
        for (let i = 0; i <= 200; i++) {
          const v = xr[0] + (xr[1] - xr[0]) * i / 200;
          const y = x.length * width * o.density(v);
          pts.push([v, isFinite(y) ? y : NaN]);
        }
      }
      pts.forEach((p) => { if (isFinite(p[1])) ymax = Math.max(ymax, Math.min(p[1], ymax * 3)); });
      return { o, pts };
    });
    const [sx, sy] = axes(svg, box, xr, [0, ymax * 1.08], 'value', 'frequency', { yInt: true });
    bars.forEach((b) => {
      if (!b.f) return;
      el(svg, 'rect', { x: sx(b.lo), y: sy(b.f), width: Math.max(0, sx(b.hi) - sx(b.lo)), height: Math.max(0, sy(0) - sy(b.f)), class: 's3-barrect' });
    });
    curves.forEach((c, i) => {
      const cls = CURVE_CLASSES[i % CURVE_CLASSES.length];
      const ok = c.pts.filter((p) => isFinite(p[1])).map((p) => [sx(p[0]), sy(Math.min(p[1], ymax * 1.08))]);
      el(svg, 'polyline', { points: ok.map((p) => p.join(',')).join(' '), class: cls + ' s3-ovline' + (c.o.discrete ? ' s3-ovthin' : '') });
      if (c.o.discrete) ok.forEach((p) => el(svg, 'circle', { cx: p[0], cy: p[1], r: 3.5, class: cls + ' s3-ovdot' }));
    });
    return svg;
  }
  function legend(items) {
    const div = document.createElement('div');
    div.className = 's3-legend';
    div.innerHTML = items.map((s, i) => '<span><svg width="26" height="10" aria-hidden="true"><line x1="1" y1="5" x2="25" y2="5" class="' + CURVE_CLASSES[i % 4] + ' s3-ovline"/></svg> ' + esc(s) + '</span>').join('');
    return div;
  }

  function boxPlots(cols, nm) {
    const W = chartWidth(), rowH = 54, H = 40 + rowH * cols.length + 30;
    const svg = chart(W, H, 'Box plots');
    const all = [].concat.apply([], cols);
    const lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), pad = (hi - lo) * 0.04 || 1;
    const box = [90, 10, W - 16, H - 40];
    const [sx] = axes(svg, box, [lo - pad, hi + pad], [0, 1], 'value', '', { noY: true });
    cols.forEach((x, i) => {
      if (x.length < 2) return;
      const d = S.describe(x), yc = 34 + i * rowH, cls = 's3-box' + i;
      const lf = d.q1 - 1.5 * d.iqr, uf = d.q3 + 1.5 * d.iqr;
      const inside = d.sorted.filter((v) => v >= lf && v <= uf);
      const wl = inside[0], wh = inside[inside.length - 1];
      el(svg, 'text', { x: 82, y: yc + 4, 'text-anchor': 'end' }, nm[i]);
      el(svg, 'line', { x1: sx(wl), x2: sx(d.q1), y1: yc, y2: yc, class: 's3-axis' });
      el(svg, 'line', { x1: sx(d.q3), x2: sx(wh), y1: yc, y2: yc, class: 's3-axis' });
      el(svg, 'line', { x1: sx(wl), x2: sx(wl), y1: yc - 9, y2: yc + 9, class: 's3-axis' });
      el(svg, 'line', { x1: sx(wh), x2: sx(wh), y1: yc - 9, y2: yc + 9, class: 's3-axis' });
      el(svg, 'rect', { x: sx(d.q1), y: yc - 15, width: Math.max(1, sx(d.q3) - sx(d.q1)), height: 30, class: cls });
      el(svg, 'line', { x1: sx(d.median), x2: sx(d.median), y1: yc - 15, y2: yc + 15, class: cls, 'stroke-width': 3 });
      el(svg, 'circle', { cx: sx(d.mean), cy: yc, r: 3.5, class: 's3-c' + i });
      d.sorted.filter((v) => v < lf || v > uf).forEach((v) => el(svg, 'circle', { cx: sx(v), cy: yc, r: 3.5, fill: 'none', class: cls }));
    });
    return svg;
  }

  function scatter(x, y, nx, ny, lines) {
    const W = chartWidth(), H = Math.round(W * 0.55) + 40, box = [60, 16, W - 16, H - 52];
    const svg = chart(W, H, 'Scatter diagram of ' + ny + ' against ' + nx);
    const px = (Math.max.apply(null, x) - Math.min.apply(null, x)) * 0.06 || 1;
    const py = (Math.max.apply(null, y) - Math.min.apply(null, y)) * 0.06 || 1;
    const xr = [Math.min.apply(null, x) - px, Math.max.apply(null, x) + px];
    const yr = [Math.min.apply(null, y) - py, Math.max.apply(null, y) + py];
    const [sx, sy] = axes(svg, box, xr, yr, nx, ny);
    if (lines) {
      const clipY = (v) => Math.max(yr[0], Math.min(yr[1], v));
      // Y on X: y = a + b x
      el(svg, 'line', { x1: sx(xr[0]), y1: sy(clipY(lines.ayx + lines.byx * xr[0])), x2: sx(xr[1]), y2: sy(clipY(lines.ayx + lines.byx * xr[1])), class: 's3-line0' });
      // X on Y: x = a + b y, drawn as y from x
      if (lines.bxy !== 0) {
        const yAt = (xv) => (xv - lines.axy) / lines.bxy;
        el(svg, 'line', { x1: sx(xr[0]), y1: sy(clipY(yAt(xr[0]))), x2: sx(xr[1]), y2: sy(clipY(yAt(xr[1]))), class: 's3-line1' });
      }
    }
    for (let i = 0; i < x.length; i++) el(svg, 'circle', { cx: sx(x[i]), cy: sy(y[i]), r: 4.5, class: 's3-c0 s3-pt' });
    return svg;
  }

  /* ---------------------------------------------------------------- 3-D scatter */
  function plot3d(container, pts, nm, plane) {
    const wrap = document.createElement('div');
    wrap.className = 's3-3d';
    const canvas = document.createElement('canvas');
    canvas.tabIndex = 0;
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', '3-D scatter plot of ' + pts.length + ' points: ' + nm.join(', ') +
      '. Drag, swipe or use the arrow keys to turn it.');
    wrap.appendChild(canvas);
    container.appendChild(wrap);
    const ranges = [0, 1, 2].map((a) => {
      const v = pts.map((p) => p[a]);
      let lo = Math.min.apply(null, v), hi = Math.max.apply(null, v);
      if (hi === lo) { lo -= 1; hi += 1; }
      return [lo, hi];
    });
    const norm = (p) => p.map((v, a) => 2 * (v - ranges[a][0]) / (ranges[a][1] - ranges[a][0]) - 1);
    let yaw = -0.7, pitch = 0.45;
    function project(q, w, h) {
      // axes: 0 to the right, 1 into the screen, 2 (the dependent variable) up
      const cy = Math.cos(yaw), syw = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
      const x = q[0] * cy - q[1] * syw, yd = q[0] * syw + q[1] * cy;
      const y = q[2] * cp - yd * sp, depth = q[2] * sp + yd * cp;
      const s = Math.min(w, h) * 0.27;
      return [w / 2 + x * s, h / 2 - y * s, depth];
    }
    function draw() {
      const dpr = window.devicePixelRatio || 1, w = wrap.clientWidth || 600, h = Math.min(560, Math.round(w * 0.8));
      canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
      canvas.style.height = h + 'px';
      const g = canvas.getContext('2d');
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
      g.clearRect(0, 0, w, h);
      const ink = colorVar('--s3-soft'), grid = colorVar('--s3-line'), pt = colorVar('--s3-c0'), cv = colorVar('--s3-curve'), txt = colorVar('--s3-ink');
      const corners = [];
      for (let i = 0; i < 8; i++) corners.push([(i & 1) ? 1 : -1, (i & 2) ? 1 : -1, (i & 4) ? 1 : -1]);
      g.lineWidth = 1; g.strokeStyle = grid;
      for (let i = 0; i < 8; i++) for (let j = i + 1; j < 8; j++) {
        const diff = (i ^ j);
        if (diff === 1 || diff === 2 || diff === 4) {
          const a = project(corners[i], w, h), b = project(corners[j], w, h);
          g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.stroke();
        }
      }
      // the three labelled axes, along the edges through (-1, -1, -1)
      g.strokeStyle = ink; g.lineWidth = 1.6; g.fillStyle = txt; g.font = '13px system-ui, sans-serif';
      for (let a = 0; a < 3; a++) {
        const p0 = [-1, -1, -1], p1 = [-1, -1, -1];
        p1[a] = 1;
        const A = project(p0, w, h), B = project(p1, w, h);
        g.beginPath(); g.moveTo(A[0], A[1]); g.lineTo(B[0], B[1]); g.stroke();
        // the axis is named past its far end, with its range, so the three
        // axes' labels never meet at the shared corner
        const lab = p1.slice(); lab[a] = 1.3;
        const L = project(lab, w, h);
        g.textAlign = 'center';
        g.fillText(nm[a], L[0], L[1]);
        g.font = '11px system-ui, sans-serif';
        g.fillText(tickText(ranges[a][0]) + ' to ' + tickText(ranges[a][1]), L[0], L[1] + 14);
        g.font = '13px system-ui, sans-serif';
      }
      if (plane) {
        g.strokeStyle = cv; g.globalAlpha = 0.55; g.lineWidth = 1;
        const N = 8;
        for (let dir = 0; dir < 2; dir++) {
          for (let i = 0; i <= N; i++) {
            g.beginPath();
            let started = false;
            for (let j = 0; j <= 40; j++) {
              const u = -1 + 2 * i / N, v = -1 + 2 * j / 40;
              const nx = dir ? u : v, ny = dir ? v : u;
              const X = ranges[0][0] + (nx + 1) / 2 * (ranges[0][1] - ranges[0][0]);
              const Y = ranges[1][0] + (ny + 1) / 2 * (ranges[1][1] - ranges[1][0]);
              const Z = plane[0] + plane[1] * X + plane[2] * Y;
              const nz = 2 * (Z - ranges[2][0]) / (ranges[2][1] - ranges[2][0]) - 1;
              if (nz < -1.001 || nz > 1.001) { started = false; continue; }
              const P = project([nx, ny, nz], w, h);
              if (!started) { g.moveTo(P[0], P[1]); started = true; } else g.lineTo(P[0], P[1]);
            }
            g.stroke();
          }
        }
        g.globalAlpha = 1;
      }
      const proj = pts.map((p) => project(norm(p), w, h)).sort((a, b) => a[2] - b[2]);
      const dmin = -2, dmax = 2;
      proj.forEach((P) => {
        const near = (P[2] - dmin) / (dmax - dmin);
        g.globalAlpha = 0.45 + 0.55 * near;
        g.fillStyle = pt;
        g.beginPath(); g.arc(P[0], P[1], 3.2 + 2.6 * near, 0, 2 * Math.PI); g.fill();
      });
      g.globalAlpha = 1;
    }
    let drag = null;
    canvas.addEventListener('pointerdown', (e) => { drag = [e.clientX, e.clientY]; canvas.setPointerCapture(e.pointerId); });
    canvas.addEventListener('pointermove', (e) => {
      if (!drag) return;
      yaw += (e.clientX - drag[0]) * 0.01;
      pitch = Math.max(-1.45, Math.min(1.45, pitch + (e.clientY - drag[1]) * 0.01));
      drag = [e.clientX, e.clientY];
      draw();
    });
    const stop = () => { drag = null; };
    canvas.addEventListener('pointerup', stop);
    canvas.addEventListener('pointercancel', stop);
    canvas.addEventListener('keydown', (e) => {
      const k = { ArrowLeft: [-0.12, 0], ArrowRight: [0.12, 0], ArrowUp: [0, -0.12], ArrowDown: [0, 0.12] }[e.key];
      if (!k) return;
      e.preventDefault();
      yaw += k[0]; pitch = Math.max(-1.45, Math.min(1.45, pitch + k[1]));
      draw();
    });
    const reset = document.createElement('button');
    reset.type = 'button'; reset.className = 's3-quiet'; reset.textContent = 'Reset the view';
    reset.addEventListener('click', () => { yaw = -0.7; pitch = 0.45; draw(); });
    container.appendChild(reset);
    if (window.ResizeObserver) new ResizeObserver(() => draw()).observe(wrap);
    if (window.matchMedia) {
      const mq = window.matchMedia('(prefers-color-scheme: dark)');
      if (mq.addEventListener) mq.addEventListener('change', draw);
    }
    requestAnimationFrame(draw);
    return { draw };
  }

  /* ---------------------------------------------------------------- 2. descriptive */
  function needData(out, what) {
    out.innerHTML = '<p class="s3-note">' + what + ' <a href="#data">Enter data</a>.</p>';
  }

  function renderDescriptive() {
    const out = $('s3-desc');
    const data = readData(), nm = names();
    if (data.errors.length) { needData(out, 'Some cells are empty or not numbers (' + esc(data.errors[0]) + ') Fill them first.'); return; }
    const vars = data.cols.map((c, i) => ({ i, x: c })).filter((v) => v.x.length >= 2);
    if (!vars.length) { needData(out, 'Each variable needs at least two values.'); return; }
    const D = vars.map((v) => S.describe(v.x));
    const rows = [
      ['Number of observations, \\(n\\)', (d) => d.n, null, 0],
      ['Sum, \\(\\sum x\\)', (d) => d.sum, 'mean'],
      ['Arithmetic mean, \\(\\bar x\\)', (d) => d.mean, 'mean'],
      ['Median', (d) => d.median, 'median'],
      ['Mode', (d) => (d.modes.length ? d.modes.map((m) => f(m)).join(', ') + ' (' + d.modeCount + ' times)' : 'none: no value repeats'), 'mode', 'raw'],
      ['Geometric mean', (d) => d.gm, 'gm'],
      ['Harmonic mean', (d) => d.hm, 'hm'],
      ['Minimum', (d) => d.min, 'range'],
      ['Maximum', (d) => d.max, 'range'],
      ['Range', (d) => d.range, 'range'],
      ['Lower quartile, \\(Q_1\\)', (d) => d.q1, 'qd'],
      ['Upper quartile, \\(Q_3\\)', (d) => d.q3, 'qd'],
      ['Inter-quartile range, \\(Q_3 - Q_1\\)', (d) => d.iqr, 'qd'],
      ['Quartile deviation, \\((Q_3 - Q_1)/2\\)', (d) => d.qd, 'qd'],
      ['Coefficient of QD', (d) => d.coeffQD, 'qd'],
      ['Mean deviation about the mean', (d) => d.mdMean, 'md'],
      ['Mean deviation about the median', (d) => d.mdMedian, 'md'],
      ['Variance, \\(\\sigma^2\\) (divisor \\(n\\))', (d) => d.varN, 'sd'],
      ['Standard deviation, \\(\\sigma\\)', (d) => d.sdN, 'sd'],
      ['Sample variance, \\(s^2\\) (divisor \\(n-1\\))', (d) => d.var, 'sd'],
      ['Sample SD, \\(s\\)', (d) => d.sd, 'sd'],
      ['Standard error of the mean, \\(s/\\sqrt n\\)', (d) => d.se, 'sd'],
      ['Coefficient of variation, \\(100\\,\\sigma/\\bar x\\) (%)', (d) => d.cv, 'sd'],
      ['\\(\\mu_2\\)', (d) => d.mu2, 'moments'],
      ['\\(\\mu_3\\)', (d) => d.mu3, 'moments'],
      ['\\(\\mu_4\\)', (d) => d.mu4, 'moments'],
      ['\\(\\beta_1 = \\mu_3^2/\\mu_2^3\\)', (d) => d.beta1, 'skew'],
      ['\\(\\gamma_1 = \\mu_3/\\mu_2^{3/2}\\)', (d) => d.gamma1, 'skew'],
      ['\\(\\beta_2 = \\mu_4/\\mu_2^2\\)', (d) => d.beta2, 'kurt'],
      ['\\(\\gamma_2 = \\beta_2 - 3\\)', (d) => d.gamma2, 'kurt'],
      ["Karl Pearson's skewness, \\(3(\\bar x - \\text{Md})/\\sigma\\)", (d) => d.skPearson, 'skew'],
      ["Karl Pearson's skewness, \\((\\bar x - \\text{Mo})/\\sigma\\)", (d) => d.skPearsonMode, 'skew'],
      ["Bowley's skewness, \\((Q_3 + Q_1 - 2\\text{Md})/(Q_3 - Q_1)\\)", (d) => d.skBowley, 'skew']
    ];
    let h = '<h3 id="each-variable">Each variable</h3><div class="table-scroll"><table class="s3-table"><thead><tr><th>Measure</th>' +
      vars.map((v) => '<th>' + esc(nm[v.i]) + '</th>').join('') + '</tr></thead><tbody>';
    rows.forEach(([label, fn, key, mode]) => {
      const vals = D.map((d) => fn(d));
      if (vals.every((v) => v === undefined || (typeof v === 'number' && Number.isNaN(v)))) return;
      h += '<tr><td class="s3-l">' + (key ? '<a href="' + LEARN[key][0] + '">' + label + '</a>' : label) + '</td>' +
        vals.map((v) => '<td class="s3-num">' + (mode === 'raw' ? v : mode === 0 ? v : f(v)) + '</td>').join('') + '</tr>';
    });
    h += '</tbody></table></div>';
    h += '<p class="s3-small">Quartiles and the median by the \\((n+1)p\\) rule, interpolating between the two values around that position. '
      + 'A measure that cannot be found (a geometric mean of data with zero or negative values, a single mode when none or several repeat most often) is shown as &ndash;.</p>';
    h += '<ul class="s3-reading">' + vars.map((v, j) => '<li><strong>' + esc(nm[v.i]) + ':</strong> ' + reading(D[j]) + '</li>').join('') + '</ul>';
    h += vars.map((v, j) => workingDesc(nm[v.i], v.x, D[j])).join('');
    h += '<h3 id="frequency-table">Frequency table and histogram</h3><label>Variable <select id="s3-hist-var">' +
      vars.map((v) => '<option value="' + v.i + '">' + esc(nm[v.i]) + '</option>').join('') + '</select></label><div id="s3-hist"></div>';
    h += '<h3 id="box-plots">Box plots</h3><div id="s3-box"></div>' +
      '<p class="s3-small">Box from \\(Q_1\\) to \\(Q_3\\), the median as the thick line and the mean as the dot; whiskers reach the furthest values within 1.5 IQR of the box, and values beyond them are drawn as open circles. '
      + learn('graphs', 'Graphs of a frequency distribution') + '</p>';
    if (state.k >= 2) {
      h += '<h3 id="two-variables">Two variables</h3><label>Pair <select id="s3-pair">' + pairOptions() + '</select></label><div id="s3-pair-out"></div>';
    }
    if (state.k >= 3) {
      h += '<h3 id="correlation-matrix">Correlation matrix</h3><div id="s3-matrix"></div>';
      h += '<h3 id="three-variables">Three variables</h3><p>Choose the three variables for partial and multiple correlation, the plane of regression and the 3-D plot.</p>' +
        '<div class="s3-controls">' + [0, 1, 2].map((j) => '<label>Variable ' + (j + 1) + ' <select id="s3-tri-' + j + '">' +
          nm.slice(0, state.k).map((s, i) => '<option value="' + i + '"' + (i === j ? ' selected' : '') + '>' + esc(s) + '</option>').join('') + '</select></label>').join('') +
        '</div><div id="s3-three"></div>';
    }
    out.innerHTML = h;
    const drawHist = () => {
      const i = +$('s3-hist-var').value, x = data.cols[i], ft = S.freqTable(x);
      const div = $('s3-hist');
      let tb = '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Class</th><th>Mid-value</th><th>Frequency</th><th>Cumulative</th><th>Relative</th></tr></thead><tbody>';
      ft.classes.forEach((c, j) => {
        tb += '<tr><td class="s3-l">' + f(c.lo) + ' &ndash; ' + (j === ft.classes.length - 1 ? f(c.hi) + ' (inclusive)' : 'under ' + f(c.hi)) + '</td><td>' + f(c.mid) +
          '</td><td>' + c.f + '</td><td>' + c.cf + '</td><td>' + f(c.rel) + '</td></tr>';
      });
      tb += '</tbody></table></div><p class="s3-small">Sturges: \\(1 + 3.322\\log_{10} n = ' + t(1 + 3.322 * Math.log10(x.length), 2) +
        '\\), so about ' + ft.sturges + ' classes, with the width rounded up to a tidy ' + f(ft.width) + '. ' + learn('freq') + '</p>';
      div.innerHTML = tb;
      div.appendChild(figure(histogram(x, [], 'Histogram of ' + nm[i]), 'Histogram of ' + esc(nm[i]) + '.'));
      typeset(div);
    };
    $('s3-hist-var').addEventListener('change', drawHist);
    drawHist();
    $('s3-box').appendChild(figure(boxPlots(vars.map((v) => v.x), vars.map((v) => nm[v.i])), ''));
    if (state.k >= 2) {
      const drawPair = () => renderPair(data, $('s3-pair').value.split(',').map(Number));
      $('s3-pair').addEventListener('change', drawPair);
      drawPair();
    }
    if (state.k >= 3) {
      renderMatrix(data);
      const drawThree = () => renderThree(data, [0, 1, 2].map((j) => +$('s3-tri-' + j).value));
      [0, 1, 2].forEach((j) => $('s3-tri-' + j).addEventListener('change', drawThree));
      drawThree();
    }
    typeset(out);
  }

  function pairOptions() {
    const nm = names(), out = [];
    for (let i = 0; i < state.k; i++) for (let j = i + 1; j < state.k; j++) {
      out.push('<option value="' + i + ',' + j + '">' + esc(nm[i]) + ' and ' + esc(nm[j]) + '</option>');
    }
    return out.join('');
  }

  function reading(d) {
    const out = [];
    if (d.gamma1 !== undefined) {
      const g = d.gamma1;
      out.push(Math.abs(g) < 0.1 ? 'roughly symmetric (\\(\\gamma_1 = ' + t(g, 3) + '\\))'
        : (g > 0 ? 'positively skewed, with a longer tail to the right' : 'negatively skewed, with a longer tail to the left') + ' (\\(\\gamma_1 = ' + t(g, 3) + '\\))');
      const b = d.beta2;
      out.push(Math.abs(b - 3) < 0.1 ? 'about as peaked as the normal curve (mesokurtic, \\(\\beta_2 \\approx 3\\))'
        : b > 3 ? 'more peaked than the normal curve (leptokurtic, \\(\\beta_2 = ' + t(b, 3) + ' > 3\\))'
          : 'flatter than the normal curve (platykurtic, \\(\\beta_2 = ' + t(b, 3) + ' < 3\\))');
    }
    if (d.n < 8) out.push('with only ' + d.n + ' values, read the shape measures loosely');
    return out.join('; ') + '.';
  }

  function workingDesc(name, x, d) {
    const n = d.n, sx2 = x.reduce((a, v) => a + v * v, 0), T = (s) => '\\text{' + texText(s) + '}';
    let w = '<details class="s3-working"><summary>Show the working for ' + esc(name) + '</summary>';
    w += disp('\\sum x = ' + t(d.sum) + ',\\qquad \\sum x^2 = ' + t(sx2) + ',\\qquad n = ' + n);
    w += disp('\\bar x = \\frac{\\sum x}{n} = \\frac{' + t(d.sum) + '}{' + n + '} = ' + t(d.mean));
    w += disp('\\sigma^2 = \\frac{\\sum x^2}{n} - \\bar x^2 = \\frac{' + t(sx2) + '}{' + n + '} - ' + tp(d.mean) + '^2 = ' + t(d.varN) +
      ',\\qquad \\sigma = ' + t(d.sdN));
    w += disp('s^2 = \\frac{\\sum (x - \\bar x)^2}{n - 1} = \\frac{' + t(d.ss) + '}{' + (n - 1) + '} = ' + t(d.var) + ',\\qquad s = ' + t(d.sd));
    w += '<p>Arranged in order: ' + d.sorted.map((v) => f(v)).join(', ') + '.</p>';
    w += disp(T('Median') + ' = \\left(\\frac{n+1}{2}\\right)\\text{th value} = ' + t((n + 1) / 2, 2) + '\\text{th} = ' + t(d.median));
    w += disp('Q_1 = \\left(\\frac{n+1}{4}\\right)\\text{th} = ' + t((n + 1) / 4, 2) + '\\text{th} = ' + t(d.q1) + ',\\qquad Q_3 = \\left(\\frac{3(n+1)}{4}\\right)\\text{th} = ' + t(3 * (n + 1) / 4, 2) + '\\text{th} = ' + t(d.q3));
    if (d.mu2 > 0) {
      w += disp('\\mu_2 = ' + t(d.mu2) + ',\\quad \\mu_3 = ' + t(d.mu3) + ',\\quad \\mu_4 = ' + t(d.mu4));
      w += disp('\\beta_1 = \\frac{\\mu_3^2}{\\mu_2^3} = \\frac{' + tp(d.mu3) + '^2}{' + t(d.mu2) + '^3} = ' + t(d.beta1) +
        ',\\qquad \\beta_2 = \\frac{\\mu_4}{\\mu_2^2} = \\frac{' + t(d.mu4) + '}{' + t(d.mu2) + '^2} = ' + t(d.beta2));
    }
    return w + '</details>';
  }

  function renderMatrix(data) {
    const nm = names(), out = $('s3-matrix'), s = data.sizes;
    if (s.some((v) => v !== s[0])) { out.innerHTML = '<p class="s3-note">' + esc(equalSizes(s.map((_, i) => i))) + '</p>'; return; }
    let h = '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">r</th>' + data.cols.map((_, i) => '<th>' + esc(nm[i]) + '</th>').join('') + '</tr></thead><tbody>';
    data.cols.forEach((a, i) => {
      h += '<tr><th class="s3-l">' + esc(nm[i]) + '</th>' + data.cols.map((b, j) => '<td>' + (i === j ? '1' : f(S.bivariateNoRank(a, b))) + '</td>').join('') + '</tr>';
    });
    out.innerHTML = h + '</tbody></table></div><p class="s3-small">Karl Pearson\u2019s r for every pair, from the ' + s[0] + ' rows. ' + learn('pearson') + '</p>';
  }

  function renderPair(data, idx) {
    const nm = names(), out = $('s3-pair-out');
    if (data.sizes[idx[0]] !== data.sizes[idx[1]]) { out.innerHTML = '<p class="s3-note">' + esc(equalSizes(idx)) + '</p>'; return; }
    const [x, y] = paired(data, idx);
    if (x.length < 3) { out.innerHTML = '<p class="s3-note">At least three pairs are needed.</p>'; return; }
    const b = S.bivariate(x, y), nx = nm[idx[0]], ny = nm[idx[1]];
    const sxy = x.reduce((a, v, i) => a + v * y[i], 0), sx = S.sum(x), sy = S.sum(y);
    const sx2 = x.reduce((a, v) => a + v * v, 0), sy2 = y.reduce((a, v) => a + v * v, 0);
    let h = '<p>Using the ' + b.n + ' pairs of ' + esc(nx) + ' and ' + esc(ny) + '.</p>';
    h += '<div class="table-scroll"><table class="s3-table"><tbody>' +
      '<tr><td class="s3-l">Covariance, divisor \\(n\\)</td><td>' + f(b.covN) + '</td></tr>' +
      '<tr><td class="s3-l">Covariance, divisor \\(n-1\\)</td><td>' + f(b.cov) + '</td></tr>' +
      '<tr><td class="s3-l">' + learn('pearson', "Karl Pearson's \\(r\\)") + '</td><td>' + f(b.r) + '</td></tr>' +
      '<tr><td class="s3-l">Coefficient of determination \\(r^2\\)</td><td>' + f(b.r2) + '</td></tr>' +
      '<tr><td class="s3-l">' + learn('spearman', "Spearman's \\(\\rho\\)") + '</td><td>' + f(b.spearman) + '</td></tr>' +
      '</tbody></table></div>' +
      '<p>' + learn('regression', 'Regression of ' + ny + ' on ' + nx) + ': \\(' + tn(ny) + ' = ' + t(b.ayx) + (b.byx < 0 ? ' - ' : ' + ') + t(Math.abs(b.byx)) + '\\,' + tn(nx) + '\\)<br>' +
      learn('regression', 'Regression of ' + nx + ' on ' + ny) + ': \\(' + tn(nx) + ' = ' + t(b.axy) + (b.bxy < 0 ? ' - ' : ' + ') + t(Math.abs(b.bxy)) + '\\,' + tn(ny) + '\\)</p>';
    if (b.tieCF > 0) h += '<p class="s3-small">Some values are tied, so Spearman\u2019s \\(\\rho\\) uses the tie correction \\(\\sum (m^3 - m)/12 = ' + t(b.tieCF) + '\\). The Pearson correlation of the mid-ranks is ' + f(b.spearmanRanksR) + '.</p>';
    h += '<details class="s3-working"><summary>Show the working</summary>' +
      disp('n = ' + b.n + ',\\quad \\sum x = ' + t(sx) + ',\\quad \\sum y = ' + t(sy) + ',\\quad \\sum x^2 = ' + t(sx2) + ',\\quad \\sum y^2 = ' + t(sy2) + ',\\quad \\sum xy = ' + t(sxy)) +
      disp('r = \\frac{n\\sum xy - \\sum x\\sum y}{\\sqrt{n\\sum x^2 - (\\sum x)^2}\\,\\sqrt{n\\sum y^2 - (\\sum y)^2}} = \\frac{' + t(b.n * sxy - sx * sy) + '}{\\sqrt{' + t(b.n * sx2 - sx * sx) + '}\\,\\sqrt{' + t(b.n * sy2 - sy * sy) + '}} = ' + t(b.r)) +
      disp('b_{yx} = \\frac{\\operatorname{cov}(x, y)}{\\sigma_x^2} = ' + t(b.byx) + ',\\qquad b_{xy} = \\frac{\\operatorname{cov}(x, y)}{\\sigma_y^2} = ' + t(b.bxy) + ',\\qquad b_{yx}\\,b_{xy} = ' + t(b.byx * b.bxy) + ' = r^2') +
      disp('\\rho = 1 - \\frac{6\\left[\\sum d^2 + \\sum \\frac{m^3 - m}{12}\\right]}{n(n^2 - 1)} = 1 - \\frac{6(' + t(b.sumd2) + ' + ' + t(b.tieCF) + ')}{' + b.n + '(' + b.n + '^2 - 1)} = ' + t(b.spearman)) +
      '</details>';
    out.innerHTML = h;
    out.appendChild(figure(scatter(x, y, nx, ny, b), 'Scatter diagram with the regression of ' + esc(ny) + ' on ' + esc(nx) + ' (solid) and of ' + esc(nx) + ' on ' + esc(ny) + ' (dashed). They cross at the means.'));
    typeset(out);
  }

  function renderThree(data, idx) {
    const all = names(), out = $('s3-three'), nm = idx.map((i) => all[i]);
    if (new Set(idx).size < 3) { out.innerHTML = '<p class="s3-note">Choose three different variables.</p>'; return; }
    if (idx.some((i) => data.sizes[i] !== data.sizes[idx[0]])) { out.innerHTML = '<p class="s3-note">' + esc(equalSizes(idx)) + '</p>'; return; }
    const cols = paired(data, idx);
    if (cols[0].length < 4) { out.innerHTML = '<p class="s3-note">At least four observations of each are needed.</p>'; return; }
    const n = cols[0].length;
    let h = '<p>Using the ' + n + ' rows of the three variables. Variable 1 is ' + esc(nm[0]) + ', 2 is ' + esc(nm[1]) + ', 3 is ' + esc(nm[2]) + '.</p>';
    const t3 = S.trivariate(cols[0], cols[1], cols[2]);
    h += '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Correlation</th><th>' + esc(nm[0]) + '</th><th>' + esc(nm[1]) + '</th><th>' + esc(nm[2]) + '</th></tr></thead><tbody>' +
      '<tr><th class="s3-l">' + esc(nm[0]) + '</th><td>1</td><td>' + f(t3.r12) + '</td><td>' + f(t3.r13) + '</td></tr>' +
      '<tr><th class="s3-l">' + esc(nm[1]) + '</th><td>' + f(t3.r12) + '</td><td>1</td><td>' + f(t3.r23) + '</td></tr>' +
      '<tr><th class="s3-l">' + esc(nm[2]) + '</th><td>' + f(t3.r13) + '</td><td>' + f(t3.r23) + '</td><td>1</td></tr></tbody></table></div>';
    h += '<div class="table-scroll"><table class="s3-table"><tbody>' +
      '<tr><td class="s3-l">' + learn('partial', 'Partial') + ' \\(r_{12\\cdot 3}\\)</td><td>' + f(t3.r12_3) + '</td><td class="s3-sub s3-l">' + esc(nm[0]) + ' and ' + esc(nm[1]) + ', ' + esc(nm[2]) + ' held fixed</td></tr>' +
      '<tr><td class="s3-l">' + learn('partial', 'Partial') + ' \\(r_{13\\cdot 2}\\)</td><td>' + f(t3.r13_2) + '</td><td class="s3-sub s3-l">' + esc(nm[0]) + ' and ' + esc(nm[2]) + ', ' + esc(nm[1]) + ' held fixed</td></tr>' +
      '<tr><td class="s3-l">' + learn('partial', 'Partial') + ' \\(r_{23\\cdot 1}\\)</td><td>' + f(t3.r23_1) + '</td><td class="s3-sub s3-l">' + esc(nm[1]) + ' and ' + esc(nm[2]) + ', ' + esc(nm[0]) + ' held fixed</td></tr>' +
      '<tr><td class="s3-l">' + learn('multiple', 'Multiple') + ' \\(R_{1\\cdot 23}\\)</td><td>' + f(t3.R1_23) + '</td><td class="s3-sub s3-l">' + esc(nm[0]) + ' on ' + esc(nm[1]) + ' and ' + esc(nm[2]) + '</td></tr>' +
      '<tr><td class="s3-l">' + learn('multiple', 'Multiple') + ' \\(R_{2\\cdot 13}\\)</td><td>' + f(t3.R2_13) + '</td><td class="s3-sub s3-l">' + esc(nm[1]) + ' on ' + esc(nm[0]) + ' and ' + esc(nm[2]) + '</td></tr>' +
      '<tr><td class="s3-l">' + learn('multiple', 'Multiple') + ' \\(R_{3\\cdot 12}\\)</td><td>' + f(t3.R3_12) + '</td><td class="s3-sub s3-l">' + esc(nm[2]) + ' on ' + esc(nm[0]) + ' and ' + esc(nm[1]) + '</td></tr>' +
      '</tbody></table></div>';
    h += '<details class="s3-working"><summary>Show the working</summary>' +
      disp('r_{12\\cdot 3} = \\frac{r_{12} - r_{13}r_{23}}{\\sqrt{(1 - r_{13}^2)(1 - r_{23}^2)}} = \\frac{' + t(t3.r12) + ' - ' + tp(t3.r13) + '\\times' + tp(t3.r23) + '}{\\sqrt{(1 - ' + tp(t3.r13) + '^2)(1 - ' + tp(t3.r23) + '^2)}} = ' + t(t3.r12_3)) +
      disp('R_{1\\cdot 23} = \\sqrt{\\frac{r_{12}^2 + r_{13}^2 - 2r_{12}r_{13}r_{23}}{1 - r_{23}^2}} = ' + t(t3.R1_23)) + '</details>';
    h += '<h4 id="regression-plane">Plane of regression</h4><label>Dependent variable <select id="s3-plane-dep">' +
      [0, 1, 2].map((i) => '<option value="' + i + '">' + esc(nm[i]) + '</option>').join('') + '</select></label>' +
      '<label class="s3-check"><input type="checkbox" id="s3-plane-show" checked> Draw the fitted plane</label>' +
      '<div id="s3-plane-out"></div><div id="s3-3d-host"></div>' +
      '<p class="s3-small">Drag or swipe the plot to turn it; on a keyboard, focus it and use the arrow keys. The vertical axis is the dependent variable. ' + learn('plane') + '</p>';
    out.innerHTML = h;
    const drawPlane = () => {
      const dep = +$('s3-plane-dep').value, others = [0, 1, 2].filter((i) => i !== dep);
      const r = S.regress2(cols[dep], cols[others[0]], cols[others[1]]);
      const po = $('s3-plane-out'), host = $('s3-3d-host');
      if (!r) { po.innerHTML = '<p class="s3-note">The two explanatory variables are exactly collinear, so the plane is not determined.</p>'; host.innerHTML = ''; return; }
      po.innerHTML = '<p>' + tex(tn(nm[dep]) + ' = ' + t(r.b[0]) + sgn(r.b[1]) + t(Math.abs(r.b[1])) + '\\,' + tn(nm[others[0]]) + sgn(r.b[2]) + t(Math.abs(r.b[2])) + '\\,' + tn(nm[others[1]])) +
        ', with \\(R^2 = ' + t(r.r2) + '\\). The coefficients are the partial regression coefficients: each is the change in ' + esc(nm[dep]) + ' for a unit change in that variable with the other held fixed.</p>';
      host.innerHTML = '';
      const pts = cols[0].map((_, i) => [cols[others[0]][i], cols[others[1]][i], cols[dep][i]]);
      plot3d(host, pts, [nm[others[0]], nm[others[1]], nm[dep]], $('s3-plane-show').checked ? r.b : null);
      typeset(po);
    };
    $('s3-plane-dep').addEventListener('change', drawPlane);
    $('s3-plane-show').addEventListener('change', drawPlane);
    drawPlane();
  }
  function sgn(v) { return v < 0 ? ' - ' : ' + '; }

  /* ---------------------------------------------------------------- 3. inferential */
  const ALPHAS = ['0.10', '0.05', '0.01', '0.001'];
  const P = {
    v1: { label: 'Variable', kind: 'var', def: 0 },
    v2: { label: 'Second variable', kind: 'var', def: 1 },
    dep: { label: 'Dependent variable', kind: 'var', def: 0 },
    v3: { label: 'Held fixed', kind: 'var', def: 2 },
    e1: { label: 'Explanatory variable', kind: 'var', def: 1 },
    e2: { label: 'Second explanatory variable', kind: 'var', def: 2 },
    mu0: { label: 'Hypothesised mean \u03bc\u2080', kind: 'num', def: '' },
    sigma: { label: 'Known population SD \u03c3', kind: 'num', def: '' },
    sigma2: { label: 'Known SD of the second population', kind: 'num', def: '' },
    s0sq: { label: 'Hypothesised variance \u03c3\u2080\u00b2', kind: 'num', def: '' },
    d0: { label: 'Hypothesised difference (usually 0)', kind: 'num', def: '0' },
    rho0: { label: 'Hypothesised correlation \u03c1\u2080', kind: 'num', def: '0.5' },
    m0: { label: 'Hypothesised median', kind: 'num', def: '' }
  };
  const TESTS = [
    { g: 'Means and variances', id: 'z1', name: 'z test for one mean (\u03c3 known)', params: ['v1', 'mu0', 'sigma'], alt: true, need: 1 },
    { g: 'Means and variances', id: 't1', name: 't test for one mean, and its confidence interval', params: ['v1', 'mu0'], alt: true, need: 1 },
    { g: 'Means and variances', id: 'chiVar', name: '\u03c7\u00b2 test for one variance, and its confidence interval', params: ['v1', 's0sq'], alt: true, need: 1 },
    { g: 'Means and variances', id: 'z2', name: 'z test for two means (\u03c3\u2081, \u03c3\u2082 known)', params: ['v1', 'v2', 'sigma', 'sigma2', 'd0'], alt: true, need: 2 },
    { g: 'Means and variances', id: 't2pooled', name: 't test for two means (equal variances, pooled)', params: ['v1', 'v2', 'd0'], alt: true, need: 2 },
    { g: 'Means and variances', id: 't2welch', name: "Welch's t test for two means (unequal variances)", params: ['v1', 'v2', 'd0'], alt: true, need: 2 },
    { g: 'Means and variances', id: 'tpaired', name: 'Paired t test', params: ['v1', 'v2', 'd0'], alt: true, need: 2 },
    { g: 'Means and variances', id: 'fVar', name: 'F test for two variances, and the interval for their ratio', params: ['v1', 'v2'], alt: true, need: 2 },
    { g: 'Analysis of variance', id: 'anova', name: 'One-way ANOVA (each variable a group)', params: [], need: 2 },
    { g: 'Analysis of variance', id: 'bartlett', name: "Bartlett's test of equal variances", params: [], need: 2 },
    { g: 'Correlation and regression', id: 'rZero', name: 't test that the correlation is zero', params: ['v1', 'v2'], alt: true, need: 2 },
    { g: 'Correlation and regression', id: 'rFisher', name: "Fisher's z test of \u03c1 = \u03c1\u2080, and the interval for \u03c1", params: ['v1', 'v2', 'rho0'], alt: true, need: 2 },
    { g: 'Correlation and regression', id: 'partial', name: 'Test of a partial correlation', params: ['v1', 'v2', 'v3'], alt: true, need: 3 },
    { g: 'Correlation and regression', id: 'multiple', name: 'F test of a multiple correlation', params: ['dep', 'e1', 'e2'], need: 3 },
    { g: 'Correlation and regression', id: 'reg1', name: 'Simple regression: t tests, intervals, ANOVA', params: ['dep', 'e1'], need: 2 },
    { g: 'Correlation and regression', id: 'reg2', name: 'Regression on two variables: t tests, intervals, F test', params: ['dep', 'e1', 'e2'], need: 3 },
    { g: 'Non-parametric', id: 'sign1', name: 'Sign test for a median', params: ['v1', 'm0'], alt: true, need: 1 },
    { g: 'Non-parametric', id: 'sign2', name: 'Sign test for paired data', params: ['v1', 'v2'], alt: true, need: 2 },
    { g: 'Non-parametric', id: 'wil1', name: 'Wilcoxon signed-rank test for a median', params: ['v1', 'm0'], alt: true, need: 1 },
    { g: 'Non-parametric', id: 'wil2', name: 'Wilcoxon signed-rank test for paired data', params: ['v1', 'v2'], alt: true, need: 2 },
    { g: 'Non-parametric', id: 'mw', name: 'Mann\u2013Whitney U test (two independent samples)', params: ['v1', 'v2'], alt: true, need: 2 },
    { g: 'Non-parametric', id: 'kw', name: 'Kruskal\u2013Wallis H test (each variable a group)', params: [], need: 2 },
    { g: 'Non-parametric', id: 'runs', name: 'Runs test for randomness (in the order entered)', params: ['v1'], alt: true, need: 1 }
  ];

  let formBuilt = false;
  function renderTestForm() {
    const sel = $('s3-test');
    if (!formBuilt) {
      let h = '', g = '';
      TESTS.forEach((T) => {
        if (T.g !== g) { h += (g ? '</optgroup>' : '') + '<optgroup label="' + esc(T.g) + '">'; g = T.g; }
        h += '<option value="' + T.id + '">' + esc(T.name) + '</option>';
      });
      sel.innerHTML = h + '</optgroup>';
      sel.value = 't1';
      sel.addEventListener('change', buildParams);
      $('s3-test-go').addEventListener('click', runTest);
      formBuilt = true;
    }
    buildParams();
  }
  function buildParams() {
    const T = TESTS.find((x) => x.id === $('s3-test').value), box = $('s3-test-params'), nm = names();
    const old = {};
    box.querySelectorAll('[data-p]').forEach((e) => { old[e.dataset.p] = e.value; });
    let h = '';
    if (state.k < T.need) {
      h += '<p class="s3-note">This test needs ' + T.need + ' variables; ' + state.k + (state.k === 1 ? ' is' : ' are') + ' entered.</p>';
    }
    T.params.forEach((p) => {
      const d = P[p];
      if (d.kind === 'var') {
        const def = old[p] !== undefined ? old[p] : String(Math.min(d.def, state.k - 1));
        h += '<label>' + d.label + ' <select data-p="' + p + '">' +
          nm.slice(0, state.k).map((s, i) => '<option value="' + i + '"' + (String(i) === def ? ' selected' : '') + '>' + esc(s) + '</option>').join('') + '</select></label>';
      } else {
        h += '<label>' + d.label + ' <input type="text" inputmode="decimal" data-p="' + p + '" value="' + esc(old[p] !== undefined ? old[p] : d.def) + '"></label>';
      }
    });
    h += '<label>Level of significance \u03b1 <select data-p="alpha">' + ALPHAS.map((a) => '<option' + (a === (old.alpha || '0.05') ? ' selected' : '') + '>' + a + '</option>').join('') + '</select></label>';
    if (T.alt) {
      h += '<label>Alternative hypothesis <select data-p="alt">' +
        [['two', 'two-sided (\u2260)'], ['less', 'one-sided, less than (<)'], ['greater', 'one-sided, greater than (>)']]
          .map(([v, s]) => '<option value="' + v + '"' + (v === (old.alt || 'two') ? ' selected' : '') + '>' + s + '</option>').join('') + '</select></label>';
    }
    box.innerHTML = h;
  }

  function param(p) {
    const e = $('s3-test-params').querySelector('[data-p="' + p + '"]');
    return e ? e.value : undefined;
  }
  function numParam(p, label, check) {
    const v = parseNum(param(p));
    if (v === null || Number.isNaN(v)) throw new Error('Enter a number for \u201c' + label + '\u201d.');
    if (check && !check(v)) throw new Error('\u201c' + label + '\u201d is outside its range.');
    return v;
  }

  const ALTSYM = { two: '\\ne', less: '<', greater: '>' };
  const ALTWORD = { two: 'differs from', less: 'is less than', greater: 'is greater than' };
  function critTex(sym, alt, crit, symmetric) {
    if (alt === 'two') {
      if (symmetric) return '|' + sym + '| \\ge ' + t(crit[1], 4);
      return sym + ' \\le ' + t(crit[0], 4) + '\\ \\text{or}\\ ' + sym + ' \\ge ' + t(crit[1], 4);
    }
    return sym + (alt === 'less' ? ' \\le ' : ' \\ge ') + t(crit[0], 4);
  }
  function decisionHtml(r, alpha, ifReject, ifKeep) {
    const a = +alpha;
    if (r.p === null || Number.isNaN(r.p)) return '<div class="s3-decision s3-na">The test cannot be made for these data.</div>';
    const pctA = (+(a * 100).toPrecision(3)) + '%';
    return '<div class="s3-decision ' + (r.reject ? 's3-reject' : 's3-keep') + '">' +
      (r.reject ? 'Reject \\(H_0\\) at the ' + pctA + ' level: \\(' + pEq(r.p) + ' \\le ' + a + '\\).'
        : 'Do not reject \\(H_0\\) at the ' + pctA + ' level: \\(' + pEq(r.p) + ' > ' + a + '\\).') +
      '</div><p>' + (r.reject ? ifReject : ifKeep) + '</p>';
  }
  function card(title, learnKeys, body) {
    return '<div class="s3-card"><h3>' + title + '</h3>' + learnLine(learnKeys) + body + '</div>';
  }
  function table(rows) {
    return '<table class="s3-table s3-kv"><tbody>' +
      rows.map(([a, b]) => '<tr><td class="s3-l">' + a + '</td><td class="s3-l s3-num">' + b + '</td></tr>').join('') + '</tbody></table>';
  }
  /* An interval: the two limits first, then the formula that gave them. */
  function ciCell(formula, ci) {
    return tex('(' + t(ci[0]) + ',\\ ' + t(ci[1]) + ')') + (formula ? '<br><span class="s3-sub">' + tex(formula) + '</span>' : '');
  }
  const KEEP = 'The data are consistent with \\(H_0\\). That does not prove \\(H_0\\) true; a larger sample might detect a difference this one cannot.';

  function runTest() {
    const out = $('s3-test-out'), T = TESTS.find((x) => x.id === $('s3-test').value);
    const data = readData(), nm = names();
    try {
      if (data.errors.length) throw new Error('Some cells are empty or not numbers (' + data.errors[0] + ') Fill them on the Enter data tab.');
      if (state.k < T.need) throw new Error('This test needs ' + T.need + ' variables.');
      const alpha = +param('alpha'), alt = param('alt') || 'two';
      const num = (p, d) => (param(p) !== undefined ? +param(p) : d);
      const v1 = num('v1', 0), v2 = num('v2', 1), v3 = num('v3', 2), dep = num('dep', 0), e1 = num('e1', 1), e2 = num('e2', 2);
      const X = data.cols[v1], Y = data.cols[v2];
      const need = (arr, k, who) => { if (arr.length < k) throw new Error((who || 'Each variable') + ' needs at least ' + k + ' values.'); };
      const used = T.params.filter((p) => P[p].kind === 'var').map((p) => num(p, 0));
      if (new Set(used).size < used.length) throw new Error('Choose ' + (used.length === 2 ? 'two' : 'three') + ' different variables.');
      out.innerHTML = TESTRUN[T.id]({ data, nm, alpha, alt, v1, v2, v3, dep, e1, e2, X, Y, need });
    } catch (e) {
      out.innerHTML = '<p class="s3-note">' + esc(e.message) + '</p>';
    }
    typeset(out);
  }

  const TESTRUN = {
    z1(c) {
      c.need(c.X, 2);
      const mu0 = numParam('mu0', P.mu0.label), sg = numParam('sigma', P.sigma.label, (v) => v > 0);
      const r = S.z1(c.X, mu0, sg, c.alpha, c.alt), N = nameT(c.v1);
      return card('z test for the mean of ' + esc(c.nm[c.v1]), ['z1', 'ci'],
        '<p>\\(H_0: \\mu = ' + t(mu0) + '\\) against \\(H_1: \\mu ' + ALTSYM[c.alt] + ' ' + t(mu0) + '\\). The population SD is known, \\(\\sigma = ' + t(sg) + '\\); the sample is random, and the population normal or \\(n\\) large.</p>' +
        disp('z = \\frac{\\bar x - \\mu_0}{\\sigma/\\sqrt n} = \\frac{' + t(r.mean) + ' - ' + tp(mu0) + '}{' + t(sg) + '/\\sqrt{' + r.n + '}} = \\frac{' + t(r.mean - mu0) + '}{' + t(r.se) + '} = ' + t(r.stat)) +
        table([['\\(z\\)', f(r.stat)], ['p-value', pv(r.p)], ['Critical region', tex(critTex('z', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\mu\\)', ciCell('\\bar x \\pm z_{\\alpha/2}\\,\\sigma/\\sqrt n = ' + t(r.mean) + ' \\pm ' + t(r.zHalf) + '\\times' + t(r.se), r.ci)]]) +
        decisionHtml(r, c.alpha, 'The mean of ' + esc(c.nm[c.v1]) + ' ' + ALTWORD[c.alt] + ' ' + f(mu0) + '.', KEEP));
    },
    t1(c) {
      c.need(c.X, 2);
      const mu0 = numParam('mu0', P.mu0.label), r = S.t1(c.X, mu0, c.alpha, c.alt);
      return card('t test for the mean of ' + esc(c.nm[c.v1]), ['t1', 'ci'],
        '<p>\\(H_0: \\mu = ' + t(mu0) + '\\) against \\(H_1: \\mu ' + ALTSYM[c.alt] + ' ' + t(mu0) + '\\). Assumes a random sample from a normal population with unknown \\(\\sigma\\).</p>' +
        disp('t = \\frac{\\bar x - \\mu_0}{s/\\sqrt n} = \\frac{' + t(r.mean) + ' - ' + tp(mu0) + '}{' + t(r.s) + '/\\sqrt{' + r.n + '}} = \\frac{' + t(r.mean - mu0) + '}{' + t(r.se) + '} = ' + t(r.stat) + ',\\qquad \\nu = n - 1 = ' + r.df) +
        table([['\\(t\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical region', tex(critTex('t', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\mu\\)', ciCell('\\bar x \\pm t_{\\alpha/2,\\,' + r.df + '}\\,s/\\sqrt n = ' + t(r.mean) + ' \\pm ' + t(r.tHalf) + '\\times' + t(r.se), r.ci)]]) +
        decisionHtml(r, c.alpha, 'The mean of ' + esc(c.nm[c.v1]) + ' ' + ALTWORD[c.alt] + ' ' + f(mu0) + '.', KEEP));
    },
    chiVar(c) {
      c.need(c.X, 2);
      const s0 = numParam('s0sq', P.s0sq.label, (v) => v > 0), r = S.chiVar(c.X, s0, c.alpha, c.alt);
      return card('\u03c7\u00b2 test for the variance of ' + esc(c.nm[c.v1]), ['chiVar', 'ci'],
        '<p>\\(H_0: \\sigma^2 = ' + t(s0) + '\\) against \\(H_1: \\sigma^2 ' + ALTSYM[c.alt] + ' ' + t(s0) + '\\). Assumes a normal population; this test is sensitive to non-normality.</p>' +
        disp('\\chi^2 = \\frac{(n-1)s^2}{\\sigma_0^2} = \\frac{' + r.df + '\\times' + t(r.s2) + '}{' + t(s0) + '} = ' + t(r.stat) + ',\\qquad \\nu = ' + r.df) +
        table([['\\(\\chi^2\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical region', tex(critTex('\\chi^2', c.alt, r.crit, false))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\sigma^2\\)', ciCell('\\left(\\frac{(n-1)s^2}{' + t(r.chiHi) + '},\\ \\frac{(n-1)s^2}{' + t(r.chiLo) + '}\\right)', r.ci)]]) +
        decisionHtml(r, c.alpha, 'The variance of ' + esc(c.nm[c.v1]) + ' ' + ALTWORD[c.alt] + ' ' + f(s0) + '.', KEEP));
    },
    z2(c) {
      c.need(c.X, 2); c.need(c.Y, 2);
      const s1 = numParam('sigma', P.sigma.label, (v) => v > 0), s2 = numParam('sigma2', P.sigma2.label, (v) => v > 0), d0 = numParam('d0', P.d0.label);
      const r = S.z2(c.X, c.Y, s1, s2, d0, c.alpha, c.alt), a = esc(c.nm[c.v1]), b = esc(c.nm[c.v2]);
      return card('z test for the means of ' + a + ' and ' + b, ['z2', 'ci'],
        '<p>\\(H_0: \\mu_1 - \\mu_2 = ' + t(d0) + '\\) against \\(H_1: \\mu_1 - \\mu_2 ' + ALTSYM[c.alt] + ' ' + t(d0) + '\\), with \\(\\sigma_1 = ' + t(s1) + '\\), \\(\\sigma_2 = ' + t(s2) + '\\) known and independent samples.</p>' +
        disp('z = \\frac{\\bar x_1 - \\bar x_2 - ' + tp(d0) + '}{\\sqrt{\\sigma_1^2/n_1 + \\sigma_2^2/n_2}} = \\frac{' + t(r.m1) + ' - ' + tp(r.m2) + ' - ' + tp(d0) + '}{\\sqrt{' + t(s1 * s1) + '/' + r.n1 + ' + ' + t(s2 * s2) + '/' + r.n2 + '}} = ' + t(r.stat)) +
        table([['\\(z\\)', f(r.stat)], ['p-value', pv(r.p)], ['Critical region', tex(critTex('z', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\mu_1 - \\mu_2\\)', ciCell(null, r.ci)]]) +
        decisionHtml(r, c.alpha, 'The difference between the means ' + ALTWORD[c.alt] + ' ' + f(d0) + '.', KEEP));
    },
    t2pooled(c) {
      c.need(c.X, 2); c.need(c.Y, 2);
      const d0 = numParam('d0', P.d0.label), r = S.t2pooled(c.X, c.Y, d0, c.alpha, c.alt), a = esc(c.nm[c.v1]), b = esc(c.nm[c.v2]);
      return card('t test for the means of ' + a + ' and ' + b + ' (pooled variance)', ['t2', 'ci'],
        '<p>\\(H_0: \\mu_1 - \\mu_2 = ' + t(d0) + '\\) against \\(H_1: \\mu_1 - \\mu_2 ' + ALTSYM[c.alt] + ' ' + t(d0) + '\\). Assumes independent random samples from normal populations with equal variances (check with the F test).</p>' +
        disp('s_p^2 = \\frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2} = \\frac{' + (r.n1 - 1) + '\\times' + t(r.s1sq) + ' + ' + (r.n2 - 1) + '\\times' + t(r.s2sq) + '}{' + r.df + '} = ' + t(r.sp2)) +
        disp('t = \\frac{\\bar x_1 - \\bar x_2 - ' + tp(d0) + '}{s_p\\sqrt{1/n_1 + 1/n_2}} = \\frac{' + t(r.m1) + ' - ' + tp(r.m2) + ' - ' + tp(d0) + '}{' + t(r.se) + '} = ' + t(r.stat) + ',\\qquad \\nu = n_1 + n_2 - 2 = ' + r.df) +
        table([['\\(t\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical region', tex(critTex('t', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\mu_1 - \\mu_2\\)', ciCell(t(r.m1 - r.m2) + ' \\pm ' + t(r.tHalf) + '\\times' + t(r.se), r.ci)]]) +
        decisionHtml(r, c.alpha, 'The difference between the means ' + ALTWORD[c.alt] + ' ' + f(d0) + '.', KEEP));
    },
    t2welch(c) {
      c.need(c.X, 2); c.need(c.Y, 2);
      const d0 = numParam('d0', P.d0.label), r = S.t2welch(c.X, c.Y, d0, c.alpha, c.alt), a = esc(c.nm[c.v1]), b = esc(c.nm[c.v2]);
      return card("Welch's t test for the means of " + a + ' and ' + b, ['t2', 'ci'],
        '<p>\\(H_0: \\mu_1 - \\mu_2 = ' + t(d0) + '\\) against \\(H_1: \\mu_1 - \\mu_2 ' + ALTSYM[c.alt] + ' ' + t(d0) + '\\). Normal populations, variances not assumed equal.</p>' +
        disp('t = \\frac{\\bar x_1 - \\bar x_2 - ' + tp(d0) + '}{\\sqrt{s_1^2/n_1 + s_2^2/n_2}} = \\frac{' + t(r.m1 - r.m2 - d0) + '}{\\sqrt{' + t(r.s1sq) + '/' + r.n1 + ' + ' + t(r.s2sq) + '/' + r.n2 + '}} = ' + t(r.stat)) +
        disp('\\nu = \\frac{(s_1^2/n_1 + s_2^2/n_2)^2}{\\frac{(s_1^2/n_1)^2}{n_1 - 1} + \\frac{(s_2^2/n_2)^2}{n_2 - 1}} = ' + t(r.df, 3)) +
        table([['\\(t\\)', f(r.stat)], ['Degrees of freedom (Welch)', f(r.df, 3)], ['p-value', pv(r.p)], ['Critical region', tex(critTex('t', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\mu_1 - \\mu_2\\)', ciCell(null, r.ci)]]) +
        decisionHtml(r, c.alpha, 'The difference between the means ' + ALTWORD[c.alt] + ' ' + f(d0) + '.', KEEP));
    },
    tpaired(c) {
      const [x, y] = paired(c.data, [c.v1, c.v2]);
      c.need(x, 2, 'The paired test');
      const d0 = numParam('d0', P.d0.label), r = S.tpaired(x, y, d0, c.alpha, c.alt), a = esc(c.nm[c.v1]), b = esc(c.nm[c.v2]);
      return card('Paired t test: ' + a + ' minus ' + b, ['tp', 'ci'],
        '<p>Using the ' + r.n + ' pairs. \\(d = ' + tn(c.nm[c.v1]) + ' - ' + tn(c.nm[c.v2]) + '\\); \\(H_0: \\mu_d = ' + t(d0) + '\\) against \\(H_1: \\mu_d ' + ALTSYM[c.alt] + ' ' + t(d0) + '\\). Assumes the differences are normal.</p>' +
        '<p class="s3-small">Differences: ' + r.d.map((v) => f(v)).join(', ') + '.</p>' +
        disp('\\bar d = ' + t(r.mean) + ',\\quad s_d = ' + t(r.s) + ',\\qquad t = \\frac{\\bar d - ' + tp(d0) + '}{s_d/\\sqrt n} = \\frac{' + t(r.mean - d0) + '}{' + t(r.se) + '} = ' + t(r.stat) + ',\\qquad \\nu = ' + r.df) +
        table([['\\(t\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical region', tex(critTex('t', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\mu_d\\)', ciCell(null, r.ci)]]) +
        decisionHtml(r, c.alpha, 'The mean difference ' + ALTWORD[c.alt] + ' ' + f(d0) + '.', KEEP));
    },
    fVar(c) {
      c.need(c.X, 2); c.need(c.Y, 2);
      const r = S.fVar(c.X, c.Y, c.alpha, c.alt), a = esc(c.nm[c.v1]), b = esc(c.nm[c.v2]);
      return card('F test for the variances of ' + a + ' and ' + b, ['fVar', 'ci'],
        '<p>\\(H_0: \\sigma_1^2 = \\sigma_2^2\\) against \\(H_1: \\sigma_1^2 ' + ALTSYM[c.alt] + ' \\sigma_2^2\\). Assumes independent samples from normal populations. ' +
        'Here \\(F = s_1^2/s_2^2\\) with ' + a + ' on top; for a two-sided test the courses put the larger variance on top and use the upper tail, which gives the same decision.</p>' +
        disp('F = \\frac{s_1^2}{s_2^2} = \\frac{' + t(r.s1sq) + '}{' + t(r.s2sq) + '} = ' + t(r.stat) + ',\\qquad \\nu_1 = ' + r.df1 + ',\\ \\nu_2 = ' + r.df2) +
        table([['\\(F\\)', f(r.stat)], ['Degrees of freedom', r.df1 + ', ' + r.df2], ['p-value', pv(r.p)], ['Critical region', tex(critTex('F', c.alt, r.crit, false))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\sigma_1^2/\\sigma_2^2\\)', ciCell('\\left(\\frac{F}{' + t(r.fHi) + '},\\ \\frac{F}{' + t(r.fLo) + '}\\right)', r.ci)]]) +
        decisionHtml(r, c.alpha, 'The two population variances differ in the direction stated.', KEEP));
    },
    anova(c) {
      const idx = c.data.cols.map((x, i) => i).filter((i) => c.data.cols[i].length > 0);
      const groups = idx.map((i) => c.data.cols[i]);
      groups.forEach((g, j) => c.need(g, 2, c.nm[idx[j]]));
      const r = S.anova1(groups, c.alpha), all = [].concat.apply([], groups);
      const sx2 = all.reduce((a, v) => a + v * v, 0), G = S.sum(all);
      const rows = '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Source</th><th>SS</th><th>df</th><th>MS</th><th>F</th></tr></thead><tbody>' +
        '<tr><td class="s3-l">Between groups</td><td>' + f(r.ssb) + '</td><td>' + r.dfb + '</td><td>' + f(r.msb) + '</td><td>' + f(r.stat) + '</td></tr>' +
        '<tr><td class="s3-l">Within groups (error)</td><td>' + f(r.ssw) + '</td><td>' + r.dfw + '</td><td>' + f(r.msw) + '</td><td></td></tr>' +
        '<tr><td class="s3-l">Total</td><td>' + f(r.sst) + '</td><td>' + (r.N - 1) + '</td><td></td><td></td></tr></tbody></table></div>';
      const means = '<p>Group means: ' + r.groups.map((g, j) => esc(c.nm[idx[j]]) + ' ' + f(g.mean) + ' (n = ' + g.n + ')').join('; ') + '.</p>';
      const cd = '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Pair</th><th>|Difference of means|</th><th>Critical difference</th><th class="s3-l">Reading</th></tr></thead><tbody>' +
        r.pairs.map((p) => '<tr><td class="s3-l">' + esc(c.nm[idx[p.i]]) + ' &ndash; ' + esc(c.nm[idx[p.j]]) + '</td><td>' + f(p.diff) + '</td><td>' + f(p.cd) + '</td><td class="s3-l">' + (p.significant ? 'differ' : 'do not differ') + '</td></tr>').join('') + '</tbody></table></div>';
      return card('One-way analysis of variance', ['anova', 'cd'],
        '<p>\\(H_0\\): the ' + r.k + ' group means are equal, against \\(H_1\\): at least two differ. Assumes independent random samples from normal populations with a common variance.</p>' + means +
        disp('CF = \\frac{G^2}{N} = \\frac{' + t(G) + '^2}{' + r.N + '} = ' + t(r.cf) + ',\\qquad TSS = \\sum x^2 - CF = ' + t(sx2) + ' - ' + t(r.cf) + ' = ' + t(r.sst)) +
        disp('SSB = \\sum \\frac{T_i^2}{n_i} - CF = ' + t(r.ssb) + ',\\qquad SSE = TSS - SSB = ' + t(r.ssw)) +
        disp('F = \\frac{SSB/(k-1)}{SSE/(N-k)} = \\frac{' + t(r.msb) + '}{' + t(r.msw) + '} = ' + t(r.stat)) +
        rows + table([['p-value', pv(r.p)], ['Critical value \\(F_{' + c.alpha + '}(' + r.dfb + ', ' + r.dfw + ')\\)', f(r.crit[0])]]) +
        decisionHtml(r, c.alpha, 'At least two group means differ. The critical differences below show which pairs.', KEEP) +
        '<h4>Critical differences</h4><p>\\(CD = t_{\\alpha/2,\\,N-k}\\sqrt{MSE\\left(\\frac{1}{n_i} + \\frac{1}{n_j}\\right)}\\), with \\(t = ' + t(r.tHalf) + '\\). Read these only after a significant F.</p>' + cd);
    },
    bartlett(c) {
      const idx = c.data.cols.map((x, i) => i).filter((i) => c.data.cols[i].length > 0);
      const groups = idx.map((i) => c.data.cols[i]);
      groups.forEach((g, j) => c.need(g, 2, c.nm[idx[j]]));
      const r = S.bartlett(groups, c.alpha);
      return card("Bartlett's test of equal variances", ['bartlett'],
        '<p>\\(H_0\\): the ' + r.k + ' population variances are equal, against \\(H_1\\): they are not all equal. Assumes normal populations; it is the usual check before the ANOVA.</p>' +
        '<p>Variances: ' + idx.map((i, j) => esc(c.nm[i]) + ' ' + f(r.vars[j]) + ' (n = ' + r.ns[j] + ')').join('; ') + '; pooled \\(s_p^2 = ' + t(r.sp2) + '\\).</p>' +
        disp('\\chi^2 = \\frac{(N-k)\\ln s_p^2 - \\sum (n_i - 1)\\ln s_i^2}{1 + \\frac{1}{3(k-1)}\\left(\\sum \\frac{1}{n_i - 1} - \\frac{1}{N-k}\\right)} = \\frac{' + t(r.top) + '}{' + t(r.C) + '} = ' + t(r.stat) + ',\\qquad \\nu = ' + r.df) +
        table([['\\(\\chi^2\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical value', f(r.crit[0])]]) +
        decisionHtml(r, c.alpha, 'The variances are not all equal; the ANOVA\u2019s common-variance assumption is in doubt (Welch\u2019s test or Kruskal\u2013Wallis may suit better).', KEEP));
    },
    rZero(c) {
      const [x, y] = paired(c.data, [c.v1, c.v2]);
      c.need(x, 3, 'The test');
      const r = S.rZero(x, y, c.alpha, c.alt);
      if (Math.abs(r.r) >= 1) throw new Error('The correlation is exactly \u00b11, so the t statistic is infinite: the points lie on a line.');
      return card('t test of \u03c1 = 0 for ' + esc(c.nm[c.v1]) + ' and ' + esc(c.nm[c.v2]), ['rZero', 'pearson'],
        '<p>\\(H_0: \\rho = 0\\) against \\(H_1: \\rho ' + ALTSYM[c.alt] + ' 0\\), using the ' + r.n + ' paired observations. Assumes bivariate normal data.</p>' +
        disp('t = \\frac{r\\sqrt{n-2}}{\\sqrt{1 - r^2}} = \\frac{' + t(r.r) + '\\sqrt{' + r.df + '}}{\\sqrt{1 - ' + tp(r.r) + '^2}} = ' + t(r.stat) + ',\\qquad \\nu = n - 2 = ' + r.df) +
        table([['\\(r\\)', f(r.r)], ['\\(t\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical region', tex(critTex('t', c.alt, r.crit, true))]]) +
        decisionHtml(r, c.alpha, 'There is a correlation between them in the population (in the direction stated).', KEEP));
    },
    rFisher(c) {
      const [x, y] = paired(c.data, [c.v1, c.v2]);
      c.need(x, 4, 'The test');
      const rho0 = numParam('rho0', P.rho0.label, (v) => v > -1 && v < 1), r = S.rFisher(x, y, rho0, c.alpha, c.alt);
      if (Math.abs(r.r) >= 1) throw new Error('The correlation is exactly \u00b11, so z is infinite.');
      return card("Fisher's z test of \u03c1 = " + f(rho0), ['rFisher'],
        '<p>\\(H_0: \\rho = ' + t(rho0) + '\\) against \\(H_1: \\rho ' + ALTSYM[c.alt] + ' ' + t(rho0) + '\\), using the ' + r.n + ' paired observations; \\(r = ' + t(r.r) + '\\).</p>' +
        disp('Z = \\tfrac12\\ln\\frac{1 + r}{1 - r} = ' + t(r.z) + ',\\quad \\xi_0 = \\tfrac12\\ln\\frac{1 + \\rho_0}{1 - \\rho_0} = ' + t(r.z0) + ',\\qquad z = \\frac{Z - \\xi_0}{1/\\sqrt{n-3}} = ' + t(r.stat)) +
        table([['\\(z\\)', f(r.stat)], ['p-value', pv(r.p)], ['Critical region', tex(critTex('z', c.alt, r.crit, true))],
          [pct(1 - c.alpha) + ' confidence interval for \\(\\rho\\)', ciCell('\\tanh\\left(Z \\pm \\frac{' + t(r.zHalf) + '}{\\sqrt{' + (r.n - 3) + '}}\\right)', r.ci)]]) +
        decisionHtml(r, c.alpha, 'The population correlation ' + ALTWORD[c.alt] + ' ' + f(rho0) + '.', KEEP));
    },
    partial(c) {
      const third = c.v3;
      const [a, b, z] = paired(c.data, [c.v1, c.v2, third]);
      c.need(a, 5, 'The test');
      const r = S.partialTest(a, b, z, c.alpha, c.alt), A = esc(c.nm[c.v1]), B = esc(c.nm[c.v2]), Z = esc(c.nm[third]);
      return card('Partial correlation of ' + A + ' and ' + B + ', ' + Z + ' held fixed', ['partialTest', 'partial'],
        '<p>\\(H_0: \\rho_{12\\cdot 3} = 0\\) against \\(H_1: \\rho_{12\\cdot 3} ' + ALTSYM[c.alt] + ' 0\\), using the ' + r.n + ' paired observations. Assumes multivariate normal data.</p>' +
        disp('r_{12\\cdot 3} = \\frac{' + t(r.r12) + ' - ' + tp(r.r13) + '\\times' + tp(r.r23) + '}{\\sqrt{(1 - ' + tp(r.r13) + '^2)(1 - ' + tp(r.r23) + '^2)}} = ' + t(r.r) + ',\\qquad t = \\frac{r_{12\\cdot 3}\\sqrt{n-3}}{\\sqrt{1 - r_{12\\cdot 3}^2}} = ' + t(r.stat) + ',\\quad \\nu = ' + r.df) +
        table([['\\(r_{12\\cdot 3}\\)', f(r.r)], ['\\(t\\)', f(r.stat)], ['Degrees of freedom', r.df], ['p-value', pv(r.p)], ['Critical region', tex(critTex('t', c.alt, r.crit, true))]]) +
        decisionHtml(r, c.alpha, A + ' and ' + B + ' are related even with ' + Z + ' held fixed.', KEEP));
    },
    multiple(c) {
      const others = [c.e1, c.e2];
      const [y, a, b] = paired(c.data, [c.dep, others[0], others[1]]);
      c.need(y, 5, 'The test');
      const r = S.multipleTest(y, a, b, c.alpha);
      return card('Multiple correlation of ' + esc(c.nm[c.dep]) + ' on ' + esc(c.nm[others[0]]) + ' and ' + esc(c.nm[others[1]]), ['partialTest', 'multiple'],
        '<p>\\(H_0: \\rho_{1\\cdot 23} = 0\\) (neither explains ' + esc(c.nm[c.dep]) + ') against \\(H_1: \\rho_{1\\cdot 23} > 0\\), using the ' + r.n + ' paired observations.</p>' +
        disp('R_{1\\cdot 23} = ' + t(r.R) + ',\\qquad F = \\frac{R^2/2}{(1 - R^2)/(n-3)} = \\frac{' + t(r.R2) + '/2}{' + t(1 - r.R2) + '/' + r.df2 + '} = ' + t(r.stat) + ',\\quad \\nu = (2,\\ ' + r.df2 + ')') +
        table([['\\(R\\)', f(r.R)], ['\\(F\\)', f(r.stat)], ['Degrees of freedom', '2, ' + r.df2], ['p-value', pv(r.p)], ['Critical value', f(r.crit[0])]]) +
        decisionHtml(r, c.alpha, 'The two variables together explain part of the variation in ' + esc(c.nm[c.dep]) + '.', KEEP));
    },
    reg1(c) {
      const [y, x] = paired(c.data, [c.dep, c.e1]);
      c.need(y, 3, 'The regression');
      const r = S.regress1(y, x, c.alpha), Yn = tn(c.nm[c.dep]), Xn = tn(c.nm[c.e1]);
      const keep = { p: r.pF, reject: r.pF <= c.alpha };
      return card('Regression of ' + esc(c.nm[c.dep]) + ' on ' + esc(c.nm[c.e1]), ['regT', 'regF', 'regression'],
        '<p>Fitted line: ' + tex(Yn + ' = ' + t(r.a) + sgn(r.b) + t(Math.abs(r.b)) + '\\,' + Xn) + ', from the ' + r.n + ' paired observations; \\(r^2 = ' + t(r.r2) + '\\). Assumes independent normal errors with a common variance.</p>' +
        '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Coefficient</th><th>Estimate</th><th>SE</th><th>t</th><th>p</th><th>' + pct(1 - c.alpha) + ' interval</th></tr></thead><tbody>' +
        '<tr><td class="s3-l">Intercept \\(a\\)</td><td>' + f(r.a) + '</td><td>' + f(r.seA) + '</td><td>' + f(r.tA) + '</td><td>' + pv(r.pA) + '</td><td>(' + f(r.ciA[0]) + ', ' + f(r.ciA[1]) + ')</td></tr>' +
        '<tr><td class="s3-l">Slope \\(b\\)</td><td>' + f(r.b) + '</td><td>' + f(r.seB) + '</td><td>' + f(r.tB) + '</td><td>' + pv(r.pB) + '</td><td>(' + f(r.ciB[0]) + ', ' + f(r.ciB[1]) + ')</td></tr></tbody></table></div>' +
        disp('SE(b) = \\sqrt{\\frac{MSE}{S_{xx}}} = \\sqrt{\\frac{' + t(r.mse) + '}{' + t(r.sxx) + '}} = ' + t(r.seB) + ',\\qquad t = \\frac{b}{SE(b)} = ' + t(r.tB) + ',\\quad \\nu = n - 2 = ' + r.df) +
        '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Source</th><th>SS</th><th>df</th><th>MS</th><th>F</th></tr></thead><tbody>' +
        '<tr><td class="s3-l">Regression</td><td>' + f(r.ssr) + '</td><td>1</td><td>' + f(r.ssr) + '</td><td>' + f(r.F) + '</td></tr>' +
        '<tr><td class="s3-l">Residual</td><td>' + f(r.sse) + '</td><td>' + r.df + '</td><td>' + f(r.mse) + '</td><td></td></tr>' +
        '<tr><td class="s3-l">Total</td><td>' + f(r.sst) + '</td><td>' + (r.n - 1) + '</td><td></td><td></td></tr></tbody></table></div>' +
        '<p>\\(H_0: \\beta = 0\\) (no linear relation) against \\(H_1: \\beta \\ne 0\\): \\(F = ' + t(r.F) + ' = t^2\\), critical value ' + f(r.fCrit) + '.</p>' +
        decisionHtml(keep, c.alpha, esc(c.nm[c.dep]) + ' depends linearly on ' + esc(c.nm[c.e1]) + '.', KEEP));
    },
    reg2(c) {
      const others = [c.e1, c.e2];
      const [y, a, b] = paired(c.data, [c.dep, others[0], others[1]]);
      c.need(y, 4, 'The regression');
      const r = S.regress2(y, a, b, c.alpha);
      if (!r) throw new Error('The two explanatory variables are exactly collinear, so the regression is not determined.');
      const nmT = [tn(c.nm[c.dep]), tn(c.nm[others[0]]), tn(c.nm[others[1]])];
      const lab = ['Intercept \\(b_0\\)', esc(c.nm[others[0]]) + ' \\(b_1\\)', esc(c.nm[others[1]]) + ' \\(b_2\\)'];
      const keep = { p: r.pF, reject: r.pF <= c.alpha };
      return card('Regression of ' + esc(c.nm[c.dep]) + ' on ' + esc(c.nm[others[0]]) + ' and ' + esc(c.nm[others[1]]), ['regT', 'regF', 'plane'],
        '<p>Fitted plane: ' + tex(nmT[0] + ' = ' + t(r.b[0]) + sgn(r.b[1]) + t(Math.abs(r.b[1])) + '\\,' + nmT[1] + sgn(r.b[2]) + t(Math.abs(r.b[2])) + '\\,' + nmT[2]) + ', from the ' + r.n + ' paired observations; \\(R^2 = ' + t(r.r2) + '\\), adjusted \\(\\bar R^2 = ' + t(r.adjR2) + '\\).</p>' +
        '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Coefficient</th><th>Estimate</th><th>SE</th><th>t</th><th>p</th><th>' + pct(1 - c.alpha) + ' interval</th></tr></thead><tbody>' +
        r.b.map((v, j) => '<tr><td class="s3-l">' + lab[j] + '</td><td>' + f(v) + '</td><td>' + f(r.se[j]) + '</td><td>' + f(r.t[j]) + '</td><td>' + pv(r.p[j]) + '</td><td>(' + f(r.ci[j][0]) + ', ' + f(r.ci[j][1]) + ')</td></tr>').join('') +
        '</tbody></table></div><p>Each t test has \\(\\nu = n - 3 = ' + r.df + '\\) degrees of freedom.</p>' +
        '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Source</th><th>SS</th><th>df</th><th>MS</th><th>F</th></tr></thead><tbody>' +
        '<tr><td class="s3-l">Regression</td><td>' + f(r.ssr) + '</td><td>2</td><td>' + f(r.msr) + '</td><td>' + f(r.F) + '</td></tr>' +
        '<tr><td class="s3-l">Residual</td><td>' + f(r.sse) + '</td><td>' + r.df + '</td><td>' + f(r.mse) + '</td><td></td></tr>' +
        '<tr><td class="s3-l">Total</td><td>' + f(r.sst) + '</td><td>' + (r.n - 1) + '</td><td></td><td></td></tr></tbody></table></div>' +
        '<p>\\(H_0: \\beta_1 = \\beta_2 = 0\\) against \\(H_1\\): not both zero; critical value ' + f(r.fCrit) + '.</p>' +
        decisionHtml(keep, c.alpha, 'The two variables together explain part of the variation in ' + esc(c.nm[c.dep]) + '; the t tests show which one carries it.', KEEP));
    },
    sign1(c) {
      c.need(c.X, 2);
      const m0 = numParam('m0', P.m0.label), r = S.signTest(c.X, m0, c.alpha, c.alt);
      return card('Sign test for the median of ' + esc(c.nm[c.v1]), ['sign'],
        '<p>\\(H_0: M = ' + t(m0) + '\\) against \\(H_1: M ' + ALTSYM[c.alt] + ' ' + t(m0) + '\\). No assumption about the shape of the distribution.</p>' +
        '<p>Values above ' + f(m0) + ': ' + r.plus + '; below: ' + r.minus + '; equal (left out): ' + r.zeros + '. Under \\(H_0\\) the number above is \\(B(' + r.n + ', \\tfrac12)\\).</p>' +
        table([['Number of + signs', r.stat], ['Usable values \\(n\\)', r.n], ['p-value (' + r.method + ')', pv(r.p)]]) +
        decisionHtml(r, c.alpha, 'The median ' + ALTWORD[c.alt] + ' ' + f(m0) + '.', KEEP));
    },
    sign2(c) {
      const [x, y] = paired(c.data, [c.v1, c.v2]);
      c.need(x, 2, 'The test');
      const d = x.map((v, i) => v - y[i]), r = S.signTest(d, 0, c.alpha, c.alt);
      return card('Sign test for paired data: ' + esc(c.nm[c.v1]) + ' minus ' + esc(c.nm[c.v2]), ['sign'],
        '<p>\\(H_0\\): the median difference is 0, against \\(H_1\\): it ' + { two: 'is not 0', less: 'is negative', greater: 'is positive' }[c.alt] + '. Using the ' + x.length + ' paired observations.</p>' +
        '<p>Positive differences: ' + r.plus + '; negative: ' + r.minus + '; zero (left out): ' + r.zeros + '.</p>' +
        table([['Number of + signs', r.stat], ['Usable pairs \\(n\\)', r.n], ['p-value (' + r.method + ')', pv(r.p)]]) +
        decisionHtml(r, c.alpha, 'The paired values differ systematically (in the direction stated).', KEEP));
    },
    wil1(c) {
      c.need(c.X, 2);
      const m0 = numParam('m0', P.m0.label);
      return wilcoxonCard(c, S.wilcoxon(c.X, m0, c.alpha, c.alt), 'Wilcoxon signed-rank test for the median of ' + esc(c.nm[c.v1]),
        '\\(H_0: M = ' + t(m0) + '\\) against \\(H_1: M ' + ALTSYM[c.alt] + ' ' + t(m0) + '\\). Assumes a distribution symmetric about its median.', 'The median ' + ALTWORD[c.alt] + ' ' + f(m0) + '.');
    },
    wil2(c) {
      const [x, y] = paired(c.data, [c.v1, c.v2]);
      c.need(x, 2, 'The test');
      const d = x.map((v, i) => v - y[i]);
      return wilcoxonCard(c, S.wilcoxon(d, 0, c.alpha, c.alt), 'Wilcoxon signed-rank test: ' + esc(c.nm[c.v1]) + ' minus ' + esc(c.nm[c.v2]),
        '\\(H_0\\): the median difference is 0, against \\(H_1\\): it ' + { two: 'is not 0', less: 'is negative', greater: 'is positive' }[c.alt] + '. Using the ' + x.length + ' paired observations; the differences are assumed symmetric.', 'The paired values differ systematically (in the direction stated).');
    },
    mw(c) {
      c.need(c.X, 2); c.need(c.Y, 2);
      const r = S.mannWhitney(c.X, c.Y, c.alpha, c.alt), a = esc(c.nm[c.v1]), b = esc(c.nm[c.v2]);
      let w = disp('R_1 = ' + t(r.R1) + ',\\quad U_1 = R_1 - \\frac{n_1(n_1 + 1)}{2} = ' + t(r.R1) + ' - ' + (r.n1 * (r.n1 + 1) / 2) + ' = ' + t(r.U1) + ',\\quad U_2 = n_1n_2 - U_1 = ' + t(r.U2));
      if (r.z !== undefined) w += disp('z = \\frac{U_1 - n_1n_2/2 \\mp \\tfrac12}{\\sqrt{\\frac{n_1n_2}{12}\\left[(N+1) - \\frac{\\sum (t^3 - t)}{N(N-1)}\\right]}} = ' + t(r.z));
      return card('Mann\u2013Whitney U test: ' + a + ' and ' + b, ['mw'],
        '<p>\\(H_0\\): the two populations are the same, against \\(H_1\\): ' + a + ' tends to be ' + { two: 'larger or smaller than', less: 'smaller than', greater: 'larger than' }[c.alt] + ' ' + b + '. Independent samples; ranks of the combined sample (ties given the mean rank).</p>' + w +
        table([['\\(U_1\\)', f(r.U1)], ['\\(n_1, n_2\\)', r.n1 + ', ' + r.n2], ['p-value (' + r.method + ')', pv(r.p)]]) +
        (r.method === 'exact' ? '' : '<p class="s3-small">Ties or samples larger than 20, so the normal approximation with the tie and continuity corrections is used.</p>') +
        decisionHtml(r, c.alpha, 'The two populations differ in location (in the direction stated).', KEEP));
    },
    kw(c) {
      const idx = c.data.cols.map((x, i) => i).filter((i) => c.data.cols[i].length > 0);
      const groups = idx.map((i) => c.data.cols[i]);
      groups.forEach((g, j) => c.need(g, 2, c.nm[idx[j]]));
      const r = S.kruskal(groups, c.alpha);
      return card('Kruskal\u2013Wallis H test', ['kw'],
        '<p>\\(H_0\\): the ' + groups.length + ' populations are the same, against \\(H_1\\): at least one tends to give larger values. Independent samples; no normality assumed.</p>' +
        '<p>Rank sums: ' + idx.map((i, j) => esc(c.nm[i]) + ' \\(R = ' + t(r.R[j]) + '\\) (n = ' + r.ns[j] + ')').join('; ') + '.</p>' +
        disp('H = \\frac{12}{N(N+1)}\\sum \\frac{R_i^2}{n_i} - 3(N+1) = ' + t(r.H) + (r.C < 1 ? ',\\qquad H_c = \\frac{H}{1 - \\sum (t^3 - t)/(N^3 - N)} = \\frac{' + t(r.H) + '}{' + t(r.C) + '} = ' + t(r.stat) : '')) +
        table([['\\(H\\)' + (r.C < 1 ? ' (corrected for ties)' : ''), f(r.stat)], ['Degrees of freedom', r.df], ['p-value (\u03c7\u00b2 approximation)', pv(r.p)], ['Critical value', f(r.crit[0])]]) +
        decisionHtml(r, c.alpha, 'The populations are not all the same.', KEEP));
    },
    runs(c) {
      c.need(c.X, 4);
      const r = S.runsTest(c.X, c.alpha, c.alt);
      if (r.n1 === 0 || r.n2 === 0) throw new Error('All usable values fall on one side of the median, so runs cannot be counted.');
      return card('Runs test for randomness of ' + esc(c.nm[c.v1]), ['runs'],
        '<p>\\(H_0\\): the order is random, against \\(H_1\\): ' + { two: 'it is not', less: 'too few runs (clustering or a trend)', greater: 'too many runs (alternation)' }[c.alt] + '. Values above the median ' + f(r.median) + ' are +, below are &minus;' + (r.dropped ? '; ' + r.dropped + ' equal to the median left out' : '') + '.</p>' +
        '<p class="s3-small">Sequence: ' + esc(r.seq) + '</p>' +
        (r.z !== undefined ? disp('E(R) = \\frac{2n_1n_2}{N} + 1 = ' + t(r.mu) + ',\\quad V(R) = ' + t(r.var) + ',\\quad z = ' + t(r.z)) : '') +
        table([['Runs \\(R\\)', r.stat], ['\\(n_1\\) (+), \\(n_2\\) (&minus;)', r.n1 + ', ' + r.n2], ['p-value (' + r.method + ')', pv(r.p)]]) +
        decisionHtml(r, c.alpha, 'The order of the values is not random.', KEEP));
    }
  };
  function wilcoxonCard(c, r, title, hyp, ifReject) {
    if (r.n === 0) throw new Error('Every difference is zero.');
    let w = '<p>' + hyp + ' Zero differences are left out (' + r.zeros + ').</p>' +
      disp('T^+ = \\text{sum of the ranks of the positive differences} = ' + t(r.tPlus) + ',\\qquad T^- = ' + t(r.tMinus) + ',\\qquad n = ' + r.n);
    if (r.z !== undefined) w += disp('z = \\frac{T^+ - n(n+1)/4 \\mp \\tfrac12}{\\sqrt{\\frac{n(n+1)(2n+1)}{24} - \\frac{\\sum (t^3 - t)}{48}}} = \\frac{' + t(r.tPlus) + ' - ' + t(r.mu) + ' \\mp 0.5}{' + t(Math.sqrt(r.var)) + '} = ' + t(r.z));
    return card(title, ['wilcoxon'], w +
      table([['\\(T^+\\)', f(r.tPlus)], ['\\(n\\)', r.n], ['p-value (' + r.method + ')', pv(r.p)]]) +
      (r.method === 'exact' ? '' : '<p class="s3-small">Ties among the |differences| or more than 50 of them, so the normal approximation with the tie and continuity corrections is used.</p>') +
      decisionHtml(r, c.alpha, ifReject, KEEP));
  }

  /* ---------------------------------------------------------------- 4. distributions */
  const SPEC = {
    degenerate: [['c', 'value c']], bernoulli: [['p', 'p']], binomial: [['p', 'p'], ['n', 'trials n']],
    poisson: [['lambda', '\u03bb']], geometric: [['p', 'p']], negbinomial: [['r', 'r'], ['p', 'p']],
    hypergeometric: [['M', 'successes M'], ['N', 'population N'], ['n', 'drawn n']], duniform: [['a', 'a'], ['b', 'b']],
    uniform: [['a', 'a'], ['b', 'b']], normal: [['mu', '\u03bc'], ['sigma', '\u03c3']], lognormal: [['mu', '\u03bc of log x'], ['sigma', '\u03c3 of log x']],
    exponential: [['lambda', '\u03bb']], laplace: [['mu', '\u03bc'], ['b', 'b']], gamma: [['alpha', '\u03b1 (shape)'], ['lambda', '\u03bb (rate)']],
    beta1: [['alpha', '\u03b1'], ['beta', '\u03b2']], beta2: [['alpha', '\u03b1'], ['beta', '\u03b2']], cauchy: [['mu', '\u03bc'], ['lambda', '\u03bb']],
    weibull: [['k', 'k (shape)'], ['lambda', '\u03bb (scale)']], logistic: [['mu', '\u03bc'], ['s', 's']], pareto: [['alpha', '\u03b1'], ['xm', 'x\u2098']]
  };
  const PDF_TEX = {
    degenerate: 'P(X = c) = 1', bernoulli: 'P(X = x) = p^x q^{1-x},\\ x = 0, 1',
    binomial: 'P(X = x) = \\binom{n}{x}p^x q^{n-x}', poisson: 'P(X = x) = \\frac{e^{-\\lambda}\\lambda^x}{x!}',
    geometric: 'P(X = x) = q^x p,\\ x = 0, 1, 2, \\ldots', negbinomial: 'P(X = x) = \\binom{x + r - 1}{x}p^r q^x',
    hypergeometric: 'P(X = x) = \\frac{\\binom{M}{x}\\binom{N-M}{n-x}}{\\binom{N}{n}}', duniform: 'P(X = x) = \\frac{1}{b - a + 1},\\ x = a, \\ldots, b',
    uniform: 'f(x) = \\frac{1}{b - a},\\ a \\le x \\le b', normal: 'f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}e^{-(x-\\mu)^2/2\\sigma^2}',
    lognormal: 'f(x) = \\frac{1}{x\\sigma\\sqrt{2\\pi}}e^{-(\\ln x-\\mu)^2/2\\sigma^2}', exponential: 'f(x) = \\lambda e^{-\\lambda x}',
    laplace: 'f(x) = \\frac{1}{2b}e^{-|x-\\mu|/b}', gamma: 'f(x) = \\frac{\\lambda^\\alpha}{\\Gamma(\\alpha)}x^{\\alpha-1}e^{-\\lambda x}',
    beta1: 'f(x) = \\frac{x^{\\alpha-1}(1-x)^{\\beta-1}}{B(\\alpha, \\beta)}', beta2: 'f(x) = \\frac{x^{\\alpha-1}}{B(\\alpha, \\beta)(1+x)^{\\alpha+\\beta}}',
    cauchy: 'f(x) = \\frac{1}{\\pi\\lambda[1 + ((x-\\mu)/\\lambda)^2]}', weibull: 'f(x) = \\frac{k}{\\lambda}\\left(\\frac{x}{\\lambda}\\right)^{k-1}e^{-(x/\\lambda)^k}',
    logistic: 'f(x) = \\frac{e^{-(x-\\mu)/s}}{s(1 + e^{-(x-\\mu)/s})^2}', pareto: 'f(x) = \\frac{\\alpha x_m^\\alpha}{x^{\\alpha+1}},\\ x \\ge x_m'
  };
  const MOM_TEX = {
    bernoulli: '\\hat p = \\bar x', binomial: '\\hat p = \\bar x/n', poisson: '\\hat\\lambda = \\bar x', geometric: '\\hat p = 1/(1 + \\bar x)',
    negbinomial: '\\tilde r = \\bar x^2/(\\sigma^2 - \\bar x),\\ \\tilde p = \\bar x/\\sigma^2', hypergeometric: '\\tilde M = N\\bar x/n',
    duniform: '\\tilde a, \\tilde b = \\bar x \\mp (\\sqrt{12\\sigma^2 + 1} - 1)/2', uniform: '\\tilde a, \\tilde b = \\bar x \\mp \\sqrt3\\,\\sigma',
    normal: '\\tilde\\mu = \\bar x,\\ \\tilde\\sigma = \\sigma', lognormal: '\\tilde\\sigma^2 = \\ln(1 + \\sigma^2/\\bar x^2),\\ \\tilde\\mu = \\ln\\bar x - \\tilde\\sigma^2/2',
    exponential: '\\tilde\\lambda = 1/\\bar x', laplace: '\\tilde\\mu = \\bar x,\\ \\tilde b = \\sigma/\\sqrt2', gamma: '\\tilde\\alpha = \\bar x^2/\\sigma^2,\\ \\tilde\\lambda = \\bar x/\\sigma^2',
    beta1: '\\tilde\\alpha = \\bar x c,\\ \\tilde\\beta = (1 - \\bar x)c,\\ c = \\bar x(1 - \\bar x)/\\sigma^2 - 1', beta2: '\\tilde\\beta = 2 + \\bar x(\\bar x + 1)/\\sigma^2,\\ \\tilde\\alpha = \\bar x(\\tilde\\beta - 1)',
    cauchy: '\\tilde\\mu = \\text{median},\\ \\tilde\\lambda = (Q_3 - Q_1)/2', weibull: '\\Gamma(1 + 2/k)/\\Gamma(1 + 1/k)^2 = 1 + \\sigma^2/\\bar x^2',
    logistic: '\\tilde\\mu = \\bar x,\\ \\tilde s = \\sqrt3\\,\\sigma/\\pi', pareto: '\\tilde x_m = \\min x,\\ \\tilde\\alpha = \\bar x/(\\bar x - x_m)'
  };
  const MLE_TEX = {
    degenerate: '\\hat c = \\text{the common value}', bernoulli: '\\hat p = \\bar x', binomial: '\\hat p = \\bar x/n', poisson: '\\hat\\lambda = \\bar x',
    geometric: '\\hat p = 1/(1 + \\bar x)', negbinomial: '\\sum\\psi(x_i + r) - n\\psi(r) + n\\ln\\frac{r}{r + \\bar x} = 0,\\ \\hat p = \\frac{\\hat r}{\\hat r + \\bar x}\\ (\\text{solved numerically})',
    hypergeometric: '\\hat M \\text{ maximises the likelihood over whole numbers}', duniform: '\\hat a = \\min x,\\ \\hat b = \\max x',
    uniform: '\\hat a = \\min x,\\ \\hat b = \\max x', normal: '\\hat\\mu = \\bar x,\\ \\hat\\sigma^2 = \\frac1n\\sum(x - \\bar x)^2',
    lognormal: '\\hat\\mu, \\hat\\sigma \\text{ are the mean and SD (divisor } n) \\text{ of } \\ln x', exponential: '\\hat\\lambda = 1/\\bar x',
    laplace: '\\hat\\mu = \\text{median},\\ \\hat b = \\frac1n\\sum|x - \\hat\\mu|', gamma: '\\ln\\hat\\alpha - \\psi(\\hat\\alpha) = \\ln\\bar x - \\overline{\\ln x},\\ \\hat\\lambda = \\hat\\alpha/\\bar x\\ (\\text{solved numerically})',
    beta1: '\\psi(\\alpha) - \\psi(\\alpha + \\beta) = \\overline{\\ln x},\\ \\psi(\\beta) - \\psi(\\alpha + \\beta) = \\overline{\\ln(1 - x)}\\ (\\text{numerically})',
    beta2: '\\text{as for } \\beta_1 \\text{ with } y = x/(1 + x)\\ (\\text{numerically})', cauchy: '\\text{maximum of the likelihood, found numerically}',
    weibull: '\\frac{\\sum x^k\\ln x}{\\sum x^k} - \\frac1k = \\overline{\\ln x},\\ \\hat\\lambda = (\\overline{x^k})^{1/k}\\ (\\text{numerically})',
    logistic: '\\text{the two likelihood equations, solved numerically}', pareto: '\\hat x_m = \\min x,\\ \\hat\\alpha = n/\\sum\\ln(x/\\hat x_m)'
  };

  let distBuilt = false;
  function renderDistForm() {
    const nm = names(), sel = $('s3-dist-var'), old = sel.value;
    sel.innerHTML = nm.slice(0, state.k).map((s, i) => '<option value="' + i + '">' + esc(s) + '</option>').join('');
    if (old && +old < state.k) sel.value = old;
    if (!distBuilt) {
      $('s3-spec-dist').innerHTML = S.DIST_ORDER.map((k) => '<option value="' + k + '">' + esc(S.DIST[k].name) + '</option>').join('');
      $('s3-spec-dist').value = 'normal';
      $('s3-spec-dist').addEventListener('change', specParams);
      $('s3-dist-go').addEventListener('click', runFits);
      $('s3-spec-go').addEventListener('click', runSpec);
      distBuilt = true;
      specParams();
    }
  }
  function specParams() {
    const k = $('s3-spec-dist').value;
    $('s3-spec-params').innerHTML = SPEC[k].map(([id, lab]) => '<label>' + esc(lab) + ' <input type="text" inputmode="decimal" data-sp="' + id + '"></label>').join('');
  }
  function distOptions() {
    const o = { alpha: +$('s3-dist-alpha').value };
    const bn = parseNum($('s3-binom-n').value), hN = parseNum($('s3-hyper-N').value), hn = parseNum($('s3-hyper-n').value);
    if (bn > 0) o.binomN = Math.round(bn);
    if (hN > 0) o.hyperN = Math.round(hN);
    if (hn > 0) o.hyperDraws = Math.round(hn);
    return o;
  }
  function paramText(fit, which) {
    const p = which === 'mom' ? fit.mom : fit.mle;
    if (!p) return '&ndash;';
    return fit.names.map((n, i) => esc(n) + ' = ' + f(p[i])).join(', ');
  }
  function badge(test) {
    if (!test || test.reject === null || test.reject === undefined || Number.isNaN(test.p)) return '<span class="s3-badge s3-na">no test</span>';
    return test.reject ? '<span class="s3-badge s3-reject">rejected</span>' : '<span class="s3-badge s3-keep">not rejected</span>';
  }

  function runFits() {
    const out = $('s3-dist-out'), data = readData(), nm = names();
    out.innerHTML = '';
    if (data.errors.length) { needData(out, 'Some cells are not numbers; correct them first.'); return; }
    const vi = +$('s3-dist-var').value, x = data.cols[vi];
    if (x.length < 5) { needData(out, 'Comparing with distributions needs at least five values of the variable.'); return; }
    const o = distOptions(), fits = S.fitAll(x, o);
    const ok = fits.filter((r) => r.applicable).sort((a, b) => a.aic - b.aic);
    const no = fits.filter((r) => !r.applicable);
    const disc = ok.filter((r) => r.kind === 'discrete'), cont = ok.filter((r) => r.kind === 'continuous');
    let h = '<p>Comparing the ' + x.length + ' values of ' + esc(nm[vi]) + ' at the ' + (o.alpha * 100) + '% level. Within each group the rows are ordered by AIC, smallest (best) first. '
      + 'AIC \\(= 2k - 2\\ln L\\), where \\(k\\) is the number of parameters estimated and \\(L\\) the likelihood at the estimates. '
      + 'Discrete and continuous fits are not compared with each other by AIC.</p>';
    const tableFor = (rows, title) => {
      if (!rows.length) return '';
      let tb = '<h3>' + title + '</h3><div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Distribution</th><th class="s3-l">Maximum-likelihood estimates</th><th>ln L</th><th>AIC</th><th>\u03c7\u00b2 (df)</th><th>p</th><th class="s3-l">\u03c7\u00b2 test</th>' +
        (rows[0].kind === 'continuous' ? '<th>K&ndash;S D</th><th>p</th><th class="s3-l">K&ndash;S test</th>' : '') + '<th>Draw</th></tr></thead><tbody>';
      rows.forEach((r) => {
        const link = LEARN[r.key] ? '<a href="' + LEARN[r.key][0] + '">' + esc(r.name) + '</a>' : esc(r.name);
        tb += '<tr><td class="s3-l"><span class="s3-dist-name">' + link + '</span></td><td class="s3-l">' + paramText(r, 'mle') + '</td><td>' + f(r.logL, 3) + '</td><td>' + f(r.aic, 3) + '</td>';
        if (r.perfect) tb += '<td colspan="3" class="s3-l">every value equal: a perfect fit</td>';
        else tb += '<td>' + (r.chi.df >= 1 ? f(r.chi.stat, 3) + ' (' + r.chi.df + ')' : '&ndash;') + '</td><td>' + (r.chi.df >= 1 ? pv(r.chi.p) : '&ndash;') + '</td><td class="s3-l">' + (r.chi.df >= 1 ? badge(r.chi) : '<span class="s3-badge s3-na">too few classes</span>') + '</td>';
        if (r.kind === 'continuous') tb += '<td>' + f(r.ks.D) + '</td><td>' + pv(r.ks.p) + '</td><td class="s3-l">' + badge(r.ks) + '</td>';
        tb += '<td><input type="checkbox" data-draw="' + r.key + '" aria-label="Draw ' + esc(r.name) + '"></td></tr>';
      });
      return tb + '</tbody></table></div>';
    };
    h += tableFor(disc, 'Discrete distributions') + tableFor(cont, 'Continuous distributions');
    if (no.length) {
      h += '<h3>Not fitted</h3><div class="table-scroll"><table class="s3-table"><tbody>' +
        no.map((r) => '<tr class="s3-dim"><td class="s3-l">' + esc(r.name) + '</td><td class="s3-l">' + esc(r.reason) + '</td></tr>').join('') + '</tbody></table></div>';
    }
    // summary
    const tested = ok.filter((r) => !r.perfect && r.chi && r.chi.df >= 1);
    const kept = tested.filter((r) => !r.chi.reject).map((r) => r.name);
    const ksKept = cont.filter((r) => r.ks && !r.ks.reject).map((r) => r.name);
    const best = (rows) => rows.length ? rows[0].name + ' (AIC ' + f(rows[0].aic, 2) + ')' : null;
    let chiLine;
    if (!tested.length) chiLine = 'With ' + x.length + ' values no \u03c7\u00b2 test is possible: after pooling classes to give expected frequencies of at least 5, too few classes are left. ';
    else if (kept.length) chiLine = 'The \u03c7\u00b2 test does not reject: ' + kept.map(esc).join(', ') + '. ';
    else chiLine = 'The \u03c7\u00b2 test rejects every distribution it could test (' + tested.map((r) => esc(r.name)).join(', ') + '). ';
    if (cont.length) chiLine += ksKept.length ? 'The K&ndash;S test does not reject: ' + ksKept.map(esc).join(', ') + '. ' : 'The K&ndash;S test rejects every continuous fit. ';
    h += '<div class="s3-card"><h3>Summary</h3><p>' + chiLine +
      (best(disc) ? 'Lowest AIC among the discrete fits: ' + esc(best(disc)) + '. ' : '') +
      (best(cont) ? 'Lowest AIC among the continuous fits: ' + esc(best(cont)) + '. ' : '') + '</p>' +
      '<p>&ldquo;Not rejected&rdquo; means the data are consistent with that distribution, not that they come from it: with few values, several quite different distributions are usually not rejected. '
      + 'The K&ndash;S p-values assume the parameters were known in advance; with parameters estimated from the same data they are too large (conservative). '
      + learn('gof') + ' &middot; ' + learn('ks') + ' &middot; ' + learn('mle') + ' &middot; ' + learn('mom') + '</p></div>';
    h += '<h3>Histogram with the fitted distributions</h3><div id="s3-fit-chart"></div>' +
      '<h3>Q&ndash;Q plot</h3><label>Against <select id="s3-qq-dist">' + cont.map((r) => '<option value="' + r.key + '">' + esc(r.name) + '</option>').join('') + '</select></label><div id="s3-qq"></div>';
    h += '<h3>Each fit in detail</h3>' + ok.map((r) => fitDetail(r, x)).join('');
    out.innerHTML = h;
    const byKey = {};
    ok.forEach((r) => { byKey[r.key] = r; });
    const pre = [disc[0], cont[0], cont[1]].filter((r) => r && !r.perfect).map((r) => r.key);
    out.querySelectorAll('[data-draw]').forEach((cb) => { cb.checked = pre.indexOf(cb.dataset.draw) >= 0; cb.addEventListener('change', drawFit); });
    function drawFit() {
      const keys = Array.from(out.querySelectorAll('[data-draw]:checked')).map((cb) => cb.dataset.draw).slice(0, 4);
      const host = $('s3-fit-chart');
      host.innerHTML = '';
      const overlays = keys.map((k) => ({ discrete: byKey[k].kind === 'discrete', density: S.densityOf(k, byKey[k].mle), name: byKey[k].name }));
      host.appendChild(figure(histogram(x, overlays, 'Histogram of ' + nm[vi] + ' with fitted distributions', disc.length > 0),
        'Bars: the data. ' + (overlays.length ? 'Lines: the expected frequencies under each ticked distribution (at most four).' : 'Tick distributions in the table to draw them.')));
      if (overlays.length) host.appendChild(legend(overlays.map((o) => o.name)));
    }
    drawFit();
    const drawQQ = () => {
      const host = $('s3-qq');
      host.innerHTML = '';
      if (!cont.length) { host.innerHTML = '<p class="s3-small">A Q&ndash;Q plot needs a continuous distribution that fits these data.</p>'; return; }
      const r = byKey[$('s3-qq-dist').value];
      host.appendChild(figure(qqPlot(x, r), 'Sample quantiles against the quantiles of the fitted ' + esc(r.name) + ' distribution, at \\((i - \\tfrac12)/n\\). Points close to the dashed line mean a good fit; a bend at the ends shows tails heavier or lighter than the distribution\u2019s.'));
      typeset(host);
    };
    if ($('s3-qq-dist')) $('s3-qq-dist').addEventListener('change', drawQQ);
    drawQQ();
    typeset(out);
  }

  function quantileOf(r, p, x) {
    const cdf = S.cdfOf(r.key, r.mle), d = S.describe(x);
    let lo = d.min - 10 * (d.range || 1), hi = d.max + 10 * (d.range || 1);
    for (let i = 0; i < 60 && cdf(lo) > p; i++) lo -= 10 * (d.range || 1) * (i + 1);
    for (let i = 0; i < 60 && cdf(hi) < p; i++) hi += 10 * (d.range || 1) * (i + 1);
    for (let i = 0; i < 200; i++) { const m = (lo + hi) / 2; if (cdf(m) < p) lo = m; else hi = m; }
    return (lo + hi) / 2;
  }
  function qqPlot(x, r) {
    const s = S.sorted(x), n = s.length;
    const q = s.map((_, i) => quantileOf(r, (i + 0.5) / n, x));
    const W = Math.min(560, chartWidth()), H = W, box = [60, 16, W - 16, H - 52];
    const svg = chart(W, H, 'Q-Q plot against the ' + r.name + ' distribution');
    const all = q.concat(s), lo = Math.min.apply(null, all), hi = Math.max.apply(null, all), pad = (hi - lo) * 0.05 || 1;
    const [sx, sy] = axes(svg, box, [lo - pad, hi + pad], [lo - pad, hi + pad], 'theoretical quantile', 'sample quantile');
    el(svg, 'line', { x1: sx(lo - pad), y1: sy(lo - pad), x2: sx(hi + pad), y2: sy(hi + pad), class: 's3-ref' });
    for (let i = 0; i < n; i++) el(svg, 'circle', { cx: sx(q[i]), cy: sy(s[i]), r: 3.8, class: 's3-c0 s3-pt' });
    return svg;
  }

  function fitDetail(r, x) {
    let h = '<details class="s3-working"><summary>' + esc(r.name) + '</summary>';
    h += '<p>' + tex(PDF_TEX[r.key]) + (LEARN[r.key] ? ' &middot; ' + learn(r.key) : '') + '</p>';
    h += '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Method</th><th class="s3-l">Equations</th><th class="s3-l">Estimates</th></tr></thead><tbody>' +
      (r.mom ? '<tr><td class="s3-l">Method of moments</td><td class="s3-l">' + tex(MOM_TEX[r.key] || '') + '</td><td class="s3-l">' + paramText(r, 'mom') + '</td></tr>' : '') +
      '<tr><td class="s3-l">Maximum likelihood (used below)</td><td class="s3-l">' + tex(MLE_TEX[r.key] || '') + '</td><td class="s3-l">' + paramText(r, 'mle') + '</td></tr></tbody></table></div>';
    if (S.DIST[r.key].momNote) h += '<p class="s3-small">' + esc(S.DIST[r.key].momNote) + '</p>';
    h += '<p class="s3-small">Here \\(\\sigma^2\\) is the variance with divisor \\(n\\). ln L = ' + f(r.logL, 4) + ', AIC = ' + f(r.aic, 4) + ', BIC = ' + f(r.bic, 4) + '.</p>';
    if (!r.perfect) h += gofTable(r.chi) + ksLine(r);
    return h + '</details>';
  }
  function gofTable(chi) {
    let h = '<div class="table-scroll"><table class="s3-table"><thead><tr><th class="s3-l">Class</th><th>Observed O</th><th>Expected E</th><th>(O &minus; E)\u00b2/E</th></tr></thead><tbody>';
    const last = chi.cells.length - 1;
    chi.cells.forEach((c, i) => {
      h += '<tr><td class="s3-l">' + cellLabel(c, i === 0, i === last, chi.discrete) + (c.merged ? ' <span class="s3-sub">(pooled)</span>' : '') +
        '</td><td>' + c.obs + '</td><td>' + f(c.exp) + '</td><td>' + f(Math.abs(c.contrib) < 1e-12 ? 0 : c.contrib) + '</td></tr>';
    });
    h += '<tr><td class="s3-l"><strong>Total</strong></td><td>' + chi.cells.reduce((a, c) => a + c.obs, 0) + '</td><td>' + f(chi.cells.reduce((a, c) => a + c.exp, 0)) + '</td><td><strong>' + f(chi.stat) + '</strong></td></tr></tbody></table></div>';
    h += '<p>Classes with expected frequency below 5 are pooled with their neighbours. ' +
      (chi.df >= 1 ? '\\(\\nu = ' + chi.cells.length + ' - 1 - ' + chi.nEst + ' = ' + chi.df + '\\) (classes, less one, less the parameters estimated); \\(\\chi^2 = ' + t(chi.stat) + '\\), \\(' + pEq(chi.p) + '\\), critical value ' + f(chi.crit) + '. ' + badge(chi)
        : 'After pooling there are too few classes for the test (\\(\\nu = ' + chi.df + '\\)).') + '</p>';
    return h;
  }
  /* A class of the chi-square table: the first is open below, the last above. */
  function cellLabel(c, first, last, discrete) {
    if (first && last) return 'all values';
    if (discrete) {
      if (first) return '&le; ' + f(c.hi);
      if (last) return '&ge; ' + f(c.lo);
      return c.lo === c.hi ? f(c.lo) : f(c.lo) + ' to ' + f(c.hi);
    }
    if (first) return 'below ' + f(c.hi);
    if (last) return f(c.lo) + ' and above';
    return f(c.lo) + ' to under ' + f(c.hi);
  }
  function ksLine(r) {
    if (!r.ks) return '';
    return '<p>Kolmogorov&ndash;Smirnov: \\(D = \\max|F_n(x) - F(x)| = ' + t(r.ks.D) + '\\), \\(' + pEq(r.ks.p) + '\\) (exact distribution of \\(D\\) for \\(n = ' + r.ks.n + '\\)' +
      (r.ks.estimated ? '; conservative here, because the parameters were estimated from these data' : '') + '). ' + badge(r.ks) + '</p>';
  }

  function runSpec() {
    const out = $('s3-spec-out'), data = readData(), nm = names();
    try {
      if (data.errors.length) throw new Error('Some cells are empty or not numbers (' + data.errors[0] + ') Fill them on the Enter data tab.');
      const vi = +$('s3-dist-var').value, x = data.cols[vi];
      if (x.length < 5) throw new Error('This needs at least five values of the variable.');
      const key = $('s3-spec-dist').value, vals = {};
      SPEC[key].forEach(([id, lab]) => {
        const v = parseNum($('s3-spec-params').querySelector('[data-sp="' + id + '"]').value);
        if (v === null || Number.isNaN(v)) throw new Error('Enter a number for ' + lab + '.');
        vals[id] = v;
      });
      const o = { alpha: +$('s3-dist-alpha').value };
      const order = SPEC[key].map(([id]) => vals[id]);
      if (key === 'binomial') o.binomN = vals.n;
      if (key === 'hypergeometric') { o.hyperN = vals.N; o.hyperDraws = vals.n; }
      const bad = { binomial: vals.p <= 0 || vals.p >= 1 || vals.n < 1, bernoulli: vals.p <= 0 || vals.p >= 1, geometric: vals.p <= 0 || vals.p >= 1,
        negbinomial: vals.p <= 0 || vals.p >= 1 || vals.r <= 0, poisson: vals.lambda <= 0, exponential: vals.lambda <= 0,
        normal: vals.sigma <= 0, lognormal: vals.sigma <= 0, laplace: vals.b <= 0, gamma: vals.alpha <= 0 || vals.lambda <= 0,
        beta1: vals.alpha <= 0 || vals.beta <= 0, beta2: vals.alpha <= 0 || vals.beta <= 0, cauchy: vals.lambda <= 0,
        weibull: vals.k <= 0 || vals.lambda <= 0, logistic: vals.s <= 0, pareto: vals.alpha <= 0 || vals.xm <= 0,
        uniform: vals.b <= vals.a, duniform: vals.b < vals.a }[key];
      if (bad) throw new Error('These parameter values are outside the range the distribution allows.');
      o.params = order;
      const r = S.fit(key, x, o);
      if (!r.applicable) throw new Error('This distribution cannot describe these data: ' + r.reason + '.');
      const spec = r.names.map((n, i) => esc(n) + ' = ' + f(order[i])).join(', ') + (key === 'binomial' ? ', n = ' + f(vals.n) : '') + (key === 'hypergeometric' ? ', N = ' + f(vals.N) + ', n = ' + f(vals.n) : '');
      const main = r.ks || r.chi;
      out.innerHTML = card('Does ' + esc(nm[vi]) + ' follow the ' + esc(r.name) + ' distribution with ' + spec + '?', ['gof'].concat(r.ks ? ['ks'] : []).concat(LEARN[key] ? [key] : []),
        '<p>\\(H_0\\): the data come from this distribution, with these parameter values; \\(H_1\\): they do not. Nothing is estimated from the data, so the degrees of freedom are not reduced.</p>' +
        (r.perfect ? '<p>Every value equals c: a perfect fit.</p>' : gofTable(r.chi) + ksLine(r)) +
        (main && !r.perfect ? decisionHtml(main, o.alpha, 'The data do not follow this distribution.', 'The data are consistent with this distribution; that does not prove they follow it.') : ''));
      if (!r.perfect) {
        const host = document.createElement('div');
        out.querySelector('.s3-card').appendChild(host);
        host.appendChild(figure(histogram(x, [{ discrete: r.kind === 'discrete', density: S.densityOf(key, order) }], 'Histogram with the specified distribution', r.kind === 'discrete'), 'Bars: the data; line: the expected frequencies under the distribution you specified.'));
      }
    } catch (e) {
      out.innerHTML = '<p class="s3-note">' + esc(e.message) + '</p>';
    }
    typeset(out);
  }

  /* ---------------------------------------------------------------- start */
  if (load()) {
    $('s3-remember').checked = true;
    syncControls(); buildSizes(); buildGrid();
  } else {
    // A first visit opens with the example, so every tab shows something.
    loadExample('corr');
  }
  show(location.hash.slice(1) || 'data', false);
})();
