"""Experiments 18 and 19 — DCG parsing, Naive Bayes, and local search.

Experiment 18 (a DCG grammar) cannot run in pytholog, which has no DCG
notation -- the .pl file carries it and a recursive-descent parser here does
the same job so the expected parse trees are checked.

Experiment 19 is a deterministic Naive Bayes calculation, and this file also
covers unit-3.md's local search: hill climbing's failure modes and simulated
annealing's escape from them, both measured.
"""
import math
import random


# --- experiment 18: a grammar, parsed ---------------------------------------

GRAMMAR = {
    "S":  [["NP", "VP"]],
    "NP": [["Det", "N"], ["Det", "Adj", "N"]],
    "VP": [["V", "NP"], ["V"]],
    "Det": [["the"], ["a"]],
    "N":  [["cat"], ["dog"], ["mouse"]],
    "Adj": [["big"], ["small"]],
    "V":  [["chases"], ["sees"], ["sleeps"]],
}


def parse(symbol, tokens, i=0):
    """Recursive descent -- exactly what a DCG compiles to in Prolog."""
    if symbol not in GRAMMAR:
        return (symbol, i + 1) if i < len(tokens) and tokens[i] == symbol else None
    for production in GRAMMAR[symbol]:
        children, j = [], i
        for part in production:
            result = parse(part, tokens, j)
            if result is None:
                break
            child, j = result
            children.append(child)
        else:
            return ((symbol, children), j)
    return None


def dcg_parsing():
    good = "the big cat chases a mouse".split()
    result = parse("S", good)
    assert result is not None, good
    tree, consumed = result
    assert consumed == len(good), (consumed, len(good))

    intransitive = "the dog sleeps".split()
    r2 = parse("S", intransitive)
    assert r2 is not None and r2[1] == len(intransitive)

    bad = "cat the chases".split()
    r3 = parse("S", bad)
    assert r3 is None or r3[1] != len(bad), "word order matters"

    def render(node, depth=0):
        label, children = node
        if isinstance(children, str) or not isinstance(children, list):
            return "  " * depth + str(label)
        lines = ["  " * depth + label]
        for c in children:
            lines.append(render(c, depth + 1) if isinstance(c, tuple)
                         else "  " * (depth + 1) + str(c))
        return "\n".join(lines)

    print(f"  '{' '.join(good)}' parses:")
    print("\n".join("    " + l for l in render(tree).splitlines()))
    print(f"  '{' '.join(intransitive)}' parses (VP -> V, intransitive)")
    print(f"  '{' '.join(bad)}' does NOT parse")
    print("       a DCG in Prolog compiles to exactly this recursive descent,")
    print("       with the token list threaded through as difference lists.")
    print("       Grammar written as inference rules -- Unit 4's machinery,")
    print("       applied to language")


# --- experiment 19: deterministic Naive Bayes -------------------------------

WEATHER = [
    # outlook, temperature, humidity, wind, play
    ("sunny",    "hot",  "high",   "weak",   "no"),
    ("sunny",    "hot",  "high",   "strong", "no"),
    ("overcast", "hot",  "high",   "weak",   "yes"),
    ("rain",     "mild", "high",   "weak",   "yes"),
    ("rain",     "cool", "normal", "weak",   "yes"),
    ("rain",     "cool", "normal", "strong", "no"),
    ("overcast", "cool", "normal", "strong", "yes"),
    ("sunny",    "mild", "high",   "weak",   "no"),
    ("sunny",    "cool", "normal", "weak",   "yes"),
    ("rain",     "mild", "normal", "weak",   "yes"),
    ("sunny",    "mild", "normal", "strong", "yes"),
    ("overcast", "mild", "high",   "strong", "yes"),
    ("overcast", "hot",  "normal", "weak",   "yes"),
    ("rain",     "mild", "high",   "strong", "no"),
]
FEATURES = ["outlook", "temperature", "humidity", "wind"]


