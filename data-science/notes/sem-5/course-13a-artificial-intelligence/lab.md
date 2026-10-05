# Practical Lab

**19 experiments**, each set out as 1. Question, 2. Aim, 3. Steps, 4. Programme, 5. Execution and
Results. The syllabus names **SWI-Prolog** and adds *"environment for practice without
installation"* — meaning [swish.swi-prolog.org](https://swish.swi-prolog.org/),
which runs in a browser.

Code lives in `labs/course-13a-ai/`.

## Read this before you read anything else

**Every Prolog file here runs, in SWI-Prolog 9.0.4.** Each experiment has two halves:

| Half | Files | Status |
|---|---|---|
| **The Prolog you submit** | **16 `.pl` files** | **Run in SWI-Prolog**: each is consulted, and every `?-` query it shows is asked, by `tools/data-science/prolog_lab.py` |
| **The check** | **7 `.py` files** | **Executed and asserted** by `tools/data-science/run_ai_labs.py`, which also runs the `.pl` files and checks that SWI-Prolog gives the same answers |

*(Updated October 2026: SWI-Prolog could not be installed where these labs are checked, and every
`.pl` file said NOT EXECUTED. It now installs from the Ubuntu archive. Running the files found
five faults, each corrected in its file and noted below: a warning on loading
`07_cut_fail.pl`, another on loading `15_logic.pl` under a non-UTF-8 locale,
`compare_searches/2` printing four comparisons, the expert system's explanation calling every
fact a rule, and forward chaining that existed only as a comment.)*

**The `.pl` file is the deliverable.** It is what you paste into SWISH and what
the examiner marks. Under **5. Execution and Results** is what SWI-Prolog answered: the
toplevel waits for a key between answers, so the queries were asked by `prolog_lab.py`, which
prints every answer as the toplevel does — `X = asha ;` for each and a full stop after the last
— and, past eight answers, the first and how many there are.

```bash
bash tools/data-science/setup_prolog.sh          # SWI-Prolog, from the Ubuntu archive
pip install -r tools/requirements.txt
python3 tools/data-science/run_ai_labs.py
```

Output ends:

```
  16 Prolog programs run
  they cover experiments: [1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19]
  (08_graph_search.pl covers experiments 8-11, which are one graph)

==============================================================
7 lab programs executed and asserted, 0 failed
covering all 19 prescribed experiments
```

**Nineteen experiments, sixteen files** because experiments 8–11 are one graph
asked four ways — represent it, DFS it, BFS it, compare the path lengths — so
they share `08_graph_search.pl`, and one section below.

<div class="warn" markdown="1">
<span class="label">IN THE PYTHON CHECK, FIVE EXPERIMENTS RUN AS REAL LOGIC PROGRAMS</span>

`pytholog` is a small Prolog engine on PyPI. It performs
**genuine SLD resolution** over facts and recursive rules, so in the Python half experiments **1,
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

That last row is the important one, and Experiment 1 below spends real space
on it. **The `.pl` file uses the idiomatic nested form, and SWI-Prolog
answers it correctly** — its answers are shown there. The engine limitation is documented, not
hidden.
</div>

---

## Experiment 1 — A family tree

### 1. Question

Represent a family tree in Prolog, with rules for father, mother, grandparent, ancestor, sibling and cousin.

### 2. Aim

State the facts, write the rules — one of them recursive — and query them.

### 3. Steps

**In SWI-Prolog**, `01_family_tree.pl`:

1. **State the facts.**
2. **Write the rules.**
3. **Ask the queries.**

**The Python check**, `01_family_tree.py`, through pytholog's resolution:

1. **State the facts and simple rules.**
2. **Resolve the recursive ancestor/2.**
3. **Put the base case first.**
4. **Guard sibling/2 against X = Y.**
5. **Count one solution per proof.**
6. **Find cousins, and pytholog's limit.**

<div class="formula" markdown="1">
<span class="label">THE TREE</span>

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
</div>


### 4. Programme

**In SWI-Prolog**, `01_family_tree.pl`:

{{programme: course-13a-ai/01_family_tree.pl}}

**The Python check**, `01_family_tree.py`, through pytholog's resolution:

{{programme: course-13a-ai/01_family_tree.py}}

### 5. Execution and Results

**In SWI-Prolog**, `01_family_tree.pl`:

{{output: course-13a-ai/01_family_tree.pl}}

**The Python check**, `01_family_tree.py`, through pytholog's resolution:

{{output: course-13a-ai/01_family_tree.py}}

<div class="example" markdown="1">
<span class="label">THREE THINGS THIS EXPERIMENT TEACHES THAT THE SYLLABUS DOES NOT SAY</span>

**1. Clause order is semantics, not style.** Put the base case first:

```prolog
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
```

