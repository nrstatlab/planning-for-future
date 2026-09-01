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
| [`data-science-major/`](data-science-major/) | APSCHE B.Sc. (Hons) Data Science major, AY 2025-26 — notes, practice and runnable labs | 5 courses, 41 note pages, 53 lab programs |
| [`ugc-net-statistics/`](ugc-net-statistics/) | UGC NET Statistics, subject code 107 | 10 units, model MCQs, solved 2026 paper |
| [`machine-learning/`](machine-learning/) | Self-study notes on 23 algorithms, with Python and R | 4 units, 16 pages |

Each section keeps its own contents page, its own stylesheet and its own
authoring guide (`CLAUDE.md`, where one exists). The only shared pieces are the
home page, `assets/nrstatlab.css`, and the `NRSTATLAB ›` bar at the top of each
section's contents page.

## Where each section came from

| Section folder | Original repository |
|---|---|
| `statistics-major/` | `nrstatlab/Statistics-Major` |
| `data-science-major/` | `nrstatlab/Data-Science-Major-2025` |
| `ugc-net-statistics/` | `nrstatlab/ugcnetstatistics` |
| `machine-learning/` | `nrstatlab/Machine-Learning` |

Those four repositories are untouched and still publish at their own URLs.

## How the site is built

GitHub Pages, with Jekyll doing one narrow job.

- The Statistics, UGC NET and Machine Learning sections are hand-authored HTML
  with no front matter, so Jekyll copies them through **byte for byte** and never
  runs Liquid over them. Nothing about how those pages work has changed.
- The Data Science section is Markdown. Each note carries three lines of front
  matter (`layout`, `title`, `section`) so Jekyll renders it as a real page using
  [`_layouts/note.html`](_layouts/note.html). The prose was not edited.
- Lab source (`.c`, `.py`, `.sql`) is copied through as plain files, so any lab
  program can be read or downloaded straight from the site.

Every internal link is **relative**. That is what lets the whole site move to a
custom domain without a single edit.

### Building it locally

```sh
gem install jekyll
jekyll build            # output in _site/
jekyll serve            # http://localhost:4000
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
assets/nrstatlab.css    hub styles, the section bar, and the Markdown note styling
_config.yml             Jekyll configuration
_layouts/note.html      renders a Data Science Markdown note
_layouts/dir.html       lists a lab folder, built from the files actually present
.github/workflows/      CI, scoped to the Machine Learning section

statistics-major/       ─┐
data-science-major/      │ the four sections, each self-contained
ugc-net-statistics/      │
machine-learning/       ─┘
```
