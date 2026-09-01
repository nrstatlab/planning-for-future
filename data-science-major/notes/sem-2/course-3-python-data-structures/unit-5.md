# Unit 5 — Abstract Data Structures and GUI Programming

**Syllabus topics:** Abstract Data Structures (ADTs) — concepts and
importance. Linked list — definition, types (singly, doubly, circular), node
structure, insertion, deletion, traversal (**singly linked list implementation
only**). Stacks — LIFO principle, implementation using a list, applications.
Queues — FIFO principle, implementation using a list, priority queues. GUI
programming with Tkinter — widgets (Label, Button, Entry, Menu, Listbox,
Canvas, etc.), event handling, building simple GUI apps.

---

> **This unit contains two unrelated subjects.** Data structures are
> algorithmic and carry most of the theory marks; Tkinter is applied and
> carries the lab marks (2 of the 18 lab programs). They share nothing. See
> [`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D7**.
>
> This file is split accordingly. Study Part A and Part B as separate topics.

---

# Part A — Abstract Data Structures

## A.1 What an ADT is

An **Abstract Data Type** specifies *what* operations a data structure supports
and what they mean, without saying *how* they are implemented.

A **Stack ADT** is defined by `push`, `pop`, `peek`, `is_empty` and the LIFO
rule. Whether you build it from a Python list, a linked list or an array is an
implementation detail the user never has to know.

**Why it matters:** the separation lets you swap implementations without
changing any code that uses the structure. Python's own `list` is an ADT whose
implementation (a dynamic array) you never see.

| ADT | Core operations | Rule |
|---|---|---|
| Stack | push, pop, peek | LIFO |
| Queue | enqueue, dequeue, front | FIFO |
| List | insert, delete, traverse, search | positional |
| Priority queue | enqueue, dequeue | by priority, not arrival |

## A.2 Linked lists

A **linked list** is a chain of **nodes**. Each node holds data and a reference
to the next node.

```
head
 |
 v
+------+------+    +------+------+    +------+------+
| 10   |  o---+--->| 20   |  o---+--->| 30   | None |
+------+------+    +------+------+    +------+------+
 data   next        data   next        data   next
```

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

### Types

| Type | Structure |
|---|---|
| **Singly** | Each node points to the next; the last points to `None` |
| **Doubly** | Each node points both forwards and backwards |
| **Circular** | The last node points back to the first |

The syllabus requires **implementation of the singly linked list only** —
define the other two and describe them, but you are not asked to code them.

### Operations

```python
class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):     # O(1)
        node = Node(data)
        node.next = self.head
        self.head = node

    def insert_at_end(self, data):           # O(n) -- must walk to the end
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def delete(self, target):                # O(n)
        current, previous = self.head, None
        while current:
            if current.data == target:
                if previous is None:         # deleting the head
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous, current = current, current.next
        return False

    def traverse(self):                      # O(n)
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
```

**Deleting the head is the special case** every exam tests. When `previous` is
`None` you must move `self.head`, not `previous.next`.

Full implementation, including reversal:
`16_linked_list.py`.

### Linked list vs array/list

| | Array / Python list | Linked list |
|---|---|---|
| Memory | Contiguous | Scattered, joined by references |
| Access by index | **O(1)** | O(n) — walk from the head |
| Insert at beginning | O(n) — shift everything | **O(1)** |
| Insert at end | O(1) amortised | O(n), or O(1) with a tail pointer |
| Memory overhead | None | One reference per node |
| Size | Resizes by reallocating | Grows one node at a time |

**When to use which:** a linked list wins when you insert and delete at the
front often and rarely need random access. Otherwise a list is usually better —
and in Python, `collections.deque` gives O(1) at both ends.

## A.3 Stacks

**LIFO — Last In, First Out.** Like a stack of plates: the last one placed is
the first one taken.

```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)              # O(1)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack underflow")
        return self.items.pop()              # O(1)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
