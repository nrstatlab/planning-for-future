"""Experiment 7 -- Gross and net salary of six employees.

Excel cannot be run here, so this script computes what the SPREADSHEET
FORMULAS compute and asserts every figure the notes quote. The formulas
themselves are in notes/sem-1/course-1-computer-fundamentals/lab.md; this
file is the proof that the numbers beside them are right.

The one thing worth taking away: Deduction is 10% of (Basic + DA), not 10%
of Basic. Get that wrong and every net salary is too high -- with no error
message, because the sheet still calculates.
"""
from fixtures import EMPLOYEES, DA_RATE, HRA_RATE, DEDUCTION_RATE


def payslip(basic):
    """One row of the sheet. Each line is one Excel formula.

        E2  DA         =D2*$B$1
        F2  HRA        =D2*$B$2
        G2  Gross      =D2+E2+F2
        H2  Deduction  =(D2+E2)*$B$3
        I2  Net        =G2-H2
    """
    da = basic * DA_RATE
    hra = basic * HRA_RATE
    gross = basic + da + hra
    deduction = (basic + da) * DEDUCTION_RATE
    net = gross - deduction
    return da, hra, gross, deduction, net


def main():
    print("  Rates: DA 30% of Basic, HRA 15% of Basic, "
          "Deduction 10% of (Basic + DA)\n")
    header = f"  {'Name':<15}{'Basic':>9}{'DA':>9}{'HRA':>8}" \
             f"{'Gross':>10}{'Deduct':>9}{'Net':>10}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    totals = [0.0] * 6
    for name, _emp_id, _dept, basic in EMPLOYEES:
        da, hra, gross, deduction, net = payslip(basic)

        # The closed form. Gross = 1.45B and Net = 1.32B fall straight out of
        # the rates, and asserting them catches the commonest error in this
        # experiment: taking the deduction on Basic alone, which would leave
        # Net = 1.35B -- 3% of Basic too much, every month, for every
        # employee.
        assert gross == basic * 1.45, (name, gross)
        assert round(net, 6) == round(basic * 1.32, 6), (name, net)
        assert net != basic * 1.35

        row = (basic, da, hra, gross, deduction, net)
        totals = [t + v for t, v in zip(totals, row)]
        print(f"  {name:<15}{basic:>9,.0f}{da:>9,.0f}{hra:>8,.0f}"
              f"{gross:>10,.0f}{deduction:>9,.0f}{net:>10,.0f}")

    print("  " + "-" * (len(header) - 2))
    print(f"  {'TOTAL':<15}" + "".join(
        f"{v:>{w},.0f}" for v, w in zip(totals, (9, 9, 8, 10, 9, 10))))

    # The column totals quoted in lab.md.
    assert totals == [200500, 60150, 30075, 290725, 26065, 264660], totals

    # Highest and lowest paid, which the experiment also asks for.
    nets = {name: payslip(basic)[4] for name, _i, _d, basic in EMPLOYEES}
    top = max(nets, key=nets.get)
    low = min(nets, key=nets.get)
    assert top == "Faisal Ahmed" and nets[top] == 68640
    assert low == "Chitra Devi" and nets[low] == 24420
    print(f"\n  Highest net  {top:<15} {nets[top]:>10,.0f}")
    print(f"  Lowest net   {low:<15} {nets[low]:>10,.0f}")

    # What the common mistake would have cost, in rupees, for this sheet.
    wrong_total = sum(basic * 1.35 for _n, _i, _d, basic in EMPLOYEES)
    overpay = wrong_total - totals[5]
    assert round(overpay, 6) == round(200500 * 0.03, 6)
    print(f"\n  Deducting 10% of Basic instead of 10% of (Basic + DA)")
    print(f"  overpays the payroll by {overpay:,.0f} a month "
          f"(3% of the {totals[0]:,.0f} basic bill).")


if __name__ == "__main__":
    main()
