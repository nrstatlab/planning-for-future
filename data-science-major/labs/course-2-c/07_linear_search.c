/* Experiment 7: Search for an element in a given list of values.
 *
 * Linear search: check each element in turn.  Worst case O(n).
 *
 * Sample input:  5
 *                10 20 30 40 50
 *                30
 * Sample output: 30 found at position 3 (index 2)
 */
#include <stdio.h>

#define MAX 100

int linear_search(const int list[], int n, int key)
{
    int i;
    for (i = 0; i < n; i++) {
        if (list[i] == key)
            return i;       /* found -- return the index */
    }
    return -1;              /* the conventional "not found" marker */
}

int main(void)
{
    int list[MAX], n, i, key, pos;

    printf("How many elements? ");
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX) return 1;

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
        if (scanf("%d", &list[i]) != 1) return 1;

    printf("Enter the element to search: ");
    if (scanf("%d", &key) != 1) return 1;

    pos = linear_search(list, n, key);
    if (pos == -1)
        printf("%d is not present in the list\n", key);
    else
        printf("%d found at position %d (index %d)\n", key, pos + 1, pos);
    return 0;
}
