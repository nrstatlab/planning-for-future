# Course 1 Lab — Computer Fundamentals and Office Automation

**14 experiments**

Word, PowerPoint and Excel cannot be installed in the environment these notes
are verified in, so each experiment has two halves:

> ### 📖 How this lab is verified
>
> - **The click-path** — the menus, dialogs and formulas, written out below.
>   Marked **NOT EXECUTED**. This is what the lab examiner asks you to
>   demonstrate.
> - **A Python equivalent that runs** — the same arithmetic, executed and
>   asserted by `tools/run_office_labs.py`,
>   with the scripts in `labs/course-1-office/`.
>
> **Eight of the fourteen have a runnable half.** Experiments 1–6 produce
> documents, a drawing or a layout, with nothing to compute; they are
> click-path only and the runner asserts that list against what is on disk, so
> an experiment cannot quietly go missing.
>
> The Python halves import nothing but the standard library, and they are
> **not a substitute for the spreadsheet**. They exist so that every figure
> below is produced by running code — when this page says grading on the total
> awards 19 of 20 students an A, experiment 8 proves it on the actual class.

```bash
python3 tools/run_office_labs.py
```

For the same spreadsheet functions applied to statistical data, see
`labs/course-4-stats/excel-walkthroughs.md`.

---

## The experiments

| # | Experiment | Unit | Tool | Verified by |
|:---:|---|:---:|---|---|
| 1 | Assembling and disassembling a computer | 2 | Hardware | — |
| 2 | Identify your institution's network topology | 2 | Observation | — |
| 3 | Prepare your resume | 3 | Word | — |
| 4 | Write a leave letter to a higher official | 3 | Word | — |
| 5 | Presentation with text, audio and video | 3 | PowerPoint | — |
| 6 | Class timetable | 4 | Excel | — |
| 7 | Gross and net salary of 5+ employees | 4 | Excel | `07_salary.py` |
| 8 | Class-wise and subject-wise results | 4 | Excel | `08_class_results.py` |
| 9 | Grade evaluation with IF, AND, OR, IFERROR | 4 | Excel | `09_grade_functions.py` |
| 10 | Employee search with VLOOKUP, HLOOKUP, XLOOKUP, INDEX, MATCH | 4 | Excel | `10_lookups.py` |
| 11 | Sales report with pivot tables and charts | 5 | Excel | `11_pivot_sales.py` |
| 12 | Data entry form with drop-downs and input rules | 5 | Excel | `12_validation.py` |
| 13 | Budget planning with Goal Seek and Scenario Manager | 5 | Excel | `13_budget.py` |
| 14 | Dashboard with combo charts, sparklines and slicers | 5 | Excel | `14_dashboard.py` |

*(The syllabus writes experiment 1 as "Dessembling" — a typo in the official
document for "Disassembling".)*

---

## Unit 2 — hardware and networks (experiments 1–2)

### 1 — Assembling and disassembling

Identify and be able to name: the motherboard, CPU and its heatsink, RAM
modules and their slots, SMPS (power supply), hard disk or SSD, SATA and power
cables, expansion cards, and the front-panel connectors.

**Safety, which examiners ask about:** unplug the power, discharge static by
touching the metal chassis or wearing an anti-static strap, never force a
component, and note the orientation of everything before removing it.

**Write notes as you go** — the practical record matters as much as the doing.

### 2 — Network topology of your institution

Walk the lab and record what you actually see: how many machines, how they
connect to the switch, where the switch sits, how the switch reaches the router,
and how the router reaches the ISP.

Almost every college lab is a **physical star** — every machine cabled to a
central switch. Draw it, label the devices, and state the topology with your
reasoning. If several labs each have a switch, all feeding one core switch, that
is a **tree** (a hierarchy of stars) and saying so earns extra credit.

## Unit 3 — Word and PowerPoint (experiments 3–5)

### 3 — Resume

Use **styles** for the section headings, not manual formatting. One page for a
first-year student. Include: name and contact details, objective, education with
percentages, skills, projects, certifications, achievements.

**Export to PDF** so the layout cannot shift on someone else's machine.

### 4 — Leave letter

Standard business letter format: sender's address, date, recipient's
designation and address, subject line, salutation, body (reason, dates,
handover arrangements), closing, signature.

Ten days' leave means stating the **exact dates** and what happens to your work
in the meantime.

### 5 — Presentation with text, audio and video

The requirement is specifically **all three media**.

