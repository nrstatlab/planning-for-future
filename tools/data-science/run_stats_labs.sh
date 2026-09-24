#!/usr/bin/env bash
# Verify the Course 4 statistics labs.
# First checks statlib against published statistical-table values, then runs
# every experiment script.
# Usage: bash tools/run_stats_labs.sh
set -u

DIR="$(cd "$(dirname "$0")/.." && pwd)/labs/course-4-stats/python"
cd "$DIR" || exit 1
fail=0

echo "Checking statlib against published table values"
if python3 test_statlib.py > /tmp/statlib_out 2>&1; then
    tail -1 /tmp/statlib_out
else
    grep FAIL /tmp/statlib_out; fail=$((fail+1))
fi

echo
echo "Running experiment scripts"
for f in 01_probability_contingency.py 02_descriptive_stats.py \
         03_random_variables_distributions.py 04_correlation_regression.py \
         05_inference_hypothesis_tests.py; do
    printf '  %-42s ' "$f"
    if python3 "$f" > /dev/null 2>&1; then
        echo "ok"
    else
        echo "FAILED"; python3 "$f" 2>&1 | tail -5; fail=$((fail+1))
    fi
done

echo
if [ "$fail" -eq 0 ]; then
    echo "All statistics labs verified."
else
    echo "FAILURES: $fail"
fi
[ "$fail" -eq 0 ]
