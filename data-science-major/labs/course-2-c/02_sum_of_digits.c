/* Experiment 2: Find the sum of individual digits of a positive integer.
 *
 * Sample input:  12345
 * Sample output: Sum of digits of 12345 = 15
 */
#include <stdio.h>

int main(void)
{
    int num, temp, sum = 0;

    printf("Enter a positive integer: ");
    if (scanf("%d", &num) != 1 || num < 0) {
        printf("Please enter a positive integer\n");
        return 1;
    }

    temp = num;
    while (temp > 0) {
        sum += temp % 10;   /* peel off the last digit */
        temp /= 10;         /* and drop it */
    }

    printf("Sum of digits of %d = %d\n", num, sum);
    return 0;
}
