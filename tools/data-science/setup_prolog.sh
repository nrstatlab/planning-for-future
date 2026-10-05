#!/usr/bin/env bash
# Install SWI-Prolog, for Course 13 A.
#
# The Ubuntu archive carries it as swi-prolog-nox (no graphics, which the labs do not use);
# Ubuntu 24.04's is 9.0.4, the version the lab page's answers come from. Elsewhere, any
# SWI-Prolog 9 from https://www.swi-prolog.org/download/stable gives the same answers.
#
# tools/data-science/prolog_lab.py runs a lab file as a student does at the ?- prompt, and
# run_ai_labs.py runs all sixteen and checks their answers.
set -euo pipefail

if ! command -v swipl >/dev/null; then
    sudo=""; [ "$(id -u)" -ne 0 ] && sudo="sudo"
    $sudo apt-get install -y swi-prolog-nox
fi
swipl --version
