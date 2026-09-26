# NRSTATLAB Learn: build prompt

Copy everything below the line into the coding assistant that will build the web application.
Give it `Webapp/BUILD-GUIDE.md` as well. The guide is the step-by-step plan this prompt refers to.

---

## Role

You are a senior Django engineer and learning-platform architect. You are building **NRSTATLAB
Learn**, a Django web application, from the static site in the repository
`nrstatlab/planning-for-future`.

Plan before you build. Build in the phases below, and stop for my approval at the end of each
phase. Never skip a test, or weaken a check, to get to green. Follow `Webapp/BUILD-GUIDE.md` step by
step. Where this prompt and the guide disagree, ask me.

## 1. What exists today

- **The site.** A static GitHub Pages site (NRSTATLAB) of 692 HTML pages and 946 redirect stubs,
  built by `tools/build_all.sh`.
  - The statistics and exam pages are hand-written HTML.
  - The Data Science pages are generated from Markdown in `data-science/notes/` by
    `tools/data-science/build_site.py`.
- **Page layout.** On every page the content sits between `<!-- /site-nav -->` and
  `<footer class="sitefoot">`.
  - The shared navigation sits between `<!-- site-nav -->` and `<!-- /site-nav -->`.
  - The navigation comes from `tools/site_nav_model.py` and is written into pages by
    `tools/add_site_nav.py`.
  - Redirect stubs are recognised by `tools/stubs.py` (`is_stub`).
- **Catalogue and markable pages.**
  - The catalogue is `tools/course_catalogue.py`: course order, groups and levels.
  - `assets/progress-index.json` lists the markable pages: 56 courses, 310 pages. It is built by
    `tools/build_progress_index.py`.
  - A page id is its path from the site root, for example
    `statistics/sampling-theory/unit2.html`.
- **Progress today.** It lives only in the browser. `assets/progress.js` stores the localStorage
  key `nrstatlab.progress.v1` as `{v: 1, done: {<page id>: …}, last: …}`.
- **Exams.**
  - `exams/ugc-net/`: 10 units, and 500 MCQs in `mcqs.html`. Each MCQ is a `div.mcq` holding
    `div.q`, `ol.options` and a `<details>` whose answer starts with the key letter. There is also
    a solved 2026 paper of 150 questions, with the key as "Answer: (D)", and a syllabus map.
  - `exams/iss/`: four papers.
  - `exams/csir-net/` and `exams/asrb-net/`.
  - `exams/appsc/`: two solved Paper-II, 2025 and 2022, each of 150 questions with the
    Commission's key.
  - The APPSC data is in `tools/exams/appsc_paper_2025.json` and `appsc_paper_2022.json`. Each
    question has `n`, `stem`, `options`, `marks` and `key`. The header holds the paper's official
    duration, total marks and negative marks.
  - The syllabus maps are in `tools/exams/*_map_data.py`, with recheck scripts alongside.
- **Quality gates** that must stay green:
  - `tools/check_*.py` (canonical, catalogue, home stats, raw TeX, markup, published, titles);
  - the browser checks `tools/check_*.js`;
  - the exam rechecks.
- **Read `docs/AUDIT-2026-09.md` first.** Section 5 lists the owner's open decisions. Six contested
  UGC NET keys must not count toward any score until the owner rules on them.

## 2. Goal

Every visitor can still read everything without an account. A signed-in learner can also:

1. keep their progress across devices;
2. take a unit test after finishing each unit;
3. attempt old papers in practice or exam mode, and review the worked solutions;
4. see how ready they are for a chosen exam, measured through the existing syllabus maps.

## 3. Architecture (decided)

- **Where the code lives.** Put the code in a new repository, `nrstatlab-learn`, recommended. This
  content repository is added as a git submodule at `content/`.
  - The reason: GitHub Pages serves every file in this repository, and server code does not belong
    on a public website.
  - If I choose instead to keep the code in this repository, put it in `Webapp/app/`. Then switch
    Pages to an Actions workflow that publishes only the site files (BUILD-GUIDE, Step 1).
