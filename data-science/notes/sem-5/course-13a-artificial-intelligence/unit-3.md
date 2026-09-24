# Unit 3 — Informed and Advanced Search Strategies

**Syllabus topics:** Informed search strategies — heuristics (concept,
admissibility, consistency), Greedy Best First Search, A* Algorithm. Local
search — Hill Climbing, Simulated Annealing. Genetic Algorithms. Constraint
Satisfaction Problems (CSP) — definition, backtracking search.

> **This unit and Unit 4 carry the marks.** A* and its admissibility guarantee
> are asked almost every year. Every figure below is computed in
> `labs/course-13a-ai/`.

---

## 3.1 Heuristics

### 🎯 The big idea

**A heuristic h(n) estimates the cost of the cheapest path from n to a goal.**

Uninformed search has no idea which direction a goal lies in. A heuristic is
**problem-specific knowledge** that gives it one — and the entire difference
between Units 2 and 3 is that h(n) exists.

| Symbol | Means |
|---|---|
| **g(n)** | Cost of the path from the start **to** n — **known** |
| **h(n)** | Estimated cost from n **to** a goal — **guessed** |
| **f(n)** | The evaluation function that orders the frontier |
| **h\*(n)** | The **true** cheapest cost from n to a goal — usually unknown |

### 🔢 Admissibility — the property everything depends on

> **h is admissible if h(n) ≤ h\*(n) for every n.**
> **It never overestimates.**

**Straight-line distance is admissible for road navigation** because a road can
never be shorter than a straight line. That single sentence is the standard
example and the standard justification.

Note that **h(goal) must be 0**.

### 🔢 Consistency (monotonicity) — the stronger property

> **h is consistent if h(n) ≤ c(n, a, n′) + h(n′) for every node n and every
> successor n′.**

It is the **triangle inequality**: going to n′ and then estimating from there
must not be cheaper than estimating directly from n.

| | Admissible | Consistent |
|---|---|---|
| Guarantees optimality for | **A\* tree search** | **A\* graph search** |
| Implies f never decreases along a path | No | **Yes** |
| Relationship | **Consistency ⟹ admissibility** | Admissibility does **not** imply consistency |

**Almost every natural heuristic is consistent**, so the distinction is mostly
theoretical — but it is examinable, and the direction of the implication is the
part that gets reversed in answers.

### 💡 Where heuristics come from — relaxed problems

**A relaxed problem has fewer restrictions on its actions, and the exact cost
of an optimal solution to the relaxed problem is an admissible heuristic for
the original.**

For the 8-puzzle:

| Relaxation | Gives |
|---|---|
| A tile can move anywhere | **h₁ = misplaced tiles** |
| A tile can move to any *adjacent* square, even an occupied one | **h₂ = Manhattan distance** |

Both are admissible by construction, and **h₂ dominates h₁** — h₂(n) ≥ h₁(n)
for every n, so A* with h₂ expands no more nodes than with h₁.

**Dominance is the right way to compare heuristics**, and a stronger claim than
"h₂ is better in my experiments".

---

## 3.2 Greedy Best First Search

**f(n) = h(n).** Expand whatever *looks* closest to the goal.

- **Not optimal.**
- **Not complete** in tree search — it can loop between two nodes that each
  look good.
- Time and space **O(b^m)** in the worst case, though a good heuristic makes it
  far better in practice.

### 🔢 Measured on Romania, Arad → Bucharest

| Strategy | Expanded | Cost |
|---|---:|---:|
| **Greedy** | **4** | **450** |
| **A\*** | 6 | **418** |
| Uniform cost | 13 | **418** |

**Greedy expanded the fewest nodes of any strategy in the course and returned a
suboptimal path.** It goes Arad → Sibiu → Fagaras → Bucharest, because Fagaras
*looks* closer to Bucharest (h = 176) than Rimnicu Vilcea (h = 193) — and it is
closer *as the crow flies*. But the road through Rimnicu Vilcea and Pitesti is
32 km shorter overall.

**Greedy is short-sighted because it ignores g(n) — the cost already paid.**
That sentence is the whole diagnosis, and it leads directly to A*.

---

## 3.3 A* search

### 🎯 The idea

> **f(n) = g(n) + h(n)**
> **cost so far + estimated cost remaining = estimated total cost**

Expand the node with the lowest f. That is the entire algorithm, and it is one
of the most important in computer science.

### 🔢 The guarantee

