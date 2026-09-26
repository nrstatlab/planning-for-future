# NRSTATLAB Learn: step-by-step build guide

This guide turns the static NRSTATLAB site into a Django web application. Visitors keep reading
everything free. Signed-in learners keep their progress, take a unit test after each unit, sit old
papers, and see how ready they are for their exam.

The guide is written to be followed in order: 21 steps, grouped into the 8 phases of
[`PROMPT.md`](PROMPT.md). Each step says what to do, how to do it, and how you know it is done.
Stop at the end of each phase and review before going on.

| Phase | Steps | Result |
|---|---|---|
| 0 Plan | 0 | Decisions made; accounts and tools ready |
| 1 Foundations | 1–6 | Every page of today's site served by Django, at the same address |
| 2 Accounts and progress | 7–8 | Sign-up, login, synced progress, dashboard |
| 3 Unit tests | 9–10 | A question bank and tests that open after each unit |
| 4 Old papers | 11 | Practice mode and exam mode for solved papers |
| 5 Readiness | 12 | Exam readiness from the syllabus maps |
| 6 Quality loop | 13 | Item analysis and the reviewer workflow |
| 7 Launch | 14–20 | Tested, secured, deployed, domain moved |

**A rough effort guide, for one experienced Django developer:**
- Phase 0: 3 days.
- Phase 1: 2 weeks.
- Phase 2: 2 weeks.
- Phase 3: 3 weeks.
- Phase 4: 1.5 weeks.
- Phase 5: 1 week.
- Phase 6: 1.5 weeks.
- Phase 7: 1 week.

That is about 12 weeks in total. Writing questions for the units that have none is separate
content work (Step 9.5).

---

## Phase 0: Plan

### Step 0. Make the decisions and gather what you need

**Decide these first.** They are the eight questions at the end of `PROMPT.md`.

| Decision | Recommendation | Why |
|---|---|---|
| Where the code lives | A new repository, `nrstatlab-learn`, with this one as a submodule | GitHub Pages serves every file in this repository, so server code would be published as web pages |
| Domain | Buy one, for example `nrstatlab.in`, and serve the app at its root | A Django app cannot run on `nrstatlab.github.io` |
| Hosting | A managed platform to start; a VPS once traffic is steady | Less to run while the product is proven |
| Email sending | A transactional email service with SPF and DKIM set up on the domain | Sign-up needs verification emails that arrive |
| Google sign-in | Yes, as an option beside email | It lowers sign-up friction for students |
| Pass mark and test length | 60% and 10 questions, set per test | Easy to change once item data arrives |
| Learners under 18 | Only with guardian consent, after legal review | India's DPDP Act, 2023 |
| Question reviewers | At least two subject reviewers | Nobody reviews their own questions |

**Accounts to create.**
- The new GitHub repository.
- A hosting account.
- A domain registrar account.
- An email-sending account.
- Optionally, a Google Cloud OAuth client for Google sign-in.

**Tools to install:**
- Python 3.12 or later;
- PostgreSQL 16, or Docker Desktop;
- Git;
- Node 20 or later, for Playwright;
- a code editor.

**Deliverable.** A one-page architecture note: the apps, the entity diagram, the URL map and the
cut-over plan. Get it approved before any code is written.

**Done when** every decision above is written down and approved.

---

## Phase 1: Foundations

### Step 1. Create the repository

**Recommended: a separate repository.**

```bash
git clone git@github.com:nrstatlab/nrstatlab-learn.git
cd nrstatlab-learn
git submodule add https://github.com/nrstatlab/planning-for-future.git content
git submodule update --init
```

- The submodule pins the content to one commit. Upgrading content is then a reviewed change:
  `git -C content pull`, then commit the new pointer.
- Add a `.gitignore` covering `.env`, `__pycache__/`, `.venv/`, `staticfiles/`, `var/`, `media/` and
  `node_modules/`.
- Commit an `.env.example`, never a `.env`.

**Alternative: keep the code in this repository**, if you prefer everything in one place.

1. Put the code in `Webapp/app/`.
2. Change GitHub Pages from "deploy from branch" to "GitHub Actions".
3. Add a workflow that copies only the site files into a folder and publishes that folder with
   `actions/upload-pages-artifact` and `actions/deploy-pages`. Leave out `Webapp/app/` and
   `tools/`.

Without the workflow, Pages publishes the server code.

