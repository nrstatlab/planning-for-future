/* Experiment 13: Read data from / write data to a file.
 *
 * Demonstrates the full cycle: fopen in "w" mode, fprintf, fclose, then
 * fopen in "r" mode, fgets, fclose.  Always check that fopen succeeded --
 * that check is worth marks.
 *
 * Takes no input; writes and reads back sample.txt in the current directory.
 */
#include <stdio.h>

int main(void)
{
    FILE *fp;
    char line[256];
    const char *filename = "sample.txt";

    /* --- WRITE --- */
    fp = fopen(filename, "w");
    if (fp == NULL) {
        printf("Error: could not open %s for writing\n", filename);
        return 1;
    }
    fprintf(fp, "Data Science Major 2025\n");
    fprintf(fp, "Problem Solving Using C\n");
    fprintf(fp, "File handling demonstration\n");
    fclose(fp);
    printf("Data written to %s\n\n", filename);

    /* --- READ BACK --- */
    fp = fopen(filename, "r");
    if (fp == NULL) {
        printf("Error: could not open %s for reading\n", filename);
        return 1;
    }
    printf("Contents of %s:\n", filename);
    while (fgets(line, sizeof(line), fp) != NULL)
        printf("  %s", line);
    fclose(fp);
    return 0;
}
