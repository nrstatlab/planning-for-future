"""Experiment 12: Demonstrate exception handling using try-except-finally.

Syllabus: Course 3, Unit 4 -- error and exception handling.
"""


class InvalidMarkError(Exception):
    """User-defined exception -- raised when a mark falls outside 0-100."""


def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print(f"  ZeroDivisionError caught: cannot divide {a} by zero")
        return None
    else:
        print(f"  else block: {a} / {b} = {result}")   # runs only if no error
        return result
    finally:
        print("  finally block: always runs, error or not")


print("1. ZeroDivisionError")
divide(10, 2)
divide(10, 0)

print("\n2. ValueError from a bad conversion")
for value in ("42", "abc"):
    try:
        print(f"  int({value!r}) = {int(value)}")
    except ValueError as exc:
        print(f"  ValueError caught: {exc}")

print("\n3. Catching several exception types")
for item in [[1, 2, 3], "hello", None]:
    try:
        print(f"  {item!r} -> first element {item[0]!r}")
    except TypeError as exc:
        print(f"  TypeError caught: {exc}")
    except IndexError as exc:
        print(f"  IndexError caught: {exc}")

print("\n4. FileNotFoundError")
try:
    with open("does_not_exist.txt") as fh:
        fh.read()
except FileNotFoundError as exc:
    print(f"  FileNotFoundError caught: {exc.strerror}")

print("\n5. raise -- signalling an error yourself")


def validate(mark):
    if not 0 <= mark <= 100:
        raise InvalidMarkError(f"{mark} is outside the valid range 0-100")
    return mark


for mark in (85, 150):
    try:
        print(f"  validate({mark}) = {validate(mark)}")
    except InvalidMarkError as exc:
        print(f"  InvalidMarkError caught: {exc}")

print("\n6. assert -- a sanity check that raises AssertionError")
try:
    scores = [80, 90]
    assert len(scores) > 0, "scores must not be empty"
    print(f"  assertion passed, average = {sum(scores) / len(scores)}")
    assert all(s <= 100 for s in scores + [120]), "every score must be <= 100"
except AssertionError as exc:
    print(f"  AssertionError caught: {exc}")
