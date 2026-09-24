% Experiment 3 -- the maximum element of a list.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

max_list([X], X).
max_list([H|T], M) :- max_list(T, M1), (H > M1 -> M = H ; M = M1).

% ?- max_list([3,7,2,9,4], M).   % M = 9

% NOTE the base case: a ONE-element list, not the empty one. max_list([], M)
% has no answer, because the maximum of nothing is undefined -- and writing
% max_list([], 0) would be wrong for a list of negative numbers.
