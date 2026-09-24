"""Experiments 9, 10, 11 — DFS, BFS and uniform cost search.

Run on Russell & Norvig's Romania map, so every figure can be checked against
the textbook as well as against this code. unit-2.md section 2.7 quotes these
numbers.

The three algorithms are the SAME LOOP with a different frontier -- a queue, a
stack, a priority queue -- and the code is written to make that obvious.
"""
import heapq
from collections import deque

from fixtures import GOAL, GRAPH_EDGES, ROMANIA, START, path_cost


# --- the three strategies: one loop, three frontiers ------------------------

def bfs(graph, start, goal):
    """FIFO queue -> expand the SHALLOWEST node."""
    frontier = deque([[start]])
    reached = {start}
    expanded = 0
    while frontier:
        path = frontier.popleft()
        expanded += 1
        if path[-1] == goal:
            return path, expanded
        for nxt in graph[path[-1]]:
            if nxt not in reached:
                reached.add(nxt)
                frontier.append(path + [nxt])
    return None, expanded


def dfs(graph, start, goal):
    """LIFO stack -> expand the DEEPEST node."""
    frontier = [[start]]
    explored = set()
    expanded = 0
    while frontier:
        path = frontier.pop()
        if path[-1] in explored:
            continue
        explored.add(path[-1])
        expanded += 1
        if path[-1] == goal:
            return path, expanded
        for nxt in reversed(list(graph[path[-1]])):
            if nxt not in explored:
                frontier.append(path + [nxt])
    return None, expanded


def ucs(graph, start, goal):
    """Priority queue on g(n) -> expand the CHEAPEST path so far."""
    frontier = [(0, [start])]
    best = {}
    expanded = 0
    while frontier:
        cost, path = heapq.heappop(frontier)
        node = path[-1]
        if node in best and best[node] <= cost:
            continue
        best[node] = cost
        expanded += 1
        # The goal test happens on EXPANSION, not generation -- a cheaper
        # path to the goal may still be waiting in the frontier.
        if node == goal:
            return path, expanded, cost
        for nxt, step in graph[node].items():
            heapq.heappush(frontier, (cost + step, path + [nxt]))
    return None, expanded, None


# --- the experiments ---------------------------------------------------------

def the_three_compared():
    """unit-2.md 2.7's table, reproduced exactly."""
    bfs_path, bfs_exp = bfs(ROMANIA, START, GOAL)
    dfs_path, dfs_exp = dfs(ROMANIA, START, GOAL)
    ucs_path, ucs_exp, ucs_cost = ucs(ROMANIA, START, GOAL)

    assert (bfs_exp, path_cost(bfs_path)) == (9, 450), (bfs_exp, path_cost(bfs_path))
    assert (dfs_exp, path_cost(dfs_path)) == (6, 607), (dfs_exp, path_cost(dfs_path))
    assert (ucs_exp, ucs_cost) == (13, 418), (ucs_exp, ucs_cost)

    assert bfs_path == ["Arad", "Sibiu", "Fagaras", "Bucharest"]
    assert ucs_path == ["Arad", "Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest"]

    # BFS found the path with the fewest EDGES -- but not the cheapest.
    assert len(bfs_path) - 1 == 3
    assert len(ucs_path) - 1 == 4
    assert path_cost(bfs_path) > ucs_cost, "fewer edges, MORE kilometres"

    print(f"  {'strategy':14} {'expanded':>9} {'edges':>6} {'cost':>6}  path")
    for name, p, e, c in (("BFS", bfs_path, bfs_exp, path_cost(bfs_path)),
                          ("DFS", dfs_path, dfs_exp, path_cost(dfs_path)),
                          ("Uniform cost", ucs_path, ucs_exp, ucs_cost)):
        print(f"  {name:14} {e:>9} {len(p) - 1:>6} {c:>6}  {' -> '.join(p)}")
    print("       BFS found the fewest EDGES (3) and 450 km, not the cheapest.")
    print("       Step costs are unequal here, so its optimality guarantee")
    print("       does not apply.")
    print("       DFS expanded fewest and found the WORST path, 607 km.")
    print("       UCS found the optimal 418 and expanded the MOST, 13.")
    print("       The optimal route runs through Rimnicu Vilcea and Pitesti,")
    print("       and NEITHER BFS NOR DFS finds it")
    return ucs_cost


def ucs_is_dijkstra(optimal):
    """UCS computes the shortest distance to EVERY city, like Dijkstra."""
    distances = {}
    frontier = [(0, START)]
    while frontier:
        cost, node = heapq.heappop(frontier)
        if node in distances:
            continue
        distances[node] = cost
        for nxt, step in ROMANIA[node].items():
            if nxt not in distances:
                heapq.heappush(frontier, (cost + step, nxt))

    assert len(distances) == len(ROMANIA) == 20
    assert distances["Bucharest"] == optimal == 418
    assert distances["Arad"] == 0
    assert distances["Sibiu"] == 140
    assert distances["Rimnicu Vilcea"] == 220, distances["Rimnicu Vilcea"]
    assert distances["Pitesti"] == 317, distances["Pitesti"]
    # 140 + 80 + 97 + 101 = 418, which is the optimal path, city by city.
    assert 140 + 80 + 97 + 101 == 418

    print(f"  shortest distance from Arad to each of {len(distances)} cities:")
    for city in ("Sibiu", "Rimnicu Vilcea", "Pitesti", "Bucharest", "Neamt"):
        print(f"    {city:16} {distances[city]:>4} km")
    print("       140 + 80 + 97 + 101 = 418, the optimal route accumulated")
    print("       one city at a time. UCS IS DIJKSTRA'S ALGORITHM -- the same")
    print("       procedure, reached from the AI side instead of graph theory")