**Done when** the repository exists, `content/` is checked out, and `.env` is ignored.

### Step 2. Create the project and the apps

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install "django>=5.2,<6" "django[argon2]" psycopg[binary] django-environ \
    django-allauth django-axes django-otp django-csp whitenoise gunicorn \
    django-q2 beautifulsoup4 lxml
pip install pytest pytest-django factory-boy playwright ruff coverage   # development only
django-admin startproject config .
mkdir apps && for a in core accounts study examinations papers assessments progress; do
  mkdir apps/$a && python manage.py startapp $a apps/$a; done
```

In each `apps/<name>/apps.py`, set `name = "apps.<name>"`. The layout:

```
nrstatlab-learn/
  config/            settings/ (base.py, dev.py, prod.py), urls.py, wsgi.py
  apps/
    core/            base template, navigation, redirects, health, search
    accounts/        User, Profile, privacy, export, delete
    study/           Programme, Course, Unit, Page; unit views
    examinations/    Exam, SyllabusItem, SyllabusLink; readiness
    papers/          SolvedPaper, PaperQuestion; exam-mode views
    assessments/     Question, Choice, UnitTest, Attempt, Response, ItemStats
    progress/        UnitProgress, ActivityEvent; dashboard; browser import
  templates/         base.html and shared partials
  static/            the app's own CSS/JS (the site's CSS comes from content/)
  content/           git submodule: the static site
  var/site_root/     generated by import_site: non-HTML site files, served at their old paths
  tests/             pytest tests; e2e/ for Playwright
```

**Split the settings.**
- `config/settings/base.py` reads everything from the environment with `django-environ`.
- `dev.py` turns on `DEBUG` and the console email backend.
- `prod.py` holds the security settings from Step 16.

**Done when** `python manage.py check` passes with every app in `INSTALLED_APPS`.

### Step 3. Create the custom user, before the first migration

A custom user model is very hard to add later. Create it before running `migrate` for the first
time.

```python
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=60)
    target_exam = models.ForeignKey("examinations.Exam", null=True, blank=True, on_delete=models.SET_NULL)
    exam_date = models.DateField(null=True, blank=True)
    terms_accepted_at = models.DateTimeField(null=True, blank=True)
    age_confirmed = models.BooleanField(default=False)
    guardian_consent = models.BooleanField(default=False)
```

Set `AUTH_USER_MODEL = "accounts.User"` in `base.py`. Then:

```bash
docker compose up -d db            # Step 4
python manage.py makemigrations accounts && python manage.py migrate
```

**Done when** `createsuperuser` asks for an email address, not a username.

### Step 4. Set up Docker Compose for development

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment: { POSTGRES_DB: nrstatlab, POSTGRES_USER: nrstatlab, POSTGRES_PASSWORD: dev-only }
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    env_file: .env
    volumes: [".:/app"]
    ports: ["8000:8000"]
    depends_on: [db]
volumes: { pgdata: {} }
```

- Set `DATABASE_URL=postgres://nrstatlab:dev-only@localhost:5432/nrstatlab` in `.env`.
- The Dockerfile uses `python:3.12-slim`, installs the requirements, and runs `collectstatic` at
  build time.

**Done when** `docker compose up` shows the Django welcome page.

### Step 5. Write the models, then import the content

Write the models from `PROMPT.md` §4, app by app, and register each in its `admin.py`. Two design
points matter.

- **`Unit.legacy_path` and `Page.legacy_path` are unique.** A path is the page id, for example
  `statistics/sampling-theory/unit2.html`. The same id is used by `progress.js`, so browser progress
  imports without translation.
- **Answers never leave the server.** `Question.answer` and `Choice.is_correct` are never
  serialised to templates before an attempt is submitted. Every "question for display" object must
  go through one function, `assessments.services.public_view(question)`.

Now write `apps/study/management/commands/import_site.py`. In outline:

