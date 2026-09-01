#!/usr/bin/env bash
# Build the PySpark virtual environment for Course 12 B, experiment 17.
#
# PySpark is not in tools/requirements.txt because it needs a Java runtime and
# a build environment that the other courses do not, and because a failed
# install must not break the other nine suites. It lives in its own venv, and
# tools/run_bigdata_labs.py runs experiment 17 there if it exists and SKIPS it
# -- loudly -- if it does not.
set -euo pipefail

VENV="${SPARK_VENV:-/tmp/sparkenv}"

if ! command -v java >/dev/null 2>&1; then
    echo "java not found -- PySpark needs a JRE (17 or 21). Install one first."
    exit 1
fi
echo "java: $(java -version 2>&1 | head -1)"

if [ ! -d "$VENV" ]; then
    # --system-site-packages so pandas, numpy and pyarrow come from the parent
    # environment instead of being rebuilt.
    python3 -m venv --system-site-packages "$VENV"
fi

# setuptools<70 because PySpark's setup still uses the legacy install path,
# and --no-build-isolation so the pinned setuptools is the one actually used.
"$VENV/bin/pip" install --quiet "setuptools<70" wheel
"$VENV/bin/pip" install --quiet --no-build-isolation pyspark

"$VENV/bin/python" -c "import pyspark; print('pyspark', pyspark.__version__)"
echo "Spark environment ready at $VENV"
echo "run experiment 17 with: $VENV/bin/python labs/course-12b-bigdata/17_spark.py"
