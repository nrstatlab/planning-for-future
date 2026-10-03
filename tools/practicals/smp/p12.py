# Practical 12 -- one-way and two-way analysis of variance, built from the
# correction factor upward, with the F tail area taken from tails.py
import math
from tails import F_upper

# Step 1: Print an analysis of variance table
def anova_table(rows, source_names):
    print(f"  {'Source':<14}{'SS':>12}{'df':>5}{'MS':>12}{'F':>10}{'p':>12}")
    err_ss, err_df = rows[-1][1], rows[-1][2]
    err_ms = err_ss / err_df
    for name, ss, df in rows[:-1]:
        ms = ss / df
        F = ms / err_ms
        print(f"  {name:<14}{ss:12.4f}{df:5d}{ms:12.4f}{F:10.4f}{F_upper(F, df, err_df):>12.4g}")
    print(f"  {'Error':<14}{err_ss:12.4f}{err_df:5d}{err_ms:12.4f}")
    tot_ss = sum(r[1] for r in rows)
    tot_df = sum(r[2] for r in rows)
    print(f"  {'Total':<14}{tot_ss:12.4f}{tot_df:5d}")

# Step 2: One-way: correction factor, then the sums of squares
groups = {"A": [20, 22, 19, 24, 25],
          "B": [27, 25, 30, 28, 26],
          "C": [23, 21, 24, 22, 25]}
allv = [v for g in groups.values() for v in g]
N = len(allv)
G = sum(allv)
CF = G * G / N
SST = sum(v * v for v in allv) - CF
SSTr = sum(sum(g) ** 2 / len(g) for g in groups.values()) - CF
SSE = SST - SSTr
print(f"one-way:  N = {N}  G = {G}  CF = {CF:.4f}")
anova_table([("Treatments", SSTr, len(groups) - 1),
             (None, SSE, N - len(groups))], None)

# Step 3: Two-way, one observation per cell
# rows = varieties, columns = blocks
tab = [[18, 22, 20, 16],
       [23, 25, 26, 21],
       [15, 19, 18, 14]]
r, c = len(tab), len(tab[0])
vals = [v for row in tab for v in row]
N2 = r * c
G2 = sum(vals)
CF2 = G2 * G2 / N2
SST2 = sum(v * v for v in vals) - CF2
SSR = sum(sum(row) ** 2 for row in tab) / c - CF2
SSC = sum(sum(tab[i][j] for i in range(r)) ** 2 for j in range(c)) / r - CF2
SSE2 = SST2 - SSR - SSC
print()
print(f"two-way:  N = {N2}  G = {G2}  CF = {CF2:.4f}")
anova_table([("Varieties", SSR, r - 1),
             ("Blocks", SSC, c - 1),
             (None, SSE2, (r - 1) * (c - 1))], None)
# Step 4: Check that the parts add back to the total
print(f"  check: SSR + SSC + SSE = {SSR + SSC + SSE2:.4f}  and  SST = {SST2:.4f}")
