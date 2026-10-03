# NRSTATLAB Learn: the launch plan for 28 November 2026

**1 October 2026.** By NRSTATLAB. Questions and corrections: GitHub Issues.

Written from three seats at once: the owner as CEO, the technical lead, and the marketing lead. It
covers what we have, what the market looks like, what success needs, and the work week by week to
28 November and through the first three months.

**The owner's choices behind it:**
- a free core, with paid extras considered later;
- UGC NET Statistics first, then APPSC Assistant Statistical Officer (ASO);
- one person, part time, with Claude doing the technical build on request;
- English only;
- success means **500 or more signed-up learners by 28 February 2027**;
- the budget is still open, so two options are costed.

**About the facts here.** The official sites (NTA, APPSC) could not be opened from the research
environment. Every exam date below comes from secondary sources and is marked so. Each is on the
owner's list to confirm at the official source in week 1. Nothing goes on the site itself without a
named official source; that rule stands.

---

## 1. Summary, as CEO

**The bet.** UGC NET Statistics (code 107) is a new subject:
- **its first sitting was the June 2026 cycle**, and **December 2026 is only its second** (reported);
- few platforms have material made for it;
- we already have the **June 2026 paper solved**: all 50 Paper I and 100 Paper II questions,
  each worked out, not just answered.

We aim to be the free, trustworthy home for code 107 while the field is still open.

**The calendar works for us** (reported dates):
- the December 2026 exam is reported for **14–19 December**;
- launch on **Saturday 28 November** is **16 days before it**, the final-revision weeks, when timed
  papers, unit tests and "what is left to study" matter most;
- APPSC has notified **196 ASO posts**, with applications **13 October to 2 November 2026**. Those
  candidates are preparing through the same months.

**The three moves:**
1. **Promote the free site now.** The study site is already live on GitHub Pages. Weekly posts can
   point at it from today. The app is linked only after your sign-off.
2. **Launch the app on 28 November** as a soft launch, the cut-over plan's stage C: the live site
   stays as it is, and gains a "Sign in to save your progress" link.
3. **Solve the December 2026 paper quickly** once NTA publishes the paper and its key. That would be
   the second solved code-107 paper anywhere. It is the strongest reason for a learner to search for
   us, share us and come back for June 2027.

**What could stop us:**
- **one part-time person:** the plan keeps the weekly load to about 6–10 hours;
- **no second reviewer yet:** a question you write cannot be approved until someone else is named
  (you settled the 37 questions in the queue yourself on 2 October);
- **the open technical choices:** host, domain and email must be made in the next ten days to leave
  time for staging.

---

## 2. What we have

| Area | What exists today | Where it stands |
|---|---|---|
| Study site | **693 pages** (675 in the sitemap), 55 courses, 5 exams, 266 lab programs, an A–Z topic index, search | Live on GitHub Pages; free, no login, no adverts |
| UGC NET Statistics | All **10 units** with study pages and a **10-question unit test** each; **500 unit MCQs**, all scored (the 6 contested keys settled on 2 October); the **June 2026 paper solved** (50 Paper I + 100 Paper II); the syllabus map; readiness | The strongest offer: ready for December |
| UGC NET Paper I | The General Paper every candidate sits: its official syllabus mapped (71 lines), and notes and **20 model MCQs per unit**, in three batches, each going live after your approval. All three batches were written on 3 October: **batch 1** (the map, Units I–IV, 80 MCQs), **batch 2** (Units V–VII, 60 MCQs, most keys proved by script) and **batch 3** (Units VIII–X, 60 MCQs, dated facts tied to the notes). **All three approved on 3 October 2026** and live on the site; their questions are scored in the app | Live |
| APPSC ASO | **Paper-II 2025 and 2022 solved** (150 questions each), sat as timed exams under the papers' own recorded rules; the APPSC syllabus map (73 lines, Assistant Director and ASO) | Paper-II only; no general-studies Paper-I |
| Question bank | **950 questions**, checked keys, numeric answers recomputed by script; a history of every change | The review queue is closed: all 37 settled on 2 October |
| Accounts and progress | Sign-up with email confirmation, a dashboard, progress kept on the account, data export, account deletion | Built and tested |
| Unit tests | **20 units** have a test (all 10 UGC NET units among them); 70% to pass | 290 of 310 units still have none |
| Old papers | 450 questions, practice mode and timed exam mode, a review by section | Built and tested |
| Readiness | 501 syllabus lines from 5 exam maps; readiness from units passed; the next units to study | UGC NET can reach 50.8% today, APPSC 41.8% |
| Quality loop | Nightly item statistics, a review queue, the two-person rule | Waits for a second reviewer |
| Security and operations | HTTPS settings, a strict content policy, every id route owner-checked, lockout after 5 wrong passwords, admin 2-factor, backups and restore rehearsed, vulnerability checks in CI | Built and tested; **CI run #18 green**; **55 of 55** offline checks pass |
| Channels | Students you teach, Telegram and WhatsApp exam groups, YouTube and Instagram | Yours to use from this week |

