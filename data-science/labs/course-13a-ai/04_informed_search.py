"""Experiment 12 — Greedy Best-First search and A*.

unit-3.md section 3.3's headline: A* finds the OPTIMAL 418 km route expanding
6 nodes where uniform cost search needs 13. And section 3.4's demonstration:
an INADMISSIBLE heuristic is faster and wrong.

Both are computed here on Russell & Norvig's Romania map.
"""
import heapq

from fixtures import (GOAL, ROMANIA, START, STRAIGHT_LINE, inflated,
                      path_cost)


def best_first(graph, start, goal, f):
    """One algorithm. f decides everything.

        f = g            -> uniform cost
        f = h            -> greedy best-first
        f = g + h        -> A*
    """
    frontier = [(f(start, 0), 0, [start])]
    best = {}
    expanded = 0
    while frontier:
        _, g, path = heapq.heappop(frontier)
        node = path[-1]
        if node in best and best[node] <= g:
            continue
        best[node] = g
        expanded += 1
        if node == goal:
            return path, expanded, g
        for nxt, step in graph[node].items():
            heapq.heappush(frontier, (f(nxt, g + step), g + step, path + [nxt]))
    return None, expanded, None


def ucs(graph, start, goal):
    return best_first(graph, start, goal, lambda n, g: g)


def greedy(graph, start, goal, h):
    return best_first(graph, start, goal, lambda n, g: h[n])


def astar(graph, start, goal, h):
    return best_first(graph, start, goal, lambda n, g: g + h[n])


def the_headline_comparison():
    """unit-3.md 3.3's table."""
    u_path, u_exp, u_cost = ucs(ROMANIA, START, GOAL)
    g_path, g_exp, _ = greedy(ROMANIA, START, GOAL, STRAIGHT_LINE)
    a_path, a_exp, a_cost = astar(ROMANIA, START, GOAL, STRAIGHT_LINE)
    g_cost = path_cost(g_path)

    assert (u_exp, u_cost) == (13, 418), (u_exp, u_cost)
    assert (g_exp, g_cost) == (4, 450), (g_exp, g_cost)
    assert (a_exp, a_cost) == (6, 418), (a_exp, a_cost)

    assert a_cost == u_cost, "A* found the SAME optimal cost as UCS"
    assert a_exp < u_exp / 2, "expanding less than half as many nodes"
    assert g_cost > a_cost, "greedy is faster still, and WRONG"

    print(f"  {'search':22} {'f(n)':12} {'expanded':>9} {'cost':>6}  optimal?")
    rows = [("Uniform cost", "g(n)", u_exp, u_cost, True),
            ("Greedy best-first", "h(n)", g_exp, g_cost, False),
            ("A*", "g(n) + h(n)", a_exp, a_cost, True)]
    for name, fn, exp, cost, opt in rows:
        print(f"  {name:22} {fn:12} {exp:>9} {cost:>6}  {'YES' if opt else 'NO'}")
    print(f"  greedy:  {' -> '.join(g_path)}")
    print(f"  A*:      {' -> '.join(a_path)}")
    print("       A* FOUND THE OPTIMAL 418 EXPANDING 6 NODES WHERE UCS NEEDED 13.")
    print("       Same answer, less than half the work -- that is why heuristics")
    print("       exist, and it is the number to quote")
    return u_exp, u_cost


def why_greedy_goes_wrong():
    """It ignores g(n) -- the cost already paid."""
    # At Sibiu the choice is Fagaras (h=176) or Rimnicu Vilcea (h=193).
    h_fagaras = STRAIGHT_LINE["Fagaras"]
    h_rimnicu = STRAIGHT_LINE["Rimnicu Vilcea"]
    assert h_fagaras < h_rimnicu, "Fagaras LOOKS closer"

    via_fagaras = ["Arad", "Sibiu", "Fagaras", "Bucharest"]
    via_rimnicu = ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]
    assert path_cost(via_fagaras) == 450
    assert path_cost(via_rimnicu) == 418
    assert path_cost(via_rimnicu) < path_cost(via_fagaras)

    print(f"  at Sibiu, greedy compares h only:")
    print(f"    h(Fagaras)        = {h_fagaras}   <- looks closer, so it goes here")
    print(f"    h(Rimnicu Vilcea) = {h_rimnicu}")
    print(f"  but the actual routes are:")
    print(f"    via Fagaras       = {path_cost(via_fagaras)} km")
    print(f"    via Rimnicu       = {path_cost(via_rimnicu)} km   <- 32 km shorter")
    print("       Fagaras IS closer as the crow flies and further by road.")
    print("       Greedy is short-sighted because it ignores g(n), the cost")
    print("       already paid -- which is exactly what A* adds back")


def astar_with_zero_heuristic_is_ucs(ucs_expanded, ucs_cost):
    """f = g + 0 = g. The same algorithm under a different name."""
    zero = {city: 0 for city in STRAIGHT_LINE}
    path, expanded, cost = astar(ROMANIA, START, GOAL, zero)

    assert (expanded, cost) == (ucs_expanded, ucs_cost) == (13, 418)

    print(f"  A* with h(n) = 0: expanded {expanded}, cost {cost}")
    print(f"  uniform cost    : expanded {ucs_expanded}, cost {ucs_cost}")
    print("       IDENTICAL. A* with a zero heuristic IS uniform cost search.")
    print("       A* sits between UCS (no information, optimal) and greedy")
    print("       (maximum information used badly, not optimal)")


