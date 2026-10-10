# StatsTricks360: the launch plan (the website now, the app when income covers it)

**Updated 10 October 2026** (first written 1 October; website first from 10 October). By StatsTricks360. Questions and corrections: GitHub Issues.

Written from three seats at once: the owner as CEO, the technical lead, and the marketing lead. It
covers what we have, what the market looks like, what success needs, and the work week by week to
28 November and through the first three months.

**The owner's choices behind it:**
- a free core, with paid extras considered later;
- UGC NET Statistics first, then APPSC Assistant Statistical Officer (ASO);
- one person, part time, with Claude doing the technical build on request;
- English only;
- success means **500 or more signed-up learners by 28 February 2027**;
- **the budget: Lean, up to ₹1,500 a month** (chosen 9 October; §6);
- **the name: StatsTricks360** (renamed from NRSTATLAB, 10 October), on YouTube and Instagram too;
- **the domain: statstricks360.com**, to be bought (chosen 10 October; it replaces nrstatlab.in);
- **the website first, the app later** (chosen 10 October; §0): the study site moves to the domain now,
  and the app goes live only **when income covers its running cost**;
- **AdSense from January 2027**, once traffic has built up (chosen 10 October);
- **paying for it: YouTube (Shorts and long videos), Instagram Reels, and AdSense on the study pages**
  (chosen 9 October; §6A).

**About the facts here.** The official sites (NTA, APPSC) could not be opened from the research
environment. Every exam date below comes from secondary sources and is marked so. Each is on the
owner's list to confirm at the official source in week 1. Nothing goes on the site itself without a
named official source; that rule stands.

---

## 0. Website first, the app later (chosen 10 October 2026)

**Why this order.** The study site (689 pages) is already built and live. On GitHub Pages it costs
nothing to host, and it can serve its own domain with free HTTPS. The app costs about ₹1,200–1,300 a
month from the day it goes live (§6). So the site goes on **statstricks360.com** now, the channels
send people to it, and the adverts on it (from January 2027) plus YouTube pay for the app. The app
serves **the same page addresses** as the site, so switching the domain to the app later is a DNS
change: links, bookmarks and search rankings carry over.

**The stages:**

| Stage | When | What | Cost |
|---|---|---|---|
| A. The new name | Done 10 October | NRSTATLAB becomes StatsTricks360 on every page, the share card and the app. Learners' saved progress is untouched (its browser key keeps the old name) | ₹0 |
| B. The domain | As soon as it is bought (target 15 October) | statstricks360.com points at the site; HTTPS on; the old github.io addresses checked to redirect; Google Search Console and the sitemap | the domain only |
| C. YouTube and Instagram | From week 1 | @statstricks360 on both; daily Shorts/Reels, two long videos a week (§6A); every video links to its page on statstricks360.com | ₹0 (a microphone if needed) |
| D. Adverts | January 2027, once page views are steady | Privacy page rewritten for cookies; Google's consent message for EEA/UK visitors; `ads.txt`; one or two ad units on study pages only (§6A rule); apply for AdSense | ₹0 |
| E. The app | When income reaches about ₹1,300 a month for two months running; decide by **31 March 2027** at the latest, so it is live before the June 2027 UGC NET | Staging on `staging.statstricks360.com`, the checks of §5, then the domain is pointed at the app | ~₹1,200–1,300 a month (§6) |

**Hosting the website.** GitHub Pages (free): the site is about 267 MB against a 1 GB limit, with a
soft 100 GB a month of bandwidth, enough for well over 100,000 page views a month. Its terms rule out
sites run *mainly* for commercial transactions or software-as-a-service; a free study site carrying
adverts is not that, but if Pages ever objects, **Cloudflare Pages** (free: up to 20,000 files,
unmetered requests) serves the same files with a DNS change.

**What it costs until the app goes live:** the domain only, about **₹900–1,300 a year** for a `.com`
(about ₹100 a month; compare the renewal price, not only the first year).

