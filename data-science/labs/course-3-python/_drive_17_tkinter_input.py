"""Drives 17_tkinter_input.py the way a student would use it, and checks what it shows.

Run by tools/data-science/capture_lab_outputs.py under a virtual display (xvfb-run), so the
lab page can show the window as it really looked. The program is loaded, not run as the main
program, so its mainloop() never starts; the driver then types into each Entry, presses the
real Button widgets with invoke(), and saves a screenshot after each action. The warning
dialog is replaced by a recorder, because a modal dialog would wait for a click forever.
"""
import importlib.util
import pathlib
import subprocess
import tkinter as tk

spec = importlib.util.spec_from_file_location("form", "17_tkinter_input.py")
form = importlib.util.module_from_spec(spec)
spec.loader.exec_module(form)            # __name__ is not "__main__", so no mainloop()

warnings = []
form.messagebox.showwarning = lambda title, message: warnings.append((title, message))

root = tk.Tk()
app = form.GreetingApp(root)
root.geometry("+0+0")              # where it opens; its size is its own
buttons = {w.cget("text"): w for w in root.winfo_children() if isinstance(w, tk.Button)}
shots = 0


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


def type_into(entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)


print("Fill in the form and press Submit:")
for entry, label, text in ((app.name_entry, "Name", "Ananya"), (app.roll_entry, "Roll number", "24001"),
                           (app.course_entry, "Course", "B.Sc. Data Science")):
    type_into(entry, text)
    print(f"  typed {text!r} into {label}")
buttons["Submit"].invoke()
shown = app.output.cget("text")
print("  the output label now reads:")
for line in shown.split("\n"):
    print("    " + line)
assert shown == "Name   : Ananya\nRoll   : 24001\nCourse : B.Sc. Data Science", shown
screenshot("after Submit")

print("\nPress Clear:")
buttons["Clear"].invoke()
left = [e.get() for e in (app.name_entry, app.roll_entry, app.course_entry)]
print(f"  the three entries now hold {left}, and the output label {app.output.cget('text')!r}")
assert left == ["", "", ""] and app.output.cget("text") == ""
screenshot("after Clear")

print("\nPress Submit with the name left empty:")
type_into(app.roll_entry, "24002")
buttons["Submit"].invoke()
print(f"  a warning appears: {warnings[-1][0]!r} -- {warnings[-1][1]!r}")
assert warnings == [("Missing data", "Name and roll number are required")]
assert app.output.cget("text") == "", "nothing should be shown for an incomplete form"
print("  and the output label stays empty")
root.destroy()