**What we do not have yet:**
- a host, a domain, an email provider and a Google sign-in client;
- a second reviewer;
- a staging run;
- the legal review;
- any measure of the live site's traffic (no trackers, by design);
- a launch video and posts;
- testimonials;
- APPSC Paper-I.

---

## 3. Market research

### 3.1 The exams and the calendar

| Fact | Detail | Source | Confidence |
|---|---|---|---|
| Statistics is a new UGC NET subject | Code 107, first sat in the June 2026 cycle (reported 30 June 2026) | Testbook, Professor Academy | Reported; check at ugcnet.nta.nic.in |
| How the exam is set | Paper 1 (50 questions, 100 marks) and Paper 2 (100 questions, 200 marks) in one 3-hour sitting; no negative marking | Testbook | Reported; it matches the June 2026 paper the site has solved |
| December 2026 exam window | 14–19 December 2026, with 20–21 December as buffer days, from NTA's calendar notice of 16 September 2026; the notification expected early October | Adda247, Shiksha, PW | Reported; **confirm in week 1** |
| The scale of UGC NET | December 2025: 9,93,702 registered and 7,35,614 appeared, across 85 subjects; 5,108 qualified for JRF and 54,713 for Assistant Professor and PhD | PW, Careers360 | Reported; no Statistics-only figure exists yet |
| APPSC ASO 2026 | Brief Notification 20/2026 of 15 September 2026: 196 posts; apply online 13 October to 2 November 2026; one online (CBRT) examination; exam date not yet announced | Testbook, Karmasandhan | Reported; **confirm at psc.ap.gov.in** |
| India's data-protection rules | DPDP Rules notified 13 November 2025; consent managers from 13 November 2026; full compliance due 13 May 2027 | PIB (official), GlobalCert | Official for the notification; the dates as reported |

### 3.2 Who the learners are

- **UGC NET Statistics aspirants:**
  - postgraduates in statistics and related subjects, aiming for JRF or Assistant Professor;
  - many are working or studying;
  - they prepare on phones, in short sessions;
  - they want the real paper's level, worked solutions, and a clear "what is left";
  - in the last weeks they sit full papers.
- **APPSC ASO candidates:**
  - graduates with statistics, in Andhra Pradesh, preparing for a state post;
  - they want past Paper-II papers under exam conditions, with negative marking as the paper
    states;
  - much of their market's material is in Telugu. We stay English-only for now, and say so plainly.
- **Both groups gather in Telegram and WhatsApp groups and on YouTube.** They are wary of sites that
  ask for payment or sign-up before showing anything. Our free, no-login study pages answer that.

### 3.3 The competition

