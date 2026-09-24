"""Shared data for the Course 13 A practicals.

ROMANIA is Russell & Norvig's map -- the canonical worked example, so the
figures here can be checked against the textbook. Arad to Bucharest is the
standard query.

STRAIGHT_LINE is the straight-line distance to Bucharest, which is the standard
ADMISSIBLE heuristic: a straight line is never longer than a road, so it can
never overestimate.

FAMILY and GRAPH are the small relational datasets the Prolog experiments use.
"""

# --- Russell & Norvig's Romania, with road distances in km ------------------
ROMANIA = {
    "Arad":           {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind":         {"Arad": 75, "Oradea": 71},
    "Oradea":         {"Zerind": 71, "Sibiu": 151},
    "Sibiu":          {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara":      {"Arad": 118, "Lugoj": 111},
    "Lugoj":          {"Timisoara": 111, "Mehadia": 70},
    "Mehadia":        {"Lugoj": 70, "Drobeta": 75},
    "Drobeta":        {"Mehadia": 75, "Craiova": 120},
    "Craiova":        {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Fagaras":        {"Sibiu": 99, "Bucharest": 211},
    "Pitesti":        {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest":      {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu":        {"Bucharest": 90},
    "Urziceni":       {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova":        {"Urziceni": 98, "Eforie": 86},
    "Eforie":         {"Hirsova": 86},
    "Vaslui":         {"Urziceni": 142, "Iasi": 92},
    "Iasi":           {"Vaslui": 92, "Neamt": 87},
    "Neamt":          {"Iasi": 87},
}

# Straight-line distance to Bucharest -- ADMISSIBLE by construction.
STRAIGHT_LINE = {
    "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242,
    "Eforie": 161, "Fagaras": 176, "Giurgiu": 77, "Hirsova": 151,
    "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
    "Oradea": 380, "Pitesti": 100, "Rimnicu Vilcea": 193, "Sibiu": 253,
    "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374,
}

START, GOAL = "Arad", "Bucharest"


def path_cost(path, graph=ROMANIA):
    """Total road distance along a path of city names."""
    return sum(graph[a][b] for a, b in zip(path, path[1:]))


# --- an INADMISSIBLE heuristic, for the section 3.4 demonstration -----------
def inflated(factor=2.0):
    """Straight-line distance times a factor -- it now OVERESTIMATES."""
    return {city: d * factor for city, d in STRAIGHT_LINE.items()}


# --- the relational datasets the Prolog experiments use ---------------------
FAMILY_FACTS = [
    "parent(ram, asha)",
    "parent(ram, ravi)",
    "parent(sita, asha)",
    "parent(sita, ravi)",
    "parent(asha, kiran)",
    "parent(asha, meena)",
    "parent(ravi, bhanu)",
    "male(ram)", "male(ravi)", "male(kiran)", "male(bhanu)",
    "female(sita)", "female(asha)", "female(meena)",
]

FAMILY_RULES = [
    "ancestor(X, Y) :- parent(X, Y)",
    "ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y)",
    "sibling(X, Y) :- parent(P, X), parent(P, Y), neq(X, Y)",
    "grandparent(X, Y) :- parent(X, Z), parent(Z, Y)",
    "father(X, Y) :- parent(X, Y), male(X)",
    "mother(X, Y) :- parent(X, Y), female(X)",
]

# A small directed graph for the DFS / BFS experiments (8, 9, 10, 11).
# Deliberately shaped so the two strategies DISAGREE: there is a short route
# a -> c -> g and a long one a -> b -> d -> e -> g. BFS finds the short one
# because it explores level by level; DFS dives into b first and finds the
# long one. A graph where they agree teaches nothing.
GRAPH_EDGES = {
    "a": ["b", "c"],
    "b": ["d"],
    "c": ["g"],
    "d": ["e"],
    "e": ["g"],
    "g": [],
}
