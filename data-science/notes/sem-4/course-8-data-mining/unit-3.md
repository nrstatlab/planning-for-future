# Unit 3 — Association Analysis

**Syllabus topics:** Association Rules — What is an Association Rule?,
Methods to Discover Association Rules, A Priori Algorithm, Partition Algorithm,
Pincer-Search Algorithm, Dynamic Itemset Counting Algorithm, FP-Tree Growth
Algorithm, Generalized Association Rule, Association Rules with Item
Constraints.

---

## 3.1 What an association rule is

### 🎯 The big idea

An association rule says **"transactions containing X tend also to contain Y"**
— written `X → Y`. It is not a prediction and not a causal claim; it is a
statement about co-occurrence that happens often enough, and reliably enough,
to be worth acting on.

The canonical setting is the **market basket**: each transaction is one
customer's shopping trip, and each item is a product.

| TID | Items |
|:---:|---|
| T1 | bread, milk |
| T2 | bread, nappies, beer, eggs |
| T3 | milk, nappies, beer, cola |
| T4 | bread, milk, nappies, beer |
| T5 | bread, milk, nappies, cola |

### Vocabulary

| Term | Meaning |
|---|---|
| **Item** | One product — `bread` |
| **Itemset** | A set of items — `{bread, milk}` |
| **k-itemset** | An itemset of size k |
| **Transaction** | One basket, with a TID |
| **Support count σ(X)** | How many transactions contain X |
| **Support s(X)** | σ(X) / N — the *fraction* |
| **Frequent itemset** | An itemset with support ≥ minsup |
| **Association rule** | X → Y where X ∩ Y = ∅ |
| **Antecedent / consequent** | X (LHS) / Y (RHS) |

### ⚠️ X and Y must be disjoint

`{bread, milk} → {milk}` is not a valid rule. The consequent must contain no
item from the antecedent, or the "rule" is trivially true and says nothing.

## 3.2 Support, confidence and lift

### 🔢 The three formulas

```
support(X → Y)    = σ(X ∪ Y) / N              "how often does this happen?"

confidence(X → Y) = σ(X ∪ Y) / σ(X)           "when X happens, how often does Y?"
                  = support(X ∪ Y) / support(X)

lift(X → Y)       = confidence(X → Y) / support(Y)
                  = support(X ∪ Y) / (support(X) × support(Y))
```

Note that `support(X ∪ Y)` means transactions containing **both** X and Y —
the union of the *itemsets*, which corresponds to the *intersection* of the
transaction sets. Students misread this constantly.

| Measure | Range | Interpretation |
|---|---|---|
| **Support** | [0, 1] | Frequency — is this worth caring about? |
| **Confidence** | [0, 1] | Reliability — a conditional probability P(Y \| X) |
| **Lift** | [0, ∞) | **Interest** — >1 positive, =1 independent, <1 negative |

### 🔢 Worked example

From the five transactions above, evaluate `{milk, nappies} → {beer}`.

```
N = 5

σ({milk, nappies})       = T3, T4, T5           = 3
σ({milk, nappies, beer}) = T3, T4               = 2
σ({beer})                = T2, T3, T4           = 3

support    = 2/5                    = 0.40
confidence = 2/3                    = 0.667
lift       = 0.667 / (3/5) = 0.667 / 0.6 = 1.111
```

**Reading it:** the combination occurs in 40% of baskets; when milk and nappies
are both bought, beer follows two-thirds of the time; and that is 1.11× the
rate at which beer is bought generally. Positive, but weakly so.

### ⚠️ Confidence alone is misleading

This is the most important idea in the unit, and it is a guaranteed exam
question.

Suppose 800 of 1,000 students play cricket and 900 study data science, with 720
doing both.

```
{cricket} → {data science}

support    = 720/1000                    = 0.72   ← looks strong
confidence = 720/800                     = 0.90   ← looks very strong
lift       = 0.90 / (900/1000) = 0.90/0.90 = 1.00 ← INDEPENDENT
```

The rule looks excellent by support and confidence and is **worthless**: 90%
of all students study data science anyway, so knowing they play cricket tells
you nothing. Confidence is high only because the consequent is common.

**Lift corrects for this**, and it is why every serious analysis reports it.
Make the numbers slightly worse — 700 of the 800 cricketers — and lift falls to
0.875/0.9 = 0.972, a *negative* association hiding behind 87.5% confidence.

### Other interest measures

| Measure | Formula | Note |
|---|---|---|
| **Lift** | s(X∪Y) / (s(X)·s(Y)) | Symmetric: lift(X→Y) = lift(Y→X) |
| **Leverage** | s(X∪Y) − s(X)·s(Y) | Absolute difference from independence; range [−0.25, 0.25] |
| **Conviction** | (1 − s(Y)) / (1 − conf(X→Y)) | ∞ when confidence is 1; **directional** |
| **Cosine** | s(X∪Y) / √(s(X)·s(Y)) | Null-invariant |
| **Jaccard** | s(X∪Y) / (s(X) + s(Y) − s(X∪Y)) | Null-invariant |

