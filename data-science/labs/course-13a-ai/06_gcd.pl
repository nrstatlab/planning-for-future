% Experiment 6 -- greatest common divisor by recursion (Euclid).
%
% Run it: swipl 06_gcd.pl, then type a query at the ?- prompt -- or paste the
% file into https://swish.swi-prolog.org/. Each "% ?-" query below was asked of
% SWI-Prolog 9.0.4 by tools/data-science/prolog_lab.py, and the lab page shows
% what it answered. 02_lists_and_arithmetic.py checks the same logic in Python.
% [Changed: this said the file had never been run, as SWI-Prolog could not be
% installed where these labs are checked. It now installs from the Ubuntu archive.]

% Step 1: Define gcd/3, by Euclid
gcd(A, 0, A) :- A > 0.
gcd(A, B, G) :- B > 0, R is A mod B, gcd(B, R, G).

% Step 2: Ask the queries
% ?- gcd(48, 18, G).   % G = 6
% ?- gcd(17, 5, G).    % G = 1   (coprime)

% The trace for gcd(48, 18):
%   gcd(48, 18) -> gcd(18, 12) -> gcd(12, 6) -> gcd(6, 0) -> 6
% Each step replaces (A, B) with (B, A mod B), and B strictly decreases, so
% termination is guaranteed. That decreasing measure is the recursion's
% variant, and it is what you point at when asked why it halts.
