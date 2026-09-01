% Experiment 19 -- a deterministic Naive Bayes calculation for categorical data.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% 07_bayes_and_local_search.py computes the same posteriors and asserts them
% against Course 8's and Course 12 A's figures.

% --- the training data: play tennis, 14 days ---------------------------------
% day(Outlook, Temperature, Humidity, Wind, Play)
day(sunny,    hot,  high,   weak,   no).
day(sunny,    hot,  high,   strong, no).
day(overcast, hot,  high,   weak,   yes).
day(rain,     mild, high,   weak,   yes).
day(rain,     cool, normal, weak,   yes).
day(rain,     cool, normal, strong, no).
day(overcast, cool, normal, strong, yes).
day(sunny,    mild, high,   weak,   no).
day(sunny,    cool, normal, weak,   yes).
day(rain,     mild, normal, weak,   yes).
day(sunny,    mild, normal, strong, yes).
day(overcast, mild, high,   strong, yes).
day(overcast, hot,  normal, weak,   yes).
day(rain,     mild, high,   strong, no).

% --- counting -----------------------------------------------------------------
count_class(C, N) :- findall(1, day(_,_,_,_,C), L), length(L, N).
total(N) :- findall(1, day(_,_,_,_,_), L), length(L, N).

count_feature(1, V, C, N) :- findall(1, day(V,_,_,_,C), L), length(L, N).
count_feature(2, V, C, N) :- findall(1, day(_,V,_,_,C), L), length(L, N).
count_feature(3, V, C, N) :- findall(1, day(_,_,V,_,C), L), length(L, N).
count_feature(4, V, C, N) :- findall(1, day(_,_,_,V,C), L), length(L, N).

prior(C, P) :- count_class(C, N), total(T), P is N / T.

likelihood(I, V, C, P) :-
    count_feature(I, V, C, N), count_class(C, D), P is N / D.

posterior([O,T,H,W], C, P) :-
    prior(C, Pc),
    likelihood(1, O, C, P1), likelihood(2, T, C, P2),
    likelihood(3, H, C, P3), likelihood(4, W, C, P4),
    P is Pc * P1 * P2 * P3 * P4.

classify(Obs, Class) :-
    posterior(Obs, yes, Py), posterior(Obs, no, Pn),
    ( Py > Pn -> Class = yes ; Class = no ).

% ?- posterior([sunny, cool, high, strong], yes, P).   % P = 0.005291...
% ?- posterior([sunny, cool, high, strong], no,  P).   % P = 0.020571...
% ?- classify([sunny, cool, high, strong], C).          % C = no
%
% Normalised: no 79.54%, yes 20.46%.

% --- THE ZERO-FREQUENCY PROBLEM -----------------------------------------------
% 'overcast' NEVER occurs with play=no, so likelihood(1, overcast, no, P) gives
% P = 0, and since the posterior is a PRODUCT, the whole thing collapses to
% zero however strongly the other three features argue for 'no'.
%
% LAPLACE SMOOTHING: add 1 to every count, and add the number of distinct
% values to the denominator:
smoothed(I, V, C, K, P) :-
    count_feature(I, V, C, N), count_class(C, D),
    P is (N + 1) / (D + K).
%
% With K = 3 outlook values: (0 + 1) / (5 + 3) = 0.125 instead of 0.
