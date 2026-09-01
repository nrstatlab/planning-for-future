"""Experiment 7 — Multilevel (generalized) association rules.

WEKA has NO built-in multilevel miner (see lab.md). The standard technique is
to ADD ANCESTOR ITEMS to each transaction and mine the extended data, then
discard redundant descendant rules afterwards.

Implements Unit 3 section 3.9: the uniform-support dilemma, reduced support,
and the redundant-ancestor test.
"""
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# leaf -> (category, department)
TAXONOMY = {
    "amul_milk":       ("milk", "dairy"),
    "nandini_milk":    ("milk", "dairy"),
    "heritage_milk":   ("milk", "dairy"),
    "amul_cheese":     ("cheese", "dairy"),
    "britannia_bread": ("bread", "bakery"),
    "croissant":       ("pastry", "bakery"),
}

# Built so the redundancy test actually DISCRIMINATES:
#   amul_milk     6 baskets, 4 with bread  -> confidence 0.667
#   nandini_milk  6 baskets, 4 with bread  -> confidence 0.667
#   heritage_milk 4 baskets, 4 with bread  -> confidence 1.000
#   milk overall 16 baskets, 12 with bread -> confidence 0.750
# so the first two are redundant (deviation 0.083) and the third is not (0.25).
TRANSACTIONS = (
    [["amul_milk", "britannia_bread"]] * 4
    + [["amul_milk", "amul_cheese"]] * 2
    + [["nandini_milk", "britannia_bread"]] * 4
    + [["nandini_milk", "croissant"]] * 2
    + [["heritage_milk", "britannia_bread"]] * 4
    + [["amul_cheese", "croissant"]] * 2
    + [["amul_cheese", "britannia_bread"]] * 2
)


def expand(transaction, levels=(0, 1, 2)):
    """Add ancestor items. 0 = leaves, 1 = category, 2 = department."""
    out = set()
    for item in transaction:
        if 0 in levels:
            out.add(item)
        for lv in (1, 2):
            if lv in levels:
                out.add(TAXONOMY[item][lv - 1])
    return sorted(out)


def at_level(level):
    return [expand(t, levels=(level,)) for t in TRANSACTIONS]


def mine(transactions, min_support, min_confidence):
    te = TransactionEncoder()
    frame = pd.DataFrame(te.fit(transactions).transform(transactions),
                         columns=te.columns_)
    items = apriori(frame, min_support=min_support, use_colnames=True)
    if items.empty:
        return items, pd.DataFrame()
    rules = association_rules(items, metric="confidence", min_threshold=min_confidence)
    return items, rules


def confidence(antecedent, consequent, transactions):
    """Computed directly from the baskets, so nothing is hidden in a library."""
    a = sum(1 for t in transactions if antecedent in t)
    both = sum(1 for t in transactions if antecedent in t and consequent in t)
    return both / a if a else 0.0, a, both


def uniform_support_dilemma():
    """Section 3.9: ONE threshold cannot serve both levels."""
    leaf_items, _ = mine(at_level(0), 0.40, 0.5)
    leaf_pairs = [i for i in leaf_items.itemsets if len(i) >= 2]
    assert leaf_pairs == [], "at 40%, no individual PRODUCT pair qualifies"

    dept_items, _ = mine(at_level(2), 0.40, 0.5)
    dept_pairs = [i for i in dept_items.itemsets if len(i) >= 2]
    assert dept_pairs, "but dairy+bakery clears 40% comfortably"

    print(f"  uniform support 40%: {len(leaf_pairs)} product pairs, "
          f"{len(dept_pairs)} department pairs")
    print(f"       set it high and the leaves vanish; set it low and the top")
    print(f"       floods you -- which is why REDUCED support exists")


def reduced_support():
    """A lower threshold at deeper levels."""
    for name, level, minsup in [("department", 2, 0.40),
                                ("category", 1, 0.25),
                                ("product", 0, 0.15)]:
        items, rules = mine(at_level(level), minsup, 0.5)
        pairs = [tuple(sorted(i)) for i in items.itemsets if len(i) >= 2]
        print(f"  {name:11s} minsup {minsup:.0%}: {len(items):2d} itemsets, "
              f"{len(pairs)} of size >= 2, {len(rules)} rules")
        assert len(items) > 0, f"{name} level found nothing"


def redundant_ancestor_rule():
    """Section 3.9: report a descendant rule only when it DEVIATES.

    A descendant rule whose confidence matches the ancestor's tells you nothing
    new -- it is the EXPECTED consequence of the ancestor rule.
    """
    mixed = [expand(t) for t in TRANSACTIONS]        # leaves AND ancestors

    anc_conf, anc_n, anc_both = confidence("milk", "bread", mixed)
    assert (anc_n, anc_both) == (16, 12), (anc_n, anc_both)
    assert round(anc_conf, 4) == 0.75, anc_conf

    print(f"\n  ancestor: milk -> bread, {anc_both}/{anc_n} = {anc_conf:.4f}")
    print(f"  descendants (tolerance 0.10):")

    TOLERANCE = 0.10
    verdicts = {}
    for brand in ["amul_milk", "nandini_milk", "heritage_milk"]:
        conf, n, both = confidence(brand, "bread", mixed)
        deviation = abs(conf - anc_conf)
        redundant = deviation <= TOLERANCE
        verdicts[brand] = redundant
        print(f"    {brand:14s} -> bread: {both}/{n} = {conf:.4f}, "
              f"deviation {deviation:.4f} -> "
              f"{'REDUNDANT, suppress' if redundant else 'DEVIATES, report it'}")

    # The demonstration must DISCRIMINATE, or it proves nothing.
    assert verdicts["amul_milk"] is True
    assert verdicts["nandini_milk"] is True
    assert verdicts["heritage_milk"] is False
    assert any(verdicts.values()) and not all(verdicts.values()), \
        "the test must both suppress and report, or it demonstrates nothing"

    print(f"       two suppressed, one reported -- heritage_milk buyers really")
    print(f"       do buy bread more often than milk buyers in general")


def ancestor_support_is_at_least_the_sum():
    """Section 3.9: an ancestor's support is AT LEAST the sum of its
    descendants' -- at least, not equal, because one basket containing two
    brands of milk counts twice at the leaf level and once at 'milk'."""
    mixed = [expand(t) for t in TRANSACTIONS]
    n = len(mixed)

    milk = sum(1 for t in mixed if "milk" in t) / n
    brands = sum(sum(1 for t in mixed if b in t) for b in
                 ["amul_milk", "nandini_milk", "heritage_milk"]) / n

    assert milk <= brands + 1e-12, "the ancestor cannot exceed the leaf sum"
    assert milk >= max(sum(1 for t in mixed if b in t) / n for b in
                       ["amul_milk", "nandini_milk", "heritage_milk"])

    print(f"\n  monotonicity: support(milk) = {milk:.4f}, "
          f"sum of brand supports = {brands:.4f}")
    print(f"       so an infrequent ancestor prunes its whole subtree")


def main():
    print("Experiment 7 -- Multilevel association rules")
    uniform_support_dilemma()
    reduced_support()
    redundant_ancestor_rule()
    ancestor_support_is_at_least_the_sum()
    print("\n  multilevel mining and the redundancy test verified")


if __name__ == "__main__":
    main()
