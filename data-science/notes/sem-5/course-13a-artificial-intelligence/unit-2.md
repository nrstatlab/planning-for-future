# Unit 2 — Problem Solving: State Space and Uninformed Search

**Syllabus topics:** State space representation — components (state,
actions, goal test, path cost). Problem formulation and examples (8-puzzle,
water jug, vacuum cleaner world). Uninformed search strategies — Breadth First
Search (BFS), Depth First Search (DFS), Uniform Cost Search. Properties —
completeness, optimality, time and space complexity.

> All node counts and path costs in this unit are computed by
> `labs/course-13a-ai/` on **Russell and
> Norvig's Romania map**, so they can be checked against the textbook as well
> as against the code.

---

## 2.1 State space representation

### 🎯 The big idea

**Formulating the problem *is* most of the work.** Given a good formulation,
the search algorithm is a dozen lines. Given a bad one, no algorithm helps.

### 🔢 The five components

A search problem is defined by:

| Component | Is | For the 8-puzzle |
|---|---|---|
| **Initial state** | Where you start | The given tile arrangement |
| **Actions(s)** | What is legal in state s | Move the blank up / down / left / right |
| **Transition model** — `Result(s, a)` | The state reached | The arrangement after the move |
| **Goal test** | Is this state a goal? | Does it match the target arrangement? |
| **Path cost** | The cost of a sequence | 1 per move |

Two derived terms the exam uses:

- **State space** — every state reachable from the initial state. Usually
  **implicit**: defined by the actions, never listed.
- **Solution** — an action sequence from initial state to goal. **Optimal
  solution** — the one with lowest path cost.

### ⚠️ State space ≠ search tree

| | **State space** | **Search tree** |
|---|---|---|
| Nodes are | **States** — a state appears **once** | **Paths** — the same state can appear many times |
| Size | Finite here | Can be **infinite**, even on a finite state space |

The 8-puzzle has **9!/2 = 181,440** reachable states, but its search tree is
infinite — you can walk left, right, left, right for ever. **That gap is why
you keep an explored set**, and it is a favourite two-mark question.

### 🔢 Problem formulation — the three standard examples

**The vacuum world.** Two squares, each clean or dirty, agent in one of them.

- States: 2 positions × 2² dirt configurations = **8 states**
- Actions: Left, Right, Suck
- Goal: both squares clean
- Cost: 1 per action

**The water jug.** A 4-litre and a 3-litre jug, no markings; measure exactly 2
litres.

- State: **(x, y)** — litres in the 4-jug and 3-jug. x ∈ 0..4, y ∈ 0..3, so
  **20 states**
- Initial: (0, 0). Goal: x = 2
- Actions: fill either jug; empty either; pour one into the other until the
  source empties or the target fills — **six actions**

A shortest solution: (0,0) → (0,3) → (3,0) → (3,3) → (4,2) → (0,2) → **(2,0)**
— six actions.

**The 8-puzzle.**

- States: **9!/2 = 181,440** reachable (the puzzle has two parity classes and
  only one contains the goal)
- Actions: move the **blank**, which is neater than moving tiles
- Cost: 1 per move

⚠️ **Half of all 8-puzzle configurations are unsolvable.** Parity —
the number of inversions — is invariant under legal moves, so a random
scramble has a 50% chance of being unreachable from the goal. **Check
solvability before searching**, or the algorithm explores 181,440 states and
correctly reports failure after a very long time.

### 💡 Choosing the representation is a real decision

For the 8-puzzle, "move the blank" gives at most **4** actions per state.
"Move a tile" gives up to 8 and needs a legality check on each. Same problem,
half the branching factor — and branching factor is the base of an exponential.

---

## 2.2 The general search algorithm

Every strategy in Units 2 and 3 is the same loop with a different queue.

```
frontier ← {initial node}
explored ← {}
loop:
    if frontier is empty          → return failure
    node ← REMOVE from frontier        ← THE ONLY THING THAT VARIES
    if node is a goal             → return the solution
    add node.state to explored
    for each action:
        child ← Result(node, action)
        if child.state not in explored and not in frontier:
            add child to frontier
```

