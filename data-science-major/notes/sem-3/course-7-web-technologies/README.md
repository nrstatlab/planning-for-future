# Course 7 — Web Technologies

**Semester III**

---

## Why a data science degree teaches web development

Three reasons, and they are all practical.

**A model nobody can use has produced nothing.** Semester VI's MLOps elective is
about deployment, and deployment usually means an HTTP interface. The Shiny app
in Course 6 is a web app; you just did not have to write the HTML.

**Dashboards are how analysis gets communicated.** Course 11 (Business
Intelligence Tools) and every reporting job you will ever have run in a browser.

**Data arrives over the web.** Unit 5's JSON is the format almost every API
speaks — including the weather API in lab experiment 15. Course 10's MongoDB
stores JSON-shaped documents natively.

This is also, incidentally, how the site you are reading was built.

## Course objectives (verbatim)

1. Understand the principles of web design and distinguish between web and
   desktop application architectures.
2. Develop static web pages using HTML elements, attributes, and multimedia
   integration techniques.
3. Style web pages effectively using CSS, including layout control, responsive
   design, and UI enhancements.
4. Implement dynamic behaviors and form validations using JavaScript and the
   Document Object Model (DOM).
5. Explore JSON and jQuery for handling structured data and simplifying
   client-side scripting.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | HTML | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | CSS | [unit-2.md](unit-2.md) | Moderate | 3 |
| 3 | JavaScript | [unit-3.md](unit-3.md) | Moderate | 3 |
| 4 | Client-side scripting | [unit-4.md](unit-4.md) | Moderate | 3 |
| 5 | JSON and jQuery | [unit-5.md](unit-5.md) | Moderate | 3 |

The material is broad rather than deep — there is a great deal of syntax and
comparatively little theory. That makes it easy to pass and easy to
underestimate: the lab exam asks you to *build* things, not describe them.

## Also here

- [practice.md](practice.md) — exam questions with solutions
- [lab.md](lab.md) — all 16 experiments
- `labs/course-7-web/` — runnable code
- `data/course-7-web/` — **practice datasets**, CSV: `products.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

> **On the lab code:** unlike the R labs, these **do run**. Node 22 with jsdom
> is available in the verification environment, so every JavaScript and DOM
> experiment is executed and asserted by
> `tools/run_web_labs.js`. The HTML and CSS
> files are structurally validated. What is *not* automated is visual
> appearance — open them in a browser for that.

## Textbooks

- Chris Bates, *Web Programming: Building Internet Applications*, Wiley, 2nd ed.
- Wang & Katila, *An Introduction to Web Design plus Programming*, Thomson
- Chaffer & Swedberg, *Learning jQuery*, Packt
- *JSON at Work*

**Reference:** David R. Brooks, *An Introduction to HTML and JavaScript for
Scientists and Engineers*, Springer

**Honest note on currency:** these textbooks predate a great deal of modern
practice. The syllabus's jQuery unit in particular describes a library whose
main purpose — smoothing over browser differences — has largely been solved by
the browsers themselves. Learn it because it is examined, and see
[unit-5.md §5.7](unit-5.md) for what the industry uses now. MDN
(developer.mozilla.org) is the reference professionals actually use.

## How to study this course

1. **Build, do not read.** Every concept here takes two minutes to try. A text
   editor and a browser are the entire toolchain.
2. **Learn the browser dev tools** — F12. The Elements tab shows live HTML, the
   Console shows JavaScript errors, the Network tab shows what was fetched.
   Debugging without them is guesswork.
3. **View source on sites you like.** Every page on the web ships its own source.
4. **Validate your HTML** at validator.w3.org. Browsers silently forgive broken
   markup; validators do not, and exams do not either.
