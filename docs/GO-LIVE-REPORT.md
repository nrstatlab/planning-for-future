# NRSTATLAB — go-live readiness report

**Reviewed:** 22 September 2026, at commit `603c723`.
**Scope:** the whole repository, read as a web designer and as a statistician would read it.
**Status:** report only. Nothing in this review has been fixed. Every finding is graded so the
order of work is a decision rather than a guess.

**One caveat up front.** Every finding below comes from the repository, not from the served
site: the review environment's proxy refuses `nrstatlab.github.io` (`CONNECT tunnel failed,
403`). Section 7 gives the three commands to run against the live URL yourself.

---

> ### Update, 24 September 2026 — what the restructure closed
>
> This report is left as it was written, including the URLs it quotes as evidence: rewriting
> those would erase the finding. Three of its items are now fixed, and one is fixed differently
> from how it was described.
>
> | Finding | Status |
> |---|---|
> | §1.5 — 160 `<loc>` entries carry a raw space, and 180 tracked paths contain one | **Fixed.** Every BSc subject folder is now a hyphenated slug; `grep -c '<loc>[^<]* ' sitemap.xml` prints 0. The 160 spaced paths that remain are redirect stubs at the old URLs, excluded from the sitemap. |
> | §1.5 — two naming conventions inside one section | **Fixed.** `statistics/bsc/` and `statistics/msc/` read the same way, and 323 filenames stopped repeating their own folder. |
> | §1.6 — the sitemap and the canonical tags disagree on the 28 directory indexes | **Unchanged.** Still one URL in the sitemap and a different one in `rel=canonical`. |
> | ARCHITECTURE §5 — 25 pages whose generators are not in the repository | **Half closed.** The 15 scripts behind the ten `exams/` pages are tracked in `tools/exams/`, each proved to reproduce its page byte for byte. The 22 behind `subjects/` are still gone, so `recheck_fa.py` (115 checks) and `recheck_econ.py` (79) remain unreproducible. |
>
> Everything else below still stands, including the econometrics arithmetic in §1.1 and the
> unsourced exam-pattern claim in §1.2. **All 691 URLs changed**, so any of this report's paths
> now name a redirect stub rather than the page; `docs/ARCHITECTURE.md` §7 explains the mapping.

---

## Contents

0. [What is actually here](#0-what-is-actually-here)
1. [Blockers](#1-blockers--fix-before-you-tell-anyone-the-url)
2. [Should fix](#2-should-fix--every-reader-sees-these)
3. [Worth knowing](#3-worth-knowing--real-but-not-launch-blocking)
4. [The statistician's read](#4-the-statisticians-read)
5. [The web designer's read](#5-the-web-designers-read)
6. [Checked and sound](#6-checked-and-sound)
7. [Launch checklist](#7-launch-checklist)

---

## 0. What is actually here

Measured from the tree, not from memory, because several published figures have drifted.

| | |
|---|---|
| URLs in `sitemap.xml` | **690** |
| HTML files tracked | 692 (691 excluding `archive/`) |
| CSS files | 31 — but only **5 distinct** production stylesheets |
| Commits | 61 |
| Working tree | 28 MB (`.git` a further 43 MB) |

By section: `data-science-major` 408 pages · `statistics-major` 241 · `exam-subjects` 15 ·
`ugc-net-statistics` 13 · `statistics-papers` 10 · 4 top-level pages.

### Published figures that are now wrong

| Claim | Where | Actual |
|---|---|---|
| "594 pages of study material" | `README.md:8` | **691** |
| "A–Z, **1,465** of them" | `README.md:25` | **1,918** — and across **283** pages, not 690 |
| "MSc: **12** subject folders, **32** unit pages" | `README.md:16` | **13** folders, **36** unit pages |
| "**21** byte-identical copies of `styles.css`" | `README.md:84` | **23** |
| test chooser "names **four** tests it does not cover" | `README.md:49–50` | it names **six** — and two of them *are* covered |

`index.html` is right where the README is wrong (13 MSc subjects, 36 units), because
`tools/check_home_stats.py` guards the home page and nothing guards the README.

**Reproduce:**
```sh
grep -c '<loc>' sitemap.xml
git ls-files '*.html' | grep -vc '^archive/'
grep -c '<dt' topics.html
ls -d statistics-major/msc/*/ | wc -l ; ls statistics-major/msc/*/unit*.html | wc -l
```

---

## 1. Blockers — fix before you tell anyone the URL

### 1.1 A worked regression example is arithmetically wrong, and the R code beside it proves it

`statistics-major/econometrics/unit2_econometrics.html:127`

> \(\bar X = 30, \bar Y = 27\), \(S_{XY} = \sum(X_i-30)(Y_i-27) = **790**\), \(S_{XX} = 1000\).

With X = (10, 20, 30, 40, 50) and Y = (11, 20, 27, 34, 43) the cross-products are
320, 70, 0, 70, 320. **S_XY = 780.** Everything downstream inherits the error:

| Line | Printed | Correct |
|---|---|---|
| `unit2:128` | β̂₁ = 0.79 | **0.78** |
| `unit2:128` | β̂₀ = 3.30 | **3.60** |
| `unit2:129` | Ŷ = 3.30 + 0.79X, MPC 0.79 | **Ŷ = 3.60 + 0.78X**, MPC **0.78** |
| `unit2:135` | Ŷ(35) = 30.95 (₹30,950) | **30.90** |
| `unit2:136` | Ŷ(100) = 82.30 (₹82,300) | **81.60** |

`statistics-major/econometrics/practical_econometrics.html:55–57` repeats all of it and adds a
second, independent set of errors at `:66–67`: TSS is given as 630 (it is **610**), RSS as 6.7
(it is **1.60**), R² as 0.9894 (it is **0.9974**), F as 279.1 (it is **1141**). RSS = 6.7 is not
even consistent with the page's *own* wrong slope, which would give 1.70.

**What makes this a blocker rather than a typo.** Three lines under the wrong answer,
`practical_econometrics.html:58–59` prints:

```r
x <- c(10,20,30,40,50); y <- c(11,20,27,34,43)
fit <- lm(y ~ x); summary(fit)
```

A student who does what the page asks gets intercept 3.60, slope 0.78, R² 0.9974 — and watches
the site contradict itself. Eleven numbers across two files.

### 1.2 The site states an exam pattern with no source, on the one point it promises not to

`ugc-net-statistics/index.html:177`

> **Pattern:** NET Paper II has 100 MCQs; conceptual clarity beats rote memorization.

`statistics-papers/index.html:175–178`

> **No exam pattern is stated here, and that is deliberate.** Marks, duration, negative marking,
> the number of papers and eligibility all change between notifications … Nothing of that kind
> appears on this site unless it was taken from the official document for that examination.

The UGC NET page's only provenance is a badge at `:56` reading "Based on official UGC NET Bureau
Syllabus" — which names no document, number, date or version, and a syllabus would not carry the
paper pattern anyway. Line 178 adds an unsourced weighting claim ("High-yield units … contribute
the largest share of questions"). `pyq2026.html:53` asserts "Held 30 June 2026" and reproduces a
50 + 100 structure, citing only "the scan".

The ISS and APPSC pages do this properly — every figure quoted and attributed by notice number
and date. UGC NET is the section that was never brought into line, and it is linked from the
page making the promise.

### 1.3 The test chooser's self-audit is wrong about itself

`which-statistical-test.html:274–282` states that the site "does not currently cover Levene's,
Bartlett's or the Brown–Forsythe test", that "Levene's is named twice in passing and taught
nowhere", and that every "Bartlett" hit is a different Bartlett.

- **Brown–Forsythe** — true, zero occurrences.
- **Levene's** — false. Seven mentions in four files, and one *teaches its use*:
  `statistics-major/msc/statistical-analysis-using-spss/practical.html:292` — "**The
  independent-samples table has two rows, and choosing between them is the examinable step.**
  SPSS prints Levene's test for equality of variances first … Read Levene, then read the row it
  points to." Also `practical.html:666, 693`, `index.html:95`, and a full worked use at
  `statistics-major/statistical techniques for research methodology/unit5.html:392`.
- **Bartlett's** — false. `statistics-major/computational statistics and r
  programming/unit4_….html:501` lists `bartlett.test()` in the standard workflow as the
  equal-variance check. That is the test.

The same section misidentifies "Friedman" — the hits in `statistical analysis of clinical
trials/syllabus.html:87` are **Friedman, L.M.**, a textbook author, not the test.

This is the one page on the site whose entire purpose is honest self-audit. Getting it wrong
costs more than the same error anywhere else.

### 1.4 "Accept H₀" — the site teaches the rule and then breaks it 50 times

`data-science-major/statistical-foundations/unit5_statistical-foundations.html:298`

> is not "accept H₀" — a jury returns "not guilty", never "innocent". Writing "accept H₀" is a
> standard mark deduction.

There are **51 "accept H₀" phrasings across 13 files**, 38 of them in the five `inferential
statistics` pages. The worst is not an example but the *general procedure*:

`statistics-major/inferential statistics/unit4_inferential statistics.html:187`

> **Decide:** if |calculated| > tabulated, reject \(H_0\); otherwise **accept** \(H_0\).

and six conclusions assert the null as established — `unit4:299` "⇒ accept \(H_0\); die is
fair", `:323` "accept \(H_0\) — the variety yields about 12 q/ha", `:361` "variances equal".

The same subject gets it right one file away (`unit2:320`, "If p-value ≥ α: do not reject
\(H_0\)"), and `which-statistical-test.html:309` says "a non-significant result is not proof of
no effect". A few instances are legitimate and should stay: the page teaching against it, and
the conventional `Accept H₀` row in the Type I/II error table at `unit2:234`.

### 1.5 160 sitemap entries are invalid

`sitemap.xml` contains 160 `<loc>` elements with **unencoded literal spaces**:

```
<loc>https://nrstatlab.github.io/planning-for-future/statistics-major/actuarial statistics/index_actuarial statistics.html</loc>
```

`tools/build_sitemap.py:68` calls `escape()` (XML escaping) but never `quote()` (URL encoding).
A `<loc>` containing a raw space is invalid per the sitemap protocol. The same 160 URLs appear
raw in `rel=canonical` and `og:url` on those pages.

The root cause is that **20 of the 21 BSc subject folders have spaces in their names** — 180
tracked paths like `statistics-major/actuarial statistics/unit1_actuarial statistics.html`. The
MSc folders next to them use hyphens, so one section carries two conventions. Renaming is cheap
now and expensive once the URLs are shared and indexed; the sitemap encoding must be fixed
either way.

### 1.6 The sitemap and the canonical tags disagree on all 28 directory indexes

- `tools/build_sitemap.py:63` strips `index.html` → publishes `…/statistics-major/`
- `tools/check_canonical.py:61` does not → writes `…/statistics-major/index.html`

So a crawler is handed one URL and told the real one is a different URL that the sitemap never
lists. `check_canonical.py:16` asserts the two "cannot drift apart" because they share the page
*set* — they do share the set, but not the URL *form*, which is what a canonical is about.

### 1.7 675 of 691 pages do not say what site they belong to

The `nrstatlab-bar` — the only site-wide identity and the only link back to the home page — is on
**16 pages**: the six section hubs and ten map pages. Every study page has none.

It is worse inside `statistics-major`: **189 of its 219 unit pages contain no link that leaves
their own subject folder**, and their breadcrumb reads `<a href="index_<subject>.html">Home</a>`
— the word "Home" pointing at the subject index. A reader arriving from a search result is
stuck in one folder with no route to the other four sections, and no search box.

`data-science-major` does it correctly (`Home » Course » Lab`, Home = the section hub), which
shows the fix is a pattern already in the repository.

### 1.8 No `og:image`, no favicon link, no structured data

- **`og:image` / `twitter:image`: 0 of 691.** Every WhatsApp, Telegram or Slack share renders as
  a bare text card. For a site meant to travel student-to-student on phones this is the single
  highest-value fix in this report.
- **`<link rel="icon">`: 0 of 691.** `favicon.ico`, `favicon.png` and `favicon.svg` sit unused at
  the repository root. Only the `.ico` will be auto-fetched, and only at the domain root.
- **JSON-LD: 0.** No `Organization`, no `WebSite` + `SearchAction`, no `BreadcrumbList`, no
  `Course` — on a site that is a course catalogue with 1,829 Q&A `<details>` blocks.
- `theme-color` on **3** pages of 691.

### 1.9 `LICENSE` claims rights over material it does not own

`LICENSE` puts "every page, note, lab program, dataset and script in this repository" under
CC BY-NC-SA 4.0. The repository also ships four third-party syllabus PDFs
(`data-science-major/docs/*.pdf`, ~1 MB) that NRSTATLAB cannot license. Either add a
"Third-party material" carve-out or drop the PDFs — they are referenced only as `<code>` text,
never linked, and are not in the sitemap.

### 1.10 `robots.txt` and `sitemap.xml` contradict each other

`robots.txt:5` disallows `/data-science-major/labs/course-7-web/`. `sitemap.xml` lists all 16 of
those URLs. Those 16 pages are also unreachable from any other page. Pick one position.

---

## 2. Should fix — every reader sees these

### 2.1 The home page promises more than the pages deliver

`index.html` states, without qualification:

> **The code runs.** Lab programs are real source in C, Python, SQL and R, checked by compiling
> and running them rather than by reading them.

**85 of the 235 lab pages carrying a verification status (36%) are marked `NOT EXECUTED`** — R
because it is not installable in the build environment, MongoDB transactions because they need a
replica set. Each page is scrupulous about saying so; only the summary at the top is absolute.

The site's fourth principle is "Gaps are stated". The third should obey it: say how many ran.
That is a *stronger* claim than the present one, because it can be checked.

### 2.2 A visible typo on the flagship map

The ISS pages ran Roman numerals through a title-caser:

- `iss/paper2.html:6, 8, 88` → **`Statistics-Ii`** (should be `Statistics-II`)
- `iss/paper3.html:6, 8, 88` → `Statistics-Iii`
- `iss/paper4.html:6` → `Statistics-Iv`
- `iss/index.html:104, 108, 112` → all three, in `<h3>` headings

It is in the browser tab, the Google snippet, the share card and the page body of the map you
called the national spine.

### 2.3 UGC NET is invisible to the site's own discovery machinery

- **No card on the home page.** Five cards are shown; six sections exist. UGC NET — 13 pages, a
  500-MCQ bank, a solved paper — is reachable only from two chips under "Start here".
- **No topic chips.** All 13 UGC NET pages and all 10 examination maps have an empty `k` field in
  `assets/search-index.json`, so search matches them on title alone.
- **Absent from the A–Z index.** `topics.html` links only into `statistics-major`,
  `data-science-major` and `exam-subjects`. It is honest in its own lede ("1918 topics across
  283 pages"), but `README.md:25` calls it "every topic the site teaches".

Overall **408 of 690 search records (59%) carry no chips.**

### 2.4 The 500-MCQ page cannot be printed with its answers

`ugc-net-statistics/styles.css` has exactly one media query (`max-width: 600px`) and **no
`@media print` at all**. The other four stylesheets carry
`details:not([open]) > *:not(summary) { display: block !important }` — the rule that unfolds
collapsed answers on paper (`statistics-major/*/css/styles.css:439`). `mcqs.html` wraps every
answer in `<details><summary>Show Answer</summary>`.

**Printing the 500-MCQ page produces 500 questions and no answers.** Same for `pyq2026.html`.

### 2.5 Contrast failures on labels and controls

Computed against the background each colour is actually painted on:

| Element | File | Ratio | Needs |
|---|---|---|---|
| `.formula .label` white on `#f59e0b` | `statistics-major/*/css/styles.css:142–144` | **2.15:1** | 4.5 |
| `.topnav a.home` white on `#f59e0b` | `ugc-net-statistics/styles.css:71` | **2.15:1** | 4.5 |
| `.unit-number` `#f59e0b` on white | `ugc-net-statistics/styles.css:103` | **2.15:1** | 4.5 |
| `.ex-label` white on `#10b981` | `ugc-net-statistics/styles.css:169` | **2.54:1** | 4.5 |
| `.hero .shint` on gradient end | `assets/nrstatlab.css:594` | **3.01:1** | 4.5 |
| `.toc a` `#3b82f6` on `#f1f5f9` | `ugc-net-statistics/styles.css:246` | **3.36:1** | 4.5 |
| `.crumbs a` `#ffe49a` on gradient end | `statistics-major/*/css/styles.css:50` | **3.47:1** | 4.5 |
| `a` `#1e7fbf` on `#f4f6fa` | `assets/nrstatlab.css:37` | **4.01:1** | 4.5 |
| `--ink-faint` `#6b7a90` on ground | `assets/nrstatlab.css:9` | **4.03:1** | 4.5 |