**A\* is complete and optimal, provided h is admissible (tree search) or
consistent (graph search).**

**A\* is also optimally efficient**: no other optimal algorithm using the same
heuristic is guaranteed to expand fewer nodes. You cannot do better without a
better heuristic.

### 🔢 The measured result — the headline of this unit

Romania, Arad → Bucharest:

| Search | h(n) | Expanded | Cost | Optimal? |
|---|---|---:|---:|:---:|
| **Uniform cost** (= A* with h = 0) | 0 | **13** | **418** | ✓ |
| **A\*** | straight-line | **6** | **418** | ✓ |
| **Greedy** | straight-line | 4 | 450 | ✗ |

**A\* found the optimal path while expanding 6 nodes where UCS needed 13 — less
than half the work, and the same answer.**

**That comparison is the reason heuristics exist**, and it is the number to
quote.

### 💡 A* with h = 0 *is* uniform cost search

Set h(n) = 0 and f(n) = g(n), which is UCS exactly. The lab asserts that both
expand 13 nodes and return 418 — the same algorithm under a different name.

**A\* sits between UCS (h = 0, no information, optimal) and greedy (g ignored,
maximum information used badly, not optimal), and takes the good half of
each.**

### ⚠️ What breaks without admissibility — measured

Multiply the straight-line heuristic by 2, so it now **overestimates**:

| Heuristic | Expanded | Cost | Optimal? |
|---|---:|---:|:---:|
| straight-line (admissible) | 6 | **418** | ✓ |
| **straight-line × 2 (inadmissible)** | **4** | **450** | **✗** |
| straight-line × 5 (inadmissible) | 4 | 450 | ✗ |

**The inflated heuristic is faster and wrong.** It expands 4 nodes instead of 6
and returns 450 instead of 418.

**Why:** an overestimating h can make the node on the optimal path *look* worse
than an alternative, so A* commits to a goal before the better path is
explored. The guarantee is gone the moment h(n) > h*(n) anywhere.

**This is the single best demonstration in the course**, because it turns "h
must never overestimate" from a rule to be memorised into a measurable
consequence.

### 🔢 A*'s weakness

**Memory.** A* keeps every generated node, so space is O(b^d) — it usually runs
out of memory long before it runs out of time.

| Variant | Fixes it by |
|---|---|
| **IDA\*** (iterative deepening A*) | Depth-first with an **f-cost limit** — linear memory |
| **RBFS** (recursive best-first) | Linear memory; re-expands nodes |
| **SMA\*** | Uses all available memory, **drops the worst node** when full |
| **Weighted A\*** — f = g + w·h, w > 1 | Deliberately inadmissible: **faster, and suboptimal by at most a factor of w**. Often the right engineering trade |

**Weighted A\* is worth knowing** because it makes the inadmissibility
demonstration above *useful*: you give up the guarantee knowingly, and get a
bounded guarantee instead.

---

## 3.4 Local search

### 🎯 The shift in thinking

**Local search keeps only the current state and moves to neighbours. It does
not keep a path.**

That is legitimate whenever **the goal state itself is the answer and the route
to it is irrelevant** — N-Queens, scheduling, VLSI layout, timetabling.

| | **Systematic search** (Units 2–3.3) | **Local search** |
|---|---|---|
| Keeps | The **path** | **One state** (or a few) |
| Memory | Exponential | **Constant** |
| Complete | Often | **No** |
| Optimal | Often | **No** |
| Good for | Route finding, puzzles | **Optimisation**, huge state spaces |

---

## 3.5 Hill climbing

**Move to the best neighbour. Stop when no neighbour is better.**

```
current ← initial state
loop:
    neighbour ← the highest-valued successor of current
    if VALUE(neighbour) ≤ VALUE(current): return current
    current ← neighbour
```

It is **greedy local search**, and it is sometimes called *steepest ascent*.

### ⚠️ The three ways it fails — a guaranteed exam question

| Failure | What happens |
|---|---|
| **Local maximum** | A peak lower than the global maximum. Every neighbour is worse, so it stops |
| **Plateau / shoulder** | A flat region. No neighbour is better, so it has no direction. A *shoulder* can be escaped by sideways moves; a flat local maximum cannot |
| **Ridge** | A sequence of local maxima that is hard to navigate, because every single-step move goes downhill even though the ridge ascends |

**On random 8-queens instances, plain hill climbing solves about 14% of them**
— the classic figure — and gets stuck the rest of the time.

### The escapes

