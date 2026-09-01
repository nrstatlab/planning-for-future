/* Experiment 11: Sort a given list of integers in ascending order.
 *
 * Bubble sort, with the early-exit flag -- exams ask for the flag as the
 * "optimised" version.  Best case O(n) on already-sorted data, worst O(n^2).
 *
 * Sample input:  6
 *                64 34 25 12 22 11
 * Sample output: 11 12 22 25 34 64
 */
#include <stdio.h>

#define MAX 100

void bubble_sort(int list[], int n)
{
    int i, j, temp, swapped;
    for (i = 0; i < n - 1; i++) {
        swapped = 0;
        for (j = 0; j < n - 1 - i; j++) {
            if (list[j] > list[j + 1]) {
                temp = list[j];
                list[j] = list[j + 1];
                list[j + 1] = temp;
                swapped = 1;
            }
        }
        if (!swapped)       /* nothing moved -- the list is already sorted */
            break;
    }
}

int main(void)
{
    int list[MAX], n, i;

    printf("How many elements? ");
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX) return 1;

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
        if (scanf("%d", &list[i]) != 1) return 1;

    bubble_sort(list, n);

    printf("Sorted list: ");
    for (i = 0; i < n; i++)
        printf("%d ", list[i]);
    printf("\n");
    return 0;
}