| Who | What they offer | Price (reported) | Where we differ |
|---|---|---|---|
| Testbook | UGC NET test series across subjects (1,300+ tests claimed); an APPSC ASO series in English and Telugu | About ₹699 a year on offer (₹1,799 list) | Theirs is broad across all subjects; ours is made for code 107, with every answer worked |
| Adda247 | UGC NET mock tests and courses; free mocks to start | Test series from about ₹849; courses from about ₹7,474 | We are free, with no adverts |
| Unacademy, PW | Live classes and tests | About ₹999–2,499 | We have no live classes; we offer self-paced checking and readiness |
| statchakravyuh, muphicafe | Sites made for UGC NET Statistics: guides, an index, notes | Not established | They are the closest rivals. Our edge: unit tests that score, timed solved papers, readiness by syllabus line, accounts |
| Toppersexam, Vijeta | APPSC ASO tests and books, Telugu medium | Not established | Our Paper-II papers are solved and timed |

**Our edge, in one line:** free and advert-free; every answer worked; keys checked by two people;
papers timed under their own rules; readiness by syllabus line.

**Pricing benchmark for later paid extras:** test series in this market sell at about **₹399–2,499**.

### 3.4 Channels

- **Personal reach:** students you teach or know. It is the fastest route to the first 30 beta
  learners and the first honest feedback.
- **Telegram and WhatsApp groups** are where exam news and PDFs travel. Post with the admin's
  agreement, at most once a week per group, and always with something useful in the post itself: a
  worked question, not just a link.
- **YouTube Shorts and Instagram Reels:** one question worked in under 60 seconds. With 150 solved
  June 2026 questions there are five months of daily posts already written.
- **Search:**
  - the site already has titles, descriptions, a sitemap and an A–Z index;
  - pages on solved papers and syllabus lines answer what aspirants type;
  - Google Search Console shows the queries without adding anything to the pages.

---

## 4. What success needs, by team

### 4.1 Product and content (owner)

1. **Done on 2 October: the 37 questions in the review queue are settled**, the 6 contested UGC NET
   keys among them. A doubtful key in exam week is the worst trust failure we can have; a key reported
   wrong from now on is flagged at once and settled the same week.
2. **Name the second reviewer:** a staff account, 2-factor, and the "Reviewers" group. You can approve
   the imported questions yourself, since the app records no author for them. A question you write
   needs someone else, since no one approves their own.
3. **Before launch:** proof-read the UGC NET unit pages and the June 2026 solutions once more (they
   are the shop window).
4. **Done on 3 October: UGC NET Paper I approved**, all three batches (the map, notes for Units
   I–X and 200 MCQs). It is live on the site, and its questions are scored in the app.
5. **After launch:**
   - APPSC Paper-I;
   - unit tests for the units the readiness map points to most.

   Each test needs 10 checked questions.

### 4.2 Technical (Claude, on request; owner decides)

1. **Host, domain, email and Google sign-in**, chosen by 9 October (§6).
2. **The release steps** in `nrstatlab-learn/docs/DEPLOY.md`:
   - `migrate`, both imports, `collectstatic`, `check --deploy`;
   - the nightly `item_stats`;
   - daily backups, with a restore test.
3. **Two small additions:**
   - a **"not yet indexed" switch** for the beta weeks (`noindex` until launch day);
   - error emails to the owner when a page fails.
4. **The lockout setting** for the host's proxy (`AXES_IPWARE_PROXY_COUNT`), so wrong passwords are
   counted per learner.
5. **Uptime monitoring** (a free external check of `/healthz`) and **Search Console** for the domain.
6. **The local copy:** rebuild the Docker image once (`docker compose up --build`), as allauth was
   upgraded for a security fix.

### 4.3 Marketing (owner, with posts drafted on request)

1. **From this week, a steady rhythm**, about 3 hours a week:
   - Monday: a Short or Reel, one June 2026 question worked;
   - Wednesday: one post per group, "this week's free unit test", with a worked question in the post;
   - Saturday: one syllabus line explained, linked to its unit page.
2. **The closed beta (weeks 5–6):** 20–30 learners you know, on the live domain, before it is
   indexed. Ask five of them for a 15-minute call. Ask permission before quoting anyone.
3. **The 30-day countdown (14 November to 13 December):** one question a day from the June 2026 paper,
   each ending "sit the whole paper, timed, free".
4. **Launch day (Saturday 28 November):**
   - a pinned post in every group;
   - a 5-minute screen recording: "Using NRSTATLAB Learn in the last 16 days before UGC NET";
   - the link from the live site.
