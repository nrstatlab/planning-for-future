% Experiment 7 -- the cut (!) and fail.
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.
%
% pytholog has NO CUT, so this experiment is documented rather than executed.
% The .py file sets out the semantics and asserts the engine limitation.

bird(tweety).
bird(polly).
penguin(pingu).
bird(pingu).

% --- the CUT-FAIL idiom: penguins do not fly ---------------------------------
fly(X) :- penguin(X), !, fail.
fly(X) :- bird(X).

% ?- fly(tweety).   % true
% ?- fly(pingu).    % false  -- the first clause commits and fails, so the
%                   %           second is NEVER tried
%
% REMOVE THE CUT and fly(pingu) succeeds via the second clause. That is a
% RED CUT: it changes the meaning of the program.

% --- GREEN vs RED cuts --------------------------------------------------------
% GREEN CUT: removes only redundant choice points. Deleting it changes speed
%            and nothing else.
% RED CUT:   changes which answers are produced. Deleting it changes meaning.
%
% max_green(X, Y, X) :- X >= Y, !.     % green -- the guard already excludes
% max_green(X, Y, Y) :- X < Y.         %          the other case
%
% max_red(X, Y, X) :- X >= Y, !.       % red -- without the cut, max_red(3,2,2)
% max_red(_, Y, Y).                    %        would also succeed

% --- negation as failure ------------------------------------------------------
not_penguin(X) :- \+ penguin(X).
% ?- not_penguin(tweety).   % true -- tweety is not KNOWN to be a penguin
%
% \+ is NEGATION AS FAILURE under the CLOSED WORLD ASSUMPTION: anything not
% derivable is taken to be false. It is NOT logical negation, which would
% require proving the fact untrue. For an unknown bird, \+ penguin(kiwi)
% succeeds simply because the database has never heard of it.
