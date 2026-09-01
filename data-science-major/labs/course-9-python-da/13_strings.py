"""Practical 13 — String operations and regular expressions on DataFrames."""
import numpy as np
import pandas as pd


def str_accessor_handles_nan():
    s = pd.Series(["  Asha Kumari ", "RAVI TEJA", "meena devi", None])

    assert s.str.len().tolist()[:3] == [14.0, 9.0, 10.0]
    assert s.str.len().dtype == np.float64, "NaN forces float, as in Unit 3"
    assert s.str.strip().str.len().tolist()[:1] == [11.0]

    assert s.str.lower().isna().sum() == 1
    assert s.str.strip().str.title().iloc[0] == "Asha Kumari"

    try:
        s.apply(str.lower)
        raise AssertionError("expected TypeError")
    except TypeError:
        pass

    print("  .str skips NaN (and returns float64 for len); .apply(str.lower) crashes")


def splitting():
    names = pd.Series(["Asha Kumari", "Ravi Teja", "Meena Devi"])

    assert names.str.split(" ").iloc[0] == ["Asha", "Kumari"]
    cols = names.str.split(" ", expand=True)
    assert cols.shape == (3, 2)
    assert cols[0].tolist() == ["Asha", "Ravi", "Meena"]
    assert cols[1].tolist() == ["Kumari", "Teja", "Devi"]

    assert names.str.split(" ").str[0].tolist() == ["Asha", "Ravi", "Meena"]
    assert names.str.cat(sep=", ").startswith("Asha Kumari, Ravi")
    assert names.str[0].tolist() == ["A", "R", "M"]
    assert names.str[-4:].tolist() == ["mari", "Teja", "Devi"]

    print("  split(expand=True) -> columns; .str[0] and .str[-4:] slice characters")


def extracting_a_roll_number():
    rolls = pd.Series(["23DSC0145", "24STA0067", "23DSC0198"])

    p = rolls.str.extract(r"(?P<year>\d{2})(?P<branch>[A-Z]{3})(?P<number>\d{4})")
    assert list(p.columns) == ["year", "branch", "number"], "NAMED groups -> names"
    assert p.year.tolist() == ["23", "24", "23"]
    assert p.branch.tolist() == ["DSC", "STA", "DSC"]
    assert p.number.iloc[0] == "0145", "extract returns STRINGS -- the zero survives"

    assert p.number.astype(int).iloc[0] == 145, "converting LOSES the leading zero"

    # A row that does not match yields NaN rather than being dropped -- so you
    # can find the malformed identifiers instead of losing them silently.
    with_bad = pd.concat([rolls, pd.Series(["BADROLL"])], ignore_index=True)
    q = with_bad.str.extract(r"(?P<year>\d{2})(?P<branch>[A-Z]{3})(?P<number>\d{4})")
    assert q.year.isna().sum() == 1
    assert len(q) == 4, "the row is KEPT, with NaN -- inspect it, do not drop it"

    print("  extract with named groups -> labelled columns; '0145' keeps its zero")
    print("       a non-matching row yields NaN and is KEPT, so you can find it")


def extract_findall_extractall():
    s = pd.Series(["Asha 23 DS", "Ravi 24 Stats"])

    first = s.str.extract(r"(\d+)")
    assert isinstance(first, pd.DataFrame) and first.shape == (2, 1), "FIRST match, a frame"

    every = s.str.findall(r"\d")
    assert every.iloc[0] == ["2", "3"], "ALL matches, as a LIST per row"

    allrows = s.str.extractall(r"(\d)")
    assert len(allrows) == 4, "ALL matches, as ROWS with a MultiIndex"
    assert allrows.index.nlevels == 2

    print("  extract -> first match as a frame; findall -> lists; extractall -> rows")


def contains_depends_on_dtype():
    """Verified on Pandas 3.0.5 -- and the reason to pass na=False anyway."""
    new = pd.Series(["abc", None])                       # Pandas 3 default: str
    assert new.str.contains("a").dtype == np.bool_ or \
        str(new.str.contains("a").dtype) == "bool"
    assert new[new.str.contains("a")].tolist() == ["abc"], "masking WORKS"

    old = pd.Series(["abc", None], dtype="object")
    mask = old.str.contains("a")
    assert str(mask.dtype) == "object", "object dtype -> object mask with None"
    try:
        old[mask]
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    assert old[old.str.contains("a", na=False)].tolist() == ["abc"]

    print("  str dtype -> bool mask, masking works; object dtype -> raises")
    print("       pass na=False anyway: you will not always know the dtype")


def replace_needs_regex_stated():
    s = pd.Series(["a.b.c", "x.y.z"])

    literal = s.str.replace(".", "", regex=False)
    assert literal.tolist() == ["abc", "xyz"], "literal dot removed"

    everything = s.str.replace(".", "", regex=True)
    assert everything.tolist() == ["", ""], "'.' matches ANY character"

    escaped = s.str.replace(r"\.", "", regex=True)
    assert escaped.tolist() == ["abc", "xyz"]

    print("  replace('.', '', regex=True) deletes EVERY character -- escape it")


def validation_patterns():
    emails = pd.Series(["asha@nri.ac.in", "bad@", "x@y.io"])
    ok = emails.str.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]{2,}")
    assert ok.tolist() == [True, False, True]

    phones = pd.Series(["9876543210", "1234567890", "98765"])
    assert phones.str.fullmatch(r"[6-9]\d{9}").tolist() == [True, False, False]

    print("  fullmatch anchors the whole string -- the right tool for validation")


def main():
    print("Practical 13 -- Strings and regular expressions")
    str_accessor_handles_nan()
    splitting()
    extracting_a_roll_number()
    extract_findall_extractall()
    contains_depends_on_dtype()
    replace_needs_regex_stated()
    validation_patterns()


if __name__ == "__main__":
    main()
