# Practical 5 -- frequency table, then mean, median, mode, variance, SD
# both from the raw values and from the grouped table, so the grouping error shows
import math

# Step 1: Enter the raw data
raw = [23, 45, 12, 37, 52, 28, 41, 19, 33, 47,
       55, 26, 38, 44, 31, 17, 49, 35, 22, 40,
       29, 51, 36, 43, 25, 48, 32, 39, 27, 46,
       34, 21, 42, 30, 53, 24, 37, 45, 33, 41]

# Step 2: Count the classes
def freq_table(values, low, width, k):
    edges = [low + i * width for i in range(k + 1)]
    counts = [0] * k
    for v in values:
        idx = int((v - low) // width)
        if idx == k:            # the top edge belongs to the last class
            idx = k - 1
        counts[idx] += 1
    return edges, counts

# Step 3: Grouped mean
def grouped_mean(edges, counts):
    mids = [(edges[i] + edges[i + 1]) / 2 for i in range(len(counts))]
    n = sum(counts)
    return sum(m * f for m, f in zip(mids, counts)) / n, mids, n

# Step 4: Grouped median
def grouped_median(edges, counts):
    n = sum(counts)
    cum = 0
    for i, f in enumerate(counts):
        if cum + f >= n / 2:
            L = edges[i]
            h = edges[i + 1] - edges[i]
            return L + (n / 2 - cum) / f * h
        cum += f

# Step 5: Grouped mode
def grouped_mode(edges, counts):
    i = counts.index(max(counts))
    f1 = counts[i]
    f0 = counts[i - 1] if i > 0 else 0
    f2 = counts[i + 1] if i + 1 < len(counts) else 0
    L = edges[i]
    h = edges[i + 1] - edges[i]
    return L + (f1 - f0) / (2 * f1 - f0 - f2) * h

# Step 6: Print the table and the grouped summaries
edges, counts = freq_table(raw, 10, 10, 5)
print("class        frequency")
for i, f in enumerate(counts):
    print(f"  {edges[i]:2d} - {edges[i+1]:2d}      {f:2d}")
print("  total        ", sum(counts))

gm, mids, n = grouped_mean(edges, counts)
gmed = grouped_median(edges, counts)
gmode = grouped_mode(edges, counts)
gvar = sum(f * (m - gm) ** 2 for m, f in zip(mids, counts)) / n
print(f"grouped:  mean {gm:.4f}  median {gmed:.4f}  mode {gmode:.4f} "
      f" variance {gvar:.4f}  sd {math.sqrt(gvar):.4f}")

# Step 7: The same summaries from the raw values
rm = sum(raw) / len(raw)
s = sorted(raw)
rmed = (s[19] + s[20]) / 2
rvar = sum((v - rm) ** 2 for v in raw) / len(raw)
print(f"raw:      mean {rm:.4f}  median {rmed:.4f} "
      f"                variance {rvar:.4f}  sd {math.sqrt(rvar):.4f}")
print(f"grouping error in the mean: {gm - rm:+.4f}")

# Step 8: The tied modal class
# the two middle classes tie at 12, so the modal class is not unique --
# apply the formula to the SECOND of them and see what happens
i = 3
f1, f0, f2 = counts[i], counts[i-1], counts[i+1]
alt = edges[i] + (f1 - f0) / (2*f1 - f0 - f2) * 10
print(f"mode from the other tied class: {alt:.4f} -- the same boundary, 40")
