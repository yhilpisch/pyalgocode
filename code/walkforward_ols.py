"""
Expanding-window walk-forward backtest for lagged-returns OLS strategy.

Python for Algorithmic Trading
Walk-Forward Validation Example
(c) Dr. Yves J. Hilpisch
AI-Powered by different LLMs
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

import numpy as np
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/epat_eod.csv")
DATA_URL = "https://hilpisch.com/epat_eod.csv"


def load_prices(path: str="data/epat_eod.csv",
                column: str="EURUSD") -> pd.Series:
    """Load end-of-day prices for a single instrument."""
    local_path = Path(path)
    src = local_path if local_path.is_file() else DATA_URL
    df = pd.read_csv(src, parse_dates=["Date"]).set_index("Date")
    prices = df[column].astype(float).dropna()
    return prices


class WalkForwardOLS:
    """Expanding-window lagged-returns OLS backtest."""

    def __init__(self, prices: pd.Series,
                 lags: int=7, cost: float=0.0001) -> None:
        self.prices = prices
        self.lags = lags
        self.cost = cost

    def _build_features(self) -> tuple[np.ndarray,
                                       np.ndarray,
                                       pd.DatetimeIndex]:
        """Convert prices to log-returns and lagged design matrix."""
        rets = np.diff(np.log(self.prices.to_numpy()))
        n = rets.shape[0]
        if n <= self.lags:
            raise ValueError("not enough observations")
        X = np.column_stack(
            [rets[(self.lags - k):(n - k)]
             for k in range(1, self.lags + 1)]
        )  # columns r_{t-1},...,r_{t-lags}
        y = rets[self.lags:]  # target r_t
        dates = self.prices.index[(self.lags + 1):]
        return X, y, dates

    @staticmethod
    def _fit_ols(X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Estimate y = beta_0 + X beta via OLS."""
        Xd = np.column_stack([np.ones(X.shape[0]), X])
        return np.linalg.lstsq(Xd, y, rcond=None)[0]

    def run(self, min_train: int=252,
            step: int=21) -> pd.Series:
        """Expanding-window walk-forward.

        Start with ``min_train`` observations, fit OLS, predict
        the next ``step`` bars, then expand the training set
        and repeat.
        """
        X, y, dates = self._build_features()
        n = X.shape[0]
        equity = [1.0]
        eq_dates = [dates[0]]
        i = min_train
        while i < n:
            end = min(i + step, n)
            beta = self._fit_ols(X[:i], y[:i])
            Xd_te = np.column_stack(
                [np.ones(end - i), X[i:end]]
            )
            pos = np.sign(Xd_te @ beta)
            rets = pos * y[i:end]
            turnover = np.abs(np.diff(pos))
            rets[1:] -= self.cost * turnover
            for r in rets:
                equity.append(equity[-1] * np.exp(float(r)))
            eq_dates.extend(dates[i:end])
            i = end
        return pd.Series(equity, index=eq_dates)


if __name__ == "__main__":
    prices = load_prices()
    wf = WalkForwardOLS(prices, lags=7, cost=0.0001)
    eq = wf.run(min_train=500, step=21)
    print(f"Final equity: {eq.iloc[-1]:.3f}")
    print(f"Observations: {len(eq)}")
