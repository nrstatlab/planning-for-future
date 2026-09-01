# Merge plan — four repositories into one

How to bring `Statistics-Major`, `Data-Science-Major-2025`, `ugcnetstatistics`
and `Machine-Learning` under one roof **without losing a single topic and
without duplicating anything that should exist once.**

Companion to [`REPO-STRUCTURE-COMPARISON.md`](REPO-STRUCTURE-COMPARISON.md).
All figures measured from the working trees on 2026-08-31.

---

## The finding that shapes the whole plan

I checked 26 core topics across all four repositories:

| | Stats-Major | ugcnet | ML | DS-Major |
|---|:--:|:--:|:--:|:--:|
| Bayes' theorem | 5 files | 5 | 6 | 11 |
| Linear regression | 37 | 4 | 5 | 7 |
| ANOVA | 38 | 8 | — | 7 |
| Estimation theory | 13 | 6 | 2 | 1 |
| Time series | 13 | 6 | 2 | 3 |

**25 of the 26 topics already appear in two or more repositories.** Only
Operations Research lives in exactly one place.

That number looks alarming, but almost none of it is waste. Four different
audiences are being served:

| Repository | Reader | Depth |
|---|---|---|
| Data-Science-Major-2025 | B.Sc. (Hons) Data Science student, APSCHE syllabus | first exposure, exam-mapped |
| Statistics-Major | undergraduate statistics major | full course treatment, proofs |
| ugcnetstatistics | UGC NET aspirant | compressed revision + MCQs |
| Machine-Learning | self-learner | algorithm-first, code-first |

Bayes' theorem for a NET aspirant is a one-screen refresher with a solved MCQ.
Bayes' theorem in Course 4 is a full derivation flagged as *examined but
off-syllabus*. They are not duplicates of each other — they are different
products of the same idea.

**So "merge without duplicating" cannot mean one page per topic.** Collapsing
those treatments would disturb every topic — which is the one thing you asked
not to happen. It means this instead:

> **One infrastructure. Four audiences. One topic index.**
> Deduplicate the *plumbing*, keep the *teaching*, and add an index so the four
> treatments of a topic know about each other instead of silently drifting apart.

---

## What actually gets deduplicated

Every item here is duplication with no pedagogical value. Nothing on this list
changes a word of study material.

| Duplicated today | Count | After |
|---|---:|---|
| Byte-identical `styles.css` copies in Statistics-Major | 21 | 1 core + 3 theme layers |
| Repeated MathJax config blocks across HTML pages | 169 | 1 shared include |
| Hand-maintained navigation systems | 4 | 1 generated nav |
| Authoring guides (2 exist, 2 missing) | 2 + 2 gaps | 1 root `CLAUDE.md` + per-tree deltas |
| Files restating Bayes' theorem in DS-Major | 11 | 1 canonical note + 10 links |
| Structural validators (only ML has one) | 1 + 3 gaps | 1 checker over all four trees |
| Topics deleted or rewritten | — | **0** |

---

## The mechanical news is good

Three things I verified that make this far cheaper than it looks:

1. **Zero root-absolute links.** Across all 340 files there is not one
   `href="/..."`. Every internal link is relative (`unit1.html`,
   `css/styles.css`). **A whole site can be moved into a subdirectory and every
   internal link still resolves** — no rewrite of 1,063 links needed.
2. **Only 6 cross-site absolute links** to `nrstatlab.github.io/...` exist in
   total. Six edits, not six hundred.
3. **The design systems already converge.** Machine-Learning's stylesheet
   contains *all 54* of Statistics-Major's selectors plus 58 of its own — it is
   already a superset, so the shared core stylesheet is extraction, not
   redesign. Only ugcnetstatistics is genuinely separate (20 of 68 selectors
   shared), and it stays a theme layer.

All three HTML sites also load MathJax from the same CDN, so there is no
conflict there either.

---

## The three plans

### Plan A — One monorepo, one site  ★ recommended

A new repository `nrstatlab.github.io` (a GitHub **user** site, served from the
root of the domain) holds everything:

```
nrstatlab.github.io/
├── index.html            one hub → the four programmes
├── shared/
│   ├── css/core.css      the 54-selector base, once
│   ├── css/theme-*.css   ml · net · stats  (visual identity per programme)
│   ├── js/notes.js       code tabs, copy button
│   └── includes/mathjax.html
├── stats/                ← Statistics-Major, 21 courses
├── ds/                   ← Data-Science-Major-2025, notes + labs
├── net/                  ← ugcnetstatistics, 10 units + MCQs
├── ml/                   ← Machine-Learning, 4 units
├── topics/               the topic registry (one entry per concept)
├── scripts/check.py      one validator over all four trees
├── CLAUDE.md             one authoring contract
└── .github/workflows/    one CI
```