Two structural causes: **`#f59e0b` used as a background for white text**, and
**`#1e7fbf` / `#3b82f6` used as both a link colour and a chip background**. Body text passes
everywhere and comfortably (13.69:1 to 17.06:1) — this is a palette-role problem, not a
legibility problem.

### 2.6 Keyboard and screen-reader gaps

- **No skip link on any of 691 pages.** On `ugc-net-statistics/*` a keyboard user tabs through 13
  sticky nav links plus a table of contents before reaching content, on every page.
- **`<main>` on 17 pages of 691.** All 241 `statistics-major`, all 408 `data-science-major`, all
  10 `statistics-papers` and all 15 `exam-subjects` pages have no landmark elements at all.
- **451 heading-level skips** — 391 of them one generator-produced `h2 → h4` pattern in
  `data-science-major`, so one fix in `build_site.py` closes most of it. Five are `h1 → h4`
  (`ugc-net-statistics/unit3,4,7,9,10.html:63`).
- **69 content SVG diagrams carry no `role`, `aria-label`, `<title>` or `aria-hidden`** — e.g.
  `statistics-major/statistical methods/unit2_….html:103, 122, 141`. 110 others are labelled
  correctly, so the convention exists and was applied unevenly.
- **`which-statistical-test.html:52–95`** — the 24 filter buttons have no `aria-pressed`;
  selected state is a CSS class and nothing else.
