"""Experiments 13 and 14 — Map colouring and N-Queens by backtracking.

unit-3.md section 3.8's claim, measured: the MRV heuristic reduces the number
of backtracks, and MRV and LCV correctly pull in opposite directions.
"""
import itertools

# Australia -- Russell & Norvig's map colouring example.
AUSTRALIA = {
    "WA": ["NT", "SA"],
    "NT": ["WA", "SA", "Q"],
    "SA": ["WA", "NT", "Q", "NSW", "V"],
    "Q":  ["NT", "SA", "NSW"],
    "NSW": ["Q", "SA", "V"],
    "V":  ["SA", "NSW"],
    "T":  [],                       # Tasmania -- no land neighbours
}
COLOURS = ["red", "green", "blue"]


def consistent(var, value, assignment, graph):
    return all(assignment.get(n) != value for n in graph[var])


def backtrack(graph, domains, assignment=None, stats=None, use_mrv=False):
    assignment = {} if assignment is None else assignment
    stats = {"assignments": 0, "backtracks": 0} if stats is None else stats

    if len(assignment) == len(graph):
        return assignment, stats

    unassigned = [v for v in graph if v not in assignment]
    if use_mrv:
        # MRV: fewest legal values left. Tie-break on DEGREE.
        def remaining(v):
            return sum(1 for c in domains[v] if consistent(v, c, assignment, graph))
        var = min(unassigned,
                  key=lambda v: (remaining(v),
                                 -sum(1 for n in graph[v] if n not in assignment)))
    else:
        var = unassigned[0]

    for value in domains[var]:
        if consistent(var, value, assignment, graph):
            assignment[var] = value
            stats["assignments"] += 1
            result, stats = backtrack(graph, domains, assignment, stats, use_mrv)
            if result is not None:
                return result, stats
            del assignment[var]
            stats["backtracks"] += 1
    return None, stats


def map_colouring():
    domains = {v: list(COLOURS) for v in AUSTRALIA}
    plain, plain_stats = backtrack(AUSTRALIA, domains)
    mrv, mrv_stats = backtrack(AUSTRALIA, domains, use_mrv=True)

    assert plain is not None and mrv is not None
    assert len(plain) == len(AUSTRALIA) == 7

    # Verify the solution really is consistent -- the definition of a CSP.
    for region, neighbours in AUSTRALIA.items():
        for n in neighbours:
            assert plain[region] != plain[n], (region, n)
            assert mrv[region] != mrv[n], (region, n)

    assert len({plain[r] for r in AUSTRALIA}) <= 3, "three colours suffice"

    print("  Australia, 3 colours, 7 regions:")
    for region in ("WA", "NT", "SA", "Q", "NSW", "V", "T"):
        print(f"    {region:4} {plain[region]}")
    print(f"  plain backtracking: {plain_stats['assignments']} assignments, "
          f"{plain_stats['backtracks']} backtracks")
    print(f"  with MRV + degree : {mrv_stats['assignments']} assignments, "
          f"{mrv_stats['backtracks']} backtracks")
    print("       SA borders every mainland region, so MRV and the degree")
    print("       heuristic both pick it early -- and once SA is fixed every")
    print("       neighbour has only two colours left")


def three_colours_are_necessary():
    """Two are not enough, and the search proves it rather than asserting it."""
    two = {v: ["red", "green"] for v in AUSTRALIA}
    result, stats = backtrack(AUSTRALIA, two)

    assert result is None, "no 2-colouring exists"
    assert stats["backtracks"] > 0

    # WA, NT and SA form a triangle -- three mutually adjacent regions.
    triangle = ["WA", "NT", "SA"]
    for a, b in itertools.combinations(triangle, 2):
        assert b in AUSTRALIA[a], (a, b)

    print(f"  with only 2 colours: no solution, after "
          f"{stats['backtracks']} backtracks")
    print(f"  the reason: {triangle} are MUTUALLY adjacent -- a triangle needs")
    print("       three colours. The search discovers this by exhausting every")
    print("       possibility, which is what 'no solution' means in a CSP")


