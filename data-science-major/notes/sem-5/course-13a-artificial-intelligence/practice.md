# Course 13 A — Practice Questions with Worked Solutions

Every figure quoted here is produced by
`labs/course-13a-ai/` and checked by
`tools/run_ai_labs.py`.

---

## Section A — Two-mark questions

**1. What is the Turing Test?**
A human judge holds a text conversation with a human and a machine. If the
judge cannot reliably tell which is which, the machine passes. It tests
**indistinguishable behaviour**, not thought.

**2. Distinguish Weak AI from Strong AI.**
**Weak (narrow) AI** performs one task without understanding — every system in
use today. **Strong (general) AI** would possess general understanding across
domains; none exists.

**3. What is a rational agent?**
One that, for each percept sequence, selects the action **expected** to
maximise its performance measure, given its built-in knowledge. Rationality is
not omniscience — a rational agent can still lose.

**4. Expand PEAS.**
**P**erformance measure, **E**nvironment, **A**ctuators, **S**ensors.

**5. Give one deterministic and one stochastic environment.**
Chess is deterministic; taxi driving is stochastic.

**6. Name the four components of a state-space problem.**
Initial **state**, **actions** (successor function), **goal test**, **path
cost**.

**7. When is BFS optimal?**
Only when **every step costs the same**. It minimises the number of edges, and
edges equal cost only under uniform step costs.

**8. State the space complexity of BFS and of DFS.**
BFS **O(b^d)**; DFS **O(bm)**. That difference — exponential against linear —
is DFS's only real advantage.

**9. What is Uniform Cost Search equivalent to?**
**Dijkstra's algorithm.** Same procedure, reached from the AI side.

**10. Define an admissible heuristic.**
h(n) **never overestimates** the true remaining cost h\*(n): h(n) ≤ h\*(n) for
every n.

**11. Define consistency (monotonicity).**
h(n) ≤ c(n, n′) + h(n′) for every edge. Consistency implies admissibility;
the reverse does not hold.

**12. What is A\*'s evaluation function?**
f(n) = g(n) + h(n) — cost paid plus cost estimated.

**13. What does A\* reduce to when h(n) = 0?**
**Uniform cost search** — verified identical: 13 expansions, cost 418 on
Romania.

**14. Why is Greedy Best-First not optimal?**
It ignores **g(n)**. At Sibiu it prefers Fagaras (h = 176) over Rimnicu Vilcea
(h = 193) and ends 32 km worse — 450 against 418.

**15. What is the main weakness of hill climbing?**
**Local maxima.** Measured here: 10 of 21 starting points (48%) get stuck.

**16. What fixes it?**
**Random restarts.** Expected restarts = 1/p, about 1.9 on this landscape.

**17. What is the acceptance probability in simulated annealing?**
e^(−ΔE/T). For ΔE = 1: **0.990050** at T = 100 and **0.000045** at T = 0.1.

**18. Name the three genetic operators.**
Selection, crossover, mutation.

**19. Define a CSP.**
A set of **variables**, each with a **domain**, and a set of **constraints** on
subsets of them. A solution assigns every variable a value violating no
constraint.

**20. What does MRV stand for and what does it order?**
**Minimum Remaining Values.** It chooses the next **variable** — the one with
fewest legal values left.

**21. And LCV?**
**Least Constraining Value.** It orders the **values** of the chosen variable.

**22. Why do MRV and LCV pull in opposite directions?**
**Variables: fail fast. Values: fail late.** You want to discover a dead end
early, but once committed to a value you want it to survive.

**23. Why does Australia need three colours?**
`WA`, `NT` and `SA` are **mutually adjacent** — a triangle. Two colours give no
solution, discovered after 4 backtracks.

**24. How many solutions has 8-Queens?**
**92**, found after 2,056 placements.

**25. Is P ⇒ Q true when P is false?**
**Yes** — vacuously. P ⇒ Q ≡ ¬P ∨ Q.