- **The self-study-notes tabs** declare `role="tablist"` and `role="tab"` with **zero
  `role="tabpanel"`**, no `aria-controls`, no roving `tabindex`.
- **2,911 tables, 4 use `scope=`.** Row-header tables need `scope="row"`.
- **Zero `aria-current`**, including on the 13 sticky nav bars where the current unit is unmarked.

### 2.7 Search-result presentation

- **297 of 691 titles exceed 60 characters** (longest 131) and will be truncated.
- **88 meta descriptions exceed 165 characters.**
- **Only 3 of 692 titles contain "NRSTATLAB"**, across six competing suffix conventions
  (`— Complete Study Material`, `— Official Syllabus`, `— Practical Lab`, …). Two hubs are bare:
  `statistics-papers/index.html:6` is just "Statistics for Examinations".
- `og:type` is `article` on 673 pages, including every hub.

---

## 3. Worth knowing — real but not launch-blocking

1. **CI validates 29 of 691 pages.** `.github/workflows/validate.yml:44` blacklists
   `statistics-major`, `data-science-major` and `ugc-net-statistics`, and its `--match` list
   omits `topics.html` and `which-statistical-test.html`. The thirteen statistics rechecks and
   the map rechecks live in a scratchpad and run only by hand.
2. **`data-science-major/css/styles.css` is missing a rule its own header says it has.** Its
   comment (L4–8) says everything above the ADDITIONS rule is "unchanged … keep it that way so
   the two stylesheets stay diffable". It lacks
   `.concept, .formula, .example, .tip { overflow-wrap: break-word }`
   (`statistics-major/*/css/styles.css:285`) — the rule that stops un-typeset TeX dragging the
   page sideways before MathJax runs.
