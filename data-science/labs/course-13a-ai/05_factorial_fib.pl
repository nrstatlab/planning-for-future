% Experiment 5 -- factorial and Fibonacci.
%
% Run it: swipl 05_factorial_fib.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 02_lists_and_arithmetic.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]
%
% pytholog does not evaluate is/2, so this cannot run there either.

% Step 1: Define factorial
fact(0, 1).
fact(N, F) :- N > 0, N1 is N - 1, fact(N1, F1), F is N * F1.

% Step 2: Define Fibonacci
fib(0, 0).
fib(1, 1).
fib(N, F) :- N > 1, N1 is N-1, N2 is N-2, fib(N1, F1), fib(N2, F2), F is F1+F2.

% Step 3: Ask the queries
% ?- fact(5, F).   % F = 120
% ?- fib(10, F).   % F = 55

% Step 4: Make Fibonacci linear with an accumulator
% fib(10, F) makes 177 recursive calls, because fib(8) is recomputed inside
% both fib(9) and fib(8). It is exponential. Two fixes:
%
% 1. An accumulator pair, which makes it linear:
fib_fast(N, F) :- fib_acc(N, 0, 1, F).
fib_acc(0, A, _, A).
fib_acc(N, A, B, F) :- N > 0, N1 is N-1, C is A+B, fib_acc(N1, B, C, F).
% ?- fib_fast(30, F).   % F = 832040, at once -- fib(30, F) makes 2,692,537 calls
% [Added: nothing asked for fib_fast/2, so it had never been tried.]
%
% 2. assertz/1 to memoise -- Prolog's dynamic programming:
%      :- dynamic fibm/2.
%      fibm(N, F) :- fib(N, F), assertz(fibm(N, F)).