**The owner's steps for stage B** (Claude does the rest the same day):
1. Check statstricks360.com is free, and buy it (any registrar; Cloudflare Registrar sells at cost).
2. Put its DNS on Cloudflare (free plan), with these records set to **DNS only** (grey cloud):
   - four `A` records for `statstricks360.com`: `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153` (GitHub Pages);
   - a `CNAME` record `www` → `nrstatlab.github.io`.
3. Tell Claude. Claude then commits the `CNAME` file and the new address in the site's generators
   (canonical links, sitemap, share tags), rebuilds, and checks every page.
4. In the GitHub repository: Settings → Pages → Custom domain: `statstricks360.com`; when the
   certificate is ready, tick **Enforce HTTPS**.
5. Add the domain to Google Search Console (a DNS `TXT` record) and submit `sitemap.xml`.

**The app's plan below (§4–§9) still holds**, with its dates moved: the weeks of §5 start when stage
E is triggered, not in October. The website weeks are:

| Week | Dates | Owner | Claude |
|---|---|---|---|
| 1 | 10–15 Oct | Buy statstricks360.com and set the DNS; open @statstricks360 on YouTube and Instagram; first Shorts | Stage B the same day; the first four weeks of Shorts scripts |
| 2–3 | 16–29 Oct | Two long videos a week; daily Shorts; confirm the exam dates | Search Console checks; "Watch this solved" links on pages that have a video |
| 4–9 | 30 Oct – 13 Dec | The December 2026 UGC NET countdown on the channels | Content as it comes; site fixes |
| 10+ | From 20 Dec | Solve the December 2026 paper as a video series | Import the paper; stage D in January 2027 |

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
1. **Promote the free site now**, on statstricks360.com (§0). Weekly posts can point at it from
   today. The app is linked only after your sign-off.
2. **Launch the app when income covers it** (§0, stage E; it was planned for 28 November) as a soft
   launch, the cut-over plan's stage C: the live site stays as it is, and gains a "Sign in to save
   your progress" link.
3. **Solve the December 2026 paper quickly** once NTA publishes the paper and its key. That would be
   the second solved code-107 paper anywhere. It is the strongest reason for a learner to search for
   us, share us and come back for June 2027.

**What could stop us:**
- **one part-time person:** the plan keeps the weekly load to about 7–10 hours, the videos of §6A
  included;
- **no second reviewer yet:** a question you write cannot be approved until someone else is named
  (you settled the 37 questions in the queue yourself on 2 October);
- **the open technical choices** slipped past the 9 October date: the domain, the host and email
  accounts must be opened **by 15 October** to leave time for staging;
- **the running cost before there is income:** about ₹1,300 a month (§6) once the app is live;
  until then only the domain (§0). The app waits for the channels in §6A to cover it.

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
- a YouTube channel and an Instagram professional account in the StatsTricks360 name;
- an AdSense account (it needs the own domain first);
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

1. **Host, domain, email and Google sign-in**: Render (Lean), statstricks360.com, Brevo and Cloudflare,
   with the accounts opened by 15 October (§6).
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
   - **From 9 October, with the channels of §6A:** a Short/Reel every day (batch-recorded once a week)
     and **two long videos a week** (a solved-paper set or a unit walkthrough), about 3 more hours a
     week. Claude drafts the scripts and slides from the existing pages on request.
2. **The closed beta (weeks 5–6):** 20–30 learners you know, on the live domain, before it is
   indexed. Ask five of them for a 15-minute call. Ask permission before quoting anyone.
3. **The 30-day countdown (14 November to 13 December):** one question a day from the June 2026 paper,
   each ending "sit the whole paper, timed, free".
4. **Launch day (Saturday 28 November):**
   - a pinned post in every group;
   - a 5-minute screen recording: "Using StatsTricks360 Learn in the last 16 days before UGC NET";
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

- **Nothing is paid by learners at launch.** Study pages stay free without login.
- **Adverts (decided 9 October), from 2027:** AdSense on the public study pages only, to cover the
  running cost (§6A). Never on unit tests, papers in exam mode, results, the dashboard or account
  pages; one or two clearly labelled units a page; none inside a worked solution. Until then: no
  adverts and no trackers.
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

**The steady load after launch, about 9–11 hours a week** (the videos of §6A included):

