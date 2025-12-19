"""
Vectorized lagged-returns OLS backtest on EURUSD.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_URL = ("https://raw.githubusercontent.com/yhilpisch/epatcode/"
            "refs/heads/main/data/epat_eod.csv")

plt.style.use("seaborn-v0_8")


def load_prices(path: str="data/epat_eod.csv",
                column: str="EURUSD") -> pd.Series:
    """Load end-of-day prices for a single instrument.

    Uses a local CSV file if available; otherwise falls back to the
    remote URL, letting :func:`pandas.read_csv` stream the data.
    """
    local_path = Path(path)
    if local_path.is_file():
        src: str | Path = local_path
    else:
        src = DATA_URL
        print(f"Local data file {local_path} not found, loading from {DATA_URL}")
    df = pd.read_csv(src, parse_dates=["Date"])
    df = df.set_index("Date")
    prices = df[column].astype(float).dropna()
    return prices


def make_lagged_returns(prices: pd.Series,
                        lags: int=7) -> tuple[np.ndarray, np.ndarray, pd.DatetimeIndex]:
    """Compute log-returns and build a lagged design matrix."""
    log_prices = np.log(prices.to_numpy())
    rets = np.diff(log_prices)  #  r_t = log S_t - log S_{t-1}
    dates = prices.index[1:]

    n = rets.shape[0]
    if n <= lags:
        raise ValueError("Not enough observations for the chosen number of lags.")

    X = np.column_stack(
        [rets[(lags - k):(n - k)] for k in range(1, lags + 1)]
    )  #  columns r_{t-1},...,r_{t-lags}
    y = rets[lags:]  #  target r_t
    dates_eff = dates[lags:]  #  effective dates for y and X rows
    return X, y, dates_eff


def fit_ols(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Estimate linear model y = beta_0 + X beta via OLS."""
    X_design = np.column_stack([np.ones(X.shape[0]), X])  #  add intercept column
    beta = np.linalg.lstsq(X_design, y, rcond=None)[0]
    return beta


def run_lag_strategy(X: np.ndarray, y: np.ndarray,
                     beta: np.ndarray,
                     cost: float=0.0001) -> np.ndarray:
    """Compute strategy returns from lagged OLS predictions."""
    X_design = np.column_stack([np.ones(X.shape[0]), X])
    y_pred = X_design @ beta  #  one-step-ahead forecasts

    pos = np.sign(y_pred)  #  -1, 0, or +1 depending on forecast sign
    strat_rets = pos * y  #  gross strategy returns; prediction for r_t applied to r_t

    turnover = np.abs(pos[1:] - pos[:-1])  #  trades per step
    strat_rets[1:] = strat_rets[1:] - cost * turnover  #  apply transaction costs
    return strat_rets


def plot_equity(dates: pd.DatetimeIndex,
                y: np.ndarray,
                strat_rets: np.ndarray,
                outfile: str="figures/vecback_lag_ols_equity.pdf") -> None:
    """Plot equity curves for buy-and-hold, strategy, and coin-flip control."""
    eq_bh = np.cumprod(1.0 + y)
    eq_strat = np.cumprod(1.0 + strat_rets)

    rng = np.random.default_rng(seed=42)
    coin_pos = rng.choice([-1.0, 1.0], size=y.shape[0])  #  random long/short
    coin_rets = coin_pos * y
    eq_coin = np.cumprod(1.0 + coin_rets)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(dates, eq_strat, label="Lag-OLS strategy")
    ax.plot(dates, eq_bh, label="Buy & hold (EURUSD)", ls="--", lw=1.0)
    ax.plot(dates, eq_coin, label="Coin-flip long/short", ls="-.", lw=1.0)

    ax.set_xlabel("date")
    ax.set_ylabel("normalized equity")
    ax.set_title("Vectorized lagged-returns strategy on EURUSD")
    ax.legend(loc="best")

    fig.tight_layout()
    fig.savefig(outfile, bbox_inches="tight")
    plt.close(fig)


def max_drawdown_and_duration(equity: np.ndarray) -> tuple[float, int]:
    """Compute maximum drawdown and its duration (in periods)."""
    peak = np.maximum.accumulate(equity)
    dd = equity / peak - 1.0  #  drawdown series (<= 0)
    underwater = dd < 0.0
    max_dur = 0
    cur = 0
    for flag in underwater:
        if flag:
            cur += 1
            if cur > max_dur:
                max_dur = cur
        else:
            cur = 0
    return float(dd.min()), int(max_dur)


if __name__ == "__main__":
    prices = load_prices()
    X, y, dates = make_lagged_returns(prices, lags=7)

    rows = min(5, y.shape[0])
    cols = min(X.shape[1], 7)
    diag_cols = [y[:rows]] + [X[:rows, k] for k in range(cols)]
    diag_labels = ["y_t"] + [f"r_t_minus_{k + 1}" for k in range(cols)]
    diag_df = pd.DataFrame(
        np.column_stack(diag_cols),
        columns=diag_labels,
        index=dates[:rows],
    )
    print("First rows of target and lagged returns")
    print(diag_df.round(6))

    beta = fit_ols(X, y)
    strat_rets = run_lag_strategy(X, y, beta)
    plot_equity(dates, y, strat_rets)

    bh_eq = np.cumprod(1.0 + y)
    strat_eq = np.cumprod(1.0 + strat_rets)

    total_ret_bh = float(bh_eq[-1] - 1.0)
    total_ret_strat = float(strat_eq[-1] - 1.0)

    max_dd_bh, dur_bh = max_drawdown_and_duration(bh_eq)
    max_dd_strat, dur_strat = max_drawdown_and_duration(strat_eq)

    ann_ret_bh = float(y.mean() * 252.0)
    ann_vol_bh = float(y.std(ddof=1) * np.sqrt(252.0))
    ann_ret_strat = float(strat_rets.mean() * 252.0)
    ann_vol_strat = float(strat_rets.std(ddof=1) * np.sqrt(252.0))

    sharpe_bh = ann_ret_bh / ann_vol_bh if ann_vol_bh > 0.0 else float("nan")
    sharpe_strat = (ann_ret_strat / ann_vol_strat
                    if ann_vol_strat > 0.0 else float("nan"))

    summary = pd.DataFrame(
        {
            "final_equity": [bh_eq[-1], strat_eq[-1]],
            "total_return": [total_ret_bh, total_ret_strat],
            "max_drawdown": [max_dd_bh, max_dd_strat],
            "dd_duration": [dur_bh, dur_strat],
            "ann_return": [ann_ret_bh, ann_ret_strat],
            "ann_vol": [ann_vol_bh, ann_vol_strat],
            "sharpe": [sharpe_bh, sharpe_strat],
        },
        index=["buy_and_hold", "lag_ols_strategy"],
    )

    print("Vectorized lagged-returns OLS backtest on EURUSD")
    print(f"  samples={y.shape[0]}, lags={X.shape[1]}\n")
    print(
        summary.round(
            {
                "final_equity": 3,
                "total_return": 3,
                "max_drawdown": 3,
                "ann_return": 4,
                "ann_vol": 4,
                "sharpe": 2,
            }
        ).T.to_string()
    )