Write it left-recursively — `ancestor(X,Y) :- ancestor(X,Z), parent(Z,Y).` — and the
query never reaches a parent fact. The logic is identical; the *procedure* is not, because
Prolog is backward chaining with **depth-first** search. **Corrected:** this page said
SWI-Prolog "loops for ever". Run here, SWI-Prolog 9.0.4 stops after about 6.3 million nested
calls and nine seconds with `Stack limit (1.0Gb) exceeded … Probable infinite recursion
(cycle)`.

**2. `sibling/2` needs a guard.** Without `X \= Y`:

```
sibling(asha, X)  with the guard -> ['ravi']
without the guard                -> ['asha', 'ravi']   <- asha is her own sibling
```

Every `parent(P,X), parent(P,Y)` pair unifies with `X = Y` unless you forbid it.

**3. One solution per *proof*, not per answer.** SWI-Prolog answers `sibling(asha, X)` with
`X = ravi` twice: `asha` and `ravi` share **both** `ram` and `sita`, so the goal succeeds
twice — once down each parent. `setof/3` collapses it to `[ravi]`. This is a property of
resolution, not a bug, and examiners like the answer. `cousin(kiran, X)` gives `bhanu` twice
for the same reason: the parents' `sibling/2` succeeds twice.
</div>

<div class="warn" markdown="1">
<span class="label">WHERE PYTHOLOG GETS COUSIN/2 WRONG</span>

| Formulation | Answer for `cousin(kiran, X)` |
|---|---|
| **Flat** — parents' sibling's children, inline | **`['bhanu']`** — correct |
| **Nested** — calls a derived `sib/2` | `['bhanu', 'kiran', 'meena']` — **wrong** |

`kiran` is not his own cousin, and `meena` is his **sister**. pytholog does not
propagate the inequality guard correctly through a nested derived predicate.
**SWI-Prolog answers the nested form correctly** — only `bhanu`, above — and the `.pl` file
uses it because it is the idiomatic encoding. This is an **engine** limitation.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

ancestor(ram, X) gives five answers, the three below his children only through the recursive clause; sibling(asha, X) and cousin(kiran, X) each answer twice, once per proof.
</div>


## Experiment 2 — member, append, reverse and length

### 1. Question

Write list predicates in Prolog: member, append, reverse and length.

### 2. Aim

Define the four predicates recursively, and run append/3 backwards.

### 3. Steps

**In SWI-Prolog**, `02_lists.pl`:

1. **Define member/2.**
2. **Define append/3.**
3. **Define reverse/2, with an accumulator.**
4. **Define length/2.**
5. **Ask the queries.**
6. **Run append/3 backwards.**

**The Python check**, `02_lists_and_arithmetic.py`, for experiments 2–7:

1. **Prove pytholog's limits first.**
2. **Experiment 2: the list predicates.**
3. **Experiment 3: the maximum.**
4. **Experiment 4: flatten.**
5. **Experiments 5 and 6: factorial, Fibonacci and GCD.**
6. **Experiment 7: cut, fail and negation.**

<div class="formula" markdown="1">
<span class="label">THE PREDICATES</span>

| Goal | Result |
|---|---|
| `member(b, [a,b,c])` | true |
| `append([a,b,c], [d,e], X)` | `[a,b,c,d,e]` |
| `reverse([a,b,c], X)` | `[c,b,a]` |
| `length([a,b,c], N)` | `3` |

The file names them `mem/2`, `app/3`, `rev/2` and `len/2`, so they do not clash with the
built-in predicates of the same names.

pytholog has neither list terms nor arithmetic evaluation, and the Python check
**asserts both failures first** — `mem(b, [a,b,c]) -> ['No']` and
`fact(5, X) -> ['No']` — before checking the logic of experiments 2–7 in Python.
</div>


### 4. Programme

**In SWI-Prolog**, `02_lists.pl`:

{{programme: course-13a-ai/02_lists.pl}}

**The Python check**, `02_lists_and_arithmetic.py`, for experiments 2–7:

{{programme: course-13a-ai/02_lists_and_arithmetic.py}}

### 5. Execution and Results

**In SWI-Prolog**, `02_lists.pl`:

{{output: course-13a-ai/02_lists.pl}}

**The Python check**, `02_lists_and_arithmetic.py`, for experiments 2–7:

{{output: course-13a-ai/02_lists_and_arithmetic.py}}

<div class="example" markdown="1">
<span class="label">THE ANSWER THAT EARNS THE MARKS</span>

**`append/3` runs backwards.** SWI-Prolog's four answers to `app(X, Y, [a,b,c])`, above, are
every way to split the list: one definition both concatenates and splits,
because a Prolog rule states a **relation**, not a function. A Python
`append()` can never do this. If the viva asks "what makes Prolog different",
this is the two-line answer.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

append(X, Y, [a,b,c]) has four solutions: one definition both concatenates and splits.
</div>


## Experiment 3 — The maximum of a list

### 1. Question

Find the maximum element of a list.

### 2. Aim

Define max_list/2 recursively, from the right base case.

### 3. Steps

1. **Define max_list/2, from a one-element base case.**
2. **Ask the query.**

<div class="formula" markdown="1">
<span class="label">THE BASE CASE</span>