| Fix | How |
|---|---|
| **Sideways moves** | Allow equal-valued moves, with a limit. Raises 8-queens to ~94% |
| **Random restarts** | Restart from a random state. **If each try succeeds with probability p, expected restarts = 1/p** — so a 14% success rate needs about **7** tries |
| **Stochastic hill climbing** | Choose randomly among uphill moves, weighted by steepness |
| **First-choice** | Generate successors at random until one is better — good when there are thousands |
| **Simulated annealing** | §3.6 |

**Random-restart hill climbing is complete with probability approaching 1**,
simply because it eventually starts somewhere from which the peak is reachable.
That is worth stating.

---

## 3.6 Simulated annealing

### 🎯 The idea

**Sometimes accept a worse move, and accept fewer of them over time.**

The name is from metallurgy: heat a metal, then cool it slowly so its atoms
settle into a low-energy crystal instead of freezing into a defective one.

```
for t = 1 to ∞:
    T ← schedule(t)                      # temperature, decreasing
    if T = 0: return current
    next ← a RANDOMLY chosen successor
    ΔE ← VALUE(next) − VALUE(current)
    if ΔE > 0:  current ← next                    # always take an improvement
    else:       current ← next with probability e^(ΔE/T)
```

### 🔢 The acceptance probability is the whole algorithm

> **P(accept a worse move) = e^(ΔE / T)**

| | Effect |
|---|---|
| **ΔE very negative** (much worse) | Probability near 0 — rarely accepted |
| **T high** (early) | Probability near 1 — **almost anything accepted**; it explores |
| **T → 0** (late) | Probability → 0 — **it becomes hill climbing**; it exploits |

**So annealing is a scheduled slide from random walk to hill climbing.** That
sentence answers the five-mark question.

**The theoretical guarantee:** if T is lowered slowly enough, simulated
annealing finds the global optimum with probability approaching 1. **"Slowly
enough" is impractically slow**, so real schedules are geometric
(T ← 0.95 T) and the guarantee is given up — a fact worth stating rather than
hiding.

---

## 3.7 Genetic algorithms

### 🎯 The idea

**A population of candidate solutions, bred by selection, crossover and
mutation.** It is stochastic **beam search** with a sexual-reproduction
operator.

```
population ← k random individuals
repeat:
    evaluate FITNESS of each individual
    select parents, with probability proportional to fitness
    CROSSOVER pairs of parents to make children
    MUTATE each child with small probability
    population ← the new generation
until a fit-enough individual appears or time runs out
```

| Term | Means | 8-queens example |
|---|---|---|
| **Individual / chromosome** | One candidate solution | A string like `24748552` — the row of the queen in each column |
| **Gene** | One position | One digit |
| **Fitness function** | How good it is | **Non-attacking pairs**, maximum 28 |
| **Selection** | Choosing parents | Roulette wheel, tournament, elitism |
| **Crossover** | Combining two parents at a cut point | `247|48552` + `327|52411` → `24752411` |
| **Mutation** | A random change | One digit becomes random |

### 💡 Crossover is what distinguishes a GA from a random restart

