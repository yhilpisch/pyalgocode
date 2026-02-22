import numpy as np
import pandas as pd

"""
Computation of return and risk metrics for one or more P&L or return series.

The core class, StrategyMetrics, accepts either P&L levels `x_t` or periodic
returns `r_t` for one or several strategies, computes a suite of diagnostics,
and returns a pandas DataFrame whose rows are metrics and whose columns are
individual series.

The metrics mirror the concepts discussed in the appendix "When is a Strategy
`Good`?" of the accompanying article:

- total and annualized returns
- excess returns relative to an optional benchmark
- annualized volatility
- Sharpe and Sortino ratios
- maximum drawdown and drawdown duration
- hit rate and skewness of the return distribution

In the main block, three instruments from data/epat_eod.csv are loaded and
compared side by side using these metrics.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""


class StrategyMetrics:
    """Compute risk/return diagnostics for P&L or return series.

    Parameters
    ----------
    periods_per_year : int, optional
        Number of return observations per year, used for annualization.
        For daily data 252 is typical; for monthly data 12 would be used.
    risk_free_rate : float, optional
        Risk-free rate per period (expressed in the same units as the
        returns). For daily data this is usually a small number, for
        example 0.02 / 252 for 2% per year.
    sortino_target : float, optional
        Target return used in the Sortino ratio. Values below this level
        are treated as downside outcomes; the default of 0.0 interprets
        any negative return as downside.
    benchmark : pd.Series, optional
        Benchmark return series r_t^b used to compute excess returns.
        If provided, it must be aligned in time with the strategy
        returns; any mismatched dates are dropped.
    """

    def __init__(
        self,
        periods_per_year: int = 252,
        risk_free_rate: float = 0.0,
        sortino_target: float = 0.0,
        benchmark: pd.Series | None = None,
    ) -> None:
        self.periods_per_year = periods_per_year
        self.risk_free_rate = risk_free_rate
        self.sortino_target = sortino_target
        self.benchmark = benchmark

    @staticmethod
    def _to_returns_from_pnl(pnl: pd.Series) -> pd.Series:
        """Convert a P&L / equity series x_t into simple returns r_t."""
        pnl = pnl.sort_index()  # ensure chronological order
        rets = pnl.pct_change(fill_method=None).dropna()  # r_t = x_t/x_{t-1} - 1
        return rets

    def _ensure_returns(
        self, data: pd.Series | pd.DataFrame, from_pnl: bool
    ) -> pd.DataFrame:
        """Convert P&L to returns if requested and standardize to DataFrame."""
        if isinstance(data, pd.Series):
            data_df = data.to_frame(name=data.name or "series")
        else:
            data_df = data.copy()
        if from_pnl:
            data_df = data_df.apply(self._to_returns_from_pnl)
        data_df = data_df.dropna(how="all")  # drop rows that are all NaN
        return data_df

    def _align_with_benchmark(self, rets: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series | None]:
        """Align strategy returns with the benchmark if one is provided."""
        if self.benchmark is None:
            return rets, None
        bench = self.benchmark.sort_index().dropna()
        # align on common dates
        joint = rets.join(bench.to_frame("benchmark"), how="inner")
        rets_aligned = joint[rets.columns]
        bench_aligned = joint["benchmark"]
        return rets_aligned, bench_aligned

    @staticmethod
    def _max_drawdown_and_duration(equity: np.ndarray) -> tuple[float, int]:
        """Compute maximum drawdown and its duration for one equity curve."""
        peak = np.maximum.accumulate(equity)
        dd = equity / peak - 1.0  # drawdown series
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

    def _metric_dict_for_series(
        self,
        name: str,
        rets: pd.Series,
        bench_rets: pd.Series | None,
    ) -> dict[str, float]:
        """Compute metrics for a single return series."""
        rets_clean = rets.dropna()
        if rets_clean.empty:
            raise ValueError(f"no valid returns for series '{name}'")

        mu = float(rets_clean.mean())  # average periodic return
        sigma = float(rets_clean.std(ddof=1))  # periodic volatility

        # annualized quantities
        ann_ret = (1.0 + mu) ** self.periods_per_year - 1.0
        ann_vol = sigma * np.sqrt(self.periods_per_year)

        # total and annualized return from compounded equity
        equity = np.cumprod(1.0 + rets_clean.to_numpy())
        total_ret = float(equity[-1] - 1.0)

        # Sharpe ratio based on periodic risk-free rate
        rf = self.risk_free_rate
        excess_periodic = mu - rf
        sharpe = (
            excess_periodic / sigma * np.sqrt(self.periods_per_year)
            if sigma > 0.0
            else np.nan
        )

        # Sortino ratio using downside deviation
        target = self.sortino_target
        downside = rets_clean[rets_clean < target]  # downside tail
        if downside.empty:
            sortino = np.nan
        else:
            diff = downside - target
            sigma_down = float(np.sqrt((diff**2).mean()))
            sortino = (
                (mu - target)
                / sigma_down
                * np.sqrt(self.periods_per_year)
                if sigma_down > 0.0
                else np.nan
            )

        # drawdown statistics from equity curve
        max_dd, dd_dur = self._max_drawdown_and_duration(equity)

        # hit rate and skewness
        hit_rate = float((rets_clean > 0.0).mean())
        centered = rets_clean - mu
        if sigma > 0.0:
            skew = float(((centered / sigma) ** 3).mean())
        else:
            skew = np.nan

        # excess return metrics relative to benchmark, if provided
        if bench_rets is not None:
            aligned = rets_clean.to_frame("s").join(
                bench_rets.to_frame("b"), how="inner"
            )
            ex = aligned["s"] - aligned["b"]
            ex_mu = float(ex.mean())
            ex_sigma = float(ex.std(ddof=1))
            ex_ann_ret = (1.0 + ex_mu) ** self.periods_per_year - 1.0
            ex_ann_vol = ex_sigma * np.sqrt(self.periods_per_year)
            ex_sharpe = (
                ex_mu / ex_sigma * np.sqrt(self.periods_per_year)
                if ex_sigma > 0.0
                else np.nan
            )
        else:
            ex_ann_ret = np.nan
            ex_ann_vol = np.nan
            ex_sharpe = np.nan

        return {
            "total_return": total_ret,
            "ann_return": float(ann_ret),
            "ann_vol": float(ann_vol),
            "sharpe": float(sharpe),
            "sortino": float(sortino),
            "max_drawdown": max_dd,
            "dd_duration": float(dd_dur),
            "hit_rate": hit_rate,
            "skewness": float(skew),
            "ex_ann_return": float(ex_ann_ret),
            "ex_ann_vol": float(ex_ann_vol),
            "ex_sharpe": float(ex_sharpe),
        }

    def summarize_from_pnl(
        self, pnl: pd.Series | pd.DataFrame
    ) -> pd.DataFrame:
        """Compute metrics when input is one or more P&L series x_t.

        The index of the resulting DataFrame contains metric names;
        columns correspond to the individual series in the input.
        """
        rets = self._ensure_returns(pnl, from_pnl=True)
        rets_aligned, bench = self._align_with_benchmark(rets)

        metrics: dict[str, dict[str, float]] = {}
        for col in rets_aligned.columns:
            ser = rets_aligned[col]
            metrics[col] = self._metric_dict_for_series(col, ser, bench)

        result = pd.DataFrame(metrics)

        # Order metrics so that annualized and excess quantities are
        # grouped together, followed by risk and distributional stats.
        metric_order = [
            "total_return",
            "ann_return",
            "ex_ann_return",
            "ann_vol",
            "ex_ann_vol",
            "sharpe",
            "ex_sharpe",
            "sortino",
            "max_drawdown",
            "dd_duration",
            "hit_rate",
            "skewness",
        ]
        present = [m for m in metric_order if m in result.index]
        result = result.reindex(index=present)
        return result

    def summarize_from_returns(
        self, rets: pd.Series | pd.DataFrame
    ) -> pd.DataFrame:
        """Compute metrics when input is one or more return series r_t."""
        rets_df = self._ensure_returns(rets, from_pnl=False)
        rets_aligned, bench = self._align_with_benchmark(rets_df)

        metrics: dict[str, dict[str, float]] = {}
        for col in rets_aligned.columns:
            ser = rets_aligned[col]
            metrics[col] = self._metric_dict_for_series(col, ser, bench)

        result = pd.DataFrame(metrics)

        metric_order = [
            "total_return",
            "ann_return",
            "ex_ann_return",
            "ann_vol",
            "ex_ann_vol",
            "sharpe",
            "ex_sharpe",
            "sortino",
            "max_drawdown",
            "dd_duration",
            "hit_rate",
            "skewness",
        ]
        present = [m for m in metric_order if m in result.index]
        result = result.reindex(index=present)
        return result


def _load_prices(csv_path: str = "data/epat_eod.csv") -> pd.DataFrame:
    """Load daily prices for multiple instruments from the example CSV file."""
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    df = df.set_index("Date")
    prices = df.astype(float).dropna(how="all")  # drop rows with all NaN
    return prices


if __name__ == "__main__":
    # Example: compare three instruments from the example data set.
    prices_all = _load_prices()

    # Select three representative series; all are daily and fairly liquid.
    cols = ["EURUSD", "SPY", "AAPL"]
    prices = prices_all[cols]

    # Use SPY as a simple benchmark when computing excess-return metrics.
    benchmark_returns = prices["SPY"].pct_change(fill_method=None).dropna()

    metrics_engine = StrategyMetrics(
        periods_per_year=252,
        risk_free_rate=0.0,
        sortino_target=0.0,
        benchmark=benchmark_returns,
    )

    # Treat the three price columns as individual P&L series (indexed by date).
    summary = metrics_engine.summarize_from_pnl(prices)

    # Print a rounded overview with metrics as index and instruments as columns.
    print("Strategy metrics for selected instruments from data/epat_eod.csv\n")
    decimals = {
        "total_return": 3,
        "ann_return": 4,
        "ann_vol": 4,
        "sharpe": 2,
        "sortino": 2,
        "max_drawdown": 3,
        "dd_duration": 0,  # integer-style display (no decimals)
        "hit_rate": 3,
        "skewness": 3,
        "ex_ann_return": 4,
        "ex_ann_vol": 4,
        "ex_sharpe": 2,
    }

    # Build a string-formatted DataFrame so that each metric can use its
    # own number of decimal places (dd_duration without decimals, others
    # with the requested precision).
    formatted = summary.copy().astype(object)
    for metric, dec in decimals.items():
        if metric not in summary.index:
            continue
        for col in summary.columns:
            val = summary.loc[metric, col]
            if np.isnan(val):
                formatted.loc[metric, col] = "NaN"
            elif dec == 0:
                formatted.loc[metric, col] = f"{int(round(val))}"
            else:
                formatted.loc[metric, col] = f"{val:.{dec}f}"

    print(formatted.to_string())
