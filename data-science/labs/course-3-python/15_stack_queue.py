"""Experiment 15: Implement a stack (LIFO) and a queue (FIFO) using both lists
and linked lists.

Syllabus: Course 3, Unit 5 -- stacks, queues, priority queues.
"""

# --------------------------------------------------------------------------
# STACK using a Python list
# --------------------------------------------------------------------------


class StackList:
    """LIFO -- Last In, First Out. Think of a stack of plates."""

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)          # add at the top

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty stack (stack underflow)")
        return self.items.pop()          # remove from the top

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# --------------------------------------------------------------------------
# QUEUE using a Python list
# --------------------------------------------------------------------------


class QueueList:
    """FIFO -- First In, First Out. Think of a queue at a counter."""

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)          # join at the rear

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from an empty queue (queue underflow)")
        return self.items.pop(0)         # leave from the front

    def front(self):
        if self.is_empty():
            raise IndexError("front of an empty queue")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# --------------------------------------------------------------------------
# STACK using a linked list -- push/pop at the head, both O(1)
# --------------------------------------------------------------------------


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class StackLinked:
    def __init__(self):
        self.top = None
        self.count = 0

    def push(self, item):
        node = Node(item)
        node.next = self.top
        self.top = node
        self.count += 1

    def pop(self):
        if self.top is None:
            raise IndexError("stack underflow")
        node = self.top
        self.top = node.next
        self.count -= 1
        return node.data

    def is_empty(self):
        return self.top is None

    def display(self):
        values, current = [], self.top
        while current:
            values.append(str(current.data))
            current = current.next
        return "top -> " + " -> ".join(values) if values else "top -> (empty)"


# --------------------------------------------------------------------------
# QUEUE using a linked list -- enqueue at rear, dequeue at front, both O(1)
# --------------------------------------------------------------------------


class QueueLinked:
    def __init__(self):
        self.front_node = None
        self.rear_node = None
        self.count = 0

    def enqueue(self, item):
        node = Node(item)
        if self.rear_node is None:
            self.front_node = self.rear_node = node
        else:
            self.rear_node.next = node
            self.rear_node = node
        self.count += 1

    def dequeue(self):
        if self.front_node is None:
            raise IndexError("queue underflow")
        node = self.front_node
        self.front_node = node.next
        if self.front_node is None:      # the queue is now empty
            self.rear_node = None
        self.count -= 1
        return node.data

    def display(self):
        values, current = [], self.front_node
        while current:
            values.append(str(current.data))
            current = current.next
        return "front -> " + " -> ".join(values) if values else "front -> (empty)"


# --------------------------------------------------------------------------
# PRIORITY QUEUE -- the item with the smallest priority number leaves first
# --------------------------------------------------------------------------


class PriorityQueue:
    def __init__(self):
        self.items = []                  # list of (priority, value) tuples

    def enqueue(self, value, priority):
        self.items.append((priority, value))
        self.items.sort(key=lambda pair: pair[0])

    def dequeue(self):
        if not self.items:
            raise IndexError("priority queue is empty")
        return self.items.pop(0)[1]

    def display(self):
        return ", ".join(f"{v}(p{p})" for p, v in self.items) or "(empty)"


if __name__ == "__main__":
    print("STACK using a list -- LIFO")
    st = StackList()
    for item in (10, 20, 30):
        st.push(item)
        print(f"  push({item}) -> {st.items}")
    print(f"  peek()    = {st.peek()}")
    print(f"  pop()     = {st.pop()}  -> {st.items}")
    print(f"  pop()     = {st.pop()}  -> {st.items}")

    print("\nQUEUE using a list -- FIFO")
    q = QueueList()
    for item in ("A", "B", "C"):
        q.enqueue(item)
        print(f"  enqueue({item}) -> {q.items}")
    print(f"  front()    = {q.front()}")
    print(f"  dequeue()  = {q.dequeue()} -> {q.items}")
    print(f"  dequeue()  = {q.dequeue()} -> {q.items}")

    print("\nSTACK using a linked list")
    sl = StackLinked()
    for item in (1, 2, 3):
        sl.push(item)
        print(f"  push({item}) -> {sl.display()}")
    print(f"  pop()   = {sl.pop()}   -> {sl.display()}")

    print("\nQUEUE using a linked list")
    ql = QueueLinked()
    for item in ("X", "Y", "Z"):
        ql.enqueue(item)
        print(f"  enqueue({item}) -> {ql.display()}")
    print(f"  dequeue() = {ql.dequeue()} -> {ql.display()}")

    print("\nPRIORITY QUEUE -- lower number means higher priority")
    pq = PriorityQueue()
    for value, priority in (("routine checkup", 3), ("heart attack", 1),
                            ("fracture", 2)):
        pq.enqueue(value, priority)
        print(f"  enqueue({value!r}, p{priority}) -> {pq.display()}")
    print(f"  dequeue() = {pq.dequeue()!r}")
    print(f"  dequeue() = {pq.dequeue()!r}")

    print("\nUNDERFLOW is an error, not a silent None")
    try:
        StackList().pop()
    except IndexError as exc:
        print(f"  {exc}")

    print("\nAPPLICATION OF A STACK: balanced-bracket checking")

    def balanced(expression):
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = StackList()
        for ch in expression:
            if ch in "([{":
                stack.push(ch)
            elif ch in pairs:
                if stack.is_empty() or stack.pop() != pairs[ch]:
                    return False
        return stack.is_empty()

    for expr in ("{[()]}", "{[(])}", "((("):
        print(f"  {expr:<10} balanced? {balanced(expr)}")