For `max/2` the base case is the **one-element** list, not the empty one —
`max([], M)` has no answer, and writing `max([], 0)` is wrong for negative
numbers.
</div>


### 4. Programme

{{programme: course-13a-ai/03_maximum.pl}}

### 5. Execution and Results

{{output: course-13a-ai/03_maximum.pl}}

The Python check for this experiment, `02_lists_and_arithmetic.py`, is shown in full under Experiment 2, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

max_list([3,7,2,9,4], M) gives M = 9.
</div>


## Experiment 4 — Flatten a nested list

### 1. Question

Flatten a nested list into a single-level list.

### 2. Aim

Define flatten/2 in three clauses: the empty list, a list head and an atom.

### 3. Steps

1. **Define flatten/2 in three clauses.**
2. **Ask the query.**

<div class="formula" markdown="1">
<span class="label">THE THREE CLAUSES</span>

For `flatten/2` there are three clauses: empty list, list head
(recurse and append), atom head (keep). **Empty sublists disappear** —
`flatten([[], [[]], 1])` gives `[1]`, which is the case people forget. The Python check
asserts both.
</div>


### 4. Programme

{{programme: course-13a-ai/04_flatten.pl}}

### 5. Execution and Results

{{output: course-13a-ai/04_flatten.pl}}

The Python check for this experiment, `02_lists_and_arithmetic.py`, is shown in full under Experiment 2, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

flatten([1,[2,[3,4],5],[[6]],7], X) gives [1, 2, 3, 4, 5, 6, 7].
</div>


## Experiment 5 — Factorial and Fibonacci

### 1. Question

Compute factorial and Fibonacci numbers by recursion.

### 2. Aim

Define fact/2 and fib/2 with is/2, see why the naive fib/2 is slow, and make it linear.

### 3. Steps

1. **Define factorial.**
2. **Define Fibonacci.**
3. **Ask the queries.**
4. **Make Fibonacci linear with an accumulator.**

<div class="formula" markdown="1">
<span class="label">THE NUMBERS</span>

```
factorial 0..5 -> [1, 1, 2, 6, 24, 120]
fibonacci 0..9 -> [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
naive fib(10) makes 177 recursive calls
```

**177 calls for `fib(10)`** is the number to quote: the naive Prolog definition
is exponential for exactly the reason the Python one is. The fix is an
accumulator, or `assertz/1` to memoise — Prolog's dynamic programming.
</div>


### 4. Programme

{{programme: course-13a-ai/05_factorial_fib.pl}}

### 5. Execution and Results

{{output: course-13a-ai/05_factorial_fib.pl}}

**Added:** nothing in the file asked for its accumulator version, `fib_fast/2`; the query
above runs it. `fib_fast(30, F)` answers at once, where the naive `fib(30, F)` makes 2,692,537
calls.

The Python check for this experiment, `02_lists_and_arithmetic.py`, is shown in full under Experiment 2, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

fact(5, F) gives 120 and fib(10, F) gives 55; fib_fast(30, F) gives 832040 at once.
</div>


## Experiment 6 — GCD by recursion

### 1. Question

Find the greatest common divisor of two numbers by recursion.

### 2. Aim

Define gcd/3 by Euclid's algorithm, and see why it terminates.

### 3. Steps

1. **Define gcd/3, by Euclid.**
2. **Ask the queries.**

<div class="formula" markdown="1">
<span class="label">THE TRACE</span>

```
gcd(48, 18) = 6   trace: (48,18) -> (18,12) -> (12,6) -> 6
gcd(17, 5)  = 1   (coprime)
```

Each step replaces (A, B) with (B, A mod B), and B strictly decreases, so termination is
guaranteed.
</div>


### 4. Programme

{{programme: course-13a-ai/06_gcd.pl}}

### 5. Execution and Results

{{output: course-13a-ai/06_gcd.pl}}

The Python check for this experiment, `02_lists_and_arithmetic.py`, is shown in full under Experiment 2, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

gcd(48, 18, G) gives 6; gcd(17, 5, G) gives 1.
</div>


## Experiment 7 — Cut and fail

### 1. Question

Demonstrate the cut (!) and fail.

### 2. Aim

Write the cut-fail idiom, tell a green cut from a red one, and negate by failure.

### 3. Steps

1. **State the facts.**
2. **Write the cut-fail rule.**
3. **Tell a green cut from a red one.**
4. **Negate by failure.**

<div class="formula" markdown="1">
<span class="label">THE CONSTRUCTS</span>

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
</div>


### 4. Programme

{{programme: course-13a-ai/07_cut_fail.pl}}

### 5. Execution and Results

{{output: course-13a-ai/07_cut_fail.pl}}

**Corrected:** `bird(pingu)` came after `penguin(pingu)`, so the clauses of `bird/1` were
not together, and SWI-Prolog warned *"Clauses of bird/1 are not together in the source-file"*
on loading. They are together now, and the file loads silently.