def dfs_and_bfs_on_a_small_graph():
    """Experiments 9-11 proper: trace both on a graph small enough to check."""
    simple = {k: {v: 1 for v in vs} for k, vs in GRAPH_EDGES.items()}

    bfs_path, bfs_exp = bfs(simple, "a", "g")
    dfs_path, dfs_exp = dfs(simple, "a", "g")

    assert bfs_path == ["a", "c", "g"], bfs_path
    assert dfs_path == ["a", "b", "d", "e", "g"], dfs_path
    assert len(bfs_path) - 1 == 2 and len(dfs_path) - 1 == 4
    assert bfs_exp == dfs_exp == 5, (bfs_exp, dfs_exp)

    print("  graph:  a -> b,c    b -> d    d -> e    e -> g    c -> g")
    print(f"    BFS  {' -> '.join(bfs_path):24} {len(bfs_path) - 1} edges, "
          f"expanded {bfs_exp}")
    print(f"    DFS  {' -> '.join(dfs_path):24} {len(dfs_path) - 1} edges, "
          f"expanded {dfs_exp}")
    print("       SAME AMOUNT OF WORK, TWICE THE PATH. BFS explores level by")
    print("       level so it cannot miss the 2-edge route; DFS dived into b")
    print("       and committed to the long way round. That is the guarantee")
    print("       BFS gives and DFS does not")


def bfs_is_optimal_only_with_equal_step_costs():
    """The condition stated in the property table, demonstrated both ways."""
    unit = {k: {v: 1 for v in vs} for k, vs in GRAPH_EDGES.items()}
    bfs_p, _ = bfs(unit, "a", "g")
    ucs_p, _, ucs_c = ucs(unit, "a", "g")
    assert len(bfs_p) - 1 == ucs_c, "with UNIT costs, BFS's answer IS optimal"

    # Now make the SHORT route expensive; BFS cannot see the difference.
    weighted = {k: {v: 1 for v in vs} for k, vs in GRAPH_EDGES.items()}
    weighted["c"]["g"] = 50
    bfs_p2, _ = bfs(weighted, "a", "g")
    ucs_p2, _, ucs_c2 = ucs(weighted, "a", "g")

    assert bfs_p2 == ["a", "c", "g"], bfs_p2
    assert path_cost(bfs_p2, weighted) == 51, path_cost(bfs_p2, weighted)
    assert ucs_p2 == ["a", "b", "d", "e", "g"], ucs_p2
    assert ucs_c2 == 4, ucs_c2
    assert path_cost(bfs_p2, weighted) > ucs_c2

    print(f"  unit step costs  : BFS cost {len(bfs_p) - 1}, UCS cost {ucs_c}  -- EQUAL")
    print(f"  make c->g cost 50: BFS cost {path_cost(bfs_p2, weighted)} "
          f"({' -> '.join(bfs_p2)})")
    print(f"                     UCS cost {ucs_c2} ({' -> '.join(ucs_p2)})")
    print("       BFS counts EDGES, not cost. With equal step costs those are")
    print("       the same thing and BFS is optimal; the moment they differ,")
    print("       it is not. That is exactly what the property table says")


def iterative_deepening_is_not_wasteful():
    """unit-2.md 2.5's arithmetic: 123,456 against 111,111 at b=10, d=5."""
    def bfs_nodes(b, d):
        return sum(b ** i for i in range(d + 1))

    def ids_nodes(b, d):
        return sum((d + 1 - i) * b ** i for i in range(d + 1))

    b, d = 10, 5
    bfs_total = bfs_nodes(b, d)
    ids_total = ids_nodes(b, d)

    assert bfs_total == 111111, bfs_total
    assert ids_total == 123456, ids_total
    assert ids_total / bfs_total < 1.12

    print(f"  b = {b}, d = {d}:")
    print(f"    BFS generates {bfs_total:,} nodes")
    print(f"    IDS generates {ids_total:,} nodes  "
          f"({(ids_total / bfs_total - 1) * 100:.1f}% more)")
    print(f"    and IDS uses O(bd) = {b * d} memory instead of O(b^d) = {b ** d:,}")
    print("       the repetition is cheap because the BOTTOM LEVEL holds most")
    print("       of the nodes -- regenerating everything above it costs almost")
    print("       nothing. IDS is the preferred uninformed search when the")
    print("       depth is unknown")


def main():
    print("Experiments 9-11 -- Uninformed search: DFS, BFS, uniform cost")
    optimal = the_three_compared()
    ucs_is_dijkstra(optimal)
    dfs_and_bfs_on_a_small_graph()
    bfs_is_optimal_only_with_equal_step_costs()
    iterative_deepening_is_not_wasteful()


if __name__ == "__main__":
    main()
