% Experiment 3 -- the maximum element of a list.
%
% Run it: swipl 03_maximum.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 02_lists_and_arithmetic.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: Define max_list/2, from a one-element base case
max_list([X], X).
max_list([H|T], M) :- max_list(T, M1), (H > M1 -> M = H ; M = M1).

% Step 2: Ask the query
% ?- max_list([3,7,2,9,4], M).   % M = 9

% NOTE the base case: a ONE-element list, not the empty one. max_list([], M)
% has no answer, because the maximum of nothing is undefined -- and writing
% max_list([], 0) would be wrong for a list of negative numbers.
