"""Experiments 2-7 — List predicates, arithmetic, and the cut.

pytholog has NO LIST TERMS, NO ARITHMETIC EVALUATION and NO CUT, so these six
experiments cannot be run as logic programs here. That limitation is ASSERTED
below rather than described, and the same computations are then performed in
Python so the expected answers in the .pl files are checked.

The .pl files carry the real Prolog, and they are the lab deliverable.
"""
import pytholog as pl


def pytholog_has_no_lists():
    """Asserted, so this file can never quietly start claiming to test lists."""
    kb = pl.KnowledgeBase("lists")
    kb(["mem(X, [X|_])", "mem(X, [_|T]) :- mem(X, T)"])
    result = kb.query(pl.Expr("mem(b, [a,b,c])"))

    assert result == ["No"], result
    print("  pytholog: mem(b, [a,b,c]) -> ['No']  (SWI-Prolog answers 'true')")
    print("       there are no list TERMS, so [X|T] never unifies. Experiments")
    print("       2, 3 and 4 are executed in Python below; the .pl files carry")
    print("       the real Prolog")


def pytholog_has_no_arithmetic():
    kb = pl.KnowledgeBase("arith")
    kb(["fact(0, 1)", "fact(N, F) :- N1 is N-1, fact(N1, F1), F is N*F1"])
    result = kb.query(pl.Expr("fact(5, X)"))

    assert result == ["No"], result
    print("  pytholog: fact(5, X) -> ['No']  (SWI-Prolog answers X = 120)")
    print("       'is/2' does not evaluate, so experiments 5 and 6 are executed")
    print("       in Python too")


# --- experiment 2: member, append, reverse, length --------------------------

def list_predicates():
    """What the Prolog definitions compute, checked in Python."""
    xs = ["a", "b", "c"]
    ys = ["d", "e"]

    assert "b" in xs and "z" not in xs                     # member/2
    assert xs + ys == ["a", "b", "c", "d", "e"]            # append/3
    assert list(reversed(xs)) == ["c", "b", "a"]           # reverse/2
    assert len(xs) == 3                                    # length/2

    # append/3 is RELATIONAL: it can also split a list, which is the property
    # that makes Prolog different from a functional language.
    splits = [(xs[:i], xs[i:]) for i in range(len(xs) + 1)]
    assert len(splits) == 4
    assert splits[0] == ([], ["a", "b", "c"])
    assert splits[-1] == (["a", "b", "c"], [])

    print(f"  member(b, {xs})      -> true")
    print(f"  append({xs}, {ys}, X) -> {xs + ys}")
    print(f"  reverse({xs}, X)     -> {list(reversed(xs))}")
    print(f"  length({xs}, N)      -> {len(xs)}")
    print(f"  append(X, Y, {xs})   -> {len(splits)} solutions: {splits}")
    print("       that last one is the point of Prolog: append/3 RUNS BACKWARDS.")
    print("       One definition both concatenates and splits, because a rule")
    print("       states a RELATION rather than a function")


def maximum_of_a_list():
    """Experiment 3."""
    def maximum(xs):
        best = xs[0]
        for x in xs[1:]:
            if x > best:
                best = x
        return best

    assert maximum([3, 7, 2, 9, 4]) == 9
    assert maximum([5]) == 5
    assert maximum([-3, -7, -2]) == -2

    print(f"  max([3,7,2,9,4]) -> {maximum([3, 7, 2, 9, 4])}")
    print("       the Prolog version recurses on the tail and compares against")
    print("       the maximum of the rest. The base case is the ONE-element")
    print("       list, not the empty one -- max([]) has no answer")


def flatten_a_nested_list():
    """Experiment 4."""
    def flatten(x):
        if not isinstance(x, list):
            return [x]
        out = []
        for item in x:
            out.extend(flatten(item))
        return out

    nested = [1, [2, [3, 4], 5], [[6]], 7]
    assert flatten(nested) == [1, 2, 3, 4, 5, 6, 7]
    assert flatten([]) == []
    assert flatten([[], [[]], 1]) == [1], "empty lists vanish"

    print(f"  flatten({nested}) -> {flatten(nested)}")
    print(f"  flatten([[], [[]], 1]) -> {flatten([[], [[]], 1])}")
    print("       three clauses in Prolog: the empty list, a list head (recurse")
    print("       into it and append), and an atom head (keep it). Empty")
    print("       sublists disappear, which is the case people forget")


# --- experiments 5 and 6: arithmetic ----------------------------------------

