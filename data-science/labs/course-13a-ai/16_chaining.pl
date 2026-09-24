% Experiment 16 -- forward and backward chaining.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

% --- the rule base -----------------------------------------------------------
fact(a).
fact(b).

c(X) :- fact(a), fact(b), X = derived_c.
d(X) :- c(_), X = derived_d.
e(X) :- d(_), fact(a), X = derived_e.

% --- BACKWARD CHAINING is what Prolog does natively --------------------------
% ?- e(X).
%   To prove e, it needs d; to prove d, it needs c; to prove c, it needs the
%   facts a and b. It proves ONLY what the goal requires, and touches nothing
%   else. Goal-driven, depth-first.

% --- FORWARD CHAINING has to be written explicitly ---------------------------
% Prolog does not do it, so you drive it with assertz/1:
%
%   :- dynamic known/1.
%
%   forward :-
%       ( rule(Premises, Conclusion),
%         all_known(Premises),
%         \+ known(Conclusion)
%       -> assertz(known(Conclusion)), forward
%       ;  true ).
%
%   all_known([]).
%   all_known([P|Ps]) :- known(P), all_known(Ps).
%
% It loops until no rule adds anything new, deriving EVERYTHING derivable --
% including whatever nobody asked for. Data-driven.

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
