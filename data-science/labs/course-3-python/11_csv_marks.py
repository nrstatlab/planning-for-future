"""Experiment 11: Read and process student marks from a CSV file, calculating
the average, highest and lowest.

Syllabus: Course 3, Unit 4 -- CSV files.
Uses the standard-library csv module (no pandas needed).
"""

import csv

FILENAME = "marks.csv"

rows = [
    ["roll", "name", "maths", "statistics", "python"],
    ["24001", "Ananya", "85", "78", "92"],
    ["24002", "Bhavana", "72", "88", "65"],
    ["24003", "Charan", "91", "95", "89"],
    ["24004", "Divya", "64", "70", "75"],
    ["24005", "Eshwar", "78", "62", "81"],
]

with open(FILENAME, "w", newline="") as fh:
    csv.writer(fh).writerows(rows)

# DictReader gives each row as a dictionary keyed by the header row.
students = []
with open(FILENAME, "r", newline="") as fh:
    for row in csv.DictReader(fh):
        subjects = {k: int(v) for k, v in row.items()
                    if k not in ("roll", "name")}
        total = sum(subjects.values())
        students.append({
            "roll": row["roll"],
            "name": row["name"],
            "subjects": subjects,
            "total": total,
            "average": total / len(subjects),
        })

print(f"{'Roll':<8}{'Name':<12}{'Maths':>7}{'Stats':>7}{'Python':>8}"
      f"{'Total':>7}{'Avg':>8}")
print("-" * 57)
for s in students:
    m, st, p = s["subjects"]["maths"], s["subjects"]["statistics"], s["subjects"]["python"]
    print(f"{s['roll']:<8}{s['name']:<12}{m:>7}{st:>7}{p:>8}"
          f"{s['total']:>7}{s['average']:>8.2f}")

print("\nCLASS SUMMARY")
averages = [s["average"] for s in students]
print(f"  Class average : {sum(averages) / len(averages):.2f}")

best = max(students, key=lambda s: s["total"])
worst = min(students, key=lambda s: s["total"])
print(f"  Highest total : {best['name']} with {best['total']}")
print(f"  Lowest total  : {worst['name']} with {worst['total']}")

print("\nPER-SUBJECT")
for subject in ("maths", "statistics", "python"):
    scores = [s["subjects"][subject] for s in students]
    print(f"  {subject:<12} avg {sum(scores) / len(scores):6.2f}   "
          f"high {max(scores):3d}   low {min(scores):3d}")