```

**Underflow** is popping from an empty stack; **overflow** is pushing onto a
full one (only meaningful for a fixed-size implementation).

### Applications — a guaranteed exam question

1. **Function call management** — the call stack; how recursion works
2. **Expression evaluation** — infix to postfix conversion, postfix evaluation
3. **Balanced bracket checking** — `{[()]}`
4. **Undo/redo** in editors
5. **Backtracking** — maze solving, browser back button
6. **Depth-first search** in graphs

### Balanced brackets — the standard worked example

```python
def balanced(expression):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in expression:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return len(stack) == 0        # anything left over is unclosed
```

`{[()]}` → True. `{[(])}` → False. `(((` → False, because the stack is not
empty at the end.

## A.4 Queues

**FIFO — First In, First Out.** Like a queue at a counter.

```python
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)              # join at the rear -- O(1)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue underflow")
        return self.items.pop(0)             # leave from the front -- O(n)!

    def front(self):
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0
```

**`pop(0)` is O(n)** — every remaining element shifts down one place. For a
real program use `collections.deque`, whose `popleft()` is O(1):

```python
from collections import deque
q = deque()
q.append(1)          # enqueue
q.popleft()          # dequeue -- O(1)
```

The syllabus asks for the list implementation, so write that in the exam, but
mentioning the `deque` alternative and *why* shows understanding.

### Types of queue

| Type | Description |
|---|---|
| **Simple queue** | Plain FIFO |
| **Circular queue** | The rear wraps around to reuse freed space |
| **Priority queue** | Highest priority leaves first, regardless of arrival |
| **Double-ended (deque)** | Insert and delete at both ends |

### Priority queue

```python
class PriorityQueue:
    def __init__(self):
        self.items = []                      # list of (priority, value)

    def enqueue(self, value, priority):
        self.items.append((priority, value))
        self.items.sort(key=lambda pair: pair[0])   # lowest number first

    def dequeue(self):
        if not self.items:
            raise IndexError("priority queue is empty")
        return self.items.pop(0)[1]
```

The classic example is a hospital emergency room: a heart attack arriving after
a routine checkup is still seen first.

This implementation is O(n log n) per insertion because it re-sorts. A real one
uses a **heap** — Python's `heapq` module — giving O(log n). Worth a sentence
in a long answer.

### Applications of queues

1. **CPU and disk scheduling**
2. **Printer job queues**
3. **Breadth-first search** in graphs
4. **Call-centre systems**
5. **Buffering** — keyboard input, network packets

### Stack vs queue

| | Stack | Queue |
|---|---|---|
| Principle | LIFO | FIFO |
| Insert at | Top | Rear |
| Remove from | Top | Front |
| Pointers needed | One (top) | Two (front, rear) |
| Operations | push, pop | enqueue, dequeue |
| Used in | Recursion, undo, DFS | Scheduling, buffering, BFS |

Full implementations of all of these:
`15_stack_queue.py`.

---

# Part B — GUI Programming with Tkinter

Tkinter is Python's standard GUI library. It ships with Python, so nothing
needs installing (on Debian/Ubuntu Linux it is a separate package,
`python3-tk`).

## B.1 The minimal program

```python
import tkinter as tk

window = tk.Tk()                     # the main window
window.title("My Application")
window.geometry("400x300")           # width x height in pixels

label = tk.Label(window, text="Hello, Tkinter!")
label.pack()

window.mainloop()                    # start the event loop -- BLOCKS here
```

**`mainloop()` must be the last line.** It hands control to Tkinter, which then
waits for events. Anything written after it does not run until the window
closes.

## B.2 Widgets

| Widget | Purpose |
|---|---|
| `Label` | Display static text or an image |
| `Button` | A clickable button, bound to a handler |
| `Entry` | Single-line text input |
| `Text` | Multi-line text input |
| `Listbox` | A list of selectable items |
| `Checkbutton` | An on/off tick box |
| `Radiobutton` | One choice from several |
| `Canvas` | Freeform drawing — lines, shapes, images |
| `Frame` | A container for grouping widgets |
| `Menu` | A menu bar |
| `Scrollbar` | Scrolling for another widget |
| `messagebox` | Pop-up dialogs (from `tkinter.messagebox`) |

## B.3 Geometry managers

Three ways to place widgets. **Never mix them within the same container** — the
result is undefined and typically a blank window.

```python
widget.pack()                                  # stacks vertically or by side
widget.pack(side="left", padx=5, pady=5)

widget.grid(row=0, column=1, sticky="e")       # a table -- best for forms

widget.place(x=50, y=100)                      # absolute pixels -- avoid
```

| Manager | Best for |
|---|---|
| `pack` | Simple vertical or horizontal stacking |
| `grid` | Forms and anything table-shaped — **the usual choice** |
| `place` | Precise positioning; does not adapt to resizing |

## B.4 Event handling

The `command` parameter binds a function to a button:

```python
def on_click():
    name = entry.get()                 # read the Entry widget
    label.config(text=f"Hello, {name}!")   # update the Label

button = tk.Button(window, text="Submit", command=on_click)
```

**Pass the function, do not call it.** `command=on_click` is correct;
`command=on_click()` calls it immediately at startup and binds the *result*.

To pass arguments, use a lambda:

```python
tk.Button(window, text="7", command=lambda: press("7"))
```

### `bind()` for other events

```python
widget.bind("<Button-1>", handler)      # left mouse click
widget.bind("<Return>", handler)        # Enter key
widget.bind("<KeyPress>", handler)      # any key
```

Handlers bound this way receive an `event` object as their argument.

## B.5 Reading and writing widgets

```python
value = entry.get()                     # read an Entry
entry.delete(0, tk.END)                 # clear it
entry.insert(0, "default text")         # set it

label.config(text="new text")           # update a Label

listbox.insert(tk.END, "item")
listbox.get(listbox.curselection())     # the selected item
```

## B.6 A complete example

```python
import tkinter as tk
from tkinter import messagebox


class GreetingApp:
    def __init__(self, root):
        root.title("Greeting")

        tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry = tk.Entry(root)
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(root, text="Greet", command=self.greet
                  ).grid(row=1, column=0, columnspan=2, pady=10)

        self.output = tk.Label(root, text="")
        self.output.grid(row=2, column=0, columnspan=2)

    def greet(self):
        name = self.entry.get().strip()
        if not name:
            messagebox.showwarning("Missing", "Please enter a name")
            return
        self.output.config(text=f"Hello, {name}!")


window = tk.Tk()
GreetingApp(window)
window.mainloop()
```

Wrapping the GUI in a class keeps the widgets and their handlers together, and
demonstrates the OOP from Unit 4 — examiners like seeing the two connected.

Full programs:
`17_tkinter_input.py` and
`18_tkinter_calculator.py`.

> Both were **syntax-checked but not executed** in this repository's
> verification, because `tkinter` is not installed in that environment and a
> GUI needs a display. Run them on your own machine.

---

## Exam questions from this unit

**Two marks**

1. What is an abstract data type?
2. State the LIFO and FIFO principles.
3. What is stack underflow?
4. Why is `pop(0)` inefficient for a queue?
5. Name any five Tkinter widgets.
6. What does `mainloop()` do?

**Five marks**

1. Explain the node structure of a singly linked list and write the insertion
   operation.
2. Explain stack operations with a Python implementation.
3. Compare a stack and a queue.
4. Explain the three Tkinter geometry managers.
5. Explain a priority queue with an implementation and a real example.

**Ten marks**

1. Implement a singly linked list with insertion, deletion, search and
   traversal, and explain each operation.
2. Explain stacks and queues fully — principles, implementations, operations
   and applications.
3. Write a Tkinter application with Label, Entry and Button widgets, and
   explain event handling.

## Mistakes that cost marks

- Forgetting the head-deletion special case in a linked list
- Losing the rest of the chain by reassigning `next` in the wrong order
- Not checking for an empty stack or queue before popping
- Writing `command=on_click()` instead of `command=on_click`
- Mixing `pack()` and `grid()` in the same container
- Putting code after `mainloop()` and expecting it to run
- Claiming a linked list gives O(1) access by index — it does not
