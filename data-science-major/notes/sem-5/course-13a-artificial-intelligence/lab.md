# Course 13 A — Practical Lab

**19 experiments**
The syllabus names **SWI-Prolog** and adds *"environment for practice without
installation"* — meaning [swish.swi-prolog.org](https://swish.swi-prolog.org/),
which runs in a browser.

Code lives in `labs/course-13a-ai/`.

## Read this before you read anything else

**SWI-Prolog is not installed in the verification environment.** The Debian
repositories that host it are blocked by the egress policy, the same wall that
stopped R in Course 6, WEKA in Course 8 and `mongod` in Course 10.

So this course ships **two halves**, and you must know which is which:

| Half | Files | Status |
|---|---|---|
| **The Prolog you submit** | **16 `.pl` files** | **`*** NOT EXECUTED ***`** in the header of every one |
| **The verification** | **7 `.py` files** | **Executed and asserted** by `tools/run_ai_labs.py` |

**The `.pl` file is the deliverable.** It is what you paste into SWiSH and what
the examiner marks. The `.py` file exists so that every number quoted in these
notes has been *computed* rather than remembered.

```bash
pip install -r tools/requirements.txt
python3 tools/run_ai_labs.py
```

Output ends:

```
16 Prolog programs, all carrying '*** NOT EXECUTED ***'
they cover experiments: [1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19]
(08_graph_search.pl covers experiments 8-11, which are one graph)

7 lab programs executed and asserted, 0 failed
covering all 19 prescribed experiments
```

**Nineteen experiments, sixteen files** because experiments 8–11 are one graph
asked four ways — represent it, DFS it, BFS it, compare the path lengths — so
they share `08_graph_search.pl`.

### ⚠️ Five experiments *do* run as real logic programs

`pytholog` is a small Prolog engine on PyPI, and PyPI is reachable. It performs
**genuine SLD resolution** over facts and recursive rules, so experiments **1,
15, 16, 17 and the backward-chaining half of 16** are not simulated — they are
resolved.

**Its limits are real, and the script proves each one before working around
it** rather than quietly avoiding it:

| Limit | What the script shows | Which experiments |
|---|---|---|
| **No list terms** | `mem(b, [a,b,c])` returns **`['No']`** where SWI-Prolog says `true` | 2, 3, 4 |
| **`is/2` does not evaluate** | `fact(5, X)` returns **`['No']`** where SWI-Prolog gives `X = 120` | 5, 6 |
| **No cut** | `!` is not a term at all | 7 |
| **No DCG** | `-->` is not parsed | 18 |
| **Arity ≥ 1 required** | a 0-arity proposition raises `IndexError` | 16 (rewritten with a dummy argument) |
| **Nested derived rules** | `cousin` via `sib/2` returns **`['bhanu', 'kiran', 'meena']`** — kiran is his own cousin | 1 |

That last row is the important one, and §"Experiment 1" below spends real space
on it. **The `.pl` file uses the idiomatic nested form because SWI-Prolog
handles it correctly.** The engine limitation is documented, not hidden.

---

## Experiment 1 — A family tree

`01_family_tree.pl` ·
`01_family_tree.py` — **runs
through real SLD resolution**

The tree, from `fixtures.py`:
`ram` and `sita` have `asha` and `ravi`; `asha` has `meena` and `kiran`;
`ravi` has `bhanu`.

| Query | Answer |
|---|---|
| `parent(ram, X)` | `['asha', 'ravi']` |
| `father(X, asha)` | `['ram']` |
| `grandparent(ram, X)` | `['bhanu', 'kiran', 'meena']` |
| `ancestor(ram, X)` | `['asha', 'bhanu', 'kiran', 'meena', 'ravi']` |

**`ancestor/2` is the one that matters.** `parent(ram, X)` returns two names;
`ancestor(ram, X)` returns five. The extra three are two levels down and reach
the answer **only through the recursive clause**. Delete that clause and they
vanish — which is the demonstration that this is resolution and not a lookup.

### 🎯 Three things this experiment teaches that the syllabus does not say

**1. Clause order is semantics, not style.** Put the base case first:

```prolog
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
```