<div class="concept" markdown="1">
<span class="label">GREEN CUT AND RED CUT</span>

- **Green cut** — removes only redundant choice points. Delete it and nothing
  changes but speed.
- **Red cut** — changes the **meaning**. Delete it and the answers change.

The cut is where Prolog stops being pure logic: clause order and cut placement
become semantically load-bearing, which is why it is the hardest thing to
debug.
</div>

<div class="warn" markdown="1">
<span class="label">\+ IS NOT LOGICAL NEGATION</span>

```
known birds: ['polly', 'tweety'], known penguins: ['pingu']
\+ penguin(tweety)  succeeds  -- tweety is not known to be one
\+ bird(kiwi)       succeeds  -- but we simply do not know
```

Prolog assumes a **closed world**: anything not derivable is false. Logical
negation would require *proving* the fact untrue. A kiwi is a bird.
</div>

The Python check for this experiment, `02_lists_and_arithmetic.py`, is shown in full under Experiment 2, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

fly(tweety) is true and fly(pingu) is false: the first clause commits and fails, so the second is never tried.
</div>


## Experiments 8–11 — A graph, DFS, BFS, and the comparison

### 1. Question

Experiment 8: represent a graph as facts. Experiment 9: search it depth-first. Experiment 10: search it breadth-first. Experiment 11: compare the paths they find.

### 2. Aim

State one graph, search it both ways, and see that DFS finds the long way round and BFS the short one.

### 3. Steps

**In SWI-Prolog**, `08_graph_search.pl`:

1. **Experiment 8: state the graph as edge/2 facts.**
2. **Experiment 9: search depth-first.**
3. **Experiment 10: search breadth-first, with a queue.**
4. **Experiment 11: compare the paths.**

**The Python check**, `03_uninformed_search.py`, for experiments 8–11:

1. **Compare BFS, DFS and uniform cost on the Romania map.**
2. **See uniform cost as Dijkstra.**
3. **Run DFS and BFS on the six-node graph.**
4. **Make one step cost more.**
5. **Count iterative deepening's extra nodes.**

<div class="formula" markdown="1">
<span class="label">THE ROMANIA RUN</span>

Four experiments, one graph. The Python check runs both on the **Romania map**
from Russell & Norvig (20 cities, real distances) and on a six-node graph built
to make one specific point.

**The Romania run — the table to memorise:**

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
</div>


### 4. Programme

**In SWI-Prolog**, `08_graph_search.pl`:

{{programme: course-13a-ai/08_graph_search.pl}}

**The Python check**, `03_uninformed_search.py`, for experiments 8–11:

{{programme: course-13a-ai/03_uninformed_search.py}}

### 5. Execution and Results

**In SWI-Prolog**, `08_graph_search.pl`:

{{output: course-13a-ai/08_graph_search.pl}}

**The Python check**, `03_uninformed_search.py`, for experiments 8–11:

{{output: course-13a-ai/03_uninformed_search.py}}

In SWI-Prolog, `dfs/3` and `bfs/3` each find both paths: pressing `;` after DFS's long way
gives the short one, and the other way round for BFS. **The order is the difference.**
**Corrected:** `compare_searches/2` let both backtrack, so it printed four comparisons and
succeeded four times; it now takes the first path each finds, with `once/1`, and prints one.

<div class="example" markdown="1">
<span class="label">UCS IS DIJKSTRA</span>

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
</div>

**The six-node graph — same work, twice the path:**

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

<div class="example" markdown="1">
<span class="label">AND THE COUNTEREXAMPLE THAT KILLS "BFS IS OPTIMAL"</span>

| Step costs | BFS cost | UCS cost |
|---|---:|---:|
| all 1 | 2 | 2 — **equal** |
| make `c→g` cost 50 | **51** (a → c → g) | **4** (a → b → d → e → g) |

**BFS counts edges, not cost.** With equal step costs those are the same thing,
so BFS is optimal. The moment they differ it is not — and the gap here is
51 against 4.
</div>

<div class="example" markdown="1">
<span class="label">ITERATIVE DEEPENING COSTS 11.1%</span>

With branching factor **b = 10** and depth **d = 5**:

| | Nodes generated | Memory |
|---|---:|---|
| BFS | **111,111** | O(b^d) = 100,000 |
| IDS | **123,456** | **O(bd) = 50** |

**11.1% more nodes for 2,000× less memory.** The repetition is cheap because
the bottom level holds most of the nodes, so regenerating everything above it
costs almost nothing. IDS is the preferred uninformed search when the depth is
unknown — and 111,111 / 123,456 are pleasing enough to remember.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

DFS finds a → b → d → e → g (5 nodes) first, BFS a → c → g (3); on the Romania map neither finds the optimal 418 km, which uniform cost does.
</div>


## Experiment 12 — Greedy Best-First and A*

### 1. Question

Search the Romania map with Greedy Best-First search and A*.

### 2. Aim

Run A* with the straight-line heuristic, compare it with greedy and uniform cost, and check the heuristic is admissible.

