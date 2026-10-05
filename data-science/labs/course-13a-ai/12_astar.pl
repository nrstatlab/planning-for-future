% Experiment 12 -- Greedy Best-First search and A* on the Romania map.
%
% Run it: swipl 12_astar.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 04_informed_search.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]
%
% pytholog cannot evaluate arithmetic, so 04_informed_search.py runs the search
% in Python, and reproduces Russell & Norvig's figures.

% Step 1: State the map
road(arad, zerind, 75).        road(arad, sibiu, 140).
road(arad, timisoara, 118).    road(zerind, oradea, 71).
road(oradea, sibiu, 151).      road(sibiu, fagaras, 99).
road(sibiu, rimnicu, 80).      road(rimnicu, pitesti, 97).
road(rimnicu, craiova, 146).   road(fagaras, bucharest, 211).
road(pitesti, bucharest, 101). road(craiova, pitesti, 138).

edge(X, Y, D) :- road(X, Y, D).
edge(X, Y, D) :- road(Y, X, D).

% Step 2: State the heuristic
% ADMISSIBLE by construction: a straight line can never be longer than a road.
h(arad, 366).      h(bucharest, 0).    h(craiova, 160).
h(fagaras, 176).   h(oradea, 380).     h(pitesti, 100).
h(rimnicu, 193).   h(sibiu, 253).      h(timisoara, 329).
h(zerind, 374).

% Step 3: Search with A*
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

% Step 4: Ask the query
% ?- astar(arad, bucharest, P, C).
%   P = [arad, sibiu, rimnicu, pitesti, bucharest],
%   C = 418
% Press ; and A* goes on to the other routes, in order of cost: 450 via
% Fagaras, then 575, 605, 607 and 762.
%
% GREEDY is the same predicate with f_of(node(_,_,_,H), H) -- ordering by h
% alone. It returns 450 via Fagaras, because Fagaras LOOKS closer (h=176 vs
% 193) and is further by road. Ignoring g is what makes greedy short-sighted.
