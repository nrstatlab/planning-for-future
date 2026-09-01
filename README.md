# NRSTATLAB

Statistics, Data Science and Machine Learning study material — written to teach,
with every step shown.

This repository holds the whole of NRSTATLAB as one site. It was assembled from
four separate repositories so that everything can sit under a single domain.
The material itself was not rewritten in the move: the pages are the same pages.

**Live site:** open [`index.html`](index.html), or browse the sections below.

## Sections

| Section | What it is | Size |
|---|---|---|
| [`statistics-major/`](statistics-major/) | The full three-year B.Sc. Statistics major, one folder per subject | 21 subjects, 105 unit pages |
| [`data-science-major/`](data-science-major/) | B.Sc. (Hons) Data Science major — the whole programme, Semesters I–VI | 19 courses, 332 lab programs, 266 practice questions |
| [`ugc-net-statistics/`](ugc-net-statistics/) | UGC NET Statistics, subject code 107 | 10 units, model MCQs, solved 2026 paper |

Machine Learning is not a separate section. It is
[Course 12A](data-science-major/machine-learning/) of the Data Science major —
the Track A elective the syllabus places in Semester V. That course carries
**two** treatments of the subject, deliberately:

- its **five syllabus units**, following the model unit list, like every other course
- a deeper set of [self-study notes](data-science-major/machine-learning/self-study-notes/)
  organised by the kind of supervision signal an algorithm learns from, covering
  23 algorithms with their mathematics, failure modes and runnable Python and R

Each section keeps its own contents page, its own stylesheet and its own
authoring guide (`CLAUDE.md`, where one exists). The only shared pieces are the
home page, `assets/nrstatlab.css`, and the `NRSTATLAB ›` bar at the top of each
section's contents page.

## Where each section came from

| Section folder | Original repository |
|---|---|
| `statistics-major/` | `nrstatlab/Statistics-Major` |
| `data-science-major/` | `nrstatlab/Data-Science-Major-2025` (its `main` branch) |
| `ugc-net-statistics/` | `nrstatlab/ugcnetstatistics` |
| `data-science-major/machine-learning/self-study-notes/` | `nrstatlab/Machine-Learning` |

Those four repositories are untouched and still publish at their own URLs.

**Every path on every branch of all four is present here** — 1199 paths across
their nine branches, checked by content hash, with none missing. The only
deliberate exclusion is `tools/node_modules`, which is vendored dependencies
rather than material and is reinstallable from the `package.json` that is here.

Three files existed only on side branches and never on any `main`; they are kept
in [`archive/`](archive/) with a note on where each came from, so the sources can
be retired without losing anything. What a file copy cannot carry is the commit
history, the four `nrstatlab.github.io/<repo>/` URLs, and any issues or releases —
so **archiving those repositories is safer than deleting them**, and costs nothing.

> Note for later: `Data-Science-Major-2025`'s **default branch is not `main`** —
> it is `claude/data-science-syllabus-review-eoirk3`, an older snapshot. The
> content here came from `main`, which is the fuller and more recent tree. If you
> keep working in that repository, set `main` as its default first.

## How the site is built

It isn't. There is no build step and no generator.

Every page is plain HTML, served exactly as committed. A `.nojekyll` file at the
root tells GitHub Pages to skip Jekyll entirely, so nothing is parsed, rewritten
or templated on the way out — what is in the repository is what a reader gets.

Two things follow from that, and both are deliberate:

- **The Markdown in `data-science-major/notes/` is source, not pages.** The HTML
  course folders are generated from it by
  [`data-science-major/tools/build_site.py`](data-science-major/tools/build_site.py).
  Edit the Markdown, re-run that script, commit both.
- **Every internal link is relative.** That is what lets the whole site move to a
  custom domain without a single edit.

To preview locally, any static server will do:

```sh
python3 -m http.server 8000
```

## Checking it

The Data Science section brings its own verification, all runnable from
`data-science-major/`:

```sh
python3 tools/check_coverage.py    # every syllabus topic maps to a notes section
bash    tools/verify_all.sh        # compiles and runs the lab programs
```

The self-study notes have their own structural validator, which CI also runs:

```sh
cd data-science-major/machine-learning/self-study-notes && python3 scripts/check_notes.py
```

## Putting it on your own domain

1. **Settings → Pages → Build and deployment**: source *Deploy from a branch*,
   branch `main`, folder `/ (root)`.
2. Buy the domain, then **Settings → Pages → Custom domain**: enter it and tick
   *Enforce HTTPS*. GitHub will ask you to add a `CNAME` file — that is one line
   at the repository root containing the bare domain.
3. At your DNS provider, point the apex record at GitHub Pages' four `A`
   records, and a `www` `CNAME` at `nrstatlab.github.io`.

No page needs editing for any of this. Until a domain is set, the site is served
at `https://nrstatlab.github.io/<repository-name>/`.

## Repository layout

```
index.html              NRSTATLAB home page
404.html                not-found page (styles inlined; it is served from any depth)
assets/nrstatlab.css    hub styles and the section bar
.nojekyll               serve the repository as-is, no Jekyll
.github/workflows/      CI, scoped to the Machine Learning self-study notes

statistics-major/       21 subjects, each its own folder
ugc-net-statistics/     10 units, MCQs, solved paper
data-science-major/     19 course folders (the site) + notes/ (the source)
                        + labs/, data/, docs/, tools/
```
