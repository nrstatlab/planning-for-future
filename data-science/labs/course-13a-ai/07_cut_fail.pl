% Experiment 7 -- the cut (!) and fail.
%
% Run it: swipl 07_cut_fail.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 02_lists_and_arithmetic.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]
%
% pytholog has NO CUT, so the .py file sets out the semantics and asserts the
% engine limitation; the cut itself runs here, in SWI-Prolog.

% Step 1: State the facts
bird(tweety).
bird(polly).
bird(pingu).
penguin(pingu).
% [Corrected: bird(pingu) came after penguin(pingu), so bird/1's clauses were not
% together, and SWI-Prolog warned "Clauses of bird/1 are not together" on loading.]

% Step 2: Write the cut-fail rule
fly(X) :- penguin(X), !, fail.
fly(X) :- bird(X).

% ?- fly(tweety).   % true
% ?- fly(pingu).    % false  -- the first clause commits and fails, so the
%                   %           second is NEVER tried
%
% REMOVE THE CUT and fly(pingu) succeeds via the second clause. That is a
% RED CUT: it changes the meaning of the program.

% Step 3: Tell a green cut from a red one
% GREEN CUT: removes only redundant choice points. Deleting it changes speed
%            and nothing else.
% RED CUT:   changes which answers are produced. Deleting it changes meaning.
%
% max_green(X, Y, X) :- X >= Y, !.     % green -- the guard already excludes
% max_green(X, Y, Y) :- X < Y.         %          the other case
%
% max_red(X, Y, X) :- X >= Y, !.       % red -- without the cut, max_red(3,2,2)
% max_red(_, Y, Y).                    %        would also succeed

% Step 4: Negate by failure
not_penguin(X) :- \+ penguin(X).
% ?- not_penguin(tweety).   % true -- tweety is not KNOWN to be a penguin
%
% \+ is NEGATION AS FAILURE under the CLOSED WORLD ASSUMPTION: anything not
% derivable is taken to be false. It is NOT logical negation, which would
% require proving the fact untrue. For an unknown bird, \+ penguin(kiwi)
% succeeds simply because the database has never heard of it.
