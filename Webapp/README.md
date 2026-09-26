# Webapp: turning NRSTATLAB into a learning platform

This folder holds everything planned for **NRSTATLAB Learn**, the Django web application built from
this site. In it, visitors still read everything free. Signed-in learners also:
- keep their progress on every device;
- take a unit test after each unit;
- sit old papers in exam mode;
- see how ready they are for their exam.

| File | What it is | Read it when |
|---|---|---|
| [`Webapp.docx`](Webapp.docx) | The CEO brief (vision, principles, the apps decision, measures of success, scope, risks) with the build prompt | First: it explains the why |
| [`PROMPT.md`](PROMPT.md) | The build prompt as plain text, ready to paste into a coding assistant | When you start the build |
| [`BUILD-GUIDE.md`](BUILD-GUIDE.md) | The step-by-step guide: 21 steps in 8 phases, each with how to do it and how you know it is done | During the build, one phase at a time |

## The plan in brief

**One Django project, with the three areas as three apps.** Four supporting apps sit beside them.

| App | Holds |
|---|---|
| `study` (Study Material) | Courses and units, at today's addresses |
| `examinations` (Examinations) | Exams, syllabus items, readiness |
| `papers` (Old Papers Solved) | Solved papers, official keys, exam mode |
| `assessments` | The one question bank and test engine the three areas share |
| `progress` | Studied and passed status, the dashboard, and import of browser progress |
| `accounts` | Login, privacy, export and deletion |
| `core` | Layout, navigation and redirects |

**The phases:**
- **0. Plan**
- **1. Foundations:** today's pages, served by Django at the same URLs.
- **2. Accounts and progress.**
- **3. Unit tests.**
- **4. Old papers.**
- **5. Readiness.**
- **6. Quality loop:** item analysis and review.
- **7. Launch:** security, hosting, and the domain move.

**What never changes:**
- Study material stays free without login.
- Every answer key is checked before it is scored.
- There is no exam claim without an official source.
- The app collects the minimum personal data.

## Before building

Answer the eight questions at the end of `PROMPT.md`: where the code lives, domain, hosting, email
provider, Google sign-in, pass mark and test length, learners under 18, and reviewers. Two of them
shape everything:

- **Where the code lives.** The recommendation is a separate repository. GitHub Pages publishes
  every file in this one, and that includes this folder.
- **The domain.** A Django application cannot run on `nrstatlab.github.io`, so the application
  needs a domain of its own (BUILD-GUIDE, Step 20).