def naive_bayes():
    """Course 8's and Course 12A's worked example, computed a third time."""
    yes = [r for r in WEATHER if r[4] == "yes"]
    no = [r for r in WEATHER if r[4] == "no"]
    assert (len(yes), len(no), len(WEATHER)) == (9, 5, 14)

    prior = {"yes": len(yes) / 14, "no": len(no) / 14}

    def likelihood(rows, index, value):
        return sum(1 for r in rows if r[index] == value) / len(rows)

    query = ("sunny", "cool", "high", "strong")
    posterior = {}
    for label, rows in (("yes", yes), ("no", no)):
        p = prior[label]
        for i, value in enumerate(query):
            p *= likelihood(rows, i, value)
        posterior[label] = p

    assert round(posterior["yes"], 6) == 0.005291, round(posterior["yes"], 6)
    assert round(posterior["no"], 6) == 0.020571, round(posterior["no"], 6)
    assert posterior["no"] > posterior["yes"]

    total = sum(posterior.values())
    normalised = {k: v / total for k, v in posterior.items()}
    assert round(normalised["no"], 4) == 0.7954

    print(f"  14 days: {len(yes)} play, {len(no)} do not")
    print(f"  query: {query}")
    print(f"    P(yes) x likelihoods = {posterior['yes']:.6f}")
    print(f"    P(no)  x likelihoods = {posterior['no']:.6f}   <- larger")
    print(f"    normalised: no {normalised['no'] * 100:.2f}%, "
          f"yes {normalised['yes'] * 100:.2f}%")
    print("       identical to Course 8 and Course 12 A. Three courses, three")
    print("       implementations, the same numbers -- which is the point of")
    print("       reusing the dataset")


def the_zero_frequency_problem():
    """One unseen value zeroes the whole product."""
    yes = [r for r in WEATHER if r[4] == "yes"]

    # 'overcast' never appears with play=no, so P(overcast | no) = 0.
    no = [r for r in WEATHER if r[4] == "no"]
    overcast_no = sum(1 for r in no if r[0] == "overcast")
    assert overcast_no == 0, "overcast NEVER coincides with no"

    p_no = (len(no) / 14) * 0.0
    assert p_no == 0.0

    # Laplace: (0 + 1) / (5 + 3 outlook values) = 1/8
    smoothed = (len(no) / 14) * (1 / (len(no) + 3))
    assert round(smoothed, 6) == 0.044643, round(smoothed, 6)

    print(f"  'overcast' appears {overcast_no} times with play=no")
    print(f"    P(no | overcast, ...) without smoothing = {p_no}")
    print(f"    with Laplace (+1, 3 outlook values)     = {smoothed:.6f}")
    print("       a single zero vetoes the class whatever the other three")
    print("       features say, because the likelihood is a PRODUCT")


# --- unit-3's local search, measured ----------------------------------------

def hill_climbing_gets_stuck():
    """A landscape with a local maximum, and the measured failure rate."""
    def value(x):
        # Two peaks: a low one near 2 and the global one near 8.
        return -abs(x - 2) * 0.7 + 3 if x < 5 else -abs(x - 8) * 0.5 + 5

    def climb(start, step=0.1):
        x = start
        while True:
            candidates = [x - step, x + step]
            best = max(candidates, key=value)
            if value(best) <= value(x):
                return x
            x = best

    starts = [i * 0.5 for i in range(21)]           # 0.0 to 10.0
    peaks = [round(climb(s), 1) for s in starts]
    global_max = sum(1 for p in peaks if abs(p - 8.0) < 0.35)
    local_max = len(peaks) - global_max

    assert len(starts) == 21
    assert local_max > 0, "some starts get stuck on the local peak"
    assert global_max > 0

    print(f"  a landscape with a local peak near x=2 and the global near x=8:")
    print(f"    {len(starts)} starting points")
    print(f"    reached the GLOBAL maximum: {global_max}")
    print(f"    stuck on the LOCAL maximum: {local_max}  "
          f"({local_max / len(starts) * 100:.0f}%)")
    print("       hill climbing is complete only with RANDOM RESTARTS. If each")
    print(f"       try succeeds with probability p, expected restarts = 1/p")
    print(f"       -- here about {len(starts) / global_max:.1f}")


