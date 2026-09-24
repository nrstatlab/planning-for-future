/* Experiment 4: Find both the largest and the smallest number in a list.
 *
 * Sample input:  5
 *                23 7 91 4 56
 * Sample output: Largest  = 91
 *                Smallest = 4
 */
#include <stdio.h>

#define MAX 100

int main(void)
{
    int list[MAX], n, i, largest, smallest;

    printf("How many numbers? ");
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX) {
        printf("Please enter a count between 1 and %d\n", MAX);
        return 1;
    }

    printf("Enter %d numbers: ", n);
    for (i = 0; i < n; i++) {
        if (scanf("%d", &list[i]) != 1) {
            printf("Invalid input\n");
            return 1;
        }
    }

    /* Seed both with the first element -- not with 0, which breaks on
       all-negative lists. */
    largest = smallest = list[0];
    for (i = 1; i < n; i++) {
        if (list[i] > largest)
            largest = list[i];
        if (list[i] < smallest)
            smallest = list[i];
    }

    printf("Largest  = %d\n", largest);
    printf("Smallest = %d\n", smallest);
    return 0;
}
