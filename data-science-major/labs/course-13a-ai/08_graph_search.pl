% Experiments 8-11 -- a graph, DFS, BFS, and comparing path lengths.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

% --- experiment 8: the graph as edge/2 facts ---------------------------------
edge(a, b).  edge(a, c).
edge(b, d).
edge(c, g).
edge(d, e).
edge(e, g).

% --- experiment 9: recursive DFS ---------------------------------------------
% The Visited list is what stops it looping. Without it, a cycle is fatal.
dfs(Start, Goal, Path) :- dfs_helper(Start, Goal, [Start], P), reverse(P, Path).

dfs_helper(Goal, Goal, Visited, Visited).
dfs_helper(Node, Goal, Visited, Path) :-
    edge(Node, Next),
    \+ member(Next, Visited),
    dfs_helper(Next, Goal, [Next|Visited], Path).

% ?- dfs(a, g, P).   % P = [a,b,d,e,g]  -- the LONG way, found first

% --- experiment 10: BFS, with an explicit queue ------------------------------
bfs(Start, Goal, Path) :- bfs_queue([[Start]], Goal, R), reverse(R, Path).

bfs_queue([[Goal|Rest]|_], Goal, [Goal|Rest]).
bfs_queue([[N|Rest]|Others], Goal, Path) :-
    findall([M,N|Rest], (edge(N, M), \+ member(M, [N|Rest])), Children),
    append(Others, Children, NewQueue),      % APPEND -> a FIFO queue
    bfs_queue(NewQueue, Goal, Path).

% ?- bfs(a, g, P).   % P = [a,c,g]  -- the SHORT way

% --- experiment 11: comparing them -------------------------------------------
compare_searches(Start, Goal) :-
    dfs(Start, Goal, DP), length(DP, DL),
    bfs(Start, Goal, BP), length(BP, BL),
    format("DFS: ~w (~w nodes)~nBFS: ~w (~w nodes)~n", [DP, DL, BP, BL]).

% ?- compare_searches(a, g).
%   DFS: [a,b,d,e,g] (5 nodes)
%   BFS: [a,c,g] (3 nodes)
%
% THE ONLY DIFFERENCE IS append(Others, Children, Q) versus
% append(Children, Others, Q). Appending children at the BACK gives a FIFO
% queue and breadth-first order; at the FRONT gives a LIFO stack and
% depth-first. One argument order is the whole distinction between the two
% algorithms, and it is worth showing the examiner.