**26. Define validity and satisfiability.**
**Valid** = true in every model (P ∨ ¬P, 8/8). **Satisfiable** = true in at
least one (P ∧ Q, 2/8). **Unsatisfiable** = true in none (P ∧ ¬P, 0/8).

**27. State modus ponens and modus tollens.**
P ⇒ Q, P ⊢ Q. P ⇒ Q, ¬Q ⊢ ¬P.

**28. Why is affirming the consequent invalid?**
Row (F, T) of the truth table: P false, Q true, P ⇒ Q true. So Q does not
force P.

**29. Define entailment and give its refutation form.**
KB ⊨ α when α is true in every model of KB. Equivalently **KB ∧ ¬α is
unsatisfiable** — the form resolution mechanises.

**30. What is unification?**
Finding a substitution making two expressions identical:
`Knows(John, x)` and `Knows(y, Mary)` unify with {x/Mary, y/John}.

**31. Difference between ∀ and ∃ in the connective they take.**
∀ pairs with **⇒**, ∃ pairs with **∧**. `∀x Student(x) ∧ Smart(x)` claims
everything is a smart student.

**32. Forward or backward chaining for "does this patient have malaria?"**
**Backward** — many facts, one question.

**33. What is negation as failure?**
`\+ G` succeeds if G cannot be **proved**. It assumes a **closed world** and is
not logical negation: `\+ bird(kiwi)` succeeds only because no one said so.

**34. What is a red cut?**
A cut whose removal **changes the answers**, not just the speed.

**35. Name the four components of an expert system.**
**Knowledge base**, **inference engine**, **working memory**, **explanation
facility** (plus a knowledge-acquisition interface).

**36. State Bayes' theorem.**
P(H|E) = P(E|H) · P(H) / P(E).

**37. What independence does Naive Bayes assume?**
**Conditional** independence of the features **given the class**.

**38. What is the zero-frequency problem, and the fix?**
An unseen feature–class pair gives likelihood 0, which vetoes the class because
the likelihood is a **product**. Fix: **Laplace smoothing** — 0.0 becomes
0.044643 here.

**39. Difference between probability and a fuzzy membership value.**
Probability measures **uncertainty about a crisp fact**; fuzzy membership
measures **degree of truth** of a vague predicate. A 0.7 chance of rain is not
0.7 rain.

**40. Why is search a distinct paradigm from machine learning?**
Search is given a **description** of the problem and explores it; learning is
given **examples** and fits a function. Nothing in this course is trained.

---

## Section B — Five-mark questions

### 1. Explain PEAS with an example, and classify the environment

**PEAS** specifies an agent before you design it.

For an **automated taxi**:

| | |
|---|---|
| **Performance** | safety, legality, trip time, fuel, passenger comfort, profit |
| **Environment** | roads, other traffic, pedestrians, weather, customers |
| **Actuators** | steering, accelerator, brake, indicators, horn, display |
| **Sensors** | cameras, LIDAR, speedometer, GPS, engine sensors, microphone |

Environment classification:

| Property | Taxi | Chess |
|---|---|---|
| Observable | **Partially** | Fully |
| Deterministic | **Stochastic** | Deterministic |
| Episodic | **Sequential** | Sequential |
| Static | **Dynamic** | Semi-dynamic |
| Discrete | **Continuous** | Discrete |
| Agents | **Multi** | Multi |

**Why it matters:** each "hard" answer forces machinery. Partially observable
forces a belief state; stochastic forces expected-value reasoning; continuous
forbids enumerating the state space. **PEAS is a design document, not a
description.**

### 2. Compare BFS, DFS and UCS on completeness, optimality and complexity

| | BFS | DFS | UCS |
|---|---|---|---|
| Complete | **Yes** (finite b) | **No** (infinite depth / loops) | Yes (positive costs) |
| Optimal | **Only if step costs equal** | No | **Yes** |
| Time | O(b^d) | O(b^m) | O(b^(1+⌊C\*/ε⌋)) |
| Space | **O(b^d)** | **O(bm)** | O(b^(1+⌊C\*/ε⌋)) |

