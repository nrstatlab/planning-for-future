"""Experiment 9 (Python equivalent) -- dplyr/tidyr operations in pandas.

R version: ../09_wrangling.R
Every pandas call is annotated with its dplyr counterpart, which is the point
of this file: the two libraries do the same six things.
"""
import pandas as pd
from _shared import STUDENTS

COLS = ["name", "section", "gender", "hours", "marks", "attendance"]
df = pd.DataFrame(STUDENTS, columns=COLS)

if __name__ == "__main__":
    pd.set_option("display.width", 100)

    print("filter()   dplyr: filter(df, marks > 70)")
    print(df[df.marks > 70][["name", "section", "marks"]].to_string(index=False))

    print("\nselect()   dplyr: select(df, name, marks)")
    print(df[["name", "marks"]].head(3).to_string(index=False))

    print("\nmutate()   dplyr: mutate(df, grade = case_when(...))")
    df["grade"] = pd.cut(df.marks, bins=[0, 40, 60, 75, 90, 101],
                         labels=["F", "D", "C", "B", "A"], right=False)
    print(df[["name", "marks", "grade"]].head(5).to_string(index=False))

    print("\narrange()  dplyr: arrange(df, desc(marks))")
    print(df.sort_values("marks", ascending=False)[["name", "marks"]]
            .head(3).to_string(index=False))

    print("\ngroup_by + summarise")
    print("  dplyr: group_by(section) %>% summarise(n=n(), avg=mean(marks))")
    g = (df.groupby("section")
           .agg(n=("marks", "size"), avg=("marks", "mean"),
                highest=("marks", "max"),
                pass_pct=("marks", lambda s: (s >= 40).mean() * 100))
           .reset_index())
    print(g.to_string(index=False))

    print("\npivot_longer()  tidyr: pivot_longer(cols = c(hours, marks))")
    long = df.melt(id_vars=["name", "section"], value_vars=["hours", "marks"],
                   var_name="measure", value_name="value")
    print(long.head(4).to_string(index=False))
    print(f"  wide {df.shape} -> long {long.shape}")

    print("\npivot_wider()   tidyr: pivot_wider(names_from, values_from)")
    wide = long.pivot_table(index=["name", "section"], columns="measure",
                            values="value").reset_index()
    print(wide.head(3).to_string(index=False))

    assert len(long) == len(df) * 2, "melt must double the rows for two measures"
    assert set(g.section) == {"A", "B", "C"}
    print("\n  long form has 2x the rows, as pivot_longer would produce ✓")
