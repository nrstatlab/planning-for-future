"""Course 4 Lab, experiments 3-6: measures of central tendency and dispersion,
histograms and bar charts.

Standard library only -- `statistics` is part of Python, no install needed.
Charts are drawn as text so they render anywhere.
"""

import statistics
from collections import Counter

marks = [45, 67, 78, 52, 89, 91, 73, 64, 58, 82,
         76, 69, 71, 85, 60, 55, 93, 48, 79, 66]

print("=" * 62)
print("EXPERIMENT 3: Measures of central tendency")
print("=" * 62)
print(f"Dataset (n = {len(marks)}): {sorted(marks)}\n")

n = len(marks)
mean = sum(marks) / n
ordered = sorted(marks)
if n % 2 == 0:
    median = (ordered[n // 2 - 1] + ordered[n // 2]) / 2
else:
    median = ordered[n // 2]

counts = Counter(marks)
top = max(counts.values())
modes = [v for v, c in counts.items() if c == top]

print("MEAN -- the balance point. Add everything, divide by how many.")
print(f"  mean = {sum(marks)} / {n} = {mean:.2f}")
print(f"  cross-check statistics.mean() = {statistics.mean(marks):.2f}")

print("\nMEDIAN -- the middle value once sorted. Half are below, half above.")
print(f"  n = {n} is even, so average the {n//2}th and {n//2+1}th values:")
print(f"  ({ordered[n//2-1]} + {ordered[n//2]}) / 2 = {median}")
print(f"  cross-check statistics.median() = {statistics.median(marks)}")

print("\nMODE -- the most frequent value.")
if top == 1:
    print("  every value appears once, so there is no mode")
else:
    print(f"  {modes} (appearing {top} times)")

print("\nWHICH ONE TO USE")
print("  The mean uses every value, so one extreme value drags it. Add a")
print("  single mark of 500 to this dataset:")
skewed = marks + [500]
print(f"    mean   {mean:.2f} -> {sum(skewed)/len(skewed):.2f}   moved a lot")
print(f"    median {median} -> {statistics.median(skewed)}   barely moved")
print("  That resistance is why income and house prices are quoted as medians.")

print("\n" + "=" * 62)
print("EXPERIMENT 4: Measures of dispersion")
print("=" * 62)

data_range = max(marks) - min(marks)


def quartile(sorted_data, q):
    """Linear-interpolation quartile, matching Excel's QUARTILE.INC."""
    pos = (len(sorted_data) - 1) * q
    lower = int(pos)
    upper = min(lower + 1, len(sorted_data) - 1)
    return sorted_data[lower] + (pos - lower) * (sorted_data[upper] - sorted_data[lower])


q1, q2, q3 = quartile(ordered, 0.25), quartile(ordered, 0.5), quartile(ordered, 0.75)
iqr = q3 - q1

# Population vs sample: the divisor is n for a population, n-1 for a sample.
pop_var = sum((x - mean) ** 2 for x in marks) / n
sam_var = sum((x - mean) ** 2 for x in marks) / (n - 1)

print(f"RANGE = max - min = {max(marks)} - {min(marks)} = {data_range}")
print("  Uses only two values, so a single outlier defines it entirely.")

print(f"\nQUARTILES and IQR")
print(f"  Q1 = {q1:.2f}   Q2 (median) = {q2:.2f}   Q3 = {q3:.2f}")
print(f"  IQR = Q3 - Q1 = {q3:.2f} - {q1:.2f} = {iqr:.2f}")
print("  The IQR is the spread of the middle 50%, so outliers cannot inflate it.")

print(f"\nVARIANCE -- the mean squared distance from the mean")
print(f"  population variance (divide by n)     = {pop_var:.2f}")
print(f"  sample variance     (divide by n - 1) = {sam_var:.2f}")
print("  Use n-1 when the data is a SAMPLE. Dividing by n underestimates the")
print("  spread, because deviations are measured from the sample's own mean.")
print("  This is Bessel's correction, and choosing wrongly costs marks.")
print(f"  cross-check statistics.pvariance() = {statistics.pvariance(marks):.2f}")
print(f"  cross-check statistics.variance()  = {statistics.variance(marks):.2f}")

print(f"\nSTANDARD DEVIATION -- the square root of the variance")
print(f"  population sd = {pop_var ** 0.5:.2f}")
print(f"  sample sd     = {sam_var ** 0.5:.2f}")
print("  Back in the original units (marks), unlike variance (marks squared).")

print(f"\nCOEFFICIENT OF VARIATION -- relative spread, unit-free")
print(f"  CV = sd / mean x 100 = {sam_var ** 0.5 / mean * 100:.2f}%")

print("\nOUTLIER RULE: anything below Q1 - 1.5xIQR or above Q3 + 1.5xIQR")
low_fence, high_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"  fences: [{low_fence:.2f}, {high_fence:.2f}]")
outliers = [x for x in marks if x < low_fence or x > high_fence]
print(f"  outliers: {outliers if outliers else 'none'}")

print("\n" + "=" * 62)
print("EXPERIMENT 5: Histogram and the shape of the distribution")
print("=" * 62)

bins = [(40, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100)]
print(f"\n{'Class':<12}{'Frequency':<12}Histogram")
for low, high in bins:
    freq = sum(1 for m in marks if low <= m < high)
    print(f"{low}-{high:<8} {freq:<12}{'#' * freq * 3}")

# Pearson's second coefficient of skewness.
skew = 3 * (mean - median) / (sam_var ** 0.5)
print(f"\nSHAPE")
print(f"  mean = {mean:.2f}, median = {median}")
print(f"  Pearson skewness = 3(mean - median)/sd = {skew:.3f}")
if abs(skew) < 0.5:
    shape = "roughly symmetric"
elif skew > 0:
    shape = "positively skewed -- a tail to the right"
else:
    shape = "negatively skewed -- a tail to the left"
print(f"  The distribution is {shape}.")
print("  Rule of thumb: mean > median suggests a right tail; mean < median a")
print("  left tail; mean = median = mode means perfectly symmetric.")

print("\n" + "=" * 62)
print("EXPERIMENT 6: Bar chart of categorical data")
print("=" * 62)

survey = [("Male", "A"), ("Female", "A"), ("Male", "B"), ("Female", "B"),
          ("Male", "A"), ("Female", "C"), ("Male", "C"), ("Female", "A"),
          ("Male", "B"), ("Female", "B"), ("Male", "A"), ("Female", "A"),
          ("Male", "C"), ("Female", "B"), ("Male", "B")]

sections = sorted({s for _, s in survey})
genders = sorted({g for g, _ in survey})

print(f"\n{'Section':<10}" + "".join(f"{g:>10}" for g in genders) + f"{'Total':>10}")
print("-" * 40)
for section in sections:
    row = [sum(1 for g, s in survey if s == section and g == gender)
           for gender in genders]
    print(f"{section:<10}" + "".join(f"{v:>10}" for v in row) + f"{sum(row):>10}")

print("\nGrouped bar chart")
for section in sections:
    for gender in genders:
        count = sum(1 for g, s in survey if s == section and g == gender)
        print(f"  {section}-{gender:<8} {'|' * count * 4} {count}")

print("\nINTERPRETATION")
print("  A bar chart is for CATEGORIES -- the bars are separated, and their")
print("  order carries no meaning. A histogram is for CONTINUOUS data -- the")
print("  bars touch, because the classes are adjacent intervals. Drawing one")
print("  when the question asks for the other is a common way to lose marks.")
