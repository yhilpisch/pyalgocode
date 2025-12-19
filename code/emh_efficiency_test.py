import numpy as np
import matplotlib.pyplot as plt

"""
Autocorrelation-based efficiency test for synthetic return series.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

plt.style.use("seaborn-v0_8")


def simulate_returns(steps: int=500, rho: float=0.0) -> np.ndarray:
    """Simulate AR(1) returns with parameter rho.

    Parameters
    ----------
    steps : int
        Number of time steps to simulate.
    rho : float
        Autoregressive parameter; rho=0.0 corresponds to serially
        independent returns, rho>0 introduces positive autocorrelation.
    """
    rng = np.random.default_rng(seed=3)
    eps = rng.normal(0.0, 0.02, size=steps)  #  daily shocks
    r = np.empty(steps)
    r[0] = eps[0]
    for t in range(1, steps):
        r[t] = rho * r[t - 1] + eps[t]  #  AR(1) recursion
    return r


def autocorr(x: np.ndarray, max_lag: int=10) -> np.ndarray:
    """Compute sample autocorrelation up to max_lag.

    Uses a direct definition based on centered data and the
    sample variance in the denominator.
    """
    x_centered = x - x.mean()
    denom = np.dot(x_centered, x_centered)  #  variance * (n - 1)
    acf = np.empty(max_lag)
    for k in range(1, max_lag + 1):
        num = np.dot(x_centered[:-k], x_centered[k:])  #  lag-k covariance
        acf[k - 1] = num / denom
    return acf


def plot_efficiency_example(outfile: str="figures/emh_efficiency_test.pdf") -> None:
    """Compare autocorrelation patterns for efficient and inefficient returns.

    The function generates two return series, computes their
    autocorrelation functions, and plots them with approximate
    95% confidence bands under the null of zero autocorrelation.
    """
    r_eff = simulate_returns(rho=0.0)  #  approximately efficient
    r_ineff = simulate_returns(rho=0.3)  #  clearly predictable

    max_lag = 10
    acf_eff = autocorr(r_eff, max_lag=max_lag)
    acf_ineff = autocorr(r_ineff, max_lag=max_lag)

    z = 1.96  #  normal quantile for 95% band
    n = len(r_eff)
    conf = z / np.sqrt(n)  #  approximate standard error of acf under null

    lags = np.arange(1, max_lag + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), sharey=True)

    ax1.axhspan(-conf, conf, color="lightgrey", alpha=0.5)  #  confidence band
    ax1.bar(lags, acf_eff, width=0.6, color="tab:blue")
    ax1.set_title("Approx. efficient (AR(1) with $\\rho=0$)")
    ax1.set_xlabel("lag")
    ax1.set_ylabel("autocorrelation")

    ax2.axhspan(-conf, conf, color="lightgrey", alpha=0.5)  #  confidence band
    ax2.bar(lags, acf_ineff, width=0.6, color="tab:orange")
    ax2.set_title("Predictable (AR(1) with $\\rho=0.3$)")
    ax2.set_xlabel("lag")

    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    r_eff = simulate_returns(rho=0.0)
    r_ineff = simulate_returns(rho=0.3)

    acf_eff = autocorr(r_eff, max_lag=10)
    acf_ineff = autocorr(r_ineff, max_lag=10)

    print("Approx. efficient AR(1) with rho=0.0")
    print(f"  mean={r_eff.mean():.6f}, std={r_eff.std(ddof=1):.6f}")
    print(f"  first three acf lags={acf_eff[:3]}")

    print("\nPredictable AR(1) with rho=0.3")
    print(f"  mean={r_ineff.mean():.6f}, std={r_ineff.std(ddof=1):.6f}")
    print(f"  first three acf lags={acf_ineff[:3]}")

    plot_efficiency_example()