Write it left-recursively — `ancestor(X,Y) :- ancestor(X,Z), parent(Z,Y).` —
and SWI-Prolog **loops for ever**. The logic is identical; the *procedure* is
not, because Prolog is backward chaining with **depth-first** search.

**2. `sibling/2` needs a guard.** Without `X \= Y`:

```
sibling(asha, X)  with the guard -> ['ravi']
without the guard                -> ['asha', 'ravi']   <- asha is her own sibling
```

Every `parent(P,X), parent(P,Y)` pair unifies with `X = Y` unless you forbid it.

**3. One solution per *proof*, not per answer.**

```
raw solutions for sibling(asha, X): ['ravi', 'ravi']
distinct                          : ['ravi']
```

`asha` and `ravi` share **both** `ram` and `sita`, so the goal succeeds twice —
once down each parent. `setof/3` collapses it. This is a property of
resolution, not a bug, and examiners like the answer.

### ⚠️ Where pytholog gets `cousin/2` wrong

| Formulation | Answer for `cousin(kiran, X)` |
|---|---|
| **Flat** — parents' sibling's children, inline | **`['bhanu']`** — correct |
| **Nested** — calls a derived `sib/2` | `['bhanu', 'kiran', 'meena']` — **wrong** |

`kiran` is not his own cousin, and `meena` is his **sister**. pytholog does not
propagate the inequality guard correctly through a nested derived predicate.
**SWI-Prolog handles the nested form correctly**, and the `.pl` file uses it
because it is the idiomatic encoding. This is an **engine** limitation.

---

## Experiments 2–7 — Lists, arithmetic and the cut

`02_lists.pl` ·
`03_maximum.pl` ·
`04_flatten.pl` ·
`05_factorial_fib.pl` ·
`06_gcd.pl` ·
`07_cut_fail.pl` ·
`02_lists_and_arithmetic.py`

pytholog has neither list terms nor arithmetic evaluation, and the script
**asserts both failures first** — `mem(b, [a,b,c]) -> ['No']` and
`fact(5, X) -> ['No']` — before executing the logic in Python.

### Experiment 2 — `member/2`, `append/3`, `reverse/2`, `length/2`

| Goal | Result |
|---|---|
| `member(b, [a,b,c])` | true |
| `append([a,b,c], [d,e], X)` | `[a,b,c,d,e]` |
| `reverse([a,b,c], X)` | `[c,b,a]` |
| `length([a,b,c], N)` | `3` |

### 🎯 The answer that earns the marks

```
append(X, Y, [a,b,c]) -> 4 solutions:
  ([], [a,b,c])   ([a], [b,c])   ([a,b], [c])   ([a,b,c], [])
```

**`append/3` runs backwards.** One definition both concatenates and splits,
because a Prolog rule states a **relation**, not a function. A Python
`append()` can never do this. If the viva asks "what makes Prolog different",
this is the two-line answer.

### Experiments 3 and 4 — maximum, and flatten

```
max([3,7,2,9,4]) -> 9
flatten([1, [2, [3, 4], 5], [[6]], 7]) -> [1, 2, 3, 4, 5, 6, 7]
flatten([[], [[]], 1])                 -> [1]
```

For `max/2` the base case is the **one-element** list, not the empty one —
`max([], M)` has no answer, and writing `max([], 0)` is wrong for negative
numbers. For `flatten/2` there are three clauses: empty list, list head
(recurse and append), atom head (keep). **Empty sublists disappear** — the
second example is the case people forget.

### Experiments 5 and 6 — factorial, Fibonacci, GCD

```
factorial 0..5 -> [1, 1, 2, 6, 24, 120]
fibonacci 0..9 -> [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
naive fib(10) makes 177 recursive calls

gcd(48, 18) = 6   trace: (48,18) -> (18,12) -> (12,6) -> 6
gcd(17, 5)  = 1   (coprime)
```

**177 calls for `fib(10)`** is the number to quote: the naive Prolog definition
is exponential for exactly the reason the Python one is. The fix is an
accumulator, or `assertz/1` to memoise — Prolog's dynamic programming.

### Experiment 7 — cut and fail

pytholog has no cut, so this experiment is documented as **semantics** and the
`.pl` file carries the real program.