Each tree is brought in with `git subtree add`, which **preserves that
repository's full commit history** inside the monorepo. The four old
repositories are never deleted — they stay alive as redirect stubs (198
generated `<meta refresh>` pages) so every bookmarked and indexed URL keeps
working.

- **Gains:** all seven rows of the dedup table. One place to change a colour, one
  CI, one contract, cross-links between the four treatments of a topic.
- **Costs:** ~10 working days. URLs change (mitigated by stubs). One large repo
  (~6 MB, 340 files — still small).
- **Risk:** low, because each tree moves independently and each move is
  verifiable by link parity.

### Plan B — Federation: keep four repos, share a theme

Extract one `nrstatlab-theme` repository and consume it from all four, either as
a git submodule or copied in by a CI job.

- **Gains:** the stylesheet duplication only. Live URLs never change. ~3 days.
- **Costs:** GitHub Pages does not build submodules without a workflow, so you
  add CI to four repos to solve one problem. Nav, validators, authoring guide and
  the topic index all stay quadrupled.
- **Verdict:** the right answer if the four sites must keep separate identities
  forever. The ceiling is low — it fixes one of seven rows.

### Plan C — Two repos, split by format

Merge the three HTML sites (`stats` + `net` + `ml`) into one site repository;
leave `Data-Science-Major-2025` alone as the markdown-and-runnable-code
repository.

- **Gains:** most of the CSS/nav/CI dedup, and it respects the real format
  boundary — markdown notes and executable labs genuinely are a different kind of
  artifact from a MathJax site. ~6 days.
- **Costs:** the topic index spans two repos, so cross-links between a DS-Major
  note and a Statistics-Major course have to be maintained by hand — which is
  exactly the failure mode we're trying to remove.
- **Verdict:** a reasonable stopping point if Plan A stalls. It is also Plan A's
  Phase 4, so nothing is wasted by aiming at A and stopping here.

---

## Recommended: Plan A, executed in Plan B's order

Do not do a big-bang merge. Land the shared layer first, then move one tree at a
time, **cheapest and best-tooled first**, so the risky one benefits from a
pattern already proven three times.

Order: **ML → ugcnet → DS-Major → Statistics-Major.**
Statistics-Major goes last because it needs 156 file renames, and by then the
rename-plus-redirect procedure will have been rehearsed on three smaller trees.

### Phase 0 — Safety net (Day 1)

- Create `nrstatlab.github.io`, add `.nojekyll` and a placeholder hub.
- **Snapshot every live URL** from all four sites into `redirects.tsv`
  (198 HTML pages + the DS-Major markdown routes). This file is the contract:
  at the end, every line in it must still resolve.
- Write `scripts/check_links.py` — takes `redirects.tsv`, walks the new site,
  fails on any URL that no longer answers. Nothing merges until this exists.

*Deliverable: an empty site and a test that would catch any loss.*

### Phase 1 — The shared layer (Day 2)

- Extract `shared/css/core.css` from Machine-Learning's stylesheet (it already
  contains the entire Statistics-Major base).
- Write `theme-ml.css`, `theme-stats.css`, `theme-net.css` as thin overlays —
  each programme keeps its own look.
- One `shared/includes/mathjax.html`, one `shared/js/notes.js`.
- Merge the two existing `CLAUDE.md` files into a root authoring contract:
  Statistics-Major's pedagogy rules (no skipped steps, verify every number in
  Python first) plus Machine-Learning's six-part topic template.

*Deliverable: the infrastructure, with no content on it yet.*

### Phase 2 — Move Machine-Learning (Day 3)

The rehearsal: 16 pages, already has a validator and CI.

- `git subtree add --prefix=ml https://github.com/nrstatlab/Machine-Learning main`
- Point its pages at `shared/`; delete the local `css/` and `js/`.
- Fold `check_notes.py` into `scripts/check.py` as the `ml` tree's rules, and
  **document the `EXPECTED_ALGORITHMS` bump** in `CLAUDE.md` while you are there.
- Generate 16 redirect stubs into the old repository.
- Run link parity. It must be green before Phase 3 starts.

*Deliverable: the full move procedure, proven end to end on the smallest tree.*

### Phase 3 — Move ugcnetstatistics (Days 4–5)

- `git subtree add --prefix=net …`
- Fold the two inline `<style>` blocks into `theme-net.css` — they are the
  invisible drift found in the structure review.
