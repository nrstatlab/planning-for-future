#!/usr/bin/env python3
"""Run and assert the Course 14 B practicals.

THIS COURSE HAS NO 'NOT EXECUTED' FILE. statsmodels is installed, so every
technique the syllabus names is a real call against a real implementation:
decomposition and STL, ACF and PACF, the ADF and KPSS tests, ARMA, ARIMA and
SARIMA, AIC/BIC and rolling-origin cross-validation, prediction intervals,
vector autoregression with Granger causality, unobserved-components models
driven by the Kalman filter, periodograms, Holt-Winters, and the whole family
of forecast error metrics.

The discipline that makes it worth running: the series are GENERATED FROM
KNOWN COEFFICIENTS, so the fitted models can be checked against the truth that
produced them. A model that merely converges has proved nothing.
"""
import pathlib
import sys
import traceback

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "labs" / "course-14b-timeseries"

LABS = [
    ("01_explore_decompose", "1, 2"),
    ("03_acf_stationarity", "3, 4"),
    ("05_arma_arima_sarima", "5, 6"),
    ("07_selection_forecast", "7, 8"),
    ("09_var_statespace_spectral", "9, 10, 11"),
    ("12_compare_evaluate", "12, 13"),
]


def banner(text):
    print("\n" + "=" * 62)
    print(text)
    print("=" * 62)


def main():
    banner("Course 14 B -- Time Series Analysis and Forecasting")
    sys.path.insert(0, str(LAB))

    passed, failed = 0, 0
    for module, exps in LABS:
        print(f"\n  --- {module}.py   (experiments {exps})")
        try:
            __import__(module).main()
            passed += 1
        except Exception:
            traceback.print_exc()
            print(f"  FAILED: experiments {exps}")
            failed += 1

    banner(f"{passed} lab programs executed and asserted, {failed} failed")
    print("covering all 13 prescribed experiments")
    print("""EVERY EXPERIMENT IN THIS COURSE RUNS. No file here is marked
NOT EXECUTED, because nothing the syllabus asks for is blocked --
statsmodels implements all of it.

The series are generated from KNOWN coefficients, so the fits are
checked against the truth: an AR(2) built with phi = (0.6, -0.3), an
MA(1) whose lag-1 ACF must equal theta/(1+theta^2), and a three-series
macro system whose Granger causality is known in both directions.""")
    print("=" * 62)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