**Support and lift are symmetric; confidence and conviction are not.** So
`X → Y` and `Y → X` always share a support and a lift but generally differ in
confidence — which is how you tell the direction of a rule.

## 3.3 The problem, and why it is hard

Finding rules is a two-step process:

1. **Find all frequent itemsets** — those with support ≥ minsup. *This is the
   expensive step.*
2. **Generate strong rules from them** — those with confidence ≥ minconf. This
   is cheap by comparison.

### 🔢 Why step 1 is expensive

With *d* items there are **2ᵈ − 1** possible non-empty itemsets.

| d items | Candidate itemsets |
|---:|---:|
| 5 | 31 |
| 10 | 1,023 |
| 20 | 1,048,575 |
| 100 | ≈ 1.27 × 10³⁰ |

A supermarket stocks tens of thousands of products. Brute-force enumeration is
not slow — it is **physically impossible**. Every algorithm in this unit is a
strategy for avoiding that enumeration.

### Total possible rules

From *d* items the number of possible rules is **3ᵈ − 2^(d+1) + 1**. For
d = 6 that is 729 − 128 + 1 = **602** rules. The exponential in the base 3
comes from each item being in the antecedent, the consequent, or neither.

## 3.4 The Apriori algorithm

### 🎯 The Apriori principle

> **If an itemset is frequent, all of its subsets are frequent.**
>
> Equivalently (the contrapositive, which is the useful form):
> **if an itemset is infrequent, all of its supersets are infrequent.**

This is called the **anti-monotone property** of support, and it holds because
adding an item to an itemset can only ever *reduce* the number of transactions
containing it:

```
X ⊆ Y  ⟹  support(X) ≥ support(Y)
```

**The consequence is pruning.** If `{beer, bread}` is infrequent, then
`{beer, bread, milk}`, `{beer, bread, eggs}` and every other superset can be
eliminated **without counting them at all**. That single observation is what
makes association mining feasible.

```
                    {}
        ┌───────┬────┴───┬───────┐
       {A}     {B}      {C}     {D}
      ┌──┴──┬───┴──┬─────┴──┐
    {A,B}  {A,C}  {A,D}  {B,C} {B,D} {C,D}
      │      │             ╳     ╳     ╳     ← {B,C} infrequent...
   {A,B,C} {A,B,D} …       ╳╳╳╳╳╳╳╳╳╳╳╳     ← ...so ALL its supersets pruned
```

### The algorithm

```
L₁ = {frequent 1-itemsets}                    (one pass over the data)
k = 2
while L(k-1) is not empty:
    Cₖ = apriori_gen(L(k-1))                  ← join, then prune
    for each transaction t in D:              ← ONE pass per level
        for each candidate c in Cₖ:
            if c ⊆ t: c.count++
    Lₖ = { c in Cₖ : c.count ≥ minsup_count }
    k++
return the union of all Lₖ
```

**`apriori_gen` has two parts:**

- **Join step.** Join L(k−1) with itself: two (k−1)-itemsets combine if their
  first k−2 items are identical. (Keeping the items sorted is what makes this
  work and avoids generating each candidate twice.)
- **Prune step.** Discard any candidate having *any* (k−1)-subset not in
  L(k−1). This is the Apriori principle applied before counting.

### 🔢 A full worked trace

Transactions, with **minsup = 60%**, so minimum support count = 0.6 × 5 = **3**:

| TID | Items |
|:---:|---|
| T1 | A, C, D |
| T2 | B, C, E |
| T3 | A, B, C, E |
| T4 | B, E |
| T5 | A, B, C, E |

**Pass 1 — C₁ → L₁**

| Itemset | Count | ≥ 3? |
|---|:---:|:---:|
| {A} | 3 (T1,T3,T5) | ✓ |
| {B} | 4 (T2,T3,T4,T5) | ✓ |
| {C} | 4 (T1,T2,T3,T5) | ✓ |
| {D} | 1 (T1) | ✗ **pruned** |
| {E} | 4 (T2,T3,T4,T5) | ✓ |

**L₁ = {A}, {B}, {C}, {E}**. D is gone, and with it every itemset containing D
— which is 15 of the 31 possible itemsets, eliminated after one pass.

**Pass 2 — C₂ → L₂**

Join L₁ with itself: C₂ = {A,B}, {A,C}, {A,E}, {B,C}, {B,E}, {C,E}. No pruning
is possible at k=2 (all 1-subsets are in L₁).

| Itemset | Transactions | Count | ≥ 3? |
|---|---|:---:|:---:|
| {A,B} | T3, T5 | 2 | ✗ |
| {A,C} | T1, T3, T5 | 3 | ✓ |
| {A,E} | T3, T5 | 2 | ✗ |
| {B,C} | T2, T3, T5 | 3 | ✓ |
| {B,E} | T2, T3, T4, T5 | 4 | ✓ |
| {C,E} | T2, T3, T5 | 3 | ✓ |

