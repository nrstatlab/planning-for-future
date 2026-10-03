# Practical 4 -- median and mode of an array, written out
# Step 1: Median: sort, then take the middle
def median(a):
    s = sorted(a)
    n = len(s)
    mid = n // 2
    if n % 2:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2

# Step 2: Mode: count, then keep every value at the top count
def mode(a):
    freq = {}
    for v in a:
        freq[v] = freq.get(v, 0) + 1
    top = max(freq.values())
    modes = sorted(k for k, c in freq.items() if c == top)
    return modes, top, freq

# Step 3: Enter the test arrays
odd = [7, 3, 9, 3, 5, 8, 3, 9, 4]
even = [12, 4, 9, 4, 15, 7]
bimodal = [2, 5, 2, 7, 5, 9]

# Step 4: Medians for odd and even n
print("odd  n =", len(odd), " median =", median(odd))
print("even n =", len(even), " median =", median(even))
# Step 5: Modes: one, two and none
m, c, f = mode(odd)
print("odd  mode(s) =", m, "occurring", c, "times; frequencies", dict(sorted(f.items())))
m, c, f = mode(bimodal)
print("bimodal mode(s) =", m, "occurring", c, "times -- two modes, so the mode is not unique")
allsame = [4, 6, 9, 11]
m, c, _ = mode(allsame)
print("no repeats:", m, "each", c, "time -- the mode is undefined for this data, not 'all of them'")
