"""
Toy example illustrating Granger causality between two return series.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn-v0_8")


def simulate_coupled_returns(
    steps: int=500,
    rho_x: float=0.2,
    beta_xy: float=0.5,
    sigma: float=0.02,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate two AR(1) processes where X helps to predict Y."""
    rng = np.random.default_rng(seed=21)
    eps_x = rng.normal(0.0, sigma, size=steps)  #  innovation shocks for X
    eps_y = rng.normal(0.0, sigma, size=steps)  #  innovation shocks for Y

    x = np.empty(steps)  #  allocate array for X returns
    y = np.empty(steps)  #  allocate array for Y returns
    x[0] = eps_x[0]  #  initialize X with first shock
    y[0] = eps_y[0]  #  initialize Y with first shock

    for t in range(1, steps):
        x[t] = rho_x * x[t - 1] + eps_x[t]  #  AR(1) recursion for X
        y[t] = beta_xy * x[t - 1] + eps_y[t]  #  X drives Y with one lag

    return x, y


def simple_granger_regression(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    """Compute R^2 for Y on lags of Y only vs lags of Y and X."""
    # one-lag design matrices for Y_t = a + b Y_{t-1} + e_t
    y_lag = y[:-1]  #  lagged Y
    y_t = y[1:]  #  current Y aligned with lag

    X_y = np.column_stack([np.ones_like(y_lag), y_lag])  #  intercept and Y_{t-1}
    beta_y, *_ = np.linalg.lstsq(X_y, y_t, rcond=None)  #  restricted regression
    y_hat_y = X_y @ beta_y  #  fitted values using Y lags only
    ss_tot = np.sum((y_t - y_t.mean()) ** 2)  #  total sum of squares
    ss_res_y = np.sum((y_t - y_hat_y) ** 2)  #  residual sum of squares
    r2_y = 1.0 - ss_res_y / ss_tot  #  R^2 for restricted model

    # augmented model: Y_t = a + b Y_{t-1} + c X_{t-1} + e_t
    x_lag = x[:-1]  #  lagged X
    X_xy = np.column_stack(
        [np.ones_like(y_lag), y_lag, x_lag]
    )  #  intercept, Y_{t-1}, X_{t-1}
    beta_xy, *_ = np.linalg.lstsq(X_xy, y_t, rcond=None)  #  full regression
    y_hat_xy = X_xy @ beta_xy  #  fitted values using Y and X lags
    ss_res_xy = np.sum((y_t - y_hat_xy) ** 2)  #  residual sum of squares (full)
    r2_xy = 1.0 - ss_res_xy / ss_tot  #  R^2 for full model

    return float(r2_y), float(r2_xy)


def main() -> None:
    """Run simulation, compute R^2 values, and plot a bar chart."""
    x, y = simulate_coupled_returns()  #  simulate coupled AR(1) returns
    r2_y, r2_xy = simple_granger_regression(x, y)  #  compute R^2 values

    labels = [
        r"$Y_t$ on $Y_{t-1}$",
        r"$Y_t$ on $Y_{t-1}, X_{t-1}$",
    ]  #  LaTeX-style labels for bar categories
    values = [r2_y, r2_xy]  #  restricted vs full model R^2 values

    fig, ax = plt.subplots(figsize=(4.5, 2.8))  #  create figure and axes
    bars = ax.bar(
        labels,
        values,
        color=["#001F5B", "#FF7F0E"],
    )  #  simple bar plot with brand-aligned colors

    y_max = max(values)  #  largest R^2 value
    ax.set_ylim(0.0, y_max * 1.35)  #  headroom for labels and title

    for bar, val in zip(bars, values):
        height = bar.get_height()  #  height of current bar
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.01,
            f"{val:.3f}",
            ha="center",
            va="bottom",
        )  #  annotate bars with numeric R^2 slightly above bar

    ax.set_ylabel(r"$R^2$")  #  y-axis label with math typesetting
    ax.set_title(r"Granger-style $R^2$ comparison")  #  descriptive title
    fig.tight_layout()  #  reduce unnecessary margins
    fig.savefig("figures/granger_r2_comparison.pdf", bbox_inches="tight")
    plt.close(fig)  #  free figure resources

    x, y = simulate_coupled_returns()
    r2_y, r2_xy = simple_granger_regression(x, y)
    print({"R2_y_only": r2_y, "R2_y_and_x": r2_xy})  #  simple textual summary


if __name__ == "__main__":
    main()
