# NRSTATLAB Learn: learning paths and exams worldwide

**2 October 2026.** By NRSTATLAB. Questions and corrections: GitHub Issues.

A CEO plan for two questions from the owner.
1. Should the platform also serve people learning statistics, data analysis or data science for
   their own sake, testing themselves whenever they need, not only exam candidates?
2. Which statistics exams around the world fit our scope?

**The owner's choices behind it:**
- after the 28 November launch, in waves;
- two paths first: Statistics Foundations, then Data Analyst;
- Claude drafts the new questions, and the owner approves them in the review queue;
- a finished path earns a "path complete" badge on the dashboard, with no certificate and no
  accreditation claim.

**About the facts here.** Each exam fact names its source and says whether it is official or
reported. Nothing goes on the site without an official source, and no page will call itself
preparation for a certification.

---

## 1. Summary, as CEO

**Yes, after launch.** Exam candidates come in seasons; people learning a subject come all year.
Paths give a learner a reason to return between exams, and they reach people who will never sit
UGC NET.

**The cost is questions, not code.** A path has the same shape as an exam's syllabus map: lines of
skills, each linked to the units that teach it. The app already turns that into "how far along you
are", and already gives every unit a test once it has ten checked questions.
- The **pages** for both paths exist today.
- The **questions** don't, yet: 169 for Statistics Foundations and 140 for Data Analyst.

**The order:**
1. **The GATE Statistics and IIT JAM Mathematical Statistics maps, in December.** Both exams are in
   mid-February 2027, and our MSc pages already teach most of their syllabus.
2. **The Statistics Foundations path, from January.**
3. **The Data Analyst path, from March.**

One wave at a time, so the launch and its exam season come first.

---

## 2. What we have

| Area | On the site today | For a path |
|---|---|---|
| Statistics | 36 courses with 153 unit pages, BSc and MSc, worked examples | Statistics Foundations draws 24 units from 7 courses |
| Data Science | 19 courses with units, 5 units each: Excel, databases and SQL, Power BI and Tableau, R, Python for data analysis, statistical foundations, time series, machine learning | Data Analyst draws 15 units from 5 courses |
| Unit tests | 20 units have one, 10 questions from a checked pool, 70% to pass | 4 of the 24 Foundations units; none of the 15 Data Analyst units |
| Readiness | Turns a syllabus map into "how ready you are" from the units passed, with the most reachable today | Works for a path unchanged |
| Review queue | Draft and flagged questions, approve or send back, a history of every change | The route by which new questions enter |

The 266 Data Science "practice questions" are lab tasks with datasets: open work, not keyed
questions. So neither path can reuse them as test questions.

---

## 3. The two paths

### Statistics Foundations: 24 units

| Skill area | Units |
|---|---|
| Describing data | Descriptive Statistics Units 1–5: description of data, scales and presentation, central tendency, dispersion, moments, skewness and kurtosis |
| Probability | Theory of Probability Units 1, 2, 4, 5: elementary probability, random variables, expectation, generating functions with the LLN and CLT |
| Distributions | Discrete Units 1–2 (binomial, Poisson); Continuous Units 2, 4, 5 (exponential, normal, sampling distributions) |
| Relationships | Statistical Methods Units 2 and 4: correlation, regression |
| Inference | Inferential Statistics Units 1–5: estimation, testing, large-sample, small-sample and non-parametric tests |
| Sampling | Sampling Techniques Units 1–3: survey concepts, simple random and stratified sampling |

**Questions:**
- 4 units are tested today: Descriptive Statistics 2–4 and Statistical Methods 2.
- 4 more are partly there: Descriptive Statistics 1 (9), 5 (8), Probability 1 (6), Sampling 1 (4).
- **169 more questions** bring every unit to ten.

### Data Analyst: 15 units

| Skill area | Units |
|---|---|
| Spreadsheets | Computer Fundamentals Units 4–5: spreadsheet basics, data analysis and visualisation |
| Databases and SQL | DBMS Units 3–4: the relational model and normalisation, SQL |
| BI tools | Business Intelligence Units 2–5: Power BI, Tableau, data modelling, dashboards |
| Python | Python for Data Analysis Units 2, 3, 5: pandas, input and cleaning, wrangling and visualisation |
| Statistics for analysis | Statistical Foundations Units 1, 3, 4, 5: probability, distributions, correlation and regression, inference |

**Questions:** none of the 15 units has a test yet (Computer Fundamentals 4 has 9 questions). **140
questions** are needed.

### What the learner sees

1. **Pick a path** on the dashboard, beside or instead of an exam.
2. **See how far along you are,** skill by skill. Each line shows its units, which are studied,
   passed or not started, and which have a test.
3. **Test yourself any time:**
   - any unit test, as often as you like (unseen questions first);
   - a **path check**: 30 questions drawn across the units you have studied, scored like a unit test,
     for a mixed revision whenever you want one.
