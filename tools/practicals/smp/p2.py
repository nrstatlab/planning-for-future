# Practical 2 -- determinant by cofactor expansion and inverse by the adjoint
from fractions import Fraction

# Step 1: Delete a row and a column
def minor(M, i, j):
    return [[M[r][c] for c in range(len(M)) if c != j]
            for r in range(len(M)) if r != i]

# Step 2: Expand the determinant along row 1
def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    return sum((-1) ** j * M[0][j] * det(minor(M, 0, j)) for j in range(n))

# Step 3: Invert by the transposed cofactors
def inverse(M):
    d = det(M)
    if d == 0:
        raise ValueError("matrix is singular -- no inverse")
    n = len(M)
    cof = [[(-1) ** (i + j) * det(minor(M, i, j)) for j in range(n)] for i in range(n)]
    # the adjoint is the TRANSPOSE of the cofactor matrix
    return [[Fraction(cof[j][i], d) for j in range(n)] for i in range(n)]

# Step 4: Print a matrix of fractions
def show(name, M):
    print(name)
    for row in M:
        print("  " + "  ".join(f"{str(v):>8}" for v in row))

# Step 5: Find det(A) and the inverse
A = [[2, 1, 1], [1, 3, 2], [1, 0, 4]]
print("det(A) =", det(A))
Ainv = inverse(A)
show("A inverse", Ainv)

# Step 6: Check that A times its inverse is I
# check: A times its inverse must be the identity, exactly
prod = [[sum(Fraction(A[i][k]) * Ainv[k][j] for k in range(3)) for j in range(3)]
        for i in range(3)]
show("A x A inverse", prod)

# Step 7: Try a singular matrix
S = [[1, 2, 3], [2, 4, 6], [1, 0, 1]]
print("det(S) =", det(S), "-- row 2 is twice row 1, so S is singular")
