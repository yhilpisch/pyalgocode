import numpy as np
import matplotlib.pyplot as plt

"""
Random-walk simulation and visualization for prices and returns.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

plt.style.use("seaborn-v0_8")


def simulate_random_walk(steps: int=252, paths: int=10,
                         mu: float=0.0, sigma: float=0.02,
                         s0: float=100.0) -> tuple[np.ndarray, np.ndarray]:
    """Simulate geometric random walk prices and log-returns.

    Parameters
    ----------
    steps : int
        Number of time steps (e.g. trading days).
    paths : int
        Number of independent simulated paths.
    mu : float
        Drift of the log-returns per step.
    sigma : float
        Volatility of the log-returns per step.
    s0 : float
        Initial price level.
    """
    rng = np.random.default_rng(seed=42)
    log_returns = rng.normal(mu, sigma, size=(steps, paths))
    log_returns[0] = 0.0  #  start all paths exactly at s0
    prices = s0 * np.exp(log_returns.cumsum(axis=0))  #  geometric random walk
    return prices, log_returns


def plot_random_walk(prices: np.ndarray, log_returns: np.ndarray,
                     outfile: str = "figures/random_walk_sim.pdf") -> None:
    """Plot price paths and log-return histogram and save to a file."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))

    ax1.plot(prices)  #  simulated price paths
    ax1.set_title("Random walk price paths")
    ax1.set_xlabel("time step")
    ax1.set_ylabel("price level")

    ax2.hist(log_returns.ravel(), bins=30, density=True, alpha=0.7)
    ax2.set_title("Histogram of simulated log-returns")
    ax2.set_xlabel("log-return")

    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    prices, log_returns = simulate_random_walk()
    plot_random_walk(prices, log_returns)

    mean_lr = float(log_returns.mean())
    std_lr = float(log_returns.std(ddof=1))
    print("Random-walk simulation summary")
    print(f"  log-return mean={mean_lr:.6f}, std={std_lr:.6f}")
    print(f"  first 5 log-returns={log_returns[:5, 0]}")
