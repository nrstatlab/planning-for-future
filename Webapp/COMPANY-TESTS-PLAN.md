# StatsTricks360 Learn: company tests

**2 October 2026.** By StatsTricks360. Questions and corrections: GitHub Issues.

A CEO plan for a question from the owner: a company may ask us to test its employees on chosen topics
or units. Can we offer that, and how?

**The owner's choices behind it:**
- **Build the full feature**, not a pilot run by hand.
- **The questions** come from a **private pool plus our checked bank**. The private pool lives only
  in the app's database, never in the public content repository.
- **Paid, per employee per test.** This is the first paid extra under "free core, paid extras later".
- **The company sees** each employee's score, pass or fail, and score by topic, for that test only.
  The employee is told this before starting.

**About the facts here:**
- Prices and dates are the plan's own proposals, marked as such.
- Facts about other platforms and the law name their source and say whether it is official or
  reported.
- Nothing is built before the 28 November launch; building waits for the owner's approval.

---

## 1. Summary, as CEO

**Yes, and most of it is built already.** A company test is a unit test with these changes:
- a different owner;
- a guest list;
- a window;
- a results page.

The app already has these parts:
- it draws a test from checked questions;
- it gives each attempt its own option labels, so answers can't be passed on by letter;
- it keeps a hard deadline, with a 30-second grace;
- it scores by section;
- it runs every question through a two-person review.

What's new is the company's side:
- an organisation and its coordinator;
- invitations;
- a private question pool;
- results by topic, and a CSV;
- a usage count for invoices.

**Who would buy:** teams whose work is statistics, and who now test with spreadsheets or nothing:
- analytics and data teams;
- risk and actuarial teams;
- clinical research;
- manufacturing quality;
- market research;
- college placement cells.

**What it costs us:**
- about two months of build, January to February 2027;
- 60 private questions for the pilot;
- about an hour a week of the owner's selling.

**The trade-off:** owner review rises in February and March, so **the Data Analyst path moves to
April–May 2027.** That is decision 4 in §12.

**The order:**
1. Build in January and February 2027.
2. A free pilot with one company in March.
3. Paid from April.

---

## 2. What companies get

A **coordinator** account for each organisation. The coordinator:

**Creates a test:**

| Setting | Choices |
|---|---|
| Title | Free text, e.g. "Quality team: SQC check, March 2027" |
| Topics | Units picked from the courses, or lines of an exam map or a learning path; private-pool topics as well |
| Questions | How many, e.g. 20–50; drawn evenly across the chosen topics |
| Time limit | Minutes |
| Window | Opens and closes (date and time) |
| Pass mark | A percentage |
| Attempts | One |
| Answers | Shown to employees after the window closes, or never |

**Invites employees:**
- by a list of email addresses, or a CSV upload;
- each gets a one-time link;
- they sign in, or create a free account, and the link joins them to the test.

**Sees results,** when the window closes or as people finish:
- each employee's score, pass or fail, time taken, and score by topic;
- the team's average by topic, showing where the team is weak;
- a CSV download of the same.

**Nothing else** from an employee's account is visible to the company: not their study progress,
other tests, or readiness.

The coordinator can also:
- **void a question for everyone** if it is disputed, and all scores are recomputed. This is the
  same rule as the papers' "not counted".

---

## 3. What employees see

1. **A notice before starting.** It says:
   - who set the test;
   - what the company will see: score, pass or fail, time, and score by topic;
   - how long the results are kept;
   - that leaving the tab is counted, if the company turned that on.

   The employee presses "Start" to accept.
2. **The test, timed,** in the same screen as the paper exam mode: a countdown, and answers saved as
   they go.
3. **Their own result** at once: the score and the score by topic.
4. **The answers and the working** come only after the window closes, so nobody passes them to a
   colleague who hasn't sat yet. Or they never come, if the company chose that.

The employee keeps their free account and everything in it. The company test appears in their data
export.

---

## 4. How it's built on what exists

Every part below exists in the application repository today and is reused, not rewritten.

| Need | What exists | Where |
|---|---|---|
| A test drawn from chosen units | The unit-test draw from the published questions of a unit | `apps/assessments/engine.py` (`draw`, `pool`) |
| Answers that can't be shared by letter | Option labels and order unique to each attempt | `engine.token` |
| A hard deadline | Exam-mode deadline, answers refused after it, a 30-second grace | `apps/papers/services.py` (`GRACE`) |
| Score by topic | The paper review's totals by section | `apps/papers/services.py` (the review) |
| Void a question | The papers' "not counted" with a note | `apps/papers/services.py` |
| Question quality | The review queue: no one approves their own work, a history, and nightly item statistics | `apps/assessments/review.py`, `stats.py` |
| Accounts | Sign-up with email confirmation, 2-factor for staff, export and deletion registries | `apps/accounts/services.py` (`register_exporter`) |
| Authorisation discipline | Every route that takes an id is listed with its protection, and tested | `tests/test_authorisation.py` |
| App boundaries | Which app may call which, enforced by a test | `tests/test_dependencies.py` |

