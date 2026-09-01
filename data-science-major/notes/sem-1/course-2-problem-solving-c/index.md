---
layout: note
title: "Course 2 — Problem Solving Using C"
section: "Data Science Major"
---

# Course 2 — Problem Solving Using C

**Semester I · 3 credits theory (3 hrs/week) + 1 credit lab (2 hrs/week)**
Syllabus source: pages 9–13 of [the PDF](../../../docs/Data-Science-Major-Sem1-2.pdf)

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

## Course objectives (verbatim, page 9)

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
| 1 | Introduction to computer programming | [unit-1.md](unit-1.html) | Easy |
| 2 | Control statements | [unit-2.md](unit-2.html) | Easy |
| 3 | Derived data types — arrays and strings | [unit-3.md](unit-3.html) | Moderate |
| 4 | Pointers, functions and storage classes | [unit-4.md](unit-4.html) | **Hard** |
| 5 | Dynamic memory, structures, unions, files | [unit-5.md](unit-5.html) | **Hard** |

**Note on Unit 4:** the syllabus titles it "Functions", but the printed topic
list opens with pointers and covers functions afterwards. See
[`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.html) finding **D5**. Do not be
caught out by revising from the unit title alone.

Units 4 and 5 carry most of the difficulty and most of the marks. Plan your
time accordingly — the [study plan](../../../STUDY-PLAN.html) gives them three
weeks between them.

## Also here

- [practice.md](practice.html) — exam-style questions with full solutions
- [lab.md](lab.html) — all 15 lab experiments, with the code and expected output
- [`labs/course-2-c/`](../../../labs/course-2-c/) — the programs as `.c` files,
  all compiled and run

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
