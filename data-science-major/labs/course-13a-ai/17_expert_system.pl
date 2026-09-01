% Experiment 17 -- a rule-based expert system with an explanation facility.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% The rule base IS executed in 06_logic_and_chaining.py, through pytholog.

% =============================================================================
% KNOWLEDGE BASE -- general, persistent, written by the knowledge engineer
% =============================================================================
viral(X)        :- fever(X), cough(X).
flu(X)          :- viral(X), fatigue(X).
bacterial(X)    :- fever(X), rash(X).
strep(X)        :- bacterial(X), sore_throat(X).
rest_advised(X) :- flu(X).
antibiotic(X)   :- bacterial(X).

% =============================================================================
% WORKING MEMORY -- facts about THIS case, cleared for the next patient
% =============================================================================
:- dynamic fever/1, cough/1, fatigue/1, rash/1, sore_throat/1.

fever(patient).
cough(patient).
fatigue(patient).

% ?- flu(patient).            % true
% ?- rest_advised(patient).   % true
% ?- bacterial(patient).      % false -- no rash was recorded

% =============================================================================
% EXPLANATION FACILITY -- "HOW did you conclude that?"
% =============================================================================
% Re-run the proof, printing each step. In a real system the inference engine
% records the derivation as it goes.
explain(Goal) :- explain(Goal, 0).

explain(Goal, Depth) :-
    clause(Goal, Body),
    tab(Depth), format("~w  because:~n", [Goal]),
    D1 is Depth + 2,
    explain_body(Body, D1).
explain(Goal, Depth) :-
    \+ clause(Goal, _), call(Goal),
    tab(Depth), format("~w  -- a fact in working memory~n", [Goal]).

explain_body(true, _) :- !.
explain_body((A, B), D) :- !, explain_body(A, D), explain_body(B, D).
explain_body(G, D) :- explain(G, D).

% ?- explain(rest_advised(patient)).
%   rest_advised(patient)  because:
%     flu(patient)  because:
%       viral(patient)  because:
%         fever(patient)  -- a fact in working memory
%         cough(patient)  -- a fact in working memory
%       fatigue(patient)  -- a fact in working memory
%
% THAT is what an expert system has and a neural network does not. The chain
% IS the explanation, and it falls out of the proof for free.
%
% "WHY are you asking?" is the other direction: when the system requests a
% symptom, it names the rule it is trying to establish and which premise is
% still missing.

% --- THE CLOSED WORLD ASSUMPTION, and why it makes the system BRITTLE --------
% ?- bacterial(patient).   % false
%
% That "false" means "I cannot prove it", NOT "the patient does not have a
% bacterial infection". The system reports the same answer for "definitely
% not" and "nobody told me". A human expert who meets an unfamiliar case says
% so; an expert system produces a confident wrong answer. See unit-5.md 5.1.