- Split `mcqs.html` (2,150 lines) into per-unit MCQ pages; keep the old URL as a
  hub linking to them, so no bookmark breaks.
- Replace the nav hardcoded in all 13 pages with the generated one.

*Deliverable: the first real structural improvement, on the smallest content set.*

### Phase 4 — Move Data-Science-Major-2025 (Days 6–7)

- `git subtree add --prefix=ds …` — notes and labs move unchanged.
- Collapse the eleven-file Bayes restatement: the unit note becomes canonical,
  and `README`, `SYLLABUS-MAP`, `STUDY-PLAN` and `SYLLABUS-REVIEW` link to it
  instead of repeating it. Do the same for the two off-syllabus warnings.
- Wire the existing `verify_all.sh` and `check_coverage.py` into the shared CI —
  the scripts are already written; only the trigger is missing.

*Deliverable: the markdown tree joined, and this repo's worst duplication gone.*
*If the project must stop early, stop here — this is Plan C, complete.*

### Phase 5 — Move Statistics-Major (Days 8–10)

The big one: 169 pages, 156 filenames with spaces, 21 stylesheet copies.

- `git subtree add --prefix=stats …`
- Rename with `git mv` so history follows each file:
  `theoretical continuous distributions/unit3_theoretical continuous distributions.html`
  → `theoretical-continuous-distributions/unit3.html`. This also settles the two
  competing naming conventions.
- Delete the 21 stylesheet copies; repoint every page at `shared/` (scripted,
  one pass).
- Replace hardcoded prev/next chains with the generated nav, so inserting a unit
  stops editing its neighbours.
- Generate 169 redirect stubs — the largest redirect set, done last, by a script
  used three times already.

*Deliverable: the largest maintenance liability in the estate, removed.*

### Phase 6 — The topic registry (Days 11–12)

This is what makes the merge worth more than a tidy-up.

- One entry per concept in `topics/`, e.g. `topics/bayes-theorem.yml`, listing
  every place it is taught and at what depth:

  ```yaml
  id: bayes-theorem
  name: Bayes' theorem
  taught_in:
    - ds/notes/sem-2/course-4/unit-1.md#16   # derivation, exam-mapped
    - stats/theory-of-probability/unit2.html # full treatment with proofs
    - net/unit1.html#bayes                   # revision + MCQs
    - ml/unit1-classification.html#naive-bayes  # applied
  ```

- Each page declares `data-topic="bayes-theorem"`; the build renders a
  "also covered at" strip from the registry.
- `scripts/check.py` fails when a page claims a topic ID that does not exist, or
  a registry entry points at a file that moved.

*Deliverable: the four treatments of every topic linked, one index, no prose duplicated.*

---

## How "without disturbing any topic" is enforced

Not by care — by checks that fail:

1. **URL parity.** `redirects.tsv` is written in Phase 0 and asserted in every
   phase after. If a page ever stops resolving, CI goes red.
2. **Content parity.** After each subtree move, page *bodies* must be
   byte-identical to the source repository — only paths change. A diff proves it.
3. **One tree per pull request.** Four merges, four reviewable PRs, each
   revertible on its own.
4. **The old repositories are never deleted.** They become redirect stubs. If
   anything is wrong, the original is still there, at its original URL, with its
   original history.
5. **History is preserved.** `git subtree` keeps each repository's commits, so
   `git log` and `git blame` still work on every moved file.

---

## What I need from you before Phase 0

Two decisions, and one is nearly free:

1. **Repository name.** `nrstatlab.github.io` gives the cleanest URLs
   (`nrstatlab.github.io/ml/unit1.html`) because a user site serves from the
   domain root. The alternative is merging into an existing repository, which
   keeps one site's URLs unchanged but leaves the other three deeper in the path.
   *Recommendation: the new user site.*
2. **Should the four sites keep separate looks?** The theme layer supports either
   answer, and the cost is the same. *Recommendation: yes — a NET revision sheet
   and a B.Sc. course note are read differently, and one visual identity for all
   four would flatten a distinction that is doing real work.*

---

## Effort summary

| Plan | Days | Dedup achieved | URLs change | Reversible |
|---|---:|---|---|---|
| **A — monorepo** | ~10–12 | 7 of 7 rows | Yes, with 198 stubs | Per phase |
| B — federated theme | ~3 | 1 of 7 rows | No | Yes |
| C — two repos by format | ~6 | 5 of 7 rows | Partly | Per phase |

Phases 0–2 are three days and prove the whole approach on the smallest tree. If
it does not feel right at the end of Day 3, nothing has moved except
Machine-Learning, and that move reverts with one command.