def factorial_and_fibonacci():
    def fact(n):
        return 1 if n == 0 else n * fact(n - 1)

    def fib(n):
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    assert [fact(n) for n in range(6)] == [1, 1, 2, 6, 24, 120]
    assert [fib(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fact(10) == 3628800

    # Naive fib is exponential -- 177 calls for fib(10).
    calls = {"n": 0}

    def counted(n):
        calls["n"] += 1
        return n if n < 2 else counted(n - 1) + counted(n - 2)

    counted(10)
    assert calls["n"] == 177, calls["n"]

    print(f"  factorial 0..5 -> {[fact(n) for n in range(6)]}")
    print(f"  fibonacci 0..9 -> {[fib(n) for n in range(10)]}")
    print(f"  naive fib(10) makes {calls['n']} recursive calls")
    print("       the naive Prolog definition is exponential for the same")
    print("       reason. Add an accumulator, or use assertz/1 to memoise --")
    print("       which is Prolog's version of dynamic programming")


def gcd_by_recursion():
    """Experiment 6 -- Euclid's algorithm."""
    def gcd(a, b):
        return a if b == 0 else gcd(b, a % b)

    assert gcd(48, 18) == 6
    assert gcd(17, 5) == 1
    assert gcd(0, 7) == 7
    assert gcd(100, 75) == 25

    steps = []
    a, b = 48, 18
    while b:
        steps.append((a, b))
        a, b = b, a % b
    assert steps == [(48, 18), (18, 12), (12, 6)]

    print(f"  gcd(48, 18) = {gcd(48, 18)}   trace: {steps} -> 6")
    print(f"  gcd(17, 5)  = {gcd(17, 5)}    (coprime)")
    print("       two clauses in Prolog: gcd(A,0,A) is the base case, and")
    print("       gcd(A,B,G) :- B > 0, R is A mod B, gcd(B,R,G)")


# --- experiment 7: cut and fail ---------------------------------------------

def cut_and_fail_are_documented_only():
    """No cut in pytholog, so this is stated as semantics, not tested."""
    behaviours = [
        ("!", "commits to the current clause AND to the bindings made "
              "before it; discards remaining choice points"),
        ("fail", "always fails, forcing backtracking"),
        ("!, fail", "the CUT-FAIL idiom: commit, then fail, so the whole "
                    "goal fails with no alternatives tried"),
        ("\\\\+ G", "negation as failure -- succeeds if G cannot be proved"),
    ]
    assert len(behaviours) == 4

    print("  the cut and fail, as semantics (pytholog has no cut):")
    for op, meaning in behaviours:
        print(f"    {op:10} {meaning}")
    print()
    print("  the classic cut-fail example -- 'penguins do not fly':")
    print("      fly(X) :- penguin(X), !, fail.")
    print("      fly(X) :- bird(X).")
    print("    for a penguin the first clause commits and fails, so the second")
    print("    is NEVER tried. Remove the cut and every penguin flies.")
    print()
    print("  GREEN CUT   -- removes only redundant choice points; deleting it")
    print("                 changes nothing but speed")
    print("  RED CUT     -- changes the MEANING; deleting it changes answers")
    print("       the cut is the point where Prolog stops being pure logic:")
    print("       clause order and cut placement become semantically load")
    print("       bearing, which is why it is the hardest thing to debug")


def negation_as_failure_is_not_logical_negation():
    """The examinable subtlety, demonstrated with a closed world."""
    known_birds = {"tweety", "polly"}
    known_penguins = {"pingu"}

    # \+ penguin(tweety) succeeds because tweety is not KNOWN to be a penguin
    assert "tweety" not in known_penguins
    # ... but the database simply may not know. That is the CLOSED WORLD
    # ASSUMPTION: anything not derivable is taken to be false.
    unknown_bird = "kiwi"
    assert unknown_bird not in known_birds and unknown_bird not in known_penguins

    print(f"  known birds: {sorted(known_birds)}, known penguins: "
          f"{sorted(known_penguins)}")
    print(f"  \\\\+ penguin(tweety)  succeeds -- tweety is not known to be one")
    print(f"  \\\\+ bird({unknown_bird})       succeeds -- but we simply do not know")
    print("       Prolog's \\\\+ is NEGATION AS FAILURE, not logical negation.")
    print("       It assumes a CLOSED WORLD: anything not derivable is false.")
    print("       Logical negation would require proving the fact untrue")


def main():
    print("Experiments 2-7 -- Lists, arithmetic, and the cut")
    print("  engine limits, asserted:")
    pytholog_has_no_lists()
    pytholog_has_no_arithmetic()
    print("  experiment 2 -- list predicates:")
    list_predicates()
    print("  experiment 3 -- maximum of a list:")
    maximum_of_a_list()
    print("  experiment 4 -- flatten:")
    flatten_a_nested_list()
    print("  experiments 5 and 6 -- factorial, Fibonacci, GCD:")
    factorial_and_fibonacci()
    gcd_by_recursion()
    print("  experiment 7 -- cut and fail:")
    cut_and_fail_are_documented_only()
    negation_as_failure_is_not_logical_negation()


if __name__ == "__main__":
    main()
