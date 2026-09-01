# Course 1 — Practice Questions with Solutions

---

## Section A — Number system conversions

Every answer below is checked by
`labs/course-1-office/unit1_number_systems.py`, which fails if any conversion
on this page is wrong.

### Q1 — Convert (11010110)₂ to decimal, octal and hexadecimal

**Decimal:** 128 + 64 + 0 + 16 + 0 + 4 + 2 + 0 = **214**

**Octal** — group in threes from the right: `011 | 010 | 110` → 3, 2, 6 →
**(326)₈**

**Hexadecimal** — group in fours from the right: `1101 | 0110` → D, 6 →
**(D6)₁₆**

*Check:* 13 × 16 + 6 = 208 + 6 = 214 ✓

### Q2 — Convert (2024)₁₀ to binary, octal and hexadecimal

**Binary** — divide by 2 repeatedly:
2024→1012 r0, 1012→506 r0, 506→253 r0, 253→126 r**1**, 126→63 r0, 63→31 r**1**,
31→15 r**1**, 15→7 r**1**, 7→3 r**1**, 3→1 r**1**, 1→0 r**1**

Reading upwards: **(11111101000)₂**

**Hexadecimal** — group the binary in fours: `0111 | 1110 | 1000` → 7, E, 8 →
**(7E8)₁₆**

*Check:* 7 × 256 + 14 × 16 + 8 = 1792 + 224 + 8 = 2024 ✓

**Octal** — group in threes: `011 | 111 | 101 | 000` → 3, 7, 5, 0 →
**(3750)₈**

*Check:* 3 × 512 + 7 × 64 + 5 × 8 + 0 = 1536 + 448 + 40 = 2024 ✓

### Q3 — Convert (A7C)₁₆ to decimal, binary and octal

**Decimal:** A(10) × 256 + 7 × 16 + C(12) × 1 = 2560 + 112 + 12 = **2684**

**Binary:** A → `1010`, 7 → `0111`, C → `1100` → **(101001111100)₂**

**Octal** — regroup the binary in threes: `101 | 001 | 111 | 100` → 5, 1, 7, 4
→ **(5174)₈**

*Check:* 5 × 512 + 1 × 64 + 7 × 8 + 4 = 2560 + 64 + 56 + 4 = 2684 ✓

### Q4 — Convert (0.6875)₁₀ to binary

Multiply by 2 and read the integer parts **downwards**:

| Step | Result | Integer |
|---|---|---|
| 0.6875 × 2 | 1.375 | **1** |
| 0.375 × 2 | 0.75 | **0** |
| 0.75 × 2 | 1.5 | **1** |
| 0.5 × 2 | 1.0 | **1** |

**(0.1011)₂**

*Check:* 0.5 + 0 + 0.125 + 0.0625 = 0.6875 ✓

### Q5 — Perform (110110)₂ − (10111)₂

```
   110110      (54)
 - 010111      (23)
 --------
   011111      (31)
```

*Check:* 54 − 23 = 31, and 011111 = 16 + 8 + 4 + 2 + 1 = 31 ✓

### Q6 — Find the 1's and 2's complement of (01101001)₂ in 8 bits

The number is 64 + 32 + 8 + 1 = **105**.

**1's complement** — flip every bit: **10010110**

**2's complement** — add 1 to that: **10010111**

*Check:* `01101001 + 10010111 = 100000000`; the ninth bit overflows out of 8
bits, leaving `00000000` ✓

---

## Section B — Short answers

**Q7. Why do computers use binary rather than decimal?**

A transistor has two stable states — conducting or not — so two symbols map
directly onto the hardware. A decimal system would need ten distinguishable
voltage levels, which is far harder to build reliably and far more susceptible
to noise. Binary also makes arithmetic circuits simple, since Boolean algebra
maps directly onto logic gates.

**Q8. Distinguish the ALU from the CU.**

The **ALU** performs the actual arithmetic (+, −, ×, ÷) and logical (AND, OR,
NOT, comparison) operations. The **CU** performs no computation at all — it
fetches instructions, decodes them, and generates the control signals that tell
every other unit what to do and when. Together with registers they make up the
CPU.

**Q9. Why is 2's complement preferred over sign–magnitude?**

Three reasons: subtraction becomes addition, so one circuit does both; there is
only one representation of zero (sign–magnitude has +0 and −0); and the range is
slightly wider — 8 bits give −128 to +127 rather than −127 to +127.

**Q10. Distinguish a hub from a switch.**

A **hub** operates at the physical layer and broadcasts every incoming frame to
every port, so bandwidth is shared and collisions occur. A **switch** operates at
the data link layer, learns which MAC address is on which port, and forwards the
frame only to the correct port — giving each connection full bandwidth and no
collisions.

**Q11. Why does a "500 GB" hard disk show as about 465 GB?**

The manufacturer uses decimal units: 500 GB = 500,000,000,000 bytes. The
operating system divides by 1024 three times, giving 500 × 10⁹ / 1024³ ≈ 465.
Nothing is missing; the two are counting in different bases.

**Q12. Differentiate a transition from an animation.**

A **transition** is the effect when moving from one slide to the next
(Transitions tab). An **animation** is the effect applied to an object *within* a
slide — text flying in, a chart building (Animations tab).

---

## Section C — Spreadsheet problems

### Q13 — Write a formula to assign grades

Marks are in column B. Assign A ≥ 90, B ≥ 75, C ≥ 60, D ≥ 40, otherwise F.