| Construct | Meaning |
|---|---|
| `!` | commits to this clause **and** to the bindings made before it; discards remaining choice points |
| `fail` | always fails, forcing backtracking |
| `!, fail` | commit, then fail — the whole goal fails with **no alternatives tried** |
| `\+ G` | negation as failure — succeeds if `G` cannot be proved |

```prolog
fly(X) :- penguin(X), !, fail.
fly(X) :- bird(X).
```

For a penguin the first clause commits and fails, so **the second is never
tried**. Remove the cut and every penguin flies.

### 📖 Green cut and red cut

- **Green cut** — removes only redundant choice points. Delete it and nothing
  changes but speed.
- **Red cut** — changes the **meaning**. Delete it and the answers change.

The cut is where Prolog stops being pure logic: clause order and cut placement
become semantically load-bearing, which is why it is the hardest thing to
debug.

### ⚠️ `\+` is not logical negation

```
known birds: ['polly', 'tweety'], known penguins: ['pingu']
\+ penguin(tweety)  succeeds  -- tweety is not known to be one
\+ bird(kiwi)       succeeds  -- but we simply do not know
```

Prolog assumes a **closed world**: anything not derivable is false. Logical
negation would require *proving* the fact untrue. A kiwi is a bird.

---

## Experiments 8–11 — A graph, DFS, BFS, and the comparison

`08_graph_search.pl` ·
`03_uninformed_search.py`

Four experiments, one graph. The Python half runs both on the **Romania map**
from Russell & Norvig (20 cities, real distances) and on a six-node graph built
to make one specific point.

### The Romania run — the table to memorise

| Strategy | Expanded | Edges | Cost | Path |
|---|---:|---:|---:|---|
| **BFS** | 9 | **3** | 450 | Arad → Sibiu → Fagaras → Bucharest |
| **DFS** | **6** | 5 | **607** | Arad → Zerind → Oradea → Sibiu → Fagaras → Bucharest |
| **Uniform cost** | **13** | 4 | **418** | Arad → Sibiu → **Rimnicu Vilcea → Pitesti** → Bucharest |

Read it in three lines:

- **BFS found the fewest edges (3) and 450 km — not the cheapest.** Step costs
  are unequal here, so its optimality guarantee **does not apply**.
- **DFS expanded the fewest (6) and found the worst path, 607 km.** Cheap and
  wrong.
- **UCS found the optimal 418 and expanded the most, 13.** Optimality is paid
  for in nodes.

**Neither BFS nor DFS finds the optimal route**, because it runs through
Rimnicu Vilcea and Pitesti and neither strategy has any reason to go that way.

### 🔢 UCS *is* Dijkstra

```
shortest distance from Arad:
  Sibiu           140 km
  Rimnicu Vilcea  220 km
  Pitesti         317 km
  Bucharest       418 km
  Neamt           824 km
```

**140 + 80 + 97 + 101 = 418** — the optimal route accumulated one city at a
time. Same procedure, reached from the AI side rather than from graph theory.

### The six-node graph — same work, twice the path

```
a -> b, c    b -> d    d -> e    e -> g    c -> g
```

| | Path | Edges | Expanded |
|---|---|---:|---:|
| **BFS** | a → c → g | **2** | **5** |
| **DFS** | a → b → d → e → g | **4** | **5** |

**Identical work, twice the path.** BFS explores level by level so it cannot
miss the 2-edge route; DFS dived into `b` and committed to the long way round.
That is exactly the guarantee BFS gives and DFS does not — stated as a measured
fact rather than as a property table.

### 🔢 And the counterexample that kills "BFS is optimal"

| Step costs | BFS cost | UCS cost |
|---|---:|---:|
| all 1 | 2 | 2 — **equal** |
| make `c→g` cost 50 | **51** (a → c → g) | **4** (a → b → d → e → g) |

**BFS counts edges, not cost.** With equal step costs those are the same thing,
so BFS is optimal. The moment they differ it is not — and the gap here is
51 against 4.

### 🔢 Iterative deepening costs 11.1%

With branching factor **b = 10** and depth **d = 5**:

| | Nodes generated | Memory |
|---|---:|---|
| BFS | **111,111** | O(b^d) = 100,000 |
| IDS | **123,456** | **O(bd) = 50** |

