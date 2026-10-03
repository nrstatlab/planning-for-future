# Practical 7 -- random numbers from five distributions, built from an LCG upward
import math

# Step 1: The base generator
class LCG:
    """Lehmer's minimal standard generator: x <- 16807 x mod (2**31 - 1)."""
    def __init__(self, seed=12345):
        self.x = seed
    def uniform(self):
        self.x = (16807 * self.x) % 2147483647
        return self.x / 2147483647

rng = LCG(12345)

# Step 2: Uniform, Bernoulli and binomial
def uniform(a, b):                      # inverse transform on U(0,1)
    return a + (b - a) * rng.uniform()

def bernoulli(p):
    return 1 if rng.uniform() < p else 0

def binomial(n, p):                     # sum of n Bernoulli trials
    return sum(bernoulli(p) for _ in range(n))

# Step 3: Poisson by Knuth's method
def poisson(lam):                       # Knuth: multiply uniforms until below e^-lam
    L, k, prod = math.exp(-lam), 0, 1.0
    while True:
        prod *= rng.uniform()
        if prod <= L:
            return k
        k += 1

# Step 4: Normal by Box-Muller
def normal(mu=0.0, sigma=1.0):          # Box-Muller, one of the pair kept
    u1, u2 = rng.uniform(), rng.uniform()
    z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mu + sigma * z

# Step 5: Exponential by inverse transform
def exponential(lam):                   # inverse transform: -ln(U)/lambda
    return -math.log(rng.uniform()) / lam

# Step 6: Compare a sample with the theory
def summarise(name, sample, mean_th, var_th):
    n = len(sample)
    m = sum(sample) / n
    v = sum((x - m) ** 2 for x in sample) / n
    print(f"{name:12s} n={n}  mean {m:8.4f} (theory {mean_th:7.4f})"
          f"   var {v:9.4f} (theory {var_th:8.4f})")

# Step 7: Draw 20,000 of each and compare
N = 20000
summarise("Uniform(2,8)", [uniform(2, 8) for _ in range(N)], 5.0, 36 / 12)
summarise("Bin(10,0.3)", [binomial(10, 0.3) for _ in range(N)], 3.0, 10 * 0.3 * 0.7)
summarise("Poisson(4)", [poisson(4) for _ in range(N)], 4.0, 4.0)
summarise("Normal(5,2)", [normal(5, 2) for _ in range(N)], 5.0, 4.0)
summarise("Exp(0.5)", [exponential(0.5) for _ in range(N)], 2.0, 4.0)