| Job | Hours a week |
|---|---|
| Read the uptime and error emails; note the Saturday figures | 0.5 |
| GitHub Issues, twice a week | 1 |
| The review queue | 1–2 |
| Marketing: group posts, syllabus line | 2 |
| Videos: seven Shorts batch-recorded, two long videos (§6A) | 4 |
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

> **10 October:** these are the app's weeks, written for a 28 November launch. With the website
> first (§0), they now run from the week stage E is triggered; the dates show the length of each
> step, not the calendar. The website weeks are in §0.

The owner's load is shown in hours per week. "Claude" means the technical work done on request.

| Week | Dates | Owner | Claude | Hours |
|---|---|---|---|---|
| 1 | 9–15 Oct | Walk `LOCAL-CHECK.md` and sign off; **buy statstricks360.com**; open the Render, Brevo and Cloudflare accounts; make the Google sign-in client; confirm the UGC NET and APPSC dates at the official sites; **open the YouTube channel and the Instagram professional account** (same name); first Shorts | Draft the first four weeks of Shorts scripts and two long-video scripts from the June 2026 paper | 10 |
| 2 | 16–22 Oct | Walk the checklist on staging; ask the second reviewer; two long videos a week from now | Staging on `staging.statstricks360.com` (password, `noindex`); the release steps; the `noindex` switch; error emails; Cloudflare in front; the lockout's proxy setting; memory check of the imports on 512 MB | 9 |
| 3 | 23–29 Oct | The legal review starts, adverts included | Restore test on staging; uptime check; Search Console | 9 |
| 4 | 30 Oct – 5 Nov | Invite 20–30 beta learners; APPSC applications close on 2 November | Fix what staging found; move staging to the live domain, still `noindex` | 9 |
| 5 | 6–11 Nov | Five feedback calls; write the one-page emergency note | Fix what the beta found | 9 |
| 6 | 12–18 Nov | **Feature freeze** on 14 November; the 30-day countdown starts; legal review done; record the launch video; give a stand-in a staff account with 2-factor | Only fixes from now on | 9 |
| 7 | 19–25 Nov | Schedule launch posts; **go / no-go on 25 November** | Launch-day checklist; a final backup and restore | 7 |
| Launch | 26 Nov – 2 Dec | **Saturday 28 November: launch**; the link from the live site; pinned posts | Watch errors and sign-ups; same-day fixes | 10 |
| Pre-exam | 3–13 Dec | Countdown posts; answer issues | Nightly statistics running; nothing new deployed | 6 |
| Exam | 14–19 Dec (reported) | Exam-week support only | Nothing deployed | 3 |
| After | 20 Dec – 31 Jan | Solve the December 2026 paper once NTA publishes it, as a video series too; the APPSC campaign once its date is known | Import the new paper; the stage D move once the app has run steadily; then the AdSense build (§6A) and the application | 9 |
| Review | 1–28 Feb | Three-month review on 28 February: the figures, the money question, what to build next | Prepare the figures | 4 |

**After launch, in waves:** the GATE Statistics and IIT JAM MS maps in December, then the
Statistics Foundations and Data Analyst learning paths from January. See `PATHS-AND-EXAMS-PLAN.md`.
Company tests, the first paid extra, follow from January 2027: see `COMPANY-TESTS-PLAN.md`.

---

## 6. What it costs (chosen 9 October: Lean, up to ₹1,500 a month)

> **10 October:** until the app goes live (§0, stage E), the cost is the domain only, about
> ₹100 a month. The figures below are the app's, from the month it goes live.

Prices as published or reported in **October 2026**, in US dollars at about ₹88 to the dollar,
before GST. Several come from secondary sources (§10). **Check each on the provider's own page
before buying.**

**One-time:**
- the domain **statstricks360.com**: about ₹900–1,300 for the first year (offers vary widely; compare the
  renewal price, not only the first year);
- if the phone's microphone is poor, a clip-on microphone: about ₹1,500–2,500.

Nothing else is one-time: the application is already built and tested.

**Every month, Lean:**