def admissibility_is_what_guarantees_optimality():
    """unit-3.md 3.4: inflate the heuristic and A* becomes faster and WRONG."""
    rows = []
    for label, h in (("straight-line (admissible)", STRAIGHT_LINE),
                     ("straight-line x 2", inflated(2.0)),
                     ("straight-line x 5", inflated(5.0))):
        path, expanded, cost = astar(ROMANIA, START, GOAL, h)
        rows.append((label, expanded, cost, cost == 418, path))

    admissible = rows[0]
    doubled = rows[1]
    assert admissible[1:4] == (6, 418, True)
    assert doubled[1:4] == (4, 450, False), doubled
    assert doubled[1] < admissible[1], "the bad heuristic is FASTER"
    assert doubled[2] > admissible[2], "and WRONG"

    print(f"  {'heuristic':28} {'expanded':>9} {'cost':>6}  optimal?")
    for label, expanded, cost, opt, _ in rows:
        print(f"  {label:28} {expanded:>9} {cost:>6}  {'YES' if opt else 'NO'}")
    print(f"  the inflated heuristic returns: {' -> '.join(doubled[4])}")
    print("       THE INADMISSIBLE HEURISTIC IS FASTER AND WRONG -- 4 nodes")
    print("       instead of 6, and 450 instead of 418. Overestimating makes")
    print("       the node on the optimal path LOOK worse than an alternative,")
    print("       so A* commits to a goal before the better path is explored.")
    print("       The guarantee is gone the moment h(n) > h*(n) anywhere")


def check_the_heuristic_really_is_admissible():
    """h(n) <= h*(n) for every city -- verified against true shortest paths."""
    # True cost from every city to Bucharest, by running UCS backwards.
    true_cost = {}
    frontier = [(0, GOAL)]
    while frontier:
        cost, node = heapq.heappop(frontier)
        if node in true_cost:
            continue
        true_cost[node] = cost
        for nxt, step in ROMANIA[node].items():
            if nxt not in true_cost:
                heapq.heappush(frontier, (cost + step, nxt))

    violations = [(c, STRAIGHT_LINE[c], true_cost[c])
                  for c in true_cost if STRAIGHT_LINE[c] > true_cost[c]]
    assert violations == [], violations
    assert STRAIGHT_LINE[GOAL] == 0, "h(goal) must be 0"
    assert true_cost[START] == 418

    tightest = min(true_cost[c] - STRAIGHT_LINE[c]
                   for c in true_cost if c != GOAL)

    # And the inflated one DOES violate it -- which is the whole point.
    bad = inflated(2.0)
    bad_violations = [c for c in true_cost if bad[c] > true_cost[c]]
    assert len(bad_violations) > 10, len(bad_violations)

    print(f"  checked all {len(true_cost)} cities against their TRUE cost to "
          f"{GOAL}:")
    print(f"    straight-line violations: {len(violations)}  -- admissible")
    print(f"    h(Bucharest) = {STRAIGHT_LINE[GOAL]}")
    print(f"    tightest margin h*(n) - h(n) = {tightest} km")
    print(f"    the x2 heuristic violates admissibility at "
          f"{len(bad_violations)} of {len(true_cost)} cities")
    print("       a straight line can never be longer than a road, which is")
    print("       why this heuristic is admissible BY CONSTRUCTION rather than")
    print("       by luck -- and that is the argument to give in the exam")


def eight_puzzle_heuristics_and_dominance():
    """h2 dominates h1, so A* with h2 expands no more nodes."""
    goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    state = (1, 2, 3, 4, 0, 6, 7, 5, 8)

    def misplaced(s):
        return sum(1 for i, v in enumerate(s) if v != 0 and v != goal[i])

    def manhattan(s):
        total = 0
        for i, v in enumerate(s):
            if v == 0:
                continue
            j = goal.index(v)
            total += abs(i // 3 - j // 3) + abs(i % 3 - j % 3)
        return total

    assert misplaced(goal) == 0 and manhattan(goal) == 0
    assert misplaced(state) == 2, misplaced(state)
    assert manhattan(state) == 2, manhattan(state)

    scrambled = (7, 2, 4, 5, 0, 6, 8, 3, 1)
    h1, h2 = misplaced(scrambled), manhattan(scrambled)
    # By hand: six tiles are out of place (7, 4, 5, 8, 3, 1), and their
    # Manhattan distances are 2 + 3 + 1 + 1 + 3 + 4 = 14.
    assert h1 == 6 and h2 == 14, (h1, h2)
    assert h2 >= h1, "h2 DOMINATES h1 -- it is always at least as large"

    print(f"  goal state:      h1 (misplaced) = 0, h2 (Manhattan) = 0")
    print(f"  one tile out:    h1 = {misplaced(state)}, h2 = {manhattan(state)}")
    print(f"  well scrambled:  h1 = {h1}, h2 = {h2}")
    print("       both come from RELAXED problems -- h1 lets a tile move")
    print("       anywhere, h2 lets it move to any adjacent square -- so both")
    print("       are admissible by construction.")
    print("       h2 >= h1 everywhere, so h2 DOMINATES h1 and A* with h2")
    print("       expands no more nodes. Dominance is the right way to compare")
    print("       heuristics, and a stronger claim than 'it was faster'")


def main():
    print("Experiment 12 -- Greedy Best-First search and A*")
    ucs_exp, ucs_cost = the_headline_comparison()
    why_greedy_goes_wrong()
    astar_with_zero_heuristic_is_ucs(ucs_exp, ucs_cost)
    admissibility_is_what_guarantees_optimality()
    check_the_heuristic_really_is_admissible()
    eight_puzzle_heuristics_and_dominance()


if __name__ == "__main__":
    main()