**What's new:**

- **An eighth app, `organisations`.**
  - **Its models:**
    - `Organisation`;
    - `Membership` (a coordinator or an employee);
    - `CompanyTest` (the topics, the number of questions, the minutes, the window, the pass mark,
      whether answers are shown, and whether tab-leaving is counted);
    - `Invitation` (an email, a one-time token, when it was accepted, and the attempt).
  - **What it may call:** `assessments`, `study`, `examinations` and `accounts`, and only through
    their `services.py`. `tests/test_dependencies.py` gains the eighth app.
- **In `assessments`:**
  - `Attempt.kind` gains `company_test`. The database rule tying each kind to its target is
    extended to match.
  - `Question.visibility` (public or private).
  - A draw over several units plus the private pool, evenly by topic.
  - All of this is reached through `assessments/services.py`.
- **The routes:**
  - `/org/…` for the coordinator: tests, invitations, results, the CSV;
  - `/t/<token>` for the employee: the notice, the test, the result.

  Each goes into the authorisation table:
  - a coordinator sees only their own organisation;
  - an employee sees only their own attempt;
  - a used or expired token shows nothing.
- **The tab-leave count** is a small script served by the app, within the existing Content
  Security Policy. It sends a count, not a recording.
- **The checks,** as for every phase:
  - tests for each rule;
  - a mutation test for each new check;
  - a walk through the coordinator's and the employee's screens;
  - CI green.

---

## 5. The private pool

- Each question gets a **visibility**: public or private.
- **Private questions are never:**
  - on the site;
  - in public unit tests, papers or practice;
  - in the public export or search.

  A test proves that no public route can reach one.
- **They are written as the path questions are.** Claude drafts each with a worked answer and a
  recompute log; the owner approves it in the review queue. No one approves their own work.
- **They are loaded by a new command, `import_private_questions`,** from a JSON file kept outside
  the public repository, in the same shape as the public bank. The content repository is the live
  site, so private questions never go there.
- **Backed up** with the database, as everything else is.
- **The first 60** cover the pilot company's topics. More come as companies ask for topics our bank
  doesn't test.

---

## 6. Integrity

**What we offer:**
- a different draw for each person, in a different order, with option labels unique to them;
- one attempt, and a deadline the server enforces;
- private questions that aren't public;
- answers held back until the window closes;
- if the company wants it, a count of how often each person left the tab, shown to the coordinator.

**What we don't offer, and don't claim:**
- webcam or screen proctoring;
- browser lockdown;
- identity checks beyond the invited email.

The offer says so plainly: these are low-stakes skill checks, not hiring exams.

---

## 7. Data protection

**Who is who, under the Digital Personal Data Protection Act, 2023:**
- The company decides why its employees are tested, so it is the **Data Fiduciary** for the
  results.
- We process them on its behalf, so we are its **Data Processor**.
- Section 8(2) says a Data Fiduciary may use a Data Processor only under a valid contract.

So:
- **A short data-processing agreement** with each company, drafted with the legal review that the
  launch already needs. It covers:
  - what we process: name, email, answers, scores, times;
  - why;
  - how long it is kept;
  - security;
  - telling the company about a breach;
  - deletion at the end.
- **The notice before the test** (§3) tells the employee the same.
- **Retention:** results are kept for an agreed time (the proposal is 12 months), then deleted
  automatically. A nightly command does this, as the item statistics are done.
- **Export and deletion:**
  - the employee's export includes their company tests;
  - what happens to a company's copy when an employee deletes their account is for the legal review
    to settle.
- **The minimum:** the company never sees anything beyond §2.

---

## 8. Price and customers

**The price, a proposal to test with the pilot:**
- The first company is **free**: the pilot.
- Then about **₹150–300 per employee per test**, with a minimum per test, e.g. ₹3,000.
- An employee counts **once they start**. An invitation never used costs nothing.

For comparison:
- The large platforms (Mercer Mettl, iMocha) quote custom prices.
- One India-focused platform publishes about ₹100 a credit.
- These are reported prices (sources in §13).
- They sell hiring tests with proctoring. We sell a narrower thing: checked statistics questions on
  the company's own topics, with results by topic.

**Billing, by hand at first:**
- The coordinator's page and a `company_usage` command show the count per test and per month.
- An invoice goes by email; there is no payment gateway at first.
- GST registration, the invoice format and the contract terms come with a professional's advice.