3. **The self-study-notes stylesheet has no mobile overflow guards.** No
   `table { display: block; overflow-x: auto }`, no `overflow-wrap` on `p`/`li`/`td`/`code`, and
   **no `mjx-container[display="true"] { overflow-x: auto }` anywhere in the file** — all three
   present in its sibling sheets. 69 `table.data-mini-table` elements have no rule of their own.
4. **`ugc-net-statistics` sets `scroll-behavior: smooth` and a sticky nav but no
   `scroll-margin-top`.** Every table-of-contents anchor lands with its heading hidden behind the
   bar. The section that does not need the guard has it; the one that does, does not.
5. **`scroll-behavior: smooth` in 24 stylesheets with no `prefers-reduced-motion` guard.**
6. **`archive/…-single-file.html`** — 258 KB, publicly served, unreachable, no canonical, no
   `noindex`, not in `robots.txt`; a duplicate of the live ML notes and the only page pulling
   Google Fonts and cdnjs Prism.
7. **Four pages carry more than one `<h1>`** (`# Part A` in markdown rendering as `<h1>`).
8. **No SRI** on the MathJax tag 255 pages load from `cdn.jsdelivr.net`.
9. **`topics.html` is 425 KB** — 1,918 `<dt>` and 2,141 links in one document, laid out in
   `columns: 2` (`assets/nrstatlab.css:377`), which forces a full column-flow layout before
   first paint. The heaviest page on the site by 2.7×.