5. **After the exam:** solve the December 2026 paper as soon as NTA's paper and key are public. Post
   each section as it is done.
6. **APPSC:** once the exam date is announced, run a "Paper-II, timed, with negative marking" campaign
   for the last four weeks before it.

### 4.4 Legal and operations

- **The legal review** of the privacy notice and the 18-and-over rule against the DPDP Act and Rules.
  The full obligations apply from May 2027; we keep to them from launch.
- **Support** through GitHub Issues, checked twice a week; a short reply within two days.
- **An incident routine:**
  - a wrong key: flag it in the admin at once; it then stops being scored;
  - a site failure: the host's restart, then a restore from backup if needed.

### 4.5 Money

- **Nothing is paid at launch.** Study pages stay free without login, with no adverts or trackers.
- **Review on 28 February 2027** with three months of figures. Candidate paid extras:
  - a timed full-mock series for June 2027, with new questions;
  - printable paper packs;
  - live doubt sessions.

  Price against the ₹399–2,499 market.
- **Taking payments** needs a payment gateway, terms and refund rules, and advice on tax and GST from a
  professional. It is a decision for then, not now.

### 4.6 Running it alone

**One person can run it at this size**, about 500 learners in the first three months, because most of
a team's work is already automatic:
- the managed host and database: servers, patches, daily backups;
- sign-up, password reset and account deletion;
- scoring, the exam timer and readiness;
- the nightly question statistics;
- the vulnerability check on every code change;
- an uptime check that emails you.

**The steady load after launch, about 6–8 hours a week:**

| Job | Hours a week |
|---|---|
| Read the uptime and error emails; note the Saturday figures | 0.5 |
| GitHub Issues, twice a week | 1 |
| The review queue | 1–2 |
| Marketing: Short, group posts, syllabus line | 3 |
| New questions (optional; a new unit test takes about 3–5 hours) | 0–2 |

Plus 1–2 hours a month for the restore test and any fix the vulnerability check asks for (Claude
makes it on request).

**The peaks:**
- launch week: 10–15 hours;
- the two weeks after each exam: 15–20 hours, solving the new paper;
- exam week: about 3 hours, with nothing new released.

**The four conditions:**
1. **A second reviewer, for the questions you write.** Approval is refused only to a question's
   author, and the 950 imported questions have none in the app. About 1–2 hours a month of someone's
   time.
2. **A stand-in for emergencies.** The site runs while you are away, but:
   - write a one-page note of what to do if the site is down or a key is reported wrong;
   - give one trusted person a staff account with 2-factor, so they can flag a question.
3. **Professionals for two one-off jobs:** the legal review now, and a tax adviser before anything is
   paid.
4. **Don't promise what needs a second person:**
   - live classes;
   - instant doubt answers;
   - 24-hour support;
   - a Telegram group of your own to moderate;
   - a Telugu version.

**Claude's part:** building, fixing, deploying and drafting, whenever you ask. Claude does not watch
the site or answer learners on its own.

**Signs it is time for help:**
- support takes more than 3 hours a week;
- the review queue falls more than two weeks behind;
- more than about 2,000 learners;
- or a decision for paid extras, live sessions or Telugu.

---

## 5. The plan, week by week

The owner's load is shown in hours per week. "Claude" means the technical work done on request.

