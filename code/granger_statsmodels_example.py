"""
Granger-causality test using statsmodels on synthetic return series.

(c) Dr. Yves J. Hilpisch
AI-Powered by different LLMs
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests

from granger_example import simulate_coupled_returns


def run_granger_tests(max_lag: int=2) -> None:
    """Apply standard Granger-causality tests to simulated returns."""
    x, y = simulate_coupled_returns()  # simulate coupled X, Y returns

    data_yx = np.column_stack([y, x])  # outcome, then candidate cause
    # H0: X does not Granger-cause Y (second col does not cause first)
    results_xy = grangercausalitytests(data_yx, maxlag=max_lag, verbose=False)

    data_xy = np.column_stack([x, y])  # reverse ordering
    # H0: Y does not Granger-cause X (second col does not cause first)
    results_yx = grangercausalitytests(data_xy, maxlag=max_lag, verbose=False)

    print("Testing whether X Granger-causes Y")  # header for first direction
    for lag in range(1, max_lag + 1):
        test_res = results_xy[lag][0]["ssr_ftest"]  # (statistic, p-value, ...)
        print(f"lag={lag}: p-value={test_res[1]:.4f}")  # small p => reject null

    print("\nTesting whether Y Granger-causes X")  # header for reverse test
    for lag in range(1, max_lag + 1):
        test_res = results_yx[lag][0]["ssr_ftest"]  # same F-test in reverse
        # A large p-value does not reject the reverse null.
        print(f"lag={lag}: p-value={test_res[1]:.4f}")


if __name__ == "__main__":
    run_granger_tests()
