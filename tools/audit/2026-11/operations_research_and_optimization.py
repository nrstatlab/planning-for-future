#!/usr/bin/env python3
"""Recompute the worked answers of Operations Research and Optimization Techniques."""
from itertools import permutations
import numpy as np
from scipy.optimize import linprog, linear_sum_assignment

ok = lambda a, b, tol=1e-6: abs(a - b) <= tol * max(1, abs(b))
def lp(c, A=None, b=None, sense="max"):
    r = linprog([-v for v in c] if sense == "max" else c, A_ub=A, b_ub=b, method="highs")
    return (-r.fun if sense == "max" else r.fun), r.x

# Operations Research
assert ok(lp([3, 5], [[1, 0], [0, 2], [3, 2]], [4, 12, 18])[0], 36)
assert ok(lp([20, 10], [[-1, -2], [-3, -1], [-4, -3]], [-40, -30, -60], "min")[0], 260)
assert ok(lp([2, 1, 3], [[1, 1, 1], [1, 0, 0], [0, 0, 1]], [4, 2, 1])[0], 8)
assert ok(lp([4, 6], [[2, 3], [1, 4]], [24, 20])[0], 48) and ok(lp([3, 2], [[1, 1], [1, 3]], [4, 6])[0], 12)
assert ok(lp([2, 4, 3], [[3, 4, 2], [2, 1, 2], [1, 3, 2]], [60, 40, 80])[0], 230 / 3)
assert ok(lp([5, 4], [[-2, -1], [-1, -2]], [-12, -12], "min")[0], 36)
assert ok(lp([4, 5], [[2, 1], [1, 2]], [8, 10])[0], 28) and ok(lp([8, 10], [[-2, -1], [-1, -2]], [-4, -5], "min")[0], 28)
assert ok(lp([3, 2, 1], [[-3, -1, -1], [3, -3, -1]], [-3, -6], "min")[0], 4.5)
assert ok(lp([5, 4], [[6, 4], [1, 2], [-1, 1], [0, 1]], [24, 6, 1, 2])[0], 21)
assert ok(lp([7, 9], [[-3, -6], [-8, -4]], [-18, -16], "min")[0], 86 / 3)
assert ok(lp([2, 4], [[1, 2], [1, 1]], [5, 4])[0], 10)
assert ok(lp([2, 1], [[-3, -1], [-4, -3], [1, 2]], [-3, -6, 3], "min")[0], 2.4)
# Optimization Techniques: transportation
cost = np.array([[3, 1, 7, 4], [2, 6, 5, 9], [8, 3, 3, 2]]); sup = [300, 400, 500]; dem = [250, 350, 400, 200]
Aeq = []; beq = []
for i in range(3):
    row = np.zeros((3, 4)); row[i] = 1; Aeq.append(row.ravel()); beq.append(sup[i])
for j in range(4):
    col = np.zeros((3, 4)); col[:, j] = 1; Aeq.append(col.ravel()); beq.append(dem[j])
assert ok(linprog(cost.ravel(), A_eq=Aeq, b_eq=beq, method="highs").fun, 2850)
# assignment
def assign(C, maximize=False):
    C = np.array(C); r, c = linear_sum_assignment(C, maximize=maximize); return C[r, c].sum()
assert assign([[10, 12, 19, 11], [5, 10, 7, 8], [12, 14, 13, 11], [8, 15, 11, 9]]) == 38
assert assign([[3, 5, 4], [5, 3, 2], [4, 4, 5]]) == 9 and assign([[1, 4, 6], [9, 7, 10], [4, 5, 11]]) == 16
assert assign([[40, 52, 49], [32, 46, 58], [56, 54, 47]], True) == 166
# sequencing: best makespan over all orders
def makespan(order, T):
    done = [0] * len(T[order[0]])
    for j in order:
        for k, t in enumerate(T[j]):
            done[k] = max(done[k], done[k - 1] if k else 0) + t
    return done[-1]
best = lambda T: min(makespan(o, T) for o in permutations(T))
T = dict(A=(5, 2), B=(1, 6), C=(9, 7), D=(3, 8), E=(10, 4)); assert makespan("BDCEA", T) == best(T) == 30
T = {1: (4, 5), 2: (9, 6), 3: (8, 2), 4: (6, 3)}; assert makespan((1, 2, 4, 3), T) == best(T) == 29
T = dict(A=(8, 5, 4), B=(10, 6, 9), C=(6, 2, 8), D=(7, 3, 6)); assert makespan("CBAD", T) == makespan("CBDA", T) == best(T) == 41
T = dict(A=(7, 3, 2, 6), B=(9, 2, 4, 9), C=(8, 4, 3, 5), D=(10, 1, 3, 8))
assert makespan("BDCA", T) == makespan("BCDA", T) == makespan("DBCA", T) == best(T) == 45
# games: value by linear programming
def value(M):
    M = np.array(M, float); m, n = M.shape
    r = linprog(np.r_[np.zeros(m), -1], A_ub=np.c_[-M.T, np.ones(n)], b_ub=np.zeros(n),
                A_eq=[np.r_[np.ones(m), 0]], b_eq=[1], bounds=[(0, None)] * m + [(None, None)], method="highs")
    return -r.fun
assert ok(value([[5, 1], [3, 4]]), 3.4) and ok(value([[2, 4], [6, 3]]), 3.6) and ok(value([[3, 2, 4], [-1, 4, 2], [2, 2, 6]]), 7 / 3)
assert ok(value([[2, 1, 0, -2], [1, 0, 3, 2]]), .4) and ok(value([[2, 4], [2, 3], [3, 2], [-2, 6]]), 8 / 3)
assert ok(value([[3, 2, 4, 0], [3, 4, 2, 4], [4, 2, 4, 0], [0, 4, 0, 8]]), 8 / 3)
assert ok(value([[-2, 15, -2], [-5, -6, -4], [-5, 20, -8]]), -2) and ok(value([[8, 6, 2, 8], [8, 9, 4, 5], [7, 5, 3, 5]]), 4)
print("operations-research, optimization-techniques: all recomputed answers agree")
