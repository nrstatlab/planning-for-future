% Experiments 8-11 -- a graph, DFS, BFS, and comparing path lengths.
%
% Run it: swipl 08_graph_search.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 03_uninformed_search.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: Experiment 8: state the graph as edge/2 facts
edge(a, b).  edge(a, c).
edge(b, d).
edge(c, g).
edge(d, e).
edge(e, g).

% Step 2: Experiment 9: search depth-first
% The Visited list is what stops it looping. Without it, a cycle is fatal.
dfs(Start, Goal, Path) :- dfs_helper(Start, Goal, [Start], P), reverse(P, Path).

dfs_helper(Goal, Goal, Visited, Visited).
dfs_helper(Node, Goal, Visited, Path) :-
    edge(Node, Next),
    \+ member(Next, Visited),
    dfs_helper(Next, Goal, [Next|Visited], Path).

% ?- dfs(a, g, P).   % P = [a,b,d,e,g]  -- the LONG way, found first; ; gives [a,c,g]

% Step 3: Experiment 10: search breadth-first, with a queue
bfs(Start, Goal, Path) :- bfs_queue([[Start]], Goal, R), reverse(R, Path).

bfs_queue([[Goal|Rest]|_], Goal, [Goal|Rest]).
bfs_queue([[N|Rest]|Others], Goal, Path) :-
    findall([M,N|Rest], (edge(N, M), \+ member(M, [N|Rest])), Children),
    append(Others, Children, NewQueue),      % APPEND -> a FIFO queue
    bfs_queue(NewQueue, Goal, Path).

% ?- bfs(a, g, P).   % P = [a,c,g]  -- the SHORT way, found first

% Step 4: Experiment 11: compare the paths
compare_searches(Start, Goal) :-
    once(dfs(Start, Goal, DP)), length(DP, DL),     % the FIRST path each one finds
    once(bfs(Start, Goal, BP)), length(BP, BL),
    format("DFS: ~w (~w nodes)~nBFS: ~w (~w nodes)~n", [DP, DL, BP, BL]).
% [Corrected: without once/1, dfs/3 and bfs/3 each find both paths on
% backtracking, so compare_searches printed four comparisons and succeeded four
% times.]

% ?- compare_searches(a, g).
%   DFS: [a,b,d,e,g] (5 nodes)
%   BFS: [a,c,g] (3 nodes)
%
% THE ONLY DIFFERENCE IS append(Others, Children, Q) versus
% append(Children, Others, Q). Appending children at the BACK gives a FIFO
% queue and breadth-first order; at the FRONT gives a LIFO stack and
% depth-first. One argument order is the whole distinction between the two
% algorithms, and it is worth showing the examiner.
