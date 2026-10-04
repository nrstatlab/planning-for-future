"""Experiment 18: A simple calculator application in Tkinter.

Syllabus: Course 3, Unit 5 -- GUI programming with Tkinter.

Run for the lab page under a virtual display (xvfb-run) by
_drive_18_tkinter_calculator.py, which presses its buttons and asserts what the display
shows. Run it locally with `python3 18_tkinter_calculator.py`.

Note on eval(): this uses a restricted eval with the character set validated
first. eval() on unfiltered user input is a security hole -- never do it in a
real application.
"""

import tkinter as tk

ALLOWED = set("0123456789+-*/(). ")


class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.geometry("300x380")
        root.resizable(False, False)

        self.expression = ""

        # Step 1: The display and the buttons
        self.display = tk.Entry(root, font=("Arial", 20), justify="right",
                                bd=8, relief="sunken")
        self.display.grid(row=0, column=0, columnspan=4, sticky="we",
                          padx=5, pady=10, ipady=8)

        buttons = [
            ("C", 1, 0), ("(", 1, 1), (")", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("<", 5, 2), ("=", 5, 3),
        ]

        for text, row, col in buttons:
            tk.Button(root, text=text, font=("Arial", 15), width=4, height=2,
                      command=lambda t=text: self.on_click(t)
                      ).grid(row=row, column=col, padx=3, pady=3)

    # Step 2: One handler for every button
    def on_click(self, key):
        """Single event handler for every button."""
        if key == "C":
            self.expression = ""
        elif key == "<":
            self.expression = self.expression[:-1]
        elif key == "=":
            self.evaluate()
            return
        else:
            self.expression += key
        self.refresh()

    # Step 3: Evaluate, safely
    def evaluate(self):
        if not self.expression:
            return
        if not set(self.expression) <= ALLOWED:
            self.show("Error")
            self.expression = ""
            return
        try:
            # Empty globals/builtins: nothing but arithmetic can be reached.
            result = eval(self.expression, {"__builtins__": {}}, {})
            self.expression = str(result)
        except ZeroDivisionError:
            self.expression = ""
            self.show("Cannot divide by zero")
            return
        except (SyntaxError, NameError, TypeError):
            self.expression = ""
            self.show("Error")
            return
        self.refresh()

    def refresh(self):
        self.show(self.expression)

    def show(self, text):
        self.display.delete(0, tk.END)
        self.display.insert(0, text)


if __name__ == "__main__":
    # Step 4: Start the event loop
    window = tk.Tk()
    Calculator(window)
    window.mainloop()