| Week | Dates | Owner | Claude | Hours |
|---|---|---|---|---|
| 1 | 1–7 Oct | Walk `LOCAL-CHECK.md` and sign off; choose the budget option; confirm the UGC NET and APPSC dates at the official sites; start the Monday/Wednesday/Saturday posts to the live site | Draft the first four weeks of posts on request | 8 |
| 2 | 8–14 Oct | Buy the domain; open the host, database and email accounts; make the Google sign-in client | Set up staging; the release steps; the `noindex` switch; error emails | 6 |
| 3 | 15–21 Oct | Walk the checklist on staging; ask the second reviewer | Restore test on staging; uptime check; Search Console | 8 |
| 4 | 22–28 Oct | The legal review starts | Fix what staging found | 8 |
| 5 | 29 Oct – 4 Nov | Invite 20–30 beta learners; APPSC applications close on 2 November | Move staging to the live domain, still `noindex` | 6 |
| 6 | 5–11 Nov | Five feedback calls; legal review done; write the one-page emergency note | Fix what the beta found | 8 |
| 7 | 12–18 Nov | **Feature freeze** on 14 November; the 30-day countdown starts; record the launch video; give a stand-in a staff account with 2-factor | Only fixes from now on | 8 |
| 8 | 19–25 Nov | Schedule launch posts; **go / no-go on 25 November** | Launch-day checklist; a final backup and restore | 6 |
| Launch | 26 Nov – 2 Dec | **Saturday 28 November: launch**; the link from the live site; pinned posts | Watch errors and sign-ups; same-day fixes | 10 |
| Pre-exam | 3–13 Dec | Countdown posts; answer issues | Nightly statistics running; nothing new deployed | 6 |
| Exam | 14–19 Dec (reported) | Exam-week support only | Nothing deployed | 3 |
| After | 20 Dec – 31 Jan | Solve the December 2026 paper once NTA publishes it; the APPSC campaign once its date is known | Import the new paper; the stage D move once the app has run steadily | 8 |
| Review | 1–28 Feb | Three-month review on 28 February: the figures, the money question, what to build next | Prepare the figures | 4 |

**After launch, in waves:** the GATE Statistics and IIT JAM MS maps in December, then the
Statistics Foundations and Data Analyst learning paths from January. See `PATHS-AND-EXAMS-PLAN.md`.
Company tests, the first paid extra, follow from January 2027: see `COMPANY-TESTS-PLAN.md`.

---

## 6. Budget options

Prices were reported in August and September 2026, in US dollars at about ₹85–90 to the dollar.
**Check each before buying.**

| | Lean | Steady |
|---|---|---|
| App hosting | Render Starter (about $7 a month) or Railway; nearest region Singapore | DigitalOcean App Platform, Bangalore (from about $5–12 a month) |
| Database | Render PostgreSQL (from about $6 a month) | DigitalOcean managed PostgreSQL, Bangalore (from about $15 a month), with daily backups |
| Email | Brevo free, 300 emails a day | Brevo paid (from about $15 a month), or Amazon SES at about $0.10 per 1,000 |
| Domain | A `.in` domain, about ₹600–900 a year | The same |
| Promotion | Free channels only | Small boosted posts, about ₹1,000–1,500 a month, tried for four weeks then judged |
| **About a month** | **₹1,200–1,500** | **₹3,500–5,000** |
| Risk | Small memory: check the imports fit during staging; Singapore adds a little delay | Higher fixed cost before there are learners |

**Recommendation:** start **Lean** for staging and launch, and move up when sign-ups or memory need
it. The code runs the same on either (`docs/DEPLOY.md`).

---

## 7. How we measure success, without trackers

The app counts what learners do on the server, so no tracker is added to any page.
- Each Saturday, look in the admin, or run `python manage.py data_counts`.
- Note the week's figures in one row of a spreadsheet.

| Figure | Why it matters | Launch week | 31 Dec | 28 Feb 2027 |
|---|---|---|---|---|
| Signed-up learners (email confirmed) | **The main goal** | 100 | 300 | **500** |
| Learners who took a unit test or sat a paper | They used the reason they signed up | 60 | 180 | 300 |
| Learners who set a readiness target | They plan with us | 30 | 90 | 150 |
| Learners active in two different weeks | They came back | 30 | 120 | 200 |
| Wrong keys reported and fixed within 7 days | Trust | All | All | All |
| Search clicks a week (Search Console) | Free growth | Baseline | +50% | +100% |

**If a figure is behind by the end of December,** change one channel at a time. For example, double
the Shorts, or ask two more group admins. Judge it after two weeks.

---

## 8. Risks

