"""Experiment 16: Implement a singly linked list -- node creation, insertion,
deletion and traversal.

The syllabus (Unit 5) names singly, doubly and circular linked lists but says
"Single Linked list implementation only", so that is what is implemented here.

Syllabus: Course 3, Unit 5 -- linked lists.
"""


class Node:
    """One link in the chain: a value, plus a reference to the next node."""

    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    # ---------------- INSERTION ----------------

    def insert_at_beginning(self, data):
        """O(1) -- the cheapest insertion."""
        node = Node(data)
        node.next = self.head
        self.head = node

    def insert_at_end(self, data):
        """O(n) -- must walk to the last node first."""
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    def insert_after(self, target, data):
        """Insert immediately after the first node holding `target`."""
        current = self.head
        while current:
            if current.data == target:
                node = Node(data)
                node.next = current.next
                current.next = node
                return True
            current = current.next
        return False

    # ---------------- DELETION ----------------

    def delete(self, target):
        """Delete the first node holding `target`."""
        current = self.head
        previous = None
        while current:
            if current.data == target:
                if previous is None:      # deleting the head
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    # ---------------- SEARCH and TRAVERSAL ----------------

    def search(self, target):
        current = self.head
        position = 0
        while current:
            if current.data == target:
                return position
            current = current.next
            position += 1
        return -1

    def length(self):
        count, current = 0, self.head
        while current:
            count += 1
            current = current.next
        return count

    def reverse(self):
        """Reverse the list in place by flipping each next pointer."""
        previous, current = None, self.head
        while current:
            following = current.next
            current.next = previous
            previous = current
            current = following
        self.head = previous

    def display(self):
        values, current = [], self.head
        while current:
            values.append(str(current.data))
            current = current.next
        return " -> ".join(values) + " -> None" if values else "(empty list)"


if __name__ == "__main__":
    ll = SinglyLinkedList()
    print(f"empty list: {ll.display()}")

    print("\nINSERTION")
    ll.insert_at_end(20)
    print(f"  insert_at_end(20)       -> {ll.display()}")
    ll.insert_at_end(30)
    print(f"  insert_at_end(30)       -> {ll.display()}")
    ll.insert_at_beginning(10)
    print(f"  insert_at_beginning(10) -> {ll.display()}")
    ll.insert_after(20, 25)
    print(f"  insert_after(20, 25)    -> {ll.display()}")

    print("\nTRAVERSAL")
    print(f"  contents: {ll.display()}")
    print(f"  length  : {ll.length()}")

    print("\nSEARCH")
    for target in (25, 99):
        pos = ll.search(target)
        print(f"  search({target}) -> "
              + (f"found at index {pos}" if pos != -1 else "not found"))

    print("\nDELETION")
    ll.delete(25)
    print(f"  delete(25)  -> {ll.display()}")
    ll.delete(10)
    print(f"  delete(10)  -> {ll.display()}   (deleting the head)")
    print(f"  delete(99)  -> {ll.delete(99)} (nothing to delete)")

    print("\nREVERSE")
    ll.insert_at_end(40)
    print(f"  before: {ll.display()}")
    ll.reverse()
    print(f"  after : {ll.display()}")

    print("\nWHY A LINKED LIST rather than an array/list:")
    print("  insertion at the beginning is O(1), not O(n)")
    print("  it grows without reallocating a contiguous block")
    print("  but there is no random access -- reaching index k costs O(k)")
