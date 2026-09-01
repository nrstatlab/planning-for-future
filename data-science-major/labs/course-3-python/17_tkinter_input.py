"""Experiment 17: A Tkinter program with Label, Entry and Button widgets that
takes user input and displays it.

Syllabus: Course 3, Unit 5 -- GUI programming with Tkinter.

NOT EXECUTED IN CI: this file was syntax-checked with `python3 -m py_compile`
only. tkinter is not installed in the environment these labs were verified in,
and a GUI needs a display in any case. Run it on your own machine with
`python3 17_tkinter_input.py`; tkinter ships with the standard Windows and
macOS Python installers, and is `sudo apt install python3-tk` on Debian/Ubuntu.
"""

import tkinter as tk
from tkinter import messagebox


class GreetingApp:
    def __init__(self, root):
        self.root = root
        root.title("Student Input Form")
        root.geometry("420x260")

        # ---- Labels and Entry widgets ----
        tk.Label(root, text="Student Details", font=("Arial", 14, "bold")
                 ).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(root, text="Name:").grid(row=1, column=0, sticky="e", padx=5,
                                          pady=5)
        self.name_entry = tk.Entry(root, width=25)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Roll number:").grid(row=2, column=0, sticky="e",
                                                 padx=5, pady=5)
        self.roll_entry = tk.Entry(root, width=25)
        self.roll_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Course:").grid(row=3, column=0, sticky="e",
                                            padx=5, pady=5)
        self.course_entry = tk.Entry(root, width=25)
        self.course_entry.grid(row=3, column=1, padx=5, pady=5)

        # ---- Buttons: `command` binds the handler (event handling) ----
        tk.Button(root, text="Submit", width=10, command=self.submit
                  ).grid(row=4, column=0, pady=15)
        tk.Button(root, text="Clear", width=10, command=self.clear
                  ).grid(row=4, column=1, pady=15)

        # ---- Output label, updated at run time ----
        self.output = tk.Label(root, text="", font=("Arial", 11), fg="darkblue",
                               wraplength=380, justify="left")
        self.output.grid(row=5, column=0, columnspan=2)

    def submit(self):
        """Event handler for the Submit button."""
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        course = self.course_entry.get().strip()

        if not name or not roll:
            messagebox.showwarning("Missing data",
                                   "Name and roll number are required")
            return

        self.output.config(
            text=f"Name   : {name}\nRoll   : {roll}\nCourse : {course}")

    def clear(self):
        """Event handler for the Clear button."""
        for entry in (self.name_entry, self.roll_entry, self.course_entry):
            entry.delete(0, tk.END)
        self.output.config(text="")


if __name__ == "__main__":
    window = tk.Tk()
    GreetingApp(window)
    window.mainloop()          # starts the event loop; blocks until closed
