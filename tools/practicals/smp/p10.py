# Practical 10 -- correlation and BOTH regression lines
import math

# Step 1: Enter the data; the sums of squares and products
x = [65, 63, 67, 64, 68, 62, 70, 66, 68, 67]
y = [68, 66, 68, 65, 69, 66, 68, 65, 71, 67]
n = len(x)

xb, yb = sum(x) / n, sum(y) / n
Sxx = sum((v - xb) ** 2 for v in x)
Syy = sum((v - yb) ** 2 for v in y)
Sxy = sum((u - xb) * (v - yb) for u, v in zip(x, y))
print(f"n = {n}   xbar = {xb:.4f}   ybar = {yb:.4f}")
print(f"Sxx = {Sxx:.4f}   Syy = {Syy:.4f}   Sxy = {Sxy:.4f}")

# Step 2: The correlation
r = Sxy / math.sqrt(Sxx * Syy)
print(f"r = {r:.6f}   r^2 = {r*r:.6f}")

# Step 3: Both regression lines, and the checks
b_yx = Sxy / Sxx
a_yx = yb - b_yx * xb
b_xy = Sxy / Syy
a_xy = xb - b_xy * yb
print(f"y on x :  y = {a_yx:.6f} + {b_yx:.6f} x")
print(f"x on y :  x = {a_xy:.6f} + {b_xy:.6f} y")
print(f"check   :  b_yx * b_xy = {b_yx*b_xy:.6f}  and  r^2 = {r*r:.6f}")
print(f"the two lines meet at the point (xbar, ybar) = ({xb:.4f}, {yb:.4f})")
print(f"  y on x at xbar : {a_yx + b_yx*xb:.4f}")
print(f"  x on y at ybar : {a_xy + b_xy*yb:.4f}")

# Step 4: The angle between the lines
# the angle between the two lines, which is zero only when |r| = 1
m1, m2 = b_yx, 1 / b_xy
theta = math.degrees(math.atan(abs((m2 - m1) / (1 + m1 * m2))))
print(f"angle between the lines = {theta:.4f} degrees "
      f"(it would be 0 if r were +-1, and 90 if r were 0)")

# Step 5: The residual sd and a prediction
# residual standard deviation and the prediction at a new x
see = math.sqrt((Syy - b_yx * Sxy) / (n - 2))
print(f"residual sd (n-2 divisor) = {see:.6f}")
print(f"predicted y at x = 69 : {a_yx + b_yx*69:.6f}")