**Who it's for:**

| Customer | Why statistics | Our topics |
|---|---|---|
| Analytics and data teams | Hypothesis tests, regression and sampling are daily work | Statistical inference, regression, the Data Science courses |
| Banks' and insurers' risk and actuarial teams | Probability, distributions and time series | Probability, distributions, time series |
| Pharma and clinical-research firms | Trial design and analysis | The clinical-trials course, design of experiments |
| Manufacturing quality | Control charts, acceptance sampling, Six Sigma | Statistical quality control |
| Market-research firms | Sampling and surveys | Sampling theory, survey methods |
| College placement cells | A check before campus interviews | Any units, chosen by the college |

**Selling,** about an hour a week of the owner's time:
- a one-page offer;
- a **sample test** anyone can sit;
- **20 companies approached** on LinkedIn, starting with people the owner knows;
- placement cells reached through the colleges whose students already use the site.

---

## 9. Timing, and the trade-off

Code is Claude's work. The owner's time goes on approving private questions and on selling.

| When | What | The owner's part |
|---|---|---|
| By 15 December 2026 | Decide on the Data Analyst move (decision 4) | The decision |
| January – February 2027 | Build: the models, the private pool, the coordinator's pages, invitations, the employee's flow, results and the CSV, usage counts. Tests, mutations, the authorisation table, a walk | Try it on your computer, as with every phase |
| By 28 February 2027 | Name the pilot company (decision 2) | The approaches |
| February – March 2027 | 60 private-pool questions for the pilot's topics; the data-processing agreement drafted with the legal review | Review about 15 private questions a week |
| March 2027 | A free pilot with one company | Be the pilot's contact |
| From April 2027 | Paid, per employee per test | Invoices; about an hour a week of selling |

**The trade-off with the learning paths:**
- In February and March, owner review would be about 45 questions a week: 30 for Statistics
  Foundations and 15 for the private pool.
- To keep that possible for one part-time person, **the Data Analyst path moves from March–April to
  April–May 2027.**
- Statistics Foundations keeps its dates.

---

## 10. Success

| Measure | Target |
|---|---|
| A pilot company has run a test | By 31 March 2027 |
| The pilot's coordinator would use it again | Yes, asked at the end of the pilot |
| Paying companies | 3 by 30 June 2027 |
| Employee-tests | 200 by 30 June 2027 |
| Disputed questions | Under 2% of the questions used, each settled within a week |

These come from the app's own counts (`company_usage`, the review queue); no tracker is added.

---

## 11. Risks

| Risk | What we do |
|---|---|
| Selling takes time one person doesn't have | A one-page offer and a sample test; 20 approaches, not 200 |
| Companies ask for proctoring, single sign-on or their own branding | Say no at first, note each request, and build only on demand |
| A dispute about a score | Every question is checked and reviewed, with item statistics; the coordinator can void a question for everyone |
| Personal data | The data-processing agreement, the notice before the test, a retention limit, export and deletion |
| Private questions leak | A per-person draw from a larger pool; rotate the pool; retire leaked questions |
| Seeming to certify people | "A skill check set by your company", never "certified" or "accredited" |
| It crowds out the exam work | It starts only after the launch and Wave 1; the Data Analyst move keeps review to one load a week |

---

## 12. Decisions needed from you

| # | Decision | By |
|---|---|---|
| 1 | The price: confirm or change ₹150–300 per employee per test, and the minimum | At the pilot, March 2027 |
| 2 | The pilot company | 28 February 2027 |
| 3 | How long results are kept (proposal: 12 months) | With the legal review |
| 4 | Accept the Data Analyst path moving to April–May 2027 | 15 December 2026 |

---

## 13. Sources

Official:
- The Digital Personal Data Protection Act, 2023, section 8 (Data Processors under a valid
  contract), as published by MeitY:
  https://www.meity.gov.in/static/uploads/2024/06/2bf1f0e9f04e6fb4f8fef35e82c42aa5.pdf

Reported:
- Assessment platforms in India and their pricing (Mercer Mettl and iMocha custom; Goodfit ₹100 a
  credit), in a guide published by one of the vendors. Seen in search results on 2 October 2026;
  the page itself was blocked from here, so check it before quoting:
  https://goodfit.so/guides/best-pre-employment-assessment-tools-india

Our own:
- the application repository on 2 October 2026 (`apps/assessments/engine.py`,
  `apps/papers/services.py`, `apps/assessments/review.py`, `tests/test_authorisation.py`,
  `tests/test_dependencies.py`);
- the review loads in `PATHS-AND-EXAMS-PLAN.md` §5.
