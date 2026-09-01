# Course 3 — Python Programming and Data Structures

**Semester II**

---

## Why this course matters more than any other in the first year

Python is the language you will use for the rest of the degree and, most
likely, the rest of your career in data science. Data Mining (Sem IV), Python
for Data Analysis (Sem IV), Machine Learning, Deep Learning, NLP — all of them
assume this course.

Weak Python here means struggling in every later course. Strong Python here
makes them comfortable. If you have limited time in Semester II, spend it on
this course.

## Course objectives (verbatim)

1. To introduce the fundamentals of Python programming, including environment
   setup, syntax and core concepts.
2. To develop problem-solving skills using control flow, functions and modules.
3. To provide knowledge of Python data structures, file handling and exception
   handling for effective programming.
4. To impart object-oriented programming concepts and GUI development skills
   for building applications.

## Course outcomes

1. Explain the basic features, syntax, data types and operators of Python.
2. Apply control flow constructs, functions and modules to develop structured
   programs.
3. Demonstrate the use of sequences, sets and dictionaries for data handling.
4. Implement file handling and exception handling for robust applications.
5. Develop object-oriented and GUI-based applications.

## Units

| Unit | Topic | Notes | Difficulty | Weeks needed |
|:---:|---|---|---|:---:|
| 1 | Basics of Python programming | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | Control flow, functions and modules | [unit-2.md](unit-2.md) | Easy–Moderate | 2 |
| 3 | Sequences, sets and mapping types | [unit-3.md](unit-3.md) | Moderate | 3 |
| 4 | Files, exceptions and OOP | [unit-4.md](unit-4.md) | **Hard — overloaded** | **4** |
| 5 | Data structures and GUI | [unit-5.md](unit-5.md) | **Hard — two subjects** | 3 |

### Two warnings from the syllabus review

**Unit 4 holds roughly double a normal unit's content** — file handling *and*
exception handling *and* the whole of object-oriented programming (classes,
constructors, destructors, encapsulation, three kinds of inheritance, method
overriding). Compare Unit 1, which covers only literals, variables and
operators. Budget twice the time. See finding **D6**.

**Unit 5 fuses two unrelated subjects** — abstract data structures (linked
lists, stacks, queues) and Tkinter GUI programming. They share nothing. Study
them as two separate topics; the notes split the file accordingly. See finding
**D7**.

## Also here

- [practice.md](practice.md) — exam-style questions with solutions
- [lab.md](lab.md) — all 18 lab experiments explained
- `labs/course-3-python/` — the programs, all run
- `data/course-3-python/` — **practice datasets**, CSV: `students.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## Textbooks

- Anita Goel, *Python Programming — An Object Oriented Approach*, Universities Press
- Reema Thareja, *Python Programming using Problem Solving Approach*, OUP, 2020
- Budd T. A., *Exploring Python*, McGraw-Hill, 1st edition, 2011

**References:** Martin C. Brown, *Python: The Complete Reference* (McGraw-Hill,
2018) · Kenneth A. Lambert, *Fundamentals of Python: First Programs* (Cengage,
2nd edition, 2019)

## How to study this course

1. **Use the interactive shell constantly.** Type `python3`, then experiment.
   Anything you are unsure about takes ten seconds to check.
2. **Do not just read code — predict it.** Before running a snippet, write down
   what you think it prints. Being wrong is where the learning happens.
3. **Learn the error messages.** `IndentationError`, `TypeError`,
   `AttributeError`, `KeyError`, `IndexError` — each tells you precisely what
   went wrong once you can read it.
4. **Practise the mutable/immutable distinction until it is automatic.** It
   explains more Python surprises than anything else, and it is heavily
   examined.
