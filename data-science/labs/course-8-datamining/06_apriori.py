"""Experiment 6 — Association rules with Apriori.

WEKA equivalent: Associate tab -> Apriori (see lab.md).

This script reproduces the hand-traced examples from Unit 3 EXACTLY, so the
notes and the code check each other. Every assertion below corresponds to a
number written out in notes/sem-4/course-8-data-mining/unit-3.md.

Run:  python3 tools/run_data_labs.py     (or this file directly)
"""
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


def frequent_itemsets(transactions, min_support):
    """One-hot encode the baskets and run Apriori."""
    te = TransactionEncoder()
    frame = pd.DataFrame(te.fit(transactions).transform(transactions),
                         columns=te.columns_)
    return apriori(frame, min_support=min_support, use_colnames=True)


def as_dict(itemsets, n):
    """{frozenset -> support COUNT}, which is what the notes tabulate."""
    return {frozenset(r.itemsets): round(r.support * n) for r in itemsets.itertuples()}


def unit3_main_trace():
    """Unit 3 section 3.4: five transactions, minsup count 3 (60%)."""
    T = [list("ACD"), list("BCE"), list("ABCE"), list("BE"), list("ABCE")]
    n = len(T)

    items = frequent_itemsets(T, 3 / n)
    found = as_dict(items, n)

    expected = {
        frozenset("A"): 3, frozenset("B"): 4, frozenset("C"): 4, frozenset("E"): 4,
        frozenset("AC"): 3, frozenset("BC"): 3, frozenset("BE"): 4, frozenset("CE"): 3,
        frozenset("BCE"): 3,
    }
    assert found == expected, f"\n got      {found}\n expected {expected}"
    assert len(found) == 9, "the notes claim nine frequent itemsets"
    assert frozenset("D") not in found, "{D} has support 1 and must be pruned"

    # Rule generation from {B,C,E} with minconf 0.8
    rules = association_rules(items, metric="confidence", min_threshold=0.8)
    strong = {
        (frozenset(r.antecedents), frozenset(r.consequents)): (round(r.confidence, 4),
                                                               round(r.lift, 4))
        for r in rules.itertuples()
        if frozenset(r.antecedents) | frozenset(r.consequents) == frozenset("BCE")
    }
    assert strong == {
        (frozenset("BC"), frozenset("E")): (1.0, 1.25),
        (frozenset("CE"), frozenset("B")): (1.0, 1.25),
    }, strong

    print(f"  3.4 trace: {len(found)} frequent itemsets, "
          f"{len(strong)} strong rules from {{B,C,E}} -- matches the notes")
    return found


