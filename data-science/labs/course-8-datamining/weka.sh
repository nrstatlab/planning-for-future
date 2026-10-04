# Sourced by the _weka.sh scripts beside it. Defines `weka`, which runs one WEKA class from
# the command line and prints the command first, as a terminal would show it, and sets
# $DATA to WEKA's datasets. tools/data-science/setup_weka.sh installs both in $WEKA_HOME (/tmp/weka by default).
#
# Each WEKA class run this way prints what the Explorer shows in its output pane for the
# same choice of algorithm and options -- the Explorer runs the same classes.

WEKA_HOME="${WEKA_HOME:-/tmp/weka}"
DATA="$WEKA_HOME/data"
if [ ! -f "$WEKA_HOME/weka-stable-3.8.7.jar" ]; then
    echo "WEKA is not installed in $WEKA_HOME: run tools/data-science/setup_weka.sh" >&2
    exit 1
fi

weka() {
    # The command as you would type it, with the datasets' folder shortened to data/.
    local shown="${*//$DATA\//data/}"
    printf '\n$ java %s\n' "$shown"
    # JAVA_TOOL_OPTIONS is emptied because the JVM announces it on every run, and the
    # announcement is not WEKA's output. The linear-algebra libraries' notes that they
    # found no native code, and fell back to Java -- two timestamped lines per note --
    # are the same: the JVM's log, not WEKA's output.
    JAVA_TOOL_OPTIONS= java -cp "$WEKA_HOME/*" "$@" 2>&1 \
        | { grep -v -e '^Picked up JAVA_TOOL_OPTIONS' -e '^WARNING: core mtj jar files are not available' \
                    -e '^WARNING: Failed to load implementation from: com.github.fommil.netlib' \
                    -e '^[A-Z][a-z][a-z] [0-9][0-9], [0-9]* [0-9:]* [AP]M com.github.fommil.netlib' || true; }
    return "${PIPESTATUS[0]}"
}
