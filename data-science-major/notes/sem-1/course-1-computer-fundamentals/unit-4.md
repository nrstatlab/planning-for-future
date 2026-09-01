# Unit 4 — Spreadsheet Basics

**Syllabus topics:** Spreadsheet concepts — understanding rows, columns,
cells in tools like MS Excel/Google Sheets, cell referencing. Functions and
formulae — SUM, AVERAGE, IF, COUNT. Charts and graphs — creating visual
representations. Data handling — sorting, filtering, conditional formatting.
Text functions — LEFT, RIGHT, MID, LEN, TRIM, CONCAT, TEXTJOIN. Advanced
functions — logical: IF, AND, OR, IFERROR; lookup: VLOOKUP, HLOOKUP, XLOOKUP,
INDEX, MATCH.

---

The most immediately employable unit in the first year. VLOOKUP and pivot
tables are, by a wide margin, the most used data-analysis skills in the world.

These same functions applied to statistical data appear in
`labs/course-4-stats/excel-walkthroughs.md`
— worth reading alongside this unit.

## 4.1 Spreadsheet structure

| Term | Meaning |
|---|---|
| **Workbook** | The whole file (`.xlsx`) |
| **Worksheet** | One sheet within it |
| **Column** | Vertical, labelled A, B, C … XFD (16,384 columns) |
| **Row** | Horizontal, numbered 1 … 1,048,576 |
| **Cell** | The intersection, addressed as `B5` |
| **Range** | A block of cells, `A1:C10` |
| **Active cell** | The one currently selected |
| **Name box** | Shows the address; can also name a range |
| **Formula bar** | Shows the cell's actual contents |

