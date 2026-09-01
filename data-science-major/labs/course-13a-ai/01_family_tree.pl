% Experiment 1 -- A family tree in Prolog: ancestor/2, sibling/2, cousin/2.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The facts and the recursive rules ARE executed in the matching .py file,
% through pytholog, which implements SLD resolution.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% Run it: swipl 01_family_tree.pl   -- or paste into https://swish.swi-prolog.org/

% --- facts -------------------------------------------------------------------
parent(ram,   asha).
parent(ram,   ravi).
parent(sita,  asha).
parent(sita,  ravi).
parent(asha,  kiran).
parent(asha,  meena).
parent(ravi,  bhanu).

male(ram).    male(ravi).   male(kiran).  male(bhanu).
female(sita). female(asha). female(meena).

% --- rules -------------------------------------------------------------------
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

% --- queries to demonstrate ---------------------------------------------------
% ?- ancestor(ram, X).            % asha, ravi, kiran, meena, bhanu
% ?- descendant(kiran, X).        % asha, ram, sita
% ?- sibling(asha, X).            % ravi  (twice -- once per shared parent)
% ?- cousin(kiran, X).            % bhanu
% ?- father(X, kiran).            % no -- kiran's parent asha is female
% ?- findall(X, ancestor(ram, X), L).   % L = [asha, ravi, kiran, meena, bhanu]

% --- WHY sibling(asha, X) GIVES ravi TWICE -----------------------------------
% asha and ravi share BOTH ram and sita, and Prolog reports one solution per
% way of proving the goal. Use setof/3 to get distinct answers:
%   ?- setof(X, sibling(asha, X), L).
% This is a real property of resolution, not a bug, and it is examinable.
