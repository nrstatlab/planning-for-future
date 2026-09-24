/* Experiment 6: Perform various string operations.
 *
 * Shows both the library functions from <string.h> and hand-written versions,
 * because exams commonly ask you to implement strlen/strcpy/strcmp yourself.
 *
 * Sample input:  Hello
 *                World
 */
#include <stdio.h>
#include <string.h>

/* Hand-written equivalents -- the "write it without the library" exam question. */
int my_strlen(const char *s)
{
    int len = 0;
    while (s[len] != '\0')
        len++;
    return len;
}

void my_strcpy(char *dest, const char *src)
{
    int i = 0;
    while (src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

int my_strcmp(const char *a, const char *b)
{
    int i = 0;
    while (a[i] != '\0' && a[i] == b[i])
        i++;
    return a[i] - b[i];
}

void my_strrev(char *s)
{
    int i = 0, j = my_strlen(s) - 1;
    char temp;
    while (i < j) {
        temp = s[i];
        s[i] = s[j];
        s[j] = temp;
        i++;
        j--;
    }
}

int main(void)
{
    char s1[100], s2[100], copy[200], joined[200];

    printf("Enter first string : ");
    if (scanf("%99s", s1) != 1) return 1;
    printf("Enter second string: ");
    if (scanf("%99s", s2) != 1) return 1;

    printf("\nLibrary functions\n");
    printf("  strlen(s1)     = %d\n", (int) strlen(s1));
    printf("  strcmp(s1, s2) = %d\n", strcmp(s1, s2));

    strcpy(joined, s1);
    strcat(joined, s2);
    printf("  strcat(s1, s2) = %s\n", joined);

    printf("\nHand-written versions\n");
    printf("  my_strlen(s1)     = %d\n", my_strlen(s1));
    printf("  my_strcmp(s1, s2) = %d\n", my_strcmp(s1, s2));

    my_strcpy(copy, s1);
    printf("  my_strcpy -> %s\n", copy);

    my_strrev(copy);
    printf("  my_strrev -> %s\n", copy);
    return 0;
}
