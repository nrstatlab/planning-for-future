---
layout: note
title: "Course 1 Lab — Computer Fundamentals and Office Automation"
section: "Data Science Major"
---

# Course 1 Lab — Computer Fundamentals and Office Automation

**1 credit · 2 hrs/week · 14 experiments** (syllabus pages 7–8)

Unlike the other courses, this lab produces documents and spreadsheets rather
than code, so there are no files in `labs/` for it. What follows is what each
experiment asks for and how to do it well.

For the same spreadsheet functions applied to statistical data, see
[`labs/course-4-stats/excel-walkthroughs.md`](../../../labs/course-4-stats/excel-walkthroughs.html).

---

## The experiments

| # | Experiment | Unit | Tool |
|:---:|---|:---:|---|
| 1 | Assembling and disassembling a computer | 2 | Hardware |
| 2 | Identify your institution's network topology | 2 | Observation |
| 3 | Prepare your resume | 3 | Word |
| 4 | Write a leave letter to a higher official | 3 | Word |
| 5 | Presentation with text, audio and video | 3 | PowerPoint |
| 6 | Class timetable | 4 | Excel |
| 7 | Gross and net salary of 5+ employees | 4 | Excel |
| 8 | Class-wise and subject-wise results | 4 | Excel |
| 9 | Grade evaluation with IF, AND, OR, IFERROR | 4 | Excel |
| 10 | Employee search with VLOOKUP, HLOOKUP, XLOOKUP, INDEX, MATCH | 4 | Excel |
| 11 | Sales report with pivot tables and charts | 5 | Excel |
| 12 | Data entry form with drop-downs and input rules | 5 | Excel |
| 13 | Budget planning with Goal Seek and Scenario Manager | 5 | Excel |
| 14 | Dashboard with combo charts, sparklines and slicers | 5 | Excel |

*(The syllabus writes experiment 1 as "Dessembling" — a typo in the official
document for "Disassembling".)*

---

## Notes on each experiment

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

*(The same calculation in C is lab experiment 12 of Course 2 — comparing the two
is instructive.)*

### 8 — Class results

Twenty students, several subjects. Compute per student: total, average, result
(pass/fail), grade. Compute per subject: highest, lowest, average, pass count.

```excel
Total          =SUM(C2:G2)
Average        =AVERAGE(C2:G2)
Result         =IF(MIN(C2:G2)>=40,"Pass","Fail")
Grade          =IF(H2>=90,"A",IF(H2>=75,"B",IF(H2>=60,"C",IF(H2>=40,"D","F"))))
Subject high   =MAX(C2:C21)
Subject low    =MIN(C2:C21)
Pass count     =COUNTIF(C2:C21,">=40")
```

Note the `Result` formula uses `MIN` — a student must pass **every** subject,
not merely average 40.

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
`IFERROR` actually doing something. An examiner will try exactly that.

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

Be ready to explain that in the viva — it is the obvious question.

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

### 14 — Dashboard

The capstone. Combine everything:

1. **Combo chart** — revenue as columns, growth percentage as a line on a
   **secondary axis**
2. **Sparklines** — a trend line beside each product row
3. **Slicers** connected to every pivot table
4. **KPI cells** at the top: total, growth, best product, average
5. **Tidy up:** hide gridlines (View → uncheck Gridlines), hide the working
   sheets, protect the dashboard sheet

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
