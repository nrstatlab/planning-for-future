"""Course 4 Lab, experiments 1-2: contingency tables, conditional probability,
independence, and Bayes' theorem.

Experiment 2 is reconstructed -- the official text survives only as the
fragment "a positive result." See SYLLABUS-REVIEW.md findings D1 and D3.

Standard library only: no numpy, no pandas, no scipy.
"""

from fractions import Fraction

# ---------------------------------------------------------------------
# EXPERIMENT 1: contingency table, conditional probabilities, independence
# ---------------------------------------------------------------------
print("=" * 66)
print("EXPERIMENT 1: Contingency table from sales data")
print("=" * 66)

# Rows = region, columns = whether the customer bought the premium product.
table = {
    "North": {"Premium": 30, "Standard": 70},
    "South": {"Premium": 45, "Standard": 55},
    "East":  {"Premium": 25, "Standard": 75},
}
columns = ["Premium", "Standard"]

row_totals = {r: sum(cells.values()) for r, cells in table.items()}
col_totals = {c: sum(table[r][c] for r in table) for c in columns}
grand_total = sum(row_totals.values())

print(f"\n{'Region':<10}" + "".join(f"{c:>12}" for c in columns) + f"{'Total':>10}")
print("-" * 46)
for region, cells in table.items():
    print(f"{region:<10}" + "".join(f"{cells[c]:>12}" for c in columns)
          + f"{row_totals[region]:>10}")
print("-" * 46)
print(f"{'Total':<10}" + "".join(f"{col_totals[c]:>12}" for c in columns)
      + f"{grand_total:>10}")

print("\nJOINT probabilities  P(Region and Purchase) = cell / grand total")
for region, cells in table.items():
    for col in columns:
        print(f"  P({region} and {col:<8}) = {cells[col]:>3}/{grand_total} "
              f"= {cells[col] / grand_total:.4f}")

print("\nMARGINAL probabilities")
for region in table:
    print(f"  P({region:<6}) = {row_totals[region]}/{grand_total} "
          f"= {row_totals[region] / grand_total:.4f}")
for col in columns:
    print(f"  P({col:<8}) = {col_totals[col]}/{grand_total} "
          f"= {col_totals[col] / grand_total:.4f}")

print("\nCONDITIONAL probabilities  P(A|B) = P(A and B) / P(B)")
for region in table:
    joint = table[region]["Premium"] / grand_total
    marginal = row_totals[region] / grand_total
    print(f"  P(Premium | {region:<6}) = {joint:.4f} / {marginal:.4f} "
          f"= {joint / marginal:.4f}")

print("\nINDEPENDENCE CHECK")
print("  A and B are independent if P(A and B) = P(A) x P(B)")
for region in table:
    joint = table[region]["Premium"] / grand_total
    product = (row_totals[region] / grand_total) * (col_totals["Premium"] / grand_total)
    verdict = "independent" if abs(joint - product) < 1e-9 else "NOT independent"
    print(f"  {region:<6}: P(joint) = {joint:.4f}, P(A)xP(B) = {product:.4f}"
          f"  -> {verdict}")
print("\n  Conclusion: region and purchase type are dependent -- knowing the")
print("  region changes the probability of a premium purchase.")

# ---------------------------------------------------------------------
# EXPERIMENT 2 [RECONSTRUCTED]: Bayes' theorem, medical testing
# ---------------------------------------------------------------------
print("\n" + "=" * 66)
print("EXPERIMENT 2 [RECONSTRUCTED]: Bayes' theorem")
print("=" * 66)
print("""
Question (reconstructed from the surviving fragment "a positive result."):

  A disease affects 1% of a population. A test for it is 99% sensitive
  (it correctly flags 99% of people who have the disease) and 95% specific
  (it correctly clears 95% of people who do not).

  A randomly chosen person tests positive. What is the probability that
  they actually have the disease, given a positive result?
""")

p_disease = 0.01                 # prior P(D)
p_no_disease = 1 - p_disease
sensitivity = 0.99               # P(+ | D)
specificity = 0.95               # P(- | not D)
false_positive = 1 - specificity  # P(+ | not D)

# Total probability of a positive result (the denominator).
p_positive = sensitivity * p_disease + false_positive * p_no_disease
posterior = sensitivity * p_disease / p_positive

print("  Given:")
print(f"    P(D)          = {p_disease}          prior probability of disease")
print(f"    P(+ | D)      = {sensitivity}          sensitivity")
print(f"    P(- | not D)  = {specificity}          specificity")
print(f"    P(+ | not D)  = {false_positive:.2f}          false positive rate")

print("\n  Law of total probability -- P(+):")
print(f"    P(+) = P(+|D)P(D) + P(+|not D)P(not D)")
print(f"         = {sensitivity} x {p_disease} + {false_positive:.2f} x {p_no_disease}")
print(f"         = {sensitivity * p_disease:.4f} + {false_positive * p_no_disease:.4f}"
      f" = {p_positive:.4f}")

print("\n  Bayes' theorem -- P(D | +):")
print(f"    P(D|+) = P(+|D)P(D) / P(+)")
print(f"           = {sensitivity * p_disease:.4f} / {p_positive:.4f}")
print(f"           = {posterior:.4f}  ->  about {posterior * 100:.1f}%")

print(f"""
  THE POINT OF THIS QUESTION: the test is 99% sensitive, yet a positive
  result means only a {posterior * 100:.0f}% chance of having the disease. Because the
  disease is rare, the 5% of false positives drawn from the 99% who are
  healthy vastly outnumber the true positives.

  Out of 10,000 people:
    {int(10000 * p_disease)} have the disease, of whom {10000 * p_disease * sensitivity:.0f} test positive
    {int(10000 * p_no_disease)} do not, of whom {10000 * p_no_disease * false_positive:.0f} still test positive
    so {10000 * p_positive:.0f} positives in total, of which only {10000 * p_disease * sensitivity:.0f} are real.

  Confusing P(D|+) with P(+|D) is called the base rate fallacy, and it is
  the single most examined idea in this part of the syllabus.
""")

print("  Exact fraction:", Fraction(posterior).limit_denominator(10000))
