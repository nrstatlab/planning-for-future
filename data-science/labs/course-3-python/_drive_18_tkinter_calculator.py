"""Drives 18_tkinter_calculator.py the way a student would use it, and checks what it shows.

Run by tools/data-science/capture_lab_outputs.py under a virtual display (xvfb-run). The
program is loaded, not run as the main program, so its mainloop() never starts; the driver
presses the calculator's real Button widgets with invoke() and reads the display after each
calculation, with a screenshot.
"""
import importlib.util
import pathlib
import subprocess
import tkinter as tk

spec = importlib.util.spec_from_file_location("calc", "18_tkinter_calculator.py")
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)            # __name__ is not "__main__", so no mainloop()

root = tk.Tk()
app = calc.Calculator(root)
root.geometry("+0+0")              # where it opens; its size is its own
keys = {w.cget("text"): w for w in root.winfo_children() if isinstance(w, tk.Button)}
shots = 0


def press(sequence):
    for key in sequence:
        keys[key].invoke()
    return app.display.get()


def screenshot(what):
    global shots
    root.update()
    root.after(300)
    root.update()
    shots += 1
    size = f"{root.winfo_width()}x{root.winfo_height()}+0+0"   # the window as it really is
    subprocess.run(["import", "-window", "root", "-crop", size, "+repage",
                    str(pathlib.Path("screens") / f"{shots}.png")], check=True)
    print(f"  [screenshot {shots}: {what}]")


for sequence, expected, what in (
        ("12+7*3=", "33", "precedence: * before +"),
        ("C(12+7)*3=", "57", "brackets first"),
        ("C7/2=", "3.5", "true division"),
        ("C8/0=", "Cannot divide by zero", "division by zero, caught"),
        ("C2**3=", "8", "** is two * keys, so the character check lets it through"),
        ("C9<<=", "", "< deletes, so 9 then two deletes leaves nothing to evaluate")):
    shown = press(sequence)
    print(f"press {' '.join(sequence)}   display: {shown!r}   ({what})")
    assert shown == expected, (sequence, shown)
    if expected in ("33", "Cannot divide by zero"):
        screenshot(f"after {sequence}")

# The character check: anything but digits, operators, brackets, a point and a space is refused
# before eval() is reached -- the buttons cannot type a letter, so it is tested directly.
app.expression = "__import__('os')"
app.evaluate()
print(f"\nan expression with letters, set directly: display {app.display.get()!r}")
assert app.display.get() == "Error"
root.destroy()