### 3. Steps

**In SWI-Prolog**, `12_astar.pl`:

1. **State the map.**
2. **State the heuristic.**
3. **Search with A*.**
4. **Ask the query.**

**The Python check**, `04_informed_search.py`, for experiment 12:

1. **Compare uniform cost, greedy and A*.**
2. **See why greedy goes wrong.**
3. **Run A* with h = 0.**
4. **Inflate the heuristic.**
5. **Check admissibility at every city.**
6. **Compare the 8-puzzle heuristics.**

<div class="formula" markdown="1">
<span class="label">THE HEADLINE</span>

**The single most quotable result in the course:**

| Search | f(n) | Expanded | Cost | Optimal? |
|---|---|---:|---:|---|
| Uniform cost | g(n) | 13 | **418** | YES |
| Greedy best-first | h(n) | **4** | 450 | NO |
| **A\*** | **g(n) + h(n)** | **6** | **418** | **YES** |

**A\* found the optimal 418 expanding 6 nodes where UCS needed 13.** Same
answer, less than half the work. That one sentence is why heuristics exist.
</div>


### 4. Programme

**In SWI-Prolog**, `12_astar.pl`:

{{programme: course-13a-ai/12_astar.pl}}

**The Python check**, `04_informed_search.py`, for experiment 12:

{{programme: course-13a-ai/04_informed_search.py}}

### 5. Execution and Results

**In SWI-Prolog**, `12_astar.pl`:

{{output: course-13a-ai/12_astar.pl}}

**The Python check**, `04_informed_search.py`, for experiment 12:

{{output: course-13a-ai/04_informed_search.py}}

In SWI-Prolog, `astar/4` gives 418 first; press `;` and it goes on to the other routes **in
order of cost** — 450, 575, 605, 607 and 762 — because the queue is always sorted by
f = g + h.

**Why greedy goes wrong, in two numbers.** At Sibiu, greedy compares `h` only:

```
h(Fagaras)        = 176   <- looks closer, so it goes here
h(Rimnicu Vilcea) = 193
```

but the actual routes are **450 km via Fagaras** and **418 km via Rimnicu** —
32 km shorter. **Fagaras is closer as the crow flies and further by road.**
Greedy is short-sighted because it ignores `g(n)`, the cost already paid, which
is precisely what A* adds back.

<div class="example" markdown="1">
<span class="label">A* WITH h = 0 IS UNIFORM COST SEARCH</span>

```
A* with h(n) = 0: expanded 13, cost 418
uniform cost    : expanded 13, cost 418
```

**Identical, not merely similar.** A* sits between UCS (no information,
optimal) and greedy (maximum information, used badly, not optimal).
</div>

<div class="warn" markdown="1">
<span class="label">AN INADMISSIBLE HEURISTIC IS FASTER AND WRONG</span>

| Heuristic | Expanded | Cost | Optimal? |
|---|---:|---:|---|
| straight-line (admissible) | 6 | **418** | YES |
| straight-line **× 2** | **4** | 450 | **NO** |
| straight-line **× 5** | **4** | 450 | **NO** |

Overestimating makes the node on the optimal path *look* worse than an
alternative, so A* commits to a goal before the better path is explored. **The
guarantee is gone the moment h(n) > h\*(n) anywhere** — and the price here is
2 fewer expansions for 32 extra kilometres.
</div>

**Admissibility, checked rather than assumed:**

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

**8-puzzle: h2 dominates h1:**

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

<div class="concept" markdown="1">
<span class="label">RESULT</span>

A* finds the optimal 418 km expanding 6 nodes where uniform cost needs 13; greedy expands 4 and finds 450.
</div>


## Experiment 13 — Map colouring

### 1. Question

Colour a map so that no two neighbouring regions share a colour, as a constraint satisfaction problem.

### 2. Aim

Colour Australia's seven regions with three colours by backtracking, and see why two are not enough.

### 3. Steps

**In SWI-Prolog**, `13_map_colouring.pl`:

1. **State the colours.**
2. **Write the constraints.**
3. **Ask the query.**

**The Python check**, `05_csp_backtracking.py`, for experiments 13 and 14:

1. **Colour the map.**
2. **Try two colours.**
3. **Order by MRV and LCV.**
4. **Solve 8-Queens.**
5. **Count the solutions for each board size.**

<div class="formula" markdown="1">
<span class="label">THE COLOURING</span>

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
</div>


### 4. Programme

**In SWI-Prolog**, `13_map_colouring.pl`:

{{programme: course-13a-ai/13_map_colouring.pl}}

**The Python check**, `05_csp_backtracking.py`, for experiments 13 and 14:

{{programme: course-13a-ai/05_csp_backtracking.py}}

### 5. Execution and Results

**In SWI-Prolog**, `13_map_colouring.pl`:

{{output: course-13a-ai/13_map_colouring.pl}}

**The Python check**, `05_csp_backtracking.py`, for experiments 13 and 14:

