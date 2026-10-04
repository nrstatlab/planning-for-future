/* Experiment 1: Check whether a given number is an Armstrong number.
 *
 * An Armstrong number of n digits equals the sum of its own digits each
 * raised to the power n.  153 -> 1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153.
 *
 * Sample input:  153
 * Sample output: 153 is an Armstrong number
 */
#include <stdio.h>

/* Step 1: Count the digits */
int count_digits(int n)
{
    int digits = 0;
    if (n == 0)
        return 1;
    while (n > 0) {
        digits++;
        n /= 10;
    }
    return digits;
}

/* Step 2: Raise a digit to a power */
int power(int base, int exp)
{
    int result = 1, i;
    for (i = 0; i < exp; i++)
        result *= base;
    return result;
}

int main(void)
{
    int num, temp, digit, sum = 0, n;

    /* Step 3: Read the number */
    printf("Enter a number: ");
    if (scanf("%d", &num) != 1) {
        printf("Invalid input\n");
        return 1;
    }

    /* Step 4: Add each digit raised to the number of digits */
    n = count_digits(num);
    temp = num;
    while (temp > 0) {
        digit = temp % 10;
        sum += power(digit, n);
        temp /= 10;
    }

    /* Step 5: Compare the sum with the number */
    if (sum == num)
        printf("%d is an Armstrong number\n", num);
    else
        printf("%d is not an Armstrong number\n", num);
    return 0;
}