def simulated_annealing_escapes():
    """The acceptance probability, and the schedule that makes it work."""
    def acceptance(delta, T):
        return 1.0 if delta > 0 else math.exp(delta / T)

    # High T accepts almost anything; low T accepts almost nothing.
    assert round(acceptance(-1.0, 100.0), 4) == 0.9900
    assert round(acceptance(-1.0, 1.0), 4) == 0.3679
    assert round(acceptance(-1.0, 0.1), 6) == 0.000045
    assert acceptance(+1.0, 0.1) == 1.0, "an improvement is ALWAYS accepted"

    print("    P(accept a move that is 1.0 worse) = e^(-1/T):")
    for T in (100.0, 10.0, 1.0, 0.1):
        print(f"      T = {T:6.1f}  ->  {acceptance(-1.0, T):.6f}")
    print("       T high: it accepts almost anything and EXPLORES.")
    print("       T -> 0: it accepts nothing worse and becomes HILL CLIMBING.")
    print("       Annealing is a scheduled slide from random walk to hill")
    print("       climbing, which is exactly why it escapes local maxima")


def genetic_algorithm_fitness():
    """8-queens fitness: non-attacking pairs, maximum 28."""
    def fitness(individual):
        n = len(individual)
        attacking = sum(
            1 for i in range(n) for j in range(i + 1, n)
            if individual[i] == individual[j]
            or abs(individual[i] - individual[j]) == j - i)
        return math.comb(n, 2) - attacking

    assert math.comb(8, 2) == 28, "28 pairs on an 8x8 board"
    solution = (0, 4, 7, 5, 2, 6, 1, 3)          # from experiment 14
    assert fitness(solution) == 28, "a solution has ZERO attacking pairs"

    bad = (0, 0, 0, 0, 0, 0, 0, 0)               # all on one row
    assert fitness(bad) == 0, "every pair attacks"

    middling = (2, 4, 7, 4, 8, 5, 5, 2)
    assert 0 < fitness(middling) < 28

    # Crossover preserves contiguous blocks -- the reason it can help.
    parent_a, parent_b = (2, 4, 7, 4, 8, 5, 5, 2), (3, 2, 7, 5, 2, 4, 1, 1)
    cut = 3
    child = parent_a[:cut] + parent_b[cut:]
    assert child == (2, 4, 7, 5, 2, 4, 1, 1)
    assert child[:cut] == parent_a[:cut] and child[cut:] == parent_b[cut:]

    print(f"  fitness = non-attacking pairs, maximum C(8,2) = {math.comb(8, 2)}")
    print(f"    a valid solution {solution} -> {fitness(solution)}")
    print(f"    all on one row   -> {fitness(bad)}")
    print(f"    a middling one   -> {fitness(middling)}")
    print(f"  crossover at position {cut}: {parent_a} + {parent_b}")
    print(f"                            -> {child}")
    print("       crossover preserves CONTIGUOUS BLOCKS. It helps only if")
    print("       neighbouring genes form a partial solution; with a badly")
    print("       ordered representation it is just noise, and the GA")
    print("       degenerates into an expensive random search")


def main():
    print("Experiments 18-19 -- DCG parsing, Naive Bayes, and local search")
    print("  experiment 18 -- a grammar (DCG in the .pl; recursive descent here):")
    dcg_parsing()
    print("  experiment 19 -- deterministic Naive Bayes:")
    naive_bayes()
    the_zero_frequency_problem()
    print("  unit-3 local search -- hill climbing:")
    hill_climbing_gets_stuck()
    print("  unit-3 local search -- simulated annealing:")
    simulated_annealing_escapes()
    print("  unit-3 -- genetic algorithm fitness and crossover:")
    genetic_algorithm_fitness()


if __name__ == "__main__":
    main()
