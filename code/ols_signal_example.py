import numpy as np
import matplotlib.pyplot as plt

"""
Synthetic signal/return regression example for OLS diagnostics.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

plt.style.use("seaborn-v0_8")


def simulate_signal_and_returns(
    steps: int=250,
    alpha_true: float=0.0005,
    beta_true: float=0.1,
    sigma_eps: float=0.02,
) -> tuple[np.ndarray, np.ndarray]:
    """Simulate a simple linear relation between signal and returns.

    Parameters
    ----------
    steps : int
        Number of observations to simulate.
    alpha_true : float
        Intercept of the data-generating process.
    beta_true : float
        Slope of the data-generating process with respect to the signal.
    sigma_eps : float
        Standard deviation of the noise term.
    """
    rng = np.random.default_rng(seed=7)
    x = rng.normal(0.0, 1.0, size=steps)  #  synthetic signal series
    eps = rng.normal(0.0, sigma_eps, size=steps)  #  noise term
    r = alpha_true + beta_true * x + eps  #  linear relation plus noise
    return x, r


def ols_fit(x: np.ndarray, r: np.ndarray) -> tuple[float, float]:
    """Estimate alpha and beta via ordinary least squares."""
    X = np.column_stack([np.ones_like(x), x])  #  design matrix with intercept
    alpha_hat, beta_hat = np.linalg.lstsq(X, r, rcond=None)[0]
    return float(alpha_hat), float(beta_hat)


def plot_signal_regression(
    x: np.ndarray,
    r: np.ndarray,
    alpha_hat: float,
    beta_hat: float,
    outfile: str="figures/ols_signal_example.pdf",
) -> None:
    """Create scatter plot and fitted regression line for signal vs returns."""
    x_line = np.linspace(x.min(), x.max(), 100)  #  grid for fitted line
    r_line = alpha_hat + beta_hat * x_line

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.scatter(x, r, alpha=0.5, label="simulated returns")
    ax.plot(x_line, r_line, color="tab:red", linewidth=2, label="OLS fit")

    ax.set_xlabel("signal $x_t$")
    ax.set_ylabel("strategy return $r_t$")
    ax.set_title("Signal vs strategy returns with OLS fit")
    ax.legend(loc="best")

    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    x, r = simulate_signal_and_returns()
    alpha_hat, beta_hat = ols_fit(x, r)
    plot_signal_regression(x, r, alpha_hat, beta_hat)

    X = np.column_stack([np.ones_like(x), x])
    r_hat = X @ np.array([alpha_hat, beta_hat])
    ss_tot = np.sum((r - r.mean()) ** 2)
    ss_res = np.sum((r - r_hat) ** 2)
    r2 = 1.0 - ss_res / ss_tot

    print("Synthetic OLS signal example")
    print(f"  alpha_true=0.0005, alpha_hat={alpha_hat:.6f}")
    print(f"  beta_true=0.1000,  beta_hat={beta_hat:.6f}")
    print(f"  R^2={r2:.3f}")