Measured on the Romania map, Arad → Bucharest:

| Strategy | Expanded | Edges | Cost |
|---|---:|---:|---:|
| BFS | 9 | **3** | 450 |
| DFS | **6** | 5 | **607** |
| UCS | **13** | 4 | **418** |

**Read it as a trade:** DFS did the least work and found the worst path; UCS
did the most work and found the best. BFS minimised *edges*, which is not the
same as cost — the guarantee it offers does not apply here.

**The counterexample to "BFS is optimal":** on a six-node graph with unit
costs, BFS and UCS both return cost 2. Raise one edge to 50 and BFS returns
**51** where UCS returns **4**.

### 3. Explain iterative deepening and justify its cost

IDS runs depth-limited DFS with limit 0, 1, 2, … until the goal is found. It
has **DFS's memory and BFS's guarantee**.

The obvious objection is that it regenerates the upper levels every time. With
b = 10, d = 5:

| | Nodes generated | Memory |
|---|---:|---|
| BFS | 111,111 | 100,000 |
| IDS | **123,456** | **50** |

**11.1% more nodes, 2,000× less memory.** The repetition is cheap because the
bottom level holds most of the nodes — regenerating everything above it costs
almost nothing. **IDS is the uninformed search of choice when depth is
unknown.**

### 4. Explain admissibility and why an inadmissible heuristic breaks A*

h is **admissible** if h(n) ≤ h\*(n) everywhere. A* then never expands a node
whose f exceeds the optimal cost, so it cannot return a worse goal.

Measured on Romania:

| Heuristic | Expanded | Cost | Optimal? |
|---|---:|---:|---|
| straight-line | 6 | **418** | YES |
| straight-line **× 2** | **4** | 450 | **NO** |
| straight-line **× 5** | 4 | 450 | NO |

**The inadmissible heuristic was faster and wrong.** Overestimating makes a
node on the optimal path *look* worse than an alternative, so A* commits to a
goal before the better route is explored.

**Verification, not assertion:** checked at all 20 cities, straight-line
violated admissibility **0 times**, h(Bucharest) = 0, and the tightest margin
h\*(n) − h(n) was **1 km**. The ×2 heuristic violates at **18 of 20**.

The general argument: **a straight line can never be longer than a road.**
Admissible **by construction**, not by luck.

### 5. Explain heuristic dominance with the 8-puzzle

h1 = misplaced tiles. h2 = sum of Manhattan distances.

| State | h1 | h2 |
|---|---:|---:|
| goal | 0 | 0 |
| one tile out | 2 | 2 |
| scrambled | **6** | **14** |

Both are admissible because both solve a **relaxed** problem — h1 lets a tile
teleport, h2 lets it move to any adjacent square, ignoring the blank. A
relaxed-problem solution can never cost more than the real one.

**h2 ≥ h1 everywhere, so h2 dominates h1**, and A* with h2 expands no more
nodes than A* with h1. Dominance is a stronger and more precise claim than "it
was faster on my example" — and it explains *why* you would derive heuristics
by relaxing constraints.

### 6. Explain forward and backward chaining and when to use each

**Forward** (data-driven): apply every rule whose premises hold, add the
conclusions, repeat. From `{a, b}` and 3 rules it derived `['c', 'd', 'e']` —
**everything derivable**, wanted or not.

**Backward** (goal-driven): to prove `e`, prove its premises; recurse. Proving
`e` needed `d`, which needed `c`, which needed `a` and `b` — and **nothing
outside that chain**.

| Scenario | Use | Because |
|---|---|---|
| A sensor reading arrives — what follows? | Forward | few facts, many conclusions |
| Does this patient have malaria? | **Backward** | many facts, **one** question |
| Continuous plant alarm monitoring | Forward | you want every consequence |
| Why will this car not start? | **Backward** | test only what matters |

**Prolog is backward chaining with depth-first search.** That single sentence
explains why clause order matters and why a left-recursive rule never
terminates.

---

