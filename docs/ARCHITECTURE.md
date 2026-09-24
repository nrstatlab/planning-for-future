# NRSTATLAB — code hierarchy and architecture

**As of** 24 September 2026, after the restructure. Every count here was measured from the tree
at that commit, and each one carries the command that produced it.

This is the long version of the README's "Repository layout" block. The README tells you where
files sit; this tells you how they are produced, which matters because **editing the wrong file
throws the work away.**

> **What changed in the restructure.** The section folders were renamed and flattened onto one
> URL scheme, 323 filenames stopped repeating their own folder, the three `tools/` directories
> became one, and the 180 paths containing spaces became hyphenated slugs. Every old URL still
> resolves: GitHub Pages cannot issue a redirect, so 690 stub pages sit at the old paths, each
> carrying a meta refresh and `robots noindex`. §7 describes them.

---

## Contents

1. [The three build regimes](#1-the-three-build-regimes)
2. [Directory tree](#2-directory-tree)
3. [The Python tooling](#3-the-python-tooling)
4. [Inside `build_site.py`](#4-inside-build_sitepy)
5. [The syllabus-map generators](#5-the-syllabus-map-generators)
6. [Build order](#6-build-order)
7. [The stub layer](#7-the-stub-layer)
8. [The navigation](#8-the-navigation)

---

## 1. The three build regimes

691 pages, produced three different ways — plus one archived file that is not part of the
site, and 690 stubs that are not pages at all.

| Regime | Pages | Source of truth | Where you edit |
|---|---|---|---|
| **Generated** | 408 | `data-science/notes/**/*.md`, plus the page tree for `topics.html` | the markdown or the generator — **never the HTML** |
| **Generated from syllabus data** | 10 | the data files in `tools/exams/` | the data file, then re-run its generator |
| **Hand-written** | 273 | the HTML itself | the HTML |

Which is which:

```
GENERATED          data-science/**                407 pages   ← build_site.py
                   topics.html                      1 page    ← build_topic_index.py
                   sitemap.xml robots.txt                     ← build_sitemap.py
                   assets/search-index.json                   ← build_search_index.py

                   exams/iss/       5 pages                   ← iss_map.py
                   exams/appsc/     3 pages                   ← appsc_map.py
                   exams/csir-net/  1 page                    ← gen_csir.py
                   exams/asrb-net/  1 page                    ← asrb_map.py --apply

HAND-WRITTEN       statistics/bsc/**              168 pages
                   statistics/msc/**               72 pages
                   exams/ugc-net/**                13 pages
                   subjects/**                     15 pages
                   statistics/index.html exams/index.html      2 pages
                   index.html guides/which-test.html 404.html  3 pages

STUBS              the five old section roots     690 files   ← restructure.py
```

A `.nojekyll` file at the root stops GitHub Pages processing anything, so what is committed is
byte-for-byte what a reader gets.

**Reproduce:**
```sh
python3 - <<'PY'
import pathlib, sys; sys.path.insert(0, "tools"); import stubs
p = [q for q in pathlib.Path(".").rglob("*.html") if ".git" not in q.parts]
print(sum(not stubs.is_stub(q) for q in p), "pages,", sum(map(stubs.is_stub, p)), "stubs")
PY
```

---

## 2. Directory tree

The URL is the design and the folders follow it — a reader's address bar and this tree are the
same thing.

```
planning-for-future/
│
├── index.html                    home page + site-wide search        HAND
├── topics.html                   A–Z index, 2,021 topics             GEN
├── 404.html                      styles inlined — served at any depth HAND
├── sitemap.xml  robots.txt       690 URLs, stubs excluded            GEN
├── .nojekyll                     serve the repo as-is
│
├── assets/                       shared front-end
│   ├── nrstatlab.css             home, A–Z, test chooser only
│   ├── site-nav.css              the navigation, on ALL 691 pages     §8
│   ├── search.js                 index fetched on first focus
│   └── search-index.json         690 records                         GEN
│
├── guides/
│   └── which-test.html           13 tests, assumptions, fallbacks    HAND
│
├── tools/                        ALL generators and checkers          §3
│   ├── *.py                      12 site-wide scripts
│   ├── stubs.py                  the one is_stub() the four tree-walkers share
│   ├── restructure.py            the move script — see §7
│   ├── data-science/             22 .py + 5 .sh — build_site.py and the lab runners
│   └── exams/                    15 .py — the four syllabus maps and their rechecks
│
├── docs/
│   ├── GO-LIVE-REPORT.md         pre-launch audit
│   └── ARCHITECTURE.md           this file
│
├── statistics/                   241 pages, HAND-WRITTEN
│   ├── index.html                the programme hub
│   ├── bsc/                      21 subjects, 8 files each
│   │   ├── descriptive-statistics/    index syllabus unit1..5 practical
│   │   ├── theory-of-probability/     + css/styles.css
│   │   └── … 19 more
│   └── msc/                      13 subjects, hyphenated folders, bare filenames
│
├── data-science/                 407 pages, GENERATED
│   ├── notes/                    153 .md — THE SOURCE OF TRUTH
│   ├── labs/                     358 runnable lab sources
│   ├── data/                     52 CSV datasets
│   ├── docs/                     4 syllabus PDFs (third-party)
│   ├── css/styles.css            the whole section
│   ├── machine-learning/         ┐ 19 course folders
│   ├── data-science-r/           │ each: index unit1..5 lab practice
│   ├── … 17 more                 ┘ + one page per lab program
│   └── machine-learning/self-study-notes/   23 algorithms, own CSS + JS
│
├── exams/                        24 pages
│   ├── index.html                the hub                             HAND
│   ├── ugc-net/                  10 units, 500 MCQs, solved paper    HAND
│   ├── iss/                      index + paper1..4, 147 lines graded GEN
│   ├── csir-net/                 index, 52 lines                     GEN
│   ├── appsc/                    index + 2 posts, 73 lines           GEN
│   └── asrb-net/                 index, 99 lines                     GEN
│
├── subjects/                     15 pages, HAND-WRITTEN
│   ├── economics/                index + unit1..6
│   ├── financial-accounting/     index + unit1..6
│   └── css/styles.css            a 22nd byte-identical copy of the subject sheet
│
├── statistics-major/  data-science-major/  statistics-papers/
├── exam-subjects/     ugc-net-statistics/  which-statistical-test.html
│                                 690 redirect stubs, nothing else     §7
│
└── archive/                      kept, not part of the site, unlinked
```

### One naming convention

Before the restructure this section carried two, and it was the thing a new reader tripped on:
BSc folders had spaces and repeated the subject in every filename, MSc folders next to them were
hyphenated with bare filenames. Now both read the same way:

```
statistics/bsc/descriptive-statistics/     index.html syllabus.html
statistics/msc/probability-theory/         unit1.html … unit5.html
data-science/data-mining/                  practical.html  (BSc) / lab.html (DS)
```

**No page path contains a space**, down from 180 such paths, and 0 `<loc>` entries in
`sitemap.xml` carry one, down from 160. The only spaced paths left are 160 of the stubs, and
they have to be: the old URL had a space, so the file that keeps it alive must sit there. They
are excluded from the sitemap, the search index and the A–Z index.

```sh
git ls-files '*.html' | grep ' ' | wc -l          # 160, every one a stub
grep -c '<loc>[^<]* ' sitemap.xml                 #   0
```

### Stylesheets

One production sheet has 22 byte-identical copies:

```sh
md5sum statistics/bsc/*/css/styles.css subjects/css/styles.css \
  | awk '{print $1}' | sort -u | wc -l     # must print 1
```

`tools/add_statistics_navigation.py` writes all of them together; a hand edit must be repeated
22 times.

---

## 3. The Python tooling

Three sets, all now under `tools/`.

### `tools/` — 12 scripts, site-wide

| Script | Reads | Writes |
|---|---|---|
| `build_topic_index.py` | the "Topics Covered" chips on every page | `topics.html` |
| `build_search_index.py` | titles, headings, chips, descriptions | `assets/search-index.json` |
| `build_sitemap.py` | the page tree | `sitemap.xml`, `robots.txt` |
| `check_canonical.py` | the sitemap | `rel=canonical` on all 690; asserts nothing outside has one |
| `check_home_stats.py` | the tree | verifies (`--fix` corrects) the home page's figures |
| `check_no_raw_tex.py` | titles, descriptions, chips, search index | fails if TeX reaches a string MathJax never touches |
| `stubs.py` | an .html file's head | `is_stub()` — the one definition the four tree-walkers share |
| `site_nav_model.py` | the tree, and each hub's own `<title>` | the menu, as data — run it to print all 78 links |
| `add_site_nav.py` | `site_nav_model.py` | the navigation on all 691 pages |
| `check_site_nav.js` | a served copy of the site, in Chromium | fails if the menu is clipped, invisible, off-screen or too tall |
| `restructure.py` | `git ls-files` | the move, the link rewrite and the stub layer (§7) |
| `add_statistics_navigation.py` | `statistics/` only | heading ids + contents lists |
| `add_ugcnet_chips.py` | `exams/ugc-net/` only | the "Topics Covered" chip blocks |
| `retitle_and_describe.py` | the hand-written pages | titles and meta descriptions — one-shot |
| `build_favicon.py` | — | the three favicon files |

The `check_*` scripts are the site's only automated safety net, and **CI runs none of them** —
`.github/workflows/validate.yml` covers 29 of 691 pages.

### `tools/data-science/` — 22 Python + 5 shell, 9,388 lines

| Group | Files | Job |
|---|---|---|
| Site builder | `build_site.py` (2,656 lines) | markdown → 407 pages (§4) |
| Content generators | `make_questions.py`, `make_datasets.py` | the 266 practice questions and 52 datasets |
| Auditors | `check_datasets.py`, `check_coverage.py`, `audit_content.py` | every dataset answer recovered from the file; every syllabus topic mapped; structure and links |
| Lab harnesses | 18 `run_*` scripts (+ 5 `.sh`) | compile and execute the lab programs, per course |
| Extraction | `extract_syllabus.py`, `fetch_nlp_data.py` | the 4 syllabus PDFs → HTML |

`build_site.py` needs **Pygments** — it highlights the code blocks at build time rather than
shipping a syntax highlighter to the browser.

### `tools/exams/` — 15 Python, 2,910 lines

See §5.

---

## 4. Inside `build_site.py`

2,656 lines, and the only file in the repository large enough to need a map. Its own section
banners divide it cleanly:

| Lines | What | Notes |
|---|---|---|
| 46–96 | **Configuration** | `SITE_BASE` (L54) is **the only absolute URL in the repository**. Every internal link is relative, which is what lets the site move to a custom domain without editing a page. `ROOT` is the *section* root, `data-science/`, not the repository root. |
| 102–1049 | **The page inventory** | `COURSES` (L102) is ~850 lines of declarative course data; then `EXTRA_PAGES` (L957), `SIDE_CARDS` (L996), `TOP_PAGES` (L1010). **Data, not logic — most page changes happen here.** |
| 1063–1212 | **Markdown → HTML** | `collapse_practice_answers` (L1063), `add_anchors_and_toc` (L1127), `render_markdown` (L1199) |
| 1216–1294 | **The math shield** | `shield_math` (L1243) hides TeX spans behind a `zzmathshieldzz` sentinel so the Markdown converter cannot mangle them; `unshield_math` (L1265) puts them back. |
| 1296–1380 | **`detex()`** (L1359) | Writes TeX out as real characters for the four places MathJax never reaches: the browser tab, the Google snippet, the A–Z index and the search dropdown. It **fails on a symbol it has never seen** rather than shipping a backslash — `check_no_raw_tex.py` is its guard. |
| 1384–1436 | **Build-time highlighting** | `highlight_code` (L1405), Pygments, `github-dark` |
| 1502–1979 | **Box promotion** | `.concept` / `.formula` / `.example` / `.tip` callouts inferred from markdown shape — `promote_markdown_boxes` (L1606) |
| 2035–2655 | **Page builders** | `build_program_pages` (L2119), `build_language_pages` (L2208), `build_lab_pages` (L2324), `build_course` (L2391), `build_top_pages` (L2550), then `build_link_map` (L2611) → `main` (L2626) |

To add a course page, edit `COURSES`. To change how every page looks, edit the builders. To
change how markdown becomes HTML, edit the middle.

---

## 5. The syllabus-map generators

Ten pages in `exams/` are generated from syllabus data, by 15 scripts in `tools/exams/`. Each
one was proved to reproduce its live page **byte for byte** before being tracked.

| Exam | Pages | Generator | Data | Recheck |
|---|---|---|---|---|
| ISS | 5 | `iss_map.py` | `iss_map_data.py`, `iss_syllabus.txt` | — |
| CSIR NET | 1 | `gen_csir.py` | `csirmap.py` | — |
| APPSC | 3 | `appsc_map.py` | `appsc_map_data.py` | `recheck_appsc.py`, 155 checks |
| ASRB NET | 1 | `asrb_map.py --apply` | `asrb_map_data.py`, `asrb_syllabus.txt` | `recheck_asrb.py`, 523 checks |

Shared: `mapkit.py` (grade tallies, tables, heading ids, gap lists), `labels.py`, `shell_iss.py`
(the page shell), `pdftext.py` and `pdftext_appsc.py` (two PDF text extractors — the header of
the second says why both exist).

Two rules these generators are built on, and both are load-bearing:

- **A link's label is read from the destination page's own `<title>`**, never hand-written, so a
  retitled page cannot end up with a stale label on a map.
- **A recheck is written after the page, from the source document rather than from the
  generator**, and reads the finished HTML — so a bug in the generator cannot hide behind the
  same bug in its check. Each was mutation-tested: a check that has never failed proves nothing.

Two rechecks are still missing: `recheck_fa.py` (115 checks) and `recheck_econ.py` (79) for the
15 pages in `subjects/`. They were written in an ephemeral scratchpad and do not survive, so
those numbers appear in commit messages but **cannot be reproduced from a clean clone.** Those
pages are hand-written and are listed as such in §1.

---

## 6. Build order

The generators have real dependencies. In order, from the repository root:

```
① after editing data-science/notes/**/*.md
   python3 tools/data-science/build_site.py                → 407 HTML pages
   (commit BOTH the markdown and the generated HTML)

② after editing a syllabus map's data file
   cd tools/exams
   python3 iss_map.py ; python3 appsc_map.py
   python3 gen_csir.py ; python3 asrb_map.py --apply
   python3 recheck_asrb.py ; python3 recheck_appsc.py      → must print 0 failures

③ after adding, removing or renaming ANY page
   python3 tools/build_topic_index.py  --apply             → topics.html
   python3 tools/add_site_nav.py       --apply             → the navigation, all 691
   python3 tools/build_search_index.py --apply             → assets/search-index.json
   python3 tools/build_sitemap.py      --apply             → sitemap.xml, robots.txt
   python3 tools/check_canonical.py    --apply             → rel=canonical on all 690
   python3 tools/check_home_stats.py   --fix               → the home page figures

④ always, before committing
   python3 tools/check_no_raw_tex.py
   python3 tools/data-science/audit_content.py             structure, links, formatting
   python3 tools/data-science/check_coverage.py            syllabus topic → notes section
   python3 tools/data-science/check_datasets.py            every answer recovered from the file
   bash    tools/data-science/verify_all.sh                compile and run the lab programs
   cd data-science/machine-learning/self-study-notes && python3 scripts/check_notes.py

⑤ preview
   python3 -m http.server 8000
```

Order matters in ③, in both directions. The topic index reads the chips on every page, and the
search index and sitemap read the page tree, so they run after ① and ②. `add_site_nav.py` runs
after `build_topic_index.py` because that one rewrites `topics.html` whole and would drop the
navigation from it — and before the search index and sitemap, so those read the finished pages.
`check_canonical.py` reads the sitemap and so runs after `build_sitemap.py`; the map generators
deliberately emit no `rel=canonical` of their own, which is why their eight pages differ from
the committed ones until ③ has run.

Anything in ① or ② rewrites a whole page and therefore drops the navigation, which
`add_site_nav.py` then puts back. That is why the sequence is one pass and not a loop: running
it twice leaves the tree byte-identical (`git write-tree` gives the same hash), which is the
thing to check if the order is ever changed.

### Two things that are deliberate and easy to undo by accident

- **Every internal link is relative.** `SITE_BASE` (`tools/data-science/build_site.py:54`) holds
  the only absolute URL, used for `og:url` and the sitemap. Changing domain means rebasing that
  one constant and re-running ③ — nothing else.
- **22 copies of one stylesheet must move together.** `add_statistics_navigation.py` does this
  correctly; a hand edit must be repeated 22 times, including the copy in `subjects/`.

---

## 7. The stub layer

**GitHub Pages has no redirect mechanism.** No `.htaccess`, no `_redirects`, no server rule —
the only thing it offers is `404.html`. So the only way to keep 690 published URLs alive across
a rename is to leave a file at each of them, and that is what `tools/restructure.py` does:

```html
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=../../statistics/bsc/theory-of-probability/unit1.html">
```

No `rel=canonical`: it is meaningless on a `noindex` page, and it would break
`check_canonical.py`'s assertion that nothing outside the sitemap carries one.

`tools/stubs.py` holds the single `is_stub()` test — a meta refresh plus `robots noindex` —
and the four tree-walkers (`build_sitemap`, `build_search_index`, `build_topic_index`,
`check_canonical`) all import it. Without that, every stub would be listed in the sitemap,
indexed by the search box, mined for chips and asserted on as though a reader could land on it.
`robots.txt` disallows the six old roots as well.

### What `restructure.py` learned the hard way

The script is tracked, idempotent and dry-run-first, and four of its rules exist because the
first run broke something:

- **Links are resolved, not pattern-matched.** Every `href`/`src` is resolved against the file's
  *old* directory to an absolute repository path, mapped, then made relative to its *new*
  directory — so a depth change fixes itself, which a regex over `../` could not do. The list of
  old paths must be taken **before** the first `git mv`; taking it afterwards produced 2,507
  broken links.
- **The href/src pass runs on HTML and nothing else.** In Markdown and JavaScript those
  attributes are code, not links: all 20 in the `.md` sources are inside fenced blocks teaching
  HTML, and `search.js` builds a link by concatenation. Rewriting them produced nonsense.
- **`<code>` and `<pre>` are skipped even in HTML**, for the same reason — a lesson that shows
  the reader `href="styles.css"` must keep saying that.
- **Both regexes stop at a newline.** `[^"]*` ran from a URL in one line past every newline to
  the next quotation mark 35 lines later and percent-encoded everything between. That is what it
  did to `README.md`, `docs/GO-LIVE-REPORT.md` and, worst, `sitemap.xml`, where one match
  swallowed the whole file.

---

## 8. The navigation

One bar on all 691 pages, replacing three patterns that were doing the job between them: a site
bar on 17 pages, a sticky 13-link row on the UGC NET pages, and nothing at all on 23. 675 pages
had no route to the rest of the site, and not one page anywhere carried `aria-current` or a skip
link.

```
NRSTATLAB   Statistics ▾   Data Science ▾   Examinations ▾   Subjects ▾   Topics A–Z   Which test?
```

- **`tools/site_nav_model.py`** is the menu as data — 77 links, built from the tree, every label
  read from the destination page's own `<title>` (the rule the syllabus maps use). Run it on its
  own to print the whole menu with its targets and check that each one exists.
- **`tools/add_site_nav.py`** writes it into every page, idempotently, and removes the two
  patterns it replaces. It must run after anything that rewrites a whole page — see §6 ③.
- **`assets/site-nav.css`** is one file, linked last on every page. Four of the five stylesheets
  style *every* `<details>`, so the first block of that file exists only to undo their chrome
  inside the bar.
- **`tools/check_site_nav.js`** opens the site in Chromium at 1180px, at 400px, and once more
  with JavaScript disabled.

**No JavaScript.** The menu is `<details>`/`<summary>`, which the site already uses 1,829 times,
so it is the house mechanism rather than a new dependency. Click to open, which is also the only
thing that works on a touch screen. The breadcrumb stays: it answers a different question — where
am I — and it is the only thing that does.

### What only a browser caught

The HTML was right the whole time these two faults existed, and every text-level check passed:

- the subject stylesheets paint every `<summary>` `#0f4c81`, which is this bar's own background,
  so on 240 pages all four menu labels were dark blue on dark blue — in the DOM, in the
  accessibility tree, correctly positioned, and invisible;
- those sheets also set `details { overflow: hidden }` to round the corners of a collapsible
  proof, which clipped the open menu to the height of its own summary. The panel still measured
  532px and still reported itself visible.

`check_site_nav.js` therefore asks the browser what is *painted* at three points inside the open
panel, and compares each label's computed colour with the bar's computed background. Both checks
are mutation tested: restoring `overflow: hidden` fails 11 of 33 loads, and removing the colour
reset fails 12, naming four invisible labels on each subject page.

The phone bar is **80px on every page**, two rows, against the ~120px the sticky row it replaced
took out of a 400px viewport — and the UGC NET pages lose nothing, because those 13 pages are
listed inside the Examinations menu, which costs no vertical space until a reader opens it.

---

## Where to start reading

| If you want to… | Open |
|---|---|
| add or change a Data Science page | `data-science/notes/**/*.md`, then §6 ① |
| add a Data Science *course* | `COURSES` at `tools/data-science/build_site.py:102` |
| change how any generated page looks | the builders, `build_site.py:2035`+ |
| change a Statistics unit | the HTML directly — it is hand-written |
| change a syllabus map | the data file in `tools/exams/`, then §6 ② |
| move or rename anything | `tools/restructure.py` and §7 — never `git mv` by hand |
| change what is in the menu | `tools/site_nav_model.py`, then §6 ③ |
| know what to fix before launch | `docs/GO-LIVE-REPORT.md` |
