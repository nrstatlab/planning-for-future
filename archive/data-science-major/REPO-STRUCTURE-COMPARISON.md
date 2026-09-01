# Repository structure comparison — nrstatlab

A structural review of the four `nrstatlab` study repositories, judged on one
question: **how much work is it to change one topic?**

Measured 2026-08-31 against the default branch of each repository.

| Repository | Files | Size | Shape | Tooling |
|---|---:|---:|---|---|
| [Machine-Learning](https://github.com/nrstatlab/Machine-Learning) | 25 | 456 KB | 3-level HTML: hub → unit → topic | validator + 4-job CI |
| [Data-Science-Major-2025](https://github.com/nrstatlab/Data-Science-Major-2025) | 108 | 1.5 MB | Markdown: `notes/sem/course/unit` + `labs/` | 7 scripts, no CI |
| [ugcnetstatistics](https://github.com/nrstatlab/ugcnetstatistics) | 15 | 628 KB | Flat HTML, one file per unit | none |
| [Statistics-Major](https://github.com/nrstatlab/Statistics-Major) | 192 | 3.4 MB | 21 course folders × 9 files | none |

---

## Verdict

**Machine-Learning has the best structure to update and modify a topic.**
It is not the simplest repository — `ugcnetstatistics` is — but it is the only
one where *simple* and *safe* are the same thing.

Ranking, best first:

1. **Machine-Learning** — right granularity, no duplication, checks that fail loudly
2. **Data-Science-Major-2025** — clean tree, but one fact lives in eleven files
3. **ugcnetstatistics** — simplest to open, hardest to grow
4. **Statistics-Major** — most content, weakest structure

---

## 1. Machine-Learning — the model to copy

```
index.html               hub
├── unitN.html           unit page (topic tiles)
│   └── unitN-topic.html topic page (the algorithms)
├── syllabus.html        scope + what is not covered
├── css/styles.css       one stylesheet, shared
├── js/notes.js          one script, shared
└── scripts/check_notes.py + .github/workflows/validate.yml
```

**Why it wins**

- **Predictable path.** A topic's file name is derivable from its position:
  Unit 2 clustering is `unit2-clustering.html`. No guessing, no search.
- **Right edit size.** Topic pages average 20 KB — big enough that related
  algorithms sit together, small enough to hold in your head. Editing K-Means
  means opening exactly one file.
- **Zero duplication.** One `css/styles.css`, one `js/notes.js`. A design
  change is a one-file change.
- **Documented contract.** `CLAUDE.md` fixes the shape of every algorithm —
  six parts, in order (Definition, Mathematical Foundation, How It Works,
  Assumptions and Failure Modes, three Worked Examples, Python + R code). New
  content has a template instead of a precedent to guess at.
- **The checks are real.** `scripts/check_notes.py` catches unescaped `<`/`&`
  in code panes, unbalanced MathJax delimiters, stray `$`, broken inter-page
  links, tabs pointing at missing panes, and Python that no longer parses. CI
  adds HTML5 validation, external link checking, and *actually executes every
  Python pane*. This is the only repository where a bad edit is caught before
  a reader finds it.

**Cost to change a topic:** 1 file.
**Cost to add a topic:** 3 files (topic page, parent unit page tile,
`syllabus.html`) + the `EXPECTED_ALGORITHMS` constant.

**The one friction point:** `check_notes.py` hardcodes `EXPECTED_ALGORITHMS = 23`
and derives expected example and code-pane counts from it. Adding an algorithm
fails CI until that number is bumped. That is a deliberate inventory guard, not
a bug — but it should be documented in `CLAUDE.md` as step one of "adding a
topic", because the failure message does not say so.

---

## 2. Data-Science-Major-2025 — clean tree, scattered facts

```
notes/sem-N/course-N-name/{README,unit-1..5,practice,lab}.md
labs/course-N-lang/…            runnable code
tools/…                          coverage checker + lab runners
README · SYLLABUS-MAP · SYLLABUS-REVIEW · STUDY-PLAN
```

**Strengths**

- The `sem → course → unit` hierarchy mirrors how the degree is actually
  organised, so the path to a topic is obvious from the syllabus alone.
- Every course folder holds the same seven files. Uniform and predictable.
- Markdown is the cheapest format to edit — no delimiters to balance, no
  markup to break, readable diffs.
- Notes average ~330 lines, which is a comfortable single-topic edit.
- `tools/verify_all.sh` runs every lab in every language (C, Python, SQL,
  stats) in one command — genuinely good, and no other repository has it.

**The real weakness: one topic lives in many files.**

Bayes' theorem appears in **eleven** tracked files — the unit note, the course
README, `lab.md`, `formula-sheet.md`, `SYLLABUS-MAP.md`, `STUDY-PLAN.md`, the
root `README.md`, `SYLLABUS-REVIEW.md`, a lab program, `excel-walkthroughs.md`,
and the extracted syllabus. Correcting or expanding it means finding and updating all of them, and
nothing enforces that. The two "examined but off-syllabus" warnings are
themselves repeated in three places each.

Second weakness: `tools/check_coverage.py` verifies coverage with a **hand-written
keyword list per unit file**. It catches a deleted topic, but the map itself has
to be maintained by hand and drifts silently. And there is **no CI** — the checker
only runs if someone remembers to run it.

**Cost to change a topic:** 1 file to edit, up to 10 more to check by hand.

---

## 3. ugcnetstatistics — simplest, but simple only while it is small

15 files in one flat directory: `index.html`, ten unit pages, `mcqs.html`,
`pyq2026.html`, one `styles.css`, a README.

**Strengths:** nothing to navigate. One stylesheet, shared by every page. The
whole repository fits on one screen. For ten units of exam prep this is the
correct amount of structure — adding structure here would be overhead, not order.

**Where it breaks down**

- **No sub-unit granularity.** Unit pages run 391–928 lines, and `mcqs.html`
  is 2,150 lines / 148 KB. Changing one MCQ means editing a file 15× larger
  than the change. Merge conflicts get likely as soon as two edits land near
  each other.
- **Style drift has already started.** `mcqs.html` and `pyq2026.html` each
  carry an inline `<style>` block *on top of* the shared stylesheet. Those
  overrides are invisible from `styles.css`, so a change there silently fails
  to reach two pages.
- **No validator, no CI, no `CLAUDE.md`.** Nothing defines what a unit page
  should contain, and nothing checks that it does.
- Adding an eleventh unit means editing the hardcoded nav in all 13 existing pages by
  hand — every page carries the full 10-unit list.

---

## 4. Statistics-Major — most content, weakest structure

21 courses × (index, syllabus, practical, 5 units, css) = 192 files.

**Strengths:** the per-course folder pattern is consistent — every course has the
same nine files, so within a course you always know where a topic is.
`CLAUDE.md` is the most detailed authoring guide of the four, and the pedagogy
rules in it (no skipped steps, verify every number in Python first) are worth
keeping as the house standard.

**Four structural problems, in order of cost**

1. **The stylesheet is copied 21 times.** All 21 `css/styles.css` files are
   byte-identical (md5 `7c367323…`). Every design change is 21 edits, or it
   silently becomes 21 different sites. This is the single biggest maintenance
   liability in any of the four repositories.
2. **156 filenames contain spaces** — and worse, the course name is repeated
   inside the file name: `theoretical continuous distributions/unit3_theoretical
   continuous distributions.html`. Every shell command, script, and URL needs
   quoting or escaping. Renaming a course means renaming nine files.
3. **Two naming conventions coexist.** 18 courses use the
   `unit1_<course name>.html` form; 3 (clinical trials, quality control,
   research methodology) use plain `unit1.html`. Any script that walks the tree
   has to handle both.
4. **Hardcoded prev/next chains.** Each unit page links directly to its
   neighbours (`unit2` → `unit1`, `unit3`). Inserting or reordering a unit means
   editing the two adjacent pages too.

Plus: **no validator and no CI**, on the largest body of MathJax-heavy HTML of
the four — where a broken `\(` delimiter is both easiest to introduce and
hardest to spot.

**Cost to change a topic:** 1 file, if the change is confined to prose.
**Cost to change anything shared:** 21 files.

---

## Scorecard

| | ML | DS-Major | ugcnet | Stats-Major |
|---|:--:|:--:|:--:|:--:|
| Path to a topic is predictable | ✅ | ✅ | ✅ | ⚠️ two conventions |
| Edit granularity | ✅ ~20 KB | ✅ ~330 lines | ❌ up to 2,150 lines | ✅ |
| No duplicated assets | ✅ | ✅ | ⚠️ inline overrides | ❌ 21× css |
| One fact in one place | ✅ | ❌ up to 11 files | ✅ | ✅ |
| Documented content contract | ✅ CLAUDE.md | ⚠️ implied | ❌ | ✅ CLAUDE.md |
| Automated checks | ✅ CI | ⚠️ scripts, no CI | ❌ | ❌ |
| Tooling-friendly filenames | ✅ | ✅ | ✅ | ❌ 156 with spaces |
| Adding a topic is local | ✅ 3 files | ⚠️ +map files | ❌ nav in 13 pages | ⚠️ +neighbours |

---

## Recommendations

**Make Machine-Learning's shape the house standard**: hub → unit → topic, one
shared `css/` and `js/`, a `CLAUDE.md` contract, `scripts/check_*.py`, and a CI
workflow. It is the only one of the four that stays cheap to edit as it grows.

Highest-value fix per repository:

- **Statistics-Major** — replace the 21 copies of `styles.css` with a single
  root `/css/styles.css`, then normalise filenames to lowercase-hyphenated
  without the course-name suffix. Both are mechanical, and together they remove
  most of the repository's maintenance cost.
- **Data-Science-Major-2025** — make the unit note the single source of truth
  for each topic and have `README`, `SYLLABUS-MAP` and `STUDY-PLAN` link to it
  instead of restating it. Then add a CI workflow running the existing
  `tools/verify_all.sh` and `check_coverage.py` — the scripts are already
  written; only the trigger is missing.
- **ugcnetstatistics** — fold the two inline `<style>` blocks into
  `styles.css`, and split `mcqs.html` per unit. Leave the flat layout alone;
  at this size it is right.
- **Machine-Learning** — document the `EXPECTED_ALGORITHMS` bump in `CLAUDE.md`
  as the first step of adding a topic.