| Strategy | The frontier is a | Removes |
|---|---|---|
| **BFS** | **FIFO queue** | The **shallowest** node |
| **DFS** | **LIFO stack** | The **deepest** node |
| **Uniform cost** | **Priority queue on g(n)** | The **cheapest path so far** |
| **Greedy** (Unit 3) | Priority queue on h(n) | The node that **looks closest** |
| **A\*** (Unit 3) | Priority queue on g(n) + h(n) | The best **estimated total** |

**Learn that table.** It compresses two units into six rows, and it is the
single most useful thing in the course.

### ⚠️ Tree search vs graph search

**Graph search keeps an explored set; tree search does not.** Without it,
search revisits states endlessly and can loop for ever on a graph with cycles.
The cost is memory proportional to the number of states visited.

**Always use graph search unless the question says otherwise**, and say why.

---

## 2.3 Measuring a search strategy

### 🔢 The four properties — the table you will be asked to reproduce

| | **Complete?** | **Optimal?** | **Time** | **Space** |
|---|---|---|---|---|
| **BFS** | **Yes** (if b finite) | **Yes, if step costs are equal** | O(b^d) | **O(b^d)** |
| **Uniform cost** | Yes | **Yes** | O(b^(1+⌊C*/ε⌋)) | O(b^(1+⌊C*/ε⌋)) |
| **DFS** | **No** (infinite depth / loops) | **No** | O(b^m) | **O(bm)** |
| Depth-limited | No (if l < d) | No | O(b^l) | O(bl) |
| **Iterative deepening** | **Yes** | **Yes, if step costs equal** | O(b^d) | **O(bd)** |
| Bidirectional | Yes | Yes (with BFS) | **O(b^(d/2))** | O(b^(d/2)) |

where **b** = branching factor, **d** = depth of the shallowest goal,
**m** = maximum depth, **C\*** = optimal cost, **ε** = minimum step cost.

| Property | Means |
|---|---|
| **Complete** | If a solution exists, it will be found |
| **Optimal** | The solution found has lowest path cost |
| **Time** | Nodes generated |
| **Space** | Nodes held in memory at once |

### ⚠️ BFS's real problem is memory, not time

At b = 10 and 1,000 nodes/second and 100 bytes/node, depth 12 needs about
**11 hours and 1 petabyte**. The time is bad; **the memory is impossible**.

**Space is the binding constraint on BFS**, and saying so — rather than "it is
slow" — is the mark.

---

## 2.4 Breadth First Search

**Expand the shallowest unexpanded node.** FIFO queue.

- **Complete** whenever b is finite.
- **Optimal only when all step costs are equal**, because it finds the
  *shallowest* goal, not the *cheapest*.
- Time and space both **O(b^d)** — exponential in both.

### 💡 The goal test goes on generation, not expansion

Test a child as it is generated, not when it is removed from the frontier.
Otherwise you expand an entire extra level before noticing, which multiplies
the work by b.

---

## 2.5 Depth First Search

**Expand the deepest unexpanded node.** LIFO stack.

- **Not complete** — it can descend an infinite branch, or loop on a cycle
  without an explored set.
- **Not optimal** — it returns the first goal it stumbles on.
- Time **O(b^m)**, which is worse than BFS when m ≫ d.
- **Space O(bm) — linear.** This is its one great virtue.

### 🔢 Depth-limited and iterative deepening

**Depth-limited search** is DFS with a cut-off l. It is complete only if l ≥ d,
and it introduces a new failure mode: returning "no solution" when the solution
is simply deeper than l.

**Iterative deepening (IDS)** runs depth-limited search with l = 0, 1, 2, …
until a goal is found. It sounds wasteful and is not:

> Nodes generated by IDS = (d+1)b⁰ + d·b¹ + (d−1)b² + … + 1·b^d

At **b = 10, d = 5**: BFS generates **111,111** nodes; IDS generates
**123,456**. **About 11% more work** — and IDS uses **O(bd)** memory instead of
O(b^d).

**Why the repetition is cheap:** in a tree with branching factor b, the bottom
level holds most of the nodes. Regenerating all the levels above it costs
almost nothing by comparison.