## Section C — Ten-mark questions

### 1. Formulate the 8-puzzle as a state-space problem and solve it with A*

**Formulation:**

| Component | 8-puzzle |
|---|---|
| **State** | a permutation of tiles 1–8 and a blank in a 3×3 grid |
| **Initial state** | any configuration |
| **Actions** | move the **blank** up, down, left, right (2–4 legal) |
| **Goal test** | equality with the goal arrangement |
| **Path cost** | 1 per move |

**Modelling the blank rather than the tiles** cuts the branching factor from
about 20 to under 4. This is the modelling decision the question is really
testing.

**State space size:** 9! = 362,880 arrangements, of which **only half are
reachable** from any given state — parity is invariant under a blank move, so
181,440 configurations are unsolvable from a given start. Never claim 9!
without that.

**Heuristics** — h1 misplaced tiles, h2 Manhattan distance, both admissible by
relaxation, h2 dominant (6 against 14 on a scrambled board).

**A\* on the Romania map** — the same algorithm, verified: **6 expansions,
cost 418**, against UCS's **13 expansions, cost 418**. Same optimal answer,
less than half the work.

**Why h2 is better** is not "it is bigger" but: a larger admissible heuristic
prunes more nodes while keeping the bound, so **dominance implies no more
expansions**, never fewer guarantees.

**The failure mode:** double h2 and A* expands 4 nodes and returns 450 instead
of 418. **Speed bought by breaking admissibility is not speed, it is a
different algorithm.**

### 2. Solve map colouring as a CSP; explain backtracking, MRV, degree and LCV

**Formulation:** variables = the 7 Australian regions; domain = {red, green,
blue}; constraints = adjacent regions differ.

**Solution found:**

| WA | NT | SA | Q | NSW | V | T |
|---|---|---|---|---|---|---|
| red | green | **blue** | red | green | red | red |

**Measured, honestly:**

| Method | Assignments | Backtracks |
|---|---:|---:|
| plain backtracking | 7 | **0** |
| MRV + degree | 7 | **0** |

**The heuristics saved nothing on this problem**, and saying so is worth marks.
The reason: **SA borders every mainland region**, so once SA is assigned every
neighbour has only two values — and the plain ordering happens to reach SA
early too. On a larger map the orderings diverge.

**What the heuristics do:**

After `WA = red`, values remaining:

| Region | Left |
|---|---:|
| **NT** | **2** |
| **SA** | **2** |
| Q, NSW, V, T | 3 |

- **MRV** picks NT — fewest values, most likely to fail, so **fail fast**.
- **Degree** breaks the NT/SA tie by constraint count — SA has 5 neighbours.
- **LCV** then orders NT's values `['green', 'blue']`, least constraining
  first — **fail late**, because you want the committed value to survive.

**With two colours: no solution, after 4 backtracks.** `WA`, `NT`, `SA` form a
mutually adjacent triangle. The search *proves* insolubility by exhausting the
space, which is what "no solution" means for a CSP — it is not a timeout.

**Why CSP beats generic search here:** the goal test is decomposable into
constraints, so you can detect failure at a **partial** assignment instead of
at a complete state. That is the entire advantage.

### 3. Explain propositional logic: syntax, semantics, truth tables and inference

**Syntax:** atomic propositions, and the connectives ¬, ∧, ∨, ⇒, ⇔ with
precedence in that order.

**Semantics:** a **model** assigns true/false to every proposition. A sentence
is true or false *in a model*; n propositions give 2^n models.

**The truth table:**

| P | Q | ¬P | P∧Q | P∨Q | **P⇒Q** | P⇔Q |
|---|---|---|---|---|---|---|
| F | F | T | F | F | **T** | T |
| F | T | T | F | T | **T** | F |
| T | F | F | F | T | **F** | F |
| T | T | F | T | T | T | T |

**The two rows people get wrong** are the first two. **P ⇒ Q is true whenever P
is false**, because it claims only *there is no case where P holds and Q
fails*. That is exactly **¬P ∨ Q**, verified over all 4 models — and it is
step 2 of the CNF conversion, so resolution depends on it.

