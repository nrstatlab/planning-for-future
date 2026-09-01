/* Experiment 3: Generate the first n terms of the Fibonacci sequence.
 *
 * Sample input:  10
 * Sample output: 0 1 1 2 3 5 8 13 21 34
 */
#include <stdio.h>

int main(void)
{
    int n, i;
    long long first = 0, second = 1, next;

    printf("Enter the number of terms: ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Please enter a positive number of terms\n");
        return 1;
    }

    printf("Fibonacci sequence: ");
    for (i = 0; i < n; i++) {
        printf("%lld", first);
        if (i < n - 1)
            printf(" ");
        next = first + second;
        first = second;
        second = next;
    }
    printf("\n");
    return 0;
}
