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
9. [Presentation: trust, one visual system, dark mode](#9-presentation-trust-one-visual-system-dark-mode)
10. [Reader progress](#10-reader-progress)
11. [Folded topic sections on long pages](#11-folded-topic-sections-on-long-pages)
12. [The home page's three columns](#12-the-home-pages-three-columns)
13. [A solved question paper, from the Commission's own PDF](#13-a-solved-question-paper-from-the-commissions-own-pdf)

---

## 1. The three build regimes

691 pages, produced three different ways — plus one archived file that is not part of the
site, and 946 stubs that are not pages at all.

| Regime | Pages | Source of truth | Where you edit |
|---|---|---|---|
| **Generated** | 408 | `data-science/notes/**/*.md`, plus the page tree for `topics.html` | the markdown or the generator — **never the HTML** |
| **Generated from syllabus data** | 11 | the data files in `tools/exams/` | the data file, then re-run its generator |
| **Hand-written** | 272 | the HTML itself (the two course hubs' course lists: `tools/course_catalogue.py`) | the HTML |

Which is which:

```
GENERATED          data-science/**                407 pages   ← build_site.py
                   topics.html                      1 page    ← build_topic_index.py
                   assets/topics-index.json                   ← build_topic_index.py
                   sitemap.xml robots.txt                     ← build_sitemap.py
                   assets/search-index.json                   ← build_search_index.py

                   exams/iss/       5 pages                   ← iss_map.py
                   exams/appsc/     3 pages                   ← appsc_map.py
                   exams/appsc/solved-2025-paper-ii.html  1   ← appsc_paper.py --apply
                   exams/csir-net/  1 page                    ← gen_csir.py
                   exams/asrb-net/  1 page                    ← asrb_map.py --apply
                   exams/ugc-net/index.html  1 page           ← ugc_map.py --apply
                   (the UGC NET hub is its map, as for the other four)

                   the course lists on statistics/index.html and
                   data-science/index.html                    ← build_course_hubs.py

HAND-WRITTEN       statistics/<course>/**         253 pages   36 courses
                   exams/ugc-net/** (not index)    12 pages
                   statistics/index.html exams/index.html      2 pages
                   index.html guides/which-test.html 404.html  3 pages
                   about.html                                  1 page

STUBS              the six old section roots      690 files   ← restructure.py
                   statistics/bsc/ statistics/msc/ subjects/
                                                  255 files   ← restructure2.py
                   exams/ugc-net/syllabus-map.html  1 file    (by hand, when the map became the hub)
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
│   ├── search.js                 index fetched on first focus; data-inline on the home page
│   ├── az.js                     the home page's A–Z column
│   ├── topics-index.json         2,021 topics by letter, for az.js     GEN
│   ├── sections.js               folds topic sections on long pages
│   └── search-index.json         690 records                         GEN
│
├── guides/
│   └── which-test.html           13 tests, assumptions, fallbacks    HAND
│
├── tools/                        ALL generators and checkers          §3
│   ├── *.py                      12 site-wide scripts
│   ├── stubs.py                  the one is_stub() the four tree-walkers share
│   ├── restructure.py            the first move script — see §7
│   ├── restructure2.py           the second: one Statistics, no programmes — §7
│   ├── course_catalogue.py       every course, in learning order — §8
│   ├── data-science/             22 .py + 5 .sh — build_site.py and the lab runners
│   └── exams/                    19 .py — the five syllabus maps and their rechecks
│
├── docs/
│   ├── GO-LIVE-REPORT.md         pre-launch audit
│   └── ARCHITECTURE.md           this file
│
├── statistics/                   254 pages, HAND-WRITTEN
│   ├── index.html                the one course hub, course list GENERATED
│   ├── descriptive-statistics/   ┐ 36 course folders, one catalogue
│   ├── probability-theory/       │ each: index unit1..N practical
│   ├── economics/                │ (economics, financial-accounting: allied)
│   ├── … 33 more                 ┘ 21 carry their own css/styles.css
│   └── css/styles.css            the sheet the other 15 share
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
├── statistics-major/  data-science-major/  statistics-papers/
├── exam-subjects/     ugc-net-statistics/  which-statistical-test.html
│                                 690 redirect stubs, nothing else     §7
├── statistics/bsc/  statistics/msc/  subjects/
│                                 255 redirect stubs, nothing else     §7
│
└── archive/                      kept, not part of the site, unlinked
```

### One naming convention

Before the first restructure this section carried two, and it was the thing a new reader
tripped on: BSc folders had spaces and repeated the subject in every filename, MSc folders next
to them were hyphenated with bare filenames. After the second there is also no programme in the
path at all — a course is a course:

```
statistics/descriptive-statistics/         index.html syllabus.html
statistics/probability-theory/             unit1.html … unit4.html
data-science/data-mining/                  practical.html (Statistics) / lab.html (DS)
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
md5sum statistics/*/css/styles.css statistics/css/styles.css \
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
| `build_topic_index.py` | the "Topics Covered" chips on every page | `topics.html`, and `assets/topics-index.json` from the same grouping for the home page's A–Z column |
| `build_search_index.py` | titles, headings, chips, descriptions | `assets/search-index.json` |
| `build_sitemap.py` | the page tree | `sitemap.xml`, `robots.txt` |
| `check_canonical.py` | the sitemap | `rel=canonical` on all 690 indexed pages; asserts nothing outside has one |
| `check_home_stats.py` | the tree | verifies (`--fix` corrects) the home page's figures |
| `check_no_raw_tex.py` | titles, descriptions, chips, search index | fails if TeX reaches a string MathJax never touches |
| `stubs.py` | an .html file's head | `is_stub()` — the one definition the four tree-walkers share |
| `course_catalogue.py` | — | every course in learning order; fails if a folder is missing or listed twice |
| `build_course_hubs.py` | `course_catalogue.py` | the course lists on the Statistics and Data Science hubs |
| `build_exam_courses.py` | the links on every exam page | "Courses for this exam" on each exam hub; "Useful for" and "Next course" on each course hub |
| `build_progress_index.py` | the catalogue and the course folders | `assets/progress-index.json` — the markable units of every course, for `assets/progress.js`; `role_of()` tells `add_site_nav.py` which pages load that script |
| `check_home.js` | a served copy, in Chromium | the home page's three columns at 1280, 900 and 390px; a search answered inside the middle column and left there when the reader clicks elsewhere; Escape; a letter's topics listed in the column, as many as `topics-index.json` holds; a letter clearing a search; a letter still reaching `topics.html` with the data unreachable or scripts off |
| `check_sections.js` | a served copy, in Chromium | on four long pages, twice (with and without the browser's `hidden="until-found"`): first section open and the rest closed, heading clicks, Open all / Close all, `#links` to a heading or into a section, contents-list links, nothing of the page's own navigation folded, print shows everything, no text lost, nothing at all with scripts off |
| `check_progress.js` | a served copy, in Chromium | marks a unit done and follows it to the course home, hub, exam hub and home page; clears it; and proves nothing appears with scripts off or storage blocked |
| `check_catalogue.py` | the finished pages | fails if the menu leaves catalogue order, a title, breadcrumb or hub heading says Semester/BSc/MSc, or an exam–course link has no link behind it (also in CI) |
| `retire_programme_labels.py` | the Statistics pages | one-shot: took the programme and semester out of their titles, breadcrumbs, banners, footers and framing prose |
| `data-science/retire_course_numbers.py` | `data-science/notes/**/*.md` | one-shot: "Course 5" became the course's name; the semester and elective-track sentences reworded |
| `site_nav_model.py` | the catalogue, and each page's own `<title>` | the menu, as data — run it to print all 77 links |
| `add_site_nav.py` | `site_nav_model.py` | the navigation on all 691 pages |
| `check_site_nav.js` | a served copy of the site, in Chromium | fails if the menu, footer, favicon, share card, search, reading measure, one-colour rules or print layout break |
| `check_contrast.js` | a served copy, in Chromium, light and dark | every text element against the background actually painted behind it; fails below WCAG AA |
| `build_dark_theme.py` | every stylesheet, `<style>` block and colour `style=` attribute | `assets/site-dark.css` (plus `dark_theme_extra.css`, hand-written) |
| `content_dates.py` | one `git log` over the whole history | the "Content last updated" date for each page |
| `build_og_card.js` | — | `assets/og-card.jpg`, the 1200×630 share card |
| `restructure.py` | `git ls-files` | the move, the link rewrite and the stub layer (§7) |
| `restructure2.py` | `git ls-files` | the second move: programmes out of the URL, stubs re-pointed (§7) |
| `add_statistics_navigation.py` | `statistics/` only | heading ids + contents lists |
| `add_ugcnet_chips.py` | `exams/ugc-net/` only | the "Topics Covered" chip blocks |
| `retitle_and_describe.py` | the hand-written pages | titles and meta descriptions — one-shot |
| `build_favicon.py` | — | the three favicon files |

The `check_*` scripts are the site's only automated safety net, and **CI runs only one of them, `check_catalogue.py`** —
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
| APPSC 2025 Paper-II, solved | 1 | `appsc_paper.py --apply` | `appsc_paper_data.py` (the working, topics, flags), `appsc_paper_2025.json` (from `pdftext_appsc_paper.py` and `docs/sources/appsc-aso-2025-paper-ii.pdf`) | `recheck_appsc_paper.py`, 1,047 checks |
| UGC NET | 1 | `ugc_map.py --apply` | `ugc_map_data.py`, `ugc_syllabus.txt` (from `pdftext_ugc.py` and `docs/sources/ugc-net-statistics-code-107.pdf`) | `recheck_ugc.py`, 502 checks |

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
15 allied-course pages (`statistics/economics/`, `statistics/financial-accounting/`). They were written in an ephemeral scratchpad and do not survive, so
those numbers appear in commit messages but **cannot be reproduced from a clean clone.** Those
pages are hand-written and are listed as such in §1.

---

## 6. Build order

**`bash tools/build_all.sh` runs ① to ③ below in order.** The steps are listed so each can be
run alone; the script is the order.

The generators have real dependencies. In order, from the repository root:

```
① after editing data-science/notes/**/*.md
   python3 tools/data-science/build_site.py                → 407 HTML pages
   (commit BOTH the markdown and the generated HTML)

② after editing a syllabus map's data file
   cd tools/exams
   python3 iss_map.py ; python3 appsc_map.py
   python3 gen_csir.py ; python3 asrb_map.py --apply ; python3 ugc_map.py --apply
   python3 appsc_paper.py --apply
   python3 recheck_asrb.py ; python3 recheck_appsc.py ; python3 recheck_ugc.py
   python3 recheck_appsc_paper.py                                         → 0 failures

③ after adding, removing or renaming ANY page, or editing ANY stylesheet
   python3 tools/course_catalogue.py                       → must print 0 problems
   python3 tools/build_course_hubs.py  --apply             → the two hubs' course lists
   python3 tools/build_exam_courses.py --apply             → exam ↔ course blocks, next-course links
   python3 tools/build_progress_index.py --apply           → assets/progress-index.json
   python3 tools/build_dark_theme.py   --apply             → assets/site-dark.css
   python3 tools/build_topic_index.py  --apply             → topics.html, assets/topics-index.json
   python3 tools/add_site_nav.py       --apply             → bar, footer and <head> tags, all 690
   python3 tools/build_search_index.py --apply             → assets/search-index.json
   python3 tools/build_sitemap.py      --apply             → sitemap.xml, robots.txt
   python3 tools/check_canonical.py    --apply             → rel=canonical on all 690
   python3 tools/check_home_stats.py   --fix               → the home page figures
   python3 tools/check_catalogue.py                        → must print "agree"

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
  correctly; a hand edit must be repeated 22 times, including the shared `statistics/css/`.

---

## 7. The stub layer

**GitHub Pages has no redirect mechanism.** No `.htaccess`, no `_redirects`, no server rule —
the only thing it offers is `404.html`. So the only way to keep 946 published URLs alive across
two renames is to leave a file at each of them, and that is what `tools/restructure.py` and
`tools/restructure2.py` do:

```html
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url=../../statistics/theory-of-probability/unit1.html">
```

**No stub points at another stub.** When the second restructure moved a page, the stub the
first one had left for it was re-pointed straight at the new address, so every old URL — from
either scheme — lands on the page in one hop. One pre-existing two-hop chain (an old ML notes
URL) was flattened at the same time.

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
NRSTATLAB   Examinations ▾   Statistics ▾   Data Science ▾   Topics A–Z   Which test?
```

- **Examinations comes first**, because the site is for exam preparation: its menu lists the
  NET exams (UGC, CSIR, ASRB), then the other exams (ISS, APPSC). The UGC NET units are
  reached from its hub, not the menu.
- **Statistics and Data Science list course names, not programmes or semesters**, in the topic
  groups and learning order of **`tools/course_catalogue.py`** — the one place that order is
  written. Where a topic has a Foundation and an Advanced course, both are listed side by side.
  The catalogue fails if a course folder on disk is missing from it or listed twice, so a new
  course cannot silently fall out of the menu.
- **`tools/site_nav_model.py`** is the menu as data — 77 links, built from the catalogue, every
  label read from the destination page's own `<title>` (the rule the syllabus maps use). Run it
  on its own to print the whole menu with its targets and check that each one exists.
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

## 9. Presentation: trust, one visual system, dark mode

What a first-time visitor judges a site by, measured rather than eyeballed. See
`docs/GO-LIVE-REPORT.md` for the audit that asked for it.

**Trust.** `about.html` says who writes the material (NRSTATLAB), how it is written and
checked, the examination-details rule, how to report an error (GitHub Issues — no email is
published), the CC BY-NC-SA 4.0 licence, and that the four third-party syllabus PDFs are not
NRSTATLAB's to license. Every page ends with one site footer — About, Report an error,
Licence, Topics A–Z, and **when that page's content last changed**. That date comes from
`tools/content_dates.py`, which follows history back through the restructure (a *copy* in git,
because a stub was left behind) and skips site-wide mechanical commits: those named in the tool,
and any commit carrying the trailer `Site-chrome: yes`. **Put that trailer on any future commit
that touches every page without changing what they teach**, or every page will be dated that day.

**Brand.** Favicon links and the `og:image` share card on every page, and schema.org JSON-LD —
`LearningResource`, `CollectionPage` for hubs, `AboutPage`, `WebSite`, and a `BreadcrumbList`
named from each folder's own hub title. Deliberately no `Course` (it asks for providers and
schedules the site does not have) and no `SearchAction` (the search has no URL to call).

**One visual system.** `assets/site-base.css` is linked on every page after the section's own
sheet and before the chrome: one link colour, one page ground, one header card, a 75-character
reading measure, a numbered "start here" path, and a block of contrast corrections — each the
smallest darker shade of the same hue that passes. `check_contrast.js` found the light theme,
which nothing had ever measured, with 2,870 of 16,371 text elements below WCAG AA; it is now 0.

**Dark mode.** Generated, not written: `build_dark_theme.py` reads every rule that sets a
colour and writes the same selector back inside `prefers-color-scheme: dark`, with light
surfaces moved dark and dark text moved light, same hue. Tokens are resolved the way the
browser resolves them — the sheet's own, then `site-base.css` on top, since it is linked later —
and colours written in `style=` attributes are matched by attribute with `!important`, the one
place the site needs it. Diagrams keep a light panel instead of being inverted. It is trusted
only because `check_contrast.js` passes on both themes: 0 of 32,742 text elements below AA.
**Re-run the generator after editing any stylesheet**, or the dark theme falls behind it.

**Print.** The bar, search and footer links are hidden, tables that scroll on screen are
un-scrolled so no column is cut off an A4 page, and in-site navigation is dropped from paper.

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
| change a colour anywhere | the section sheet or `assets/site-base.css`, then `build_dark_theme.py --apply` and `check_contrast.js` |
| know what to fix before launch | `docs/GO-LIVE-REPORT.md` |

---

## 10. Reader progress

A visitor can mark a unit done and pick up where they left off. **It is kept in their own
browser and nowhere else**: one `localStorage` key, `nrstatlab.progress.v1`, holding
`{v, done: {page id: date}, last: {path, title, at}}`. Nothing is sent anywhere, there are no
accounts, and progress does not follow a reader to another device. The About page says so and
has the "Clear my progress" button.

- **`assets/progress.js`** is loaded only where it acts. `add_site_nav.py` writes
  `data-progress="unit"` on unit pages (the toggle, and "last page read") and
  `data-progress="summary"` on hubs, course homes, exam hubs, the home page and About (totals).
  Every other page loads nothing for it.
- **A page id is its path from the site root** (`statistics/sampling-theory/unit2.html`), worked
  out from the script's own `src`, so it is right at any depth. Those ids are the keys a future
  account system would sync.
- **What counts as a unit** comes from `assets/progress-index.json`, built by
  `tools/build_progress_index.py` from the catalogue and the folders: every `unitN.html`, then
  `practical.html` or `lab.html`. UGC NET's ten units, MCQ bank and solved paper count as one
  course. `check_catalogue.py` asserts every course is in it and every listed file exists.
- **With scripts off, or storage blocked** (a private window), every page is exactly as
  published. `tools/check_progress.js` proves both, and each of its assertions was broken once
  and failed.

---

## 11. Folded topic sections on long pages

A long page opens with its first topic section showing and the rest folded to their headings,
with "Open all · Close all" above them.

- **Which pages.** `add_site_nav.collapsible()` decides at build time: at least four topic
  headings (`<h2 id>`, not "Topics Covered") and at least 1,500 words, and not a hub
  (`index.html`), `topics.html` or `404.html`. About 276 pages qualify, and only those load
  `assets/sections.js`, after `progress.js`.
- **What it does.** Each topic heading's text moves into a `<button aria-expanded>` inside the
  same `<h2>`, which keeps its `id`, so every link and syllabus-map anchor still lands. The
  following siblings, up to the next `<h2>`, move into a `div.sec-body`. The page's own
  navigation and generated blocks (`.page-nav`, `.pagination`, the unit toggle,
  `p.next-course`, "Courses for this exam", `footer`) end a section and are never folded.
- **Links, find and print.**
  - A `#link` to a heading, or to anything inside a folded section, opens that section. This
    works on load and on `hashchange`.
  - Folded sections are `hidden="until-found"` where the browser supports it, so find-in-page
    reaches them.
  - Printing opens everything, and a print rule backs that up.
- **With scripts off** the page is exactly as published. `tools/check_sections.js` proves all
  of this; each assertion was broken once and failed. `check_contrast.js` opens every folded
  section before it measures.

---

## 12. The home page's three columns

Examinations on the left, **Topics A–Z** in the middle, study material on the right.

- **Widths.**
  - At 1100px and wider, three columns side by side, with the middle one sticky while the
    others scroll.
  - Below that, the A–Z column spans the top, with the other two side by side beneath it.
  - Under 700px, one column in source order: Examinations, A–Z, study material.
- **The middle column answers in the middle column.**
  - Its search box is the site search (`assets/search.js`, the same index). `data-inline` on
    the `.search` block makes the results a list in the column rather than a box dropped over
    the page.
  - The results stay until the box is cleared (Escape clears it), and `.showing` hides the
    letter view meanwhile.
- **Letters.**
  - Each letter is a link to `topics.html#letter-x`. With scripts on, `assets/az.js` lists that
    letter's topics in the column instead, each with the pages that teach it.
  - The list comes from `assets/topics-index.json`, written by `build_topic_index.py` from the
    grouping `topics.html` uses, and fetched the first time a letter is picked.
  - If the fetch fails, the letter follows its link.
- **The figure in the column's heading** ("2,021 topics") is checked by `check_home_stats.py`
  like the rest. `tools/check_home.js` proves all of the above; each of its assertions was
  broken once and failed.

---

## 13. A solved question paper, from the Commission's own PDF

`exams/appsc/solved-2025-paper-ii.html` is the APPSC Assistant Statistical Officer Paper-II of
29 April 2025, all 150 questions solved. It is built the way the maps are: the paper is never
retyped.

- **Extraction.** `pdftext_appsc_paper.py` reads `docs/sources/appsc-aso-2025-paper-ii.pdf`, the
  Commission's "Question Paper Preview", and keeps the English block of each bilingual question.
  It writes `appsc_paper_2025.json` with the stem (paragraphs, tables, images), the four options
  and the key.
- **The key is read twice.** The key comes from the tick icon beside each option. The option
  text colour (green for correct, red for wrong) must agree, or the extraction stops. Q134
  carries the Commission's blue note withdrawing it, and it alone may have no key.
- **Pictures.** 26 formulas and cells are printed as images. They were read off 4× renders and
  are declared by page and position in `IMAGES`. On the page they are marked
  `span.pdfimg[data-img]`.
- **What is written by hand** (`appsc_paper_data.py`):
  - the working for each question;
  - its topic, which gives the syllabus item and a "Study this" link, checked by an evidence
    pattern against the linked page's text;
  - a flag where the paper is loose (a misprint, or a key resting on one reading).

  The answer shown is always the paper's. Topics the site does not teach have no link, and are
  listed at the end of the page.
- **`recheck_appsc_paper.py`**, written after the page, re-reads the PDF with its own code. It
  checks:
  - every question's words (as a multiset) against the page;
  - the page's marked option and answer against the tick position;
  - the withdrawn question;
  - the image set, question by question;
  - the header figures the page quotes;
  - every link.

  It is mutation-tested. It also caught a real extractor bug: a "." printed level with an image
  had been dropped.