10. **`exam-subjects/css/styles.css` is a 23rd identical copy** that the documented md5 guard
    (`README.md:89`) does not cover, so it can drift silently.
11. **A latent trap.** 242 pages let MathJax use its defaults (`\(…\)` only); the 13 UGC NET
    pages override `inlineMath` to accept `$…$`, and `mcqs.html` alone has 2,987 `$` outside
    `<code>`. Checked — **not a bug today**: the 11 bare `$` in the Excel unit (`$A$1`) sit on a
    default-config page and render literally. Unifying the config later breaks one side or the
    other.
12. **Five "phone" breakpoints** — 600, 620, 640, 700, 760px — across four stylesheets.

---

## 4. The statistician's read

Roughly sixty worked examples were recomputed across descriptive statistics, probability,
estimation, testing, regression, ANOVA, design of experiments, quality control, sampling, index
numbers, actuarial, econometrics, economics and accounting; ~120 of the 500 MCQs were checked
against their keys; all 323 Python blocks under `data-science-major/notes/` were parsed.

**The mathematics is unusually reliable.** Gauss–Markov (including the explicit note that
normality is *not* required), Lindeberg–Lévy, WLLN/SLLN, Cramér–Rao with its attainment
condition, Rao–Blackwell with its equality condition, Lehmann–Scheffé, Neyman–Fisher
factorisation and Neyman–Pearson are all stated with correct conditions. The MSc Estimation
Theory unit is exact to six decimal places throughout.

Beyond §1.1, §1.3 and §1.4, these are the content defects worth listing:

### 4.1 Two MCQs are unusable as printed

`ugc-net-statistics/mcqs.html:1599` (Unit 8, Q16) — *"PCA finds:"* A. Eigenvectors of covariance
matrix / B. Eigenvalues of correlation matrix **only** / C. **Largest** singular value / D. All
of the above. **Marked D.** D cannot be right: B's "only" contradicts A, and C names one
singular value where PCA yields the spectrum. **A is correct.**

`ugc-net-statistics/mcqs.html:1611` (Unit 8, Q19) — option D reads
`$\text{tr}\Sigma$ — same as A` and the answer says `D. Both A and "trace of $\Sigma$"`. An
editorial note has leaked into the rendered option, and the key admits two options are right.

Three more have duplicate or double-correct options: `:137` ($L^2$ and "mean square" are the same
mode of convergence), `:157` (for a *continuous* random variable both A and C are true), `:1469`
($1/T$ and $1/n$ are the same quantity).

Across ~120 sampled, that is 2 wrong keys and 3 defective option sets — about 4%.

### 4.2 An inflated coverage grade