4. **Finish:** when every unit on the path is passed, the dashboard shows **Path complete** with the
   date. It is a record of what you did here, not a certificate.

### What it takes in the app

Small, because the parts exist:
- a `kind` on `Exam` (exam or path), so paths sit beside exams in the menus and on the dashboard: one
  migration;
- the path maps, written in the content repository the way the exam maps are, and read by the same
  syllabus importer;
- the path check: a mixed draw over a path's units, reusing the unit-test engine;
- the badge: a line on the dashboard and in the data export.

---

## 4. How the questions get written

| Step | Who | What |
|---|---|---|
| Draft | Claude | Each question is written against its unit page: a stem, four options, the key and a worked answer. Numeric keys get a recompute log, as the imported banks have |
| Import | Claude | Into the bank as **drafts**, so none is drawn until approved |
| Review | You | In the review queue, approve or send back with a note. You can approve these, since the app records no author for them |
| Watch | The app | After 30 answers, the nightly statistics flag a question that behaves badly (p or r_pb out of range) |

**Pace:** about 30 questions drafted a week, and 2–3 hours of review for you.
- Foundations: about six weeks.
- Data Analyst: about five.

That fits inside the 6–8 hours a week of running the platform alone (`LAUNCH-PLAN.md` §4.6) only if
nothing else is being built at the same time. Hence one wave at a time.

---

## 5. The waves

| Wave | When | What | Your part |
|---|---|---|---|
| 0 | 28 November | Launch, as planned | The launch plan |
| 1 | 1–20 December | Syllabus maps for **GATE Statistics (ST)** and **IIT JAM Mathematical Statistics (MS)**, from their official syllabus PDFs; readiness for both, since our MSc units teach most lines | Download the two official syllabus PDFs if the sites stay blocked here; confirm the dates |
| 2 | January – mid February 2027 | **Statistics Foundations:** the path map, the path check, the badge, and 169 questions drafted and reviewed | Review about 30 questions a week; settle the badge wording |
| 3 | March – April 2027 (April – May if the company tests go ahead) | **Data Analyst:** 140 questions, then the path | Review about 30 a week |
| 4 | From May 2027, after the three-month review | More maps: SSC CGL Junior Statistical Officer, ISI MStat; topic maps for the international exams in §6 | Choose which, from the figures |

**Company tests** (a company tests its employees on chosen units) are planned beside the waves:
built January – February 2027, a pilot in March, paid from April. Their private questions add review
in February and March, so Wave 3 would move to April – May. See `COMPANY-TESTS-PLAN.md`.

**A path goes live before every test exists**, as the exam maps already do: readiness shows the most
that can be reached today, and each unit's test opens the day it has ten approved questions.

---

## 6. Statistics exams worldwide, and how they fit

**Fit:**
- **A:** our pages teach most of it, and a syllabus map is enough;
- **B:** a topic map without any claim to be preparation;
- **C:** a data certification whose statistics and tools we teach, not the vendor's exam;
- **No:** not a fit.

| Exam | Body | Who sits it | When | Fit | The work | Priority | Source |
|---|---|---|---|---|---|---|---|
| GATE Statistics (ST) | IIT Madras for 2027 | Graduates seeking MSc, PhD and PSU posts | 6–21 February 2027; 65 questions, 85 of 100 marks on Statistics; a revised 12-section syllabus | A | A map from the official syllabus | **Wave 1** | IIT Madras press release (official) |
| IIT JAM Mathematical Statistics (MS) | An IIT, by rotation | Graduates seeking IIT MSc | 14 February 2027 (reported); about 25% maths, 75% statistics; MCQ, MSQ, numerical | A | A map; the maths part is thinner on our site | **Wave 1** | PW, Shiksha (reported) |
| SSC CGL, Junior Statistical Officer, Paper II | Staff Selection Commission | Graduates seeking central posts | With CGL Tier 2; 100 questions, 2 hours, −0.5 a wrong answer (reported) | A | A map; our BSc units cover it | Wave 4 | PW, Testbook (reported) |
| ISI admission test, MStat | Indian Statistical Institute | Graduates seeking ISI's MStat | May 2027 (reported) | A | A map; problem-solving depth | Wave 4 | isical.ac.in (to confirm) |
| Other state commissions' ASO posts; CUET-PG Statistics | Various | Graduates | Varies | A | One map each, as for APPSC | Later | Each commission (to confirm) |
| Actuarial Statistics CS1 | Institute of Actuaries of India; IFoA | Actuarial students | IAI: 29–30 October 2026, and May; weights: data analysis 10%, distributions 20%, inference 25%, regression 30%, Bayesian 15% | B | A topic map to our actuarial and inference units; Bayesian is thin | Wave 4 | IAI syllabus PDF (official) |
| Exam P (Probability) | Society of Actuaries | Actuarial students worldwide | Year-round, computer-based; 30 multiple-choice questions in 3 hours | B | A topic map to our probability and distribution units | Wave 4 | SOA syllabus (official) |
| AP Statistics | College Board | School students, mainly in the US | Each May; revised for 2026–27 into five units | B | A topic map to Descriptive Statistics and Inferential Statistics | Later | College Board (official) |
| Six Sigma Green Belt | ASQ | Quality and process professionals | Year-round; probability, statistics, capability, DOE, SPC | B | A topic map to our quality-control and design units | Later | ASQ Body of Knowledge (official) |
| Power BI Data Analyst (PL-300) | Microsoft | Analysts | Year-round; prepare 25–30%, model 25–30%, visualise and analyse 25–30%, deploy 15–20% | C | The Data Analyst path covers the same ground; never called PL-300 preparation | With Wave 3 | Microsoft study guide (official) |
| Google Data Analytics certificate | Google (on Coursera) | Career changers | Self-paced; spreadsheets, SQL, Tableau, R | C | The same, as for PL-300 | With Wave 3 | Google / Coursera (official) |
| RSS examinations | Royal Statistical Society | — | Withdrawn in 2017 | No | — | — | HKSS notice (reported) |
| ASA PStat / GStat | American Statistical Association | — | An accreditation by portfolio, not an exam | No | — | — | ASA guidelines (official) |
| RBI Grade B (DSIM) | RBI | — | Removed from the site earlier, by your decision | No | — | — | — |

