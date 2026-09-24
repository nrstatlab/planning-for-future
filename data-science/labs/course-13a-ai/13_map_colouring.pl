% Experiment 13 -- map colouring by backtracking.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

colour(red). colour(green). colour(blue).

% Australia. Two regions joined by an edge must differ.
% Prolog's backtracking IS the CSP search -- there is no separate algorithm.
colouring(WA, NT, SA, Q, NSW, V, T) :-
    colour(WA), colour(NT), colour(SA),
    colour(Q), colour(NSW), colour(V), colour(T),
    WA \= NT, WA \= SA,
    NT \= SA, NT \= Q,
    SA \= Q, SA \= NSW, SA \= V,
    Q \= NSW,
    NSW \= V.
    % Tasmania (T) has no land neighbours, so it is unconstrained.

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
