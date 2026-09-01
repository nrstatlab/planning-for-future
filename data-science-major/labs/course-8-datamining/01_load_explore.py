"""Experiment 1 — Load datasets and explore ARFF/CSV formats.

WEKA equivalent: Preprocess tab -> Open file (see lab.md).
This prints the same summary WEKA's attribute panel shows, so you can compare.
"""
import io
import pandas as pd
from weather import weather_frame, ARFF


def parse_arff(text):
    """A minimal ARFF reader -- enough to show the format's structure.

    Real work uses scipy.io.arff or liac-arff; this exists so the format is
    legible rather than magic.
    """
    attributes, rows, in_data = [], [], False
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("%"):
            continue
        low = line.lower()
        if low.startswith("@attribute"):
            parts = line.split(None, 2)
            name, spec = parts[1], parts[2].strip()
            if spec.startswith("{"):
                kind, domain = "nominal", [v.strip() for v in spec.strip("{}").split(",")]
            else:
                kind, domain = spec.lower(), None
            attributes.append((name, kind, domain))
        elif low.startswith("@data"):
            in_data = True
        elif in_data:
            rows.append([None if v.strip() == "?" else v.strip()
                         for v in line.split(",")])
    return attributes, pd.DataFrame(rows, columns=[a[0] for a in attributes])


def describe(df, name):
    """What WEKA's Preprocess panel reports."""
    print(f"  {name}: {len(df)} instances, {len(df.columns)} attributes")
    for col in df.columns:
        missing = int(df[col].isna().sum())
        if pd.api.types.is_numeric_dtype(df[col]):
            print(f"    {col:14s} numeric  min={df[col].min():g} max={df[col].max():g} "
                  f"mean={df[col].mean():.4f} sd={df[col].std():.4f} missing={missing}")
        else:
            counts = df[col].value_counts().to_dict()
            print(f"    {col:14s} nominal  {counts} missing={missing}")


def main():
    print("Experiment 1 -- Load and explore")

    attributes, df = parse_arff(ARFF)
    assert len(df) == 14, "weather.nominal has 14 instances"
    assert len(attributes) == 5, "and 5 attributes"
    assert all(a[1] == "nominal" for a in attributes), "all five are nominal"
    assert attributes[-1][0] == "play", "the LAST attribute is the class by default"
    describe(df, "weather.nominal.arff")

    # Round-trip through CSV, which is how WEKA imports non-ARFF data.
    csv = df.to_csv(index=False)
    back = pd.read_csv(io.StringIO(csv))
    assert back.equals(df), "CSV round-trip must preserve the data"

    # The trap from lab.md: a numeric-looking CATEGORY.
    df2 = weather_frame()
    df2["ClassID"] = [101, 102, 103] * 4 + [104, 105]
    assert pd.api.types.is_integer_dtype(df2.ClassID), \
        "read as numeric -- every algorithm would treat it as a MAGNITUDE"
    df2["ClassID"] = df2.ClassID.astype("category")
    assert isinstance(df2.ClassID.dtype, pd.CategoricalDtype), \
        "NumericToNominal is the WEKA filter that fixes this"
    print("  numeric-looking category converted (WEKA: NumericToNominal)")
    print("  format checks passed")


if __name__ == "__main__":
    main()