{{output: course-13a-ai/05_csp_backtracking.py}}

SWI-Prolog's first answer is the colouring above; there are 18 in all, three choices for
Tasmania, which touches nothing, times six for the mainland.

**With only two colours: no solution, after 4 backtracks.** The reason is structural:
**`WA`, `NT` and `SA` are mutually adjacent** — a triangle needs three colours. The search
discovers this by exhausting every possibility, which is what "no solution" *means* in a CSP.

<div class="example" markdown="1">
<span class="label">MRV AND LCV PULL IN OPPOSITE DIRECTIONS, AND THAT IS CORRECT</span>

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
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

WA red, NT green, SA blue, Q red, NSW green, V red, T red — the first of 18 colourings; with two colours there is none.
</div>


## Experiment 14 — N-Queens

### 1. Question

Place N queens on an N × N board so that no two attack each other.

### 2. Aim

Place the queens as a permutation, check only the diagonals, and count the solutions.

### 3. Steps

1. **Place the queens as a permutation.**
2. **Check the diagonals.**
3. **Ask the queries.**

<div class="formula" markdown="1">
<span class="label">THE BOARD</span>

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

The Python check counts rows from 0; SWI-Prolog's first answer, `[1, 5, 8, 6, 3, 7, 2, 4]`,
is the same board counted from 1.
</div>


### 4. Programme

{{programme: course-13a-ai/14_n_queens.pl}}

### 5. Execution and Results

{{output: course-13a-ai/14_n_queens.pl}}

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

SWI-Prolog prints the list of all 92 abbreviated, with `|...`: the toplevel shortens long
answers, and `N = 92` is the part to read.

The Python check for this experiment, `05_csp_backtracking.py`, is shown in full under Experiment 13, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

queens(8, Qs) gives [1, 5, 8, 6, 3, 7, 2, 4] first, and there are 92.
</div>


## Experiment 15 — Facts and rules in propositional and first-order logic

### 1. Question

Encode facts and rules in propositional and first-order logic.

### 2. Aim

Encode a propositional rule and a first-order one, and check truth tables, validity and entailment.

### 3. Steps

**In SWI-Prolog**, `15_logic.pl`:

1. **Encode a propositional fact and rule.**
2. **Encode first-order facts and one rule.**

**The Python check**, `06_logic_and_chaining.py`, for experiments 15–17:

1. **Experiment 15: the truth tables.**
2. **Show P ⇒ Q is ¬P ∨ Q.**
3. **Test validity, satisfiability and entailment.**
4. **Check modus ponens and modus tollens.**
5. **Experiment 16: chain forward.**
6. **Chain backward, by resolution.**
7. **Choose between them.**
8. **Experiment 17: run the expert system.**
9. **See the closed world.**

<div class="formula" markdown="1">
<span class="label">THE TRUTH TABLE</span>

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
</div>


### 4. Programme

**In SWI-Prolog**, `15_logic.pl`:

{{programme: course-13a-ai/15_logic.pl}}

**The Python check**, `06_logic_and_chaining.py`, for experiments 15–17:

{{programme: course-13a-ai/06_logic_and_chaining.py}}

### 5. Execution and Results

**In SWI-Prolog**, `15_logic.pl`:

{{output: course-13a-ai/15_logic.pl}}

**The Python check**, `06_logic_and_chaining.py`, for experiments 15–17:

{{output: course-13a-ai/06_logic_and_chaining.py}}

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

**Corrected:** the file's comments use logic symbols (∀ ⇒ ∧), and under a non-UTF-8 locale
SWI-Prolog warned *"Illegal multibyte Sequence"* on loading it. It now begins with
`:- encoding(utf8).`

<div class="concept" markdown="1">
<span class="label">RESULT</span>

wet_ground is proved by modus ponens; passes/1 holds for asha and meena; {P, P⇒Q} ⊨ Q.
</div>


## Experiment 16 — Forward and backward chaining

### 1. Question

Implement forward and backward chaining.

### 2. Aim

Chain backward, as Prolog does, and forward, written out with assertz/1, from the same rules.

### 3. Steps

1. **State the rule base.**
2. **Chain backward.**
3. **Chain forward.**
4. **Ask for a goal nothing defines.**

<div class="formula" markdown="1">
<span class="label">THE TWO DIRECTIONS</span>

**Forward**, from `{a, b}` and 3 rules:

```
derived, in order: ['c', 'd', 'e']
final KB:          ['a', 'b', 'c', 'd', 'e']
```

**Backward**, the same rule base: to prove `e` it needs `d`, which needs `c`, which needs `a`
and `b` — and it **never derives anything outside that chain**. Forward chaining derives
everything derivable whether or not it was wanted.
</div>


### 4. Programme

{{programme: course-13a-ai/16_chaining.pl}}

### 5. Execution and Results

{{output: course-13a-ai/16_chaining.pl}}

**Corrected:** forward chaining, `forward/0`, was only a comment in the file, so it could
not be run. It is now code, with the same three rules written as `rule/2` facts, and the query
above runs it.