| Item | Choice | $ a month | ₹ a month |
|---|---|---|---|
| The app | Render **Starter** web service (512 MB, 0.5 CPU), Singapore region | 7 | ~620 |
| The database | Render PostgreSQL **Basic-256mb**, with backups | 6 | ~530 |
| The workspace | Render **Hobby** workspace: free, with 5 GB of bandwidth a month, then $0.15 a GB (new plans from 1 August 2026) | 0 | 0 |
| CDN and DNS | **Cloudflare free**, in front of the app: it caches pages, images and MathJax, so the app's own bandwidth stays near the 5 GB allowance | 0 | 0 |
| Sending email | **Brevo free**: 300 emails a day (sign-up, password reset, reviewers); SPF, DKIM and DMARC on the domain | 0 | 0 |
| Receiving email | Cloudflare Email Routing to the owner's Gmail | 0 | 0 |
| The domain | statstricks360.com, spread over 12 months | — | ~100 |
| Uptime check, Search Console | free tiers | 0 | 0 |
| **Total** | | **about 13** | **about ₹1,200–1,300** |

- **First three months:** about ₹4,500, the domain included.
- **The one risk to the budget is memory.** Django takes about 100 MB per gunicorn worker, and 512 MB is
  tight. Run 2 workers with threads, and measure the imports' peak during staging (week 2).
  - If it fits: stay on Lean.
  - If not, Render's next size is Standard (2 GB, $25): about ₹2,700 a month, over the cap.
  - **The fallback inside the cap:** one 1 GB server (a DigitalOcean droplet in Bangalore, $6, about
    ₹530) running the app and PostgreSQL together, with nightly `pg_dump` copies kept off the server.
    It is cheaper, but the server's updates become ours (Claude does them on request).
- **Steady, only when sign-ups or memory need it:** about ₹3,500–5,000 a month (a bigger database
  with longer backups, paid email). The code runs the same on any of these (`docs/DEPLOY.md`).
- **No paid promotion** until income covers the running cost (§6A).

---

## 6A. Paying for it: YouTube, Instagram and AdSense (chosen 9 October)

**The target:** income of **₹1,500 a month**, the running cost with a margin.

**Planning rates.** These are estimates from 2026 secondary sources; the real figures come from
YouTube Studio and the AdSense reports once each is running.

| Route | Rate (estimate) | To earn ₹1,500 a month | When it can start |
|---|---|---|---|
| **AdSense on the study pages** | about ₹165–415 per 1,000 page views (education, India) | about **3,600–9,100 page views** a month | After stage D, when the study pages are served from statstricks360.com (an own domain is needed; github.io cannot carry AdSense). Approval needs original content, a privacy policy that covers cookies, and the owner aged 18+. Some sources say Indian sites need about 6 months' age: unconfirmed, check when applying |
| **YouTube adverts** | about ₹80–200 per 1,000 monetised views (education, India) | about **7,500–19,000 views** a month | After the YouTube Partner Program: **1,000 subscribers and 4,000 public watch hours in 12 months, or 10 million Shorts views in 90 days**. Reported: rising to 8,000 hours or 20 million Shorts views on **1 February 2027**, with channels already in the programme kept in. **Aim to qualify before then** |
| YouTube fan funding | Super Thanks, memberships | small | The lower tier: 500 subscribers, 3 uploads in 90 days, and 3,000 watch hours or 3 million Shorts views |
| **Instagram** | Gifts (low bar, small); Subscriptions (about 10,000 followers); brand deals (about 1,000 engaged followers) | not counted on | For **reach**: every Reel points to the YouTube video and the free page |

**What the numbers say:**
- **AdSense is the quickest route to the target:** a few thousand page views a month. It waits only for
  the domain move (January 2027) and approval.
- **YouTube is larger but slower:** it pays only after the Partner Program, which takes months. The
  watch hours come from long videos, not Shorts.
- **Instagram brings people,** not money, at our size.

### What we post, from content we already have

No new writing is needed for a year:

- **Shorts and Reels, one a day (about 60 seconds):** one question worked.
  - the **150 June 2026 UGC NET questions** (Paper I and II);
  - the **300 APPSC Paper-II questions** (2025 and 2022);
  - the **worked problems added this month** (curve fitting, theory of attributes, the χ², t and F
    proofs, sampling, ANOVA, time series).

  That is more than 450 items, over a year of daily posts. Batch-record seven at once each week.
