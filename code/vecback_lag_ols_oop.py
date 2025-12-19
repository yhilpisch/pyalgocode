"""
Object-oriented lagged-returns OLS backtest on EURUSD.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

plt.style.use("seaborn-v0_8")


DATA_URL = ("https://raw.githubusercontent.com/yhilpisch/epatcode/"
            "refs/heads/main/data/epat_eod.csv")


class LagOLSBacktest:
    """Lagged-returns OLS vectorized backtest.

    This class loads daily prices for a single instrument, converts them
    to log-returns, builds a lagged design matrix, fits a linear model
    of returns on their own lags, and derives a simple long/short
    strategy from the sign of the model's forecast.
    """

    def __init__(self, csv_path: str="data/epat_eod.csv",
                 column: str="EURUSD", lags: int=7, cost: float=0.0001) -> None:
        """Initialize backtest with data source, lags, and cost model."""
        self.csv_path = csv_path  # path to CSV file with EOD prices
        self.column = column  # instrument column to trade
        self.lags = lags  # number of past returns used as predictors
        self.cost = cost  # proportional transaction cost parameter
        # read raw prices and prepare lagged-return features once
        self._load_data()
        self._prepare_data()
        self.beta: np.ndarray | None = None
        self.strat_rets: np.ndarray | None = None

    def _load_data(self) -> None:
        """Load end-of-day prices for the configured instrument."""
        local_path = Path(self.csv_path)
        if local_path.is_file():
            src: str | Path = local_path
        else:
            src = DATA_URL
            print(f"Local data file {local_path} not found, loading from {DATA_URL}")
        df = pd.read_csv(src, parse_dates=["Date"]).set_index("Date")
        prices = df[self.column].astype(float).dropna()  # ensure numeric, drop gaps
        self.prices = prices  # pandas Series indexed by date

    def _prepare_data(self) -> None:
        """Convert prices to log-returns and assemble lagged design matrix."""
        log_prices = np.log(self.prices.to_numpy())  # work with log prices
        rets = np.diff(log_prices)  # daily log-returns r_t
        dates = self.prices.index[1:]  # dates aligned with returns
        n = rets.shape[0]  # sample size in returns
        if n <= self.lags:
            raise ValueError("not enough observations for chosen lags")
        X = np.column_stack(
            [rets[(self.lags - k):(n - k)] for k in range(1, self.lags + 1)]
        )  # columns r_{t-1},...,r_{t-lags}
        y = rets[self.lags:]  # target r_t
        self.X = X  # feature matrix
        self.y = y  # dependent variable
        self.dates = dates[self.lags:]  # effective backtest dates

    def fit(self) -> None:
        """Estimate regression coefficients for return on lagged returns."""
        X_design = np.column_stack([np.ones(self.X.shape[0]), self.X])
        self.beta = np.linalg.lstsq(X_design, self.y, rcond=None)[0]  # OLS solution

    def run_strategy(self) -> np.ndarray:
        """Compute strategy returns implied by the fitted model."""
        if self.beta is None:
            self.fit()
        X_design = np.column_stack([np.ones(self.X.shape[0]), self.X])
        y_pred = X_design @ self.beta  # one-step-ahead return forecasts
        pos = np.sign(y_pred)  # desired position based on forecast sign
        strat_rets = pos * self.y  # gross strategy returns
        turnover = np.abs(pos[1:] - pos[:-1])  # trade size per step
        strat_rets[1:] = strat_rets[1:] - self.cost * turnover  # apply costs
        self.strat_rets = strat_rets  # cache for reuse
        self.pos = pos  # realized positions
        return strat_rets

    def equity_curves(self) -> pd.DataFrame:
        """Return buy-and-hold and strategy equity curves as a DataFrame."""
        if self.strat_rets is None:
            self.run_strategy()
        eq_bh = np.cumprod(1.0 + self.y)  # buy & hold equity curve
        eq_strat = np.cumprod(1.0 + self.strat_rets)  # type: ignore[arg-type]
        return pd.DataFrame(
            {"eq_bh": eq_bh, "eq_strat": eq_strat},
            index=self.dates,
        )

    def plot_equity(self, outfile: str | None=None) -> None:
        """Plot equity curves and optionally save them to disk."""
        curves = self.equity_curves()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(curves.index, curves["eq_bh"], label="Buy & hold (EURUSD)")
        ax.plot(curves.index, curves["eq_strat"], label="Lag-OLS strategy")
        ax.set_xlabel("date")
        ax.set_ylabel("equity (normalized)")
        ax.set_title("LagOLSBacktest equity curves")
        ax.legend(loc="best")
        fig.tight_layout()
        if outfile is not None:
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
    backtest = LagOLSBacktest()
    strat_rets = backtest.run_strategy()
    backtest.plot_equity(outfile="figures/vecback_lag_ols_oop_equity.pdf")

    curves = backtest.equity_curves()
    eq_bh = curves["eq_bh"].to_numpy()
    eq_strat = curves["eq_strat"].to_numpy()

    total_ret_bh = float(eq_bh[-1] - 1.0)
    total_ret_strat = float(eq_strat[-1] - 1.0)

    max_dd_bh, dur_bh = max_drawdown_and_duration(eq_bh)
    max_dd_strat, dur_strat = max_drawdown_and_duration(eq_strat)

    ann_ret_bh = float(backtest.y.mean() * 252.0)
    ann_vol_bh = float(backtest.y.std(ddof=1) * np.sqrt(252.0))
    ann_ret_strat = float(strat_rets.mean() * 252.0)
    ann_vol_strat = float(strat_rets.std(ddof=1) * np.sqrt(252.0))

    sharpe_bh = ann_ret_bh / ann_vol_bh if ann_vol_bh > 0.0 else float("nan")
    sharpe_strat = (ann_ret_strat / ann_vol_strat
                    if ann_vol_strat > 0.0 else float("nan"))

    summary = pd.DataFrame(
        {
            "final_equity": [eq_bh[-1], eq_strat[-1]],
            "total_return": [total_ret_bh, total_ret_strat],
            "max_drawdown": [max_dd_bh, max_dd_strat],
            "dd_duration": [dur_bh, dur_strat],
            "ann_return": [ann_ret_bh, ann_ret_strat],
            "ann_vol": [ann_vol_bh, ann_vol_strat],
            "sharpe": [sharpe_bh, sharpe_strat],
        },
        index=["buy_and_hold", "lag_ols_strategy"],
    )

    print("LagOLSBacktest (OOP) on EURUSD")
    print(f"  samples={backtest.y.shape[0]}, lags={backtest.lags}, "
          f"cost={backtest.cost}\n")
    print(
        summary.round(
            {
                "final_equity": 3,
                "total_return": 3,
                "max_drawdown": 3,
                "dd_duration": 0,
                "ann_return": 4,
                "ann_vol": 4,
                "sharpe": 2,
            }
        ).T.to_string()
    )
