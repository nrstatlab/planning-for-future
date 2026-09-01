# Course 13 A — Artificial Intelligence

**Semester V**

**This is a Track A course**, paired with
Course 12 A (Machine Learning). Take one
track and you take it for Semester VI too.

---

## The one thing to understand before anything else

**This course is not about machine learning, and the difference is the point.**

Course 12 A learns a function from examples. This course **searches** — it is
given a description of a problem and finds a solution by exploring
possibilities. Nothing here is trained on data.

| | **Machine learning (12 A)** | **Classical AI (this course)** |
|---|---|---|
| Given | **Examples** with answers | A **description** of the problem |
| Produces | A fitted model | **A solution, or a path to one** |
| Method | Optimise parameters | **Search** and **inference** |
| Knowledge | Implicit, in the weights | **Explicit**, in facts and rules |
| Explains itself | Poorly | **Completely** — you can print the chain |
| Fails by | Overfitting | **Combinatorial explosion** |
| Good at | Perception, prediction | Reasoning, planning, constraints |

**Both are AI.** This course is the older half — search, logic, knowledge
representation — and it remains the right tool whenever the rules are known
and the answer must be justified. A hospital triage system that must explain
its reasoning is an expert system, not a neural network.

### 💡 The two halves of the course, in one line each

- **Units 2 and 3 are search.** Given a state space, find a goal. Everything
  is a variation on *which node do I expand next?*
- **Units 4 and 5 are knowledge.** Given facts and rules, derive new facts.
  Everything is a variation on *what follows from what I know?*

Unit 1 sets up the vocabulary for both.

## Where it sits in the degree

| From | You have | Used here |
|---|---|---|
| **Course 2 / 3** | Recursion, stacks, queues | **Unit 2 is those data structures.** DFS *is* a stack; BFS *is* a queue |
| **Course 3** | Complexity, big-O | Every search strategy is compared on time and space |
| **Course 4** | Probability, Bayes' theorem | **Unit 5's Bayesian networks** — Bayes again, on a graph |
| **Course 12 A** | Naive Bayes, evaluation | Unit 5 §5.4 is the same theorem; §5.6 contrasts the two paradigms |
| **Course 5** | Relational algebra, queries | Prolog is a database that can reason. `parent(X, Y)` is a table |
| **Course 1** | Boolean logic, truth tables | **Unit 4's propositional logic** is that, made into an inference system |

### ⚠️ The Prolog surprise

**The lab is entirely in Prolog**, a language you have not met. It is not like
C, Python or JavaScript: you do not write *how* to compute, you write *what is
true* and let the engine search.

Budget two weeks for the shift in thinking. §Lab setup below gets you running
without installing anything.

## Course objectives (verbatim)

1. Understand the fundamental concepts, history, types, and applications of
   Artificial Intelligence.
2. Develop problem-solving skills using state-space representations and search
   strategies for AI applications.
3. Apply informed and advanced search techniques including heuristics, local
   search, genetic algorithms, and constraint satisfaction problems.
4. Learn knowledge representation methods and reasoning techniques using
   propositional and first-order logic for intelligent agents.
5. Explore expert systems, probabilistic reasoning, fuzzy logic, and emerging
   AI technologies including NLP, robotics, and ethical considerations.

## Units

| Unit | Topic | Notes | Difficulty | Weeks |
|:---:|---|---|---|:---:|
| 1 | AI and intelligent agents | [unit-1.md](unit-1.md) | Easy | 2 |
| 2 | State space and uninformed search | [unit-2.md](unit-2.md) | Moderate | 3 |
| 3 | Informed and advanced search | [unit-3.md](unit-3.md) | **Hard** | 4 |
| 4 | Knowledge representation and reasoning | [unit-4.md](unit-4.md) | **Hard** | 4 |
| 5 | Expert systems, probabilistic and emerging AI | [unit-5.md](unit-5.md) | Moderate | 2 |

**Units 3 and 4 carry the marks.** A* and its admissibility proof, and
resolution with unification, are the two things this course is really about,
and both are asked every year.

## Also here

- [practice.md](practice.md) — exam questions with worked solutions
- [lab.md](lab.md) — all 19 experiments
- `labs/course-13a-ai/` — code
- `data/course-13a-ai/` — **practice datasets**, CSV: `family-relations.csv`, `graph-edges.csv`, `map-colouring.csv`.
  Every one was generated from a known truth, so you can score your answer
  rather than just produce one; `data/README.md` lists what each was built
  from, `data/PRACTICE-QUESTIONS.md` sets questions on each with a computed
  answer key, and `tools/check_datasets.py` proves every one of those
  answers against the file.

> **On the lab code.** SWI-Prolog cannot be installed here — the Debian
> repositories that host it are blocked by the egress policy — so each
> experiment has two halves:
>
> - **The `.pl` file** you would run in SWI-Prolog or SWISH. Marked
>   **NOT EXECUTED**. **This is what the lab examiner will ask for.**
> - **A Python half that runs**, verified by
>   `tools/run_ai_labs.py`.
>
> **Five experiments genuinely execute Prolog-style resolution.** The
> `pytholog` package on PyPI implements SLD resolution over facts and
> recursive rules, so the family tree, the graph, the logic encodings, forward
> chaining and the expert system are **run as logic programs**, not simulated.
>
> Its limits are asserted rather than glossed over: **pytholog has no list
> terms, no arithmetic evaluation, no cut and no DCG**, so those experiments
> are executed in Python instead and the `.pl` file carries the real Prolog.
> [lab.md](lab.md) says which is which for every experiment.

## Textbooks

- **Russell & Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed.,
  Pearson** — the standard text worldwide, and this syllabus follows its
  structure almost exactly. Chapters 2–4 are Units 1–3; 7–9 are Unit 4.
- Rich & Knight, *Artificial Intelligence*, 3rd ed., McGraw-Hill — older,
  shorter, and closer to the Indian syllabus tradition.
- Sterling & Shapiro, *The Art of Prolog*, MIT Press.
- **Blackburn, Bos & Striegnitz, *Learn Prolog Now!*** — free online, and the
  fastest way into the lab.

## How to study this course

1. **Get Prolog running in week 1**, before the theory needs it.
   [SWISH](https://swish.swi-prolog.org/) runs in a browser with no install.
2. **Trace every search by hand once.** BFS and DFS on the same small graph,
   writing the frontier at each step. Do it on paper; the code makes sense
   afterwards, and the exam asks for the trace.
3. **Learn the four properties of every search strategy** — complete, optimal,
   time, space. They are a table you will be asked to reproduce.
4. **Understand admissibility properly.** "h never overestimates" is the whole
   of A*'s guarantee, and §3.4 shows what breaks without it.
5. **Practise resolution until it is mechanical** — convert to CNF, negate the
   goal, unify, derive the empty clause. It is the hardest procedure in the
   course and the most reliably examined.
