# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit II: fifty exam-standard model questions."""
from . import AR, Q, ar, st

TITLE = "Real Analysis and Matrix Algebra"
BLURB = ("Countability, sequences and series, power series, continuity and uniform convergence, "
         "differentiation, Riemann and improper integrals, functions of two variables, vector spaces, rank, "
         "determinants, linear equations, characteristic roots and quadratic forms.")

M = lambda rows: r"\begin{pmatrix}" + r"\\".join("&".join(str(x) for x in r) for r in rows) + r"\end{pmatrix}"

QUESTIONS = [
 Q(r"Consider the following sets:"
   + st("The set of all polynomials with integer coefficients.",
        "The set of all infinite sequences of 0s and 1s.",
        r"The set of all finite subsets of $\mathbb N$.",
        "The set of all irrational numbers in $(0,1)$.")
   + "Which of these sets are countable?",
   ["I only", "I, II and III only", "I and III only", "III and IV only"], "C",
   r"(I) For each degree there are countably many polynomials, and a countable union of countable sets is "
   r"countable. (III) The finite subsets of $\{1,\dots,n\}$ are finitely many for each $n$; again a countable "
   r"union. (II) is uncountable by Cantor's diagonal argument (it has the cardinality of $\mathbb R$). "
   r"(IV) is uncountable, because $(0,1)$ is uncountable and its rational points are countable.", "sets"),

 Q(r"Let $A=\left\{\tfrac1n:n\in\mathbb N\right\}\subset\mathbb R$. Consider the statements:"
   + st("$A$ is a closed set.", "0 is the only limit point of $A$.", r"$A\cup\{0\}$ is compact.", "$A$ is countable.")
   + "Which of the statements are correct?",
   ["I and IV only", "II and IV only", "I, II and III only", "II, III and IV only"], "D",
   r"$\tfrac1n\to 0$, so 0 is a limit point, and no other point is one: (II) true. $0\notin A$, so $A$ does not "
   r"contain all its limit points: (I) false. $A\cup\{0\}$ is closed and bounded, hence compact by "
   r"Heine&ndash;Borel: (III) true. $n\mapsto\tfrac1n$ is a bijection from $\mathbb N$: (IV) true.", "sets"),

 Q(r"$\displaystyle\lim_{n\to\infty}\left(1+\frac{2}{n}\right)^{3n}$ equals:",
   [r"$e^{5}$", r"$e^{6}$", r"$e^{3/2}$", r"$e^{2/3}$"], "B",
   r"$\left(1+\tfrac2n\right)^{3n}=\left[\left(1+\tfrac2n\right)^{n/2}\right]^{6}\to e^{6}$. In general "
   r"$\left(1+\tfrac an\right)^{bn}\to e^{ab}$.", "seq"),

 Q(r"For the sequence $a_n=\sin\dfrac{n\pi}{2}+(-1)^n$, the values of $\limsup a_n$ and $\liminf a_n$ are, "
   r"respectively:",
   [r"$1$ and $-2$", r"$2$ and $-2$", r"$1$ and $-1$", r"$2$ and $0$"], "A",
   r"The sequence has period 4: $n=1$: $1-1=0$; $n=2$: $0+1=1$; $n=3$: $-1-1=-2$; $n=4$: $0+1=1$. Its "
   r"subsequential limits are $0,1,-2$, so $\limsup a_n=1$ and $\liminf a_n=-2$. The value 2 is never reached "
   r"because $\sin\tfrac{n\pi}2=1$ only for odd $n$, where $(-1)^n=-1$.", "seq"),

 Q(r"Let $a_1=1$ and $a_{n+1}=\sqrt{6+a_n}$ for $n\ge1$. Then $\{a_n\}$:",
   ["is unbounded", "converges to 2", "converges to 3", r"converges to $\sqrt6$"], "C",
   r"By induction $a_n\lt 3$ and $a_{n+1}\gt a_n$ (since $6+a\gt a^2$ for $0\lt a\lt 3$), so the sequence is "
   r"increasing and bounded above, hence convergent. The limit satisfies $l^2=6+l$, i.e. $(l-3)(l+2)=0$, and "
   r"$l\gt0$ gives $l=3$.", "seq"),

 Q(r"Consider the statements about real sequences:"
   + st("Every bounded sequence has a convergent subsequence.",
        r"Every Cauchy sequence of rational numbers converges to a rational number.",
        "Every bounded monotone sequence converges.",
        r"If $|a_n|\to|a|$, then $a_n\to a$.")
   + "Which of the statements are correct?",
   ["I and II only", "I and III only", "I, III and IV only", "I, II and III only"], "B",
   r"(I) is the Bolzano&ndash;Weierstrass theorem and (III) the monotone convergence theorem. (II) is false: the "
   r"decimal approximations of $\sqrt2$ form a Cauchy sequence of rationals with no rational limit ($\mathbb Q$ is "
   r"not complete). (IV) is false: $a_n=(-1)^n$ has $|a_n|\to1$ but does not converge.", "seq"),

 Q(r"The sum of the series $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+1)(n+2)}$ is:",
   [r"$\dfrac12$", r"$\dfrac13$", r"$\dfrac16$", r"$\dfrac14$"], "D",
   r"$\dfrac{1}{n(n+1)(n+2)}=\dfrac12\left[\dfrac{1}{n(n+1)}-\dfrac{1}{(n+1)(n+2)}\right]$, which telescopes: "
   r"the sum is $\dfrac12\cdot\dfrac{1}{1\cdot2}=\dfrac14$.", "series"),

 Q(r"The series $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n(\ln n)^{p}}$ converges if and only if:",
   [r"$p\gt 1$", r"$p\ge 1$", r"$p\gt 0$", r"$p\gt 2$"], "A",
   r"By the integral test (or Cauchy's condensation test), compare with "
   r"$\displaystyle\int_2^\infty\frac{dx}{x(\ln x)^p}=\int_{\ln2}^\infty\frac{du}{u^p}$, which converges if and only if "
   r"$p\gt1$. At $p=1$ the series $\sum\tfrac{1}{n\ln n}$ diverges, although very slowly.", "series"),

 Q(r"Consider the statements:"
   + st(r"$\displaystyle\sum\frac{(-1)^n}{\sqrt n}$ is conditionally convergent.",
        r"$\displaystyle\sum\sin\frac1n$ is convergent.",
        r"$\displaystyle\sum_{n=1}^{\infty}\frac{n}{2^n}=2$.",
        "Every rearrangement of an absolutely convergent series converges to the same sum.")
   + "Which of the statements are correct?",
   ["I and III only", "II and IV only", "I, II and IV only", "I, III and IV only"], "D",
   r"(I) Converges by Leibniz's test, but $\sum\tfrac1{\sqrt n}$ diverges: true. (II) $\sin\tfrac1n\big/\tfrac1n\to1$, "
   r"so by limit comparison with $\sum\tfrac1n$ it diverges: false. (III) $\sum nx^n=\dfrac{x}{(1-x)^2}$, which is 2 "
   r"at $x=\tfrac12$: true. (IV) is Dirichlet's rearrangement theorem: true.", "series"),

 Q(r"The sum of the series $\displaystyle\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ is:",
   ["2", "4", "6", "8"], "C",
   r"Differentiating the geometric series twice gives $\displaystyle\sum_{n\ge1}n^2x^n=\frac{x(1+x)}{(1-x)^3}$ for "
   r"$|x|\lt1$. At $x=\tfrac12$: $\dfrac{\tfrac12\cdot\tfrac32}{\tfrac18}=6$. (Probabilistically: it is "
   r"$E(N^2)$ for a geometric variate with $p=\tfrac12$, i.e. $\operatorname{Var}+\text{mean}^2=2+4$.)", "series"),

 Q(ar(r"The terms of the series $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}$ can be rearranged so that "
      r"the new series converges to any prescribed real number.",
      "The series is conditionally convergent."),
   AR, "A",
   r"The series converges (to $\ln 2$) by Leibniz's test, while $\sum\tfrac1n$ diverges, so it is conditionally "
   r"convergent: (R) is true. Riemann's rearrangement theorem says exactly that a conditionally convergent series "
   r"can be rearranged to converge to any real number (or to diverge), so (A) is true and (R) is the reason.", "series"),

 Q(r"The radius of convergence of the power series $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}\,x^n$ is:",
   ["1", r"$e$", r"$\dfrac1e$", r"$\infty$"], "B",
   r"With $a_n=\dfrac{n!}{n^n}$, $\dfrac{a_n}{a_{n+1}}=\dfrac{(n+1)^{n+1}}{(n+1)\,n^n}=\left(1+\dfrac1n\right)^n\to e$. "
   r"So $R=e$.", "power"),

 Q(r"The interval of convergence of $\displaystyle\sum_{n=1}^{\infty}\frac{(x-1)^n}{n\,3^n}$ is:",
   [r"$(-2,4)$", r"$[-2,4]$", r"$[-2,4)$", r"$(-2,4]$"], "C",
   r"The radius is 3, so the series converges for $|x-1|\lt3$. At $x=4$ it is $\sum\tfrac1n$, divergent; at "
   r"$x=-2$ it is $\sum\tfrac{(-1)^n}{n}$, convergent by Leibniz's test. The interval is $[-2,4)$.", "power"),

 Q(r"Which of the following functions is uniformly continuous on the open interval $(0,1)$?",
   [r"$\sin\dfrac1x$", r"$\dfrac1x$", r"$x\sin\dfrac1x$", r"$\ln x$"], "C",
   r"A continuous function on $(0,1)$ is uniformly continuous there if and only if it has finite limits at both "
   r"end points. $x\sin\tfrac1x\to0$ as $x\to0^+$, so it extends continuously to $[0,1]$. $\sin\tfrac1x$ oscillates "
   r"and has no limit at 0; $\tfrac1x$ and $\ln x$ are unbounded near 0.", "functions"),

 Q(r"Let $f(x)=x$ if $x$ is rational and $f(x)=0$ if $x$ is irrational. Then $f$ is continuous:",
   ["only at $x=0$", "at every rational point", "at every irrational point", "nowhere"], "A",
   r"$|f(x)|\le|x|$, so $f(x)\to0=f(0)$ as $x\to0$: continuous at 0. At $c\ne0$, sequences of rationals and of "
   r"irrationals tending to $c$ give the limits $c$ and $0$, which differ, so $f$ is discontinuous at every "
   r"$c\ne0$.", "functions"),

 Q(r"Consider the statements about uniform convergence as $n\to\infty$:"
   + st(r"$f_n(x)=x^n$ converges uniformly on $\left[0,\tfrac12\right]$.",
        r"$f_n(x)=x^n$ converges uniformly on $[0,1]$.",
        r"$g_n(x)=\dfrac{x}{1+nx^2}$ converges uniformly on $\mathbb R$.",
        r"$h_n(x)=\dfrac{nx}{1+n^2x^2}$ converges uniformly on $[0,1]$.")
   + "Which of the statements are correct?",
   ["I only", "I and III only", "I, III and IV only", "II and IV only"], "B",
   r"(I) $\sup|x^n|=2^{-n}\to0$: true. (II) The pointwise limit is 0 on $[0,1)$ and 1 at 1, discontinuous, so the "
   r"convergence of continuous functions cannot be uniform: false. (III) $|g_n|$ is largest at $x=\pm\tfrac1{\sqrt n}$, "
   r"where it equals $\tfrac1{2\sqrt n}\to0$: true. (IV) $h_n\to0$ pointwise but $h_n\left(\tfrac1n\right)=\tfrac12$ "
   r"for every $n$: false.", "functions"),

 Q(r"For $f(x)=x^3-3x$ on $[0,2]$, the point $c\in(0,2)$ given by Lagrange's mean value theorem is:",
   ["1", r"$\dfrac{\sqrt3}{2}$", r"$\sqrt{\dfrac23}$", r"$\dfrac{2}{\sqrt3}$"], "D",
   r"$\dfrac{f(2)-f(0)}{2-0}=\dfrac{2-0}{2}=1$. Solve $f'(c)=3c^2-3=1$: $c^2=\tfrac43$, $c=\tfrac{2}{\sqrt3}\approx1.155$, "
   r"which lies in $(0,2)$. ($c=1$ is where $f'=0$, the point Rolle's theorem would give on $[0,\sqrt3]$.)", "diff"),

 Q(r"The number of real roots of the equation $e^x=1+x+\dfrac{x^2}{2}$ is:",
   ["exactly one", "exactly two", "exactly three", "zero"], "A",
   r"Let $g(x)=e^x-1-x-\tfrac{x^2}2$. Then $g'(x)=e^x-1-x\ge0$, with equality only at $x=0$, so $g$ is strictly "
   r"increasing and has at most one zero. $g(0)=0$, so $x=0$ is the only root. (By Taylor's theorem "
   r"$g(x)=\tfrac{x^3}{6}e^{\xi}$, which has the sign of $x$.)", "diff"),

 Q(r"The coefficient of $x^4$ in the Maclaurin expansion of $e^x\cos x$ is:",
   [r"$\dfrac1{24}$", r"$-\dfrac16$", r"$-\dfrac1{12}$", r"$0$"], "B",
   r"$e^x\cos x=\operatorname{Re}\,e^{(1+i)x}$, so the coefficient of $x^4$ is $\operatorname{Re}\dfrac{(1+i)^4}{4!}$. "
   r"$(1+i)^2=2i$, $(1+i)^4=-4$, giving $-\tfrac{4}{24}=-\tfrac16$. The expansion is "
   r"$1+x-\tfrac{x^3}{3}-\tfrac{x^4}{6}-\cdots$.", "diff"),

 Q(r"Let $f(x)=x^2\sin\dfrac1x$ for $x\ne0$ and $f(0)=0$. Consider the statements:"
   + st(r"$f$ is differentiable at every point of $\mathbb R$.", r"$f'$ is continuous at 0.",
        r"$f'$ is bounded on $[-1,1]$.", r"$f$ is of bounded variation on $[0,1]$.")
   + "Which of the statements are correct?",
   ["I only", "I and II only", "I and III only", "I, III and IV only"], "D",
   r"$f'(0)=\lim_{h\to0}h\sin\tfrac1h=0$ and for $x\ne0$, $f'(x)=2x\sin\tfrac1x-\cos\tfrac1x$: (I) true. "
   r"$\cos\tfrac1x$ has no limit at 0, so $f'$ is not continuous there: (II) false. $|f'(x)|\le 2|x|+1\le3$ on "
   r"$[-1,1]$: (III) true. A function with a bounded derivative is Lipschitz, hence of bounded variation: "
   r"(IV) true.", "diff"),

 Q(r"The value of $\displaystyle\int_0^\infty x^2e^{-x^2}\,dx$ is:",
   [r"$\dfrac{\sqrt\pi}{2}$", r"$\sqrt\pi$", r"$\dfrac{\sqrt\pi}{4}$", r"$\dfrac{\pi}{4}$"], "C",
   r"Put $u=x^2$: the integral is $\dfrac12\displaystyle\int_0^\infty u^{1/2}e^{-u}du=\dfrac12\Gamma\left(\tfrac32\right)"
   r"=\dfrac12\cdot\dfrac{\sqrt\pi}{2}=\dfrac{\sqrt\pi}{4}$. Over the whole line the integral is twice this, "
   r"$\tfrac{\sqrt\pi}{2}$.", "riemann"),

 Q(r"The improper integral $\displaystyle\int_0^\infty\frac{x^{a-1}}{1+x}\,dx$ converges if and only if:",
   [r"$a\gt0$", r"$0\lt a\lt1$", r"$a\lt1$", r"$0\lt a\lt2$"], "B",
   r"Near 0 the integrand behaves like $x^{a-1}$, integrable if and only if $a\gt0$. Near $\infty$ it behaves like "
   r"$x^{a-2}$, integrable if and only if $a\lt1$. Both are needed: $0\lt a\lt1$, and then the value is "
   r"$\dfrac{\pi}{\sin a\pi}=B(a,1-a)$.", "riemann"),

 Q(r"$\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}\frac{n}{n^2+k^2}$ equals:",
   [r"$\dfrac{\pi}{4}$", r"$\dfrac{\pi}{2}$", r"$\ln 2$", r"$1$"], "A",
   r"$\displaystyle\sum_{k=1}^{n}\frac{n}{n^2+k^2}=\frac1n\sum_{k=1}^{n}\frac{1}{1+(k/n)^2}$ is a Riemann sum of "
   r"$\dfrac{1}{1+x^2}$ on $[0,1]$, so the limit is $\displaystyle\int_0^1\frac{dx}{1+x^2}=\tan^{-1}1=\frac\pi4$.", "riemann"),

 Q(r"Consider the statements about Riemann integrability on $[a,b]$:"
   + st(r"The function that is 1 at rational points and 0 at irrational points is not Riemann integrable.",
        "Every monotone function is Riemann integrable.",
        "Every bounded function with finitely many discontinuities is Riemann integrable.",
        r"If $|f|$ is Riemann integrable, then $f$ is Riemann integrable.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and III only", "II, III and IV only", "I, II, III and IV"], "A",
   r"(I) Every upper sum is $b-a$ and every lower sum is 0. (II) and (III) are standard theorems (a bounded function "
   r"is Riemann integrable if and only if its discontinuities form a set of measure zero). (IV) is false: take "
   r"$f=1$ on rationals and $-1$ on irrationals; $|f|\equiv1$ is integrable but $f$ is not. The converse of (IV) "
   r"is the true statement.", "riemann"),

 Q(r"If $F(x)=\displaystyle\int_{x}^{x^2}e^{-t^2}\,dt$, then $F'(1)$ equals:",
   [r"$\dfrac2e$", r"$0$", r"$\dfrac3e$", r"$\dfrac1e$"], "D",
   r"By Leibniz's rule $F'(x)=2x\,e^{-x^4}-e^{-x^2}$. At $x=1$: $\dfrac2e-\dfrac1e=\dfrac1e$. Forgetting the lower "
   r"limit gives $\tfrac2e$.", "riemann"),

 Q(r"The value of $\displaystyle\int_0^{\pi/2}\sin^4\theta\,\cos^2\theta\,d\theta$ is:",
   [r"$\dfrac{\pi}{16}$", r"$\dfrac{3\pi}{32}$", r"$\dfrac{\pi}{32}$", r"$\dfrac{\pi}{8}$"], "C",
   r"$\displaystyle\int_0^{\pi/2}\sin^{2m-1}\theta\cos^{2n-1}\theta\,d\theta=\tfrac12B(m,n)$ with $m=\tfrac52$, $n=\tfrac32$: "
   r"$\dfrac12\cdot\dfrac{\Gamma(5/2)\Gamma(3/2)}{\Gamma(4)}=\dfrac12\cdot\dfrac{\tfrac34\sqrt\pi\cdot\tfrac12\sqrt\pi}{6}"
   r"=\dfrac{\pi}{32}$.", "riemann"),

 Q(r"Let $f(x,y)=\dfrac{xy}{x^2+y^2}$ for $(x,y)\ne(0,0)$ and $f(0,0)=0$. At the origin:",
   ["$f$ is continuous but the partial derivatives do not exist",
    "both partial derivatives exist but $f$ is not continuous",
    "$f$ is continuous and both partial derivatives exist",
    "$f$ is differentiable"], "B",
   r"$f(x,0)=0$ and $f(0,y)=0$ for all $x,y$, so $f_x(0,0)=f_y(0,0)=0$ exist. Along $y=x$, $f=\tfrac12$ for all "
   r"$x\ne0$, while along the axes $f=0$; the limit at the origin does not exist, so $f$ is not continuous, and "
   r"therefore not differentiable. Existence of partial derivatives does not imply continuity.", "two"),

 Q(r"The function $f(x,y)=x^3+y^3-3xy$ has:",
   ["a local maximum at $(1,1)$ and a saddle point at $(0,0)$",
    "local minima at both $(0,0)$ and $(1,1)$",
    "a saddle point at $(1,1)$ and a local minimum at $(0,0)$",
    "a local minimum at $(1,1)$ and a saddle point at $(0,0)$"], "D",
   r"$f_x=3x^2-3y=0$, $f_y=3y^2-3x=0$ give $(0,0)$ and $(1,1)$. With $f_{xx}=6x$, $f_{yy}=6y$, $f_{xy}=-3$: at "
   r"$(1,1)$, $f_{xx}f_{yy}-f_{xy}^2=36-9\gt0$ and $f_{xx}\gt0$, a local minimum with $f=-1$; at $(0,0)$ the "
   r"discriminant is $-9\lt0$, a saddle point.", "two"),

 Q(r"The value of $\displaystyle\int_0^1\!\!\int_x^1e^{y^2}\,dy\,dx$ is:",
   [r"$\dfrac{e-1}{2}$", r"$e-1$", r"$\dfrac e2$", r"$\dfrac{e+1}{2}$"], "A",
   r"$e^{y^2}$ has no elementary antiderivative, so change the order: the region is $0\le x\le y\le1$, and the "
   r"integral is $\displaystyle\int_0^1\!\!\int_0^ye^{y^2}dx\,dy=\int_0^1ye^{y^2}dy=\left[\tfrac12e^{y^2}\right]_0^1=\frac{e-1}{2}$.", "two"),

 Q(r"The maximum value of $xy$ subject to $\dfrac{x^2}{8}+\dfrac{y^2}{2}=1$ is:",
   ["1", "4", "2", r"$2\sqrt2$"], "C",
   r"Lagrange: $y=\lambda\tfrac x4$, $x=\lambda y$ give $y^2=\tfrac{x^2}{4}$, and the constraint then gives $x^2=4$, "
   r"$y^2=1$: $xy=2$ at $(2,1)$ and $(-2,-1)$. Or put $x=2\sqrt2\cos\theta$, $y=\sqrt2\sin\theta$: "
   r"$xy=2\sin2\theta\le2$.", "two"),

 Q(r"The value of $\displaystyle\iint_{x^2+y^2\le1}\frac{dx\,dy}{1+x^2+y^2}$ is:",
   [r"$\dfrac{\pi}{2}\ln2$", r"$2\pi\ln2$", r"$\dfrac{\pi^2}{4}$", r"$\pi\ln2$"], "D",
   r"In polar coordinates the Jacobian is $r$: "
   r"$\displaystyle\int_0^{2\pi}\!\!\int_0^1\frac{r\,dr\,d\theta}{1+r^2}=2\pi\cdot\left[\tfrac12\ln(1+r^2)\right]_0^1=\pi\ln2$.", "two"),

 Q(r"The dimension of the real vector space of all $3\times3$ real symmetric matrices with trace zero is:",
   ["6", "5", "8", "3"], "B",
   r"A $3\times3$ symmetric matrix has $\tfrac{3\cdot4}{2}=6$ free entries. Trace zero is one non-trivial linear "
   r"condition, which lowers the dimension by one: $6-1=5$. (All $3\times3$ matrices with trace zero form a space of "
   r"dimension 8; the skew-symmetric ones, dimension 3.)", "vec"),

 Q(r"$W_1$ and $W_2$ are subspaces of $\mathbb R^5$ with $\dim W_1=3$ and $\dim W_2=4$. The possible values of "
   r"$\dim(W_1\cap W_2)$ are:",
   ["1, 2 or 3", "only 2", "2 or 3", "only 3"], "C",
   r"$\dim(W_1\cap W_2)=\dim W_1+\dim W_2-\dim(W_1+W_2)=7-\dim(W_1+W_2)$. Since $W_2\subseteq W_1+W_2\subseteq\mathbb R^5$, "
   r"$\dim(W_1+W_2)$ is 4 or 5, so the intersection has dimension 3 (when $W_1\subseteq W_2$) or 2.", "vec"),

 Q(r"The vectors $(1,2,3)$, $(2,3,4)$ and $(3,5,k)$ of $\mathbb R^3$ are linearly dependent when $k$ equals:",
   ["7", "6", "8", "5"], "A",
   r"$(1,2,3)+(2,3,4)=(3,5,7)$, so for $k=7$ the third vector is the sum of the first two. Check by the "
   r"determinant: $\begin{vmatrix}1&2&3\\2&3&4\\3&5&k\end{vmatrix}=7-k$, which vanishes only for $k=7$.", "vec"),

 Q(r"$A$ is a real $4\times5$ matrix of rank 3. The dimensions of the solution spaces of $Ax=0$ and of "
   r"$A^{T}y=0$ are, respectively:",
   ["1 and 2", "2 and 2", "3 and 1", "2 and 1"], "D",
   r"Rank&ndash;nullity: $Ax=0$ has $x\in\mathbb R^5$, so the nullity is $5-3=2$. $A^T$ is $5\times4$ with the same "
   r"rank 3 and $y\in\mathbb R^4$, so its nullity is $4-3=1$.", "rank"),

 Q(r"The rank of the $4\times4$ matrix whose diagonal entries are all $-3$ and whose off-diagonal entries are "
   r"all $1$ is:",
   ["4", "3", "2", "1"], "B",
   r"The matrix is $J-4I$, where $J$ is the matrix of ones, with eigenvalues $4,0,0,0$. So $J-4I$ has eigenvalues "
   r"$0,-4,-4,-4$: exactly one zero eigenvalue, and since the matrix is symmetric its rank is $3$. (Each row sums "
   r"to zero, which shows directly that it is singular.)", "rank"),

 Q(r"For real matrices $A$ and $B$ of suitable orders, consider the statements:"
   + st(r"$\operatorname{rank}(AB)\le\min\{\operatorname{rank}A,\operatorname{rank}B\}$.",
        r"$\operatorname{rank}(A+B)\le\operatorname{rank}A+\operatorname{rank}B$.",
        r"$\operatorname{rank}(A^{T}A)=\operatorname{rank}A$.",
        r"$\operatorname{rank}(AB)=\operatorname{rank}(BA)$ whenever $A$ and $B$ are square of the same order.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "I, III and IV only", "I, II, III and IV"], "A",
   r"(I) and (II) are standard. (III) $A^TAx=0\Rightarrow x^TA^TAx=\|Ax\|^2=0\Rightarrow Ax=0$, so $A^TA$ and $A$ "
   r"have the same null space. (IV) is false: with $A=" + M([[0, 1], [0, 0]]) + r"$ and $B=" + M([[1, 0], [0, 0]])
   + r"$, $AB=0$ but $BA=A$ has rank 1.", "rank"),

 Q(r"If $A$ is a $3\times3$ matrix with $\det A=2$, then $\det\big(\operatorname{adj}(2A)\big)$ equals:",
   ["16", "32", "64", "256"], "D",
   r"For an $n\times n$ matrix, $\operatorname{adj}(kA)=k^{n-1}\operatorname{adj}A$ and $\det(\operatorname{adj}A)=(\det A)^{n-1}$. "
   r"So $\operatorname{adj}(2A)=4\operatorname{adj}A$ and $\det=4^3(\det A)^2=64\cdot4=256$. Equivalently "
   r"$\det(2A)=16$ and $16^2=256$.", "det"),

 Q(r"A $3\times3$ matrix $A$ has characteristic roots 1, 2 and 3. Then $\det(A^2-A+I)$ equals:",
   ["6", "36", "21", "11"], "C",
   r"If $\lambda$ is a characteristic root of $A$, then $\lambda^2-\lambda+1$ is one of $A^2-A+I$. These are "
   r"$1,3,7$, and the determinant is their product, $21$. (The trace would be their sum, 11.)", "det"),

 Q(r"The system $x+y+z=6$, $\;x+2y+3z=10$, $\;x+2y+\lambda z=\mu$ has no solution when:",
   [r"$\lambda\ne3$", r"$\lambda=3$ and $\mu\ne10$", r"$\lambda=3$ and $\mu=10$", r"$\lambda\ne3$ and $\mu=10$"], "B",
   r"Subtracting the second equation from the third gives $(\lambda-3)z=\mu-10$. If $\lambda\ne3$ there is a unique "
   r"solution; if $\lambda=3$ and $\mu=10$ the third equation repeats the second and there are infinitely many; "
   r"if $\lambda=3$ and $\mu\ne10$ the ranks of the coefficient and augmented matrices are 2 and 3, so the system "
   r"is inconsistent.", "sys"),

 Q(r"The Gram&ndash;Schmidt process is applied to $v_1=(1,1,0)$, $v_2=(1,0,1)$ in that order. The second vector "
   r"of the orthonormal set obtained is:",
   [r"$\dfrac{1}{\sqrt6}(1,-1,2)$", r"$\dfrac{1}{\sqrt2}(1,-1,0)$", r"$\dfrac{1}{\sqrt3}(1,-1,1)$", r"$\dfrac{1}{\sqrt6}(1,1,-2)$"], "A",
   r"$u_1=\tfrac{1}{\sqrt2}(1,1,0)$. $w_2=v_2-(v_2\cdot u_1)u_1=(1,0,1)-\tfrac12(1,1,0)=\left(\tfrac12,-\tfrac12,1\right)$, "
   r"with $\|w_2\|^2=\tfrac32$. So $u_2=\tfrac{1}{\sqrt6}(1,-1,2)$; check $u_2\cdot u_1=0$. Option D is also "
   r"orthogonal to $u_1$ but does not lie in the span of $v_1,v_2$.", "gs"),

 Q(r"If $A=" + M([[4, 1], [2, 3]]) + r"$, then the trace of $A^3$ is:",
   ["343", "91", "133", "1000"], "C",
   r"The characteristic equation is $\lambda^2-7\lambda+10=0$, so the characteristic roots are 2 and 5. Those of "
   r"$A^3$ are $8$ and $125$, and the trace is their sum, $133$. ($343=7^3$ is the cube of the trace; "
   r"$1000=\det(A^3)$.)", "eig"),

 Q(r"$A$ is a real $3\times3$ matrix with $A^2=A$ and rank 2. Then $\det(I+A)$ equals:",
   ["2", "4", "8", "1"], "B",
   r"The characteristic roots of an idempotent matrix are 0 or 1, and it is diagonalisable with rank equal to "
   r"trace, so the roots are $1,1,0$. Those of $I+A$ are $2,2,1$ and the determinant is $4$.", "eig"),

 Q(r"For $A=" + M([[1, 2], [3, 4]]) + r"$, the Cayley&ndash;Hamilton theorem gives $A^{-1}$ as:",
   [r"$\dfrac12(5I-A)$", r"$\dfrac12(A+5I)$", r"$A-5I$", r"$\dfrac12(A-5I)$"], "D",
   r"The characteristic equation is $\lambda^2-5\lambda-2=0$, so $A^2-5A-2I=0$, i.e. $A(A-5I)=2I$ and "
   r"$A^{-1}=\tfrac12(A-5I)=" + M([[-2, 1], [r"\tfrac32", r"-\tfrac12"]]) + r"$.", "cay"),

 Q(r"Let $A$ be a real $n\times n$ matrix with $A^3=A$. Consider the statements:"
   + st(r"$A$ is diagonalisable over $\mathbb R$.", r"Every characteristic root of $A$ is $0$, $1$ or $-1$.",
        "$A$ is non-singular.", "The trace of $A$ is an integer.")
   + "Which of the statements are correct?",
   ["I and II only", "II and IV only", "I, II and IV only", "I, II, III and IV"], "C",
   r"$A$ satisfies $x^3-x=x(x-1)(x+1)$, so its minimal polynomial divides a product of distinct linear factors: "
   r"$A$ is diagonalisable with roots in $\{0,1,-1\}$, and the trace, a sum of such numbers, is an integer. (III) is "
   r"false: $A=0$ satisfies $A^3=A$.", "cay"),

 Q(r"Consider the statements about real square matrices:"
   + st("The characteristic roots of a symmetric matrix are real.",
        "A skew-symmetric matrix of odd order is singular.",
        "Every characteristic root of an orthogonal matrix has modulus 1.",
        "The product of two symmetric matrices is symmetric.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and III only", "II, III and IV only", "I, II, III and IV"], "A",
   r"(I) and (III) are standard. (II) $\det A=\det A^T=\det(-A)=(-1)^n\det A$, so $\det A=0$ for odd $n$. (IV) is "
   r"false: $(AB)^T=B^TA^T=BA$, which equals $AB$ only when $A$ and $B$ commute.", "sym"),

 Q(r"If $A$ is a real skew-symmetric matrix, then $(I-A)(I+A)^{-1}$ is:",
   ["symmetric", "orthogonal", "skew-symmetric", "idempotent"], "B",
   r"The characteristic roots of $A$ are zero or purely imaginary, so $I+A$ is non-singular. With "
   r"$P=(I-A)(I+A)^{-1}$ and $A^T=-A$: $P^T=(I-A)^{-1}(I+A)$, and since $I-A$ and $I+A$ commute, "
   r"$P^TP=(I-A)^{-1}(I+A)(I-A)(I+A)^{-1}=I$. This is Cayley's transform.", "sym"),

 Q(r"The quadratic form $x^2+y^2+z^2+2a(xy+yz+zx)$ is positive definite if and only if:",
   [r"$-1\lt a\lt1$", r"$a\lt1$", r"$-\dfrac12\lt a\lt1$", r"$a\gt-\dfrac12$"], "C",
   r"Its matrix is $(1-a)I+aJ$, with characteristic roots $1+2a$ (once) and $1-a$ (twice). All are positive if and "
   r"only if $-\tfrac12\lt a\lt1$. The leading principal minors give the same: $1\gt0$, $1-a^2\gt0$, "
   r"$(1-a)^2(1+2a)\gt0$.", "pd"),

 Q(r"The rank and the signature of the quadratic form $2xy+2yz+2zx$ are, respectively:",
   ["2 and 0", "3 and 1", "3 and 3", "3 and $-1$"], "D",
   r"The matrix is $J-I$ (zero diagonal, ones elsewhere) with characteristic roots $2,-1,-1$. All three are "
   r"non-zero, so the rank is 3; there is one positive and two negative roots, so the signature is $1-2=-1$ and "
   r"the form is indefinite.", "pd"),

 Q(ar("If a real symmetric matrix $A$ is positive definite, then $A^{-1}$ is positive definite.",
      r"The characteristic roots of $A^{-1}$ are the reciprocals of the characteristic roots of $A$."),
   AR, "A",
   r"A symmetric matrix is positive definite if and only if all its characteristic roots are positive. $A^{-1}$ is "
   r"symmetric, and its roots are $1/\lambda_i\gt0$. So both statements are true and (R) is the reason for (A).", "pd"),
]
