% Experiment 14 -- N-Queens by backtracking.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

queens(N, Qs) :- numlist(1, N, Ns), permutation(Ns, Qs), safe(Qs).

safe([]).
safe([Q|Qs]) :- no_attack(Q, Qs, 1), safe(Qs).

no_attack(_, [], _).
no_attack(Q, [Q1|Qs], D) :-
    Q =\= Q1 + D,            % not on the down diagonal
    Q =\= Q1 - D,            % not on the up diagonal
    D1 is D + 1,
    no_attack(Q, Qs, D1).

% ?- queens(8, Qs).
%   Qs = [1, 5, 8, 6, 3, 7, 2, 4]  (and 91 more)
% ?- findall(Q, queens(8, Q), L), length(L, N).
%   N = 92
%
% --- WHY permutation/2 IS THE RIGHT REPRESENTATION ---------------------------
% Qs is a list of ROWS, one per column. Using a permutation of 1..N means no
% two queens can share a row OR a column BY CONSTRUCTION -- only the diagonals
% need checking. That reduces the space from N^N (16.7 million for N=8) to N!
% (40,320), before any search happens.
%
% CHOOSING THE REPRESENTATION IS MOST OF THE WORK. This is the same point as
% moving the blank rather than the tiles in the 8-puzzle (unit-2.md 2.1).
%
% Solution counts are famously irregular: 2, 10, 4, 40, 92 for N = 4..8.
% N=6 has FEWER solutions than N=5. There is no formula.