```excel
=IF(B2>=90,"A", IF(B2>=75,"B", IF(B2>=60,"C", IF(B2>=40,"D","F"))))
```

**Order matters** — the highest threshold must be tested first. Reversing the
ladder gives every passing student a D, because `>=40` is true for all of them
and the first true condition wins.

Excel 2019+ alternative:
```excel
=IFS(B2>=90,"A", B2>=75,"B", B2>=60,"C", B2>=40,"D", TRUE,"F")
```

### Q14 — Look up an employee's salary by ID

IDs in A2:A100, names in B, departments in C, salaries in D. The ID to look up
is in F2.

```excel
=VLOOKUP(F2, $A$2:$D$100, 4, FALSE)
```

- `$A$2:$D$100` — anchored, so copying the formula down does not shift the table
- `4` — the fourth column **of the table array**, which is column D
- `FALSE` — exact match; omitting it defaults to approximate and gives silently
  wrong answers

Wrapped against a missing ID:
```excel
=IFERROR(VLOOKUP(F2,$A$2:$D$100,4,FALSE), "Employee not found")
```

The modern equivalent, which can look leftwards and needs no IFERROR:
```excel
=XLOOKUP(F2, $A$2:$A$100, $D$2:$D$100, "Employee not found")
```

### Q15 — Split a full name into first and last name

Full name in A2, e.g. `Ananya Sharma`.

```excel
First name:  =LEFT(A2, FIND(" ",A2)-1)
Last name:   =RIGHT(A2, LEN(A2)-FIND(" ",A2))
```

`FIND(" ",A2)` returns 7 for `Ananya Sharma`. So `LEFT(A2,6)` gives `Ananya`,
and `RIGHT(A2, 13-7)` = `RIGHT(A2,6)` gives `Sharma`.

**Wrap it in IFERROR** for names with no space, or `FIND` returns `#VALUE!`.

### Q16 — Count and total conditionally

| Task | Formula |
|---|---|
| How many scored above 75 | `=COUNTIF(B2:B50, ">75")` |
| How many in IT scoring above 75 | `=COUNTIFS(A2:A50,"IT", B2:B50,">75")` |
| Total salary of the IT department | `=SUMIF(A2:A50, "IT", C2:C50)` |
| Average salary in IT | `=AVERAGEIF(A2:A50, "IT", C2:C50)` |

Note the argument order: `SUMIF(range, criteria, sum_range)` but
`SUMIFS(sum_range, range1, criteria1, …)`.

### Q17 — Highlight an entire row where marks are below 40

1. Select the full data range, `A2:F50`
2. Conditional Formatting → New Rule → *Use a formula to determine which cells
   to format*
3. Enter `=$C2<40`
4. Choose a red fill

**The reference must be `$C2`.** The `$` locks the column so every cell in the
row is tested against column C, while the relative row number lets each row test
its own value. `$C$2` would test every row against one cell; `C2` would test
each cell against the column beside it.

### Q18 — Using Goal Seek

A budget sheet computes savings in B10 from income (B2) and expenses. Savings
currently show ₹4,000; you want ₹12,000.

**Data → What-If Analysis → Goal Seek:**

| Field | Value |
|---|---|
| Set cell | `B10` (the savings formula) |
| To value | `12000` |
| By changing cell | `B2` (income) |

Goal Seek adjusts income until savings reach 12,000 and reports the value
required.

**The changing cell must contain a value, not a formula** — Goal Seek can only
adjust an input, not a calculated result.

---

## Section D — Long answers

### Q19 — Explain the generations of computers

Give a table with generation, years, technology, languages and examples, then a
paragraph on each generation's characteristics, then the overall trend —
smaller, faster, cheaper, more reliable, lower power.

Full treatment in [unit-1.md §1.4](unit-1.md).

### Q20 — Explain the network topologies

Draw bus, star and ring. For each give the structure, advantages and
disadvantages. Then state which is dominant today and why — star, because every
switched Ethernet network is physically a star, and a single node failing does
not affect the rest.

Add the mesh cable-count formula, **n(n−1)/2**, if the question mentions mesh.

### Q21 — Explain pivot tables and dashboards

Cover the four areas (Rows, Columns, Values, Filters), creation, value settings,
grouping and refreshing. Then explain slicers and Report Connections — one
slicer driving several pivot tables is what makes a dashboard interactive
rather than a set of static charts.

Finish with the layout and design principles from [unit-5.md §5.6](unit-5.md).

---

## Quick self-test

1. Convert (1010)₂ to decimal and (10)₁₀ to binary.
2. How many bits in a nibble? In a byte?
3. Which unit of a computer directs all the others?
4. What is the difference between primary and secondary memory?
5. Name the three topologies on the syllabus.
6. Which email protocol sends mail?
7. What does `$` do in a cell reference?
8. What must you do after changing the source data of a pivot table?
9. Which what-if tool answers "what input gives me this result"?
10. Which cell do you select before Freeze Panes to freeze both row 1 and
    column A?

**Answers:** 1. 10; `1010`. · 2. 4 and 8. · 3. The Control Unit. · 4. Primary is
directly accessible to the CPU and mostly volatile; secondary is slower,
non-volatile, and reached only through primary. · 5. Bus, star, ring. ·
6. **SMTP**. · 7. Makes the reference absolute so it does not shift when copied.
· 8. **Refresh** it. · 9. **Goal Seek**. · 10. **B2**.
