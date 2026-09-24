/* Experiment 10: Multiplication of two N x N matrices.
 *
 * C[i][j] = sum over k of A[i][k] * B[k][j]
 *
 * Sample input:  2
 *                1 2 3 4
 *                5 6 7 8
 * Sample output: 19 22
 *                43 50
 */
#include <stdio.h>

#define MAX 10

void multiply(int a[MAX][MAX], int b[MAX][MAX], int c[MAX][MAX], int n)
{
    int i, j, k;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            c[i][j] = 0;                 /* must reset before accumulating */
            for (k = 0; k < n; k++)
                c[i][j] += a[i][k] * b[k][j];
        }
    }
}

int main(void)
{
    int a[MAX][MAX], b[MAX][MAX], c[MAX][MAX];
    int n, i, j;

    printf("Enter N (order of the square matrices): ");
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX) return 1;

    printf("Enter %d elements of matrix A: ", n * n);
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            if (scanf("%d", &a[i][j]) != 1) return 1;

    printf("Enter %d elements of matrix B: ", n * n);
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            if (scanf("%d", &b[i][j]) != 1) return 1;

    multiply(a, b, c, n);

    printf("\nA x B =\n");
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++)
            printf("%6d", c[i][j]);
        printf("\n");
    }
    return 0;
}