- **Project and apps.** One Django project, `config`, with apps in `apps/`:
  - `core`: layout, navigation, redirects, search, health;
  - `accounts`: users, profile, consent, export and delete;
  - `study` (Study Material): programmes, courses, units, practicals;
  - `examinations` (Examinations): exams, papers, syllabus items, links to units, readiness;
  - `papers` (Old Papers Solved): solved papers, official keys, withdrawn questions, attempts;
  - `assessments`: the question bank, unit tests, attempts, scoring, item analysis;
  - `progress`: unit status, dashboard, import from the browser.
- **App boundaries.**
  - Each app writes only its own models. Other apps call functions in its `services.py`.
  - URLs are namespaced and templates live with each app. No circular imports.
- **Domain.** A Django application cannot run on `nrstatlab.github.io`. The application gets its
  own domain and serves every page at its current path. Once it is live, the GitHub Pages URLs
  become redirects to the new domain (BUILD-GUIDE, Step 20).

## 4. Data model (a starting point; propose refinements in Phase 0)

- **accounts**
  - `User`: a custom model from the first migration; email is the login, with no username.
  - `Profile`: `display_name`; optional `target_exam` and `exam_date`; `terms_accepted_at`;
    `age_confirmed` / `guardian_consent`.
- **study**
  - `Programme`.
  - `Course`: `slug`, `title`, `programme`, `level`, `group`, `order`.
  - `Unit`: `course`, `number`, `slug`, `title`, `legacy_path` (unique, today's URL), `head_html`,
    `body_html`, `has_math`, `content_hash`, `markable`, `published`.
  - `Page`: every other public page (hubs, guides, labs), holding `legacy_path` and the same HTML
    fields.
  - `Redirect`: `old_path`, `new_path`.
- **examinations**
  - `Exam`: `slug`, `name`, `conducting_body`, `official_source_url`, `source_note`.
  - `ExamPaper`.
  - `SyllabusItem`: `exam`, `paper`, `code`, `text`, `order`.
  - `SyllabusLink`: `item`, `unit`, `depth`, where depth is `deep` or `brief`.
- **papers**
  - `SolvedPaper`: `exam`, `title`, `held_on`, `source`, and the official fields
    `duration_minutes`, `marks_per_question`, `negative_marks`. Fill the official fields only from
    the paper's own header, and record where each came from.
  - `PaperQuestion`: `paper`, `number`, `question` (FK to `assessments.Question`),
    `official_key`, `withdrawn`, `withdrawn_note`.
- **assessments**
  - `Question`:
    - `stem_html`, `qtype` (single, multiple, numeric, assertion-reason, match),
      `solution_html`, `difficulty`, `tags`, `source`;
    - `answer` and `tolerance`, which are server-only;
    - `status` (draft, reviewed, published, flagged, retired), `flag_reason`;
    - `author`, `reviewer`, `reviewed_at`, `recompute_log`.
  - `Choice`: `question`, `label`, `text_html`, `is_correct`, which is server-only.
  - `QuestionUnit`: a many-to-many link from questions to units.
  - `UnitTest`: `unit`, `n_questions`, `pass_mark`, optional `time_limit`.
  - `Attempt`: `user`, `unit_test` or `paper`, `mode`, `started_at`, `submitted_at`, `score`,
    `max_score`, `seed`.
  - `Response`: `attempt`, `question`, `answer`, `correct`, `seconds`.
  - `ItemStats`: `question`, `n`, `difficulty`, `point_biserial`, `updated_at`.
- **progress**
  - `UnitProgress`: `user`, `unit`, `status`, `first_seen`, `studied_at`, `passed_at`,
    `best_score`, `source`. Status is `not_started`, `studying`, `studied` or `passed`; source is
    `web` or `browser_import`.
  - `ActivityEvent`.

## 5. Behaviour and acceptance criteria

- **Study.**
  - A guest opens any page at its current path and gets a 200 with the same content as today.
  - A signed-in learner sees a "Mark as studied" button on markable units.
  - Course pages show counts such as "3 of 5 studied, 2 passed".
- **When a unit test opens.** Both conditions must hold:
  - the unit is marked studied;
  - the unit has at least 10 published questions (configurable).

  Otherwise the page says "This unit has no test yet", with no date promised.
- **Unit test.**
  - It draws N questions (default 10), balanced across difficulty, and shuffles the question and
    option order from a stored seed.
  - Scoring happens only on the server. The results page shows the score, each worked solution,
    and a link to the section that teaches the question.
  - The pass mark defaults to 70% (7 of 10). It can be set per test and is not tied to any exam's rules.
  - A pass sets the unit to `passed`.
  - Retakes are allowed and use unseen questions first. Every attempt is kept, and the best score
    is shown.
- **Old papers.**
  - Practice mode shows one question at a time, with the solution on request.
  - Exam mode is the whole paper:
    - it has a timer only if the official duration is recorded;
    - it applies negative marking only if the official scheme is recorded;
    - each rule shows its source on screen.
  - Withdrawn questions are shown, never scored, and explained: APPSC 2025 Q134, and APPSC 2022
    Q51 and Q81.
  - A full review page follows submission.
- **Readiness.**
  - The learner picks a target exam and, optionally, a date.
  - The dashboard lists each syllabus item with its linked units and their status.
  - Readiness is the share of linked units passed, with deep links counted twice and brief links
    once.
  - It shows the next three units to study.
- **Browser progress import.**
  - On first sign-in, if `nrstatlab.progress.v1` exists, offer "Bring over the progress saved in
    this browser".
  - Imported page ids become `studied`, never `passed`. Ids that do not match a markable unit are
    ignored and reported.
  - Server data is never overwritten. Guests keep today's browser-only behaviour.
- **Dashboard.** Courses in progress, units studied and passed, recent scores, weak topics (from
  question tags) and a study streak.

## 6. Content import (one source of truth)

- **`import_site`** is a management command that reads:
  - the built static tree in `content/`;
  - `course_catalogue.py`;
  - `progress-index.json`;
  - the `tools/exams/` data.

  It creates or updates programmes, courses, units, pages, redirects, exams, syllabus items,
  solved papers and questions.
  - It is idempotent (it compares content hashes) and has `--dry-run`.
  - It copies every non-HTML file (CSS, JS, images, PDFs) into a site-root folder that WhiteNoise
    serves at the original paths.
- **The command fails loudly** unless the counts match:
  - 56 courses and 310 markable pages;
  - 675 indexed pages and 946 redirects;
  - 5 exams;
  - 500 UGC NET MCQs;
  - 2 × 150 APPSC questions;
  - the UGC NET solved 2026 paper's 150 questions.
- **Authoring stays in the static generators.** They remain the authoring tool at first. Django
  renders the stored body inside its own base template, with the same CSS, MathJax and dark theme.
  Moving authoring into the admin comes later, as a proposal.
- **Every existing URL keeps working.** Redirect stubs become 301s. Keep the canonical tags,
  `sitemap.xml` and `robots.txt`, rewritten for the new domain.

## 7. Question bank rules (accuracy is the product)

- **Seed only from keyed sources:**
  - the UGC NET 500 MCQs;
  - the APPSC papers (the Commission's keys);
  - the UGC NET solved 2026 paper;
  - the practice questions already on unit pages.

  Map each question to units through the syllabus maps and "Study this" links. Anything that
  cannot be mapped stays in the exam bank and does not go into unit tests.
- **The six contested keys** in `docs/AUDIT-2026-09.md` §5.1 are set to `flagged`: shown in
  practice, never scored.
- **New questions** go through draft, then reviewed, then published.
  - The reviewer is never the author.
  - Every numeric answer is recomputed by a script, with the output stored in `recompute_log`.
  - AI-assisted drafting may create drafts only, never published questions.
- **Item analysis** runs nightly once a question has 30 or more responses. It computes difficulty
  (the share correct) and the point-biserial correlation against the rest-score (the score without
  this item).
  - A question returns to review if its point-biserial is below 0, or if more than 95% or fewer
    than 10% of learners answer it correctly.

## 8. Accounts, privacy and security

- **Sign-in.** Use django-allauth with email and password, and mandatory email verification.
  Google sign-in is optional. Do not ask for a phone number.
- **Data collected.** Only email, display name, and optionally the target exam and date.
  - Provide a plain privacy page, a self-service JSON export, and account deletion.
  - Deletion is a hard delete. The learner's attempts are anonymised and kept only for item
    statistics.
- **India's DPDP Act, 2023 and its Rules.** At launch, sign-up is for learners aged 18 or over,
  who confirm their age; guests of any age read everything. A guardian-consent flow for younger
  learners needs legal review first. The privacy terms get legal review before launch either way.
- **Security settings:**
  - HTTPS only (HSTS); secure and HttpOnly cookies; CSRF;
  - a strict Content-Security-Policy, with MathJax self-hosted;
  - Argon2 password hashing; django-axes rate limiting; django-otp for the admin;
  - secrets only in environment variables;
  - answers never sent to the browser before submission.
- **No ads and no third-party trackers.** Use self-hosted, privacy-respecting analytics or server
  logs only.
- **The owner's email** must never appear in code, pages or emails. The public contact stays
  GitHub Issues.

## 9. Technology

- Python 3.12 or later, Django at the current LTS release, PostgreSQL 16.
- HTMX with small vanilla JavaScript, and no single-page-app framework.
- Reuse `assets/site-base.css`, `site-dark.css`, `site-nav.css` and the per-course stylesheets.
- MathJax 3, self-hosted.
- WhiteNoise and Gunicorn.
- django-q2 or cron-run management commands for jobs.
- Docker Compose for development.
- For quality: pytest-django, factory_boy, Playwright, ruff and GitHub Actions.
- **Hosting.** Propose two options, a managed platform and a small VPS. Give each with its current
  monthly cost, backups and a restore test.

## 10. Front end and accessibility

- Keep the current look.
- Build mobile first at 390 px, with no horizontal page scroll.
- Meet WCAG AA contrast in both themes; reuse `tools/check_contrast.js`.
- Make tests fully keyboard-operable, with MathJax in stems, options and solutions.
- Keep pages usable on slow connections.

## 11. Testing and quality gates

- **Unit tests** cover scoring for every question type, unlock rules, readiness, retake selection,
  import idempotence and privacy export/delete. Keep coverage at 90% or more on `assessments` and
  `progress`.
- **Playwright end-to-end** at 390 px and 1280 px:
  - a guest reads a unit;
  - sign-up with verification;
  - mark studied;
  - fail a test, retake it, pass it;
  - see the same progress in a second browser;
  - import from localStorage;
  - exam mode on an old paper;
  - export, then delete the account.
- **Existing checks.** Keep the crawl, contrast, markup and title checks running against the
  rendered Django pages.
- **Performance.** p95 server time under 300 ms on public pages. Largest Contentful Paint under
  2.5 s on a mid-range phone.

## 12. Phases (stop for approval after each)

| Phase | Name | Done when |
|---|---|---|
| 0 | Plan | Architecture note, entity diagram, URL map, cut-over plan and risks exist. No code yet |
| 1 | Foundations | Repo, project, apps, custom user, `import_site`, public pages and 301s, CI. All 675 indexed paths return 200 with the same text as today; every stub returns 301 |
| 2 | Accounts and progress | Sign-up, login, mark studied, dashboard, browser import, privacy page, export, delete |
| 3 | Unit tests | Seeded bank, engine, unlocking, results with solutions, retakes |
| 4 | Old papers | Practice mode, exam mode, review, withdrawn questions |
| 5 | Readiness | Target exam, readiness per syllabus item, next units |
| 6 | Quality loop | Item analysis, reviewer workflow in the admin, authoring tools |
| 7 | Launch | Staging, load test, security review, backups, runbook, domain cut-over and a tested rollback |

At the end of each phase, report:
- what changed;
- the test results;
- screenshots at 390 px and 1280 px;
- any open questions.

## 13. House rules (always)

- No university name anywhere.
- The byline is NRSTATLAB, and the contact is GitHub Issues only.
- No marks, pattern, cut-off, negative-marking or eligibility claim without a named official source
  stored with it.
- Do not change what a page teaches, except to correct an error. Content changes go through the
  owner.
- Study material stays free without login. Keep the CC BY-NC-SA 4.0 licence and the notices on
  third-party PDFs.
- No "coming soon" or dated promises anywhere in the interface.

## 14. Decisions

These were answered on 26 September 2026 and are recorded in `Webapp/ARCHITECTURE.md` §1.
They were asked as:

1. Where the code lives: a new `nrstatlab-learn` repository, or `Webapp/app/` here.
2. The domain name.
3. The hosting budget and provider.
4. The email-sending provider.
5. Whether to offer Google sign-in.
6. The default pass mark and test length.
7. Whether learners under 18 are allowed.
8. Who reviews questions.