- **Long videos, two a week (15–30 minutes): the watch-hours engine.**
  - "UGC NET June 2026 Paper II, questions 1–10 solved", and so on through the paper;
  - one unit walkthrough a week, from the unit pages (e.g. "Curve fitting in 20 minutes");
  - once a month, a full paper solved live, timed.

  4,000 watch hours is about 8,000 views of a 30-minute video, or 16,000 of a 15-minute one.
- **Every video links back:**
  - the free page or unit test on statstricks360.com, in the description and a pinned comment;
  - once a video exists, its page gets a "Watch this solved" link.
- **Who does what:**
  - Claude, on request: scripts and on-screen slides from the existing pages and figures, titles,
    descriptions and tags, a week's batch at a time;
  - the owner: records the voice and uploads.

  About **3 more hours a week** than before.

### The rule for adverts on the site

It replaces "no adverts or trackers"; the privacy notice and the legal review change with it.
- **Adverts on the public study pages only.** Never on unit tests, papers in exam mode, results, the
  dashboard or account pages.
- **One or two units a page, labelled "Advertisement".** None inside a worked solution or between a
  question and its answer.
- **Privacy:**
  - the privacy notice is rewritten to cover cookies and Google's adverts;
  - a consent banner for visitors from the EEA, UK and Switzerland (Google requires a certified
    consent platform there);
  - the legal review (week 3) covers it under the DPDP Act.
- **Built after launch, in January 2027 (Claude), then apply:**
  - the content policy (`apps/core/csp.py`) allows the AdSense script on study pages only, tried in
    report-only mode first;
  - `/ads.txt`;
  - one template slot for an advert unit.

### The money guard-rail

- **28 February 2027:** if income does not yet cover the monthly cost:
  - stay on Lean;
  - spend nothing on promotion;
  - keep the free channels going.
- **The next lever** is still a paid extra (a mock series, priced in the ₹399–2,499 market; §4.5).
- **Before any money comes in:** ask a tax adviser about declaring YouTube and AdSense income and about
  GST.

---

## 7. How we measure success, without trackers of our own