**L₂ = {A,C}, {B,C}, {B,E}, {C,E}**

**Pass 3 — C₃ → L₃**

*Join:* sorted itemsets sharing their first item —
{A,C} ⋈ nothing (no other itemset starts with A);
{B,C} ⋈ {B,E} → **{B,C,E}**.

*Prune:* the 2-subsets of {B,C,E} are {B,C} ✓, {B,E} ✓, {C,E} ✓ — all in L₂,
so it survives.

Note the pruning that did *not* need to happen: **{A,C,E}** would arise from a
naive join, but {A,E} ∉ L₂, so it is eliminated **without a single count**.
That is the Apriori principle earning its keep.

| Itemset | Transactions | Count | ≥ 3? |
|---|---|:---:|:---:|
| {B,C,E} | T2, T3, T5 | 3 | ✓ |

**L₃ = {B,C,E}**

**Pass 4** — L₃ has only one itemset, so no join is possible. **C₄ = ∅** and
the algorithm stops.

**Frequent itemsets:** {A}, {B}, {C}, {E}, {A,C}, {B,C}, {B,E}, {C,E}, {B,C,E}
— nine of the 31 possible, found in four passes.

### 🔢 Rule generation from {B,C,E}

For each frequent itemset of size ≥ 2, consider every way of splitting it into
a non-empty antecedent and consequent. A k-itemset yields **2ᵏ − 2** candidate
rules — here 2³ − 2 = **6**.

σ({B,C,E}) = 3, so every rule has support 3/5 = 0.60. With **minconf = 80%**:

| Rule | Confidence | ≥ 0.8? |
|---|---|:---:|
| {B,C} → {E} | 3/3 = **1.00** | ✓ |
| {B,E} → {C} | 3/4 = 0.75 | ✗ |
| {C,E} → {B} | 3/3 = **1.00** | ✓ |
| {B} → {C,E} | 3/4 = 0.75 | ✗ |
| {C} → {B,E} | 3/4 = 0.75 | ✗ |
| {E} → {B,C} | 3/4 = 0.75 | ✗ |

**Two strong rules:** `{B,C} → {E}` and `{C,E} → {B}`, both with confidence
1.00.

Their lifts: `lift({B,C}→{E}) = 1.00 / (4/5) = 1.25`, and
`lift({C,E}→{B}) = 1.00 / (4/5) = 1.25`. Both positive.

### 💡 Confidence is anti-monotone within an itemset

Moving items from the antecedent to the consequent can only *lower* confidence.
So if `{B} → {C,E}` fails, then `{} → {B,C,E}` would too — and more usefully,
if `{B,C} → {E}` fails, every rule whose consequent is a superset of {E} drawn
from this itemset fails. This lets rule generation prune too, level by level on
the consequent size.

### Complexity and weaknesses

| | |
|---|---|
| Database passes | **k+1**, where k is the largest frequent itemset |
| Main cost | Repeated scanning; candidate generation at k=2 |
| Memory | Must hold Cₖ |

**Apriori's two weaknesses**, both examined:

1. **Too many candidates.** With 10⁴ frequent 1-itemsets, C₂ has about
   10⁴ × 10⁴ / 2 = **5 × 10⁷** candidates. The k=2 step is usually the
   bottleneck.
2. **Too many database scans.** Finding a frequent 20-itemset needs 21 passes
   over data that may be far larger than memory.

Every remaining algorithm in this unit attacks one of those two problems.

## 3.5 The Partition algorithm

### 🎯 The idea

**Two database scans, always, regardless of itemset size.**

Divide the database into *p* partitions, each small enough to fit in memory.

```
Scan 1:  for each partition i:
             find ALL locally frequent itemsets in partition i
             (in memory, with minsup applied to that partition's size)
         global candidates = UNION of all local frequent itemsets

Scan 2:  count every global candidate over the WHOLE database
         keep those meeting global minsup
```

### 🔢 Why the union is safe — the completeness argument

This is the exam question, and the argument is short:

> Let X be globally frequent, so σ(X) ≥ minsup × N. Suppose X is locally
> frequent in **no** partition. Then in every partition i, σᵢ(X) < minsup × Nᵢ.
> Summing over all partitions:
> `σ(X) = Σ σᵢ(X) < minsup × Σ Nᵢ = minsup × N` — contradicting X being
> globally frequent.

**Therefore any globally frequent itemset must be locally frequent in at least
one partition**, so the union of local frequent itemsets is a **superset** of
the true answer. No false negatives. Scan 2 removes the false positives.

| | Apriori | Partition |
|---|---|---|
| Database scans | k+1 | **2** |
| Memory | Candidates only | One partition at a time |
| False positives | None | Many, removed in scan 2 |
| Parallelisable | Poorly | **Naturally** — one partition per node |

**Its weakness:** if the partitions are not representative — say, transactions
arrive sorted by date and seasonal items cluster — the union of local frequent
itemsets becomes enormous, and scan 2 counts a huge candidate set. Random
partitioning mitigates this.

## 3.6 The Pincer-Search algorithm

