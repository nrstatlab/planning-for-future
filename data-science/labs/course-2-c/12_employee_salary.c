/* Experiment 12: Calculate the salaries of all employees using an Employee
 * structure (ID, Name, Designation, Basic Pay, DA, HRA, Gross, Deduction, Net).
 *
 * Rules given in the syllabus:
 *   DA        = 30% of Basic Pay
 *   HRA       = 15% of Basic Pay
 *   Deduction = 10% of (Basic Pay + DA)
 *   Gross     = Basic Pay + DA + HRA
 *   Net       = Gross - Deduction
 *
 * Sample input:  2
 *                101 Alice Manager 50000
 *                102 Bob Clerk 20000
 */
#include <stdio.h>

#define MAX_EMP 50

struct Employee {
    int   id;
    char  name[50];
    char  designation[50];
    float basic_pay;
    float da;
    float hra;
    float gross_salary;
    float deduction;
    float net_salary;
};

void compute_salary(struct Employee *e)
{
    e->da        = 0.30f * e->basic_pay;
    e->hra       = 0.15f * e->basic_pay;
    e->deduction = 0.10f * (e->basic_pay + e->da);
    e->gross_salary = e->basic_pay + e->da + e->hra;
    e->net_salary   = e->gross_salary - e->deduction;
}

int main(void)
{
    struct Employee staff[MAX_EMP];
    int n, i;

    printf("How many employees? ");
    if (scanf("%d", &n) != 1 || n <= 0 || n > MAX_EMP) return 1;

    for (i = 0; i < n; i++) {
        printf("Employee %d (id name designation basic_pay): ", i + 1);
        if (scanf("%d %49s %49s %f", &staff[i].id, staff[i].name,
                  staff[i].designation, &staff[i].basic_pay) != 4)
            return 1;
        compute_salary(&staff[i]);
    }

    printf("\n%-6s %-12s %-12s %10s %9s %9s %10s %10s %10s\n",
           "ID", "Name", "Designation", "Basic", "DA", "HRA",
           "Gross", "Deduction", "Net");
    for (i = 0; i < n; i++) {
        printf("%-6d %-12s %-12s %10.2f %9.2f %9.2f %10.2f %10.2f %10.2f\n",
               staff[i].id, staff[i].name, staff[i].designation,
               staff[i].basic_pay, staff[i].da, staff[i].hra,
               staff[i].gross_salary, staff[i].deduction, staff[i].net_salary);
    }
    return 0;
}