```python
ROOT = settings.CONTENT_DIR            # the submodule
SITE_ROOT = settings.SITE_ROOT_DIR     # var/site_root

def handle(self, dry_run=False, **kw):
    catalogue = load_module(ROOT / "tools/course_catalogue.py")
    index = json.loads((ROOT / "assets/progress-index.json").read_text())
    is_stub = load_module(ROOT / "tools/stubs.py").is_stub
    sitemap = load_module(ROOT / "tools/build_sitemap.py")

    # 1. Copy every non-HTML file (css, js, png, svg, pdf, json …) to SITE_ROOT, same relative path.
    # 2. For each .html under ROOT (skipping .git, archive/):
    #      stub     -> Redirect(old_path, new_path read from the meta refresh)
    #      indexed  -> split the file:
    #                    head_html = <head> contents minus <title>, canonical, og:url (rebuilt by the template)
    #                    nav       = between <!-- site-nav --> and <!-- /site-nav --> (dropped; Django renders it)
    #                    body_html = between <!-- /site-nav --> and <footer class="sitefoot">
    #                  -> Unit if listed in progress-index.json (markable), else Page
    # 3. Programmes/Courses from course_catalogue.py (order, group, level).
    # 4. Exams + SyllabusItems + SyllabusLinks from tools/exams/*_map_data.py.
    # 5. SolvedPapers + Questions (Step 9).
    # 6. Save only when content_hash changed; wrap everything in one transaction.
    # 7. Assert the counts; raise CommandError on any mismatch:
    expected = {"courses": 56, "markable": 310, "indexed": 675, "redirects": 946, "exams": 5,
                "ugc_mcqs": 500, "ugc_solved_2026": 150, "appsc_2025": 150, "appsc_2022": 150}
```

- **Keep links working as they are.** Keep each page's own relative links unchanged. The page is
  served at the same path, so `href="index.html"` and `../../assets/site-base.css` still resolve.
- **Serve the non-HTML files.** In `base.py`, set `WHITENOISE_ROOT = SITE_ROOT_DIR`. WhiteNoise then
  serves the copied CSS, images and PDFs at their original URLs.
- **Keep HTML out of that folder.** Never copy HTML into `SITE_ROOT`. If you did, WhiteNoise would
  serve those pages directly and Django would never render them.

**Done when:**
- `python manage.py import_site --dry-run` prints the expected counts;
- a real run creates the rows;
- a second run changes nothing.

### Step 6. Serve every page at its old address

```python
# config/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("me/", include("apps.progress.urls")),        # dashboard, import
    path("test/", include("apps.assessments.urls")),   # unit tests
    path("papers/", include("apps.papers.urls")),      # attempts
    path("readiness/", include("apps.examinations.urls")),
    path("healthz", core_views.health),
    path("", core_views.page, {"legacy_path": "index.html"}),
    re_path(r"^(?P<legacy_path>.+\.html)$", core_views.page),   # last: every legacy page
]
```

`core_views.page` works through these checks in order:
1. Look up a `Redirect`. If there is one, return a 301.
2. Look up a `Unit`, then a `Page`.
3. If neither exists, return the site's own 404 page.