**11.1% more nodes for 2,000× less memory.** The repetition is cheap because
the bottom level holds most of the nodes, so regenerating everything above it
costs almost nothing. IDS is the preferred uninformed search when the depth is
unknown — and 111,111 / 123,456 are pleasing enough to remember.

---

## Experiment 12 — Greedy Best-First and A*

`12_astar.pl` ·
`04_informed_search.py`

### 🔢 The single most quotable result in the course

| Search | f(n) | Expanded | Cost | Optimal? |
|---|---|---:|---:|---|
| Uniform cost | g(n) | 13 | **418** | YES |
| Greedy best-first | h(n) | **4** | 450 | NO |
| **A\*** | **g(n) + h(n)** | **6** | **418** | **YES** |

**A\* found the optimal 418 expanding 6 nodes where UCS needed 13.** Same
answer, less than half the work. That one sentence is why heuristics exist.

### Why greedy goes wrong, in two numbers

At Sibiu, greedy compares `h` only:

```
h(Fagaras)        = 176   <- looks closer, so it goes here
h(Rimnicu Vilcea) = 193
```

but the actual routes are **450 km via Fagaras** and **418 km via Rimnicu** —
32 km shorter. **Fagaras is closer as the crow flies and further by road.**
Greedy is short-sighted because it ignores `g(n)`, the cost already paid, which
is precisely what A* adds back.

### 🎯 A* with h = 0 *is* uniform cost search

```
A* with h(n) = 0: expanded 13, cost 418
uniform cost    : expanded 13, cost 418
```

**Identical, not merely similar.** A* sits between UCS (no information,
optimal) and greedy (maximum information, used badly, not optimal).

### ⚠️ An inadmissible heuristic is faster and wrong

| Heuristic | Expanded | Cost | Optimal? |
|---|---:|---:|---|
| straight-line (admissible) | 6 | **418** | YES |
| straight-line **× 2** | **4** | 450 | **NO** |
| straight-line **× 5** | **4** | 450 | **NO** |

Overestimating makes the node on the optimal path *look* worse than an
alternative, so A* commits to a goal before the better path is explored. **The
guarantee is gone the moment h(n) > h\*(n) anywhere** — and the price here is
2 fewer expansions for 32 extra kilometres.

### 🔢 Admissibility, checked rather than assumed

```
checked all 20 cities against their TRUE cost to Bucharest:
  straight-line violations: 0   -- admissible
  h(Bucharest) = 0
  tightest margin h*(n) - h(n) = 1 km
  the x2 heuristic violates admissibility at 18 of 20 cities
```

**A straight line can never be longer than a road**, so this heuristic is
admissible **by construction**, not by luck. That is the argument to give in
the exam — and the margin of **1 km** shows how tight the bound is, which is
what makes the heuristic good rather than merely valid.

### 🔢 8-puzzle: h2 dominates h1

| State | h1 (misplaced tiles) | h2 (Manhattan) |
|---|---:|---:|
| goal | 0 | 0 |
| one tile out | 2 | 2 |
| well scrambled | **6** | **14** |

Both come from **relaxed** problems — h1 lets a tile move anywhere, h2 lets it
move to any adjacent square — so both are admissible **by construction**.
**h2 ≥ h1 everywhere, so h2 dominates**, and A* with h2 expands no more nodes
than A* with h1. *Dominance* is the right way to compare two heuristics, and a
far stronger claim than "it was faster on my example".

---

## Experiments 13 and 14 — CSP: map colouring and N-Queens

`13_map_colouring.pl` ·
`14_n_queens.pl` ·
`05_csp_backtracking.py`

### Experiment 13 — Australia, 3 colours, 7 regions

| Region | Colour |
|---|---|
| WA | red |
| NT | green |
| **SA** | **blue** |
| Q | red |
| NSW | green |
| V | red |
| T | red |

| Method | Assignments | Backtracks |
|---|---:|---:|
| plain backtracking | 7 | **0** |
| MRV + degree | 7 | **0** |

**Zero backtracks either way** — and that is worth saying honestly rather than
pretending the heuristics saved the day. **SA borders every mainland region**,
so MRV and the degree heuristic both pick it early; but the plain ordering
happens to reach it early too, and once SA is fixed every neighbour has only
two colours left.

