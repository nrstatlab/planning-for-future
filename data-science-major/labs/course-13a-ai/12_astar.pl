% Experiment 12 -- Greedy Best-First search and A* on the Romania map.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% pytholog cannot evaluate arithmetic, so the search itself is executed in
% 04_informed_search.py, which reproduces Russell & Norvig's figures.

% --- the map: edge(From, To, Distance) ---------------------------------------
road(arad, zerind, 75).        road(arad, sibiu, 140).
road(arad, timisoara, 118).    road(zerind, oradea, 71).
road(oradea, sibiu, 151).      road(sibiu, fagaras, 99).
road(sibiu, rimnicu, 80).      road(rimnicu, pitesti, 97).
road(rimnicu, craiova, 146).   road(fagaras, bucharest, 211).
road(pitesti, bucharest, 101). road(craiova, pitesti, 138).

edge(X, Y, D) :- road(X, Y, D).
edge(X, Y, D) :- road(Y, X, D).

% --- the heuristic: straight-line distance to Bucharest ----------------------
% ADMISSIBLE by construction: a straight line can never be longer than a road.
h(arad, 366).      h(bucharest, 0).    h(craiova, 160).
h(fagaras, 176).   h(oradea, 380).     h(pitesti, 100).
h(rimnicu, 193).   h(sibiu, 253).      h(timisoara, 329).
h(zerind, 374).

% --- A* ----------------------------------------------------------------------
astar(Start, Goal, Path, Cost) :-
    h(Start, H),
    astar_search([node(Start, [Start], 0, H)], Goal, RevPath, Cost),
    reverse(RevPath, Path).

astar_search([node(Goal, Path, G, _)|_], Goal, Path, G).
astar_search([node(N, Path, G, _)|Rest], Goal, Result, Cost) :-
    findall(node(M, [M|Path], G2, F2),
            ( edge(N, M, D),
              \+ member(M, Path),
              G2 is G + D,
              h(M, HM),
              F2 is G2 + HM ),
            Children),
    append(Rest, Children, All),
    sort_by_f(All, Sorted),                  % priority queue on f = g + h
    astar_search(Sorted, Goal, Result, Cost).

sort_by_f(Nodes, Sorted) :-
    map_list_to_pairs(f_of, Nodes, Pairs),
    keysort(Pairs, SortedPairs),
    pairs_values(SortedPairs, Sorted).
f_of(node(_, _, _, F), F).

% ?- astar(arad, bucharest, P, C).
%   P = [arad, sibiu, rimnicu, pitesti, bucharest],
%   C = 418
%
% GREEDY is the same predicate with f_of(node(_,_,_,H), H) -- ordering by h
% alone. It returns 450 via Fagaras, because Fagaras LOOKS closer (h=176 vs
% 193) and is further by road. Ignoring g is what makes greedy short-sighted.