### 🎯 The idea

Search **from both ends at once**. Apriori works bottom-up, level by level; if
the longest frequent itemset has 20 items, that is 21 passes. Pincer-Search
adds a **top-down** search that can identify long frequent itemsets early.

It maintains two structures:

| Structure | Meaning |
|---|---|
| **Lₖ** | Frequent k-itemsets, found bottom-up as in Apriori |
| **MFCS** | Maximal Frequent Candidate Set — the current top-down guess |
| **MFS** | Maximal Frequent Set — maximal itemsets confirmed frequent |

A **maximal frequent itemset** is a frequent itemset with **no frequent
superset**. Knowing the maximal ones implicitly gives you all the frequent
ones, since every subset of a maximal frequent itemset is frequent.

```
MFCS starts as the single itemset containing ALL items.
Each pass:
    count Cₖ (bottom-up) AND the members of MFCS (top-down)
    any MFCS member found frequent  → move to MFS; its subsets need no counting
    any infrequent itemset found    → SPLIT the MFCS members containing it
```

### 💡 When it wins and when it loses

**It wins** when there are a few long frequent itemsets — the top-down search
confirms one 15-itemset in an early pass and Apriori's next thirteen levels
become unnecessary.

**It loses** when frequent itemsets are short and numerous: the top-down search
does work that never pays off, and the MFCS splits repeatedly. In the worst
case it does strictly more work than Apriori.

That conditional answer — "it depends on whether the frequent itemsets are long"
— is what a five-mark question is looking for.

### ⚠️ Maximal versus closed itemsets

Another guaranteed two-mark question.

| | **Maximal** frequent itemset | **Closed** frequent itemset |
|---|---|---|
| Definition | No **frequent** superset | No superset with the **same support** |
| Recovers | Which itemsets are frequent | Which are frequent **and their supports** |
| Count | Fewest | More than maximal, fewer than all |
| Lossy? | **Yes** — supports are lost | **No** — lossless |

Every maximal itemset is closed; the converse is false.

**Worked example.** Suppose {A,B} has support 3, {A,B,C} has support 3, and
{A,B,C,D} has support 1 with minsup 2.

- {A,B,C} is **maximal** — its only superset {A,B,C,D} is infrequent.
- {A,B} is **not closed** — its superset {A,B,C} has the *same* support 3.
- {A,B,C} is **closed** and maximal.

So from the maximal set alone you know {A,B} is frequent but not that its
support is 3. The closed set preserves that.

## 3.7 Dynamic Itemset Counting (DIC)

### 🎯 The idea

Apriori counts itemsets of size k throughout a whole pass, then starts on
k+1. **DIC starts counting an itemset as soon as all its subsets are known to
be frequent** — even in the middle of a pass.

The database is divided into intervals of M transactions. At every interval
boundary, DIC re-evaluates what it should be counting. Itemsets move between
four states:

| State | Meaning |
|---|---|
| **Dashed circle** | Suspected frequent, still being counted |
| **Dashed square** | Suspected infrequent, still being counted |
| **Solid circle** | Confirmed frequent — counting finished |
| **Solid square** | Confirmed infrequent — counting finished |

```
Transactions:  |--M--|--M--|--M--|--M--|--M--|  (wraps around to the start)
Start counting  1-sets
       at M:    + any 2-set whose 1-subsets already look frequent
      at 2M:    + any 3-set whose 2-subsets already look frequent   ...
```

An itemset that began counting mid-pass keeps counting past the end of the
database, **wrapping around** to the beginning, until it has seen all N
transactions. That is what makes its final count correct.

### The trade-off

| | Apriori | DIC |
|---|---|---|
| Scans | k+1 | Typically **2 or fewer** (in wrapped equivalents) |
| Bookkeeping | Simple | Complex — four states, wrap-around |
| Works best when | Any data | Data is **homogeneous** — early transactions resemble later ones |

**DIC's assumption is its weakness.** It decides an itemset "looks frequent"
from a prefix of the data. If the data is sorted — by date, by store, by
category — that prefix is unrepresentative, DIC starts counting the wrong
itemsets, and it can perform worse than Apriori. **Shuffling the data first is
not optional.**

## 3.8 The FP-Growth algorithm

### 🎯 The idea

**Generate no candidates at all.** Compress the database into a tree, then
mine the tree recursively. Two database scans, and no candidate generation
anywhere.

### Step 1 — Build the FP-tree

**Scan 1:** count each item's support, discard infrequent items, and sort the
rest by descending frequency (the **F-list**).

**Scan 2:** for each transaction, drop infrequent items, sort the rest into
F-list order, and insert the resulting path into the tree, incrementing counts
where a prefix already exists.

### 🔢 A full worked trace

Same data, **minsup count = 3**:

| TID | Items |
|:---:|---|
| T1 | A, C, D |
| T2 | B, C, E |
| T3 | A, B, C, E |
| T4 | B, E |
| T5 | A, B, C, E |

**Scan 1:** counts are A:3, B:4, C:4, D:1, E:4. **D is dropped** (1 < 3).

