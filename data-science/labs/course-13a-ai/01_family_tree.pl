% Experiment 1 -- A family tree in Prolog: ancestor/2, sibling/2, cousin/2.
%
% Run it: swipl 01_family_tree.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 01_family_tree.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: State the facts
parent(ram,   asha).
parent(ram,   ravi).
parent(sita,  asha).
parent(sita,  ravi).
parent(asha,  kiran).
parent(asha,  meena).
parent(ravi,  bhanu).

male(ram).    male(ravi).   male(kiran).  male(bhanu).
female(sita). female(asha). female(meena).

% Step 2: Write the rules
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).

grandparent(X, Y) :- parent(X, Z), parent(Z, Y).

% ancestor/2 -- the recursive one, and the point of the experiment.
% BASE CASE FIRST. Prolog tries clauses top to bottom, so putting the
% recursive clause first makes it recurse before it can ever succeed.
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

descendant(X, Y) :- ancestor(Y, X).

% sibling/2 -- share a parent, and are not the same person.
% Without the X \= Y guard, everyone is their own sibling.
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.

% cousin/2 -- their parents are siblings.
cousin(X, Y) :- parent(A, X), parent(B, Y), sibling(A, B).

% Step 3: Ask the queries
% ?- ancestor(ram, X).            % asha, ravi, kiran, meena, bhanu
% ?- descendant(kiran, X).        % asha, ram, sita
% ?- sibling(asha, X).            % ravi  (twice -- once per shared parent)
% ?- cousin(kiran, X).            % bhanu  (twice -- through each shared parent of
%                                 %  asha and ravi; setof/3 gives it once)
% ?- father(X, kiran).            % no -- kiran's parent asha is female
% ?- findall(X, ancestor(ram, X), L).   % L = [asha, ravi, kiran, meena, bhanu]

% --- WHY sibling(asha, X) GIVES ravi TWICE -----------------------------------
% asha and ravi share BOTH ram and sita, and Prolog reports one solution per
% way of proving the goal. Use setof/3 to get distinct answers:
%   ?- setof(X, sibling(asha, X), L).
% This is a real property of resolution, not a bug, and it is examinable.