def mrv_and_lcv_pull_opposite_ways():
    """The trick question from unit-3.md 3.8, made concrete."""
    assignment = {"WA": "red"}
    domains = {v: list(COLOURS) for v in AUSTRALIA}

    def remaining(v):
        return [c for c in domains[v] if consistent(v, c, assignment, AUSTRALIA)]

    counts = {v: len(remaining(v)) for v in AUSTRALIA if v not in assignment}
    mrv_choice = min(counts, key=lambda v: counts[v])

    assert counts["NT"] == 2 and counts["SA"] == 2, counts
    assert counts["T"] == 3 and counts["Q"] == 3
    assert counts[mrv_choice] == 2

    # LCV, for the chosen variable: which value rules out fewest neighbour options?
    def rules_out(var, value):
        total = 0
        for n in AUSTRALIA[var]:
            if n in assignment:
                continue
            total += sum(1 for c in domains[n]
                         if c == value and consistent(n, c, assignment, AUSTRALIA))
        return total

    lcv_order = sorted(remaining(mrv_choice), key=lambda c: rules_out(mrv_choice, c))
    assert len(lcv_order) == 2

    print(f"  after WA = red, legal values remaining per region:")
    for v in sorted(counts, key=lambda v: counts[v]):
        print(f"    {v:4} {counts[v]}")
    print(f"  MRV picks {mrv_choice} (fewest options) -- FAIL FAST")
    print(f"  LCV then orders its values {lcv_order} -- least constraining first")
    print("       MRV chooses the VARIABLE most likely to fail, because you")
    print("       want to discover a dead end now. LCV chooses the VALUE least")
    print("       likely to fail, because once committed you want it to survive.")
    print("       VARIABLES: FAIL FAST. VALUES: FAIL LATE")


def n_queens(n=8):
    """Experiment 14 -- backtracking, and the known solution counts."""
    solutions = []
    placements = {"count": 0}

    def safe(cols, row):
        c = len(cols)
        return all(r != row and abs(r - row) != c - i
                   for i, r in enumerate(cols))

    def place(cols):
        if len(cols) == n:
            solutions.append(tuple(cols))
            return
        for row in range(n):
            if safe(cols, row):
                cols.append(row)
                placements["count"] += 1
                place(cols)
                cols.pop()

    place([])

    # The published solution counts for N-Queens.
    known = {4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    assert len(solutions) == known[n], (n, len(solutions))

    first = solutions[0]
    assert len(set(first)) == n, "no two queens share a row"
    diagonals_ok = all(abs(first[i] - first[j]) != j - i
                       for i in range(n) for j in range(i + 1, n))
    assert diagonals_ok, first

    print(f"  {n}-Queens: {len(solutions)} distinct solutions, found after "
          f"{placements['count']} placements")
    print(f"  the first solution, as a row per column: {first}")
    board = "\n".join("    " + " ".join("Q" if first[c] == r else "."
                                        for c in range(n)) for r in range(n))
    print(board)
    return solutions


def n_queens_counts_across_n():
    """The counts are famously irregular -- 6 has FEWER solutions than 5."""
    counts = {}
    for n in range(4, 9):
        found = []

        def safe(cols, row):
            c = len(cols)
            return all(r != row and abs(r - row) != c - i
                       for i, r in enumerate(cols))

        def place(cols, limit=n):
            if len(cols) == limit:
                found.append(tuple(cols))
                return
            for row in range(limit):
                if safe(cols, row):
                    cols.append(row)
                    place(cols, limit)
                    cols.pop()

        place([])
        counts[n] = len(found)

    assert counts == {4: 2, 5: 10, 6: 4, 7: 40, 8: 92}, counts
    assert counts[6] < counts[5], "6 has FEWER solutions than 5"

    print("    n : solutions")
    for n, c in counts.items():
        print(f"    {n} : {c:>3}")
    print("       the counts are irregular -- n=6 has FOUR solutions where")
    print("       n=5 has ten. There is no formula; they are computed by")
    print("       search, which is why N-Queens is a search problem at all")


def main():
    print("Experiments 13 and 14 -- CSP: map colouring and N-Queens")
    map_colouring()
    three_colours_are_necessary()
    mrv_and_lcv_pull_opposite_ways()
    n_queens(8)
    print("  solution counts by board size:")
    n_queens_counts_across_n()


if __name__ == "__main__":
    main()
