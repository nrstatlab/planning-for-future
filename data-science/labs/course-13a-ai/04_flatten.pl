% Experiment 4 -- flatten a nested list into a single-level list.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

flatten([], []) :- !.
flatten([H|T], R) :- !, flatten(H, FH), flatten(T, FT), append(FH, FT, R).
flatten(X, [X]).

% ?- flatten([1,[2,[3,4],5],[[6]],7], X).   % X = [1,2,3,4,5,6,7]

% THREE clauses: the empty list, a list head (recurse into it and append), and
% an atom (wrap it). The cuts make the clauses mutually exclusive -- without
% them, flatten([], X) would also match the third clause and give X = [[]].
% These are RED CUTS: removing them changes the answers, not just the speed.
