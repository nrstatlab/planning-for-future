% Experiment 5 -- factorial and Fibonacci.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% pytholog does not evaluate is/2, so this cannot run there either.

fact(0, 1).
fact(N, F) :- N > 0, N1 is N - 1, fact(N1, F1), F is N * F1.

fib(0, 0).
fib(1, 1).
fib(N, F) :- N > 1, N1 is N-1, N2 is N-2, fib(N1, F1), fib(N2, F2), F is F1+F2.

% ?- fact(5, F).   % F = 120
% ?- fib(10, F).   % F = 55

% --- WHY THE NAIVE fib/2 IS SLOW ---------------------------------------------
% fib(10, F) makes 177 recursive calls, because fib(8) is recomputed inside
% both fib(9) and fib(8). It is exponential. Two fixes:
%
% 1. An accumulator pair, which makes it linear:
fib_fast(N, F) :- fib_acc(N, 0, 1, F).
fib_acc(0, A, _, A).
fib_acc(N, A, B, F) :- N > 0, N1 is N-1, C is A+B, fib_acc(N1, B, C, F).
%
% 2. assertz/1 to memoise -- Prolog's dynamic programming:
%      :- dynamic fibm/2.
%      fibm(N, F) :- fib(N, F), assertz(fibm(N, F)).