- **Audio:** Insert → Audio → Audio on My PC, or Record Audio
- **Video:** Insert → Video → This Device, or an online video
- Set playback to Automatically or On Click under the Playback tab

**Embed rather than link** where possible, or the media will not play on the
examiner's machine.

Add transitions between slides and animations within one slide, so both are
demonstrated.

## Unit 4 — Excel formulas and functions (experiments 6–10)

### 6 — Class timetable

A grid with days down the side and periods across the top. Use **Merge Cells**
for double periods, borders for the grid, and colour-coding by subject.

Use **Freeze Panes** so the day column stays visible when scrolling — a small
touch that shows understanding.

### 7 — Gross and net salary

The standard allowance structure:

```
DA        = 30% of Basic Pay
HRA       = 15% of Basic Pay
Deduction = 10% of (Basic Pay + DA)     ← includes DA
Gross     = Basic Pay + DA + HRA
Net       = Gross − Deduction
```

Put the **percentages in their own cells** and reference them absolutely
(`$B$1`), rather than typing `0.30` into every formula. Then changing the DA
rate is a one-cell edit — and that is exactly what earns marks over hard-coded
numbers.

Format as currency, and total the columns.

**The sheet, worked through.** Six employees, columns `A Name  B EmpID
C Department  D Basic`, with the rates in `$B$1`, `$B$2`, `$B$3`:

| Name | Basic | DA | HRA | Gross | Deduction | Net |
|---|---:|---:|---:|---:|---:|---:|
| Anitha Rao | 25,000 | 7,500 | 3,750 | 36,250 | 3,250 | 33,000 |
| Bharat Kumar | 32,000 | 9,600 | 4,800 | 46,400 | 4,160 | 42,240 |
| Chitra Devi | 18,500 | 5,550 | 2,775 | 26,825 | 2,405 | 24,420 |
| Daniel Joseph | 45,000 | 13,500 | 6,750 | 65,250 | 5,850 | 59,400 |
| Esha Nair | 28,000 | 8,400 | 4,200 | 40,600 | 3,640 | 36,960 |
| Faisal Ahmed | 52,000 | 15,600 | 7,800 | 75,400 | 6,760 | 68,640 |
| **TOTAL** | **200,500** | **60,150** | **30,075** | **290,725** | **26,065** | **264,660** |

Notice what falls out of the rates: **Gross is always 1.45 × Basic** and **Net
is always 1.32 × Basic**. Check one row against that and you have checked the
whole sheet.

> ### ⚠️ The deduction is on Basic **+ DA**
>
> Take 10% of Basic alone and Net becomes 1.35 × Basic instead of 1.32 ×.
> Nothing errors. On this payroll it overpays by **₹6,015 a month** — 3% of
> the ₹200,500 basic bill — and it would keep doing so until somebody
> reconciled the accounts.

*(The same calculation in C is lab experiment 12 of Course 2 — comparing the two
is instructive.)*

### 8 — Class results

Twenty students, several subjects. Compute per student: total, average, result
(pass/fail), grade. Compute per subject: highest, lowest, average, pass count.

**State your column layout before you write a single formula**, because every
cell reference below depends on it:

| A | B | C D E F G | H | I | J | K |
|---|---|---|---|---|---|---|
| Roll | Name | five subject marks | Total | Average | Result | Grade |

```excel
H2  Total     =SUM(C2:G2)
I2  Average   =AVERAGE(C2:G2)
J2  Result    =IF(MIN(C2:G2)>=40,"Pass","Fail")
K2  Grade     =IF(I2>=90,"A",IF(I2>=75,"B",IF(I2>=60,"C",IF(I2>=40,"D","F"))))
    Subject high   =MAX(C2:C21)
    Subject low    =MIN(C2:C21)
    Pass count     =COUNTIF(C2:C21,">=40")
```

> ### ⚠️ Grade on the **average**, not the total
>
> `K2` must reference **`I2`**, the average. Point it at `H2` — the total —
> and with five subjects the total runs to 500, so **every student scoring 90
> marks out of 500 is awarded an "A"**. The formula still calculates, the
> spreadsheet reports no error, and the grades are silently nonsense.
>
> This is the single easiest way to lose marks in this experiment, and it is
> why the layout table above is written down first.

Note the `Result` formula uses `MIN` — a student must pass **every** subject,
not merely average 40.

**What the two mistakes actually cost.** Run on the twenty-student class in
`labs/course-1-office/fixtures.py`:

| | Correct formula | The mistake |
|---|---|---|
| Grade | A:3 B:6 C:4 D:6 F:1 | **A:19 B:1** — and Kavya, who failed all five papers with 80/500, is awarded a **B** |
| Result | 16 pass, 4 fail | 19 pass — Divya (38 in Chemistry), Ishita (38 in Maths) and Rahul (35 in Maths) all pass in error |

Both sheets calculate cleanly. Neither shows an error. That is the whole
problem with them.

**The subject-wise half**, from the same class:

| Subject | High | Low | Average | Passed |
|---|---:|---:|---:|---:|
| Maths | 98 | 12 | 67.00 | 17 |
| Physics | 96 | 20 | 68.95 | 19 |
| Chemistry | 99 | 8 | 67.95 | 18 |
| English | 95 | 15 | 68.30 | 19 |
| Computers | 97 | 25 | 69.95 | 18 |

Maths has the lowest class average, so it is the hardest paper — even though
Chemistry contains the single lowest mark. Averages and extremes answer
different questions, and the examiner may ask for either.

### 9 — Grade evaluation with IF, AND, OR, IFERROR

The syllabus specifies all four functions.

```excel
Grade with a missing-mark guard:
=IFERROR(IF(B2>=90,"A",IF(B2>=75,"B",IF(B2>=60,"C",IF(B2>=40,"D","F")))), "No data")

Pass only if both subjects are cleared:
=IF(AND(B2>=40, C2>=40), "Pass", "Fail")

Distinction in at least one subject:
=IF(OR(B2>=90, C2>=90), "Distinction", "-")
```

**Test it with a blank cell and with text** in the marks column, so you can show
`IFERROR` actually doing something. An examiner will try exactly that — and
here is what they will find:

| `B2` holds | Plain nested `IF` | What it should say |
|---|---|---|
| `95` | A | A |
| `75` | B | B (the cut-off is `>=`, so 75 is a B, not a C) |
| `39` | F | F |
| *(empty)* | **F** | Absent |
| `AB` | **A** | No data |

> ### ⚠️ `IFERROR` does not catch a blank
>
> An empty cell is not an error, so `IFERROR` never sees it. Excel coerces it
> to **0** in the comparison and the student is graded **F** — a fail recorded
> for someone who was never examined. Text is worse: in Excel's ordering text
> sorts **above every number**, so `"AB">=90` is TRUE and the cell grades
> **A**.
>
> Guard both explicitly:
>
> ```excel
> =IF(ISBLANK(B2),"Absent",
>    IFERROR(IF(NOT(ISNUMBER(B2)),NA(),
>      IF(B2>=90,"A",IF(B2>=75,"B",IF(B2>=60,"C",IF(B2>=40,"D","F"))))),
>    "No data"))
> ```

`AND` and `OR` inherit the same coercion: with `B2` empty,
`AND(B2>=40,C2>=40)` is FALSE and `OR(B2>=90,C2>=90)` still reports a
distinction off `C2` alone.

### 10 — Employee search, four ways

Build `Name, ID, Department, Salary`, then implement the same lookup four ways:

```excel
VLOOKUP      =VLOOKUP($F$2, $A$2:$D$50, 4, FALSE)
HLOOKUP      =HLOOKUP($F$2, $A$1:$Z$5, 3, FALSE)        (for row-oriented data)
XLOOKUP      =XLOOKUP($F$2, $B$2:$B$50, $D$2:$D$50, "Not found")
INDEX+MATCH  =INDEX($D$2:$D$50, MATCH($F$2, $B$2:$B$50, 0))
```

**The point of doing all four** is to see the differences: VLOOKUP cannot look
left and breaks when a column is inserted; XLOOKUP does neither; INDEX+MATCH
matches XLOOKUP's flexibility and works in every Excel version.

Be ready to explain that in the viva — it is the obvious question. Two
demonstrations make the answer concrete, on the payroll sheet from
experiment 7 (`A Name  B EmpID  C Department  D Basic`):

**Look up by EmpID and fetch the Name.** `Name` is one column *left* of the key,
so there is no positive `col_index` that reaches it — you cannot write the
`VLOOKUP` at all. `XLOOKUP` and `INDEX+MATCH` return `Daniel Joseph` without
comment, because they take two independent ranges instead of one range and an
offset.

**Now insert a `Grade` column before `Basic Pay`.**

| Formula | Before the insert | After |
|---|---:|---|
| `=VLOOKUP($F$2,$A$2:$D$7,4,FALSE)` | 45,000 | **`G4`** — the new Grade column |
| `=XLOOKUP($F$2,$A$2:$A$7,$E$2:$E$7)` | 45,000 | 45,000 |
| `=INDEX($E$2:$E$7,MATCH($F$2,$A$2:$A$7,0))` | 45,000 | 45,000 |

