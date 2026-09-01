# Course 6 — Data Science with R

**Semester III**

---

## Why R, when you already have Python

A fair question, and worth answering properly because you will be asked it.

R was built **by statisticians, for statistics**. Python is a general-purpose
language that grew a data stack. That difference shows: a linear model in R is
`lm(y ~ x, data)` and the summary already contains coefficients, standard
errors, t-values, p-values and R². In Python you assemble that yourself.

R dominates in academic statistics, biostatistics, clinical trials and
econometrics. Python dominates in production machine learning and engineering.
**The employable answer is that you can read and write both** — and that is why
this course sits beside Course 9 rather than replacing it.

`ggplot2` is also, plainly, the best plotting library in either language, and
it is worth learning for that alone.

## Course objectives (verbatim)

1. Introduce the data science process, lifecycle, and applications in real-world
   domains.
2. Build proficiency in R programming for data manipulation, exploration, and
   visualization.
3. Train students in handling structured, unstructured, and time-based data
   effectively.
4. Familiarize with basic machine learning and statistical modeling using R.
5. Develop awareness of ethical, interpretability, and responsible use of data
   science.

## Course outcomes

1. Explain the Data Science process and perform EDA.
2. Write R programs using variables, functions, loops and packages.
3. Perform data wrangling, cleaning and visualization with `dplyr`, `tidyr`,
   `ggplot2`.
4. Build and evaluate basic machine learning models such as regression and
   clustering.
5. Apply data science techniques to practical case studies.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | The Data Science process | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | Basics of R programming | [unit-2.md](unit-2.md) | Easy–Moderate | 3 |
| 3 | Data handling and visualization | [unit-3.md](unit-3.md) | Moderate | 3 |
| 4 | Applications and case studies | [unit-4.md](unit-4.md) | **Hard** | 3 |
| 5 | Advanced topics | [unit-5.md](unit-5.md) | **Hard — overloaded** | **4** |

> ⚠ **Unit 5 carries three separate subjects.** ARIMA time series analysis
> *and* interactive `plotly` visualisation *and* the Shiny web framework — any
> one of which is a course in its own right. Compare Unit 2, which covers
> variables and loops. Budget double time, and if you are short of it, prioritise
> **time series**: it is the most examinable and it feeds the Semester VI
> elective. See [`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D12**.

## Also here

- [practice.md](practice.md) — exam-style questions with worked solutions
- [lab.md](lab.md) — all 18 practicals
- `labs/course-6-r/` — R scripts, with runnable
  Python equivalents
- `data/course-6-r/` — **practice datasets**, CSV: `car-mileage.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.
  Also `flowers.csv` in `data/shared/`, which several courses
  analyse so their answers can be compared.

> **On the lab code:** R could not be installed in the environment where this
> material was verified (the package repositories are blocked), so the R scripts
> are **desk-checked, not executed** — each says so in its header. Every one has
> a Python equivalent in `labs/course-6-r/python/`
> that **was** executed, so the logic and the expected numbers are machine-checked
> even though the R syntax is not. Run the R yourself in RStudio.

## Textbook

- James, Witten, Hastie & Tibshirani, *An Introduction to Statistical Learning
  with Applications in R*, Springer, 2nd edition, 2021 — **free and legal to
  download** from [statlearning.com](https://www.statlearning.com/); the single
  best book on this syllabus

**References:** Matloff, *The Art of R Programming* (No Starch, 2011) ·
Venables & Ripley, *Modern Applied Statistics with S* (Springer, 2002) ·
Irizarry, *Introduction to Data Science* (CRC, 2020) · Grus, *Data Science from
Scratch* (for conceptual clarity)

## How to study this course

1. **Install R and RStudio on your own machine.** Both are free. You cannot
   learn R by reading about R.
2. **Use RStudio's built-in help constantly.** `?mean` and `help(dplyr)` are
   faster than searching the web.
3. **Learn the pipe early.** `%>%` (or the newer `|>`) is what makes R code
   readable, and every `dplyr` example uses it.
4. **Remember R indexes from 1, not 0.** After a semester of Python and C this
   will catch you at least once a week.
5. **Compare with Python as you go.** The Python equivalents in the labs exist
   for exactly this — seeing `dplyr::filter()` beside `df[df.x > 5]` teaches
   both at once.
