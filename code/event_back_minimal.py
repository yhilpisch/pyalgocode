from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
Minimal event-based backtest using daily prices for a single instrument.
The design follows the architecture sketched in Section 7:
DataHandler -> Strategy -> Portfolio -> Execution, all connected
through a simple event queue processed by BacktestEngine.

(c) Dr. Yves J. Hilpisch
AI-Powered by GPT 5.1
The Python Quants GmbH | https://tpq.io
https://hilpisch.com | https://linktr.ee/dyjh
"""

plt.style.use("seaborn-v0_8")


# --- Event types ------------------------------------------------------------


@dataclass
class Event:
    """Base class for all events."""

    type: str  #  marker for dispatch in the event loop


@dataclass
class MarketEvent(Event):
    """Represents a new market bar for a single instrument."""

    time_index: pd.Timestamp  #  timestamp of the new bar
    price: float  #  last traded price


@dataclass
class SignalEvent(Event):
    """Represents a directional trading signal (+1 long, -1 short, 0 flat)."""

    time_index: pd.Timestamp
    signal: float


@dataclass
class OrderEvent(Event):
    """Represents an order to change position to target units."""

    time_index: pd.Timestamp
    quantity: float


from pathlib import Path

DATA_URL = ("https://raw.githubusercontent.com/yhilpisch/epatcode/"
            "refs/heads/main/data/epat_eod.csv")


@dataclass
class FillEvent(Event):
    """Represents an immediate fill of an order at the current price."""

    time_index: pd.Timestamp
    quantity: float
    price: float


# --- Core components --------------------------------------------------------


class CSVDataHandler:
    """Streams daily prices from a CSV file as MarketEvent objects."""

    def __init__(self, path: str="data/epat_eod.csv",
                 column: str="EURUSD") -> None:
        local_path = Path(path)
        if local_path.is_file():
            src: str | Path = local_path
        else:
            src = DATA_URL
            print(f"Local data file {local_path} not found, loading from {DATA_URL}")
        df = pd.read_csv(src, parse_dates=["Date"]).set_index("Date")
        prices = df[column].astype(float).dropna()  #  clean symbol series
        self.prices = prices
        self.iterator = iter(prices.items())
        self.continue_backtest = True

    def update_bars(self, events: Deque[Event]) -> None:
        """Push the next MarketEvent into the event queue."""
        try:
            time_index, price = next(self.iterator)
        except StopIteration:
            self.continue_backtest = False
            return
        events.append(MarketEvent(type="MARKET", time_index=time_index, price=price))


class SimpleMomentumStrategy:
    """Generates signals based on the sign of yesterday's return."""

    def __init__(self, threshold: float=0.0175) -> None:
        """Initialize strategy with a log-return threshold.

        Only moves with absolute log-return larger than ``threshold``
        generate signals, which reduces unnecessary turnover when
        daily price changes are very small.
        """
        self.threshold = threshold
        self.last_price: float | None = None

    def on_market_event(self, event: MarketEvent, events: Deque[Event]) -> None:
        """Create a SignalEvent whenever a new bar arrives."""
        if self.last_price is None:
            self.last_price = event.price
            return
        ret = np.log(event.price / self.last_price)
        if abs(ret) < self.threshold:
            # ignore small moves to avoid over-trading
            self.last_price = event.price
            return
        self.last_price = event.price
        signal = np.sign(ret)  # +1 after up-move, -1 after down-move
        events.append(
            SignalEvent(type="SIGNAL", time_index=event.time_index, signal=signal)
        )


class NaiveExecutionHandler:
    """Fills orders immediately at the current market price."""

    def on_order_event(self, event: OrderEvent, events: Deque[Event]) -> None:
        """Convert an OrderEvent into a FillEvent with the same quantity."""
        # The portfolio passes in the price it observed with the order.
        events.append(
            FillEvent(
                type="FILL",
                time_index=event.time_index,
                quantity=event.quantity,
                price=0.0,  # overwritten by portfolio when processing fill
            )
        )


class SimplePortfolio:
    """Tracks position, cash, and equity for a single-instrument strategy."""

    def __init__(self, initial_cash: float=1.0) -> None:
        self.initial_cash = initial_cash
        self.position = 0.0  #  number of units held (can be negative)
        self.cash = initial_cash
        self.equity_history: List[float] = []
        self.dates: List[pd.Timestamp] = []
        self.latest_price: float | None = None  #  last observed market price

    def on_market_event(self, event: MarketEvent) -> None:
        """Update equity based on the latest market price."""
        self.latest_price = event.price
        equity = self.cash + self.position * event.price
        self.equity_history.append(equity)
        self.dates.append(event.time_index)

    def on_signal_event(self, event: SignalEvent, events: Deque[Event]) -> None:
        """Translate a trading signal into an order for target position."""
        if self.latest_price is None:
            return
        target_position = event.signal  # long 1 unit or short 1 unit
        quantity = target_position - self.position  # change from current position
        if quantity != 0.0:
            events.append(
                OrderEvent(
                    type="ORDER",
                    time_index=event.time_index,
                    quantity=quantity,
                )
            )

    def on_fill_event(self, event: FillEvent) -> None:
        """Apply fill to position and cash; assume fill at latest price."""
        if self.latest_price is None:
            return
        trade_value = event.quantity * self.latest_price
        self.position += event.quantity
        self.cash -= trade_value