### 🔢 With only two colours: no solution, after 4 backtracks

The reason is structural: **`WA`, `NT` and `SA` are mutually adjacent** — a
triangle needs three colours. The search discovers this by exhausting every
possibility, which is what "no solution" *means* in a CSP.

### 🎯 MRV and LCV pull in opposite directions, and that is correct

After `WA = red`, the legal values remaining:

| Region | Values left |
|---|---:|
| **NT** | **2** |
| **SA** | **2** |
| Q, NSW, V, T | 3 |

MRV picks **NT** (fewest options). LCV then orders its values
`['green', 'blue']`, least constraining first.

> **Variables: fail fast. Values: fail late.**
> MRV chooses the **variable** most likely to fail, because you want to
> discover a dead end *now*. LCV chooses the **value** least likely to fail,
> because once you have committed you want it to survive.

### 🔢 Experiment 14 — 8-Queens

```
92 distinct solutions, found after 2,056 placements
the first, as a row per column: (0, 4, 7, 5, 2, 6, 1, 3)

  Q . . . . . . .
  . . . . . . Q .
  . . . . Q . . .
  . . . . . . . Q
  . Q . . . . . .
  . . . Q . . . .
  . . . . . Q . .
  . . Q . . . . .
```

| n | Solutions |
|---:|---:|
| 4 | **2** |
| 5 | 10 |
| 6 | **4** |
| 7 | 40 |
| 8 | **92** |

**The counts are irregular** — n = 6 has *four* solutions where n = 5 has ten.
There is no formula; they are computed by search. That is *why* N-Queens is a
search problem at all, and it is a better answer than "92" on its own.

---

## Experiments 15–17 — Logic, chaining and an expert system

`15_logic.pl` ·
`16_chaining.pl` ·
`17_expert_system.pl` ·
`06_logic_and_chaining.py`
— **16 and 17 run through real SLD resolution**

### Experiment 15 — truth tables and entailment

| P | Q | ¬P | P∧Q | P∨Q | P⇒Q | P⇔Q |
|---|---|---|---|---|---|---|
| F | F | T | F | F | **T** | T |
| F | T | T | F | T | **T** | F |
| T | F | F | F | T | **F** | F |
| T | T | F | T | T | T | T |

**P⇒Q is true whenever P is false.** It is not causation — it says only *there
is no case where P holds and Q fails*, which is exactly **¬P ∨ Q**, verified
over all 4 models. That equivalence is step 2 of the CNF procedure, and
everything in resolution depends on it.

Over the 8 models of P, Q, R:

| Sentence | True in | Verdict |
|---|---:|---|
| P ∨ ¬P | **8/8** | VALID (tautology) |
| P ∧ ¬P | **0/8** | UNSATISFIABLE |
| P ∧ Q | 2/8 | SATISFIABLE |

**Entailment, measured:** `{P, P⇒Q}` has **2 models**, and Q holds in all of
them, so `{P, P⇒Q} ⊨ Q`. Equivalently **KB ∧ ¬Q has zero models** — and *that*
second form is what resolution mechanises.

Modus ponens and modus tollens were verified over all 4 models. **Affirming the
consequent (P⇒Q, Q ⊢ P) is not valid**, and the table shows why in one cell:
row (F, T) has P false and Q true.

### Experiment 16 — forward and backward chaining

**Forward**, from `{a, b}` and 3 rules:

```
derived, in order: ['c', 'd', 'e']
final KB:          ['a', 'b', 'c', 'd', 'e']
```

**Backward**, the same rule base, through real resolution:

```
?- c(x).  -> Yes
?- d(x).  -> Yes
?- e(x).  -> Yes
?- z(x).  -> TypeError   (pytholog raises on an unknown predicate
                          where SWI-Prolog answers 'false')
```

To prove `e` it needs `d`, which needs `c`, which needs `a` and `b` — and it
**never derives anything outside that chain**. Forward chaining derives
everything derivable whether or not it was wanted.

> **Note the dummy argument.** These are propositions, not predicates, but
> pytholog raises `IndexError` on 0-arity terms — so the KB is written
> `c(x) :- a(x), b(x)`. The `.pl` file uses plain propositions.

