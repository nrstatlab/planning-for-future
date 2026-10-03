# Practical 3 -- four sorts and two searches, each counting its own work
# Step 1: Bubble sort, counting comparisons
def bubble(a):
    a = a[:]
    comps = 0
    for i in range(len(a) - 1):
        swapped = False
        for j in range(len(a) - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a, comps

# Step 2: Insertion sort, counting comparisons
def insertion(a):
    a = a[:]
    comps = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a, comps

# Step 3: Merge sort
def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

# Step 4: Quick sort
def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    lo = [v for v in a if v < pivot]
    eq = [v for v in a if v == pivot]
    hi = [v for v in a if v > pivot]
    return quick_sort(lo) + eq + quick_sort(hi)

# Step 5: Linear and binary search, counting comparisons
def linear_search(a, key):
    for i, v in enumerate(a):
        if v == key:
            return i, i + 1          # position, comparisons used
    return -1, len(a)

def binary_search(a, key):
    lo, hi, comps = 0, len(a) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comps += 1
        if a[mid] == key:
            return mid, comps
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, comps

# Step 6: Sort the data four ways and compare
data = [42, 17, 93, 8, 55, 23, 71, 4, 66, 30]
b, cb = bubble(data)
i_, ci = insertion(data)
print("bubble   ", b, "comparisons:", cb)
print("insertion", i_, "comparisons:", ci)
print("merge    ", merge_sort(data))
print("quick    ", quick_sort(data))
print("all four agree?", b == i_ == merge_sort(data) == quick_sort(data))

# Step 7: Search the sorted list
srt = b
print("linear search for 66:", linear_search(srt, 66))
print("binary search for 66:", binary_search(srt, 66))
print("binary search for 50:", binary_search(srt, 50))