`statistics-papers/iss/paper2.html:110` grades *"Multiple comparison tests due to Tukey, Scheffé
and Student–Newman–Keuls–Duncan"* as **deep**, pointing at
`statistics-major/msc/design-and-analysis-of-experiments/unit1.html`. That page mentions Tukey
(10×) and Duncan (13×) and contains **zero** occurrences of Scheffé, Newman or Keuls. Site-wide,
"Scheffé" appears only as **Lehmann–Scheffé**, an unrelated theorem. Two of the four named tests
are absent. This should read `brief`.

Related: the same map grades *"Index numbers: types, need, data collection mechanism,
periodicity, agencies involved, uses"* as deep. The destination teaches the formulas superbly —
Laspeyres 145.45, Paasche 146.84, Fisher 146.14 and the whole reversal-test table all verify —
but carries one sentence on the administrative half of the line and nothing on periodicity or
collection mechanism.

**The percentages themselves are honest.** Recomputed: Paper I 28/35 = 80%, Paper II 23/27 = 85%,
Paper III 25/30 = 83%, Paper IV 45/55 = 82%, and deep/brief/missing are broken out separately so
"covered" never disguises "brief".

### 4.3 The only two-way ANOVA is degenerate

`statistics-major/design and analysis of experiments/unit1_….html:199` — SS_E = 0 exactly,
because the data are perfectly additive. The page says so, but MS_E = 0 makes both F-ratios
undefined, and the ANOVA table twenty lines above tells the reader to compute MS_R/MS_E. Example
2 then supplies pre-computed sums of squares. The site's only BSc two-way ANOVA is never worked
from data to a valid F.

### 4.4 Four definitional inconsistencies

- **Yates vs Fisher trigger.** `inferential statistics/unit4:310` says use **Yates' correction**
  when an expected cell < 5; `which-statistical-test.html:242` says that is when to reach for
  **Fisher's exact**. The conventional reading is Fisher's; Yates applies to 2×2 tables
  generally. The Yates formula given is correct — it is the condition that conflicts.
- **Chi-square GOF df.** `unit4:177` correctly gives `χ²_{k−1−r}` with *r* parameters estimated;
  the summary card at `unit4:308` drops the correction to `df = n−1`.
- **F-test df.** `unit4:309` pairs "larger s² over smaller" with `df = (n₁−1, n₂−1)`. If s₂² is
  the larger, the df are (n₂−1, n₁−1). Putting the larger on top also makes the test two-tailed,
  which is not mentioned. No worked answer is affected — the examples happen to have the larger
  variance first.
- **A skewness conclusion against the unit's own rule.** `descriptive statistics/unit5:490`
  concludes "positively skewed and platykurtic". Every figure on that problem verifies (mean
  11.222, median 11.184, mode 10.917, μ₂ 9.047, μ₄ 207.07, β₂ 2.53) — but μ₃ = **−3.02**, and
  `unit5:313` defines the sign of skewness as the sign of μ₃. Pearson and Bowley say positive,
  the moment measure says negative, and the page computes μ₄ without ever computing μ₃.

### 4.5 Test-chooser assumptions that are materially thin

- **Regression** (`:131`) gives its assumptions as "the same as correlation, plus that you have
  decided which variable explains which" — omitting independence of errors, homoscedasticity,
  normality of residuals for inference, and leverage. The "if that fails" cell then offers
  correlation, which remedies none of them.
- **One-sample t** (`:144`) offers only the **sign test** as a fallback. The site teaches the
  Wilcoxon signed-rank test (`inferential statistics/unit5`, §4) and offers it for the paired row
  but not this one.
- **Independence of observations** is never listed for Pearson's r, the one-sample t or the
  two-sample t, though it is listed for ANOVA and both chi-squares.

The rest of the page is sound, and two parts are better than most textbooks: the paired-t row's
insistence that normality applies to the *differences*, and the "what a significant result does
not tell you" section (`:301–311`), correct on all four counts including the p-value conditional.

### 4.6 Smaller items

- `ugc-net-statistics/pyq2026.html:538` justifies AR(2) stationarity with Φ₁+Φ₂ < 1 alone. That
  is necessary, not sufficient (the full conditions are Φ₁+Φ₂ < 1, Φ₂−Φ₁ < 1, |Φ₂| < 1). The
  answer is right here — both roots do lie outside the unit circle — but the rule as presented
  will fail a student elsewhere.
- **Seven Python blocks are cheat-sheets fenced as `python`** and would not run as printed, e.g.
  `notes/sem-4/course-9-python-data-analysis/unit-1.md:457`
  (`np.sqrt(a)   np.exp(a)   np.log(a)`). Fence them as `text`. 313 of 323 parse cleanly, and
  three of the failures are deliberate error demonstrations.
- `statistical techniques for research methodology/unit5.html:392` — "Levene's test indicated
  equal variances" should read "did not indicate unequal variances". The rest of that paragraph
  is exemplary and every number in it verifies (pooled SD 7.858, t(198) = 5.13, CI [3.51, 7.89],
  d = 0.725).
