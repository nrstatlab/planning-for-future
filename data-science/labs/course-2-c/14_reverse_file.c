/* Experiment 14: Reverse the contents of a file and store the result in
 * another file.
 *
 * Method: seek to the end, then walk backwards one byte at a time with
 * fseek(fp, -offset, SEEK_END), writing each character to the output file.
 *
 * Creates input.txt, then produces reversed.txt from it.
 */
#include <stdio.h>

int main(void)
{
    FILE *in, *out;
    long size, i;
    int ch;

    /* Create the input file so the program is self-contained. */
    in = fopen("input.txt", "w");
    if (in == NULL) {
        printf("Error: could not create input.txt\n");
        return 1;
    }
    fprintf(in, "ABCDEFG");
    fclose(in);

    in = fopen("input.txt", "rb");
    if (in == NULL) {
        printf("Error: could not open input.txt\n");
        return 1;
    }
    out = fopen("reversed.txt", "wb");
    if (out == NULL) {
        printf("Error: could not create reversed.txt\n");
        fclose(in);
        return 1;
    }

    fseek(in, 0, SEEK_END);
    size = ftell(in);

    for (i = 1; i <= size; i++) {
        fseek(in, -i, SEEK_END);
        ch = fgetc(in);
        if (ch == EOF)
            break;
        fputc(ch, out);
    }

    fclose(in);
    fclose(out);

    /* Show the result. */
    printf("input.txt    : ");
    in = fopen("input.txt", "r");
    while ((ch = fgetc(in)) != EOF) putchar(ch);
    fclose(in);

    printf("\nreversed.txt : ");
    out = fopen("reversed.txt", "r");
    while ((ch = fgetc(out)) != EOF) putchar(ch);
    fclose(out);
    printf("\n");
    return 0;
}
