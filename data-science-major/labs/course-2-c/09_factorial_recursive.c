/* Experiment 9: Calculate the factorial of a given integer using recursion.
 *
 * The exam almost always asks you to identify the base case and the recursive
 * case, so they are labelled below.
 *
 * Sample input:  5
 * Sample output: 5! = 120
 */
#include <stdio.h>

unsigned long long factorial(int n)
{
    if (n == 0 || n == 1)          /* BASE CASE -- stops the recursion */
        return 1;
    return (unsigned long long) n * factorial(n - 1);  /* RECURSIVE CASE */
}

int main(void)
{
    int n;

    printf("Enter a non-negative integer: ");
    if (scanf("%d", &n) != 1 || n < 0) {
        printf("Factorial is not defined for negative numbers\n");
        return 1;
    }
    if (n > 20) {
        printf("%d! overflows a 64-bit integer\n", n);
        return 1;
    }

    printf("%d! = %llu\n", n, factorial(n));
    return 0;
}
