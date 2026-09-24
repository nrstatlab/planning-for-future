/* Experiment 15: Create a Book structure (ISBN, Title, Author, Price, Pages,
 * Publisher), store book details in a file, and perform:
 *   a. Add book details
 *   b. Search for a book by ISBN and display it if present
 *   c. Update a book's details using its ISBN
 *   d. Delete a book by ISBN and display the remaining books
 *
 * This is the largest program in the lab list: it combines structures, file
 * I/O and a menu-driven loop.
 *
 * The delete operation uses the standard technique -- copy every record except
 * the doomed one into a temporary file, then rename it over the original.  You
 * cannot remove bytes from the middle of a file in place.
 *
 * Sample input (menu choices):
 *   1 111 C_Programming Balaguruswamy 450.00 500 TMH
 *   1 222 Python_Basics Thareja 550.00 600 Oxford
 *   2 111
 *   3 111 600.00
 *   4 222
 *   5
 *   6
 */
#include <stdio.h>
#include <string.h>

#define DATAFILE "books.dat"
#define TEMPFILE "temp.dat"

struct Book {
    int   isbn;
    char  title[50];
    char  author[50];
    float price;
    int   pages;
    char  publisher[50];
};

static void print_header(void)
{
    printf("%-8s %-20s %-15s %10s %7s %-15s\n",
           "ISBN", "Title", "Author", "Price", "Pages", "Publisher");
}

static void print_book(const struct Book *b)
{
    printf("%-8d %-20s %-15s %10.2f %7d %-15s\n",
           b->isbn, b->title, b->author, b->price, b->pages, b->publisher);
}

/* (a) Append one book to the data file. */
void add_book(void)
{
    struct Book b;
    FILE *fp = fopen(DATAFILE, "ab");
    if (fp == NULL) {
        printf("Error: cannot open %s\n", DATAFILE);
        return;
    }
    printf("Enter ISBN title author price pages publisher: ");
    if (scanf("%d %49s %49s %f %d %49s", &b.isbn, b.title, b.author,
              &b.price, &b.pages, b.publisher) != 6) {
        printf("Invalid book details\n");
        fclose(fp);
        return;
    }
    fwrite(&b, sizeof(b), 1, fp);
    fclose(fp);
    printf("Book %d added\n", b.isbn);
}

/* (b) Search by ISBN. */
void search_book(void)
{
    struct Book b;
    int isbn, found = 0;
    FILE *fp = fopen(DATAFILE, "rb");
    if (fp == NULL) {
        printf("No books stored yet\n");
        return;
    }
    printf("Enter ISBN to search: ");
    if (scanf("%d", &isbn) != 1) {
        fclose(fp);
        return;
    }
    while (fread(&b, sizeof(b), 1, fp) == 1) {
        if (b.isbn == isbn) {
            print_header();
            print_book(&b);
            found = 1;
            break;
        }
    }
    fclose(fp);
    if (!found)
        printf("Book with ISBN %d not found\n", isbn);
}

/* (c) Update a book's price, writing the record back in place. */
void update_book(void)
{
    struct Book b;
    int isbn, found = 0;
    float new_price;
    FILE *fp = fopen(DATAFILE, "rb+");
    if (fp == NULL) {
        printf("No books stored yet\n");
        return;
    }
    printf("Enter ISBN to update and the new price: ");
    if (scanf("%d %f", &isbn, &new_price) != 2) {
        fclose(fp);
        return;
    }
    while (fread(&b, sizeof(b), 1, fp) == 1) {
        if (b.isbn == isbn) {
            b.price = new_price;
            /* Step back over the record just read, then overwrite it. */
            fseek(fp, -(long) sizeof(b), SEEK_CUR);
            fwrite(&b, sizeof(b), 1, fp);
            found = 1;
            break;
        }
    }
    fclose(fp);
    printf(found ? "Book %d updated\n" : "Book with ISBN %d not found\n", isbn);
}

/* (d) Delete by ISBN: copy all survivors to a temp file, then rename. */
void delete_book(void)
{
    struct Book b;
    int isbn, found = 0;
    FILE *fp, *temp;

    fp = fopen(DATAFILE, "rb");
    if (fp == NULL) {
        printf("No books stored yet\n");
        return;
    }
    temp = fopen(TEMPFILE, "wb");
    if (temp == NULL) {
        printf("Error: cannot create temporary file\n");
        fclose(fp);
        return;
    }
    printf("Enter ISBN to delete: ");
    if (scanf("%d", &isbn) != 1) {
        fclose(fp);
        fclose(temp);
        return;
    }
    while (fread(&b, sizeof(b), 1, fp) == 1) {
        if (b.isbn == isbn)
            found = 1;              /* skip it -- this is the deletion */
        else
            fwrite(&b, sizeof(b), 1, temp);
    }
    fclose(fp);
    fclose(temp);

    remove(DATAFILE);
    rename(TEMPFILE, DATAFILE);

    if (found)
        printf("Book %d deleted\n", isbn);
    else
        printf("Book with ISBN %d not found\n", isbn);
}

void display_all(void)
{
    struct Book b;
    int count = 0;
    FILE *fp = fopen(DATAFILE, "rb");
    if (fp == NULL) {
        printf("No books stored yet\n");
        return;
    }
    print_header();
    while (fread(&b, sizeof(b), 1, fp) == 1) {
        print_book(&b);
        count++;
    }
    fclose(fp);
    printf("(%d book(s))\n", count);
}

int main(void)
{
    int choice;

    for (;;) {
        printf("\n1.Add  2.Search  3.Update  4.Delete  5.Display all  6.Exit\n");
        printf("Enter your choice: ");
        if (scanf("%d", &choice) != 1)
            break;

        switch (choice) {
        case 1: add_book();     break;
        case 2: search_book();  break;
        case 3: update_book();  break;
        case 4: delete_book();  break;
        case 5: display_all();  break;
        case 6: printf("Exiting\n"); return 0;
        default: printf("Invalid choice\n");
        }
    }
    return 0;
}