The app counts what learners do on the server, so we add no tracker to any page. (Once AdSense runs
on the study pages, Google's own cookies come with its adverts, under the rule in §6A.)
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
| YouTube subscribers | The Partner Program needs 1,000 | 100 | 300 | **1,000** |
| YouTube public watch hours (last 12 months) | The Partner Program needs 4,000 | 200 | 1,000 | **4,000** |
| Instagram followers | Reach | 100 | 300 | 1,000 |
| Site page views a month | AdSense needs a few thousand to cover the cost | Baseline | 5,000 | 10,000 |
| Income against the ₹1,500 monthly cost | Paying for itself | — | — | 50% or more |

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
| Hosting too small or too dear | Medium | Medium | Lean first; 2 workers with threads; staging measures the memory; the 1 GB server fallback stays inside the cap (§6) |
| Bandwidth over Render's 5 GB | Medium | Low | Cloudflare caches pages, images and MathJax; overage is $0.15 a GB |
| YouTube's thresholds rise on 1 February 2027 (reported) | Medium | Medium | Two long videos a week from October; check the Partner Program page each month |
| AdSense refuses the site, or pays less than planned | Medium | Medium | Apply only after stage D with the privacy notice updated; YouTube and paid extras remain |
| Adverts cost trust | Low | Medium | The §6A rule: study pages only, labelled, never in tests or solutions |
| GitHub Pages objects to adverts on the site | Low | Medium | Move the same files to Cloudflare Pages (free) with a DNS change (§0) |
| Income stays below the app's cost | Medium | Low | The site and channels run at about ₹100 a month; the app waits (§0, stage E) |
| A group sees the posts as spam | Medium | Medium | The admin's agreement first; once a week at most; useful content in the post |
| The privacy rules | Low | High | The legal review before launch; minimum data; export and delete already built |

---

## 9. Decisions needed from you

| # | Decision | By |
|---|---|---|
| 1 | Sign off `LOCAL-CHECK.md` (55 checks) | **15 October** |
| 2 | Lean or Steady | ~~7 October~~ done 9 October: **Lean**, up to ₹1,500 a month |
| 3 | Confirm the UGC NET December and APPSC ASO dates at the official sites | 15 October |
| 4 | The domain name, the host, the email provider | Domain changed 10 October to **statstricks360.com: buy it and set the DNS by 15 October** (§0). Render, Brevo: open the accounts at stage E |
| 4A | The name StatsTricks360 on the site, the app, YouTube and Instagram | ~~open~~ done 10 October |
| 4B | Website first; the app when income covers it | ~~open~~ done 10 October (§0); the app decision by **31 March 2027** at the latest |
| 5 | Who the second reviewer is | 29 October |
| 6 | UGC NET Paper I: approve batches 1, 2 and 3 (done 3 October) | ~~17 October, 27 October, 6 November~~ done |
| 7 | The 37 questions in the review queue (done 2 October) | ~~28 October~~ done |
| 8 | The legal review signed, adverts included | 18 November |
| 9 | Go / no-go | 25 November |
| 9A | Paying for it: YouTube, Instagram, AdSense on the study pages | ~~open~~ done 9 October (§6A) |
| 9B | Apply for AdSense | January 2027 (§0, stage D) |
| 10 | Paid extras: yes or no, and which | 28 February 2027 |

---

## 10. Sources

Official:
- NTA: https://nta.ac.in/ and https://ugcnet.nta.nic.in/ (to confirm the December 2026 dates)
- APPSC: https://psc.ap.gov.in/ (to confirm Notification 20/2026)
- DPDP Rules, 2025 (Press Information Bureau): https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014

Website first (§0), added 10 October 2026 (official):
  - GitHub Pages limits and terms: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
  - GitHub Pages custom domain (apex `A` records, `www` CNAME, Enforce HTTPS):
    https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
  - Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/

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
- Updated 9 October 2026 (§6, §6A):
  - Render: https://render.com/pricing, https://render.com/docs/new-workspace-plans,
    https://render.com/changelog/updated-plans-for-render-workspaces (official);
    https://makerkit.dev/pricing-calculator/render, https://costbench.com/software/developer-tools/render/
  - Memory of Django workers: https://www.djangotricks.com/blog/2026/06/understanding-memory-usage-in-django-webserver-workers/,
    https://community.render.com/t/optimizing-gunicorn/2068
  - DigitalOcean droplet: https://costbench.com/software/cloud-infrastructure/digitalocean,
    https://www.digitalocean.com/company/blog/introducing-our-bangalore-region-blr1/
  - `.in` domain prices: https://domainoffer.net/tld/in
  - Brevo free plan: https://www.brevo.com/free-smtp-server (official)
  - Cloudflare Email Routing and free mail: https://geekflare.com/free-email-hosting-on-custom-domain/
  - YouTube Partner Program: https://support.google.com/youtube/answer/13429240 (official),
    https://vidiq.com/blog/post/monetize-youtube-guide/, https://www.tubefilter.com/?p=193559,
    https://upgrowth.in/how-to-get-youtube-monetization-approved-india-2026/
  - YouTube rates in India: https://ytgrowth.io/youtube-earnings/education/india,
    https://upgrowth.in/youtube-cpm-india-guide-2026/
  - AdSense rates and rules: https://upgrowth.in/how-to-calculate-google-adsense-earnings-india/,
    https://support.google.com/adsense/answer/7670013 (official),
    https://www.adpushup.com/blog/?p=4664
  - Instagram in India: https://bosswallah.com/blog/creator-hub/instagram-monetization-requirements-for-reels-ads-bonuses/,
    https://influencermarketinghub.com/instagram-subscriptions-gifts/
- DPDP timeline: https://www.glocertinternational.com/resources/guides/dpdp-rules-2025-compliance-timeline/

Our own figures: `Webapp/PROJECT-STATUS.md`, and in `nrstatlab-learn`, `docs/PHASE-3-REPORT.md` to
`docs/PHASE-7-OFFLINE-REPORT.md`.