**Corrected:** this page said that for a goal nothing defines, SWI-Prolog "answers false"
where pytholog raises an error. SWI-Prolog raises an error too, as `z(X)` above shows: an
existence error, because no clause for `z/1` exists at all.

The Python check's backward chaining is through pytholog's real resolution:

```
?- c(x).  -> Yes
?- d(x).  -> Yes
?- e(x).  -> Yes
?- z(x).  -> TypeError
```

> **Note the dummy argument.** These are propositions, not predicates, but
> pytholog raises `IndexError` on 0-arity terms — so the KB is written
> `c(x) :- a(x), b(x)`.

<div class="example" markdown="1">
<span class="label">WHICH CHAINING, AND WHY</span>

| Scenario | Use | Because |
|---|---|---|
| A sensor reading arrives; what does it imply? | **Forward** | few facts, many possible conclusions |
| Does this patient have malaria? | **Backward** | many facts, **one** question |
| Monitoring a plant for alarm conditions | **Forward** | you want every consequence, continuously |
| Diagnosing why a car will not start | **Backward** | test only the hypotheses that matter |

The deciding question is: **how many possible conclusions, and how many facts?**
Prolog is backward chaining with depth-first search — which is why a
left-recursive rule never reaches an answer, closing the circle back to Experiment 1.
</div>

The Python check for this experiment, `06_logic_and_chaining.py`, is shown in full under Experiment 15, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

Backward, e(X) is proved through d and c; forward, from {a, b}, c, d and e are derived and the knowledge base is [a, b, c, d, e].
</div>


## Experiment 17 — An expert system, and its explanation facility

### 1. Question

Build a rule-based expert system that explains its conclusions.

### 2. Aim

Write a knowledge base and working memory, explain a conclusion from its proof, and add a fact.

### 3. Steps

1. **Write the knowledge base.**
2. **Record the working memory.**
3. **Explain a conclusion.**
4. **Add a fact, and ask again.**

<div class="formula" markdown="1">
<span class="label">THE CASE</span>

Working memory: `fever`, `cough`, `fatigue`.

```
?- viral(patient)         -> Yes
?- flu(patient)           -> Yes
?- rest_advised(patient)  -> Yes
?- bacterial(patient)     -> not derivable (no rash recorded)
```
</div>


### 4. Programme

{{programme: course-13a-ai/17_expert_system.pl}}

### 5. Execution and Results

{{output: course-13a-ai/17_expert_system.pl}}

**The explanation is reconstructed from the derivation**, as above: each rule, then the
facts it rests on.

**Corrected:** `explain/2` printed every fact as `fever(patient)  because:`, with nothing under
it. A fact is a clause whose body is `true`, so `clause/2` matched facts in the rule clause too.
The rule clause now requires a real body, and the fact clause looks for `true`, so the facts
read *"a fact in working memory"*, as the file's own comment said they should.

<div class="example" markdown="1">
<span class="label">THIS IS THE WHOLE ARGUMENT FOR EXPERT SYSTEMS</span>

**The chain *is* the explanation, and it falls out of the proof for free.** A
neural network can tell you `flu` with 0.94 confidence and nothing else. Add
`rash` to working memory and `bacterial(patient)` becomes derivable — the last query above —
so the system's conclusions change *and it can say which fact changed them*.

That is the sentence to put in the Unit 5 answer, and it is also the honest
limit: an expert system knows only what someone wrote down.
</div>

The Python check for this experiment, `06_logic_and_chaining.py`, is shown in full under Experiment 15, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

flu and rest_advised are derived, bacterial is not; the explanation is the proof; one assertz(rash(patient)) makes bacterial true.
</div>


## Experiment 18 — A DCG grammar for English

### 1. Question

Write a definite clause grammar for simple English sentences.

### 2. Aim

Write the grammar in DCG notation, parse sentences, and build their syntax trees.

### 3. Steps

**In SWI-Prolog**, `18_dcg.pl`:

1. **Write the grammar.**
2. **Parse the sentences.**
3. **Build a syntax tree.**

**The Python check**, `07_bayes_and_local_search.py`, for experiments 18 and 19, and Unit 3's local search:

1. **Experiment 18: parse with the grammar.**
2. **Experiment 19: classify by Naive Bayes.**
3. **Smooth the zero frequency.**
4. **Climb hills.**
5. **Anneal.**
6. **Score and cross genetic boards.**

<div class="formula" markdown="1">
<span class="label">THE PARSE</span>

pytholog does not parse `-->`, so the Python check runs the equivalent recursive
descent; SWI-Prolog runs the DCG itself.

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
</div>


### 4. Programme

**In SWI-Prolog**, `18_dcg.pl`:

{{programme: course-13a-ai/18_dcg.pl}}

**The Python check**, `07_bayes_and_local_search.py`, for experiments 18 and 19, and Unit 3's local search:

{{programme: course-13a-ai/07_bayes_and_local_search.py}}

### 5. Execution and Results

