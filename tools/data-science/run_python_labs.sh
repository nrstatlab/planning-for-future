#!/usr/bin/env bash
# Run every Python lab program with its documented sample input.
# The two Tkinter programs are syntax-checked only -- tkinter is not installed
# here and a GUI needs a display.
# Usage: bash tools/run_python_labs.sh
set -u

DIR="$(cd "$(dirname "$0")/.." && pwd)/labs/course-3-python"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
pass=0; fail=0; skipped=0

run() {                     # run <file> <stdin>
    local f="$1" input="${2:-}"
    printf '%-34s ' "$f"
    if ( cd "$WORK" && printf '%b' "$input" | python3 "$DIR/$f" >out 2>&1 ); then
        echo "ok"; pass=$((pass+1))
    else
        echo "FAILED"; sed 's/^/    /' "$WORK/out" | tail -6; fail=$((fail+1))
    fi
}

compile_only() {            # compile_only <file> <reason>
    local f="$1"
    printf '%-34s ' "$f"
    if python3 -m py_compile "$DIR/$f" 2>"$WORK/err"; then
        echo "syntax ok (not run: $2)"; skipped=$((skipped+1))
    else
        echo "SYNTAX ERROR"; sed 's/^/    /' "$WORK/err"; fail=$((fail+1))
    fi
}

run 01a_basic_details.py
run 01b_operators.py            "12\n5\n"
run 02a_largest_of_three.py     "45\n78\n23\n"
run 02b_prime_check.py          "29\n"
run 02c_loop_control.py
run 03a_factorial_recursion.py  "6\n"
run 03b_function_arguments.py
run 04_string_operations.py
run 05_list_operations.py
run 06_tuple_operations.py
run 07_set_operations.py
run 08_dictionary_operations.py
run 09_count_file_characters.py
run 10_copy_file.py
run 11_csv_marks.py
run 12_exception_handling.py
run 13_student_class.py
run 14_inheritance.py
run 15_stack_queue.py
run 16_linked_list.py
compile_only 17_tkinter_input.py      "tkinter not installed"
compile_only 18_tkinter_calculator.py "tkinter not installed"

echo
echo "ran: $pass   syntax-checked only: $skipped   failed: $fail"
[ "$fail" -eq 0 ]
