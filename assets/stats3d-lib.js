/* StatsTricks360 — the mathematics behind the 3D Statistics page.

   Nothing in this file touches the page: it takes arrays of numbers and
   returns numbers, so tools/check_stats3d.js can run every function in Node
   and compare it with reference values computed independently with scipy.
   The page code (assets/stats3d.js) turns these results into tables, charts
   and worked steps.

   The distribution functions follow the site's own pure-Python library,
   data-science/labs/course-4-stats/python/statlib.py: the normal through the
   incomplete gamma function, t and F through the incomplete beta function,
   chi-square through the incomplete gamma function. Quantiles are found by
   bisection on those, to full double precision. */

(function (root) {
  'use strict';
  var S = {};
  var LN_SQRT_2PI = 0.9189385332046728;

  /* ------------------------------------------------------------------ */
  /* Special functions                                                   */
  /* ------------------------------------------------------------------ */

  var LANCZOS = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
    771.32342877765313, -176.61502916214059, 12.507343278686905,
    -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];

  function lgamma(x) {
    if (x < 0.5) return Math.log(Math.PI / Math.abs(Math.sin(Math.PI * x))) - lgamma(1 - x);
    x -= 1;
    var a = LANCZOS[0], t = x + 7.5;
    for (var i = 1; i < 9; i++) a += LANCZOS[i] / (x + i);
    return LN_SQRT_2PI + (x + 0.5) * Math.log(t) - t + Math.log(a);
  }
  S.lgamma = lgamma;
  S.gamma = function (x) {
    if (x === Math.floor(x) && x > 0 && x < 171) { var f = 1; for (var i = 2; i < x; i++) f *= i; return f; }
    return x < 0.5 ? Math.PI / (Math.sin(Math.PI * x) * S.gamma(1 - x)) : Math.exp(lgamma(x));
  };
  S.lbeta = function (a, b) { return lgamma(a) + lgamma(b) - lgamma(a + b); };
  function lchoose(n, k) {
    if (k < 0 || k > n) return -Infinity;
    return lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1);
  }
  S.lchoose = lchoose;

  /* Regularised incomplete gamma P(a, x) and Q(a, x) = 1 - P(a, x). */
  function gser(a, x) {
    var ap = a, sum = 1 / a, del = sum;
    for (var n = 0; n < 100000; n++) {
      ap += 1; del *= x / ap; sum += del;
      if (Math.abs(del) < Math.abs(sum) * 1e-17) break;
    }
    return sum * Math.exp(-x + a * Math.log(x) - lgamma(a));
  }
  function gcf(a, x) {
    var tiny = 1e-300, b = x + 1 - a, c = 1 / tiny, d = 1 / b, h = d;
    for (var i = 1; i < 100000; i++) {
      var an = -i * (i - a);
      b += 2;
      d = an * d + b; if (Math.abs(d) < tiny) d = tiny;
      c = b + an / c; if (Math.abs(c) < tiny) c = tiny;
      d = 1 / d;
      var del = d * c; h *= del;
      if (Math.abs(del - 1) < 1e-17) break;
    }
    return Math.exp(-x + a * Math.log(x) - lgamma(a)) * h;
  }
  S.gammaP = function (a, x) {
    if (x <= 0) return 0;
    return x < a + 1 ? gser(a, x) : 1 - gcf(a, x);
  };
  S.gammaQ = function (a, x) {
    if (x <= 0) return 1;
    return x < a + 1 ? 1 - gser(a, x) : gcf(a, x);
  };

  /* Regularised incomplete beta I_x(a, b). */
  function betacf(a, b, x) {
    var tiny = 1e-300, qab = a + b, qap = a + 1, qam = a - 1;
    var c = 1, d = 1 - qab * x / qap;
    if (Math.abs(d) < tiny) d = tiny;
    d = 1 / d;
    var h = d;
    for (var m = 1; m < 100000; m++) {
      var m2 = 2 * m, aa = m * (b - m) * x / ((qam + m2) * (a + m2));
      d = 1 + aa * d; if (Math.abs(d) < tiny) d = tiny;
      c = 1 + aa / c; if (Math.abs(c) < tiny) c = tiny;
      d = 1 / d; h *= d * c;
      aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
      d = 1 + aa * d; if (Math.abs(d) < tiny) d = tiny;
      c = 1 + aa / c; if (Math.abs(c) < tiny) c = tiny;
      d = 1 / d;
      var del = d * c; h *= del;
      if (Math.abs(del - 1) < 1e-17) break;
    }
    return h;
  }
  S.betaI = function (x, a, b) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    var lbt = a * Math.log(x) + b * Math.log(1 - x) - S.lbeta(a, b);
    if (x < (a + 1) / (a + b + 2)) return Math.exp(lbt) * betacf(a, b, x) / a;
    return 1 - Math.exp(lbt) * betacf(b, a, 1 - x) / b;
  };

  S.digamma = function (x) {
    var r = 0;
    while (x < 8) { r -= 1 / x; x += 1; }
    var f = 1 / (x * x);
    return r + Math.log(x) - 0.5 / x - f * (1 / 12 - f * (1 / 120 - f * (1 / 252 - f * (1 / 240 - f * (1 / 132)))));
  };
  S.trigamma = function (x) {
    var r = 0;
    while (x < 8) { r += 1 / (x * x); x += 1; }
    var f = 1 / (x * x);
    return r + 1 / x + f / 2 + f / x * (1 / 6 - f * (1 / 30 - f * (1 / 42 - f * (1 / 30))));
  };

  /* ------------------------------------------------------------------ */
  /* Distributions used by the tests                                     */
  /* ------------------------------------------------------------------ */

  S.normPdf = function (z) { return Math.exp(-0.5 * z * z - LN_SQRT_2PI); };
  S.normCdf = function (z) {
    if (z === Infinity) return 1;
    if (z === -Infinity) return 0;
    var q = 0.5 * S.gammaQ(0.5, z * z / 2);
    return z >= 0 ? 1 - q : q;
  };
  S.normSf = function (z) { return S.normCdf(-z); };
  S.normInv = function (p) {
    if (p <= 0) return -Infinity;
    if (p >= 1) return Infinity;
    var a = [-3.969683028665376e1, 2.209460984245205e2, -2.759285104469687e2, 1.383577518672690e2, -3.066479806614716e1, 2.506628277459239],
        b = [-5.447609879822406e1, 1.615858368580409e2, -1.556989798598866e2, 6.680131188771972e1, -1.328068155288572e1],
        c = [-7.784894002430293e-3, -3.223964580411365e-1, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783],
        d = [7.784695709041462e-3, 3.224671290700398e-1, 2.445134137142996, 3.754408661907416];
    var x, q, r;
    if (p < 0.02425) {
      q = Math.sqrt(-2 * Math.log(p));
      x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    } else if (p <= 1 - 0.02425) {
      q = p - 0.5; r = q * q;
      x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
    } else {
      q = Math.sqrt(-2 * Math.log(1 - p));
      x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1);
    }
    for (var i = 0; i < 2; i++) {          // Halley steps to full precision
      // e = Phi(x) - p, written through the upper tail when p is near 1
      var e = p < 0.5 ? S.normCdf(x) - p : (1 - p) - S.normSf(x);
      var u = e * Math.sqrt(2 * Math.PI) * Math.exp(x * x / 2);
      x = x - u / (1 + x * u / 2);
    }
    return x;
  };

  S.tCdf = function (t, df) {
    var tail = 0.5 * S.betaI(df / (df + t * t), df / 2, 0.5);
    return t > 0 ? 1 - tail : tail;
  };
  S.tSf = function (t, df) { return S.tCdf(-t, df); };
  S.chi2Cdf = function (x, k) { return S.gammaP(k / 2, x / 2); };
  S.chi2Sf = function (x, k) { return S.gammaQ(k / 2, x / 2); };
  S.fCdf = function (f, d1, d2) { return f <= 0 ? 0 : S.betaI(d1 * f / (d1 * f + d2), d1 / 2, d2 / 2); };
  S.fSf = function (f, d1, d2) { return f <= 0 ? 1 : S.betaI(d2 / (d2 + d1 * f), d2 / 2, d1 / 2); };

  /* Quantile by bisection: lower-tail probability p, using the survival
     function above the median so that small upper tails keep their digits. */
  function invert(cdf, sf, p, lo, hi) {
    var useSf = p > 0.5, target = useSf ? 1 - p : p;
    var f = function (x) { return useSf ? target - sf(x) : cdf(x) - target; };
    while (f(hi) < 0) { lo = hi; hi = hi * 2 + 1; }
    while (f(lo) > 0) { hi = lo; lo = lo < 0 ? lo * 2 - 1 : lo / 2; if (lo < 1e-300 && lo > 0) break; }
    for (var i = 0; i < 300; i++) {
      var mid = (lo + hi) / 2;
      if (mid === lo || mid === hi) break;
      if (f(mid) < 0) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
  }
  S.tInv = function (p, df) {
    return invert(function (x) { return S.tCdf(x, df); }, function (x) { return S.tSf(x, df); }, p, -10, 10);
  };
  S.chi2Inv = function (p, k) {
    return invert(function (x) { return S.chi2Cdf(x, k); }, function (x) { return S.chi2Sf(x, k); }, p, 0, Math.max(10, 2 * k));
  };
  S.fInv = function (p, d1, d2) {
    return invert(function (x) { return S.fCdf(x, d1, d2); }, function (x) { return S.fSf(x, d1, d2); }, p, 0, 10);
  };

  /* p-value and critical values for a statistic with a symmetric (z, t) or
     a one-sided-positive (chi-square, F) null distribution. */
  function pvalueSym(stat, cdf, sf, alt) {
    if (alt === 'less') return cdf(stat);
    if (alt === 'greater') return sf(stat);
    return Math.min(1, 2 * sf(Math.abs(stat)));
  }
  function pvalueTwoTail(stat, cdf, sf, alt) {
    if (alt === 'less') return cdf(stat);
    if (alt === 'greater') return sf(stat);
    return Math.min(1, 2 * Math.min(cdf(stat), sf(stat)));
  }
  function decide(p, alpha) { return p <= alpha; }

  /* ------------------------------------------------------------------ */
  /* Descriptive statistics                                              */
  /* ------------------------------------------------------------------ */

  function sum(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s; }
  function mean(a) { return sum(a) / a.length; }
  function sorted(a) { return a.slice().sort(function (p, q) { return p - q; }); }
  function ss(a, m) { var s = 0; for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m); return s; }
  S.sum = sum; S.mean = mean; S.sorted = sorted;
  S.variance = function (a) { return ss(a, mean(a)) / (a.length - 1); };

  /* Item at position pos (1-based) of sorted data, interpolating between the
     two values around it: the site's (n + 1)p rule (Descriptive Statistics,
     Unit 3: "interpolate between the bracketing values"). */
  function positional(s, pos) {
    var n = s.length;
    if (pos <= 1) return s[0];
    if (pos >= n) return s[n - 1];
    var lo = Math.floor(pos), fr = pos - lo;
    return s[lo - 1] + fr * (s[lo] - s[lo - 1]);
  }
  S.quantile = function (a, p) { return positional(sorted(a), p * (a.length + 1)); };

  S.describe = function (x) {
    var n = x.length, s = sorted(x), m = mean(x), i;
    var r = { n: n, sum: sum(x), mean: m, min: s[0], max: s[n - 1], sorted: s };
    r.range = r.max - r.min;
    r.median = positional(s, (n + 1) / 2);
    var counts = {}, best = 0;
    for (i = 0; i < n; i++) { counts[s[i]] = (counts[s[i]] || 0) + 1; best = Math.max(best, counts[s[i]]); }
    r.modes = best > 1 ? Object.keys(counts).filter(function (k) { return counts[k] === best; })
      .map(Number).sort(function (p, q) { return p - q; }) : [];
    r.modeCount = best;
    var allPos = s[0] > 0;
    if (allPos) {
      var sl = 0, sr = 0;
      for (i = 0; i < n; i++) { sl += Math.log(x[i]); sr += 1 / x[i]; }
      r.gm = Math.exp(sl / n); r.hm = n / sr;
    }
    r.q1 = positional(s, (n + 1) / 4);
    r.q3 = positional(s, 3 * (n + 1) / 4);
    r.iqr = r.q3 - r.q1; r.qd = r.iqr / 2;
    r.coeffQD = (r.q3 + r.q1) !== 0 ? r.iqr / (r.q3 + r.q1) : NaN;
    var mdMean = 0, mdMed = 0, m2 = 0, m3 = 0, m4 = 0;
    for (i = 0; i < n; i++) {
      var d = x[i] - m;
      mdMean += Math.abs(d); mdMed += Math.abs(x[i] - r.median);
      m2 += d * d; m3 += d * d * d; m4 += d * d * d * d;
    }
    r.ss = m2;
    r.mdMean = mdMean / n; r.mdMedian = mdMed / n;
    r.mu2 = m2 / n; r.mu3 = m3 / n; r.mu4 = m4 / n;
    r.varN = r.mu2; r.sdN = Math.sqrt(r.varN);
    r.var = n > 1 ? m2 / (n - 1) : NaN; r.sd = Math.sqrt(r.var);
    r.se = r.sd / Math.sqrt(n);
    r.cv = m !== 0 ? 100 * r.sdN / m : NaN;
    if (r.mu2 > 0) {
      r.beta1 = r.mu3 * r.mu3 / Math.pow(r.mu2, 3);
      r.beta2 = r.mu4 / (r.mu2 * r.mu2);
      r.gamma1 = r.mu3 / Math.pow(r.mu2, 1.5);
      r.gamma2 = r.beta2 - 3;
      r.skPearson = 3 * (m - r.median) / r.sdN;
      if (r.modes.length === 1) r.skPearsonMode = (m - r.modes[0]) / r.sdN;
    }
    r.skBowley = r.iqr !== 0 ? (r.q3 + r.q1 - 2 * r.median) / r.iqr : NaN;
    return r;
  };

  /* A width of 1, 2, 2.5 or 5 times a power of ten, at least w. */
  function niceStep(w) {
    if (!(w > 0)) return 1;
    var e = Math.pow(10, Math.floor(Math.log10(w))), f = w / e;
    var step = f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10;
    return step * e;
  }
  S.niceStep = niceStep;

  /* Grouped frequency table: Sturges' number of classes, rounded to a tidy
     width, classes [L, L + h) with the last one closed. */
  S.freqTable = function (x) {
    var n = x.length, s = sorted(x), lo = s[0], hi = s[n - 1];
    var k = Math.ceil(1 + 3.322 * Math.log10(n));
    var h = niceStep((hi - lo) / k || 1);
    var start = Math.floor(lo / h) * h, classes = [];
    for (var L = start; L <= hi + 1e-12 * Math.max(1, Math.abs(hi)); L = start + classes.length * h) {
      classes.push({ lo: L, hi: L + h, f: 0 });
      if (classes.length > 60) break;
    }
    for (var i = 0; i < n; i++) {
      var j = Math.min(classes.length - 1, Math.floor((s[i] - start) / h + 1e-12));
      classes[j].f++;
    }
    var cum = 0;
    classes.forEach(function (c) { cum += c.f; c.cf = cum; c.mid = (c.lo + c.hi) / 2; c.rel = c.f / n; });
    return { sturges: k, width: h, start: start, classes: classes };
  };

  /* ------------------------------------------------------------------ */
  /* Two and three variables                                             */
  /* ------------------------------------------------------------------ */

  S.ranks = function (a) {
    var idx = a.map(function (v, i) { return i; }).sort(function (p, q) { return a[p] - a[q]; });
    var r = new Array(a.length), ties = [], i = 0;
    while (i < idx.length) {
      var j = i;
      while (j + 1 < idx.length && a[idx[j + 1]] === a[idx[i]]) j++;
      var avg = (i + j) / 2 + 1;
      for (var k = i; k <= j; k++) r[idx[k]] = avg;
      if (j > i) ties.push(j - i + 1);
      i = j + 1;
    }
    return { ranks: r, ties: ties };
  };

  S.bivariate = function (x, y) {
    var n = x.length, mx = mean(x), my = mean(y), sxx = 0, syy = 0, sxy = 0, i;
    for (i = 0; i < n; i++) {
      sxx += (x[i] - mx) * (x[i] - mx); syy += (y[i] - my) * (y[i] - my);
      sxy += (x[i] - mx) * (y[i] - my);
    }
    var r = { n: n, mx: mx, my: my, sxx: sxx, syy: syy, sxy: sxy };
    r.covN = sxy / n; r.cov = sxy / (n - 1);
    r.r = sxy / Math.sqrt(sxx * syy);
    r.r2 = r.r * r.r;
    r.byx = sxy / sxx; r.ayx = my - r.byx * mx;          // Y on X
    r.bxy = sxy / syy; r.axy = mx - r.bxy * my;          // X on Y
    var rx = S.ranks(x), ry = S.ranks(y), d2 = 0;
    for (i = 0; i < n; i++) d2 += Math.pow(rx.ranks[i] - ry.ranks[i], 2);
    var cf = 0;
    rx.ties.concat(ry.ties).forEach(function (m) { cf += (m * m * m - m) / 12; });
    r.rankX = rx.ranks; r.rankY = ry.ranks;
    r.sumd2 = d2; r.tieCF = cf;
    r.spearman = 1 - 6 * (d2 + cf) / (n * (n * n - 1));
    var br = (rx.ties.length || ry.ties.length) ? S.bivariateNoRank(rx.ranks, ry.ranks) : null;
    r.spearmanRanksR = br === null ? r.spearman : br;
    return r;
  };
  S.bivariateNoRank = function (x, y) {
    var mx = mean(x), my = mean(y), a = 0, b = 0, c = 0;
    for (var i = 0; i < x.length; i++) {
      a += (x[i] - mx) * (y[i] - my); b += (x[i] - mx) * (x[i] - mx); c += (y[i] - my) * (y[i] - my);
    }
    return a / Math.sqrt(b * c);
  };

  /* Variables 1, 2, 3 (the first is the one regressed on the other two). */
  S.trivariate = function (x1, x2, x3) {
    var r12 = S.bivariateNoRank(x1, x2), r13 = S.bivariateNoRank(x1, x3), r23 = S.bivariateNoRank(x2, x3);
    function partial(a, b, c) { return (a - b * c) / Math.sqrt((1 - b * b) * (1 - c * c)); }
    function multiple(a, b, c) { return Math.sqrt((a * a + b * b - 2 * a * b * c) / (1 - c * c)); }
    var t = { n: x1.length, r12: r12, r13: r13, r23: r23 };
    t.r12_3 = partial(r12, r13, r23);
    t.r13_2 = partial(r13, r12, r23);
    t.r23_1 = partial(r23, r12, r13);
    t.R1_23 = multiple(r12, r13, r23);
    t.R2_13 = multiple(r12, r23, r13);
    t.R3_12 = multiple(r13, r23, r12);
    var reg = S.regress2(x1, x2, x3);
    t.plane = reg;
    return t;
  };

  /* ------------------------------------------------------------------ */
  /* Small linear algebra                                                */
  /* ------------------------------------------------------------------ */

  function invertMatrix(A) {
    var n = A.length, M = A.map(function (row, i) {
      return row.concat(A.map(function (_, j) { return i === j ? 1 : 0; }));
    });
    for (var c = 0; c < n; c++) {
      var p = c;
      for (var r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      if (Math.abs(M[p][c]) < 1e-14) return null;
      var tmp = M[c]; M[c] = M[p]; M[p] = tmp;
      var pv = M[c][c];
      for (var k = 0; k < 2 * n; k++) M[c][k] /= pv;
      for (r = 0; r < n; r++) {
        if (r === c) continue;
        var f = M[r][c];
        for (k = 0; k < 2 * n; k++) M[r][k] -= f * M[c][k];
      }
    }
    return M.map(function (row) { return row.slice(n); });
  }
  S.invertMatrix = invertMatrix;

  /* ------------------------------------------------------------------ */
  /* Regression                                                          */
  /* ------------------------------------------------------------------ */

  /* y = a + b x, with the ANOVA, t tests and confidence intervals. */
  S.regress1 = function (y, x, alpha) {
    alpha = alpha || 0.05;
    var b = S.bivariate(x, y), n = x.length, df = n - 2;
    var r = { n: n, a: b.ayx, b: b.byx, r: b.r, r2: b.r2, df: df, sxx: b.sxx, syy: b.syy, sxy: b.sxy, mx: b.mx, my: b.my };
    r.ssr = b.byx * b.sxy; r.sse = b.syy - r.ssr; r.sst = b.syy;
    r.mse = r.sse / df; r.se = Math.sqrt(r.mse);
    r.seB = Math.sqrt(r.mse / b.sxx);
    r.seA = Math.sqrt(r.mse * (1 / n + b.mx * b.mx / b.sxx));
    r.tB = r.b / r.seB; r.tA = r.a / r.seA;
    r.pB = Math.min(1, 2 * S.tSf(Math.abs(r.tB), df));
    r.pA = Math.min(1, 2 * S.tSf(Math.abs(r.tA), df));
    r.F = r.ssr / r.mse; r.pF = S.fSf(r.F, 1, df);
    var tc = S.tInv(1 - alpha / 2, df);
    r.tCrit = tc;
    r.ciB = [r.b - tc * r.seB, r.b + tc * r.seB];
    r.ciA = [r.a - tc * r.seA, r.a + tc * r.seA];
    r.fCrit = S.fInv(1 - alpha, 1, df);
    r.alpha = alpha;
    return r;
  };

  /* y = b0 + b1 x1 + b2 x2. */
  S.regress2 = function (y, x1, x2, alpha) {
    alpha = alpha || 0.05;
    var n = y.length, X = [], i, j, k;
    for (i = 0; i < n; i++) X.push([1, x1[i], x2[i]]);
    var XtX = [[0, 0, 0], [0, 0, 0], [0, 0, 0]], Xty = [0, 0, 0];
    for (i = 0; i < n; i++) for (j = 0; j < 3; j++) {
      Xty[j] += X[i][j] * y[i];
      for (k = 0; k < 3; k++) XtX[j][k] += X[i][j] * X[i][k];
    }
    var inv = invertMatrix(XtX);
    if (!inv) return null;
    var beta = [0, 0, 0];
    for (j = 0; j < 3; j++) for (k = 0; k < 3; k++) beta[j] += inv[j][k] * Xty[k];
    var my = mean(y), sse = 0, sst = 0;
    for (i = 0; i < n; i++) {
      var fit = beta[0] + beta[1] * x1[i] + beta[2] * x2[i];
      sse += (y[i] - fit) * (y[i] - fit); sst += (y[i] - my) * (y[i] - my);
    }
    var df = n - 3, r = { n: n, b: beta, sse: sse, sst: sst, ssr: sst - sse, df: df, alpha: alpha };
    r.r2 = 1 - sse / sst; r.adjR2 = 1 - (1 - r.r2) * (n - 1) / df;
    r.mse = sse / df; r.msr = r.ssr / 2;
    r.F = r.msr / r.mse; r.pF = S.fSf(r.F, 2, df); r.fCrit = S.fInv(1 - alpha, 2, df);
    var tc = S.tInv(1 - alpha / 2, df);
    r.tCrit = tc;
    r.se = beta.map(function (_, j) { return Math.sqrt(r.mse * inv[j][j]); });
    r.t = beta.map(function (b, j) { return b / r.se[j]; });
    r.p = r.t.map(function (t) { return Math.min(1, 2 * S.tSf(Math.abs(t), df)); });
    r.ci = beta.map(function (b, j) { return [b - tc * r.se[j], b + tc * r.se[j]]; });
    return r;
  };

  /* ------------------------------------------------------------------ */
  /* Tests of means and variances                                        */
  /* ------------------------------------------------------------------ */

  function zCrit(alpha, alt) {
    return alt === 'two' ? [S.normInv(alpha / 2), S.normInv(1 - alpha / 2)]
      : alt === 'less' ? [S.normInv(alpha)] : [S.normInv(1 - alpha)];
  }
  function tCrit(alpha, alt, df) {
    return alt === 'two' ? [S.tInv(alpha / 2, df), S.tInv(1 - alpha / 2, df)]
      : alt === 'less' ? [S.tInv(alpha, df)] : [S.tInv(1 - alpha, df)];
  }
  function chiCrit(alpha, alt, df) {
    return alt === 'two' ? [S.chi2Inv(alpha / 2, df), S.chi2Inv(1 - alpha / 2, df)]
      : alt === 'less' ? [S.chi2Inv(alpha, df)] : [S.chi2Inv(1 - alpha, df)];
  }
  function fCrit(alpha, alt, d1, d2) {
    return alt === 'two' ? [S.fInv(alpha / 2, d1, d2), S.fInv(1 - alpha / 2, d1, d2)]
      : alt === 'less' ? [S.fInv(alpha, d1, d2)] : [S.fInv(1 - alpha, d1, d2)];
  }
  function zP(z, alt) { return pvalueSym(z, S.normCdf, S.normSf, alt); }
  function tP(t, df, alt) {
    return pvalueSym(t, function (v) { return S.tCdf(v, df); }, function (v) { return S.tSf(v, df); }, alt);
  }

  /* One-sample z test, sigma known. */
  S.z1 = function (x, mu0, sigma, alpha, alt) {
    var n = x.length, m = mean(x), se = sigma / Math.sqrt(n), z = (m - mu0) / se, zc = S.normInv(1 - alpha / 2);
    var p = zP(z, alt);
    return { n: n, mean: m, se: se, stat: z, p: p, crit: zCrit(alpha, alt), reject: decide(p, alpha),
             ci: [m - zc * se, m + zc * se], zHalf: zc };
  };

  /* One-sample t test. */
  S.t1 = function (x, mu0, alpha, alt) {
    var d = S.describe(x), n = d.n, df = n - 1, se = d.sd / Math.sqrt(n), t = (d.mean - mu0) / se;
    var p = tP(t, df, alt), tc = S.tInv(1 - alpha / 2, df);
    return { n: n, mean: d.mean, s: d.sd, se: se, df: df, stat: t, p: p, crit: tCrit(alpha, alt, df),
             reject: decide(p, alpha), ci: [d.mean - tc * se, d.mean + tc * se], tHalf: tc };
  };

  /* Chi-square test for a variance. */
  S.chiVar = function (x, s0sq, alpha, alt) {
    var d = S.describe(x), df = d.n - 1, chi = df * d.var / s0sq;
    var p = pvalueTwoTail(chi, function (v) { return S.chi2Cdf(v, df); }, function (v) { return S.chi2Sf(v, df); }, alt);
    var lo = S.chi2Inv(alpha / 2, df), hi = S.chi2Inv(1 - alpha / 2, df);
    return { n: d.n, s2: d.var, df: df, stat: chi, p: p, crit: chiCrit(alpha, alt, df), reject: decide(p, alpha),
             ci: [df * d.var / hi, df * d.var / lo], chiLo: lo, chiHi: hi };
  };

  /* Two-sample z test, sigmas known. */
  S.z2 = function (x, y, s1, s2, d0, alpha, alt) {
    var n1 = x.length, n2 = y.length, m1 = mean(x), m2 = mean(y);
    var se = Math.sqrt(s1 * s1 / n1 + s2 * s2 / n2), z = (m1 - m2 - d0) / se, zc = S.normInv(1 - alpha / 2);
    var p = zP(z, alt);
    return { n1: n1, n2: n2, m1: m1, m2: m2, se: se, stat: z, p: p, crit: zCrit(alpha, alt), reject: decide(p, alpha),
             ci: [m1 - m2 - zc * se, m1 - m2 + zc * se], zHalf: zc };
  };

  /* Two-sample t test with a pooled variance. */
  S.t2pooled = function (x, y, d0, alpha, alt) {
    var a = S.describe(x), b = S.describe(y), df = a.n + b.n - 2;
    var sp2 = ((a.n - 1) * a.var + (b.n - 1) * b.var) / df;
    var se = Math.sqrt(sp2 * (1 / a.n + 1 / b.n)), t = (a.mean - b.mean - d0) / se;
    var p = tP(t, df, alt), tc = S.tInv(1 - alpha / 2, df);
    return { n1: a.n, n2: b.n, m1: a.mean, m2: b.mean, s1sq: a.var, s2sq: b.var, sp2: sp2, se: se, df: df,
             stat: t, p: p, crit: tCrit(alpha, alt, df), reject: decide(p, alpha),
             ci: [a.mean - b.mean - tc * se, a.mean - b.mean + tc * se], tHalf: tc };
  };

  /* Welch's t test (unequal variances), Welch-Satterthwaite degrees of freedom. */
  S.t2welch = function (x, y, d0, alpha, alt) {
    var a = S.describe(x), b = S.describe(y), v1 = a.var / a.n, v2 = b.var / b.n;
    var se = Math.sqrt(v1 + v2), t = (a.mean - b.mean - d0) / se;
    var df = (v1 + v2) * (v1 + v2) / (v1 * v1 / (a.n - 1) + v2 * v2 / (b.n - 1));
    var p = tP(t, df, alt), tc = S.tInv(1 - alpha / 2, df);
    return { n1: a.n, n2: b.n, m1: a.mean, m2: b.mean, s1sq: a.var, s2sq: b.var, se: se, df: df,
             stat: t, p: p, crit: tCrit(alpha, alt, df), reject: decide(p, alpha),
             ci: [a.mean - b.mean - tc * se, a.mean - b.mean + tc * se], tHalf: tc };
  };

  /* Paired t test on d = x - y. */
  S.tpaired = function (x, y, d0, alpha, alt) {
    var d = x.map(function (v, i) { return v - y[i]; });
    var r = S.t1(d, d0, alpha, alt);
    r.d = d; r.dbar = r.mean; r.sd = r.s;
    return r;
  };

  /* F test for two variances, F = s1^2 / s2^2. */
  S.fVar = function (x, y, alpha, alt) {
    var a = S.describe(x), b = S.describe(y), d1 = a.n - 1, d2 = b.n - 1, F = a.var / b.var;
    var p = pvalueTwoTail(F, function (v) { return S.fCdf(v, d1, d2); }, function (v) { return S.fSf(v, d1, d2); }, alt);
    var lo = S.fInv(alpha / 2, d1, d2), hi = S.fInv(1 - alpha / 2, d1, d2);
    return { n1: a.n, n2: b.n, s1sq: a.var, s2sq: b.var, df1: d1, df2: d2, stat: F, p: p,
             crit: fCrit(alpha, alt, d1, d2), reject: decide(p, alpha), ci: [F / hi, F / lo], fLo: lo, fHi: hi };
  };

  /* ------------------------------------------------------------------ */
  /* Analysis of variance                                                */
  /* ------------------------------------------------------------------ */

  S.anova1 = function (groups, alpha) {
    var k = groups.length, all = [].concat.apply([], groups), N = all.length, G = mean(all);
    var info = groups.map(function (g) { var d = S.describe(g); return { n: d.n, mean: d.mean, var: d.var, sum: d.sum }; });
    var ssb = 0, ssw = 0, sst = ss(all, G);
    groups.forEach(function (g, i) {
      ssb += g.length * Math.pow(info[i].mean - G, 2);
      ssw += ss(g, info[i].mean);
    });
    var dfb = k - 1, dfw = N - k, msb = ssb / dfb, msw = ssw / dfw, F = msb / msw;
    var r = { k: k, N: N, grand: G, groups: info, ssb: ssb, ssw: ssw, sst: sst, dfb: dfb, dfw: dfw,
              msb: msb, msw: msw, stat: F, p: S.fSf(F, dfb, dfw), crit: [S.fInv(1 - alpha, dfb, dfw)], alpha: alpha };
    r.reject = decide(r.p, alpha);
    var tc = S.tInv(1 - alpha / 2, dfw);
    r.tHalf = tc;
    r.pairs = [];
    for (var i = 0; i < k; i++) for (var j = i + 1; j < k; j++) {
      var cd = tc * Math.sqrt(msw * (1 / info[i].n + 1 / info[j].n));
      var diff = Math.abs(info[i].mean - info[j].mean);
      r.pairs.push({ i: i, j: j, diff: diff, cd: cd, significant: diff > cd });
    }
    r.cf = Math.pow(sum(all), 2) / N;
    return r;
  };

  S.bartlett = function (groups, alpha) {
    var k = groups.length, info = groups.map(function (g) { return S.describe(g); });
    var N = 0, num = 0, inv = 0;
    info.forEach(function (d) { N += d.n; num += (d.n - 1) * d.var; inv += 1 / (d.n - 1); });
    var sp2 = num / (N - k), lnSum = 0;
    info.forEach(function (d) { lnSum += (d.n - 1) * Math.log(d.var); });
    var top = (N - k) * Math.log(sp2) - lnSum;
    var C = 1 + (inv - 1 / (N - k)) / (3 * (k - 1));
    var chi = top / C, df = k - 1, p = S.chi2Sf(chi, df);
    return { k: k, N: N, sp2: sp2, vars: info.map(function (d) { return d.var; }), ns: info.map(function (d) { return d.n; }),
             top: top, C: C, stat: chi, df: df, p: p, crit: [S.chi2Inv(1 - alpha, df)], reject: decide(p, alpha) };
  };

  /* ------------------------------------------------------------------ */
  /* Correlation tests                                                   */
  /* ------------------------------------------------------------------ */

  S.rZero = function (x, y, alpha, alt) {
    var b = S.bivariate(x, y), n = b.n, df = n - 2, t = b.r * Math.sqrt(df) / Math.sqrt(1 - b.r2);
    var p = tP(t, df, alt);
    return { n: n, r: b.r, df: df, stat: t, p: p, crit: tCrit(alpha, alt, df), reject: decide(p, alpha) };
  };

  S.rFisher = function (x, y, rho0, alpha, alt) {
    var b = S.bivariate(x, y), n = b.n, z = Math.atanh(b.r), z0 = Math.atanh(rho0), se = 1 / Math.sqrt(n - 3);
    var stat = (z - z0) / se, p = zP(stat, alt), zc = S.normInv(1 - alpha / 2);
    return { n: n, r: b.r, z: z, z0: z0, se: se, stat: stat, p: p, crit: zCrit(alpha, alt), reject: decide(p, alpha),
             ciZ: [z - zc * se, z + zc * se], ci: [Math.tanh(z - zc * se), Math.tanh(z + zc * se)], zHalf: zc };
  };

  /* Partial correlation of variables 1 and 2 with 3 held fixed. */
  S.partialTest = function (x1, x2, x3, alpha, alt) {
    var t3 = S.trivariate(x1, x2, x3), r = t3.r12_3, n = x1.length, df = n - 3;
    var t = r * Math.sqrt(df) / Math.sqrt(1 - r * r), p = tP(t, df, alt);
    return { n: n, r: r, r12: t3.r12, r13: t3.r13, r23: t3.r23, df: df, stat: t, p: p,
             crit: tCrit(alpha, alt, df), reject: decide(p, alpha) };
  };

  /* Multiple correlation of variable 1 on 2 and 3. */
  S.multipleTest = function (x1, x2, x3, alpha) {
    var t3 = S.trivariate(x1, x2, x3), R = t3.R1_23, n = x1.length, R2 = R * R;
    var F = (R2 / 2) / ((1 - R2) / (n - 3)), p = S.fSf(F, 2, n - 3);
    return { n: n, R: R, R2: R2, r12: t3.r12, r13: t3.r13, r23: t3.r23, df1: 2, df2: n - 3, stat: F, p: p,
             crit: [S.fInv(1 - alpha, 2, n - 3)], reject: decide(p, alpha) };
  };

  /* ------------------------------------------------------------------ */
  /* Non-parametric tests                                                */
  /* ------------------------------------------------------------------ */

  function binomCdf(k, n, p) {
    var s = 0;
    for (var i = 0; i <= k; i++) s += Math.exp(lchoose(n, i) + i * Math.log(p) + (n - i) * Math.log(1 - p));
    return Math.min(1, s);
  }
  S.binomCdf = binomCdf;

  /* Sign test that the median is m0 (alt 'greater': median > m0). */
  S.signTest = function (x, m0, alpha, alt) {
    var plus = 0, minus = 0;
    x.forEach(function (v) { if (v > m0) plus++; else if (v < m0) minus++; });
    var n = plus + minus, lower = binomCdf(plus, n, 0.5), upper = 1 - binomCdf(plus - 1, n, 0.5);
    var p = alt === 'less' ? lower : alt === 'greater' ? upper : Math.min(1, 2 * Math.min(lower, upper));
    return { n: n, plus: plus, minus: minus, zeros: x.length - n, stat: plus, p: p, reject: decide(p, alpha),
             method: 'exact binomial' };
  };

  /* Exact null distribution of the signed-rank sum T+ for n untied ranks. */
  function signedRankCounts(n) {
    var max = n * (n + 1) / 2, c = new Array(max + 1).fill(0);
    c[0] = 1;
    for (var k = 1; k <= n; k++) for (var s = k * (k + 1) / 2; s >= k; s--) c[s] += c[s - k];
    return c;
  }

  /* Wilcoxon signed-rank test that the median of x is m0. */
  S.wilcoxon = function (x, m0, alpha, alt) {
    var d = [];
    x.forEach(function (v) { if (v !== m0) d.push(v - m0); });
    var n = d.length, rk = S.ranks(d.map(Math.abs)), tp = 0, tm = 0;
    d.forEach(function (v, i) { if (v > 0) tp += rk.ranks[i]; else tm += rk.ranks[i]; });
    var r = { n: n, zeros: x.length - n, tPlus: tp, tMinus: tm, stat: tp, ties: rk.ties, ranks: rk.ranks, d: d };
    if (n === 0) { r.p = 1; r.reject = false; r.method = 'no non-zero differences'; return r; }
    if (rk.ties.length === 0 && n <= 50) {
      var c = signedRankCounts(n), total = Math.pow(2, n), lower = 0, upper = 0;
      for (var s = 0; s < c.length; s++) { if (s <= tp) lower += c[s]; if (s >= tp) upper += c[s]; }
      lower /= total; upper /= total;
      r.p = alt === 'less' ? lower : alt === 'greater' ? upper : Math.min(1, 2 * Math.min(lower, upper));
      r.method = 'exact';
    } else {
      var mu = n * (n + 1) / 4, tie = 0;
      rk.ties.forEach(function (t) { tie += t * t * t - t; });
      var v = n * (n + 1) * (2 * n + 1) / 24 - tie / 48, sd = Math.sqrt(v), diff = tp - mu;
      var cc = alt === 'two' ? (diff > 0 ? 0.5 : diff < 0 ? -0.5 : 0) : alt === 'greater' ? 0.5 : -0.5;
      var z = (diff - cc) / sd;
      r.mu = mu; r.var = v; r.z = z;
      r.p = alt === 'less' ? S.normCdf(z) : alt === 'greater' ? S.normSf(z) : Math.min(1, 2 * S.normSf(Math.abs(z)));
      r.method = 'normal approximation';
    }
    r.reject = decide(r.p, alpha);
    return r;
  };

  /* Exact distribution of U for sizes m, n (no ties): counts of each U. */
  function mwCounts(m, n) {
    var layers = [], a, b, u;
    for (a = 0; a <= m; a++) layers.push([1]);               // b = 0: only U = 0
    for (b = 1; b <= n; b++) {
      var next = [[1]];                                    // a = 0
      for (a = 1; a <= m; a++) {
        var len = a * b + 1, row = new Array(len).fill(0), up = next[a - 1], left = layers[a];
        // c(a, b, u) = c(a-1, b, u - b) + c(a, b-1, u)
        for (u = 0; u < len; u++) {
          if (u - b >= 0 && u - b < up.length) row[u] += up[u - b];
          if (u < left.length) row[u] += left[u];
        }
        next.push(row);
      }
      layers = next;
    }
    return layers[m];
  }
  S.mwCounts = mwCounts;

  /* Mann-Whitney U test. alt 'greater': x tends to be larger than y. */
  S.mannWhitney = function (x, y, alpha, alt) {
    var n1 = x.length, n2 = y.length, all = x.concat(y), rk = S.ranks(all), R1 = 0, R2 = 0;
    for (var i = 0; i < n1 + n2; i++) { if (i < n1) R1 += rk.ranks[i]; else R2 += rk.ranks[i]; }
    var U1 = R1 - n1 * (n1 + 1) / 2, U2 = n1 * n2 - U1;
    var r = { n1: n1, n2: n2, R1: R1, R2: R2, U1: U1, U2: U2, stat: U1, ties: rk.ties };
    if (rk.ties.length === 0 && n1 <= 20 && n2 <= 20) {
      var c = mwCounts(n1, n2), total = Math.exp(lchoose(n1 + n2, n1)), lower = 0, upper = 0;
      for (var u = 0; u < c.length; u++) { if (u <= U1) lower += c[u]; if (u >= U1) upper += c[u]; }
      lower /= total; upper /= total;
      r.p = alt === 'less' ? lower : alt === 'greater' ? upper : Math.min(1, 2 * Math.min(lower, upper));
      r.method = 'exact';
    } else {
      var N = n1 + n2, tie = 0;
      rk.ties.forEach(function (t) { tie += t * t * t - t; });
      var mu = n1 * n2 / 2, v = n1 * n2 / 12 * ((N + 1) - tie / (N * (N - 1))), sd = Math.sqrt(v), diff = U1 - mu;
      var cc = alt === 'two' ? (diff > 0 ? 0.5 : diff < 0 ? -0.5 : 0) : alt === 'greater' ? 0.5 : -0.5;
      var z = (diff - cc) / sd;
      r.mu = mu; r.var = v; r.z = z;
      r.p = alt === 'less' ? S.normCdf(z) : alt === 'greater' ? S.normSf(z) : Math.min(1, 2 * S.normSf(Math.abs(z)));
      r.method = 'normal approximation';
    }
    r.reject = decide(r.p, alpha);
    return r;
  };

  S.kruskal = function (groups, alpha) {
    var all = [].concat.apply([], groups), N = all.length, rk = S.ranks(all), pos = 0, H = 0;
    var R = groups.map(function (g) {
      var s = 0; for (var i = 0; i < g.length; i++) s += rk.ranks[pos + i];
      pos += g.length; return s;
    });
    groups.forEach(function (g, i) { H += R[i] * R[i] / g.length; });
    H = 12 / (N * (N + 1)) * H - 3 * (N + 1);
    var tie = 0;
    rk.ties.forEach(function (t) { tie += t * t * t - t; });
    var C = 1 - tie / (N * N * N - N), Hc = H / C, df = groups.length - 1, p = S.chi2Sf(Hc, df);
    return { N: N, R: R, ns: groups.map(function (g) { return g.length; }), H: H, C: C, stat: Hc, df: df, p: p,
             crit: [S.chi2Inv(1 - alpha, df)], reject: decide(p, alpha) };
  };

  /* Probability of exactly r runs of n1 symbols of one kind and n2 of the other. */
  function runsProb(r, n1, n2) {
    var N = n1 + n2, lt = lchoose(N, n1), k;
    if (r % 2 === 0) {
      k = r / 2;
      return 2 * Math.exp(lchoose(n1 - 1, k - 1) + lchoose(n2 - 1, k - 1) - lt);
    }
    k = (r - 1) / 2;
    return Math.exp(lchoose(n1 - 1, k - 1) + lchoose(n2 - 1, k) - lt) +
           Math.exp(lchoose(n1 - 1, k) + lchoose(n2 - 1, k - 1) - lt);
  }
  S.runsProb = runsProb;

  /* Runs test for randomness: values above (+) and below (-) the median, in
     the order entered; values equal to the median are left out.
     alt 'less': too few runs (clustering or trend); 'greater': too many. */
  S.runsTest = function (x, alpha, alt) {
    var med = S.describe(x).median, seq = [];
    x.forEach(function (v) { if (v > med) seq.push('+'); else if (v < med) seq.push('-'); });
    var n1 = seq.filter(function (c) { return c === '+'; }).length, n2 = seq.length - n1, R = seq.length ? 1 : 0;
    for (var i = 1; i < seq.length; i++) if (seq[i] !== seq[i - 1]) R++;
    var r = { median: med, seq: seq.join(''), n1: n1, n2: n2, stat: R, dropped: x.length - seq.length };
    if (n1 === 0 || n2 === 0) { r.p = 1; r.reject = false; r.method = 'not possible'; return r; }
    if (n1 <= 20 && n2 <= 20) {
      var lower = 0, upper = 0, rmax = 2 * Math.min(n1, n2) + (n1 === n2 ? 0 : 1);
      for (var k = 2; k <= rmax; k++) { var pr = runsProb(k, n1, n2); if (k <= R) lower += pr; if (k >= R) upper += pr; }
      r.p = alt === 'less' ? lower : alt === 'greater' ? upper : Math.min(1, 2 * Math.min(lower, upper));
      r.method = 'exact';
    } else {
      var N = n1 + n2, mu = 2 * n1 * n2 / N + 1, v = 2 * n1 * n2 * (2 * n1 * n2 - N) / (N * N * (N - 1));
      var diff = R - mu, cc = alt === 'two' ? (diff > 0 ? 0.5 : diff < 0 ? -0.5 : 0) : alt === 'greater' ? 0.5 : -0.5;
      var z = (diff - cc) / Math.sqrt(v);
      r.mu = mu; r.var = v; r.z = z;
      r.p = alt === 'less' ? S.normCdf(z) : alt === 'greater' ? S.normSf(z) : Math.min(1, 2 * S.normSf(Math.abs(z)));
      r.method = 'normal approximation';
    }
    r.reject = decide(r.p, alpha);
    return r;
  };

  /* ------------------------------------------------------------------ */
  /* Kolmogorov-Smirnov                                                  */
  /* ------------------------------------------------------------------ */

  /* P(D_n < d), Marsaglia, Tsang and Wang (2003), "Evaluating
     Kolmogorov's distribution", J. Statistical Software 8(18). */
  S.kolmogorovCdf = function (n, d) {
    if (d <= 0) return 0;
    if (d >= 1) return 1;
    // Far in the tail (P(D >= d) below about 1e-6) the authors' quick
    // approximation is used; it is accurate there and avoids a large matrix.
    if (n * d * d > 7.24) return 1 - 2 * Math.exp(-(2.000071 + 0.331 / Math.sqrt(n) + 1.409 / n) * n * d * d);
    var k = Math.floor(n * d) + 1, m = 2 * k - 1, h = k - n * d, i, j, g;
    var H = new Float64Array(m * m);
    for (i = 0; i < m; i++) for (j = 0; j < m; j++) H[i * m + j] = (i - j + 1 < 0) ? 0 : 1;
    for (i = 0; i < m; i++) {
      H[i * m] -= Math.pow(h, i + 1);
      H[(m - 1) * m + i] -= Math.pow(h, m - i);
    }
    H[(m - 1) * m] += (2 * h - 1 > 0 ? Math.pow(2 * h - 1, m) : 0);
    for (i = 0; i < m; i++) for (j = 0; j < m; j++) if (i - j + 1 > 0) for (g = 1; g <= i - j + 1; g++) H[i * m + j] /= g;
    function mult(A, B) {
      var C = new Float64Array(m * m);
      for (var a = 0; a < m; a++) for (var c = 0; c < m; c++) {
        var av = A[a * m + c];
        if (av === 0) continue;
        for (var b = 0; b < m; b++) C[a * m + b] += av * B[c * m + b];
      }
      return C;
    }
    function power(A, eA, nn) {
      if (nn === 1) return { M: A, e: eA };
      var half = power(A, eA, Math.floor(nn / 2)), V = mult(half.M, half.M), eV = 2 * half.e;
      if (nn % 2 === 1) { V = mult(A, V); eV += eA; }
      if (V[Math.floor(m / 2) * m + Math.floor(m / 2)] > 1e140) {
        for (var q = 0; q < m * m; q++) V[q] *= 1e-140;
        eV += 140;
      }
      return { M: V, e: eV };
    }
    var P = power(H, 0, n), s = P.M[(k - 1) * m + k - 1], eQ = P.e;
    for (i = 1; i <= n; i++) {
      s = s * i / n;
      if (s < 1e-140) { s *= 1e140; eQ -= 140; }
    }
    return s * Math.pow(10, eQ);
  };

  /* One-sample K-S test against a fully specified continuous cdf. */
  S.ksTest = function (x, cdf) {
    var s = sorted(x), n = s.length, D = 0, dPlus = 0, dMinus = 0;
    for (var i = 0; i < n; i++) {
      var F = cdf(s[i]);
      dPlus = Math.max(dPlus, (i + 1) / n - F);
      dMinus = Math.max(dMinus, F - i / n);
    }
    D = Math.max(dPlus, dMinus);
    var p = Math.max(0, Math.min(1, 1 - S.kolmogorovCdf(n, D)));
    return { n: n, D: D, p: p };
  };

  /* ------------------------------------------------------------------ */
  /* Distributions for comparing a sample                                */
  /* ------------------------------------------------------------------ */

  function isInt(v) { return Math.abs(v - Math.round(v)) < 1e-9; }

  /* Newton's method on a function of one variable, with a bracket kept so
     that a bad step falls back to bisection. f must change sign on [lo, hi]. */
  function solve1(f, df, lo, hi, x0) {
    var flo = f(lo), x = x0 === undefined ? (lo + hi) / 2 : x0;
    for (var i = 0; i < 200; i++) {
      var fx = f(x);
      if (fx === 0) return x;
      if ((fx < 0) === (flo < 0)) { lo = x; flo = fx; } else hi = x;
      var step = df ? fx / df(x) : NaN, nx = x - step;
      if (!(nx > lo && nx < hi) || !isFinite(nx)) nx = (lo + hi) / 2;
      if (Math.abs(nx - x) <= 1e-15 * Math.max(1, Math.abs(x))) return nx;
      x = nx;
    }
    return x;
  }
  /* A bracket [lo, hi] around a sign change of f, growing outward from start. */
  function bracketUp(f, lo, start) {
    var hi = start;
    for (var i = 0; i < 2000 && (f(lo) < 0) === (f(hi) < 0); i++) hi *= 2;
    return hi;
  }

  /* Maximise a smooth function of a positive parameter by golden section on
     its logarithm, between lo and hi. */
  function maximiseLog(f, lo, hi) {
    var a = Math.log(lo), b = Math.log(hi), gr = (Math.sqrt(5) - 1) / 2;
    var c = b - gr * (b - a), d = a + gr * (b - a), fc = f(Math.exp(c)), fd = f(Math.exp(d));
    for (var i = 0; i < 300; i++) {
      if (fc > fd) { b = d; d = c; fd = fc; c = b - gr * (b - a); fc = f(Math.exp(c)); }
      else { a = c; c = d; fc = fd; d = a + gr * (b - a); fd = f(Math.exp(d)); }
      if (Math.abs(b - a) < 1e-13) break;
    }
    return Math.exp((a + b) / 2);
  }

  /* Two-parameter Newton for a likelihood: grad and hess are functions of
     the parameter vector; keep keeps it in range by halving the step. */
  function newton2(p, grad, hess, keep) {
    for (var it = 0; it < 500; it++) {
      var g = grad(p), H = hess(p), det = H[0][0] * H[1][1] - H[0][1] * H[1][0];
      if (!isFinite(det) || det === 0) break;
      var s0 = (H[1][1] * g[0] - H[0][1] * g[1]) / det, s1 = (H[0][0] * g[1] - H[1][0] * g[0]) / det;
      var t = 1, np;
      for (var h = 0; h < 60; h++) {
        np = [p[0] - t * s0, p[1] - t * s1];
        if (keep(np)) break;
        t /= 2;
      }
      var moved = Math.abs(np[0] - p[0]) + Math.abs(np[1] - p[1]);
      p = np;
      if (moved < 1e-14 * (1 + Math.abs(p[0]) + Math.abs(p[1]))) break;
    }
    return p;
  }

  function lnPoissonPmf(k, l) { return k * Math.log(l) - l - lgamma(k + 1); }

  /* Each entry: key, name, kind, number of parameters, applicability check,
     moment and maximum-likelihood estimates, log pdf/pmf and cdf. */
  var DIST = {};

  DIST.degenerate = {
    name: 'Degenerate', kind: 'discrete', k: 1, names: ['c'],
    applies: function (x, d) { return d.min === d.max ? '' : 'the values are not all equal, and a degenerate variable takes one value only'; },
    mle: function (x, d) { return [d.min]; }, mom: function (x, d) { return [d.mean]; },
    logpmf: function (v, p) { return v === p[0] ? 0 : -Infinity; },
    cdf: function (v, p) { return v >= p[0] ? 1 : 0; }, support: function (p) { return [p[0], p[0]]; }
  };
  DIST.bernoulli = {
    name: 'Bernoulli', kind: 'discrete', k: 1, names: ['p'],
    applies: function (x) { return x.every(function (v) { return v === 0 || v === 1; }) ? '' : 'the values are not all 0 or 1'; },
    mle: function (x, d) { return [d.mean]; }, mom: function (x, d) { return [d.mean]; },
    logpmf: function (v, p) { return v === 1 ? Math.log(p[0]) : v === 0 ? Math.log(1 - p[0]) : -Infinity; },
    cdf: function (v, p) { return v < 0 ? 0 : v < 1 ? 1 - p[0] : 1; }, support: function () { return [0, 1]; }
  };
  DIST.binomial = {
    name: 'Binomial', kind: 'discrete', k: 1, names: ['p'], fixed: ['n'],
    applies: function (x, d, o) {
      var n = o.binomN || d.max;
      if (!x.every(function (v) { return isInt(v) && v >= 0 && v <= n; })) return 'the values are not all whole numbers from 0 to n = ' + n;
      return '';
    },
    mle: function (x, d, o) { var n = o.binomN || d.max; return [d.mean / n, n]; },
    mom: function (x, d, o) { var n = o.binomN || d.max; return [d.mean / n, n]; },
    logpmf: function (v, p) { var n = p[1]; return lchoose(n, v) + v * Math.log(p[0]) + (n - v) * Math.log(1 - p[0]); },
    cdf: function (v, p) { return v < 0 ? 0 : v >= p[1] ? 1 : binomCdf(Math.floor(v), p[1], p[0]); },
    support: function (p) { return [0, p[1]]; }
  };
  DIST.poisson = {
    name: 'Poisson', kind: 'discrete', k: 1, names: ['λ'],
    applies: function (x) { return x.every(function (v) { return isInt(v) && v >= 0; }) ? '' : 'the values are not all whole numbers 0, 1, 2, …'; },
    mle: function (x, d) { return [d.mean]; }, mom: function (x, d) { return [d.mean]; },
    logpmf: function (v, p) { return lnPoissonPmf(v, p[0]); },
    cdf: function (v, p) { return v < 0 ? 0 : S.gammaQ(Math.floor(v) + 1, p[0]); },
    support: function () { return [0, Infinity]; }
  };
  DIST.geometric = {
    name: 'Geometric', kind: 'discrete', k: 1, names: ['p'],
    applies: DIST.poisson.applies,
    mle: function (x, d) { return [1 / (1 + d.mean)]; }, mom: function (x, d) { return [1 / (1 + d.mean)]; },
    logpmf: function (v, p) { return v * Math.log(1 - p[0]) + Math.log(p[0]); },
    cdf: function (v, p) { return v < 0 ? 0 : 1 - Math.pow(1 - p[0], Math.floor(v) + 1); },
    support: function () { return [0, Infinity]; }
  };
  DIST.negbinomial = {
    name: 'Negative binomial', kind: 'discrete', k: 2, names: ['r', 'p'],
    applies: function (x, d) {
      var a = DIST.poisson.applies(x);
      if (a) return a;
      if (d.varN <= d.mean) return 'the variance (' + fmt(d.varN) + ') is not larger than the mean (' + fmt(d.mean) + '); the negative binomial needs variance > mean (it tends to the Poisson otherwise)';
      return '';
    },
    mom: function (x, d) { var r = d.mean * d.mean / (d.varN - d.mean); return [r, d.mean / d.varN]; },
    mle: function (x, d) {
      var n = x.length, m = d.mean;
      function ll(r) {
        var p = r / (r + m), s = 0;
        for (var i = 0; i < n; i++) s += lgamma(x[i] + r) - lgamma(r) - lgamma(x[i] + 1) + r * Math.log(p) + x[i] * Math.log(1 - p);
        return s;
      }
      function score(r) {
        var s = n * Math.log(r / (r + m));
        for (var i = 0; i < n; i++) s += S.digamma(x[i] + r) - S.digamma(r);
        return s;
      }
      var lo = 1e-8, hi = bracketUp(function (r) { return -score(r); }, lo, 1);
      var r = score(hi) < 0 ? solve1(score, null, lo, hi) : maximiseLog(ll, 1e-8, 1e8);
      return [r, r / (r + m)];
    },
    logpmf: function (v, p) { var r = p[0]; return lgamma(v + r) - lgamma(r) - lgamma(v + 1) + r * Math.log(p[1]) + v * Math.log(1 - p[1]); },
    cdf: function (v, p) { return v < 0 ? 0 : S.betaI(p[1], p[0], Math.floor(v) + 1); },
    support: function () { return [0, Infinity]; }
  };
  DIST.hypergeometric = {
    name: 'Hypergeometric', kind: 'discrete', k: 1, names: ['M'], fixed: ['N', 'n'],
    applies: function (x, d, o) {
      if (!(o.hyperN > 0 && o.hyperDraws > 0)) return 'enter the population size N and the number drawn n';
      if (o.hyperDraws > o.hyperN) return 'the number drawn n is larger than N';
      if (!x.every(function (v) { return isInt(v) && v >= 0 && v <= o.hyperDraws; })) return 'the values are not all whole numbers from 0 to n = ' + o.hyperDraws;
      return '';
    },
    mle: function (x, d, o) {
      var N = o.hyperN, nn = o.hyperDraws, best = null, bestL = -Infinity;
      var lo = d.max, hi = N - nn + d.min;
      for (var M = lo; M <= hi; M++) {
        var L = 0;
        for (var i = 0; i < x.length; i++) L += DIST.hypergeometric.logpmf(x[i], [M, N, nn]);
        if (L > bestL) { bestL = L; best = M; }
      }
      return [best, N, nn];
    },
    mom: function (x, d, o) { return [Math.round(o.hyperN * d.mean / o.hyperDraws), o.hyperN, o.hyperDraws]; },
    logpmf: function (v, p) { return lchoose(p[0], v) + lchoose(p[1] - p[0], p[2] - v) - lchoose(p[1], p[2]); },
    cdf: function (v, p) {
      var s = 0;
      for (var i = Math.max(0, p[2] - (p[1] - p[0])); i <= Math.floor(v); i++) s += Math.exp(DIST.hypergeometric.logpmf(i, p));
      return Math.min(1, s);
    },
    support: function (p) { return [Math.max(0, p[2] - (p[1] - p[0])), Math.min(p[0], p[2])]; }
  };
  DIST.duniform = {
    name: 'Discrete uniform', kind: 'discrete', k: 2, names: ['a', 'b'],
    applies: function (x) { return x.every(isInt) ? '' : 'the values are not all whole numbers'; },
    mle: function (x, d) { return [d.min, d.max]; },
    mom: function (x, d) {
      var w = Math.sqrt(12 * d.varN + 1);               // variance ((b-a+1)^2 - 1)/12
      return [Math.round(d.mean - (w - 1) / 2), Math.round(d.mean + (w - 1) / 2)];
    },
    logpmf: function (v, p) { return v >= p[0] && v <= p[1] ? -Math.log(p[1] - p[0] + 1) : -Infinity; },
    cdf: function (v, p) { return v < p[0] ? 0 : v >= p[1] ? 1 : (Math.floor(v) - p[0] + 1) / (p[1] - p[0] + 1); },
    support: function (p) { return [p[0], p[1]]; }
  };

  DIST.uniform = {
    name: 'Uniform (rectangular)', kind: 'continuous', k: 2, names: ['a', 'b'],
    applies: function (x, d) { return d.max > d.min ? '' : 'all the values are equal'; },
    mle: function (x, d) { return [d.min, d.max]; },
    mom: function (x, d) { return [d.mean - Math.sqrt(3) * d.sdN, d.mean + Math.sqrt(3) * d.sdN]; },
    logpdf: function (v, p) { return v >= p[0] && v <= p[1] ? -Math.log(p[1] - p[0]) : -Infinity; },
    cdf: function (v, p) { return v <= p[0] ? 0 : v >= p[1] ? 1 : (v - p[0]) / (p[1] - p[0]); }
  };
  DIST.normal = {
    name: 'Normal', kind: 'continuous', k: 2, names: ['μ', 'σ'],
    applies: function (x, d) { return d.sdN > 0 ? '' : 'all the values are equal'; },
    mle: function (x, d) { return [d.mean, d.sdN]; }, mom: function (x, d) { return [d.mean, d.sdN]; },
    logpdf: function (v, p) { var z = (v - p[0]) / p[1]; return -0.5 * z * z - LN_SQRT_2PI - Math.log(p[1]); },
    cdf: function (v, p) { return S.normCdf((v - p[0]) / p[1]); }
  };
  DIST.lognormal = {
    name: 'Lognormal', kind: 'continuous', k: 2, names: ['μ', 'σ'],
    applies: function (x, d) { return d.min > 0 ? (d.max > d.min ? '' : 'all the values are equal') : 'some values are not positive'; },
    mle: function (x) { var l = x.map(Math.log), m = mean(l); return [m, Math.sqrt(ss(l, m) / l.length)]; },
    mom: function (x, d) { var s2 = Math.log(1 + d.varN / (d.mean * d.mean)); return [Math.log(d.mean) - s2 / 2, Math.sqrt(s2)]; },
    logpdf: function (v, p) {
      if (v <= 0) return -Infinity;
      var z = (Math.log(v) - p[0]) / p[1]; return -0.5 * z * z - LN_SQRT_2PI - Math.log(p[1] * v);
    },
    cdf: function (v, p) { return v <= 0 ? 0 : S.normCdf((Math.log(v) - p[0]) / p[1]); }
  };
  DIST.exponential = {
    name: 'Exponential', kind: 'continuous', k: 1, names: ['λ'],
    applies: function (x, d) { return d.min >= 0 ? (d.mean > 0 ? '' : 'all the values are 0') : 'some values are negative'; },
    mle: function (x, d) { return [1 / d.mean]; }, mom: function (x, d) { return [1 / d.mean]; },
    logpdf: function (v, p) { return v < 0 ? -Infinity : Math.log(p[0]) - p[0] * v; },
    cdf: function (v, p) { return v <= 0 ? 0 : 1 - Math.exp(-p[0] * v); }
  };
  DIST.laplace = {
    name: 'Double exponential (Laplace)', kind: 'continuous', k: 2, names: ['μ', 'b'],
    applies: function (x, d) { return d.sdN > 0 ? '' : 'all the values are equal'; },
    mle: function (x, d) {
      var s = d.sorted, n = s.length, med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2, b = 0;
      x.forEach(function (v) { b += Math.abs(v - med); });
      return [med, b / n];
    },
    mom: function (x, d) { return [d.mean, d.sdN / Math.SQRT2]; },
    logpdf: function (v, p) { return -Math.log(2 * p[1]) - Math.abs(v - p[0]) / p[1]; },
    cdf: function (v, p) { return v < p[0] ? 0.5 * Math.exp((v - p[0]) / p[1]) : 1 - 0.5 * Math.exp(-(v - p[0]) / p[1]); }
  };
  DIST.gamma = {
    name: 'Gamma', kind: 'continuous', k: 2, names: ['α', 'λ'],
    applies: DIST.lognormal.applies,
    mom: function (x, d) { return [d.mean * d.mean / d.varN, d.mean / d.varN]; },
    mle: function (x, d) {
      var lm = mean(x.map(Math.log)), s = Math.log(d.mean) - lm;
      var f = function (a) { return Math.log(a) - S.digamma(a) - s; };
      var df = function (a) { return 1 / a - S.trigamma(a); };
      var a0 = (3 - s + Math.sqrt((s - 3) * (s - 3) + 24 * s)) / (12 * s);
      var lo = a0 / 2, hi = a0 * 2;
      while (f(lo) < 0) lo /= 2;
      while (f(hi) > 0) hi *= 2;
      var a = solve1(f, df, lo, hi, a0);
      return [a, a / d.mean];
    },
    logpdf: function (v, p) { return v <= 0 ? -Infinity : p[0] * Math.log(p[1]) - lgamma(p[0]) + (p[0] - 1) * Math.log(v) - p[1] * v; },
    cdf: function (v, p) { return v <= 0 ? 0 : S.gammaP(p[0], p[1] * v); }
  };
  function betaMle(l1, l2, start) {
    return newton2(start,
      function (p) { var t = S.digamma(p[0] + p[1]); return [S.digamma(p[0]) - t - l1, S.digamma(p[1]) - t - l2]; },
      function (p) { var t = S.trigamma(p[0] + p[1]); return [[S.trigamma(p[0]) - t, -t], [-t, S.trigamma(p[1]) - t]]; },
      function (p) { return p[0] > 0 && p[1] > 0; });
  }
  DIST.beta1 = {
    name: 'Beta of the first kind', kind: 'continuous', k: 2, names: ['α', 'β'],
    applies: function (x, d) { return d.min > 0 && d.max < 1 ? (d.max > d.min ? '' : 'all the values are equal') : 'the values are not all strictly between 0 and 1'; },
    mom: function (x, d) { var c = d.mean * (1 - d.mean) / d.varN - 1; return [d.mean * c, (1 - d.mean) * c]; },
    mle: function (x, d) {
      var l1 = mean(x.map(Math.log)), l2 = mean(x.map(function (v) { return Math.log(1 - v); }));
      var st = DIST.beta1.mom(x, d);
      if (!(st[0] > 0 && st[1] > 0)) st = [1, 1];
      return betaMle(l1, l2, st);
    },
    logpdf: function (v, p) { return v <= 0 || v >= 1 ? -Infinity : (p[0] - 1) * Math.log(v) + (p[1] - 1) * Math.log(1 - v) - S.lbeta(p[0], p[1]); },
    cdf: function (v, p) { return S.betaI(Math.min(1, Math.max(0, v)), p[0], p[1]); }
  };
  DIST.beta2 = {
    name: 'Beta of the second kind', kind: 'continuous', k: 2, names: ['α', 'β'],
    applies: DIST.lognormal.applies,
    mom: function (x, d) { var b = 2 + d.mean * (d.mean + 1) / d.varN; return [d.mean * (b - 1), b]; },
    mle: function (x, d) {
      // Y = X/(1+X) is beta of the first kind with the same parameters, and the
      // Jacobian does not involve them: the same likelihood equations.
      var y = x.map(function (v) { return v / (1 + v); });
      var l1 = mean(y.map(Math.log)), l2 = mean(y.map(function (v) { return Math.log(1 - v); }));
      var st = DIST.beta2.mom(x, d);
      if (!(st[0] > 0 && st[1] > 0)) st = [1, 1];
      return betaMle(l1, l2, st);
    },
    logpdf: function (v, p) { return v <= 0 ? -Infinity : (p[0] - 1) * Math.log(v) - (p[0] + p[1]) * Math.log(1 + v) - S.lbeta(p[0], p[1]); },
    cdf: function (v, p) { return v <= 0 ? 0 : S.betaI(v / (1 + v), p[0], p[1]); }
  };
  DIST.cauchy = {
    name: 'Cauchy', kind: 'continuous', k: 2, names: ['μ', 'λ'],
    applies: function (x, d) { return d.sdN > 0 ? '' : 'all the values are equal'; },
    momNote: 'The Cauchy distribution has no mean or variance, so its "moment" estimates are the quartile ones: μ = median, λ = half the inter-quartile range.',
    mom: function (x, d) { return [d.median, d.iqr / 2 > 0 ? d.iqr / 2 : d.sdN]; },
    mle: function (x, d) {
      var n = x.length;
      var grad = function (p) {
        var g0 = 0, g1 = 0;
        for (var i = 0; i < n; i++) { var u = x[i] - p[0], q = p[1] * p[1] + u * u; g0 += 2 * u / q; g1 += 2 * p[1] / q; }
        return [g0, n / p[1] - g1];
      };
      var hess = function (p) {
        var h00 = 0, h01 = 0, h11 = 0;
        for (var i = 0; i < n; i++) {
          var u = x[i] - p[0], l2 = p[1] * p[1], q = l2 + u * u;
          h00 += 2 * (u * u - l2) / (q * q); h01 += -4 * p[1] * u / (q * q); h11 += 2 * (u * u - l2) / (q * q);
        }
        return [[h00, h01], [h01, -n / (p[1] * p[1]) - h11]];
      };
      var ll = function (p) { var s = 0; for (var i = 0; i < n; i++) s += DIST.cauchy.logpdf(x[i], p); return s; };
      var p = DIST.cauchy.mom(x, d);
      // Newton on a non-concave likelihood: accept only steps that raise it.
      for (var it = 0; it < 500; it++) {
        var g = grad(p), H = hess(p), det = H[0][0] * H[1][1] - H[0][1] * H[1][0];
        var s0 = (H[1][1] * g[0] - H[0][1] * g[1]) / det, s1 = (H[0][0] * g[1] - H[1][0] * g[0]) / det;
        var base = ll(p), t = 1, np = null, ok = false;
        if (!(isFinite(s0) && isFinite(s1)) || H[0][0] >= 0) { s0 = -g[0] * 0.1 * p[1]; s1 = -g[1] * 0.1 * p[1]; }
        for (var h = 0; h < 60; h++) {
          np = [p[0] - t * s0, p[1] - t * s1];
          if (np[1] > 0 && ll(np) >= base) { ok = true; break; }
          t /= 2;
        }
        if (!ok) break;
        var moved = Math.abs(np[0] - p[0]) + Math.abs(np[1] - p[1]);
        p = np;
        if (moved < 1e-14 * (1 + Math.abs(p[0]) + p[1])) break;
      }
      return p;
    },
    logpdf: function (v, p) { var z = (v - p[0]) / p[1]; return -Math.log(Math.PI * p[1] * (1 + z * z)); },
    cdf: function (v, p) { return 0.5 + Math.atan((v - p[0]) / p[1]) / Math.PI; }
  };
  DIST.weibull = {
    name: 'Weibull', kind: 'continuous', k: 2, names: ['k', 'λ'],
    applies: DIST.lognormal.applies,
    mom: function (x, d) {
      var target = 1 + d.varN / (d.mean * d.mean);
      var f = function (k) { return Math.exp(lgamma(1 + 2 / k) - 2 * lgamma(1 + 1 / k)) - target; };
      var lo = 0.02, hi = 2;
      while (f(hi) > 0) hi *= 2;
      var k = solve1(f, null, lo, hi);
      return [k, d.mean / Math.exp(lgamma(1 + 1 / k))];
    },
    mle: function (x) {
      var n = x.length, lx = x.map(Math.log), ml = mean(lx);
      var f = function (k) {
        var a = 0, b = 0;
        for (var i = 0; i < n; i++) { var t = Math.pow(x[i], k); a += t * lx[i]; b += t; }
        return a / b - 1 / k - ml;
      };
      var lo = 1e-3, hi = 1;
      while (f(hi) < 0) hi *= 2;
      var k = solve1(f, null, lo, hi), s = 0;
      for (var i = 0; i < n; i++) s += Math.pow(x[i], k);
      return [k, Math.pow(s / n, 1 / k)];
    },
    logpdf: function (v, p) { return v <= 0 ? -Infinity : Math.log(p[0] / p[1]) + (p[0] - 1) * Math.log(v / p[1]) - Math.pow(v / p[1], p[0]); },
    cdf: function (v, p) { return v <= 0 ? 0 : 1 - Math.exp(-Math.pow(v / p[1], p[0])); }
  };
  DIST.logistic = {
    name: 'Logistic', kind: 'continuous', k: 2, names: ['μ', 's'],
    applies: function (x, d) { return d.sdN > 0 ? '' : 'all the values are equal'; },
    mom: function (x, d) { return [d.mean, Math.sqrt(3) * d.sdN / Math.PI]; },
    mle: function (x, d) {
      var n = x.length;
      function sig(z) { return 1 / (1 + Math.exp(-z)); }
      var grad = function (p) {
        var g0 = 0, g1 = 0;
        for (var i = 0; i < n; i++) {
          var z = (x[i] - p[0]) / p[1], t = 1 - 2 * sig(-z);           // tanh(z/2)
          g0 += t / p[1]; g1 += (z * t - 1) / p[1];
        }
        return [g0, g1];
      };
      var hess = function (p) {
        var h00 = 0, h01 = 0, h11 = 0;
        for (var i = 0; i < n; i++) {
          var z = (x[i] - p[0]) / p[1], sz = sig(z), t = 2 * sz - 1, dt = 2 * sz * (1 - sz);
          h00 += -dt / (p[1] * p[1]);
          h01 += -(t + z * dt) / (p[1] * p[1]);
          h11 += (1 - 2 * z * t - z * z * dt) / (p[1] * p[1]);
        }
        return [[h00, h01], [h01, h11]];
      };
      return newton2(DIST.logistic.mom(x, d), grad, hess, function (p) { return p[1] > 0; });
    },
    logpdf: function (v, p) { var z = (v - p[0]) / p[1]; return -Math.abs(z) - 2 * Math.log1p(Math.exp(-Math.abs(z))) - Math.log(p[1]); },
    cdf: function (v, p) { return 1 / (1 + Math.exp(-(v - p[0]) / p[1])); }
  };
  DIST.pareto = {
    name: 'Pareto', kind: 'continuous', k: 2, names: ['α', 'xₘ'],
    applies: DIST.lognormal.applies,
    mle: function (x, d) { var s = 0; x.forEach(function (v) { s += Math.log(v / d.min); }); return [x.length / s, d.min]; },
    mom: function (x, d) { return [d.mean / (d.mean - d.min), d.min]; },
    logpdf: function (v, p) { return v < p[1] ? -Infinity : Math.log(p[0]) + p[0] * Math.log(p[1]) - (p[0] + 1) * Math.log(v); },
    cdf: function (v, p) { return v <= p[1] ? 0 : 1 - Math.pow(p[1] / v, p[0]); }
  };

  S.DIST = DIST;
  S.DIST_ORDER = ['degenerate', 'bernoulli', 'binomial', 'poisson', 'geometric', 'negbinomial', 'hypergeometric',
                  'duniform', 'uniform', 'normal', 'lognormal', 'exponential', 'laplace', 'gamma', 'beta1', 'beta2',
                  'cauchy', 'weibull', 'logistic', 'pareto'];

  function fmt(v) { return (Math.round(v * 1e4) / 1e4).toString(); }

  S.logLik = function (key, x, p) {
    var D = DIST[key], f = D.kind === 'discrete' ? D.logpmf : D.logpdf, s = 0;
    for (var i = 0; i < x.length; i++) s += f(x[i], p);
    return s;
  };
  S.cdfOf = function (key, p) { return function (v) { return DIST[key].cdf(v, p); }; };
  S.densityOf = function (key, p) {
    var D = DIST[key], f = D.kind === 'discrete' ? D.logpmf : D.logpdf;
    return function (v) { return Math.exp(f(v, p)); };
  };

  /* Pool classes whose expected frequency is below 5 into their neighbour,
     from both ends inward, as the courses do before a chi-square test. */
  function pool(cells) {
    cells = cells.map(function (c) { return { lo: c.lo, hi: c.hi, obs: c.obs, exp: c.exp, label: c.label, loLabel: c.loLabel, hiLabel: c.hiLabel }; });
    function merge(a, b) {
      return { lo: a.lo, hi: b.hi, obs: a.obs + b.obs, exp: a.exp + b.exp, loLabel: a.loLabel, hiLabel: b.hiLabel, merged: true };
    }
    while (cells.length > 1 && cells[0].exp < 5) cells.splice(0, 2, merge(cells[0], cells[1]));
    while (cells.length > 1 && cells[cells.length - 1].exp < 5) {
      var m = cells.length;
      cells.splice(m - 2, 2, merge(cells[m - 2], cells[m - 1]));
    }
    for (var i = 1; i < cells.length - 1; i++) {
      if (cells[i].exp < 5) { cells.splice(i, 2, merge(cells[i], cells[i + 1])); i--; }
    }
    if (cells.length > 1 && cells[cells.length - 1].exp < 5) {
      var q = cells.length;
      cells.splice(q - 2, 2, merge(cells[q - 2], cells[q - 1]));
    }
    return cells;
  }
  S.poolCells = pool;

  /* Observed and expected frequencies in classes, for a chi-square test. */
  S.gofCells = function (key, x, p) {
    var D = DIST[key], n = x.length, d = S.describe(x), cells = [], i;
    if (D.kind === 'discrete') {
      var lo = d.min, hi = d.max;
      for (var v = lo; v <= hi; v++) {
        var Pl = v === lo ? D.cdf(v, p) : D.cdf(v, p) - D.cdf(v - 1, p);
        if (v === hi) Pl = 1 - D.cdf(v - 1, p);
        if (lo === hi) Pl = 1;
        var obs = x.filter(function (t) { return t === v; }).length;
        cells.push({ lo: v, hi: v, obs: obs, exp: n * Pl,
                     loLabel: v === lo ? '≤ ' + v : String(v), hiLabel: v === hi ? '≥ ' + v : String(v) });
      }
      if (lo === hi) cells[0].loLabel = String(lo);
    } else {
      var ft = S.freqTable(x).classes;
      for (i = 0; i < ft.length; i++) {
        var a = i === 0 ? -Infinity : ft[i].lo, b = i === ft.length - 1 ? Infinity : ft[i].hi;
        var P = (b === Infinity ? 1 : D.cdf(b, p)) - (a === -Infinity ? 0 : D.cdf(a, p));
        cells.push({ lo: a, hi: b, obs: ft[i].f, exp: n * P,
                     loLabel: i === 0 ? 'below ' + num(ft[i].hi) : num(ft[i].lo), hiLabel: i === ft.length - 1 ? 'and above' : num(ft[i].hi) });
      }
    }
    return cells;
  };
  function num(v) { return String(Math.round(v * 1e6) / 1e6); }

  S.chiGof = function (key, x, p, nEst, alpha) {
    var raw = S.gofCells(key, x, p), cells = pool(raw), chi = 0;
    cells.forEach(function (c) { c.contrib = c.exp > 0 ? (c.obs - c.exp) * (c.obs - c.exp) / c.exp : (c.obs > 0 ? Infinity : 0); chi += c.contrib; });
    var df = cells.length - 1 - nEst;
    var r = { raw: raw, cells: cells, stat: chi, df: df, nEst: nEst, discrete: DIST[key].kind === 'discrete' };
    if (df < 1) { r.p = NaN; r.reject = null; r.note = 'too few classes after pooling for a chi-square test'; return r; }
    r.p = S.chi2Sf(chi, df); r.crit = S.chi2Inv(1 - alpha, df); r.reject = decide(r.p, alpha);
    return r;
  };

  /* Compare one variable with every distribution (or with one the visitor
     specifies). o: { alpha, binomN, hyperN, hyperDraws, only, params }. */
  S.fit = function (key, x, o) {
    o = o || {};
    var D = DIST[key], d = S.describe(x), alpha = o.alpha || 0.05;
    var out = { key: key, name: D.name, kind: D.kind, names: D.names };
    var why = D.applies(x, d, o);
    if (why) { out.applicable = false; out.reason = why; return out; }
    out.applicable = true;
    var specified = !!o.params;
    try {
      out.mle = specified ? o.params : D.mle(x, d, o);
      out.mom = specified ? null : D.mom(x, d, o);
    } catch (e) { out.applicable = false; out.reason = 'the estimates could not be found for these data'; return out; }
    var p = out.mle;
    out.nEst = specified ? 0 : D.k;
    out.logL = S.logLik(key, x, p);
    if (!isFinite(out.logL)) { out.applicable = false; out.reason = 'a value lies outside the range this distribution allows'; return out; }
    out.aic = 2 * out.nEst - 2 * out.logL;
    out.bic = out.nEst * Math.log(x.length) - 2 * out.logL;
    if (key === 'degenerate') { out.perfect = true; return out; }
    out.chi = S.chiGof(key, x, p, out.nEst, alpha);
    if (D.kind === 'continuous') out.ks = S.ksTest(x, S.cdfOf(key, p));
    if (out.ks) { out.ks.reject = decide(out.ks.p, alpha); out.ks.estimated = !specified; }
    return out;
  };

  S.fitAll = function (x, o) {
    return S.DIST_ORDER.map(function (k) { return S.fit(k, x, o); });
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = S;
  else root.Stats3D = S;
})(this);
