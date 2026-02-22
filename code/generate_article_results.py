from __future__ import annotations

import csv
from pathlib import Path

import emh_efficiency_test as eet
import event_back_minimal as ebm
import granger_example as ge
import ols_signal_example as ose
import random_walk_sim as rws
import numpy as np
import vecback_lag_ols as vbo


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "epat_eod.csv"
FIG_DIR = ROOT / "figures"
OUT_FILE = ROOT / "generated" / "results_values.tex"


def _fmt_num(value: float, digits: int=3) -> str:
    return f"{value:.{digits}f}"


def _fmt_pct(value: float, digits: int=2) -> str:
    return f"{100.0 * value:.{digits}f}\\%"


def _annualized_stats(log_returns: np.ndarray) -> dict[str, float]:
    ann_ret = float(log_returns.mean() * 252.0)
    ann_vol = float(log_returns.std(ddof=1) * np.sqrt(252.0))
    sharpe = ann_ret / ann_vol if ann_vol > 0.0 else float("nan")
    return {"ann_ret": ann_ret, "ann_vol": ann_vol, "sharpe": float(sharpe)}


def _vectorized_results() -> dict[str, float]:
    prices = vbo.load_prices(path=str(DATA_FILE), column="EURUSD")
    x_mat, y, dates = vbo.make_lagged_returns(prices, lags=7)
    beta = vbo.fit_ols(x_mat, y)
    strat_rets = vbo.run_lag_strategy(x_mat, y, beta, cost=0.0001)

    vbo.plot_equity(
        dates,
        y,
        strat_rets,
        outfile=str(FIG_DIR / "vecback_lag_ols_equity.pdf"),
    )

    eq_bh = np.exp(np.cumsum(y))
    eq_strat = np.exp(np.cumsum(strat_rets))

    mdd_bh, _ = vbo.max_drawdown_and_duration(eq_bh)
    mdd_strat, _ = vbo.max_drawdown_and_duration(eq_strat)

    stats_bh = _annualized_stats(y)
    stats_strat = _annualized_stats(strat_rets)

    return {
        "bh_total": float(eq_bh[-1] - 1.0),
        "bh_sharpe": stats_bh["sharpe"],
        "bh_mdd": mdd_bh,
        "strat_total": float(eq_strat[-1] - 1.0),
        "strat_sharpe": stats_strat["sharpe"],
        "strat_mdd": mdd_strat,
    }


def _event_results() -> dict[str, float]:
    data_handler = ebm.CSVDataHandler(path=str(DATA_FILE), column="EURUSD")
    strategy = ebm.SimpleMomentumStrategy()
    portfolio = ebm.SimplePortfolio()
    execution = ebm.NaiveExecutionHandler()
    engine = ebm.BacktestEngine(data_handler, strategy, portfolio, execution)
    engine.run()

    ebm.plot_equity(
        portfolio.dates,
        portfolio.equity_history,
        outfile=str(FIG_DIR / "event_back_minimal_equity.pdf"),
    )

    eq_arr = np.asarray(portfolio.equity_history)
    eq_norm = eq_arr / eq_arr[0]

    prices_eff = data_handler.prices.loc[portfolio.dates]
    eq_bh = prices_eff.to_numpy() / float(prices_eff.iloc[0])

    log_ret_bh = np.diff(np.log(eq_bh))
    log_ret_evt = np.diff(np.log(eq_norm))

    mdd_bh, _ = ebm.max_drawdown_and_duration(eq_bh)
    mdd_evt, _ = ebm.max_drawdown_and_duration(eq_norm)

    stats_bh = _annualized_stats(log_ret_bh)
    stats_evt = _annualized_stats(log_ret_evt)

    return {
        "bh_total": float(eq_bh[-1] - 1.0),
        "bh_sharpe": stats_bh["sharpe"],
        "bh_mdd": mdd_bh,
        "evt_total": float(eq_norm[-1] - 1.0),
        "evt_sharpe": stats_evt["sharpe"],
        "evt_mdd": mdd_evt,
    }