- `inferential statistics/unit4:167` draws a causal conclusion ("coaching had effect") from a
  paired design with no control.
- **Suspicion, not a finding:** `computational statistics and r programming/unit4:308` uses
  `t.test(extra ~ group, data = sleep, paired = TRUE)`. The formula interface with
  `paired = TRUE` is believed deprecated in R ≥ 4.4.0. Unverified — there is no R in the review
  environment. `unit4:416` uses the native pipe `|>`, needing R ≥ 4.1; a version note would help.

---

## 5. The web designer's read

### 5.1 Five visual systems

31 CSS files, 9 distinct byte-streams, **5 of them production stylesheets**:

| copies | file | used by |
|---|---|---|
| **23** | the shared subject sheet | 22 `statistics-major/*/css/` + `exam-subjects/css/` |
| 1 | `assets/nrstatlab.css` | home, A–Z, test chooser |
| 1 | `data-science-major/css/styles.css` | 408 pages |
| 1 | `ugc-net-statistics/styles.css` | 13 pages |
| 1 | `…/self-study-notes/css/styles.css` | the ML notes |

The 23 copies are genuinely byte-identical — that invariant holds. But the four independent
sheets disagree on almost everything a reader would notice:

| | `nrstatlab.css` | subject sheet | `ugc-net` |
|---|---|---|---|
| body size / line-height | 16px / 1.65 | **17px** / 1.65 | 16px / **1.7** |
| page background | `#f4f6fa` | `#f5f7fb` | `#f8fafc` |
| body ink | `#16233a` | `#1f2937` | `#0f172a` |
| max-width | 1120px | 980px | 1100px |
| primary blue | `#0f4c81` | `#0f4c81` | **`#1e3a8a`** |
| link colour | `#1e7fbf` | `#0f4c81` | `#3b82f6` |
| h2 size | 1.42rem | 1.55rem | 1.7rem |
| table cells | left | **centred** | left |

**The callout vocabularies do not even share names.** `statistics-major` uses `.concept` /
`.formula` / `.example` / `.tip`; `ugc-net-statistics` uses `.definition` / `.theorem` /
`.example` / `.note` / `.realworld`. Only `.example` is common, and even its label chip differs
(`#059669` vs `#10b981`). A reader crossing from a statistics unit to a UGC NET unit sees a
different site.

### 5.2 What will overflow on a 360px phone

1. **69 `table.data-mini-table` elements in the self-study notes** — `table { width: 100% }` with
   no scroll fallback and no rule of their own. Only 15 of 86 tables in that folder sit inside
   the `.table-scroll` wrapper. Four-column tables will push the document sideways.
2. **The UGC NET sticky nav** — 13 links wrapping to 3–4 rows, permanently eating ~120px of a
   360px viewport, with anchors landing underneath it (§3.4).
3. `assets/nrstatlab.css:463` — `table.tests { min-width: 56rem }` reducing to 44rem at ≤760px.
   Contained by `overflow-x: auto`, so the page does not move: correct, but it is a 704px
   scroller on a 360px screen.

### 5.3 Print

26 of 31 stylesheets have an `@media print` block. The five without are the ones that matter:
`assets/nrstatlab.css` (the three top-level pages), `ugc-net-statistics/styles.css` (§2.4), and
**no inline `<style>` block anywhere in the repo has one** — which covers
`statistics-papers/index.html`, the nine paper maps, four section hubs and `404.html`.

The blocks that do exist are thin: `statistics-major/*/css/styles.css:295` does not reset
`pre { background: #0f172a }`, so every code block prints as a solid dark rectangle, nor the
`.banner` gradient, which prints full-bleed at the top of every unit.

**What is right and should not be lost:** the `details:not([open])` unfolding rule across 1,829
collapsed answers, and `details.toc { display: none }`. That is the highest-value print rule on
the site and it is correct in four of the five sheets.

### 5.4 Performance, and what is already good

`search.js:214` binds loading to the input's `focus`, so the 391 KB index is fetched only when
someone actually uses the box — a page that is merely read costs nothing for it. No
render-blocking scripts: `search.js` and `notes.js` are `defer`, MathJax is `async`.

**Zero web fonts.** No `@font-face`, no font files, no Google Fonts on any production page — the
system stack throughout. The only external origin a live page contacts is `cdn.jsdelivr.net`.
No analytics, no trackers, no cookies, no consent banner needed.

MathJax wiring is correct where it counts: **5 pages load it with no math on them, and zero
pages have math without it.**

---

## 6. Checked and sound

Recorded so these are not re-litigated, and because the ratio matters for reading §1–§5.

- **0 broken internal links** across several thousand `href`s, and **0 broken anchors**. One
  audit reported a missing stylesheet in `data-science-major/web-technologies/unit2`; that is
  **wrong** — `../css/styles.css` resolves to a file that exists, and the hits are `<code>`
  examples inside the page's own HTML lesson. The earlier crawl (7,700 links, 2 deliberate
  exceptions) stands.