**A cell displays a result but contains a formula.** Press **Ctrl + `** (grave
accent) to show all formulas at once — useful for checking, and examiners
sometimes ask for it.

## 4.2 Cell referencing — the concept everything depends on

| Type | Syntax | Behaviour when copied |
|---|---|---|
| **Relative** | `A1` | Both parts shift |
| **Absolute** | `$A$1` | Neither part shifts |
| **Mixed (locked column)** | `$A1` | Row shifts, column does not |
| **Mixed (locked row)** | `A$1` | Column shifts, row does not |

**Press F4** while editing a reference to cycle `A1` → `$A$1` → `A$1` → `$A1`.

### Why it matters

Suppose B1 holds a tax rate and you compute tax in C2:C10.

```
=B2*B1     copied down becomes =B3*B2, =B4*B3 …   WRONG — the rate moved
=B2*$B$1   copied down becomes =B3*$B$1, =B4*$B$1  correct — the rate is anchored
```

**Forgetting the `$` is the single most common spreadsheet error.** If a
formula works in the first row and produces nonsense below, this is almost
always why.

### The multiplication table — the classic mixed-reference exercise

To build a 10×10 table with a single formula copied everywhere:

```
=$A2*B$1
```

The column of `$A2` is locked but the row moves; the row of `B$1` is locked but
the column moves. One formula, filled across and down, produces the whole table.

### References across sheets and files

```
=Sheet2!A1                  another sheet
='My Sheet'!A1              sheet name with a space -- needs quotes
=[Book2.xlsx]Sheet1!A1      another workbook
```

## 4.3 Basic functions

| Function | Purpose | Example |
|---|---|---|
| `SUM(range)` | Total | `=SUM(B2:B10)` |
| `AVERAGE(range)` | Mean | `=AVERAGE(B2:B10)` |
| `COUNT(range)` | Count **numeric** cells | `=COUNT(B2:B10)` |
| `COUNTA(range)` | Count **non-empty** cells | `=COUNTA(A2:A10)` |
| `COUNTBLANK(range)` | Count empty cells | `=COUNTBLANK(A2:A10)` |
| `MAX` / `MIN` | Largest / smallest | `=MAX(B2:B10)` |
| `ROUND(n, digits)` | Round | `=ROUND(A1, 2)` |
| `ABS`, `SQRT`, `POWER` | Arithmetic | `=SQRT(A1)` |
| `TODAY()`, `NOW()` | Current date / date-time | `=TODAY()` |

**The three counts on one range.** Given `45`, *(empty)*, `absent`, `0`, `78`,
*(empty)*, `N/A`, `91`:

| Formula | Result | Counts |
|---|---:|---|
| `=COUNT(A1:A8)` | **4** | numeric cells only — `0` counts, `absent` does not |
| `=COUNTA(A1:A8)` | **6** | every non-empty cell, text included |
| `=COUNTBLANK(A1:A8)` | **2** | the empty ones |

`COUNTA + COUNTBLANK` always equals the size of the range. `COUNT` does not —
which is exactly why a "how many students sat the exam?" formula written with
`COUNT` silently ignores anyone marked `absent`.

**`COUNT` vs `COUNTA` is a favourite two-mark question.** `COUNT` counts only
numbers; `COUNTA` counts anything non-empty, including text.

### Conditional aggregates

```excel
=COUNTIF(B2:B20, ">50")                        how many exceed 50
=COUNTIFS(A2:A20,"IT", B2:B20,">50000")        multiple criteria
=SUMIF(A2:A20, "IT", C2:C20)                   sum C where A is "IT"
=SUMIFS(C2:C20, A2:A20,"IT", B2:B20,">2")      multiple criteria
=AVERAGEIF(A2:A20, "IT", C2:C20)
```

**Note the argument order differs.** `SUMIF(range, criteria, sum_range)` puts
the criteria range first; `SUMIFS(sum_range, range1, criteria1, …)` puts the sum
range first. This inconsistency in Excel's own design catches everyone.

## 4.4 Logical functions

### IF

```excel
=IF(condition, value_if_true, value_if_false)
=IF(B2>=40, "Pass", "Fail")
```

**Nested IF** for several bands — read it as a ladder, highest first:

```excel
=IF(B2>=90,"A", IF(B2>=75,"B", IF(B2>=60,"C", IF(B2>=40,"D","F"))))
```

**Order matters.** Testing `>=40` first would give everyone a D, because the
first true condition wins.

`IFS` (Excel 2019+) is cleaner:

```excel
=IFS(B2>=90,"A", B2>=75,"B", B2>=60,"C", B2>=40,"D", TRUE,"F")
```

### AND, OR, NOT

```excel
=AND(B2>=40, C2>=40)                    both must be true
=OR(B2>=90, C2>=90)                     at least one
=NOT(B2>=40)
=IF(AND(B2>=40, C2>=40), "Pass", "Fail")
```

### IFERROR

```excel
=IFERROR(A1/B1, "Cannot divide by zero")
=IFERROR(VLOOKUP(...), "Not found")
```

Replaces an error with something readable. Essential when a lookup may legitimately
find nothing — lab experiment 9 requires it explicitly.

### Error values worth recognising

| Error | Cause |
|---|---|
| `#DIV/0!` | Division by zero |
| `#N/A` | A lookup found nothing |
| `#NAME?` | Misspelled function name |
| `#VALUE!` | Wrong data type — text where a number is needed |
| `#REF!` | A referenced cell was deleted |
| `#NUM!` | An invalid number, e.g. `SQRT(-1)` |
| `#NULL!` | An invalid range operator |
| `#####` | Not an error — the column is too narrow |

## 4.5 Text functions

| Function | Purpose | Example | Result |
|---|---|---|---|
| `LEFT(text, n)` | First n characters | `=LEFT("DataScience",4)` | `Data` |
| `RIGHT(text, n)` | Last n characters | `=RIGHT("DataScience",7)` | `Science` |
| `MID(text, start, n)` | n characters from position | `=MID("DataScience",5,7)` | `Science` |
| `LEN(text)` | Length | `=LEN("Data")` | `4` |
| `TRIM(text)` | Remove extra spaces | `=TRIM("  a  b  ")` | `a b` |
| `CONCAT(a, b, …)` | Join | `=CONCAT("Data","Science")` | `DataScience` |
| `TEXTJOIN(sep, ignore_empty, …)` | Join with a separator | `=TEXTJOIN(", ",TRUE,A1:A3)` | `a, b, c` |
| `UPPER` / `LOWER` / `PROPER` | Case | `=PROPER("john doe")` | `John Doe` |
| `FIND(sub, text)` | Position — **case-sensitive** | `=FIND("S","DataScience")` | `5` |
| `SEARCH(sub, text)` | Position — **not** case-sensitive | `=SEARCH("s","DataScience")` | `5` |
| `SUBSTITUTE(text, old, new)` | Replace text | `=SUBSTITUTE("a-b","-","+")` | `a+b` |
| `TEXT(value, format)` | Format a number as text | `=TEXT(0.85,"0%")` | `85%` |

