<img src="https://hilpisch.com/tpq_logo_bic.png" width="25%" align="right">
<br>

# Python for Algorithmic Trading · Jupyter Notebooks

The notebooks in this directory provide interactive, narrative walk-throughs of the main topics covered in the article and slide deck on **Python for Algorithmic Trading: Efficient Markets, Backtesting, and Streaming**.
They are ordered to mirror the progression of the article, from Efficient Market Hypothesis (EMH) benchmarks to vectorized and event-based backtests and finally to streaming architectures.

Each notebook combines Markdown explanations with fully commented Python code so that readers can execute, modify, and extend the examples step by step.

---

## Meta Information

- &copy; Dr. Yves J. Hilpisch  
- AI-Powered by GPT 5.x  
- The Python Quants GmbH · <https://tpq.io>  
- <https://hilpisch.com> · <https://linktr.ee/dyjh>

The notebooks are intended for educational use in The Python Quants lecture series and related trainings; they assume a working Python environment with the dependencies used in the article.

---

## `1_emh_tests.ipynb` · Efficient Markets and Random Walks (Section 2)

**Goal.** Turn the EMH and random-walk discussion into executable experiments.

Highlights:

- Introduces a `simulate_random_walk(...)` helper that generates geometric random-walk prices and log-returns (with the first log-return set to zero so paths start exactly at the initial level).
- Visualizes:
  - sample random-walk price paths, and  
  - the empirical distribution of log-returns.
- Implements an AR(1) simulator and a hand-rolled `autocorr(...)` function to compute sample autocorrelations.
- Compares autocorrelation patterns for:
  - efficient returns (`rho = 0.0`), and  
  - predictable returns (`rho = 0.3`).
- Adds a small OLS-based AR(1) test that prints lag-1 coefficients and t-statistics as a first check for linear predictability.

The notebook is the interactive companion to the article’s EMH benchmark and testing section.

---

## `2_vec_backtest_ols.ipynb` · Vectorized Lagged-Returns Strategy (Section 5)

**Goal.** Develop the lagged-returns OLS backtest on EURUSD in a transparent, vectorized way.

Highlights:

- Loads daily EURUSD prices from `data/epat_eod.csv` and inspects the series.
- Defines `make_lagged_returns(...)` to:
  - compute log-returns,  
  - build a design matrix of lagged returns (by default seven lags), and  
  - align dates with the effective sample.
- Fits an OLS model using `fit_ols(...)`, which adds an intercept and solves the normal equations via NumPy.
- Translates predictions into positions with `run_lag_strategy(...)`:
  - positions are the sign of the forecast, lagged by one day,  
  - turnover drives a simple proportional transaction-cost model.
- Constructs and plots normalized equity curves for:
  - buy-and-hold EURUSD,  
  - the lagged-returns OLS strategy, and  
  - a coin-flip long/short benchmark.

Narrative Markdown cells explain how each step maps to the mathematical description in the article and how to adapt the design to different lags, features, or assets.

---

## `3_event_backtest_momentum.ipynb` · Event-Based Backtest (Section 7)

**Goal.** Show how to move from vectorized backtests to an event-based architecture using a minimal daily momentum strategy.

Highlights:

- Defines simple event dataclasses:
  - `MarketEvent`, `SignalEvent`, `OrderEvent`, and `FillEvent`.
- Implements the four core components described in the article:
  - `CSVDataHandler` streams EURUSD prices from `data/epat_eod.csv` as market events,  
  - `SimpleMomentumStrategy` emits signals based on the sign of yesterday’s log-return,  
  - `SimplePortfolio` tracks position, cash, and equity over time, and  
  - `NaiveExecutionHandler` converts orders into fills at the latest observed price.
- Wraps everything into a small `BacktestEngine` that processes events from a `deque`, mirroring the architectural diagram from the slides.
- Runs the backtest and plots a normalized equity curve for the event-based momentum strategy.

The notebook emphasizes control flow and state management, making it easier to see how research backtests can evolve into architectures that resemble live systems.

---

## `4_streaming_zeroMQ.ipynb` · Streaming with ZeroMQ (Section 8)

**Goal.** Demonstrate how to attach strategies and analytics to a real-time tick stream using ZeroMQ, and how to compute online statistics on the fly.

Highlights:

- Implements `run_tick_server(...)`:
  - publishes synthetic EURUSD ticks (random-walk prices) over a `PUB` socket,  
  - sends small JSON messages with timestamp, symbol, and price.
- Implements `run_print_client(...)`:
  - subscribes to the same endpoint via a `SUB` socket,  
  - prints each tick to the console as it arrives.
- Implements `online_mean_var(...)` and `run_stats_client(...)`:
  - maintains a running mean and variance of log-returns without storing the full history,  
  - periodically prints updated estimates (for example, every 50 ticks).
- Includes practical notes on running server and clients in separate processes or terminals so that learners can observe the streaming behavior live.

This notebook connects the event-based backtest to a streaming context and shows how the same concepts can power paper-trading or monitoring tools.

---

## How to Use These Notebooks

- Work through the notebooks in numerical order (from `1_emh_tests.ipynb` to `4_streaming_zeroMQ.ipynb`) to follow the article’s narrative arc.
- Treat each notebook as a starting point:
  - change parameters (lags, AR(1) coefficients, cost assumptions),  
  - experiment with additional indicators or events, and  
  - adapt the streaming examples to your own data sources or endpoints.
- For reference implementations that generate the figures in the article and slides, see the Python scripts described in `code/README.md`.