| Risk | Likelihood | Impact | What we do |
|---|---|---|---|
| One part-time person runs out of hours | High | High | A fixed weekly rhythm; posts drafted in batches; a feature freeze from 14 November |
| No second reviewer by launch | Medium | Medium | Ask now. Launch still works, and you can clear the imported queue yourself; only questions you write wait |
| A doubtful key in exam week | Low | High | The queue is settled (2 October); a key reported wrong is flagged at once and settled the same week |
| The exam dates move | Medium | Medium | Confirm in week 1; the plan's anchor is our launch date, not the exam |
| Sign-up emails land in spam | Medium | High | SPF and DKIM on the domain; test with Gmail and Outlook during staging |
| Hosting too small or too dear | Low | Medium | Lean first; staging shows the memory needed; Steady is ready |
| A group sees the posts as spam | Medium | Medium | The admin's agreement first; once a week at most; useful content in the post |
| The privacy rules | Low | High | The legal review before launch; minimum data; export and delete already built |

---

## 9. Decisions needed from you

| # | Decision | By |
|---|---|---|
| 1 | Sign off `LOCAL-CHECK.md` (55 checks) | 7 October |
| 2 | Lean or Steady | 7 October |
| 3 | Confirm the UGC NET December and APPSC ASO dates at the official sites | 7 October |
| 4 | The domain name, the host, the email provider | 9 October |
| 5 | Who the second reviewer is | 21 October |
| 6 | UGC NET Paper I: approve batches 1, 2 and 3 (done 3 October) | ~~17 October, 27 October, 6 November~~ done |
| 7 | The 37 questions in the review queue (done 2 October) | ~~28 October~~ done |
| 8 | The legal review signed | 11 November |
| 9 | Go / no-go | 25 November |
| 10 | Paid extras: yes or no, and which | 28 February 2027 |

---

## 10. Sources

Official:
- NTA: https://nta.ac.in/ and https://ugcnet.nta.nic.in/ (to confirm the December 2026 dates)
- APPSC: https://psc.ap.gov.in/ (to confirm Notification 20/2026)
- DPDP Rules, 2025 (Press Information Bureau): https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014

Secondary (reported):
- UGC NET December 2026 dates: https://www.adda247.com/teaching-jobs-exam/ugc-net-exam-date-2026/,
  https://www.shiksha.com/news/sarkari-exams-ugc-net-december-2026-registration-when-will-nta-release-application-form-blogId-242325,
  https://www.pw.live/news/ugc-net-december-2026-application-form-date-registration-exam-schedule
- Statistics as a new subject, and the exam's shape: https://testbook.com/news/ugc-net-subjects-list-2026-out/,
  https://testbook.com/news/ugc-net-statistics-2026-qualification-and-syllabus-exam-pattern/,
  https://professoracademy.com/new-subject-in-ugc-net-2026-statistics/
- UGC NET December 2025 figures: https://www.pw.live/ugc-net/exams/ugc-net-december-2025-results-exam-statistics,
  https://news.careers360.com/nta-ugc-net-december-2025-exam-7-35-lakh-attendance-results-answer-key-cut-off-jrf-assistant-professor-subjects
- APPSC ASO 2026: https://testbook.com/appsc-aso, https://www.karmasandhan.com/appsc-aso-recruitment-2026/
- Competitors and prices: https://testbook.com/ugc-net-test-series-coaching, https://www.adda247.com/ugc-net/mock-test,
  https://statchakravyuh.com/ugc-net/statistics/, https://muphicafe.in/UGCNET/,
  https://toppersexam.com/STATE-LEVEL-EXAMS/APPSC-ASO/exam-info_3482.html,
  https://vijetacompetitions.net/product-category/andhra-pradesh/appsc/appsc-aso/
- Hosting and email prices: https://selfhost.dev/blog/managed-postgresql-comparison-2026/,
  https://www.buildmvpfast.com/api-costs/email
- DPDP timeline: https://www.glocertinternational.com/resources/guides/dpdp-rules-2025-compliance-timeline/

Our own figures: `Webapp/PROJECT-STATUS.md`, and in `nrstatlab-learn`, `docs/PHASE-3-REPORT.md` to
`docs/PHASE-7-OFFLINE-REPORT.md`.