**`TRIM` removes leading and trailing spaces and collapses internal runs to a
single space.** It is the first thing to try when a `VLOOKUP` mysteriously
fails — an invisible trailing space in the lookup value is a very common cause.

**`FIND` vs `SEARCH`:** `FIND` is case-sensitive and accepts no wildcards;
`SEARCH` is neither. A standard two-mark distinction.

**Splitting a full name** — a routine exam task:

```excel
First name:  =LEFT(A2, FIND(" ",A2)-1)
Last name:   =RIGHT(A2, LEN(A2)-FIND(" ",A2))
```

## 4.6 Lookup functions

**The most important section in this unit.**

### VLOOKUP — vertical lookup

```excel
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
=VLOOKUP(E2, $A$2:$D$100, 4, FALSE)
```

| Argument | Meaning |
|---|---|
| `lookup_value` | What to search for |
| `table_array` | Where to search — **anchor it with `$`** |
| `col_index_num` | Which column to return, **counting from the left of the table** |
| `range_lookup` | `FALSE` = exact match, `TRUE` = approximate |

**Four rules that cost marks when broken:**

1. **Always use `FALSE`** unless you deliberately want a range match. `TRUE` is
   the default and it silently returns wrong answers on unsorted data.
2. **The lookup value must be in the first column** of the table array. VLOOKUP
   cannot look leftwards.
3. **`col_index_num` counts from the table's first column**, not from column A
   of the sheet.
4. **Anchor the table array** with `$`, or copying the formula down shifts the
   table out from under it.

### HLOOKUP — horizontal lookup

The same thing across a row instead of down a column:

```excel
=HLOOKUP(lookup_value, table_array, row_index_num, FALSE)
```

Used when your data is laid out with categories across the top — lab experiment
10 uses it to extract department heads by role.

### XLOOKUP — the modern replacement

```excel
=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found])
=XLOOKUP(E2, $A$2:$A$100, $D$2:$D$100, "Not found")
```

**Why it is better than VLOOKUP:**

1. **Can look left** — the lookup and return arrays are independent
2. **Exact match by default** — no `FALSE` to forget
3. **Built-in not-found value** — no `IFERROR` wrapper needed
4. **Immune to inserted columns** — no numeric column index to break
5. Searches from the end with an optional argument

Available in Excel 2021 and Microsoft 365, and in Google Sheets. Older versions
need INDEX+MATCH.

### INDEX + MATCH — the classic combination

```excel
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))
=INDEX($D$2:$D$100, MATCH(E2, $A$2:$A$100, 0))
```

- `MATCH` returns the **position** of a value in a range
- `INDEX` returns the **value** at a given position

Together they do what VLOOKUP does, but can look in any direction and do not
break when columns are inserted. The `0` in MATCH means exact match — the
equivalent of VLOOKUP's `FALSE`.

**Know all three approaches.** Exams ask you to compare them, and lab experiment
10 requires VLOOKUP, HLOOKUP, XLOOKUP **and** INDEX+MATCH on the same data
precisely so you can see the differences.

### Comparison

| | VLOOKUP | HLOOKUP | XLOOKUP | INDEX+MATCH |
|---|---|---|---|---|
| Direction | Down a column | Across a row | Any | Any |
| Can look left | No | — | **Yes** | **Yes** |
| Default match | Approximate ⚠ | Approximate ⚠ | **Exact** | Set by you |
| Survives inserted columns | No | No | **Yes** | **Yes** |
| Availability | All versions | All versions | 2021+ | All versions |

