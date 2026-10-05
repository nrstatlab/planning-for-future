% Experiment 4 -- flatten a nested list into a single-level list.
%
% Run it: swipl 04_flatten.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 02_lists_and_arithmetic.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: Define flatten/2 in three clauses
flatten([], []) :- !.
flatten([H|T], R) :- !, flatten(H, FH), flatten(T, FT), append(FH, FT, R).
flatten(X, [X]).

% Step 2: Ask the query
% ?- flatten([1,[2,[3,4],5],[[6]],7], X).   % X = [1,2,3,4,5,6,7]

% THREE clauses: the empty list, a list head (recurse into it and append), and
% an atom (wrap it). The cuts make the clauses mutually exclusive -- without
% them, flatten([], X) would also match the third clause and give X = [[]].
% These are RED CUTS: removing them changes the answers, not just the speed.