F-list, descending by count, ties broken alphabetically:
**B:4, C:4, E:4, A:3**

**Scan 2** — reorder each transaction into F-list order:

| TID | Original | Filtered and ordered |
|:---:|---|---|
| T1 | A, C, D | **C, A** |
| T2 | B, C, E | **B, C, E** |
| T3 | A, B, C, E | **B, C, E, A** |
| T4 | B, E | **B, E** |
| T5 | A, B, C, E | **B, C, E, A** |

**The resulting FP-tree:**

```
                    null
                   /    \
              B:4        C:1
             /   \          \
         C:3      E:1        A:1
          |
         E:3
          |
         A:2
```

Reading it: T2, T3 and T5 all start `B, C, E`, so they share that path with
count 3; T3 and T5 continue to A, giving A:2. T4 is `B, E`, which diverges
after B, giving the separate `E:1` child. T1 is `C, A`, which shares no prefix
with B at all, so it hangs off the root as its own branch.

**The header table** links every node of the same item:

| Item | Count | → node links |
|---|:---:|---|
| B | 4 | B:4 |
| C | 4 | C:3 → C:1 |
| E | 4 | E:3 → E:1 |
| A | 3 | A:2 → A:1 |

**Why sort by descending frequency?** So that frequent items share prefixes
near the root, which is what makes the tree small. Sorting ascending would
produce a tree close to the size of the original database and defeat the
purpose.

### Step 2 — Mine the tree, from the least frequent item upwards

For each item, find its **conditional pattern base** (the prefix paths ending
at that item, with counts), build a **conditional FP-tree**, and recurse.

**Item A** (count 3, the last in the F-list):

```
Paths ending in A:  B:C:E:A with count 2   → prefix {B, C, E} : 2
                    C:A     with count 1   → prefix {C}       : 1

Conditional pattern base of A = { {B,C,E}: 2, {C}: 1 }

Counts within that base: B:2, C:3, E:2
Only C ≥ 3, so the conditional FP-tree for A is a single node C:3.

Frequent patterns ending in A:  {A}: 3,  {C,A}: 3
```

**Item E** (count 4):

```
Paths ending in E:  B:C:E with count 3  → prefix {B, C} : 3
                    B:E   with count 1  → prefix {B}    : 1

Conditional pattern base of E = { {B,C}: 3, {B}: 1 }
Counts: B:4, C:3 — both ≥ 3.

Conditional FP-tree for E:  B:4 → C:3

Mining it recursively gives:  {E}: 4,  {B,E}: 4,  {C,E}: 3,  {B,C,E}: 3
```

**Item C** (count 4):

```
Paths ending in C:  B:C with count 3 → prefix {B}: 3
                    C:1              → prefix {} : 1
Counts: B:3 ≥ 3.
Frequent patterns:  {C}: 4,  {B,C}: 3
```

**Item B** (count 4, first in the F-list, so no prefixes): `{B}: 4`

**Collected result:** {A}:3, {B}:4, {C}:4, {E}:4, {C,A}:3, {B,C}:3, {C,E}:3,
{B,E}:4, {B,C,E}:3.

**Nine frequent itemsets — identical to Apriori's answer.** Note that Apriori
wrote {A,C} and FP-Growth writes {C,A}; itemsets are unordered, so these are
the same set. **The two algorithms must always agree**; they differ only in how
they get there.

### 🔢 Apriori versus FP-Growth

| | **Apriori** | **FP-Growth** |
|---|---|---|
| Candidate generation | **Yes** — the bottleneck | **None** |
| Database scans | k + 1 | **2** |
| Data structure | Hash tree of candidates | **FP-tree** |
| Strategy | Breadth-first, level-wise | **Depth-first**, divide and conquer |
| Memory | Candidates | The whole tree — must fit |
| Speed | Slower | Typically an **order of magnitude** faster |
| Dense data | Poor | **Good** — high compression |
| Sparse data | Acceptable | Tree barely compresses |
| Implementation | **Simple** | Complex |

**FP-Growth's weakness is memory.** The tree must fit in RAM. On sparse data
with little prefix sharing, the tree can approach the size of the database
itself and the advantage disappears. Apriori's memory need is bounded by the
candidate set, not the data.

## 3.9 Generalized association rules

### 🎯 The idea

Items usually live in a **taxonomy** — a concept hierarchy — and interesting
rules may exist at a higher level than the individual product.

```
                    Food
            ┌────────┴────────┐
        Dairy               Bakery
      ┌───┴───┐           ┌───┴────┐
   Milk    Cheese      Bread   Croissant
   ┌─┴──┐
 Amul  Nandini
```

No single brand of milk may reach minsup, yet **Dairy → Bakery** may be a
strong rule. Generalized (multi-level) association mining searches the
hierarchy, not just the leaves.

### 🔢 Support monotonicity in a taxonomy

**An ancestor's support is at least the sum of its descendants' supports** —
at least, not equal, because one transaction containing both Amul and Nandini
milk counts twice at the leaf level and once at `Milk`.