**Three status classes**, over the 8 models of P, Q, R:

| Sentence | True in | Class |
|---|---:|---|
| P ∨ ¬P | 8/8 | **valid** |
| P ∧ Q | 2/8 | satisfiable |
| P ∧ ¬P | 0/8 | **unsatisfiable** |

**Entailment:** KB ⊨ α when α holds in every model of KB. Measured:
`{P, P⇒Q}` has **2 models** and Q holds in both, so `{P, P⇒Q} ⊨ Q`.

**The refutation form:** KB ⊨ α **iff KB ∧ ¬α is unsatisfiable** — zero models.
This is what resolution mechanises, because searching for *one* contradiction
is cheaper than checking *all* models.

**Inference rules:** modus ponens (P⇒Q, P ⊢ Q) and modus tollens (P⇒Q, ¬Q ⊢
¬P), both verified over all 4 models. **Affirming the consequent (P⇒Q, Q ⊢ P)
is invalid**, and the table names the counterexample: row (F, T).

**Soundness and completeness:** an inference procedure is **sound** if it
derives only entailed sentences and **complete** if it derives every entailed
sentence. Resolution is both, for propositional logic.

**The limitation that forces FOL:** propositional logic has no objects and no
quantifiers, so "every student who studies passes" needs one sentence *per
student*. A world of n objects and k properties needs n·k propositions.

### 4. Design a rule-based expert system with an explanation facility

**Architecture:**

| Component | Role |
|---|---|
| **Knowledge base** | domain rules, written by a human expert |
| **Working memory** | the facts of *this* case |
| **Inference engine** | matches rules to facts and fires them |
| **Explanation facility** | reconstructs the derivation as justification |
| **Knowledge acquisition** | how the expert adds rules |

**The separation of knowledge from inference is the architectural point** — a
domain expert edits rules without touching code, which is why expert systems
were commercially viable when general AI was not.

**The system, implemented and run:**

```prolog
viral(X)        :- fever(X), cough(X).
flu(X)          :- viral(X), fatigue(X).
bacterial(X)    :- fever(X), rash(X).
rest_advised(X) :- flu(X).
```

Working memory: `fever`, `cough`, `fatigue`. Results, through real SLD
resolution:

```
?- viral(patient)         -> Yes
?- flu(patient)           -> Yes
?- rest_advised(patient)  -> Yes
?- bacterial(patient)     -> not derivable (no rash recorded)
```

**The explanation:**

```
HOW did you conclude rest_advised(patient)?
  by rule  rest_advised(X) :- flu(X)
  flu(patient)     by  flu(X) :- viral(X), fatigue(X)
    viral(patient) by  viral(X) :- fever(X), cough(X)
      fever(patient)   -- a fact in working memory
      cough(patient)   -- a fact in working memory
    fatigue(patient)   -- a fact in working memory
```

**The chain *is* the explanation, and it falls out of the proof for free.** A
neural network can output "flu, 0.94" and nothing more. Add `rash` and
`bacterial(patient)` becomes derivable — the conclusion changes **and the
system can name the fact that changed it**.

**WHY questions** are the other direction: when the system asks for a symptom,
"why do you need this?" is answered by the rule currently being proved.

**Limitations, which the question expects:**

- **The knowledge acquisition bottleneck** — the expert's time is the cost, and
  it does not scale.
- **Brittleness** — no graceful degradation at the edge of the rule set. It
  does not know what it does not know.
- **No learning** — it never improves from cases it has seen.
- **Rule interaction** — beyond a few hundred rules, conflicts become
  unmanageable, which is what ended the 1980s expert-system boom.

### 5. Explain Bayes' theorem and Naive Bayes with a full worked calculation

**Bayes' theorem:** P(H|E) = P(E|H)·P(H) / P(E) — posterior = likelihood ×
prior / evidence.

