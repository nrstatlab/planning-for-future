"""Experiment 11 (Python equivalent) -- working with dates.

R version: ../11_dates.R  (as.Date, format, lubridate)
"""
from datetime import date, datetime, timedelta

if __name__ == "__main__":
    print("PARSING                        R: as.Date('2026-08-26')")
    d = date.fromisoformat("2026-08-26")
    print(f"  ISO         '2026-08-26' -> {d}")
    d2 = datetime.strptime("26/08/2026", "%d/%m/%Y").date()
    print(f"  DD/MM/YYYY  '26/08/2026' -> {d2}   R: format='%d/%m/%Y'")
    print(f"  same date: {d == d2}")

    print("\nCOMPONENTS                     R: lubridate::year(), month(), day()")
    print(f"  year={d.year}  month={d.month}  day={d.day}")
    print(f"  weekday       = {d.strftime('%A')}   R: wday(d, label=TRUE)")
    print(f"  day of year   = {d.timetuple().tm_yday}")
    print(f"  ISO week      = {d.isocalendar().week}")

    print("\nARITHMETIC                     R: d + 30 ; difftime()")
    print(f"  d + 30 days   = {d + timedelta(days=30)}")
    print(f"  d - 7 days    = {d - timedelta(days=7)}")
    later = date.fromisoformat("2026-12-25")
    print(f"  days to {later} = {(later - d).days}")

    print("\nFORMATTING                     R: format(d, '%d %B %Y')")
    for fmt, label in (("%d-%m-%Y", "DD-MM-YYYY"), ("%d %B %Y", "long"),
                       ("%b %d, %Y", "abbreviated"), ("%Y-%m-%d", "ISO")):
        print(f"  {label:<12} {d.strftime(fmt)}")

    print("\nWHY DATES MUST NOT BE STRINGS")
    as_text = ["10/01/2026", "02/01/2026", "21/12/2025"]
    as_dates = [datetime.strptime(x, "%d/%m/%Y").date() for x in as_text]
    print(f"  sorted as text : {sorted(as_text)}")
    print(f"  sorted as dates: {[str(x) for x in sorted(as_dates)]}")
    print("  Text sorting puts 02/01 before 10/01 before 21/12 -- alphabetical,")
    print("  not chronological. The 2025 date ends up LAST. This is exactly the")
    print("  bug that makes date columns stored as VARCHAR dangerous (Course 5).")

    assert sorted(as_dates)[0].year == 2025, "chronological order must start in 2025"
    assert sorted(as_text)[0].startswith("02"), "text order must start with 02"
    print("\n  demonstrated: text order and date order genuinely differ ✓")