That gives the pruning rule: **if an ancestor is infrequent, every descendant
is infrequent**, so whole subtrees can be discarded.

### The three strategies

| Strategy | minsup by level | Effect |
|---|---|---|
| **Uniform** | Same at every level | Simple; too high for leaves *or* too low for the root — you cannot win |
| **Reduced** | Lower at deeper levels | The usual practical choice |
| **Group-based** | Set per subtree by domain knowledge | Best results, most effort |

**Uniform support's dilemma is the exam point.** Set minsup high enough to
control the number of `Dairy → Bakery`-level rules and no individual product
passes; set it low enough for products and the upper levels produce an
unmanageable flood. Reduced support exists precisely because one threshold
cannot serve both.

### ⚠️ Redundant ancestor rules

If `Milk → Bread` has confidence 80%, and `Amul Milk` is 25% of all milk, then
`Amul Milk → Bread` at confidence ≈ 80% tells you **nothing new** — it is the
*expected* consequence of the ancestor rule.

A descendant rule is **redundant** if its support and confidence are close to
what the ancestor rule predicts. Only report a descendant rule when it
*deviates* — if `Amul Milk → Bread` had confidence 95%, that is a real finding.

## 3.10 Association rules with item constraints

Unconstrained mining produces far too many rules, most of them uninteresting.
**Constraints** let the user say what they are looking for — and, crucially,
good constraints can be **pushed into** the mining algorithm rather than
applied to its output, which is where the speed comes from.

| Constraint type | Example |
|---|---|
| **Item** | Rules must contain `beer` |
| **Knowledge-type** | Find associations, not correlations |
| **Data** | Only Vijayawada stores, only Q1 |
| **Dimension/level** | Rules at the category level only |
| **Interestingness** | minsup ≥ 2%, minconf ≥ 60%, lift > 1.2 |
| **Rule form** | At most 3 items in the antecedent |
| **Aggregate** | Total basket value > ₹500 |

### 🔢 Anti-monotone, monotone and succinct

The classification determines *whether the constraint can be pushed into the
algorithm*, which is the whole point.

| Property | Definition | Example | Can prune early? |
|---|---|---|---|
| **Anti-monotone** | If an itemset violates it, so does every superset | `sum(price) ≤ 100`, `support ≥ minsup` | **Yes — like Apriori** |
| **Monotone** | If an itemset satisfies it, so does every superset | `sum(price) ≥ 100`, `count ≥ 3` | Yes — stop checking once satisfied |
| **Succinct** | Satisfying itemsets can be enumerated directly from the items | `min(price) ≤ 50` | **Yes — generate only valid candidates** |
| **Convertible** | Becomes anti- or monotone if items are ordered suitably | `avg(price) ≤ 100` | Yes, after sorting |

**Worked example.** `sum(price) ≤ ₹100` is **anti-monotone**: if
{bread, milk} already costs ₹120, no superset can cost less, so the entire
subtree is pruned — exactly the Apriori mechanism, applied to price instead of
support.

`sum(price) ≥ ₹100` is **monotone**: once satisfied, adding items keeps it
satisfied, so the constraint need not be re-checked deeper.

`avg(price) ≤ ₹100` is neither — adding a cheap item can *lower* the average
and adding an expensive one raises it. But sort the items by price ascending
and it becomes convertible anti-monotone, which is why it is a separate
category.

**The practical point:** a constraint applied *after* mining saves the user
reading time. A constraint pushed *into* mining saves the computer's time,
often by orders of magnitude. The classification tells you which is possible.

---

## Practice problems

### Problem 1

Transactions, minsup count = 2, minconf = 70%:

| TID | Items |
|:---:|---|
| 1 | A, B, E |
| 2 | B, D |
| 3 | B, C |
| 4 | A, B, D |
| 5 | A, C |
| 6 | B, C |
| 7 | A, C |
| 8 | A, B, C, E |
| 9 | A, B, C |

(a) Run Apriori and list all frequent itemsets.
(b) Generate all strong rules from the largest frequent itemsets.
(c) Compute lift for two of them.

**Solution.** N = 9, minsup count = 2.

**Pass 1**

| Itemset | Count | ✓ |
|---|:---:|:---:|
| {A} | 6 (1,4,5,7,8,9) | ✓ |
| {B} | 7 (1,2,3,4,6,8,9) | ✓ |
| {C} | 6 (3,5,6,7,8,9) | ✓ |
| {D} | 2 (2,4) | ✓ |
| {E} | 2 (1,8) | ✓ |

**L₁ = {A}, {B}, {C}, {D}, {E}** — all five survive.

**Pass 2** — C₂ is all 10 pairs:

| Itemset | TIDs | Count | ✓ |
|---|---|:---:|:---:|
| {A,B} | 1, 4, 8, 9 | 4 | ✓ |
| {A,C} | 5, 7, 8, 9 | 4 | ✓ |
| {A,D} | 4 | 1 | ✗ |
| {A,E} | 1, 8 | 2 | ✓ |
| {B,C} | 3, 6, 8, 9 | 4 | ✓ |
| {B,D} | 2, 4 | 2 | ✓ |
| {B,E} | 1, 8 | 2 | ✓ |
| {C,D} | — | 0 | ✗ |
| {C,E} | 8 | 1 | ✗ |
| {D,E} | — | 0 | ✗ |

**L₂ = {A,B}, {A,C}, {A,E}, {B,C}, {B,D}, {B,E}**

**Pass 3** — join and prune:

| Candidate | 2-subsets | Survives prune? |
|---|---|:---:|
| {A,B,C} | {A,B}✓ {A,C}✓ {B,C}✓ | ✓ |
| {A,B,E} | {A,B}✓ {A,E}✓ {B,E}✓ | ✓ |
| {A,B,D} | {A,B}✓ **{A,D}✗** | **pruned, not counted** |
| {A,C,E} | {A,C}✓ {A,E}✓ **{C,E}✗** | **pruned** |
| {B,C,E} | {B,C}✓ {B,E}✓ **{C,E}✗** | **pruned** |
| {B,C,D} | {B,C}✓ **{C,D}✗** | **pruned** |
| {B,D,E} | {B,D}✓ {B,E}✓ **{D,E}✗** | **pruned** |

Five of seven candidates are eliminated without a single count. Only two are
counted:

| Itemset | TIDs | Count | ✓ |
|---|---|:---:|:---:|
| {A,B,C} | 8, 9 | 2 | ✓ |
| {A,B,E} | 1, 8 | 2 | ✓ |

**L₃ = {A,B,C}, {A,B,E}**

**Pass 4** — join gives {A,B,C,E}; its 3-subset {A,C,E} ∉ L₃, so it is pruned.
**C₄ = ∅**, stop.

**All frequent itemsets (13):** {A}, {B}, {C}, {D}, {E}, {A,B}, {A,C}, {A,E},
{B,C}, {B,D}, {B,E}, {A,B,C}, {A,B,E}

**(b) Rules from {A,B,C}** — support 2/9 = 0.222:

| Rule | Confidence | ≥ 0.7? |
|---|---|:---:|
| {A,B} → {C} | 2/4 = 0.50 | ✗ |
| {A,C} → {B} | 2/4 = 0.50 | ✗ |
| {B,C} → {A} | 2/4 = 0.50 | ✗ |
| {A} → {B,C} | 2/6 = 0.33 | ✗ |
| {B} → {A,C} | 2/7 = 0.286 | ✗ |
| {C} → {A,B} | 2/6 = 0.33 | ✗ |

**No strong rules from {A,B,C}.**

**Rules from {A,B,E}** — support 2/9 = 0.222:

| Rule | Confidence | ≥ 0.7? |
|---|---|:---:|
| {A,B} → {E} | 2/4 = 0.50 | ✗ |
| {A,E} → {B} | 2/2 = **1.00** | ✓ |
| {B,E} → {A} | 2/2 = **1.00** | ✓ |
| {A} → {B,E} | 2/6 = 0.33 | ✗ |
| {B} → {A,E} | 2/7 = 0.286 | ✗ |
| {E} → {A,B} | 2/2 = **1.00** | ✓ |

**Three strong rules:** `{A,E} → {B}`, `{B,E} → {A}`, `{E} → {A,B}`, each with
confidence 1.00.

**(c) Lift**

```
lift({A,E} → {B}) = 1.00 / (7/9) = 1.00 / 0.778 = 1.286
lift({E} → {A,B}) = 1.00 / (4/9) = 1.00 / 0.444 = 2.250
```

`{E} → {A,B}` is by far the more interesting: buyers of E are **2.25× more
likely** than average to buy A and B together. Note both rules have the same
confidence — **lift is what distinguishes them**, which is §3.2's lesson in
practice.

**A completeness note.** The question asked for rules from the *largest*
frequent itemsets. Mining the whole lattice also yields three strong rules from
**2-itemsets** — `{D} → {B}` (confidence 1.00, lift 1.286), `{E} → {A}` (1.00,
1.500) and `{E} → {B}` (1.00, 1.286). A real Apriori run reports these too, so
say "from the 3-itemsets" when your answer is scoped that way.

### Problem 2

Build the FP-tree for the data in Problem 1 with minsup count = 2, give the
header table, and mine the conditional pattern base for E.

**Solution.**

**Scan 1:** A:6, B:7, C:6, D:2, E:2 — all ≥ 2, none dropped.

**F-list** by descending count, alphabetical on ties:
**B:7, A:6, C:6, D:2, E:2**

**Scan 2** — reorder each transaction:

| TID | Original | Ordered |
|:---:|---|---|
| 1 | A, B, E | B, A, E |
| 2 | B, D | B, D |
| 3 | B, C | B, C |
| 4 | A, B, D | B, A, D |
| 5 | A, C | A, C |
| 6 | B, C | B, C |
| 7 | A, C | A, C |
| 8 | A, B, C, E | B, A, C, E |
| 9 | A, B, C | B, A, C |