`VLOOKUP`'s `4` is a **position**; the other two name a **range**. So only
`VLOOKUP` breaks — and it breaks silently, returning a plausible-looking value
with no error to warn you.

One more difference worth a mark: for a key that is not in the table,
`VLOOKUP` and `INDEX+MATCH` both give `#N/A`, while `XLOOKUP` returns whatever
you put in its fourth argument. That argument is the reason `XLOOKUP` exists.

## Unit 5 — Excel analysis and presentation (experiments 11–14)

### 11 — Sales report with pivot tables

Dataset: Product, Region, Date, Quantity, Revenue.

1. Insert → PivotTable
2. Rows = Region, Columns = Product, Values = Sum of Revenue
3. Add a second pivot: Rows = Date (grouped by month), Values = Sum of Revenue
4. Insert PivotCharts for both
5. Add a slicer on Region and connect it to **both** pivots via Report
   Connections

Right-click a date → **Group** → Months and Years, to turn transactions into a
monthly trend.

**The nine transactions used here are the same rows Course 11 loads into Power
BI and Tableau**, so the totals can be compared straight across the programme.
Pivot one gives:

| | Notebook | Rice 5kg | Shampoo 200ml | Tea 500g | **Total** |
|---|---:|---:|---:|---:|---:|
| North | 1,400 | 1,120 | — | — | **2,520** |
| South | — | 4,480 | 1,680 | 4,200 | **10,360** |
| **Grand Total** | **1,400** | **5,600** | **1,680** | **4,200** | **12,880** |

₹10,360 for South is the figure Course 11 reaches with DAX, Course 12 B with
Hive and Spark, Course 13 B with a warehouse query and Course 15 B with an ETL
job. Six different engines, one number — which is only meaningful because the
runner asserts the underlying rows still match.

A pivot table **is** a group-by: Rows are the keys down the side, Columns the
keys across the top, Values the aggregation, and the Grand Total is the same
aggregation with no grouping at all. Switching *Value Field Settings* on one
field between Sum, Count and Average — 87, 9 and 9.67 for Quantity here — is
the fastest way to see that.

> ### ⚠️ Grouping by month drops the empty months
>
> No sale in this data falls in March, and the grouped pivot shows **four**
> month rows, not five. A line chart drawn from it joins February straight to
> April, rendering two months of change as one step. Experiment 14 shows what
> that does to a growth column.

### 12 — Data entry form with validation

A student registration form using **Data → Data Validation**:

| Field | Validation |
|---|---|
| Course | **List** — a dropdown of allowed courses |
| Roll number | **Whole number**, within a range |
| Date of birth | **Date**, between sensible limits |
| Phone | **Text length** = 10 |
| Email | **Custom** formula: `=ISNUMBER(SEARCH("@",E2))` |

For each, fill in the **Input Message** tab (the hint shown on selection) and
the **Error Alert** tab (Stop / Warning / Information, with your own message).
The syllabus asks for all three parts explicitly.

**Stop refuses the value; Warning and Information both let it through** after a
confirmation. A form that must not accept bad data has to use Stop, and that is
a viva question.

> ### ⚠️ Know what your own rule lets through
>
> `=ISNUMBER(SEARCH("@",E2))` asks one question: does an `@` appear anywhere?
> So it accepts **`@`** on its own, and accepts **`not an email @ all`**.
> Neither is an address, and Excel takes both without a murmur.
>
> Tighten it if you like —
> `=AND(ISNUMBER(SEARCH("@",E2)),ISNUMBER(SEARCH(".",E2)),LEN(E2)>=6,ISERROR(SEARCH(" ",E2)))`
> rejects both — but nothing short of a regular expression validates an email
> address properly. **Being able to say where your validation stops is the
> point of the exercise**, and it earns more credit than a rule you cannot
> describe.

Test every rule with values that should pass *and* values that should be
refused. A rule you have not tried to break is a rule you have not tested.

### 13 — Budget with Goal Seek and Scenario Manager

Build a personal budget: income, expense categories, total expenses, savings.

**Goal Seek:** set the savings cell to a target, changing the income cell.
Report the income required.

**Scenario Manager:** create *Best case*, *Worst case* and *Realistic*, each
with different income and expense assumptions, then produce a **Scenario
Summary** report comparing them side by side.