- **"272 lines graded"** on the home page is exactly right: ISS 147 + CSIR NET 52 + APPSC 73,
  counted from the grade spans rather than the prose.
- **The two APPSC posts really do share one syllabus** — 74 identical lines, differing only in
  paper labels. Counting APPSC once at 73 is correct, not a halving of 146.
- **No university is named** in any shipped page; all 24 "universit…" hits are generic.
- **27 of 27 `<img>` have `alt`. `lang="en"` on all 691 pages.**
- **The `statistics-major` stylesheet invariant holds** — all 23 copies share one md5.
- **Sample variance conventions are consistent** across 20+ files: n−1 throughout, with the
  n-divisor version correctly labelled as the biased MLE; `sampling techniques/unit2:60` defines
  and relates σ² and S² explicitly and uses each correctly thereafter. β₂ = μ₄/μ₂² and
  γ₂ = β₂ − 3 everywhere.
- Recomputed exactly, among others: both one-way ANOVAs in DOE unit 1 (F = 24.25 and 24.20), the
  2² factorial contrasts and Yates table, every SQC control-limit constant, the index-number
  reversal tests, national income by all three methods, SLM and WDV depreciation, Hotelling's T²
  in the solved paper, and the descriptive-statistics problems including Sheppard's corrections.
- The three site checkers pass on the current tree:

```
home page figures agree with the tree (266 lab programs, 266 practice questions, 13 MSc subject(s) with 36 unit pages)
690 indexed pages; 690 already correct, 0 written, 0 wrong
1 deliberate exception(s), asserted by name
691 pages and the search index checked
no raw TeX in any title, description, chip or search field
```

- **Two apparent contrast failures dissolved** when measured against the background actually
  painted behind them (a breadcrumb on a dark banner, a footer on a dark bar) and are not
  reported as faults.

---

## 7. Launch checklist

### Before you announce

Fix, in this order — the first four are cheap and the first is embarrassing if found by a reader:

1. §1.1 the econometrics arithmetic — eleven numbers, two files.
2. §2.2 `Statistics-Ii` → `Statistics-II` on four ISS pages.
3. §1.2 either source the UGC NET pattern claim to a named document or delete the line.
4. §1.3 rewrite the test chooser's not-covered note; §0 regenerate the README counts.
5. §1.8 add an `og:image` and wire the favicons.
6. §1.4 the "accept H₀" sweep, starting with the general procedure at `unit4:187`.
7. §1.5 / §1.6 `quote()` in `build_sitemap.py`, and make the sitemap and canonical agree on
   directory URLs. Decide separately whether to rename the spaced folders — the answer is much
   more likely to be "yes" now than in six months.
8. §1.7 put the `nrstatlab-bar` on every page. This is the largest change in the list and the one
   that most changes how the site reads.

### The day you announce

Run these against the live URL — nothing in this report was verified against the served site:

```sh
curl -sI https://nrstatlab.github.io/planning-for-future/ | head -1
curl -s  https://nrstatlab.github.io/planning-for-future/sitemap.xml | grep -c '<loc>'
curl -sI "https://nrstatlab.github.io/planning-for-future/statistics-major/descriptive%20statistics/unit1_descriptive%20statistics.html" | head -1
```

Then: submit `sitemap.xml` in Google Search Console, and paste one deep page URL into WhatsApp
to see what the share card actually looks like.

### The week after

- Search Console → **Coverage**, for the 160 space-containing URLs and the 28 hub URLs whose
  canonical disagrees with the sitemap. Both will show up there if they are going to.
- Search Console → **Performance**, to see which pages people actually arrive on. That tells you
  where the missing site bar (§1.7) costs the most.
- Re-run `tools/check_home_stats.py`, `check_canonical.py` and `check_no_raw_tex.py` after any
  fix, and regenerate the search index, topic index and sitemap after any page is added or moved.

---

## What this report does not cover

The custom-domain cutover — you chose to stay on `github.io` for now. When that changes,
`SITE_BASE` at `data-science-major/tools/build_site.py:51` is the single constant to rebase, and
every generator must be re-run afterwards or 690 canonicals will point the new site at the old
one. The SSC map and the remaining ISS work queue wait on official documents.

Nothing in this report has been fixed.

---

**Note added 23 September 2026.** This report is a dated audit and has not been rewritten, but
one line above it is now out of date: the SSC card no longer exists. It was replaced by an
**ASRB NET Agricultural Statistics** map built from a supplied syllabus, so the examinations hub
now carries five built maps and no unbuilt one. Everything else in this report still stands as
written — in particular §1.1 (the econometrics arithmetic), §1.2 (the unsourced UGC NET pattern
claim), §1.3, §1.4 and §1.8 are all still unfixed. The new map added 99 graded lines and one
page, so the counts in §0 are now 691 pages and 691 sitemap URLs.