**IDS is the preferred uninformed strategy when the depth is unknown**, and
that sentence is the answer to "which uninformed search would you use?"

---

## 2.6 Uniform Cost Search

**Expand the node with the lowest path cost g(n).** Priority queue.

- **Complete and optimal**, provided every step cost is ≥ ε > 0.
- **UCS is Dijkstra's algorithm** — the same procedure, arrived at from the AI
  side rather than the graph-theory side. Course 3 met it as Dijkstra.

### ⚠️ Two details that separate UCS from BFS, and both are examined

1. **The goal test happens on expansion, not generation.** A goal found early
   may be reached by a cheaper path later, so UCS must not stop until the goal
   is *removed from the frontier*.
2. **If a better path to a frontier node is found, replace it.**

**With equal step costs, UCS degenerates to BFS** — with the goal test moved,
which is why UCS is slightly slower on such problems.

---

## 2.7 The three strategies compared — measured

Russell and Norvig's Romania map, **Arad → Bucharest**, computed in
`03_uninformed_search.py`:

| Strategy | Nodes expanded | Path cost | Path |
|---|---:|---:|---|
| **BFS** | 9 | **450** | Arad → Sibiu → Fagaras → Bucharest |
| **DFS** | **6** | **607** | Arad → Zerind → Oradea → Sibiu → Fagaras → Bucharest |
| **Uniform cost** | **13** | **418** | Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucharest |

### 💡 Read that table carefully — every row makes a different point

- **BFS finds the path with the fewest *edges* (3), not the cheapest.** 450 km
  against the optimal 418. Step costs are unequal here, so BFS is not optimal —
  exactly as the property table says.
- **DFS expanded the fewest nodes and found the worst path**, 607 km, wandering
  through Zerind and Oradea. Cheap search, expensive answer.
- **UCS found the optimal 418** and paid for it: **13 nodes expanded**, the most
  of the three.

**The optimal route goes through Rimnicu Vilcea and Pitesti — and neither BFS
nor DFS finds it.** Only UCS, which is looking at cost rather than depth.

**That trade — work now against quality of answer — is the whole of Unit 3's
motivation.** A* (§3.3) gets the same 418 while expanding only **6** nodes, and
that number is why heuristics exist.

---

## Practice problems

### Problem 1

Define a search problem and formulate the water jug problem. Give a solution.
*(10 marks)*

**Solution.**

**The five components:** initial state; Actions(s); the transition model
Result(s, a); the goal test; and path cost. Add that a **solution** is an
action sequence from initial state to goal, and an **optimal solution** is one
of lowest cost.

**The formulation.** Two jugs, 4 litres and 3 litres, unmarked; measure exactly
2 litres.

- **State:** (x, y) where x is litres in the 4-jug and y in the 3-jug, with
  x ∈ {0..4}, y ∈ {0..3} — so **20 states**
- **Initial state:** (0, 0)
- **Goal test:** x = 2
- **Actions (six):** fill the 4-jug; fill the 3-jug; empty the 4-jug; empty the
  3-jug; pour 4→3 until one is empty or full; pour 3→4 likewise
- **Path cost:** 1 per action

**A solution:**

| Step | Action | State |
|---|---|---|
| 0 | — | (0, 0) |
| 1 | Fill the 3-jug | (0, 3) |
| 2 | Pour 3 → 4 | (3, 0) |
| 3 | Fill the 3-jug | (3, 3) |
| 4 | Pour 3 → 4 (only 1 fits) | (4, 2) |
| 5 | Empty the 4-jug | (0, 2) |
| 6 | Pour 3 → 4 | **(2, 0)** ✓ |

**Six actions.** Add the point that the state space is small and finite, so
**BFS is guaranteed to find the shortest solution** here — and that
representing the state as a *pair* rather than as a list of pouring events is
what makes it a manageable problem at all.

### Problem 2

Compare BFS, DFS and uniform cost search on completeness, optimality, time and
space. Illustrate with a worked example. *(10 marks)*

**Solution.**

Give the property table, defining b, d, m, C* and ε:

| | Complete? | Optimal? | Time | Space |
|---|---|---|---|---|
| BFS | Yes | **Only if step costs are equal** | O(b^d) | **O(b^d)** |
| DFS | **No** | No | O(b^m) | **O(bm)** |
| UCS | Yes | **Yes** | O(b^(1+⌊C*/ε⌋)) | same |

**Then the worked comparison**, which is what earns the top marks. On the
Romania map, Arad → Bucharest:

| Strategy | Expanded | Cost |
|---|---:|---:|
| BFS | 9 | 450 |
| DFS | **6** | **607** |
| UCS | **13** | **418** |

- BFS found the fewest-*edges* path (3 edges) but **not the cheapest** — step
  costs are unequal, so its optimality guarantee does not apply.
- **DFS expanded fewest and found the worst answer**, wandering via Zerind and
  Oradea.
- **UCS found the optimal 418** and expanded the most.

**State the trade-off explicitly:** DFS is cheap in memory (O(bm), linear) and
gives no guarantees; BFS guarantees the shallowest goal at exponential memory
cost; UCS guarantees the cheapest and does the most work. Note that
**UCS is Dijkstra's algorithm**, and that with equal step costs it degenerates
to BFS.

Finish with **iterative deepening** as the practical compromise: complete and
optimal like BFS, linear memory like DFS, and at b=10, d=5 it generates
**123,456** nodes against BFS's **111,111** — only about **11% more**.

### Problem 3

Explain the 8-puzzle as a search problem. How large is its state space, and
what fraction of configurations are solvable? *(5 marks)*

**Solution.**

**Formulation:** state is the arrangement of eight tiles and a blank on a 3×3
grid; actions move the **blank** up, down, left or right; the transition model
swaps the blank with the adjacent tile; the goal test compares against the
target arrangement; path cost is 1 per move.

**Say why the blank moves rather than the tiles:** it gives at most **four**
actions per state instead of up to eight with a legality check on each —
halving the branching factor, which is the base of an exponential.

**State space size:** 9! = 362,880 arrangements, but **only 9!/2 = 181,440 are
reachable** from any given configuration. Legal moves preserve the **parity of
the number of inversions**, so the arrangements split into two classes that
cannot reach each other.

**Therefore exactly half of all random scrambles are unsolvable.** Check
solvability by counting inversions *before* searching — otherwise the algorithm
correctly explores all 181,440 states and reports failure, very slowly.

Add the distinction: the **state space** is finite at 181,440, but the **search
tree is infinite**, because you can move left and right for ever. That gap is
why graph search keeps an **explored set**.

---

## Exam questions from this unit

**Two marks**

1. Name the five components of a search problem.
2. What is the difference between the state space and the search tree?
3. What does "complete" mean for a search strategy?
4. What is the space complexity of DFS?
5. Which uninformed search is equivalent to Dijkstra's algorithm?
6. Why does uniform cost search test for the goal on expansion?

**Five marks**

1. Formulate the vacuum cleaner world as a search problem.
2. Explain iterative deepening and why it is not wasteful.
3. Explain the 8-puzzle, its state space size and solvability.
4. Distinguish tree search from graph search.
5. Compare BFS and DFS on all four properties.

**Ten marks**

1. Define a search problem and formulate the water jug problem with a solution.
2. Compare BFS, DFS and UCS with a worked example.
3. Explain uninformed search strategies and their complexity, with the
   comparison table.

---

## Mistakes that cost marks

- **Saying BFS is optimal.** Only when **all step costs are equal**. On Romania
  it returns 450 against the optimal 418.
- **Saying DFS is complete.** It is not — infinite branches and cycles.
- **Forgetting that DFS's virtue is memory.** O(bm) linear, against BFS's
  exponential.
- **Claiming BFS is impractical because it is slow.** The binding constraint is
  **memory**.
- **Testing UCS's goal on generation.** A cheaper path to the same goal may
  come later.
- **Confusing state space with search tree.** 181,440 states; an infinite tree.
- **Saying iterative deepening wastes most of its work.** About 11% at b=10,
  d=5, because the bottom level dominates.
- **Formulating the 8-puzzle by moving tiles.** Move the blank — half the
  branching factor.