def unit3_practice_1():
    """Unit 3 Practice Problem 1: nine transactions, minsup count 2, minconf 0.7."""
    T = [list("ABE"), list("BD"), list("BC"), list("ABD"), list("AC"),
         list("BC"), list("AC"), list("ABCE"), list("ABC")]
    n = len(T)

    items = frequent_itemsets(T, 2 / n)
    found = as_dict(items, n)

    expected = {
        frozenset("A"): 6, frozenset("B"): 7, frozenset("C"): 6,
        frozenset("D"): 2, frozenset("E"): 2,
        frozenset("AB"): 4, frozenset("AC"): 4, frozenset("AE"): 2,
        frozenset("BC"): 4, frozenset("BD"): 2, frozenset("BE"): 2,
        frozenset("ABC"): 2, frozenset("ABE"): 2,
    }
    assert found == expected, f"\n got      {found}\n expected {expected}"
    assert len(found) == 13, "the notes claim thirteen frequent itemsets"

    # {A,D}, {C,D}, {C,E}, {D,E} are infrequent, so every superset is pruned.
    for gone in ("AD", "CD", "CE", "DE", "ABD", "ACE", "BCE", "BCD", "BDE", "ABCE"):
        assert frozenset(gone) not in found, f"{{{gone}}} must not be frequent"

    rules = association_rules(items, metric="confidence", min_threshold=0.7)

    def summarise(pred):
        return sorted((sorted(r.antecedents), sorted(r.consequents),
                       round(r.confidence, 4), round(r.lift, 4))
                      for r in rules.itertuples() if pred(r))

    # The question asks for rules from the LARGEST frequent itemsets, which is
    # what the notes tabulate: the two 3-itemsets.
    from_3 = summarise(lambda r: len(frozenset(r.antecedents) | frozenset(r.consequents)) == 3)
    assert from_3 == [
        (["A", "E"], ["B"], 1.0, 1.2857),
        (["B", "E"], ["A"], 1.0, 1.5),
        (["E"], ["A", "B"], 1.0, 2.25),
    ], from_3

    # No strong rule comes from {A,B,C}: every confidence there is at most 0.5.
    from_abc = [r for r in rules.itertuples()
                if frozenset(r.antecedents) | frozenset(r.consequents) == frozenset("ABC")]
    assert from_abc == [], "the notes claim {A,B,C} yields no strong rule"

    # Mining the WHOLE itemset lattice also yields three strong rules from
    # 2-itemsets. The exam question scoped itself to the largest itemsets, but
    # a real Apriori run reports these too -- worth knowing they exist.
    from_2 = summarise(lambda r: len(frozenset(r.antecedents) | frozenset(r.consequents)) == 2)
    assert from_2 == [
        (["D"], ["B"], 1.0, 1.2857),
        (["E"], ["A"], 1.0, 1.5),
        (["E"], ["B"], 1.0, 1.2857),
    ], from_2

    print(f"  Practice 1: {len(found)} frequent itemsets, {len(from_3)} strong "
          f"rules from the 3-itemsets (+{len(from_2)} from 2-itemsets)")


def confidence_is_misleading():
    """Unit 3 section 3.2: the cricket / data science example.

    Support 0.72 and confidence 0.90 look excellent; lift is exactly 1.00,
    meaning the two are INDEPENDENT and the rule is worthless.
    """
    n = 1000
    T = ([list("cd")] * 720 + [list("c")] * 80
         + [list("d")] * 180 + [list("x")] * 20)
    assert len(T) == n

    items = frequent_itemsets(T, 0.1)
    rules = association_rules(items, metric="confidence", min_threshold=0.5)
    r = next(x for x in rules.itertuples()
             if frozenset(x.antecedents) == {"c"} and frozenset(x.consequents) == {"d"})

    assert round(r.support, 4) == 0.72
    assert round(r.confidence, 4) == 0.90
    assert round(r.lift, 4) == 1.0, "lift must be exactly 1 -- independent"

    print(f"  3.2 trap: support {r.support:.2f}, confidence {r.confidence:.2f}, "
          f"lift {r.lift:.2f} -- high confidence, ZERO interest")


def tea_and_coffee():
    """Unit 3 Practice Problem 3: a NEGATIVE association hiding behind
    respectable support and confidence."""
    both, tea_only, coffee_only = 400, 200, 350
    neither = 1000 - both - tea_only - coffee_only
    assert neither == 50

    T = ([["tea", "coffee"]] * both + [["tea"]] * tea_only
         + [["coffee"]] * coffee_only + [["water"]] * neither)

    items = frequent_itemsets(T, 0.05)
    rules = association_rules(items, metric="support", min_threshold=0.05)
    r = next(x for x in rules.itertuples()
             if frozenset(x.antecedents) == {"tea"} and frozenset(x.consequents) == {"coffee"})

    assert round(r.support, 4) == 0.40
    assert round(r.confidence, 4) == 0.6667
    assert round(r.lift, 4) == 0.8889, "lift below 1 -- a NEGATIVE association"
    assert round(r.leverage, 4) == -0.05, "leverage agrees: negative"

    print(f"  Practice 3: confidence {r.confidence:.4f} looks fine, but lift "
          f"{r.lift:.4f} < 1 -- tea drinkers are LESS likely to drink coffee")


def main():
    print("Experiment 6 -- Apriori (mlxtend)")
    unit3_main_trace()
    unit3_practice_1()
    confidence_is_misleading()
    tea_and_coffee()
    print("  all Unit 3 hand calculations reproduced")


if __name__ == "__main__":
    main()
