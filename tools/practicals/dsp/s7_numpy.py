# Stage 6a -- NumPy: build, reshape, slice, index, and aggregate.
# The teaching is in Python for Data Analysis, Unit 1; what is shown here is
# the part that bites in a pipeline -- views against copies, and axis=.
import numpy as np
np.set_printoptions(legacy="1.25")          # stable printing across versions

# Step 1: Arrays from different sources
a = np.array([40, 57, 37, 69, 36, 38])                       # from a list
b = np.arange(12).reshape(3, 4)                              # from a range
c = np.zeros((2, 3), dtype=np.int32)                         # filled
d = np.linspace(0, 1, 5)                                     # evenly spaced
print("a", a.shape, a.dtype, a)
print("b", b.shape, b.dtype, "\n", b)
print("c", c.shape, c.dtype, " d", np.round(d, 2))

# Step 2: dtype is fixed, and silently truncates
print()
i = np.array([1, 2, 3], dtype=np.int32)
i[0] = 3.9
print("int32 array assigned 3.9 ->", i, "  -- truncated, not rounded, no warning")
print("mixing types promotes:", (np.array([1, 2]) + np.array([0.5, 0.5])).dtype)

# Step 3: Reshape, transpose, ravel
print()
print("b.T\n", b.T)
print("b.ravel()", b.ravel())
print("b.reshape(2, -1)\n", b.reshape(2, -1), "  -- -1 means 'work it out'")

# Step 4: Slicing returns a VIEW; fancy indexing returns a COPY
print()
v = b[0, :]          # basic slice -> view
v[0] = 99
print("after writing through a slice, b[0,0] =", b[0, 0], " -- the original changed")
f = b[[0, 2], :]     # fancy index -> copy
f[0, 0] = -1
print("after writing through a fancy index, b[0,0] =", b[0, 0],
      " -- still 99, not -1: the fancy index wrote to a copy")
print("this single distinction accounts for most NumPy bugs.  Use .copy() when")
print("you mean a copy and mean it on purpose.")

# Step 5: Boolean indexing and where
print()
print("a > 40      ->", a > 40)
print("a[a > 40]   ->", a[a > 40])
print("np.where    ->", np.where(a > 40, "high", "low"))
print("a[a > 40] = 0 assigns in place:", end=" ")
a2 = a.copy(); a2[a2 > 40] = 0; print(a2)

# Step 6: Arithmetic, broadcasting, aggregation along an axis
print()
m = np.array([[40, 57, 37], [69, 36, 38]], dtype=float)
print("m\n", m)
print("m * 2 + 1\n", m * 2 + 1)
print("m - m.mean(axis=0)   (column means removed)\n",
      np.round(m - m.mean(axis=0), 4))
print("m.sum()", m.sum(), " m.sum(axis=0)", m.sum(axis=0),
      " m.sum(axis=1)", m.sum(axis=1))
print("axis=0 collapses the ROWS and leaves one value per column;")
print("axis=1 collapses the columns.  Reading it the other way round is the")
print("commonest NumPy slip, and it usually still returns a number.")
print()
print("mean", round(float(m.mean()), 6), " std (population, ddof=0)",
      round(float(m.std()), 6), " std (sample, ddof=1)",
      round(float(m.std(ddof=1)), 6))
print("NumPy defaults to ddof=0 and pandas to ddof=1 -- they disagree by")
print("design, so state which you used.")
