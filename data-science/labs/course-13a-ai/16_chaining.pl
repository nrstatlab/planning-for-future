% Experiment 16 -- forward and backward chaining.
%
% Run it: swipl 16_chaining.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 06_logic_and_chaining.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: State the rule base
fact(a).
fact(b).

c(X) :- fact(a), fact(b), X = derived_c.
d(X) :- c(_), X = derived_d.
e(X) :- d(_), fact(a), X = derived_e.

% Step 2: Chain backward
% ?- e(X).
%   To prove e, it needs d; to prove d, it needs c; to prove c, it needs the
%   facts a and b. It proves ONLY what the goal requires, and touches nothing
%   else. Goal-driven, depth-first.

% Step 3: Chain forward
% Prolog does not do it, so you drive it with assertz/1. The same three rules,
% written as data: rule(Premises, Conclusion).
:- dynamic known/1.

rule([a, b], c).
rule([c], d).
rule([d, a], e).

forward :-
    (   rule(Premises, Conclusion),
        all_known(Premises),
        \+ known(Conclusion)
    ->  assertz(known(Conclusion)),
        format("derived ~w~n", [Conclusion]),
        forward
    ;   true
    ).

all_known([]).
all_known([P|Ps]) :- known(P), all_known(Ps).

% start from the facts a and b
start :- retractall(known(_)), assertz(known(a)), assertz(known(b)).

% ?- start, forward, findall(K, known(K), KB).
%   derived c, then d, then e -- KB = [a, b, c, d, e]
%
% It loops until no rule adds anything new, deriving EVERYTHING derivable --
% including whatever nobody asked for. Data-driven.
% [Corrected: forward/0 was only a comment, so forward chaining could not be
% run; it is now code, and the query above runs it.]

% Step 4: Ask for a goal nothing defines
% ?- z(X).
%   SWI-Prolog does not answer false: it raises an existence error, because
%   no clause for z/1 exists at all. (unknown/2 can make it fail quietly.)

% --- WHICH TO USE ------------------------------------------------------------
% Few facts, many possible conclusions  -> FORWARD.  A sensor reading arrives;
%                                          work out everything it implies.
% Many facts, ONE question              -> BACKWARD. "Does this patient have
%                                          malaria?" -- do not derive every
%                                          other disease first.
%
% And the practical consequence of Prolog's DEPTH-FIRST backward chaining:
% a LEFT-RECURSIVE rule loops for ever.
%
%   anc(X, Y) :- anc(X, Z), parent(Z, Y).     % INFINITE LOOP
%   anc(X, Y) :- parent(X, Y).
%
% Clause order matters in Prolog and does NOT matter in logic. That gap is the
% price of an efficient, incomplete proof procedure.