`templates/base.html` rebuilds each page:
- the `<head>` from `head_html`, plus the canonical and og:url for the new domain;
- the navigation, rendered from the same data as `tools/site_nav_model.py`, with an account link
  added ("Sign in", or the learner's name);
- then `body_html` and the footer;
- on markable units, a slot for the "Mark as studied" control.

Keep `progress.js` for guests. For signed-in users, the template sets `data-progress="server"`, and
a small script uses the server's endpoints instead of localStorage.

**Test it the way the static site was tested.**
- A pytest test requests every indexed path. Each must return 200 and match today's text: compare
  the visible text of `body_html` with the original page's body.
- It requests every stub path, and each must return 301.
- Run `tools/check_contrast.js` and the link crawl against `http://localhost:8000`.

**Done when** all 675 indexed paths return 200 with identical text, and all 946 stubs return 301.
**End of Phase 1: review.**

---

## Phase 2: Accounts and progress

### Step 7. Add accounts, privacy, export and deletion

**Configure allauth** (version 65 or later):

```python
INSTALLED_APPS += ["allauth", "allauth.account", "allauth.socialaccount",
                   "allauth.socialaccount.providers.google", "axes", "django_otp",
                   "django_otp.plugins.otp_totp"]
MIDDLEWARE += ["allauth.account.middleware.AccountMiddleware", "axes.middleware.AxesMiddleware"]
AUTHENTICATION_BACKENDS = ["axes.backends.AxesStandaloneBackend",
                           "django.contrib.auth.backends.ModelBackend",
                           "allauth.account.auth_backends.AuthenticationBackend"]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher",
                    "django.contrib.auth.hashers.PBKDF2PasswordHasher"]
```

**Sign-up asks for:**
- email and password;
- a display name;
- confirmation of age 18 or over, or of guardian consent;
- acceptance of the privacy terms, recorded in `terms_accepted_at`.

Nothing else.

**Privacy page.** Say, in plain words:
- what is stored: email, display name, progress and test attempts;
- why it is stored;
- that there are no ads and no trackers;
- how to export or delete your data.

**Export.** A `/me/export` view returns one JSON file with the profile, progress and attempts.

**Deletion.**
1. `/me/delete` asks for the password again.
2. It anonymises the learner's `Attempt` rows: it sets `user = NULL` and keeps the responses for
   item statistics.
3. It deletes the user and the profile.
4. It sends a confirmation email.

**Security.** Put the admin behind django-otp: use the OTP admin site, and require TOTP for staff.

**Done when:**
- sign-up sends a verification email (use the console backend in development);
- login is rate-limited after 5 failed attempts;
- export and delete both work in an end-to-end test.

### Step 8. Add synced progress, the dashboard, and browser import

**Service functions** (`apps/progress/services.py`): these are the only way to change progress.

```python
def mark_studied(user, unit):   ...  # not_started/studying -> studied; sets studied_at
def mark_passed(user, unit, score): ... # called by assessments after a pass
def course_counts(user, course): ...  # {"units": 5, "studied": 3, "passed": 2}
def import_browser(user, page_ids):   # returns {"imported": n, "ignored": [...]}
    # only ids that match a markable Unit; never downgrade an existing status; source="browser_import"
```

**Endpoints**, each an HTMX POST with CSRF protection:
- `POST /me/progress/<unit_id>/studied` returns the updated button.
- `POST /me/progress/import` takes JSON `{"done": [...ids]}`.

**Browser import.** This runs on the first page load after sign-in:

```javascript
try {
  const s = JSON.parse(localStorage.getItem('nrstatlab.progress.v1') || 'null');
  if (s && s.v === 1 && s.done && Object.keys(s.done).length) {
    // show a banner: "Bring over the progress saved in this browser (N pages)?"  [Bring over] [Not now]
    // on click: fetch('/me/progress/import', {method:'POST', headers:{'X-CSRFToken': token,
    //   'Content-Type':'application/json'}, body: JSON.stringify({done: Object.keys(s.done)})})
  }
} catch (e) { /* storage blocked: do nothing */ }
```

- After a successful import, remember in localStorage that the offer was accepted, so it is not
  shown again.
- Do not delete the guest data.

**The dashboard** (`/me/`) shows:
- courses in progress, as "3 of 5 studied, 2 passed";
- the last five test scores;
- weak topics: the tags with the lowest share correct across the learner's responses;
- the study streak: consecutive days with at least one studied unit or submitted test;
- a readiness card if a target exam is set (Step 12).

**Done when** progress marked on one browser shows on another, and an import of mixed valid and
invalid ids reports both correctly. **End of Phase 2: review.**

---

## Phase 3: Unit tests

### Step 9. Seed the question bank

Import questions only from keyed sources. Each importer is a management command and is idempotent.

| Source | Where | How to read it | Count |
|---|---|---|---|
| UGC NET MCQs | `content/exams/ugc-net/mcqs.html` | Each `div.mcq` holds a stem (`div.q`, with the "N." prefix removed) and `ol.options > li` (four options). The key is the first letter of `details p`. The rest of that paragraph is the solution | 500 |
| UGC NET solved 2026 | `content/exams/ugc-net/solved-2026.html` | The same `div.mcq` blocks, but the number is in `span.qn` ("Q1.") and the key is in `details p strong` as "Answer: (D) …". Keep the question numbers; the 7 `.flag` notes become `flag_reason` | 150 |
| APPSC 2025 and 2022 | `content/tools/exams/appsc_paper_2025.json`, `appsc_paper_2022.json` | `questions[]` with `n`, `stem`, `options`, `key`, `marks`. The worked solutions and study links are in `appsc_paper_data.py` and `appsc_paper_2022_data.py` | 150 + 150 |
| Unit practice sets | Practice blocks on unit pages | Only where the page gives the answer | varies |

**Steps:**

1. **Link each question to units.**
   - APPSC items have "Study this" links; UGC NET items have unit numbers and syllabus maps. Turn
     each link into a `QuestionUnit` row.
   - A question with no unit link stays in the exam bank only, and is never used in unit tests.
2. **Flag the six contested keys** from `docs/AUDIT-2026-09.md` §5.1:
   - Unit 5 Q50, Unit 7 Q14, Unit 8 Q16, Unit 3 Q39, Unit 5 Q41 and Unit 2 Q45;
   - set `status = flagged`, with the reason.
3. **Mark withdrawn APPSC questions** as `withdrawn = True` on their `PaperQuestion`, with the
   Commission's note: 2025 Q134, and 2022 Q51 and Q81.
4. **Check the count.** Write a recheck: each importer's count must equal the source's count, and
   every key must be one of the question's own options.
5. **Write questions for the units that have none.** This is content work that runs alongside the
   code, course by course. For each new question:
   - an author drafts it, and AI help is allowed here;
   - a script recomputes every number, and its output goes in `recompute_log`;
   - a second person reviews it;
   - only then is it published.

   A unit's test opens by itself once it has 10 published questions.

**Done when** the counts match their sources and the six flagged keys can never be scored (a test
proves it).

### Step 10. Build the unit test engine

**When a test opens:** the unit's status is `studied` or `passed`, and it has at least
`UnitTest.n_questions` published questions.

**How questions are chosen**, in `assessments/services.py`:

```python
def draw(unit_test, user, seed):
    pool = published questions linked to unit_test.unit, excluding flagged
    unseen = pool minus questions this user has already answered in this unit's tests
    # stratify by difficulty band (easy/medium/hard by ItemStats or author estimate):
    take roughly equal numbers from each band, from `unseen` first, then from the rest
    shuffle question order and each question's options with random.Random(seed)
    return question ids (stored on the Attempt with the seed, so a reload shows the same test)
```

**Attempt lifecycle.**
1. Start: create an `Attempt` with its seed. The learner may have only one open attempt per test.
2. Answer: each question is saved as a `Response` through HTMX, so a dropped connection loses
   nothing.
3. Submit: mark the `Attempt` submitted, score it, and freeze it.
4. Results.

**Scoring, by type.** All scoring is on the server.

| Type | Correct when |
|---|---|
| single | The chosen choice is the correct choice |
| multiple | The chosen set equals the correct set exactly (no part marks at first) |
| numeric | \|answer − key\| ≤ tolerance (store the tolerance per question, e.g. 0.005 for 2-dp answers) |
| assertion-reason | Scored like single, with the standard four options |
| match | Every pair correct |

**Results page:**
- the score and whether it is a pass;
- each question with the learner's answer, the correct answer and the worked solution;
- a link back to the section of the unit that teaches it.

A pass calls `progress.services.mark_passed`.

**Retakes** are always allowed. They draw unseen questions first, the best score is kept, and every
attempt stays in history.

**Security.**
- The answer and `is_correct` are never in the page before submission.
- A submitted attempt cannot be changed.
- An attempt id belongs to its owner only: check `attempt.user == request.user` on every view.

**Done when** the unit tests pass for every question type, for unlocking, for retake selection, and
for "no answers in the HTML before submit". **End of Phase 3: review.**

---

## Phase 4: Old papers

### Step 11. Build practice mode and exam mode

**Practice mode** (`/papers/<paper>/practice`) shows one question at a time:
- "Show solution" reveals the official key and the worked solution;
- progress through the paper is saved.

**Exam mode** (`/papers/<paper>/exam`) is the whole paper on one page, with question navigation.

- **Timer.** Use one only if the paper's header records the official duration. The APPSC JSON
  header has `Duration`; show it with its source ("Duration as printed on the Commission's paper").
  - Where no official duration is recorded, there is no timer. Do not invent one.
- **Negative marking.** Apply it only from the recorded official scheme, such as the APPSC header's
  `Section Negative Marks` and each question's `marks` field ("Correct Marks : 1 Wrong Marks : 0.33").
  Show the scheme and its source before the paper starts.
- **Withdrawn questions** are shown with the Commission's note and left out of the score and of the
  maximum.
- **Submit** freezes the attempt. The review page shows each question with the learner's answer,
  the official key, whether they were right, and the worked solution. It also shows totals by
  section, and a link to the unit that teaches each question.

**Done when** an end-to-end test sits the APPSC 2025 paper in exam mode, the score matches a
hand-computed score (including negative marks), and Q134 is shown but not counted.
**End of Phase 4: review.**

---

## Phase 5: Readiness

### Step 12. Build exam readiness

The data is already imported (Step 5): `SyllabusItem` for each exam, and `SyllabusLink` from items
to units with a depth of `deep` or `brief`.

**For each syllabus item:**

```
weight(link) = 2 if deep else 1
item_readiness = Σ weight(link) × [unit passed] / Σ weight(link)      (items with no linked unit: "not covered on this site")
exam_readiness = mean of item_readiness over items that have at least one linked unit
```

**The readiness page** (`/readiness/<exam>`):
- the overall figure;
- each syllabus item with its linked units, their status, and a small bar;
- the items the site does not cover, listed plainly;
- **next three units to study**: units not yet passed, ranked by how many syllabus items of the
  target exam they serve, then by course order.

Readiness counts only passed units. Studied units are shown but do not count.

**Done when** a test fixture with known passes gives the hand-computed readiness.
**End of Phase 5: review.**

---

## Phase 6: Quality loop

### Step 13. Add item analysis and the reviewer workflow

**A nightly job** (django-q2 schedule or cron: `python manage.py item_stats`) processes each question
with 30 or more responses on submitted attempts.

- **Difficulty:** `p = correct / n`.
- **Point-biserial against the rest-score:**
  - let R be each attempt's score *without* this item;
  - let M1 and M0 be the mean R of those who answered correctly and incorrectly;
  - let s be the standard deviation of R, using n in the denominator;
  - then `r_pb = (M1 − M0) / s × √(p (1 − p))`.
- **Flag for review** if `r_pb < 0`, `p > 0.95` or `p < 0.10`: set `status = flagged` with the reason,
  and notify reviewers.

**Reviewer workflow in the admin:**
- a queue of `draft` and `flagged` questions;
- a side-by-side preview with MathJax;
- the recompute log;
- "Approve", which sets reviewed and published, records the reviewer, and refuses if the reviewer
  is the author;
- "Send back", which requires a note.

Every change is kept in history (`django-simple-history`, or a small audit table).

**Done when** fixture data produces the expected `p` and `r_pb` to 3 decimals, and a question with
a negative `r_pb` is flagged automatically. **End of Phase 6: review.**

---

## Phase 7: Launch

### Step 14. Front end and accessibility

- **Styles.** Load the site's CSS from its original paths, served by WhiteNoise (Step 5). Add one
  small `static/app.css` for the account bar, buttons, test pages and dashboard, using the same
  colour tokens as `site-base.css` and `site-dark.css`.
- **MathJax.** Self-host MathJax 3 under `static/mathjax/`, and use the same configuration as the
  pages. On test pages, typeset again after each HTMX swap: `MathJax.typesetPromise([el])`.
- **Layout.** Mobile first at 390 px, with no horizontal page scroll; wide formulas and tables
  scroll inside their own box, as they do today. Every control works from the keyboard, with a
  visible focus state.
- **Checks.** Run `tools/check_contrast.js` (0 below AA in both themes) and the link crawl against
  the Django site.

### Step 15. Testing

- **pytest.** Keep unit and integration tests in `tests/` and use factory_boy factories. Coverage
  must be 90% or more on `assessments` and `progress`.
- **Must-have tests:**
  - scoring for every type;
  - unlocking;
  - retake selection;
  - no answers in the HTML before submit;
  - readiness arithmetic;
  - item statistics;
  - browser import, valid and invalid;
  - export and delete;
  - every legacy path returns 200 or 301.
- **Playwright** runs at 390 px and 1280 px:
  - a guest reads a unit;
  - sign-up with verification;
  - mark studied;
  - fail a test, retake it and pass;
  - progress shows in a second browser context;
  - a localStorage import;
  - APPSC exam mode;
  - export, then delete.
- **CI** (`.github/workflows/ci.yml`):
  - check out with submodules;
  - start Postgres as a service;
  - run `ruff check`, `python manage.py check --deploy` (with the prod settings) and
    `makemigrations --check`;
  - run `import_site --dry-run`, `pytest --cov`, and Playwright against `runserver`.

### Step 16. Security and privacy settings

```python
# config/settings/prod.py
DEBUG = False
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000; SECURE_HSTS_INCLUDE_SUBDOMAINS = True; SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
CONTENT_SECURITY_POLICY = {   # django-csp 4.x
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'"],          # MathJax self-hosted; move inline config into a file
        "style-src": ["'self'", "'unsafe-inline'"],   # MathJax CHTML injects styles
        "img-src": ["'self'", "data:"],
        "font-src": ["'self'"],
        "frame-ancestors": ["'none'"],
    }
}
```

- **Secrets** live only in environment variables on the host: `SECRET_KEY`, `DATABASE_URL`, email
  keys and OAuth keys.
- **The admin** is at a non-default path, TOTP is required, and staff accounts are few.
- **Logs** never contain answers, passwords or tokens.
- **Backups** run daily with 30-day retention. Test a restore once before launch, then monthly.
- **Legal review.** Before launch, check the privacy page and the handling of learners under 18
  against India's DPDP Act, 2023 and its Rules.
- **Security review.**
  - Run `python manage.py check --deploy` and fix what it reports.
  - Check authorisation on every view that takes an id (attempts, exports).
  - Do a dependency audit (`pip-audit`).

### Step 17. Choose hosting and deploy

Compare two options. Check current prices before choosing; they change.

| | Managed platform (e.g. Render, Railway, Fly.io) | Small VPS (e.g. a 2 vCPU / 4 GB Linux VM) |
|---|---|---|
| Setup | Connect the repo; set env vars; add managed Postgres | Docker, Caddy or Nginx for HTTPS, systemd, Postgres, backups |
| Upkeep | Low | You patch the OS, rotate backups, watch disk |
| Good for | Launch and the first months | Steady traffic, lower monthly cost |

**Deploying, on either option:**
1. Build the image.
2. Run `migrate`, then `import_site`, then `collectstatic`.
3. Start Gunicorn: `gunicorn config.wsgi --workers 3 --timeout 30`.
4. Check that `/healthz` returns 200 and confirms the database connection.

**Jobs:** `item_stats` runs nightly, and the email queue runs if you use one.

**Monitoring:** uptime checks on `/` and `/healthz`, error alerts, and a weekly look at slow
queries.

### Step 18. Staging and load testing

- **Staging.** A staging copy on its own subdomain uses a copy of production settings and fake
  accounts only.
- **Load test.** Script a test (for example with Locust) that reads public pages and takes unit
  tests. Aim for p95 server time under 300 ms on public pages at your expected peak.
- **Caching.** Cache the rendered public pages per path for anonymous visitors, using Django's
  cache with Redis or the database. Signed-in users get fresh pages.

### Step 19. Write the runbook

Write down each of these procedures:
- deploy;
- roll back;
- restore from backup;
- rotate a secret;
- handle a reported wrong answer key (flag it, fix it, publish it, rescore attempts that included
  it, all within 7 days);
- handle a data-deletion request that arrives by GitHub Issue: point the person to the self-service
  delete, and never ask them to post personal details publicly.

### Step 20. Move the domain from GitHub Pages

A Django application cannot run on `nrstatlab.github.io`. The move:

1. **Point the new domain at the application.** Serve every page at the same path as today, for
   example `https://<new-domain>/statistics/sampling-theory/unit2.html`.
2. **Update the canonical tags, og:url, `sitemap.xml` and `robots.txt`** in Django so they use the
   new domain.
3. **Turn the GitHub Pages site into redirects.** Add a small script to this content repository.
   It writes, in the Pages publish folder, a redirect page for every path. Each redirect page has a
   meta refresh to the new domain, the same path, a canonical link to it, and `noindex`. This is
   the same stub pattern the site already uses (`tools/stubs.py`).
4. **Tell the search engines.** Submit the new sitemap in the search engines' webmaster tools.
5. **Watch for 404s for two weeks.**
6. **Rollback.** If something goes badly wrong, republish the previous Pages build. Content keeps
   being authored in this repository either way.

**Done when** a crawl of the old addresses lands every one of them on the same page at the new
domain. **End of Phase 7: launch.**

---

## After launch: what the CEO watches

Every week, look at:
- units passed per weekly active learner (the north star);
- the share of new accounts that pass a first test within 7 days;
- week-4 retention;
- the first-attempt pass rate per test (a healthy band is 50–80%);
- the share of questions with a point-biserial of 0.2 or more;
- page speed;
- reported key errors and how long each took to fix.

Set targets after the first month of real data (see Part A of `Webapp.docx`).

The next ideas, in order:
1. spaced review of weak topics;
2. teacher classes;
3. certificates of completion;
4. an AI study helper whose answers are checked before they are shown.
