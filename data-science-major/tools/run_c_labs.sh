#!/usr/bin/env bash
# Compile and run every C lab program with its documented sample input.
# Usage: bash tools/run_c_labs.sh
set -u

DIR="$(cd "$(dirname "$0")/.." && pwd)/labs/course-2-c"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
pass=0; fail=0

run() {                     # run <source> <input>
    local src="$1" input="$2" bin="$WORK/bin"
    printf '%-32s ' "$(basename "$src")"
    if ! gcc -Wall -Wextra -o "$bin" "$src" 2>"$WORK/err"; then
        echo "COMPILE FAILED"; sed 's/^/    /' "$WORK/err"; fail=$((fail+1)); return
    fi
    if [ -s "$WORK/err" ]; then
        echo "WARNINGS"; sed 's/^/    /' "$WORK/err"; fail=$((fail+1)); return
    fi
    if ( cd "$WORK" && printf '%b' "$input" | ./bin >out 2>&1 ); then
        echo "ok"; pass=$((pass+1))
    else
        echo "RUNTIME FAILURE"; sed 's/^/    /' "$WORK/out"; fail=$((fail+1))
    fi
}

run "$DIR/01_armstrong.c"             "153\n"
run "$DIR/02_sum_of_digits.c"         "12345\n"
run "$DIR/03_fibonacci.c"             "10\n"
run "$DIR/04_largest_smallest.c"      "5\n23 7 91 4 56\n"
run "$DIR/05_swap_value_address.c"    "10 20\n"
run "$DIR/06_string_operations.c"     "Hello\nWorld\n"
run "$DIR/07_linear_search.c"         "5\n10 20 30 40 50\n30\n"
run "$DIR/08_matrix_addition.c"       "2 2\n1 2 3 4\n5 6 7 8\n"
run "$DIR/09_factorial_recursive.c"   "5\n"
run "$DIR/10_matrix_multiplication.c" "2\n1 2 3 4\n5 6 7 8\n"
run "$DIR/11_sort_ascending.c"        "6\n64 34 25 12 22 11\n"
run "$DIR/12_employee_salary.c"       "2\n101 Alice Manager 50000\n102 Bob Clerk 20000\n"
run "$DIR/13_file_read_write.c"       ""
run "$DIR/14_reverse_file.c"          ""
run "$DIR/15_book_file_crud.c"        "1 111 C_Programming Balaguruswamy 450.00 500 TMH\n1 222 Python_Basics Thareja 550.00 600 Oxford\n5\n2 111\n3 111 600.00\n4 222\n5\n6\n"

echo
echo "passed: $pass   failed: $fail"
[ "$fail" -eq 0 ]
