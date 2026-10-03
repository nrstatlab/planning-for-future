# Stage 3 -- REGULAR EXPRESSIONS: search, findall, split, sub, and the two
# traps that cost marks.
import re

# Step 1: The log to be searched
LOG = """\
2026-01-14 09:12:03 INFO  order=A-1043 customer=asha@example.com total=1240.50
2026-01-14 09:15:47 WARN  order=A-1044 customer=biju@example.in  total=99.00
2026-01-15 11:02:19 ERROR order=B-2210 customer=chitra@mail.org  total=15750.75
2026-01-15 11:40:00 INFO  order=B-2211 customer=devan@example.com total=310.25
"""

# Step 2: search: the first match, with its position
m = re.search(r"ERROR", LOG)
print("search  ->", m.group(), "at", m.start())

# Step 3: findall: every match; with ONE group it returns the group, not the match
print("findall ->", re.findall(r"order=([A-Z]-\d+)", LOG))

# Step 4: Groups, named groups, and finditer for structured extraction
PAT = re.compile(r"""
    (?P<date>\d{4}-\d{2}-\d{2})\s+          # date
    (?P<time>\d{2}:\d{2}:\d{2})\s+          # time
    (?P<level>[A-Z]+)\s+                    # level
    order=(?P<order>[A-Z]-\d+)\s+
    customer=(?P<email>\S+@\S+?)\s+
    total=(?P<total>\d+\.\d{2})
""", re.VERBOSE)

print()
print("finditer with named groups:")
rows = [m.groupdict() for m in PAT.finditer(LOG)]
for r in rows:
    print("  ", r["date"], r["level"], r["order"], r["email"], r["total"])
print("records parsed:", len(rows))

# Step 5: Split on a pattern, not a fixed string
print()
print("split on any run of whitespace:", re.split(r"\s+", "a  b\tc\nd"))
print("split keeping the separator   :", re.split(r"([;,])", "a,b;c"))

# Step 6: sub, with a backreference and with a function
print()
print("sub, backreference:",
      re.sub(r"(\w+)@(\w+)\.(\w+)", r"\1@***.\3", "asha@example.com"))
print("sub, function     :",
      re.sub(r"\d+\.\d{2}", lambda m: f"{float(m.group())*1.18:.2f}",
             "total=1240.50 and total=99.00"))
print("sub, count limited:", re.sub(r"a", "A", "banana", count=2))

# Step 7: Trap 1: greedy versus lazy
html = '<td>Vizag</td><td>Kochi</td>'
print()
print("greedy .+ :", re.findall(r"<td>(.+)</td>", html))
print("lazy   .+?:", re.findall(r"<td>(.+?)</td>", html))
print("the greedy form runs to the LAST </td> and returns one wrong answer;")
print("it is not an error, which is what makes it dangerous.")

# Step 8: Trap 2: a plausible pattern that is wrong
print()
bad = r"\d+\.\d+"
good = r"\d+\.\d{2}\b"
text = "total=1240.50 version=3.14159 total=99.00"
print("pattern", bad, "->", re.findall(bad, text))
print("pattern", good, "->", re.findall(good, text))
print("the first matches a version number as if it were money.  Anchor the")
print("pattern to what you mean -- two decimal places and a word boundary.")

# Step 9: Compile once when the pattern is reused
print()
print("re.compile returns a pattern object; compiling inside a loop over a")
print("million rows is the commonest avoidable cost in an extract script.")
