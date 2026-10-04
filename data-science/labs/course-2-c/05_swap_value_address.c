/* Experiment 5: Demonstrate the change in parameter values while swapping two
 * integers using Call by Value and Call by Address.
 *
 * This is the classic exam question on parameter passing.  Call by value swaps
 * only the function's private copies, so the caller sees nothing change.  Call
 * by address passes the addresses, so the function reaches the originals.
 *
 * Sample input:  10 20
 */
#include <stdio.h>

/* Step 1: Swap by value: the function gets copies */
void swap_by_value(int a, int b)
{
    int temp = a;
    a = b;
    b = temp;
    printf("  inside swap_by_value  : a = %d, b = %d\n", a, b);
}

/* Step 2: Swap by address: the function gets pointers */
void swap_by_address(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
    printf("  inside swap_by_address: a = %d, b = %d\n", *a, *b);
}

int main(void)
{
    int x, y;

    /* Step 3: Read two integers */
    printf("Enter two integers: ");
    if (scanf("%d %d", &x, &y) != 2) {
        printf("Invalid input\n");
        return 1;
    }

    /* Step 4: Call by value: before, inside, after */
    printf("\nCALL BY VALUE\n");
    printf("  before: x = %d, y = %d\n", x, y);
    swap_by_value(x, y);
    printf("  after : x = %d, y = %d   <- unchanged\n", x, y);

    /* Step 5: Call by address: before, inside, after */
    printf("\nCALL BY ADDRESS\n");
    printf("  before: x = %d, y = %d\n", x, y);
    swap_by_address(&x, &y);
    printf("  after : x = %d, y = %d   <- swapped\n", x, y);
    return 0;
}