def _diagnostic_results() -> dict[str, float]:
    x_sig, r_sig = ose.simulate_signal_and_returns()
    alpha_hat, beta_hat = ose.ols_fit(x_sig, r_sig)

    ose.plot_signal_regression(
        x_sig,
        r_sig,
        alpha_hat,
        beta_hat,
        outfile=str(FIG_DIR / "ols_signal_example.pdf"),
    )

    x_design = np.column_stack([np.ones_like(x_sig), x_sig])
    r_hat = x_design @ np.array([alpha_hat, beta_hat])
    ss_tot = np.sum((r_sig - r_sig.mean()) ** 2)
    ss_res = np.sum((r_sig - r_hat) ** 2)
    r2_ols = float(1.0 - ss_res / ss_tot)

    x_g, y_g = ge.simulate_coupled_returns()
    r2_y, r2_xy = ge.simple_granger_regression(x_g, y_g)

    ge.main()
    prices_rw, log_returns_rw = rws.simulate_random_walk()
    rws.plot_random_walk(
        prices_rw,
        log_returns_rw,
        outfile=str(FIG_DIR / "random_walk_sim.pdf"),
    )
    eet.plot_efficiency_example(outfile=str(FIG_DIR / "emh_efficiency_test.pdf"))

    return {
        "alpha_hat": alpha_hat,
        "beta_hat": beta_hat,
        "r2_ols": r2_ols,
        "r2_y": r2_y,
        "r2_xy": r2_xy,
    }


def _dataset_meta() -> dict[str, str]:
    """Extract basic metadata (date span and symbols) from the CSV file."""
    with DATA_FILE.open("r", encoding="utf-8", newline="") as fobj:
        reader = csv.reader(fobj)
        header = next(reader)
        first_row = next(reader)
        last_row = first_row
        for row in reader:
            last_row = row

    symbols = [col for col in header if col != "Date"]
    symbols_upper = [sym.upper() for sym in symbols]
    symbols_tex = ", ".join(f"\\textsc{{{sym}}}" for sym in symbols_upper)

    return {
        "start": first_row[0],
        "end": last_row[0],
        "symbols": symbols_tex,
        "n_symbols": str(len(symbols)),
    }


def _cmd(name: str, value: str) -> str:
    return f"\\renewcommand{{\\{name}}}{{{value}}}"


def _write_values(vec_res: dict[str, float], evt_res: dict[str, float],
                  diag_res: dict[str, float]) -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data_meta = _dataset_meta()

    lines = [
        "% Generated result values for article.tex",
        _cmd("ResVecBHTotal", _fmt_pct(vec_res["bh_total"])),
        _cmd("ResVecStratTotal", _fmt_pct(vec_res["strat_total"])),
        _cmd("ResVecBHSharpe", _fmt_num(vec_res["bh_sharpe"], 2)),
        _cmd("ResVecStratSharpe", _fmt_num(vec_res["strat_sharpe"], 2)),
        _cmd("ResVecBHMDD", _fmt_pct(vec_res["bh_mdd"])),
        _cmd("ResVecStratMDD", _fmt_pct(vec_res["strat_mdd"])),
        _cmd("ResEvtBHTotal", _fmt_pct(evt_res["bh_total"])),
        _cmd("ResEvtStratTotal", _fmt_pct(evt_res["evt_total"])),
        _cmd("ResEvtBHSharpe", _fmt_num(evt_res["bh_sharpe"], 2)),
        _cmd("ResEvtStratSharpe", _fmt_num(evt_res["evt_sharpe"], 2)),
        _cmd("ResEvtBHMDD", _fmt_pct(evt_res["bh_mdd"])),
        _cmd("ResEvtStratMDD", _fmt_pct(evt_res["evt_mdd"])),
        _cmd("ResOLSAlpha", _fmt_num(diag_res["alpha_hat"], 6)),
        _cmd("ResOLSBeta", _fmt_num(diag_res["beta_hat"], 6)),
        _cmd("ResOLSRTwo", _fmt_num(diag_res["r2_ols"], 3)),
        _cmd("ResGrangerRTwoY", _fmt_num(diag_res["r2_y"], 3)),
        _cmd("ResGrangerRTwoXY", _fmt_num(diag_res["r2_xy"], 3)),
        _cmd("ResDataStart", data_meta["start"]),
        _cmd("ResDataEnd", data_meta["end"]),
        _cmd("ResDataSymbols", data_meta["symbols"]),
        _cmd("ResDataSymbolCount", data_meta["n_symbols"]),
        "",
    ]

    OUT_FILE.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    vec_res = _vectorized_results()
    evt_res = _event_results()
    diag_res = _diagnostic_results()
    _write_values(vec_res, evt_res, diag_res)
    print(f"Wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
