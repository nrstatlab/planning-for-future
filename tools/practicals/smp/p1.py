# Practical 1 -- sum and product of two matrices, no packages
# Step 1: Check the shapes
def shape(M):
    return len(M), len(M[0])

# Step 2: Add elementwise
def add(A, B):
    if shape(A) != shape(B):
        raise ValueError("addition needs matrices of the same shape")
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

# Step 3: Multiply by inner products
def multiply(A, B):
    ra, ca = shape(A)
    rb, cb = shape(B)
    if ca != rb:
        raise ValueError("columns of A must equal rows of B")
    return [[sum(A[i][k] * B[k][j] for k in range(ca)) for j in range(cb)]
            for i in range(ra)]

# Step 4: Print a matrix
def show(name, M):
    print(name)
    for row in M:
        print("  " + "  ".join(f"{v:6.2f}" for v in row))

# Step 5: Enter the two matrices
A = [[2, 1, 1], [1, 3, 2], [1, 0, 4]]
B = [[1, 0, 2], [2, 1, 0], [0, 3, 1]]

# Step 6: Form A + B, AB and BA, and compare AB with BA
show("A + B", add(A, B))
show("A x B", multiply(A, B))
show("B x A", multiply(B, A))
print("A x B equals B x A?", multiply(A, B) == multiply(B, A))
