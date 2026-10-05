% Experiment 18 -- a DCG grammar for simple English sentences.
%
% Run it: swipl 18_dcg.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 07_bayes_and_local_search.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]
%
% pytholog has NO DCG notation. 07_bayes_and_local_search.py runs the
% equivalent recursive-descent parser and checks the parses.

% Step 1: Write the grammar
sentence      --> noun_phrase, verb_phrase.

noun_phrase   --> determiner, noun.
noun_phrase   --> determiner, adjective, noun.

verb_phrase   --> verb, noun_phrase.        % transitive
verb_phrase   --> verb.                     % intransitive

determiner --> [the].
determiner --> [a].
noun       --> [cat].
noun       --> [dog].
noun       --> [mouse].
adjective  --> [big].
adjective  --> [small].
verb       --> [chases].
verb       --> [sees].
verb       --> [sleeps].

% Step 2: Parse the sentences
% ?- sentence([the, big, cat, chases, a, mouse], []).   % true
% ?- sentence([the, dog, sleeps], []).                  % true
% ?- sentence([cat, the, chases], []).                  % false

% Step 3: Build a syntax tree
s(s(NP, VP))      --> np(NP), vp(VP).
np(np(D, N))      --> det(D), n(N).
np(np(D, A, N))   --> det(D), adj(A), n(N).
vp(vp(V, NP))     --> v(V), np(NP).
vp(vp(V))         --> v(V).

det(det(the)) --> [the].
det(det(a))   --> [a].
n(n(cat))     --> [cat].
n(n(mouse))   --> [mouse].
adj(adj(big)) --> [big].
v(v(chases))  --> [chases].

% ?- s(Tree, [the, big, cat, chases, a, mouse], []).
%   Tree = s(np(det(the), adj(big), n(cat)),
%            vp(v(chases), np(det(a), n(mouse))))

% --- WHAT A DCG ACTUALLY IS ---------------------------------------------------
% --> is syntactic sugar. Prolog rewrites
%     sentence --> noun_phrase, verb_phrase.
% into
%     sentence(S0, S) :- noun_phrase(S0, S1), verb_phrase(S1, S).
% threading the token list through as a DIFFERENCE LIST -- S0 is the input and
% S what remains. Calling with [] as the second argument demands that the whole
% list is consumed.
%
% So a DCG is grammar written as INFERENCE RULES, and parsing is resolution.
% This is the point where Units 2-3 (search) and Unit 4 (logic) meet: the
% parser IS a search over derivations, driven by unification.
%
% It also runs BACKWARDS -- ?- s(Tree, S, []). GENERATES sentences.
