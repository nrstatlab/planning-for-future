% Experiment 15 -- encoding facts and rules in propositional and first-order logic.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% The propositional half (truth tables, validity, entailment) is computed
% exhaustively in 06_logic_and_chaining.py.

% --- PROPOSITIONAL: no variables, one symbol per fact ------------------------
% "If it rains, the ground is wet." "It is raining."
raining.
wet_ground :- raining.
% ?- wet_ground.   % true -- modus ponens, mechanised

% To say the same about SNOW you need a whole new symbol and a new rule. That
% is the limitation FOL removes.

% --- FIRST ORDER: objects, relations, and one rule for all of them -----------
student(asha).   student(ravi).   student(meena).
studies(asha).   studies(meena).
teacher(rao).

% "All students who study, pass."   ∀x Student(x) ∧ Studies(x) ⇒ Passes(x)
passes(X) :- student(X), studies(X).

% ?- passes(asha).      % true
% ?- passes(ravi).      % false -- ravi does not study
% ?- findall(X, passes(X), L).   % L = [asha, meena]

% --- THE QUANTIFIER PAIRING RULE ---------------------------------------------
%   ∀ GOES WITH ⇒ .    ∃ GOES WITH ∧ .
%
%   ∀x Student(x) ⇒ Passes(x)     "all students pass"           CORRECT
%   ∀x Student(x) ∧ Passes(x)     "EVERYTHING is a student
%                                  and passes"                   WRONG
%   ∃x Student(x) ∧ Passes(x)     "some student passes"          CORRECT
%   ∃x Student(x) ⇒ Passes(x)     vacuously true as soon as
%                                  anything is not a student     WRONG
%
% A Prolog RULE is a universally quantified implication with the head as the
% consequent, so 'passes(X) :- student(X), studies(X).' IS
% ∀x (Student(x) ∧ Studies(x)) ⇒ Passes(x). The pairing is built into the
% syntax, which is why Prolog makes this error hard to commit.

% --- NESTED QUANTIFIERS, which is the other trap -----------------------------
% ∀x ∃y Loves(x, y)   -- everybody loves SOMEONE (possibly different people)
% ∃y ∀x Loves(x, y)   -- there is ONE person everybody loves
% NOT the same claim. Skolemising the first gives Loves(x, f(x)) -- a FUNCTION
% of x -- and the second gives Loves(x, s1) with a CONSTANT.
