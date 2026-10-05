% Experiment 2 -- member/2, append/3, reverse/2, length/2.
%
% Run it: swipl 02_lists.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 02_lists_and_arithmetic.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]
%
% pytholog has NO LIST TERMS, so none of this can run there. The .py file
% checks what these predicates COMPUTE, in Python.

% Step 1: Define member/2
mem(X, [X|_]).
mem(X, [_|T]) :- mem(X, T).

% Step 2: Define append/3
app([], L, L).
app([H|T], L, [H|R]) :- app(T, L, R).

% Step 3: Define reverse/2, with an accumulator
rev(L, R) :- rev_acc(L, [], R).
rev_acc([], Acc, Acc).
rev_acc([H|T], Acc, R) :- rev_acc(T, [H|Acc], R).

% Step 4: Define length/2
len([], 0).
len([_|T], N) :- len(T, N1), N is N1 + 1.

% Step 5: Ask the queries
% ?- mem(b, [a,b,c]).            % true
% ?- app([a,b], [c,d], X).       % X = [a,b,c,d]
% ?- rev([a,b,c], X).            % X = [c,b,a]
% ?- len([a,b,c], N).            % N = 3

% Step 6: Run append/3 backwards
% app/3 RUNS BACKWARDS. It is a RELATION, not a function:
%   ?- app(X, Y, [a,b,c]).
%   X = [],      Y = [a,b,c] ;
%   X = [a],     Y = [b,c]   ;
%   X = [a,b],   Y = [c]     ;
%   X = [a,b,c], Y = []      .
% FOUR solutions from ONE definition. No functional language does this, and it
% is the single best demonstration of what declarative programming means.
