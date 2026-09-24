"""Experiment 4: Illustrate string slicing, concatenation, repetition and the
built-in string methods.

Syllabus: Course 3, Unit 3 -- strings.
"""

text = "Data Science Major"
print(f"text = {text!r}   (length {len(text)})")

print("\nINDEXING")
print(f"  text[0]   = {text[0]!r}    first character")
print(f"  text[-1]  = {text[-1]!r}    last character")

print("\nSLICING  text[start:stop:step]  -- stop is excluded")
print(f"  text[0:4]   = {text[0:4]!r}")
print(f"  text[5:12]  = {text[5:12]!r}")
print(f"  text[:4]    = {text[:4]!r}      start defaults to 0")
print(f"  text[13:]   = {text[13:]!r}     stop defaults to the end")
print(f"  text[::2]   = {text[::2]!r}   every second character")
print(f"  text[::-1]  = {text[::-1]!r}   reversed")

print("\nCONCATENATION and REPETITION")
print(f"  'Data' + ' ' + 'Science' = {'Data' + ' ' + 'Science'!r}")
print(f"  '-' * 20                 = {'-' * 20!r}")

print("\nMETHODS")
for call, result in (
    ("upper()",         text.upper()),
    ("lower()",         text.lower()),
    ("title()",         text.title()),
    ("split()",         text.split()),
    ("replace()",       text.replace("Major", "Minor")),
    ("find('Science')", text.find("Science")),
    ("count('a')",      text.count("a")),
    ("startswith('Data')", text.startswith("Data")),
    ("strip()",         "   padded   ".strip()),
    ("join()",          "-".join(["a", "b", "c"])),
):
    print(f"  {call:<20} -> {result!r}")

print("\nIMMUTABILITY -- strings cannot be changed in place")
try:
    text[0] = "X"
except TypeError as exc:
    print(f"  text[0] = 'X' raises TypeError: {exc}")
print("  build a new string instead:", "X" + text[1:])

print("\nTRAVERSAL and ACCUMULATION")
vowels = "".join(ch for ch in text if ch.lower() in "aeiou")
print(f"  vowels in text: {vowels!r}")
