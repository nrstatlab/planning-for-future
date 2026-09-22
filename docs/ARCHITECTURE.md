# NRSTATLAB — code hierarchy and architecture

**As of** 22 September 2026, commit `c098c13`. Every count here was measured from the tree at
that commit, and each one carries the command that produced it.

This is the long version of the README's "Repository layout" block. The README tells you where
files sit; this tells you how they are produced, which matters because **editing the wrong file
throws the work away.**

---

## Contents

1. [The three build regimes](#1-the-three-build-regimes)
2. [Directory tree](#2-directory-tree)
3. [The Python tooling](#3-the-python-tooling)
4. [Inside `build_site.py`](#4-inside-build_sitepy)
5. [The gap: two sections have no generator](#5-the-gap-two-sections-have-no-generator)
6. [Build order](#6-build-order)

---

## 1. The three build regimes

691 pages, produced three different ways.

| Regime | Pages | Source of truth | Where you edit |
|---|---|---|---|
| **Generated** | 409 | `data-science-major/notes/**/*.md`, plus the page tree for `topics.html` | the markdown or the generator — **never the HTML** |
| **Hand-written** | 257 | the HTML itself | the HTML |
| **Generated, generator absent** | 25 | *not in this repository* — see §5 | nothing safely; §5 explains |

Which is which:

```
GENERATED          data-science-major/**          408 pages   ← build_site.py
                   topics.html                      1 page    ← build_topic_index.py
                   sitemap.xml robots.txt                     ← build_sitemap.py
                   assets/search-index.json                   ← build_search_index.py

HAND-WRITTEN       statistics-major/**            241 pages
                   ugc-net-statistics/**           13 pages
                   index.html                       1 page
                   which-statistical-test.html      1 page
                   404.html                         1 page

NO GENERATOR       statistics-papers/**            10 pages   ← scripts not tracked
HERE               exam-subjects/**                15 pages   ← scripts not tracked
```

A `.nojekyll` file at the root stops GitHub Pages processing anything, so what is committed is
byte-for-byte what a reader gets.

**Reproduce:**
```sh
git ls-files 'data-science-major/*.html' | wc -l      # 408
git ls-files 'statistics-major/*.html'   | wc -l      # 241
git ls-files '*.html' | grep -vc '/'                  #   4 top-level, one of them generated
```

---

## 2. Directory tree

```
planning-for-future/
│
├── index.html                    home page + site-wide search        HAND
├── topics.html                   A–Z index, 1,918 topics, 425 KB     GEN
├── which-statistical-test.html   13 tests, assumptions, fallbacks    HAND
├── 404.html                      styles inlined — served at any depth HAND
├── sitemap.xml  robots.txt       690 URLs                            GEN
├── .nojekyll                     serve the repo as-is
│
├── assets/                       shared front-end for the 3 top pages
│   ├── nrstatlab.css             16 KB — home, A–Z, test chooser only
│   ├── search.js                 9 KB — index fetched on first focus
│   └── search-index.json         391 KB, 690 records                 GEN
│
├── tools/                        9 site-wide scripts, 1,324 lines    §3
│
├── docs/
│   ├── GO-LIVE-REPORT.md         pre-launch audit
│   └── ARCHITECTURE.md           this file
│
├── statistics-major/             241 pages, HAND-WRITTEN
│   │                             ⚠ TWO naming conventions, see below
│   ├── descriptive statistics/   ┐ 21 BSc subjects, 9 files each
│   ├── theory of probability/    │ folder names contain SPACES
│   ├── … 19 more                 ┘ subject name repeated in every filename
│   └── msc/                      13 MSc subjects, 73 files
│                                 hyphenated folders, bare filenames
│
├── data-science-major/           408 pages, GENERATED
│   ├── notes/                    153 .md — THE SOURCE OF TRUTH
│   ├── tools/                    22 .py + 5 .sh, 9,383 lines         §3
│   ├── labs/                     358 runnable lab sources
│   ├── data/                     52 CSV datasets
│   ├── docs/                     4 syllabus PDFs (third-party)
│   ├── css/styles.css            20 KB — the whole section
│   ├── data-science-r/       41  ┐
│   ├── machine-learning/     35  │ 19 course folders
│   ├── python-data-structures/30 │ each: index_ unit1..5_ lab_
│   ├── … 16 more                 ┘ practice_ + per-program topic pages
│   └── machine-learning/self-study-notes/   23 algorithms, own CSS + JS
│
├── ugc-net-statistics/           13 pages, HAND-WRITTEN
│   ├── styles.css                the only sheet with NO @media print
│   └── unit1..10, mcqs, pyq2026  500 MCQs + solved paper
│
├── statistics-papers/            10 pages, GENERATOR NOT TRACKED  ⚠ §5
│   ├── iss/     index + paper1..4       147 syllabus lines graded
│   ├── csir-net/index                    52 lines
│   └── appsc/   index + 2 posts          73 lines
│
├── exam-subjects/                15 pages, GENERATOR NOT TRACKED  ⚠ §5
│   ├── economics/           index + unit1..6
│   ├── financial-accounting/index + unit1..6
│   └── css/styles.css       ← a 23rd byte-identical copy of the subject sheet
│
└── archive/                      kept, not part of the site, unlinked
```

### The two naming conventions inside `statistics-major`

This is the thing a new reader trips on. Both live in the same section:

```
statistics-major/descriptive statistics/          ← BSc: SPACES in the folder name
    index_descriptive statistics.html             ← subject repeated in every filename
    syllabus_descriptive statistics.html
    unit1_descriptive statistics.html  … unit5_
    practical_descriptive statistics.html
    css/styles.css

statistics-major/msc/probability-theory/          ← MSc: hyphenated, no spaces
    index.html  syllabus.html  unit1.html … unit4.html
```

180 tracked paths contain spaces, all of them in the 20 BSc subject folders. They become `%20`
URLs, and 160 of them appear unencoded in `sitemap.xml` — see the go-live report §1.5.

### Stylesheets

31 CSS files, **5 distinct** production sheets. One of them has 23 byte-identical copies:

```sh
md5sum statistics-major/*/css/styles.css exam-subjects/css/styles.css \
  | awk '{print $1}' | sort -u | wc -l     # must print 1
```

The README documents this check but omits `exam-subjects/`, so that copy can drift unnoticed.

---

## 3. The Python tooling

Two sets, and they are not peers.

### `tools/` — 9 scripts, 1,324 lines, site-wide

| Script | Reads | Writes |
|---|---|---|
| `build_topic_index.py` | the "Topics Covered" chips on every page | `topics.html` |
| `build_search_index.py` | titles, headings, chips, descriptions | `assets/search-index.json` |
| `build_sitemap.py` | the page tree | `sitemap.xml`, `robots.txt` |
| `check_canonical.py` | the sitemap | `rel=canonical` on all 690; asserts nothing outside has one |
| `check_home_stats.py` | the tree | verifies (`--fix` corrects) the home page's figures |
| `check_no_raw_tex.py` | titles, descriptions, chips, search index | fails if TeX reaches a string MathJax never touches |
| `add_statistics_navigation.py` | `statistics-major/` only | heading ids + contents lists — one-shot migration |
| `retitle_and_describe.py` | the hand-written pages | titles and meta descriptions — one-shot |
| `build_favicon.py` | — | the three favicon files |

The three `check_*` scripts are the site's only automated safety net, and **CI runs none of
them** — `.github/workflows/validate.yml` covers 29 of 691 pages.

### `data-science-major/tools/` — 22 Python + 5 shell, 9,383 lines

| Group | Files | Lines | Job |
|---|---|---|---|
| Site builder | `build_site.py` | 2,651 | markdown → 408 pages (§4) |
| Content generators | `make_questions.py`, `make_datasets.py` | 2,963 | the 266 practice questions and 52 datasets |
| Auditors | `check_datasets.py`, `check_coverage.py`, `audit_content.py` | 1,837 | every dataset answer recovered from the file; every syllabus topic mapped; structure and links |
| Lab harnesses | 18 `run_*` scripts (+ 5 `.sh`) | ~1,900 | compile and execute the lab programs, per course |
| Extraction | `extract_syllabus.py`, `fetch_nlp_data.py` | 202 | the 4 syllabus PDFs → HTML |

`build_site.py` needs **Pygments** — it highlights 1,068 code blocks at build time rather than
shipping a syntax highlighter to the browser.

---

## 4. Inside `build_site.py`

2,651 lines, and the only file in the repository large enough to need a map. Its own section
banners divide it cleanly:

| Lines | What | Notes |
|---|---|---|
| 46–93 | **Configuration** | `SITE_BASE` (L51) is **the only absolute URL in the repository**. Every internal link is relative, which is what lets the site move to a custom domain without editing a page. This is the one constant to rebase. |
| 99–1046 | **The page inventory** | `COURSES` (L99) is ~850 lines of declarative course data; then `EXTRA_PAGES` (L954), `TOP_PAGES` (L1007), `SIDE_CARDS`. **Data, not logic — most page changes happen here.** |
| 1052–1209 | **Markdown → HTML** | `collapse_practice_answers` (L1060), `add_anchors_and_toc` (L1124), `render_markdown` (L1196) |
| 1213–1291 | **The math shield** | `shield_math` (L1240) hides TeX spans behind a `zzmathshieldzz` sentinel so the Markdown converter cannot mangle them; `unshield_math` (L1262) puts them back. |
| 1293–1377 | **`detex()`** (L1356) | Writes TeX out as real characters for the four places MathJax never reaches: the browser tab, the Google snippet, the A–Z index and the search dropdown. It **fails on a symbol it has never seen** rather than shipping a backslash — `check_no_raw_tex.py` is its guard. |
| 1381–1433 | **Build-time highlighting** | `highlight_code` (L1402), Pygments, `github-dark` |
| 1499–1976 | **Box promotion** | `.concept` / `.formula` / `.example` / `.tip` callouts inferred from markdown shape — `promote_markdown_boxes` (L1603) |
| 2032–2650 | **Page builders** | `build_program_pages` (L2116), `build_language_pages` (L2205), `build_lab_pages` (L2319), `build_course` (L2386), `build_top_pages` (L2545), then `build_link_map` (L2606) → `main` (L2621) |

To add a course page, edit `COURSES`. To change how every page looks, edit the builders. To
change how markdown becomes HTML, edit the middle.

---

## 5. The gap: two sections have no generator

**The repository tracks 224 Python files. Every one is under `data-science-major/` or `tools/`.**

```sh
git ls-files '*.py' | awk -F/ '{print $1}' | sort | uniq -c
#  215 data-science-major
#    9 tools
```

There is nothing for `statistics-papers/` or `exam-subjects/`. Those 25 pages were produced by
**33 scripts that are not in this repository**:

| Section | Pages | Scripts, and where they are not |
|---|---|---|
| shared | — | `mapkit.py` — grade tallies, tables, heading ids, the gap lists |
| `statistics-papers/iss/` | 5 | `iss_map.py`, `iss_map_data.py`, `labels.py`, `shell_iss.py` |
| `statistics-papers/csir-net/` | 1 | `csirmap.py`, `gen_csir.py` |
| `statistics-papers/appsc/` | 3 | `appsc_map.py`, `appsc_map_data.py`, `pdftext.py`, `recheck_appsc.py` |
| `exam-subjects/` | 15 | 22 files — `ec1`–`ec6`, `fa1`–`fa6`, `ec_common`, `fa_common`, two index builders, `hub.py`, and the `verify_*` / `recheck_*` pairs |

They exist only in an ephemeral session scratchpad, which does not survive.

### What this costs, concretely

- **Those 25 pages can only be hand-edited** — in a repository whose README says hand-editing a
  generated file is destroyed by the next run. Here there is no next run, so the danger is the
  opposite one: the HTML and the data that produced it have silently diverged, permanently.
- **The verification goes with them.** `recheck_appsc.py` (155 checks against the source PDFs),
  `recheck_fa.py` (115), `recheck_econ.py` (79). Those numbers appear in commit messages and
  **cannot be reproduced from a clean clone.**
- **The PDF extraction cannot be repeated.** The APPSC syllabus text was lifted from the two
  official notifications by an untracked `pdftext.py` that decodes subset-CID fonts through each
  font's own `/ToUnicode` CMap — written because no PDF tool was available in the environment.
- **`mapkit.py` is shared by both maps.** A change to how grades are tallied or gaps are listed
  would have to be made twice by hand, in HTML, with nothing checking they agree.

### The two ways out

1. **Track them.** Add the 33 scripts under something like `statistics-papers/tools/` and
   `exam-subjects/tools/`. Those sections become rebuildable and the rechecks become CI-able.
   This is real code entering the repository and deserves its own review.
2. **Accept those pages as hand-written**, and say so in the README and here. Honest, cheaper,
   and consistent with `statistics-major/` — but the rechecks stay unreproducible.

This document records the finding. The choice is not made here.

---

## 6. Build order

The generators have real dependencies, and the README gives them only as scattered prose. In
order, from the repository root:

```
① after editing notes/**/*.md
   python3 data-science-major/tools/build_site.py          → 408 HTML pages
   (commit BOTH the markdown and the generated HTML)

② after adding, removing or renaming ANY page
   python3 tools/build_topic_index.py  --apply             → topics.html
   python3 tools/build_search_index.py --apply             → assets/search-index.json
   python3 tools/build_sitemap.py      --apply             → sitemap.xml, robots.txt
   python3 tools/check_canonical.py    --apply             → rel=canonical on all 690
   python3 tools/check_home_stats.py   --fix               → the home page figures

③ always, before committing
   python3 tools/check_no_raw_tex.py
   cd data-science-major
   python3 tools/audit_content.py                          structure, links, formatting
   python3 tools/check_coverage.py                         syllabus topic → notes section
   python3 tools/check_datasets.py                         every answer recovered from the file
   bash    tools/verify_all.sh                             compile and run the lab programs
   cd machine-learning/self-study-notes && python3 scripts/check_notes.py

④ preview
   python3 -m http.server 8000
```

Order matters in ②: the topic index reads the chips on every page, and the search index and
sitemap read the page tree — so they must run after `build_site.py`, not before.

### Two things that are deliberate and easy to undo by accident

- **Every internal link is relative.** `SITE_BASE` (`build_site.py:51`) holds the only absolute
  URL, used for `og:url` and the sitemap. Changing domain means rebasing that one constant and
  re-running ② — nothing else.
- **23 copies of one stylesheet must move together.** `add_statistics_navigation.py` does this
  correctly; a hand edit must be repeated 23 times, including the copy in `exam-subjects/` that
  the README's md5 check does not cover.

---

## Where to start reading

| If you want to… | Open |
|---|---|
| add or change a Data Science page | `data-science-major/notes/**/*.md`, then §6 ① |
| add a Data Science *course* | `COURSES` at `build_site.py:99` |
| change how any generated page looks | the builders, `build_site.py:2032`+ |
| change a Statistics unit | the HTML directly — it is hand-written |
| change a syllabus map | read §5 first |
| know what to fix before launch | `docs/GO-LIVE-REPORT.md` |
