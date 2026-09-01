% Experiment 6 -- greatest common divisor by recursion (Euclid).
%
% *** NOT EXECUTED ***
% This is the SWI-Prolog program for the lab exam. SWI-Prolog cannot be
% installed in the verification environment (the Debian repositories that host
% it are blocked by the egress policy), so this file has never been run here.
% The matching .py file executes the same logic and asserts the answers.
% See notes/sem-5/course-13a-artificial-intelligence/lab.md.

gcd(A, 0, A) :- A > 0.
gcd(A, B, G) :- B > 0, R is A mod B, gcd(B, R, G).

% ?- gcd(48, 18, G).   % G = 6
% ?- gcd(17, 5, G).    % G = 1   (coprime)

% The trace for gcd(48, 18):
%   gcd(48, 18) -> gcd(18, 12) -> gcd(12, 6) -> gcd(6, 0) -> 6
% Each step replaces (A, B) with (B, A mod B), and B strictly decreases, so
% termination is guaranteed. That decreasing measure is the recursion's
% variant, and it is what you point at when asked why it halts.