**In SWI-Prolog**, `18_dcg.pl`:

{{output: course-13a-ai/18_dcg.pl}}

**The Python check**, `07_bayes_and_local_search.py`, for experiments 18 and 19, and Unit 3's local search:

{{output: course-13a-ai/07_bayes_and_local_search.py}}

<div class="concept" markdown="1">
<span class="label">WHAT A DCG ACTUALLY IS</span>

**A DCG compiles to exactly this recursive descent**, with the token list
threaded through as **difference lists**. `s --> np, vp.` expands to
`s(S0, S) :- np(S0, S1), vp(S1, S).` — the grammar is written as inference
rules, so this experiment is Unit 4's machinery applied to language. That is
why it sits in an AI course rather than a compilers course.
</div>

<div class="concept" markdown="1">
<span class="label">RESULT</span>

'the big cat chases a mouse' and 'the dog sleeps' parse, 'cat the chases' does not, and the first gives its tree.
</div>


## Experiment 19 — Deterministic Naive Bayes

### 1. Question

Classify a new day with Naive Bayes, by counting.

### 2. Aim

Count the training data, compute each class's posterior for a new day, and smooth a zero frequency.

### 3. Steps

1. **State the training data.**
2. **Count, and compute the probabilities.**
3. **Classify the new day.**
4. **Smooth the zero frequency.**

<div class="formula" markdown="1">
<span class="label">THE POSTERIORS</span>

The 14-day play-tennis table: **9 play, 5 do not**.

Query `(sunny, cool, high, strong)`:

| Class | P(class) × likelihoods |
|---|---:|
| yes | 0.005291 |
| **no** | **0.020571** ← larger |

**Normalised: no 79.54%, yes 20.46%.**
</div>


### 4. Programme

{{programme: course-13a-ai/19_naive_bayes.pl}}

### 5. Execution and Results

{{output: course-13a-ai/19_naive_bayes.pl}}

<div class="example" markdown="1">
<span class="label">THE CROSS-COURSE CHECK</span>

**These are Data Mining's numbers and Machine Learning's numbers.** Three courses,
three implementations — WEKA-equivalent scikit-learn in Data Mining, `GaussianNB`
and a hand calculation in Machine Learning, and this — and the same
0.005291 / 0.020571. **If they ever disagree, one of them is wrong**, and
`tools/data-science/verify_all.sh` says so.
</div>

<div class="warn" markdown="1">
<span class="label">ZERO FREQUENCY VETOES A CLASS</span>

```
'overcast' appears 0 times with play=no
  P(no | overcast, ...) without smoothing = 0.0
  with Laplace (+1, 3 outlook values)     = 0.044643
```

**A single zero vetoes the class whatever the other three features say**,
because the likelihood is a **product**. Laplace smoothing adds 1 to every
count and 3 (the number of outlook values) to every denominator: SWI-Prolog's
`smoothed(1, overcast, no, 3, P)` gives the single likelihood, 0.125, in place of 0.
**Added:** nothing in the file asked for `smoothed/5`; the last two queries run it.
</div>

The Python check for this experiment, `07_bayes_and_local_search.py`, is shown in full under Experiment 18, with what it printed.

<div class="concept" markdown="1">
<span class="label">RESULT</span>

For (sunny, cool, high, strong), no scores 0.020571 and yes 0.005291, so the class is no; Laplace smoothing turns overcast's zero into 0.125.
</div>


---

## The unit-3 extras that share `07_bayes_and_local_search.py`

The syllabus lists hill climbing, simulated annealing and genetic algorithms in
Unit 3 but prescribes **no experiment** for them. They are verified anyway,
because §3.5–3.7 quote numbers; their output is the end of what
`07_bayes_and_local_search.py` printed, under Experiment 18.

**Hill climbing gets stuck 48% of the time.** On a landscape with a local peak near x = 2
and the global near x = 8:

| From 21 starting points | Count |
|---|---:|
| reached the **global** maximum | **11** |
| stuck on the **local** maximum | **10 (48%)** |

**Hill climbing is complete only with random restarts.** If each try succeeds
with probability p, expected restarts = 1/p — here about **1.9**.

**Simulated annealing, as the acceptance probability.** P(accept a move that is 1.0 worse)
= e^(−1/T):

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

**Genetic algorithms — fitness and the crossover trap.** Fitness = non-attacking pairs,
maximum C(8,2) = **28**:

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

Plus the Prolog run: **all 16 `.pl` files, in SWI-Prolog**. Each must load without a warning,
raise no error but the one it demonstrates (`z(X)` in Experiment 16), and give the answers the
Python checks assert — `ancestor(ram, X)`'s five, A*'s 418, 92 queens, the posteriors 0.005291
and 0.020571. If a `.pl` file and its Python check ever disagree, the suite fails.

---

## Lab examination

Two hours in SWISH, one experiment number, then a viva.

**What costs marks:**

- Writing `ancestor/2` left-recursively and running the interpreter out of stack
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