**FP-tree:**

```
                     null
                   /      \
                B:7        A:2
              /  |  \         \
          A:4   C:2  D:1       C:2
         / | \
      E:1 D:1 C:2
               |
              E:1
```

Reading the B branch: transactions 1, 4, 8, 9 continue `B → A` (count 4); of
those, 8 and 9 go on to C (count 2), and 8 alone continues to E (count 1);
transaction 1 goes `B → A → E` (count 1) and 4 goes `B → A → D` (count 1).
Transactions 3 and 6 are `B → C` (count 2) and 2 is `B → D` (count 1).
Transactions 5 and 7 are `A → C`, sharing no prefix with B, so they form the
second root branch A:2 → C:2.

**Header table:**

| Item | Count | Node links |
|---|:---:|---|
| B | 7 | B:7 |
| A | 6 | A:4 → A:2 |
| C | 6 | C:2 (under B:A) → C:2 (under B) → C:2 (under A) |
| D | 2 | D:1 (under B:A) → D:1 (under B) |
| E | 2 | E:1 (under B:A) → E:1 (under B:A:C) |

**Conditional pattern base for E** — the two prefix paths ending at an E node:

```
From E:1 under B → A         →  {B, A} : 1
From E:1 under B → A → C     →  {B, A, C} : 1

Conditional pattern base of E = { {B,A}: 1, {B,A,C}: 1 }

Counts within the base:  B: 1+1 = 2 ✓,  A: 1+1 = 2 ✓,  C: 1 ✗

Conditional FP-tree for E:  B:2 → A:2
```

**Frequent patterns ending in E:** {E}:2, {B,E}:2, {A,E}:2, {B,A,E}:2 —
matching Apriori's {A,E}, {B,E} and {A,B,E}, as they must.

### Problem 3

In a survey of 1,000 people, 600 drink tea, 750 drink coffee and 400 drink
both. Evaluate `{tea} → {coffee}` on support, confidence and lift, and say
whether it should be reported.

**Solution.**

```
N = 1000
σ(tea) = 600,  σ(coffee) = 750,  σ(tea ∪ coffee) = 400

support    = 400/1000              = 0.40   (40%)
confidence = 400/600               = 0.667  (66.7%)
lift       = 0.667 / (750/1000) = 0.667 / 0.75 = 0.889
```

**No — it should not be reported as a positive rule.**

Support 40% and confidence 66.7% both look respectable, and both are
misleading. **Lift is 0.889, below 1**, which means tea drinkers are *less*
likely to drink coffee than the population at large: 66.7% against a baseline
of 75%.

The confidence is high only because coffee drinking is common. This is exactly
the failure mode of §3.2, and it is why lift must be reported alongside
confidence.

The finding is real and useful — it is a **negative** association, and worth
knowing — but stating `{tea} → {coffee}` as a discovered rule would invert its
meaning.

Check by leverage: 0.40 − (0.6 × 0.75) = 0.40 − 0.45 = **−0.05**, negative,
agreeing with lift.

---

## Exam questions from this unit

**Two marks**

1. Define support, confidence and lift.
2. State the Apriori principle.
3. What is the anti-monotone property?
4. Why is confidence alone misleading?
5. Distinguish a maximal from a closed frequent itemset.
6. How many itemsets are possible with d items?
7. How many rules can a frequent k-itemset generate?
8. Why does FP-Growth sort items by descending frequency?
9. What is a conditional pattern base?
10. Distinguish an anti-monotone from a monotone constraint.

**Five marks**

1. Explain the Apriori algorithm with a worked example.
2. Explain rule generation from frequent itemsets.
3. Explain the Partition algorithm and prove its completeness.
4. Explain Pincer-Search and when it outperforms Apriori.
5. Explain Dynamic Itemset Counting.
6. Explain generalized (multi-level) association rules.
7. Explain constraint-based mining and the constraint types.

**Ten marks**

1. Given a transaction database, apply Apriori fully — all passes, all
   candidate generation and pruning, all frequent itemsets, all strong rules
   with support, confidence and lift.
2. Construct an FP-tree for a given database and mine it completely, showing
   every conditional pattern base and conditional tree.
3. Compare Apriori and FP-Growth exhaustively, with a worked example of each
   on the same data.

## Mistakes that cost marks

- Reading `support(X ∪ Y)` as transactions containing X *or* Y
- Reporting confidence without lift
- Forgetting to divide by N — quoting support *counts* as support
- Writing a rule whose antecedent and consequent overlap
- Skipping the prune step of `apriori_gen` and counting candidates needlessly
- Generating only single-item consequents when asked for **all** rules
- Building the FP-tree without reordering transactions into F-list order
- Sorting the F-list ascending instead of descending
- Claiming FP-Growth generates candidates — it generates none
- Saying Apriori and FP-Growth can give different frequent itemsets
- Confusing maximal (no frequent superset) with closed (no superset of equal support)
- Forgetting that lift and support are symmetric while confidence is not