**Naive Bayes** classifies by argmax over classes of
P(c) · ∏ P(feature_i | c), assuming the features are **conditionally
independent given the class**. That assumption is nearly always false, and it
works anyway because classification needs only the correct class to **rank
first**, not the probabilities to be right.

**Worked, on the 14-day play-tennis data — 9 play, 5 do not.**
Query: outlook = **sunny**, temperature = **cool**, humidity = **high**,
wind = **strong**.

| | P(yes) branch | P(no) branch |
|---|---|---|
| prior | 9/14 | 5/14 |
| P(sunny \| c) | 2/9 | 3/5 |
| P(cool \| c) | 3/9 | 1/5 |
| P(high \| c) | 3/9 | 4/5 |
| P(strong \| c) | 3/9 | 3/5 |
| **product** | **0.005291** | **0.020571** |

**Normalised: no = 79.54%, yes = 20.46%. Predict NO.**

**Note the denominator is never computed** — P(E) is the same for both classes,
so it cancels in the comparison. It is needed only to normalise, and only if
you want a probability rather than a decision.

**The zero-frequency problem:** `overcast` never appears with `play = no`, so
P(overcast | no) = 0 and

```
P(no | overcast, ...) without smoothing = 0.0
with Laplace (+1, 3 outlook values)     = 0.044643
```

**One zero vetoes the class whatever the other three features say**, because
the likelihood is a **product**. Laplace smoothing adds 1 to each count and k
(the number of values the feature takes — here 3) to each denominator.

**Cross-course verification:** these are Course 8's numbers and Course 12 A's
numbers. **Three courses, three independent implementations, the same
0.005291 and 0.020571** — and `tools/verify_all.sh` fails if they ever drift.

**Bayesian belief networks** generalise this: a directed acyclic graph where
each node carries P(node | parents), and the joint distribution factorises as
the product of those tables. **Naive Bayes is the special case** in which every
feature has the class as its single parent — which is exactly what conditional
independence means, drawn.

### 6. Compare classical AI with machine learning, and state where each belongs

| | **Classical AI (this course)** | **Machine learning (12 A)** |
|---|---|---|
| Given | a **description** of the problem | **examples** with answers |
| Produces | a solution, or a path to one | a fitted model |
| Method | **search** and **inference** | optimise parameters |
| Knowledge | **explicit** — facts and rules | implicit, in the weights |
| Explains itself | **completely** | poorly |
| Fails by | **combinatorial explosion** | overfitting |
| Needs | a correct model of the world | a lot of labelled data |
| Good at | reasoning, planning, constraints | perception, prediction |

**Where classical AI is still the right answer:**

- The rules are **known and stated** — tax law, drug interaction checking,
  scheduling. Learning them from examples would be perverse.
- The decision must be **justified**. A triage system that cannot explain
  itself is not deployable, whatever its accuracy.
- There are **no examples to learn from** — a chess position never seen, a
  timetable never built.

**Where it fails:** perception. No one writes rules that recognise a cat, and
the attempt is what caused the second AI winter.

**The honest modern position:** the two are combined. A chess engine searches
with a learned evaluation function; a self-driving car uses learned perception
and a planned route. **Search supplies the guarantee, learning supplies the
model** — and each covers what the other cannot.

---

## The six things most likely to be examined

1. **The Romania table.** BFS 9/450, DFS 6/607, UCS 13/418, greedy 4/450,
   **A\* 6/418**. Five numbers that answer half of Units 2 and 3.
2. **Admissibility, with the failure case.** ×2 gives 4 expansions and 450 km —
   faster and wrong, violating at 18 of 20 cities.
3. **A\* with h = 0 is UCS**, verified identical at 13/418.
4. **The Naive Bayes calculation** — 0.005291 against 0.020571, normalising to
   79.54% no, with the zero-frequency fix at 0.044643.
5. **The expert system's explanation chain**, and the sentence that a neural
   network cannot produce one.
6. **"Variables fail fast, values fail late"** — MRV against LCV, with the
   NT-has-2-values table and the honest zero-backtracks result.