### 🎯 Which chaining, and why

| Scenario | Use | Because |
|---|---|---|
| A sensor reading arrives; what does it imply? | **Forward** | few facts, many possible conclusions |
| Does this patient have malaria? | **Backward** | many facts, **one** question |
| Monitoring a plant for alarm conditions | **Forward** | you want every consequence, continuously |
| Diagnosing why a car will not start | **Backward** | test only the hypotheses that matter |

The deciding question is: **how many possible conclusions, and how many facts?**
Prolog is backward chaining with depth-first search — which is why a
left-recursive rule loops for ever, closing the circle back to Experiment 1.

### Experiment 17 — the expert system, and its explanation facility

Working memory: `fever`, `cough`, `fatigue`.

```
?- viral(patient)         -> Yes
?- flu(patient)           -> Yes
?- rest_advised(patient)  -> Yes
?- bacterial(patient)     -> not derivable (no rash recorded)
```

**The explanation, reconstructed from the derivation:**

```
HOW did you conclude rest_advised(patient)?
  by rule  rest_advised(X) :- flu(X)
  flu(patient)     by  flu(X) :- viral(X), fatigue(X)
    viral(patient) by  viral(X) :- fever(X), cough(X)
      fever(patient)   -- a fact in working memory
      cough(patient)   -- a fact in working memory
    fatigue(patient)   -- a fact in working memory
```

### 🎯 This is the whole argument for expert systems

**The chain *is* the explanation, and it falls out of the proof for free.** A
neural network can tell you `flu` with 0.94 confidence and nothing else. Add
`rash` to working memory and `bacterial(patient)` becomes derivable — the
system's conclusions change *and it can say which fact changed them*.

That is the sentence to put in the Unit 5 answer, and it is also the honest
limit: an expert system knows only what someone wrote down.

---

## Experiment 18 — A DCG grammar for English

`18_dcg.pl` ·
`07_bayes_and_local_search.py`

pytholog does not parse `-->`, so the Python half runs the equivalent recursive
descent and the `.pl` file carries the real DCG.

```
'the big cat chases a mouse' parses:

  S
    NP
      Det  the
      Adj  big
      N    cat
    VP
      V    chases
      NP
        Det  a
        N    mouse

'the dog sleeps'  parses   (VP -> V, intransitive)
'cat the chases'  does NOT parse
```

### 📖 What a DCG actually is

**A DCG compiles to exactly this recursive descent**, with the token list
threaded through as **difference lists**. `s --> np, vp.` expands to
`s(S0, S) :- np(S0, S1), vp(S1, S).` — the grammar is written as inference
rules, so this experiment is Unit 4's machinery applied to language. That is
why it sits in an AI course rather than a compilers course.

---

## Experiment 19 — Deterministic Naive Bayes

`19_naive_bayes.pl` ·
`07_bayes_and_local_search.py`

The 14-day play-tennis table: **9 play, 5 do not**.

Query `(sunny, cool, high, strong)`:

| Class | P(class) × likelihoods |
|---|---:|
| yes | 0.005291 |
| **no** | **0.020571** ← larger |

**Normalised: no 79.54%, yes 20.46%.**

### 🎯 The cross-course check

**These are Course 8's numbers and Course 12 A's numbers.** Three courses,
three implementations — WEKA-equivalent scikit-learn in Course 8, `GaussianNB`
and a hand calculation in Course 12 A, and this — and the same
0.005291 / 0.020571. **If they ever disagree, one of them is wrong**, and
`tools/verify_all.sh` says so.

### ⚠️ Zero frequency vetoes a class

```
'overcast' appears 0 times with play=no
  P(no | overcast, ...) without smoothing = 0.0
  with Laplace (+1, 3 outlook values)     = 0.044643
```

**A single zero vetoes the class whatever the other three features say**,
because the likelihood is a **product**. Laplace smoothing adds 1 to every
count and 3 (the number of outlook values) to every denominator.

---

## The unit-3 extras that share `07_bayes_and_local_search.py`

The syllabus lists hill climbing, simulated annealing and genetic algorithms in
Unit 3 but prescribes **no experiment** for them. They are verified anyway,
because §3.5–3.7 quote numbers.

