/* Experiment 8: Use functions to add two matrices.
 *
 * Sample input:  2 2
 *                1 2 3 4
 *                5 6 7 8
 * Sample output: 6 8
 *                10 12
 */
#include <stdio.h>

#define MAX 10

void read_matrix(int m[MAX][MAX], int rows, int cols, const char *name)
{
    int i, j;
    printf("Enter %d elements of matrix %s: ", rows * cols, name);
    for (i = 0; i < rows; i++)
        for (j = 0; j < cols; j++)
            if (scanf("%d", &m[i][j]) != 1)
                return;
}

void add_matrices(int a[MAX][MAX], int b[MAX][MAX], int sum[MAX][MAX],
                  int rows, int cols)
{
    int i, j;
    for (i = 0; i < rows; i++)
        for (j = 0; j < cols; j++)
            sum[i][j] = a[i][j] + b[i][j];
}

void print_matrix(int m[MAX][MAX], int rows, int cols)
{
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++)
            printf("%4d", m[i][j]);
        printf("\n");
    }
}

int main(void)
{
    int a[MAX][MAX], b[MAX][MAX], sum[MAX][MAX];
    int rows, cols;

    printf("Enter rows and columns: ");
    if (scanf("%d %d", &rows, &cols) != 2 ||
        rows <= 0 || cols <= 0 || rows > MAX || cols > MAX) {
        printf("Dimensions must be between 1 and %d\n", MAX);
        return 1;
    }

    read_matrix(a, rows, cols, "A");
    read_matrix(b, rows, cols, "B");
    add_matrices(a, b, sum, rows, cols);

    printf("\nA + B =\n");
    print_matrix(sum, rows, cols);
    return 0;
}
