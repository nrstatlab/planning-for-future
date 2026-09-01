% Experiment 2 -- member/2, append/3, reverse/2, length/2.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% pytholog has NO LIST TERMS, so none of this can run there. The .py file
% checks what these predicates COMPUTE, in Python.

% --- member/2 -----------------------------------------------------------------
mem(X, [X|_]).
mem(X, [_|T]) :- mem(X, T).

% --- append/3 -----------------------------------------------------------------
app([], L, L).
app([H|T], L, [H|R]) :- app(T, L, R).

% --- reverse/2, with an accumulator (linear rather than quadratic) ------------
rev(L, R) :- rev_acc(L, [], R).
rev_acc([], Acc, Acc).
rev_acc([H|T], Acc, R) :- rev_acc(T, [H|Acc], R).

% --- length/2 -----------------------------------------------------------------
len([], 0).
len([_|T], N) :- len(T, N1), N is N1 + 1.

% ?- mem(b, [a,b,c]).            % true
% ?- app([a,b], [c,d], X).       % X = [a,b,c,d]
% ?- rev([a,b,c], X).            % X = [c,b,a]
% ?- len([a,b,c], N).            % N = 3

% --- THE POINT OF THIS EXPERIMENT --------------------------------------------
% app/3 RUNS BACKWARDS. It is a RELATION, not a function:
%   ?- app(X, Y, [a,b,c]).
%   X = [],      Y = [a,b,c] ;
%   X = [a],     Y = [b,c]   ;
%   X = [a,b],   Y = [c]     ;
%   X = [a,b,c], Y = []      .
% FOUR solutions from ONE definition. No functional language does this, and it
% is the single best demonstration of what declarative programming means.
