% Experiment 15 -- encoding facts and rules in propositional and first-order logic.
%
% Run it: swipl 15_logic.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 06_logic_and_chaining.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]
%
% The propositional half (truth tables, validity, entailment) is computed
% exhaustively in 06_logic_and_chaining.py.

:- encoding(utf8).
% [Corrected: the comments use logic symbols (∀ ⇒ ∧), and under a non-UTF-8
% locale SWI-Prolog warned "Illegal multibyte Sequence" loading the file.]

% Step 1: Encode a propositional fact and rule
% "If it rains, the ground is wet." "It is raining."
raining.
wet_ground :- raining.
% ?- wet_ground.   % true -- modus ponens, mechanised

% To say the same about SNOW you need a whole new symbol and a new rule. That
% is the limitation FOL removes.

% Step 2: Encode first-order facts and one rule
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