**It only helps if the representation groups meaningfully related genes
together.** Cutting a chromosome preserves *contiguous blocks* — so if
neighbouring genes form a partial solution ("the first three queens are safe
together"), crossover carries that block into the next generation intact.

**With a badly ordered representation, crossover is just noise**, and the GA
degenerates into an expensive random search. Saying that shows you understand
why GAs sometimes work and often do not.

### ⚠️ An honest assessment

GAs are **easy to apply and rarely the best tool.** They need no gradient and
no problem structure, which is their appeal — and they are usually beaten by a
method that exploits the structure they ignore. **Mention that.** An answer
that only lists the operators reads like a brochure.

---

## 3.8 Constraint Satisfaction Problems

### 🔢 The definition

A CSP is a triple **⟨X, D, C⟩**:

| | Is |
|---|---|
| **X** | A set of **variables** X₁ … Xₙ |
| **D** | A **domain** Dᵢ of allowed values for each variable |
| **C** | A set of **constraints**, each restricting the values of some subset of variables |

A **solution** is a **complete, consistent** assignment — every variable has a
value, and no constraint is violated.

### 🎯 Why CSPs are treated separately

**In a CSP the state has structure the search can exploit.** A general search
sees states as black boxes; a CSP solver can see that a partial assignment
already violates a constraint and **prune the whole subtree**.

| | Example |
|---|---|
| **Map colouring** | X = regions, D = {red, green, blue}, C = adjacent regions differ |
| **8-Queens** | X = columns, D = rows 1–8, C = no two share a row or diagonal |
| **Sudoku** | X = 81 cells, D = 1–9, C = rows, columns and boxes all-different |
| **Timetabling** | X = classes, D = slots, C = no clashes of room or teacher |

### 🔢 Backtracking search

**Depth-first search that assigns one variable at a time and backtracks the
moment a constraint is violated.**

```
function BACKTRACK(assignment, csp):
    if assignment is complete: return assignment
    var ← SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    for each value in ORDER-DOMAIN-VALUES(var, assignment, csp):
        if value is consistent with assignment:
            add {var = value} to assignment
            result ← BACKTRACK(assignment, csp)
            if result ≠ failure: return result
            remove {var = value}
    return failure
```

### 🔢 The heuristics that make it fast — and these are the examinable part

| Heuristic | Rule | Why |
|---|---|---|
| **MRV** (minimum remaining values) | Choose the variable with **fewest legal values left** | **Fail fast.** If a variable has one option, deciding it now cannot be wrong; if it has none, discover that immediately rather than after ten more assignments |
| **Degree heuristic** | Tie-break on the variable involved in the **most constraints** on unassigned variables | Reduces the branching factor for everything that follows |
| **LCV** (least constraining value) | Try the value that **rules out fewest** options for the neighbours | Keeps the most doors open — the opposite instinct from MRV, and correctly so |
| **Forward checking** | After each assignment, delete inconsistent values from neighbours' domains | Detects failure earlier |
| **Arc consistency (AC-3)** | Propagate constraints until every arc is consistent | Detects failure earlier still |

### ⚠️ MRV and LCV pull in opposite directions, and that is correct

**MRV chooses the variable most likely to fail** — because you want to discover
failure now.
**LCV chooses the value least likely to cause failure** — because once you have
committed to a variable you want the assignment to survive.

**Variables: fail fast. Values: fail late.** That is the one-line answer, and
it is asked as a trick question.

---

## Practice problems

### Problem 1

Explain the A* algorithm. What is admissibility, and what happens without it?
*(10 marks)*

**Solution.**

**The algorithm:** A* is best-first search with **f(n) = g(n) + h(n)** — cost
so far plus estimated cost remaining. Expand the node with the lowest f.
Define g, h, f and h*.

**Admissibility:** h is admissible if **h(n) ≤ h\*(n) for all n** — it **never
overestimates**. Straight-line distance is admissible for road navigation
because no road is shorter than a straight line.

**Consistency** is stronger: h(n) ≤ c(n, a, n′) + h(n′), the triangle
inequality. **Consistency implies admissibility, not the reverse.** Admissible
h guarantees optimal A* *tree* search; consistent h is needed for *graph*
search.

**The guarantee:** A* is complete and optimal, and **optimally efficient** — no
other optimal algorithm with the same heuristic expands fewer nodes.

**Then the measured demonstration**, which is what earns the top marks. On the
Romania map, Arad → Bucharest:

| Search | h | Expanded | Cost |
|---|---|---:|---:|
| Uniform cost (A* with h = 0) | 0 | **13** | 418 |
| **A\*** | straight-line | **6** | **418** |
| Greedy | straight-line | 4 | 450 |
| **A\*, h × 2** | **inadmissible** | 4 | **450** |

Three things to draw out:

1. **A\* found the optimal 418 expanding 6 nodes where UCS needed 13** — less
   than half the work for the same answer. That is why heuristics exist.
2. **A\* with h = 0 *is* UCS** — same 13 nodes, same 418.
3. **Doubling the heuristic makes it inadmissible: 4 nodes, and 450 — wrong.**
   An overestimate can make the node on the optimal path look worse than an
   alternative, so A* commits before the better path is explored.

Close with A*'s weakness — **memory**, O(b^d) — and the fixes: IDA*, RBFS,
SMA*, and **weighted A\*** (f = g + w·h), which is deliberately inadmissible
but suboptimal by at most a factor of w.

### Problem 2

Explain hill climbing, its failure modes and how they are addressed. Compare
with simulated annealing. *(10 marks)*

**Solution.**

**Hill climbing:** move to the best-valued neighbour; stop when none is better.
It keeps only the current state, so memory is constant and no path is
retained — legitimate when the **goal state itself is the answer**.

**The three failure modes:**

| Failure | What happens |
|---|---|
| **Local maximum** | A peak below the global one; every neighbour is worse, so it halts |
| **Plateau / shoulder** | A flat region with no direction. A shoulder can be crossed with sideways moves; a flat local maximum cannot |
| **Ridge** | Ascending, but every single-step move goes downhill |

**On random 8-queens, plain hill climbing solves about 14%** of instances.

**The fixes:** sideways moves (raising 8-queens to about 94%); **random
restarts** — with success probability p, expected restarts = **1/p**, so ~7
tries at 14%; stochastic and first-choice variants. Random-restart hill
climbing is **complete with probability approaching 1**.

**Simulated annealing** accepts a worse move with probability
**e^(ΔE/T)**, with T decreasing on a schedule:

- **T high** → almost anything accepted → it **explores**
- **T → 0** → nothing worse accepted → it **becomes hill climbing** → it
  **exploits**

**So annealing is a scheduled slide from random walk to hill climbing**, and
that is why it escapes local maxima where hill climbing cannot. Add the honest
caveat: the guarantee of finding the global optimum requires cooling *so*
slowly that no practical schedule achieves it.

### Problem 3

What is a CSP? Explain backtracking search and the heuristics that speed it up.
*(10 marks)*

**Solution.**

**Definition:** a CSP is ⟨X, D, C⟩ — variables, a domain per variable, and
constraints. A **solution** is a complete, consistent assignment.

**Why CSPs get their own treatment:** general search treats a state as a black
box, while a CSP solver can see that a *partial* assignment already violates a
constraint and **prune the entire subtree**. That structure is the whole
advantage.

Give examples — map colouring, 8-queens, Sudoku, timetabling — with X, D and C
named for at least one.

**Backtracking search** is depth-first assignment of one variable at a time,
undoing the last choice as soon as a constraint fails. Give the pseudocode.

**The heuristics, which are the examinable part:**

- **MRV** — choose the variable with fewest remaining legal values. **Fail
  fast**: if it has one option, deciding now cannot be wrong; if none, discover
  that immediately.
- **Degree heuristic** — tie-break on the variable constraining the most
  unassigned variables.
- **LCV** — choose the value ruling out fewest options for neighbours. **Fail
  late.**
- **Forward checking** — prune neighbours' domains after each assignment.
- **Arc consistency (AC-3)** — propagate until every arc is consistent.

**Close with the observation that is asked as a trick:** MRV and LCV pull in
opposite directions and both are right. **Variables: fail fast. Values: fail
late.** You want to *discover* a dead end as early as possible, but once
committed to a variable you want the value you pick to *survive*.

---

## Exam questions from this unit

**Two marks**

1. Define an admissible heuristic.
2. What is f(n) in A*?
3. What does A* reduce to when h(n) = 0?
4. Give one heuristic for the 8-puzzle.
5. What is a plateau in hill climbing?
6. Write the acceptance probability for simulated annealing.
7. State MRV in one sentence.

**Five marks**

1. Compare greedy best-first search with A*.
2. Explain admissibility and consistency, and how they differ.
3. Explain the failure modes of hill climbing.
4. Explain simulated annealing and the role of temperature.
5. Explain the operators of a genetic algorithm.
6. Explain forward checking and arc consistency.

**Ten marks**

1. Explain A*, admissibility, and what breaks without it.
2. Explain hill climbing and simulated annealing, with failure modes.
3. Explain CSPs, backtracking search and its heuristics.
4. Explain genetic algorithms with the 8-queens example.

---

## Mistakes that cost marks

- **Saying an admissible heuristic "is accurate".** It **never
  overestimates** — being wildly optimistic is admissible and useless, but
  still admissible.
- **Reversing the implication.** Consistency ⟹ admissibility, not the reverse.
- **Saying greedy search is A* without g.** True, and the point is *why* that
  breaks it: ignoring the cost already paid makes it short-sighted — 450
  against 418 on Romania.
- **Claiming A*'s problem is speed.** It is **memory**, O(b^d).
- **Calling hill climbing complete.** It is not; **random-restart** hill
  climbing is complete with probability approaching 1.
- **Saying simulated annealing "sometimes accepts worse moves" and stopping
  there.** The point is the **schedule** — it slides from random walk to hill
  climbing.
- **Listing GA operators without saying when crossover helps.** It helps only
  when the representation groups related genes contiguously.
- **Getting MRV and LCV the same way round.** Variables fail fast; values fail
  late.