### 🔢 Hill climbing gets stuck 48% of the time

On a landscape with a local peak near x = 2 and the global near x = 8:

| From 21 starting points | Count |
|---|---:|
| reached the **global** maximum | **11** |
| stuck on the **local** maximum | **10 (48%)** |

**Hill climbing is complete only with random restarts.** If each try succeeds
with probability p, expected restarts = 1/p — here about **1.9**.

### 🔢 Simulated annealing, as the acceptance probability

P(accept a move that is 1.0 worse) = e^(−1/T):

| T | P |
|---:|---:|
| 100.0 | **0.990050** |
| 10.0 | 0.904837 |
| 1.0 | **0.367879** |
| 0.1 | **0.000045** |

**T high: it accepts almost anything and explores. T → 0: it accepts nothing
worse and becomes hill climbing.** Annealing is a scheduled slide from random
walk to hill climbing, which is exactly why it escapes local maxima — and the
four numbers make "cooling schedule" concrete.

### 🔢 Genetic algorithms — fitness and the crossover trap

Fitness = non-attacking pairs, maximum C(8,2) = **28**:

| Board | Fitness |
|---|---:|
| a valid solution `(0,4,7,5,2,6,1,3)` | **28** |
| all queens on one row | **0** |
| a middling one | 24 |

Crossover at position 3:

```
(2,4,7, 4,8,5,5,2) + (3,2,7, 5,2,4,1,1)  ->  (2,4,7, 5,2,4,1,1)
```

**Crossover preserves contiguous blocks.** It helps only if neighbouring genes
form a partial solution; with a badly ordered representation it is just noise,
and the GA degenerates into an expensive random search. **That is the
criticism to raise** when the exam asks you to evaluate genetic algorithms.

---

## What the runner asserts

| Script | Experiments | Real resolution? |
|---|---|---|
| `01_family_tree.py` | 1 | **Yes** — `ancestor/2` is genuinely recursive |
| `02_lists_and_arithmetic.py` | 2–7 | No — proves the limit, then Python |
| `03_uninformed_search.py` | 8–11 | No — search, not logic |
| `04_informed_search.py` | 12 | No |
| `05_csp_backtracking.py` | 13, 14 | No |
| `06_logic_and_chaining.py` | 15–17 | **Yes** — 16 and 17 resolve |
| `07_bayes_and_local_search.py` | 18, 19 + unit-3 extras | No |

Plus the Prolog audit: **16 files, every one carrying `*** NOT EXECUTED ***`**.
If someone deletes that marker without running the file, the suite fails —
which is the point. The claim "this was verified" is never made by accident.

---

## Lab examination

Two hours in SWiSH, one experiment number, then a viva.

**What costs marks:**

- Writing `ancestor/2` left-recursively and hanging the interpreter
- `sibling/2` without the `X \= Y` guard — asha becomes her own sibling
- `max([], 0)` as the base case — wrong for negative numbers
- Using `=` where you meant `is` — `X = 2 + 3` binds X to the **term** `2+3`
- Reporting BFS as "optimal" without saying **"when step costs are equal"**
- Claiming A* is optimal without naming **admissibility**
- Saying `\+ bird(kiwi)` means a kiwi is not a bird
- Quoting "92 solutions" for N-Queens with no board size attached

**What earns them:**

- **`append(X, Y, [a,b,c])` giving four solutions.** One definition,
  concatenation and splitting both, because a rule is a relation.
- **Quoting A\* against UCS: 418 either way, 6 nodes against 13.** A number
  beats an adjective.
- **Showing the inadmissible heuristic being *faster*.** 4 expansions, 450 km.
  It demonstrates you know what the guarantee actually buys.
- **"h2 dominates h1"**, with 6 against 14 on a scrambled board — the right
  vocabulary for comparing heuristics.
- **"Variables fail fast, values fail late"** for MRV and LCV, with the
  NT-has-2-values table behind it.
- **Printing the explanation chain** for the expert system, and saying that is
  what a neural network cannot do.
- **Naming the closed-world assumption** when you use `\+`.
- **Saying when a heuristic did not help.** MRV saved **zero** backtracks on
  Australia. Reporting that honestly is worth more than pretending otherwise.
