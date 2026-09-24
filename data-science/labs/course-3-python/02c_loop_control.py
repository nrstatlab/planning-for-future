"""Experiment 2(c): Illustrate the loop control statements break, continue
and pass.

  break    -- leave the loop immediately
  continue -- skip the rest of this iteration, go to the next
  pass     -- do nothing; a syntactic placeholder where a statement is required

Syllabus: Course 3, Unit 2 -- loop control statements.
"""

print("break -- stop as soon as we reach 5")
for i in range(1, 11):
    if i == 5:
        break
    print(f"  {i}", end="")
print("\n")

print("continue -- skip the even numbers")
for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(f"  {i}", end="")
print("\n")

print("pass -- placeholder, the loop body does nothing for multiples of 3")
for i in range(1, 11):
    if i % 3 == 0:
        pass          # a branch we have not written yet; keeps the code valid
    else:
        print(f"  {i}", end="")
print("\n")

print("else with a loop -- runs only when the loop was NOT broken out of")
for i in range(1, 4):
    print(f"  iteration {i}")
else:
    print("  loop finished without a break")