## 4.7 Charts

| Chart | Best for |
|---|---|
| **Column / Bar** | Comparing categories |
| **Line** | Trends over time |
| **Pie** | Parts of a whole — **only if they sum to 100%** |
| **Scatter (XY)** | Relationship between two numeric variables |
| **Area** | Cumulative totals over time |
| **Combo** | Two different scales, e.g. revenue and growth % |
| **Histogram** | Distribution of continuous data |
| **Sparkline** | A tiny trend inside a single cell |

**Creating one:** select the data including headers → **Insert** → choose the
chart type.

**Chart elements that earn marks:** a title, axis titles, a legend, data labels
where useful, and sensible gridlines.

**Choosing badly is a real error.** A pie chart with fifteen slices is
unreadable; a line chart of unordered categories implies a trend that does not
exist; a scatter plot with the points joined up is simply wrong.

## 4.8 Data handling

### Sorting

**Data → Sort.** Sort by several levels — department, then salary descending.

**Always select the whole data range first**, or Excel sorts one column and
leaves the others in place, silently destroying every row's integrity. Excel
usually warns you; do not dismiss the warning.

### Filtering

**Data → Filter** adds dropdown arrows to the headers. Filter by value, by
condition (greater than, contains, between), or by colour.

**Advanced Filter** supports complex criteria and can copy results elsewhere.

Filtering **hides** rows rather than deleting them; the row numbers turn blue
and skip, which is how you can tell a filter is active.

### Conditional formatting

*(Also listed in Unit 5, where the treatment is fuller — see review finding
**D9**.)*

**Home → Conditional Formatting.** Formatting that reacts to the value:

- **Highlight Cells Rules** — greater than, between, text contains, duplicates
- **Top/Bottom Rules** — top 10, above average
- **Data Bars** — an in-cell bar chart
- **Colour Scales** — a heat map across a range
- **Icon Sets** — arrows, traffic lights
- **New Rule → Use a formula** — for anything else

**The formula-based rule** is the powerful one. To highlight the *entire row*
where column C is below 40:

```excel
=$C2<40
```

Note the mixed reference: `$C` locks the column so every cell in the row is
tested against column C, while `2` moves so each row tests its own value.

### Data validation

**Data → Data Validation** — restricts what may be entered:

| Setting | Purpose |
|---|---|
| **List** | A dropdown of allowed values |
| **Whole number / Decimal** | A numeric range |
| **Date / Time** | A valid range |
| **Text length** | Minimum and maximum |
| **Custom** | A formula |
| **Input Message** | A hint shown on selection |
| **Error Alert** | The message shown on invalid entry |

Lab experiment 12 requires all of these on a student registration form.

---

## Exam questions from this unit

**Two marks**

1. Differentiate relative and absolute referencing.
2. Distinguish `COUNT` from `COUNTA`.
3. What does `TRIM` do, and when is it needed?
4. Distinguish `FIND` from `SEARCH`.
5. Why does `#####` appear in a cell?

**Five marks**

1. Explain VLOOKUP with syntax, arguments and an example.
2. Explain the logical functions IF, AND, OR and IFERROR with examples.
3. Explain the text functions with examples.
4. Explain conditional formatting with its types.
5. Explain the types of charts and when each is appropriate.

**Ten marks**

1. Explain the lookup functions — VLOOKUP, HLOOKUP, XLOOKUP and INDEX+MATCH —
   comparing them.
2. Explain cell referencing in detail, and demonstrate with a multiplication
   table built from one formula.

## Mistakes that cost marks

- Omitting `$` and watching a formula break when copied
- Forgetting `FALSE` in VLOOKUP and getting silently wrong results
- Counting `col_index_num` from column A rather than from the table's first
  column
- Trying to make VLOOKUP look leftwards
- Sorting one column without selecting the rest of the data
- Writing a nested IF ladder in the wrong order
- Using a pie chart for data that does not sum to a whole