**One-variable data table:** list several expense values down a column and show
the resulting savings for each.

All three are required — do not stop at Goal Seek.

**Worked through** on income ₹45,000 and expenses ₹33,000 (rent 15,000, food
8,000, transport 3,500, utilities 2,800, entertainment 2,200, miscellaneous
1,500), giving savings of ₹12,000 — a rate of 26.67%.

| Goal Seek | Set cell | To value | By changing | Answer |
|---|---|---|---|---|
| A savings **amount** | Savings | 20,000 | Income | **53,000** |
| A savings **rate** | Rate | 30% | Income | **47,142.86** |

The second is the one worth doing. The rate is **not linear** in income, so you
cannot read the answer off the sheet: moving from 26.67% to 30% needs a rise of
₹2,142.86, which is not the figure most people guess.

Scenario Summary:

| Scenario | Income | Expenses | Savings | Rate |
|---|---:|---:|---:|---:|
| Best case | 52,000 | 31,000 | 21,000 | 40.4% |
| Realistic | 45,000 | 33,000 | 12,000 | 26.7% |
| Worst case | 41,000 | 35,500 | 5,500 | 13.4% |

The *Realistic* column must reproduce the live sheet exactly. If it does not,
the scenario has drifted from the model it claims to describe — the commonest
fault in this experiment, and easy to check.

> ### 📖 Why Goal Seek sometimes says it "may not have found a solution"
>
> Goal Seek is a numerical root finder, not algebra: it changes one cell,
> watches another, and stops when the watched cell is close enough. It needs
> the answer to be **reachable** and the formula to move **monotonically**
> towards it. Ask this sheet for a 100% savings rate and there is no income
> that achieves it — the rate approaches 100% but never arrives — so Goal Seek
> exhausts its iterations and reports exactly that.

The **one-variable data table** completes the set: rent down the left column,
savings recalculated beside each — 12,000 → 15,000 savings, rising to 18,000 →
9,000. A slope of exactly −1: one rupee of rent, one rupee of savings. The
table exists to make that visible rather than argued.

### 14 — Dashboard

The capstone. Combine everything:

1. **Combo chart** — revenue as columns, growth percentage as a line on a
   **secondary axis**
2. **Sparklines** — a trend line beside each product row
3. **Slicers** connected to every pivot table
4. **KPI cells** at the top: total, growth, best product, average
5. **Tidy up:** hide gridlines (View → uncheck Gridlines), hide the working
   sheets, protect the dashboard sheet

**KPI cells**, on the same nine transactions as experiment 11: total revenue
**12,880**, best product **Rice 5kg** (5,600), average per transaction
**1,431.11**, transactions **9**.

**Why the growth line needs a secondary axis:** revenue is in rupees and growth
is a percentage. Plotted on one axis, a 30% growth figure is 0.3 of a rupee and
disappears into the baseline.

> ### ⚠️ The growth column divides by the previous period
>
> Lay the months out completely and this data reads:
>
> | Month | Revenue | Growth |
> |---|---:|---:|
> | 2026-01 | 5,180 | — |
> | 2026-02 | 2,480 | −52.12% |
> | 2026-03 | 0 | −100.00% |
> | 2026-04 | 3,640 | **`#DIV/0!`** |
> | 2026-05 | 1,580 | −56.59% |
>
> March has no sales, so April divides by zero. That is what the `IFERROR`
> wrapper from experiment 9 is for — without it the line series breaks at
> April and the tile shows an error where a number should be.
>
> Dropping the empty month instead does not fix it, it hides it: April then
> reports **+46.77%**, which is two months of change labelled as one, and
> nothing on the chart says so. **Keep the empty month and wrap the formula.**

**Test it before submitting:** click a slicer and confirm that *every* chart
updates. If one does not, its pivot is not connected — the commonest fault, and
the first thing an examiner will check.

---

## Lab exam tips

1. **Save constantly**, under a filename containing your roll number.
2. **Show your formulas.** Press **Ctrl + `** to display them all; examiners
   often ask for this.
3. **Format properly.** Currency for money, borders on tables, sensible column
   widths. Marks are given for presentation.
4. **Label your charts.** Title, axis titles, legend.
5. **Use absolute references** where a formula will be copied — and be able to
   explain why.
6. **Test the edge cases** yourself: a blank cell, a zero, a value not in the
   lookup table.
7. **Expect a viva.** "Why `FALSE` in that VLOOKUP?", "what happens if I change
   this cell?", "why is that reference `$C2` and not `$C$2`?"