---

## 7. What success looks like

| Measure | Target |
|---|---|
| GATE ST and JAM MS: learners who set either as their exam | 100 before 6 February 2027 |
| Statistics Foundations: learners who start the path | 150 by 31 March 2027 |
| Statistics Foundations: "path complete" badges | 30 by 31 March 2027 |
| Data Analyst: learners who start the path | 100 by 30 June 2027 |
| New questions flagged by the statistics after 30 answers | Under 5% |

These come from the app's own counts; no tracker is added.

---

## 8. Risks

| Risk | What we do |
|---|---|
| One part-time person, too much at once | One wave at a time; nothing before the launch; review is the only weekly load the paths add |
| A wrong key in a drafted question | A worked answer and a recompute log on every question, your approval, and the nightly statistics |
| Seeming to promise a certification | "Covers the topics in the published outline", with the outline linked; never "PL-300 prep", "certified" or "accredited" |
| Copying a syllabus | Quote syllabus lines as the existing maps do, with the source linked |
| Exam dates and patterns change | Confirm each at its official site before a map is published, and recheck each year |

---

## 9. Decisions needed from you

| # | Decision | By |
|---|---|---|
| 1 | The GATE ST and JAM MS maps: yes or no | 1 December 2026 |
| 2 | The two path lists in §3: confirm or change | 15 December 2026 |
| 3 | The badge wording, e.g. "Path complete: Statistics Foundations, 3 March 2027" | 10 January 2027 |
| 4 | Which Wave 4 maps | At the review, 28 February 2027 |

---

## 10. Sources

Official:
- GATE 2027 dates and syllabus revision, IIT Madras:
  https://www.iitm.ac.in/happenings/press-releases-and-coverages/iit-madras-announces-dates-syllabus-revision-new-paper
- IAI CS1 syllabus 2026: https://www.actuariesindia.org/sites/default/files/inline-files/IAI-CS1-Syllabus-2026.pdf,
  and the IAI examination dates: https://www.actuariesindia.org/examination-dates-1
- IFoA Actuarial Statistics: https://actuaries.org.uk/qualify/curriculum/actuarial-statistics
- SOA Exam P syllabus: https://www.soa.org/education/exam-req/edu-exam-p-detail/study/
- AP Statistics exam: https://apcentral.collegeboard.org/courses/ap-statistics/exam
- ASQ Six Sigma Green Belt Body of Knowledge: https://www.asq.org/cert/resource/docs/2014/FINAL%202014%20Green%20Belt%20BOK.pdf
- Microsoft PL-300 study guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/pl-300
- Google Data Analytics certificate: https://www.coursera.org/professional-certificates/google-data-analytics
- ASA accreditation guidelines: https://www.amstat.org/asa/files/pdfs/accreditation/Guidelines.pdf

Reported:
- IIT JAM 2027: https://www.pw.live/iit-jam/exams/iit-jam-2027, https://www.shiksha.com/science/articles/iit-jam-2027-blogId-221604
- GATE Statistics 2027 syllabus sections: https://collegedunia.com/exams/gate/statistics-syllabus
- SSC CGL Statistics paper: https://www.pw.live/ssc/exams/ssc-cgl-tier-2-syllabus
- ISI admission test: https://www.sciastra.com/exams/isi-admission-test-syllabus
- RSS examinations withdrawn in 2017: https://www.hkss.org.hk/index.php/prof/exam/courses/2-uncategorised

Our own figures:
- the content repository's tree and the site's home-page check (36 statistics courses, 153 unit
  pages);
- the application's question bank, counted on a fresh `setup_local` database on 2 October 2026.