class BacktestEngine:
    """Coordinates data, strategy, portfolio, and execution components."""

    def __init__(self, data_handler: CSVDataHandler,
                 strategy: SimpleMomentumStrategy,
                 portfolio: SimplePortfolio,
                 execution: NaiveExecutionHandler) -> None:
        self.data_handler = data_handler
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution = execution
        self.events: Deque[Event] = deque()

    def run(self) -> None:
        """Main event loop: process data, signals, orders, and fills."""
        while self.data_handler.continue_backtest:
            self.data_handler.update_bars(self.events)

            while self.events:
                event = self.events.popleft()
                if event.type == "MARKET":
                    assert isinstance(event, MarketEvent)
                    self.strategy.on_market_event(event, self.events)
                    self.portfolio.on_market_event(event)
                elif event.type == "SIGNAL":
                    assert isinstance(event, SignalEvent)
                    self.portfolio.on_signal_event(event, self.events)
                elif event.type == "ORDER":
                    assert isinstance(event, OrderEvent)
                    self.execution.on_order_event(event, self.events)
                elif event.type == "FILL":
                    assert isinstance(event, FillEvent)
                    self.portfolio.on_fill_event(event)


def plot_equity(dates: List[pd.Timestamp],
                equity: List[float],
                outfile: str="figures/event_back_minimal_equity.pdf") -> None:
    """Plot normalized equity curve for the event-based strategy."""
    eq_arr = np.asarray(equity)
    eq_norm = eq_arr / eq_arr[0]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(dates, eq_norm, label="Event-based momentum strategy on EURUSD")
    ax.set_xlabel("date")
    ax.set_ylabel("equity (normalized)")
    ax.set_title("Minimal event-based backtest on EURUSD")
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
    data_handler = CSVDataHandler()
    strategy = SimpleMomentumStrategy()
    portfolio = SimplePortfolio()
    execution = NaiveExecutionHandler()
    engine = BacktestEngine(data_handler, strategy, portfolio, execution)
    engine.run()
    plot_equity(portfolio.dates, portfolio.equity_history)

    eq_arr = np.asarray(portfolio.equity_history)
    eq_norm = eq_arr / eq_arr[0]

    # benchmark: buy-and-hold equity on the same dates
    prices_eff = data_handler.prices.loc[portfolio.dates]
    eq_bh = prices_eff.to_numpy() / float(prices_eff.iloc[0])

    # log-returns for benchmark and strategy
    log_ret_bh = np.diff(np.log(eq_bh))
    log_ret_strat = np.diff(np.log(eq_norm))

    ann_ret_bh = float(log_ret_bh.mean() * 252.0)
    ann_vol_bh = float(log_ret_bh.std(ddof=1) * np.sqrt(252.0))
    sharpe_bh = ann_ret_bh / ann_vol_bh if ann_vol_bh > 0.0 else float("nan")
    total_ret_bh = float(eq_bh[-1] - 1.0)
    max_dd_bh, dur_bh = max_drawdown_and_duration(eq_bh)

    ann_ret = float(log_ret_strat.mean() * 252.0)
    ann_vol = float(log_ret_strat.std(ddof=1) * np.sqrt(252.0))
    sharpe = ann_ret / ann_vol if ann_vol > 0.0 else float("nan")
    max_dd, dd_dur = max_drawdown_and_duration(eq_norm)
    total_ret = float(eq_norm[-1] - 1.0)

    summary = pd.DataFrame(
        {
            "final_equity": [eq_bh[-1], eq_norm[-1]],
            "total_return": [total_ret_bh, total_ret],
            "max_drawdown": [max_dd_bh, max_dd],
            "dd_duration": [dur_bh, dd_dur],
            "ann_return": [ann_ret_bh, ann_ret],
            "ann_vol": [ann_vol_bh, ann_vol],
            "sharpe": [sharpe_bh, sharpe],
        },
        index=["buy_and_hold", "event_momentum"],
    )

    print("Event-based momentum backtest (single instrument)")
    print(f"  periods={eq_norm.shape[0]}\n")
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
