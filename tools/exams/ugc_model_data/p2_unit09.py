# -*- coding: utf-8 -*-
"""UGC NET Statistics, Unit IX: fifty exam-standard model questions."""
from . import AR, Q, ar, st

TITLE = "Stochastic Processes"
BLURB = ("Markov chains, classification of states, Chapman&ndash;Kolmogorov equations, limiting and stationary "
         "distributions, gambler's ruin, random walks, the Poisson process and its waiting times, birth and "
         "death processes and the M/M/1 queue.")

M = lambda rows: r"\begin{pmatrix}" + r"\\".join("&".join(str(x) for x in r) for r in rows) + r"\end{pmatrix}"
P2 = M([[0.7, 0.3], [0.4, 0.6]])

QUESTIONS = [
 Q(r"A Markov chain on the states $\{0,1\}$ has transition matrix $P=" + P2 + r"$ and initial distribution "
   r"$P(X_0=0)=P(X_0=1)=0.5$. Then $P(X_2=0)$ equals:",
   ["0.550", "0.565", "0.610", "0.571"], "B",
   r"The distribution after one step is $(0.5,0.5)P=(0.55,0.45)$, and after two steps "
   r"$P(X_2=0)=0.55(0.7)+0.45(0.4)=0.565$. ($0.610$ is $p_{00}^{(2)}$, the value when the chain starts in state 0; "
   r"$0.571$ is the limiting value $\tfrac47$.)", "mc"),

 Q(r"For the chain with $P=" + P2 + r"$ and $P(X_0=0)=P(X_0=1)=0.5$, the probability "
   r"$P(X_0=0,\,X_1=1,\,X_2=1)$ is:",
   ["0.18", "0.15", "0.045", "0.09"], "D",
   r"By the Markov property the joint probability is the initial probability times the successive transition "
   r"probabilities: $0.5\times p_{01}\times p_{11}=0.5\times0.3\times0.6=0.09$.", "mc"),

 Q(r"Let $P$ be the transition matrix of a finite Markov chain. Consider the statements:"
   + st("Every row of $P$ sums to 1.", "$P^n$ is a stochastic matrix for every $n\\ge1$.",
        "1 is a characteristic root of $P$.", "Every column of $P$ sums to 1.")
   + "Which of the statements are correct?",
   ["I, II and III only", "I and II only", "I and III only", "I, II, III and IV"], "A",
   r"Rows are probability distributions: (I). A product of stochastic matrices is stochastic: (II). "
   r"$P\mathbf 1=\mathbf 1$, so 1 is a characteristic root with the vector of ones: (III). Columns need not sum "
   r"to 1; when they do the matrix is doubly stochastic, a special case: (IV) is false.", "mc"),

 Q(r"Let $X_1,X_2,\dots$ be independent Bernoulli variables with $P(X_i=1)=p$, $0\lt p\lt1$. Which of the "
   r"following sequences is NOT in general a Markov chain?",
   [r"$S_n=X_1+\cdots+X_n$", r"$M_n=\max(X_1,\dots,X_n)$", r"$Y_n=X_n+X_{n-1}$", r"$X_n$ itself"], "C",
   r"$S_n$ and $M_n$ are functions of their previous value and a fresh independent variable, so they are "
   r"Markov; an independent sequence is trivially Markov. For $Y_n$: given $Y_n=1$, the value of $Y_{n-1}$ helps "
   r"to tell whether $X_n=1$ (if $Y_{n-1}=2$ then $X_{n-1}=1$, so $X_n=0$), and that changes the distribution of "
   r"$Y_{n+1}$. The past matters beyond the present.", "mc"),

 Q(r"For the chain with $P=" + P2 + r"$, the two-step transition probability $p_{01}^{(2)}$ is:",
   ["0.30", "0.39", "0.09", "0.61"], "B",
   r"$p_{01}^{(2)}=p_{00}p_{01}+p_{01}p_{11}=0.7(0.3)+0.3(0.6)=0.39$. The first row of $P^2$ is $(0.61,0.39)$.", "mc"),

 Q(r"A Markov chain on $\{1,2,3,4\}$ has transition matrix "
   r"$" + M([[r"\tfrac12", r"\tfrac12", 0, 0], [r"\tfrac12", r"\tfrac12", 0, 0],
            [0, r"\tfrac13", r"\tfrac13", r"\tfrac13"], [0, 0, 0, 1]]) + r"$. The transient states are:",
   ["1 and 2", "3 and 4", "none", "3 only"], "D",
   r"$\{1,2\}$ is a closed class and $\{4\}$ is absorbing; both are recurrent. From state 3 the chain leaves "
   r"with probability $\tfrac23$ at each step and can never come back, so 3 is transient: the probability of "
   r"ever returning to 3 is $\tfrac13\lt1$.", "class"),

 Q(r"A Markov chain on $\{0,1,2\}$ has $p_{01}=1$, $p_{10}=p_{12}=\tfrac12$ and $p_{21}=1$. The period of each "
   r"state is:",
   ["2", "1", "3", "4"], "A",
   r"The chain alternates between the set $\{0,2\}$ and the state 1, so a return to any state is possible only "
   r"after an even number of steps, and $p_{00}^{(2)}=\tfrac12\gt0$: the period is 2. The chain is irreducible, "
   r"and period is a class property.", "class"),

 Q(r"Consider the statements about Markov chains:"
   + st("Recurrence is a class property.", "Period is a class property.",
        "Every state of a finite irreducible chain is positive recurrent.",
        "All the states of a finite chain can be transient.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "I, II and III only", "I, II, III and IV"], "C",
   r"(I) and (II): communicating states are all recurrent or all transient, and have the same period. (III) A "
   r"finite chain cannot have null recurrent states. (IV) is false: a finite chain must spend infinitely much "
   r"time somewhere, so at least one state is recurrent.", "class"),

 Q(r"For a state $i$ of a Markov chain, $p_{ii}^{(n)}=\dfrac{1}{n^2}$ for all $n\ge2$ and $p_{ii}^{(1)}=0$. "
   r"Then state $i$ is:",
   ["positive recurrent", "transient", "null recurrent", "absorbing"], "B",
   r"A state is recurrent if and only if $\sum_np_{ii}^{(n)}=\infty$. Here "
   r"$\sum_{n\ge2}\tfrac1{n^2}\lt\infty$, so the expected number of returns is finite and the state is transient. "
   r"(With $p_{ii}^{(n)}\sim\tfrac1n$ the state would be recurrent.)", "class"),

 Q(r"The symmetric simple random walk on the integer lattice in one, two and three dimensions is, "
   r"respectively:",
   ["null recurrent, null recurrent, transient", "positive recurrent, null recurrent, transient",
    "null recurrent, transient, transient", "null recurrent, null recurrent, null recurrent"], "A",
   r"P&oacute;lya's theorem: $p_{00}^{(2n)}$ is of order $n^{-d/2}$ in $d$ dimensions, and $\sum n^{-d/2}$ "
   r"diverges for $d=1,2$ and converges for $d\ge3$. In one and two dimensions the walk returns with "
   r"probability 1, but the mean return time is infinite (null recurrent); in three dimensions it returns with "
   r"probability about 0.34 only.", "class"),

 Q(r"An irreducible Markov chain on three states has stationary distribution "
   r"$\left(\tfrac14,\tfrac12,\tfrac14\right)$. The mean recurrence time of the second state is:",
   ["4", "0.5", "3", "2"], "D",
   r"For a positive recurrent state $\mu_j=\dfrac{1}{\pi_j}=\dfrac{1}{1/2}=2$: a state visited half the time is "
   r"revisited on average every 2 steps. The other two states have mean recurrence time 4.", "class"),

 Q(r"A Markov chain on $\{0,1,2,3\}$ has 0 and 3 absorbing, $p_{10}=\tfrac13$, $p_{12}=\tfrac23$, "
   r"$p_{21}=\tfrac13$ and $p_{23}=\tfrac23$. Starting from state 1, the probability of absorption in state 3 is:",
   [r"$\dfrac49$", r"$\dfrac23$", r"$\dfrac47$", r"$\dfrac67$"], "C",
   r"Let $h_i$ be the probability of absorption at 3 from $i$. First-step analysis: $h_1=\tfrac23h_2$ and "
   r"$h_2=\tfrac23+\tfrac13h_1$. So $h_1=\tfrac49+\tfrac29h_1$, giving $h_1=\tfrac47$ (and $h_2=\tfrac67$). "
   r"$\tfrac49$ counts only the direct path $1\to2\to3$.", "class"),

 Q(r"For the Markov chain with $P=" + M([[0, 1], [r"\tfrac12", r"\tfrac12"]]) + r"$ on $\{0,1\}$, the three-step "
   r"probability $p_{00}^{(3)}$ is:",
   [r"$\dfrac12$", r"$\dfrac14$", r"$\dfrac38$", r"$\dfrac18$"], "B",
   r"$P^2=" + M([[r"\tfrac12", r"\tfrac12"], [r"\tfrac14", r"\tfrac34"]]) + r"$ and, by the "
   r"Chapman&ndash;Kolmogorov equations, "
   r"$p_{00}^{(3)}=p_{00}^{(2)}p_{00}+p_{01}^{(2)}p_{10}=\tfrac12(0)+\tfrac12\cdot\tfrac12=\tfrac14$. The only path "
   r"is $0\to1\to1\to0$.", "ck"),

 Q(ar(r"For any states $i,j,k$ and any $m,n\ge0$, $p_{ij}^{(m+n)}\ge p_{ik}^{(m)}\,p_{kj}^{(n)}$.",
      r"$p_{ij}^{(m+n)}=\sum_{k}p_{ik}^{(m)}p_{kj}^{(n)}$, and every term of the sum is non-negative."),
   AR, "A",
   r"(R) is the Chapman&ndash;Kolmogorov equation. A sum of non-negative terms is at least as large as any one "
   r"of them, which gives (A). This inequality is the tool for proving that communication is transitive and "
   r"that recurrence and period are class properties. Both are true and (R) explains (A).", "ck"),

 Q(r"For the chain with $P=" + P2 + r"$, $\displaystyle\lim_{n\to\infty}P^n$ is the matrix each of whose rows is:",
   [r"$\left(\tfrac12,\tfrac12\right)$", r"$\left(\tfrac37,\tfrac47\right)$", r"$(0.7,0.3)$", r"$\left(\tfrac47,\tfrac37\right)$"], "D",
   r"The chain is irreducible and aperiodic, so $P^n$ converges to a matrix with identical rows $\pi$, where "
   r"$\pi=\pi P$: $0.3\pi_0=0.4\pi_1$ with $\pi_0+\pi_1=1$ gives $\pi=\left(\tfrac47,\tfrac37\right)$. For a "
   r"two-state chain $\pi_0=\dfrac{p_{10}}{p_{01}+p_{10}}$.", "nstep"),

 Q(r"For the Markov chain with $P=" + M([[0, 1], [1, 0]]) + r"$:",
   [r"$\lim P^n$ exists and has rows $\left(\tfrac12,\tfrac12\right)$", "there is no stationary distribution",
    r"$\lim P^n$ does not exist, but $\tfrac1n\sum_{k=1}^{n}P^k$ converges to the matrix with rows "
    r"$\left(\tfrac12,\tfrac12\right)$", "both states are transient"], "C",
   r"$P^n$ is $P$ for odd $n$ and $I$ for even $n$, so it oscillates: the chain has period 2. The stationary "
   r"distribution $\left(\tfrac12,\tfrac12\right)$ exists and is unique, and it gives the long-run proportion of "
   r"time in each state: the averages of the powers converge although the powers themselves do not.", "nstep"),

 Q(r"For the two-state chain with $P=" + P2 + r"$, $p_{00}^{(n)}-\tfrac47$ tends to zero like $c\,r^n$, where "
   r"$r$ equals:",
   ["0.3", "0.7", "0.4", "0.6"], "A",
   r"The characteristic roots of $P$ are 1 and $1-p_{01}-p_{10}=1-0.3-0.4=0.3$ (trace $1.3$ minus 1). So "
   r"$p_{00}^{(n)}=\tfrac47+\tfrac37(0.3)^n$; check $n=2$: $0.571+0.039=0.61$. The second largest root governs "
   r"the speed of convergence.", "nstep"),

 Q(r"Consider the statements about an irreducible Markov chain:"
   + st(r"If it is aperiodic and positive recurrent, $\lim_{n\to\infty}p_{ij}^{(n)}=\pi_j$ exists.",
        "That limit does not depend on the initial state $i$.",
        r"If it is periodic, $\lim_{n\to\infty}p_{ij}^{(n)}$ still always exists.",
        r"$\pi_j=1/\mu_j$, where $\mu_j$ is the mean recurrence time of $j$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "I, III and IV only", "I, II, III and IV"], "B",
   r"(I), (II) and (IV) are the ergodic theorem for Markov chains. (III) is false: for a chain of period $d$, "
   r"$p_{jj}^{(n)}=0$ unless $d$ divides $n$, while $p_{jj}^{(nd)}\to d/\mu_j\gt0$, so the sequence has no limit.", "nstep"),

 Q(r"The stationary distribution of the chain with "
   r"$P=" + M([[0.5, 0.5, 0], [0.25, 0.5, 0.25], [0, 0.5, 0.5]]) + r"$ is:",
   [r"$\left(\tfrac13,\tfrac13,\tfrac13\right)$", r"$\left(\tfrac25,\tfrac15,\tfrac25\right)$",
    r"$\left(\tfrac14,\tfrac12,\tfrac14\right)$", r"$\left(\tfrac16,\tfrac23,\tfrac16\right)$"], "C",
   r"Solve $\pi=\pi P$: $\pi_0=0.5\pi_0+0.25\pi_1$ gives $\pi_1=2\pi_0$, and by symmetry $\pi_2=\pi_0$. With "
   r"$\sum\pi_i=1$: $\left(\tfrac14,\tfrac12,\tfrac14\right)$. The matrix is not doubly stochastic (the middle "
   r"column sums to 1.5), so the uniform distribution is not stationary.", "stat"),

 Q(r"An irreducible Markov chain on 5 states has a doubly stochastic transition matrix. Its stationary "
   r"distribution gives each state the probability:",
   [r"$\dfrac15$", r"$\dfrac1{25}$", r"$\dfrac12$", "it depends on the matrix"], "A",
   r"If the columns also sum to 1, then $\left(\tfrac1N,\dots,\tfrac1N\right)P=\left(\tfrac1N,\dots,\tfrac1N\right)$, "
   r"so the uniform distribution is stationary, and for an irreducible finite chain the stationary distribution "
   r"is unique.", "stat"),

 Q(r"If it rains today it rains tomorrow with probability 0.6; if it is dry today it rains tomorrow with "
   r"probability 0.2. In the long run, the proportion of rainy days is:",
   [r"$\dfrac25$", r"$\dfrac12$", r"$\dfrac23$", r"$\dfrac13$"], "D",
   r"With states rain, dry: $\pi_R=0.6\pi_R+0.2\pi_D$, so $0.4\pi_R=0.2\pi_D$, $\pi_D=2\pi_R$ and "
   r"$\pi_R=\tfrac13$. Equivalently $\pi_R=\dfrac{p_{DR}}{p_{DR}+p_{RD}}=\dfrac{0.2}{0.2+0.4}$.", "stat"),

 Q(r"Two balls are distributed between two urns. At each step one of the two balls is chosen at random and "
   r"moved to the other urn (Ehrenfest model). The stationary distribution of the number of balls in the first "
   r"urn, on $\{0,1,2\}$, is:",
   [r"$\left(\tfrac13,\tfrac13,\tfrac13\right)$", r"$\left(\tfrac14,\tfrac12,\tfrac14\right)$",
    r"$\left(0,1,0\right)$", r"$\left(\tfrac12,0,\tfrac12\right)$"], "B",
   r"$p_{01}=1$, $p_{10}=p_{12}=\tfrac12$, $p_{21}=1$. Detailed balance $\pi_0p_{01}=\pi_1p_{10}$ gives "
   r"$\pi_1=2\pi_0$, and similarly $\pi_1=2\pi_2$: the $\text{Bin}(2,\tfrac12)$ distribution "
   r"$\left(\tfrac14,\tfrac12,\tfrac14\right)$. The chain has period 2, so this is the long-run proportion of "
   r"time, not a limit of $p_{ij}^{(n)}$.", "stat"),

 Q(r"Consider the statements:"
   + st("An irreducible finite Markov chain has a unique stationary distribution.",
        "Every irreducible Markov chain has a stationary distribution.",
        r"If $X_0$ has the stationary distribution $\pi$, then $X_n$ has distribution $\pi$ for every $n$.",
        "A chain with two closed communicating classes has infinitely many stationary distributions.")
   + "Which of the statements are correct?",
   ["I and III only", "I, II and III only", "I, III and IV only", "I, II, III and IV"], "C",
   r"(I) and (III) are basic. (II) is false: an irreducible chain has a stationary distribution only if it is "
   r"positive recurrent; the symmetric random walk on the integers has none. (IV) Every mixture "
   r"$\alpha\pi^{(1)}+(1-\alpha)\pi^{(2)}$ of the stationary distributions of the two classes is stationary.", "stat"),

 Q(r"A gambler with 3 rupees plays a fair game, winning or losing 1 rupee each time, until he has 10 rupees or "
   r"is ruined. The probability of his ruin is:",
   ["0.7", "0.3", "0.5", "0.21"], "A",
   r"For a fair game the probability of reaching $N$ before 0 from $i$ is $\dfrac iN=0.3$, so the probability of "
   r"ruin is $1-\dfrac iN=0.7$.", "gambler"),

 Q(r"A gambler wins 1 rupee with probability $\tfrac13$ and loses 1 rupee with probability $\tfrac23$ at each "
   r"play. Starting with 1 rupee, the probability that he reaches 3 rupees before being ruined is:",
   [r"$\dfrac13$", r"$\dfrac19$", r"$\dfrac37$", r"$\dfrac17$"], "D",
   r"With $r=\dfrac qp=2$: $P(\text{reach }N)=\dfrac{1-r^i}{1-r^N}=\dfrac{1-2}{1-8}=\dfrac17$. Check by first-step "
   r"analysis: $h_1=\tfrac13h_2$, $h_2=\tfrac13+\tfrac23h_1$ give $h_1=\tfrac17$.", "gambler"),

 Q(r"In a fair game with unit stakes a gambler starts with 3 rupees and stops on reaching 10 rupees or 0. The "
   r"expected duration of the game is:",
   ["30", "21", "10", "7"], "B",
   r"For $p=\tfrac12$ the expected duration from $i$ is $D_i=i(N-i)=3\times7=21$ plays. It satisfies "
   r"$D_i=1+\tfrac12D_{i+1}+\tfrac12D_{i-1}$ with $D_0=D_N=0$.", "gambler"),

 Q(r"A gambler with 2 rupees plays against an infinitely rich opponent, winning 1 rupee with probability 0.6 "
   r"and losing 1 rupee with probability 0.4 at each play. The probability that he is eventually ruined is:",
   ["1", r"$\dfrac23$", r"$\dfrac49$", r"$\dfrac{4}{25}$"], "C",
   r"Letting $N\to\infty$ in the ruin formula with $p\gt q$: $P(\text{ruin})=\left(\dfrac qp\right)^i="
   r"\left(\dfrac23\right)^2=\dfrac49$. If $p\le\tfrac12$ ruin is certain.", "gambler"),

 Q(r"For the symmetric simple random walk starting at 0, the probability that it is at 0 after 4 steps is:",
   [r"$\dfrac38$", r"$\dfrac14$", r"$\dfrac1{16}$", r"$\dfrac12$"], "A",
   r"It must take two steps up and two down: $u_4=\binom42\left(\tfrac12\right)^4=\dfrac{6}{16}=\dfrac38$.", "rw"),

 Q(r"A simple random walk starts at 0 and moves $+1$ with probability 0.6 and $-1$ with probability 0.4. The "
   r"mean and variance of its position after 100 steps are:",
   ["20 and 24", "60 and 24", "20 and 100", "20 and 96"], "D",
   r"Each step has mean $p-q=0.2$ and variance $1-(p-q)^2=4pq=0.96$. So $E(S_{100})=20$ and "
   r"$V(S_{100})=96$. ($24=npq$ is the variance of the number of upward steps.)", "rw"),

 Q(r"For the simple random walk on the integers with $p=0.6$, $q=0.4$, the probability of ever returning to "
   r"the starting point is:",
   ["1", "0.8", "0.6", "0.4"], "B",
   r"The probability of eventual return is $1-|p-q|=1-0.2=0.8$. It equals 1 only for the symmetric walk; for "
   r"$p\ne q$ the walk drifts away and every state is transient.", "rw"),

 Q(r"For the symmetric simple random walk starting at 0, the probability that the first return to 0 occurs "
   r"at step 4 is:",
   [r"$\dfrac38$", r"$\dfrac14$", r"$\dfrac18$", r"$\dfrac1{16}$"], "C",
   r"The walk must stay strictly on one side for steps 1 to 3 and return at step 4: the paths $++--$ and "
   r"$--++$, each of probability $\tfrac1{16}$, total $\tfrac18$. In general $f_{2n}=\dfrac{u_{2n}}{2n-1}$; here "
   r"$\dfrac{3/8}{3}$.", "rw"),

 Q(r"$\{N(t)\}$ is a Poisson process with rate 2. Then $P\{N(3)=4\mid N(1)=1\}$ is about:",
   ["0.195", "0.134", "0.089", "0.147"], "A",
   r"By independent and stationary increments this is $P\{N(3)-N(1)=3\}=P\{N(2)=3\}$ with mean $2\times2=4$: "
   r"$e^{-4}\dfrac{4^3}{3!}=0.195$.", "poisson"),

 Q(r"For a Poisson process, $P\{N(1)=1\mid N(3)=2\}$ equals:",
   [r"$\dfrac13$", r"$\dfrac29$", r"$\dfrac23$", r"$\dfrac49$"], "D",
   r"Given $N(t)=n$, the $n$ events are independently and uniformly placed on $(0,t)$, so "
   r"$N(s)\sim\text{Bin}\left(n,\tfrac st\right)$. Here $\text{Bin}\left(2,\tfrac13\right)$: "
   r"$2\cdot\tfrac13\cdot\tfrac23=\tfrac49$. The answer does not involve the rate.", "poisson"),

 Q(r"Two independent Poisson processes have rates 2 and 3. The probability that the first event to occur "
   r"comes from the first process is:",
   [r"$\dfrac23$", r"$\dfrac25$", r"$\dfrac12$", r"$\dfrac35$"], "B",
   r"The first events occur after independent exponential times with rates 2 and 3, and "
   r"$P(T_1\lt T_2)=\dfrac{\lambda_1}{\lambda_1+\lambda_2}=\dfrac25$. The superposed process is Poisson with rate 5.", "poisson"),

 Q(r"Customers arrive in a Poisson process at 6 per hour, and each is independently of type A with "
   r"probability $\tfrac13$. The probability that no customer of type A arrives in an hour is about:",
   ["0.0025", "0.018", "0.135", "0.368"], "C",
   r"Thinning a Poisson process gives a Poisson process: type A customers arrive at rate $6\times\tfrac13=2$ per "
   r"hour, independently of the others. $P(\text{none})=e^{-2}=0.135$.", "poisson"),

 Q(r"For a Poisson process with rate 2, the covariance between $N(3)$ and $N(5)$ is:",
   ["6", "10", "30", "0"], "A",
   r"For $s\lt t$, $N(t)=N(s)+[N(t)-N(s)]$ with independent parts, so "
   r"$\operatorname{Cov}(N(s),N(t))=V(N(s))=\lambda s=6$; in general $\lambda\min(s,t)$. The correlation is "
   r"$\sqrt{s/t}=\sqrt{0.6}$.", "poisson"),

 Q(r"Claims arrive in a Poisson process with rate 3 per day; claim sizes are independent with mean 2 and "
   r"variance 1. The mean and variance of the total claim amount in 2 days are:",
   ["12 and 6", "12 and 24", "6 and 30", "12 and 30"], "D",
   r"For a compound Poisson process $E[X(t)]=\lambda tE(Y)=6\times2=12$ and "
   r"$V[X(t)]=\lambda tE(Y^2)=6\,(1+4)=30$. Note $E(Y^2)$, not $V(Y)$.", "poisson"),

 Q(r"For a Poisson process $\{N(t),t\ge0\}$ with rate $\lambda$, consider the statements:"
   + st("It has independent increments.", "It is a (weakly) stationary process.",
        "The times between successive events are independent exponential variables.",
        r"$N(t)-\lambda t$ is a martingale.")
   + "Which of the statements are correct?",
   ["I and III only", "I, III and IV only", "I, II and III only", "I, II, III and IV"], "B",
   r"(I) and (III) are defining properties, and (IV) follows from independent increments with "
   r"$E[N(t)-N(s)]=\lambda(t-s)$. (II) is false: the increments are stationary, but the process itself has mean "
   r"$\lambda t$ and variance $\lambda t$ that grow with $t$.", "poisson"),

 Q(r"Events occur in a Poisson process with rate 2. The mean and variance of the waiting time until the third "
   r"event are:",
   ["1.5 and 1.5", "6 and 12", "1.5 and 0.75", "0.67 and 0.22"], "C",
   r"The waiting time to the $n$th event is the sum of $n$ independent exponential times: gamma with shape $n$ "
   r"and rate $\lambda$. Mean $\dfrac n\lambda=1.5$, variance $\dfrac{n}{\lambda^2}=0.75$.", "inter"),

 Q(r"In a Poisson process exactly 4 events occurred in the interval $(0,10)$. The expected time of the first "
   r"of them is:",
   ["2", "2.5", "5", "1"], "A",
   r"Given $N(t)=n$, the event times are distributed as the order statistics of $n$ independent uniform "
   r"variables on $(0,t)$. The smallest has expectation $\dfrac{t}{n+1}=\dfrac{10}{5}=2$.", "inter"),

 Q(r"The time $T$ between events of a Poisson process with rate 2 satisfies $P(T\gt1\mid T\gt0.5)=$",
   ["0.135", "0.368", "0.607", "0.223"], "B",
   r"The exponential distribution has no memory: $P(T\gt1\mid T\gt0.5)=P(T\gt0.5)=e^{-2(0.5)}=e^{-1}=0.368$. The "
   r"unconditional $P(T\gt1)=e^{-2}=0.135$.", "inter"),

 Q(r"For a Poisson process with rate 1, the probability that the second event occurs before time 1 is about:",
   ["0.632", "0.368", "0.184", "0.264"], "D",
   r"$P(S_2\le1)=P\{N(1)\ge2\}=1-e^{-1}(1+1)=1-0.736=0.264$. The waiting time to the second event exceeds $t$ "
   r"exactly when fewer than two events have occurred by time $t$.", "inter"),

 Q(r"A Yule (linear pure birth) process with birth rate $\lambda=1$ per individual starts with one individual. "
   r"The distribution of the population size at time $t=\ln2$ is:",
   ["Poisson with mean 2", "geometric with mean $\\ln 2$", "geometric on $\\{1,2,\\dots\\}$ with mean 2",
    "binomial"], "C",
   r"For the Yule process with $X(0)=1$, $P\{X(t)=n\}=e^{-\lambda t}(1-e^{-\lambda t})^{n-1}$, $n\ge1$: geometric "
   r"with success probability $e^{-\lambda t}=\tfrac12$ and mean $e^{\lambda t}=2$.", "bd"),

 Q(r"A pure death process starts with 10 individuals, each dying independently at rate $\mu$. At the time "
   r"$t$ with $\mu t=\ln2$, the expected number alive is:",
   ["5", "2.5", "6.93", "3.07"], "A",
   r"Each individual survives to time $t$ with probability $e^{-\mu t}=\tfrac12$, independently, so the number "
   r"alive is $\text{Bin}(10,\tfrac12)$ with mean 5.", "bd"),

 Q(r"A linear birth and death process has birth rate $\lambda=2$ and death rate $\mu=1$ per individual and "
   r"starts with one individual. The probability of ultimate extinction is:",
   ["0", r"$\dfrac12$", r"$\dfrac14$", "1"], "B",
   r"If $\lambda\le\mu$ extinction is certain; if $\lambda\gt\mu$ the probability of extinction from $i$ "
   r"individuals is $\left(\dfrac\mu\lambda\right)^i=\dfrac12$. The mean population size $e^{(\lambda-\mu)t}$ grows "
   r"without bound although extinction still has probability $\tfrac12$.", "bd"),

 Q(r"In a system with Poisson arrivals at rate 4 and infinitely many servers each with exponential service "
   r"rate 2 (birth rates $\lambda_n=4$, death rates $\mu_n=2n$), the stationary probability that the system is "
   r"empty is about:",
   ["0.500", "0.018", "0.368", "0.135"], "D",
   r"$\pi_n=\pi_0\prod_{k=1}^{n}\dfrac{\lambda_{k-1}}{\mu_k}=\pi_0\dfrac{(\lambda/\mu)^n}{n!}$, so the stationary "
   r"distribution is Poisson with mean $\dfrac\lambda\mu=2$, and $\pi_0=e^{-2}=0.135$.", "bd"),

 Q(r"An M/M/1 queue has arrival rate 4 and service rate 5 per hour. The expected number in the system and the "
   r"expected waiting time in the queue (in hours) are:",
   ["4 and 0.8", "4 and 1", "3.2 and 0.8", "5 and 1"], "A",
   r"$\rho=0.8$. $L=\dfrac{\rho}{1-\rho}=4$; $W=\dfrac{1}{\mu-\lambda}=1$ hour in the system; "
   r"$W_q=W-\dfrac1\mu=0.8$ hour; $L_q=\lambda W_q=3.2$. Little's formula $L=\lambda W$ ties them together.", "mm1"),

 Q(r"In an M/M/1 queue with traffic intensity $\rho=0.8$, the stationary probability that there are at least "
   r"3 customers in the system is:",
   ["0.102", "0.488", "0.512", "0.640"], "C",
   r"The stationary distribution is geometric, $\pi_n=(1-\rho)\rho^n$, so $P(N\ge n)=\rho^n=(0.8)^3=0.512$. "
   r"($0.102$ is $P(N=3)$.)", "mm1"),

 Q(r"In an M/M/1 queue with arrival rate 4 and service rate 5 per hour, the probability that a customer "
   r"spends more than 2 hours in the system is about:",
   ["0.018", "0.135", "0.368", "0.108"], "B",
   r"In the steady state the time in the system (waiting plus service) is exponential with rate "
   r"$\mu-\lambda=1$. $P(W\gt2)=e^{-2}=0.135$.", "mm1"),

 Q(r"Consider the statements about the M/M/1 queue with traffic intensity $\rho=\lambda/\mu$:"
   + st(r"A stationary distribution exists if and only if $\rho\lt1$.",
        "The stationary distribution of the number in the system is geometric.",
        r"In the steady state the departure process is Poisson with rate $\lambda$.",
        r"The stationary probability that the server is idle is $\rho$.")
   + "Which of the statements are correct?",
   ["I and II only", "I, II and IV only", "II, III and IV only", "I, II and III only"], "D",
   r"(I) and (II): $\pi_n=(1-\rho)\rho^n$, summable only for $\rho\lt1$. (III) is Burke's theorem. (IV) is false: "
   r"the server is idle with probability $\pi_0=1-\rho$ and busy with probability $\rho$.", "mm1"),
]
