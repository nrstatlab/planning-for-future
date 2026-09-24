"""Experiment 10 -- The same employee lookup, four ways.

VLOOKUP, HLOOKUP, XLOOKUP and INDEX+MATCH all answer the same question, so
the experiment is pointless unless you can say how they DIFFER. This script
models each one's actual mechanics and then demonstrates the two differences
that matter, with the sheet in front of you:

  1. VLOOKUP can only look RIGHT from its key column. Keying on EmpID
     (column B) to fetch Name (column A) is not a hard VLOOKUP -- it is an
     impossible one.
  2. VLOOKUP's column number is a POSITION, not a reference. Insert a column
     and the formula keeps working and starts returning the wrong field.
     XLOOKUP and INDEX+MATCH do not, because they name a range instead.

The sheet is the payroll of experiment 7:  A Name  B EmpID  C Department
D Basic Pay.
"""
from fixtures import EMPLOYEES, EMP_COLUMNS


class LeftLookupError(Exception):
    """What VLOOKUP cannot do. Excel reports it as #N/A."""


def vlookup(key, table, columns, col_index, exact=True):
    """=VLOOKUP(key, range, col_index, FALSE)

    Searches the FIRST column of `table` only, and returns the col_index'th
    column of the same row, counting the search column as 1.
    """
    if not exact:
        raise NotImplementedError("approximate match is not used here")
    if not 1 <= col_index <= len(columns):
        raise IndexError("#REF!  -- col_index is outside the range")
    for row in table:
        if row[0] == key:
            return row[col_index - 1]
    return "#N/A"


def hlookup(key, table, columns, row_index):
    """=HLOOKUP(key, range, row_index, FALSE), on the TRANSPOSED sheet.

    HLOOKUP is VLOOKUP rotated: it searches the first ROW and returns from
    the row_index'th row. It exists for sheets laid out with fields down the
    side and records across the top -- which is why this one transposes the
    payroll first.
    """
    transposed = [[columns[c]] + [row[c] for row in table]
                  for c in range(len(columns))]
    header = transposed[0]                       # the Name row
    for column in range(1, len(header)):
        if header[column] == key:
            return transposed[row_index - 1][column]
    return "#N/A"


def xlookup(key, lookup_values, return_values, if_not_found="Not found"):
    """=XLOOKUP(key, lookup_array, return_array, "Not found")

    Two independent ranges, so direction is irrelevant and there is no
    position to break.
    """
    for value, result in zip(lookup_values, return_values):
        if value == key:
            return result
    return if_not_found


def index_match(key, lookup_values, return_values):
    """=INDEX(return_range, MATCH(key, lookup_range, 0))"""
    for position, value in enumerate(lookup_values, start=1):   # MATCH
        if value == key:
            return return_values[position - 1]                  # INDEX
    return "#N/A"


def column(table, columns, name):
    return [row[columns.index(name)] for row in table]


def main():
    table = [list(row) for row in EMPLOYEES]
    columns = list(EMP_COLUMNS)

    print("  The sheet:  " + "  ".join(
        f"{chr(65 + i)}={c}" for i, c in enumerate(columns)))
    print()
    for row in table:
        print(f"    {row[0]:<15}{row[1]:<7}{row[2]:<13}{row[3]:>7,}")

    # --- all four, answering "what does Daniel Joseph earn?" ----------------
    key = "Daniel Joseph"
    names = column(table, columns, "Name")
    basics = column(table, columns, "Basic")

    answers = {
        "VLOOKUP":     vlookup(key, table, columns, 4),
        "HLOOKUP":     hlookup(key, table, columns, 4),
        "XLOOKUP":     xlookup(key, names, basics),
        "INDEX+MATCH": index_match(key, names, basics),
    }
    print(f"\n  Basic pay of {key}:")
    for how, value in answers.items():
        print(f"    {how:<14}{value:>8,}")
    assert set(answers.values()) == {45000}, answers

    # A key that is not there. Each function fails differently, and the
    # difference is the reason XLOOKUP exists.
    missing = "Zoya Khan"
    print(f"\n  A key that is not in the sheet ({missing}):")
    print(f"    VLOOKUP       {vlookup(missing, table, columns, 4)}")
    print(f"    XLOOKUP       {xlookup(missing, names, basics)}"
          "     <- because you supplied the fourth argument")
    print(f"    INDEX+MATCH   {index_match(missing, names, basics)}")
    assert vlookup(missing, table, columns, 4) == "#N/A"
    assert xlookup(missing, names, basics) == "Not found"

    # --- difference 1: VLOOKUP cannot look left -----------------------------
    emp_ids = column(table, columns, "EmpID")
    print("\n  Now look up by EmpID and fetch the Name (column B -> column A):")
    try:
        # Name is one column LEFT of EmpID, so there is no positive col_index
        # that reaches it. The honest model of this is an exception, not a
        # wrong answer -- you cannot write the formula at all.
        vlookup("E104", [r[1:] for r in table], columns[1:], 0)
        raise AssertionError("a col_index of 0 should have been rejected")
    except IndexError as exc:
        print(f"    VLOOKUP       {exc}")
    print(f"    XLOOKUP       {xlookup('E104', emp_ids, names)}")
    print(f"    INDEX+MATCH   {index_match('E104', emp_ids, names)}")
    assert xlookup("E104", emp_ids, names) == "Daniel Joseph"
    assert index_match("E104", emp_ids, names) == "Daniel Joseph"

    # --- difference 2: insert a column, and VLOOKUP lies --------------------
    # Somebody adds a "Grade" column between Department and Basic Pay. Nothing
    # errors. The VLOOKUP formula still says 4.
    widened_cols = columns[:3] + ["Grade"] + columns[3:]
    widened = [row[:3] + ["G" + row[1][-1]] + row[3:] for row in table]
    still_basic = column(widened, widened_cols, "Basic")

    broken = vlookup(key, widened, widened_cols, 4)
    print("\n  Someone inserts a 'Grade' column before Basic Pay:")
    print(f"    VLOOKUP(...,4)  now returns {broken!r}  "
          "<- the Grade, silently")
    print(f"    XLOOKUP         {xlookup(key, column(widened, widened_cols, 'Name'), still_basic):,}")
    print(f"    INDEX+MATCH     {index_match(key, column(widened, widened_cols, 'Name'), still_basic):,}")

    assert broken == "G4"          # not a number, not an error -- just wrong
    assert broken != 45000
    assert xlookup(key, column(widened, widened_cols, "Name"),
                   still_basic) == 45000
    assert index_match(key, column(widened, widened_cols, "Name"),
                       still_basic) == 45000

    print("\n  That is the viva answer: VLOOKUP's 4 is a position and the")
    print("  other two name a range, so only VLOOKUP breaks -- and it breaks")
    print("  without any error to warn you.")


if __name__ == "__main__":
    main()
