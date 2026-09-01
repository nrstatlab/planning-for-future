# Course 2 — Problem Solving Using C

**Semester I**

---

## Why this course exists

You will spend your career in Python and R, not C. So why start here?

Because C hides nothing. When you write `x = y` in Python, an enormous amount
happens that you never see. In C you allocate the memory, you free it, you pass
the address. Every abstraction that Python gives you free, C makes you build —
and having built it once, you understand what Python is doing on your behalf
for the next three years.

The two ideas that matter most for later are **pointers** (Unit 4) and **manual
memory management** (Unit 5). When a Pandas operation is unexpectedly slow
because it copied a dataframe instead of viewing it, this course is why you
will know what happened.

## Course objectives (verbatim)

1. Understand the fundamentals of computer programming; apply structured
   problem-solving approaches using algorithms, flowcharts and C constructs.
2. Develop efficient logic using decision-making, loop and jump control
   statements.
3. Utilize derived data types like arrays and strings for modular program design.
4. Design and implement modular solutions using functions, recursive logic,
   pointer operations and dynamic memory management.
5. Handle complex data structures including structures, unions and text file
   operations.

## Course outcomes

At the end of the course you should be able to:

1. Understand basic computing concepts and programming paradigms, and write
   structured C programs.
2. Apply control flow statements to solve logical and repetitive tasks.
3. Implement arrays and string operations to manage and manipulate data.
4. Design modular code using functions, recursion and appropriate parameter
   passing.
5. Use pointers and memory operations effectively; demonstrate competence in
   dynamic memory allocation and text file processing.

## Units

| Unit | Topic | Notes | Difficulty |
|:---:|---|---|---|
| 1 | Introduction to computer programming | [unit-1.md](unit-1.md) | Easy |
| 2 | Control statements | [unit-2.md](unit-2.md) | Easy |
| 3 | Derived data types — arrays and strings | [unit-3.md](unit-3.md) | Moderate |
| 4 | Pointers, functions and storage classes | [unit-4.md](unit-4.md) | **Hard** |
| 5 | Dynamic memory, structures, unions, files | [unit-5.md](unit-5.md) | **Hard** |

**Note on Unit 4:** the syllabus titles it "Functions", but the printed topic
list opens with pointers and covers functions afterwards. See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D5**. Do not be
caught out by revising from the unit title alone.

Units 4 and 5 carry most of the difficulty and most of the marks. Plan your
time accordingly — the [study plan](../../../STUDY-PLAN.md) gives them three
weeks between them.

## Also here

- [practice.md](practice.md) — exam-style questions with full solutions
- [lab.md](lab.md) — all 15 lab experiments, with the code and expected output
- `labs/course-2-c/` — the programs as `.c` files,
  all compiled and run
- `data/course-2-c/` — **practice datasets**, CSV: `employee-records.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

## Textbooks

- E. Balagurusamy, *Programming in ANSI C*, TMH, 6th edition — **the primary
  reference; most exam questions track it closely**
- Reema Thareja, *Computer Fundamentals and Programming in C*, OUP

**References:** Y. Kanetkar, *Let Us C* (BPB) · Griffiths & Griffiths,
*Head First C*

## How to study this course

1. **Type every program.** Reading C teaches you nothing; the compiler's error
   messages are the lesson. `gcc -Wall -Wextra program.c -o program`.
2. **Trace on paper.** Exams ask "what is the output of this code". You cannot
   answer that by running it. Practise walking through loops and recursive
   calls with a pen, tracking each variable in a table.
3. **Draw memory.** For anything involving pointers, draw boxes for variables
   and arrows for addresses. Every pointer bug becomes obvious in a diagram
   and invisible in prose.
4. **Learn the syntax errors.** A missing semicolon, `=` instead of `==`, a
   stray semicolon after `if(...)`. Recognising them instantly is worth real
   marks in the "find the error" questions.
