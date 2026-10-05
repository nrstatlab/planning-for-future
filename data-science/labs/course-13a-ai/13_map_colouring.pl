% Experiment 13 -- map colouring by backtracking.
%
% Run it: swipl 13_map_colouring.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 05_csp_backtracking.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: State the colours
colour(red). colour(green). colour(blue).

% Australia. Two regions joined by an edge must differ.
% Prolog's backtracking IS the CSP search -- there is no separate algorithm.
% Step 2: Write the constraints
colouring(WA, NT, SA, Q, NSW, V, T) :-
    colour(WA), colour(NT), colour(SA),
    colour(Q), colour(NSW), colour(V), colour(T),
    WA \= NT, WA \= SA,
    NT \= SA, NT \= Q,
    SA \= Q, SA \= NSW, SA \= V,
    Q \= NSW,
    NSW \= V.
    % Tasmania (T) has no land neighbours, so it is unconstrained.

% Step 3: Ask the query
% ?- colouring(WA, NT, SA, Q, NSW, V, T).
%   WA = red, NT = green, SA = blue, Q = red, NSW = green, V = red, T = red
%
% --- WHY THE CONSTRAINT ORDER MATTERS ----------------------------------------
% Written as above, Prolog generates all seven colours and THEN tests -- 3^7 =
% 2187 combinations. Interleaving generate and test prunes far earlier:
%
%   colouring2(WA, NT, SA, Q, NSW, V, T) :-
%       colour(WA), colour(NT), WA \= NT,
%       colour(SA), SA \= WA, SA \= NT,
%       colour(Q),  Q \= NT, Q \= SA,
%       ...
%
% That is FORWARD CHECKING by hand, and it is why the heuristics of unit-3.md
% section 3.8 exist. SA borders every mainland region, so MRV and the degree
% heuristic both choose it first -- and once SA is fixed, every neighbour has
% only two colours left.
