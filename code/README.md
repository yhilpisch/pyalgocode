<img src="https://hilpisch.com/tpq_logo_bic.png" width="25%" align="right">
<br>

# Python for Algorithmic Trading · Code Overview

This directory contains the Python scripts that accompany the article and slide deck on **Python for Algorithmic Trading: Efficient Markets, Backtesting, and Streaming**.
The scripts are organized in the same logical order as the article, moving from Efficient Market Hypothesis (EMH) benchmarks to vectorized and event-based backtests and finally to streaming architectures and causality diagnostics.

All scripts are written to be self-contained and executable from the project root, with figures saved into the `figures/` directory where applicable.


- &copy; Dr. Yves J. Hilpisch  
- AI-Powered by GPT 5.1  
- The Python Quants GmbH · <https://tpq.io>  
- <https://hilpisch.com> · <https://linktr.ee/dyjh>

The code is intended for educational and research purposes in the context of The Python Quants lecture series and related workshops.

---

## Section 2 · Efficient Markets and Random Walks

### `random_walk_sim.py`

Simulates geometric random-walk price paths and corresponding log-returns and produces a two-panel figure with:

- several sample price paths starting from a common initial level, and  
- a histogram of log-returns across all paths.

Key elements:

- `simulate_random_walk(...)` generates log-returns from an i.i.d. normal distribution, sets the first log-return to zero so all paths start exactly at the initial price, and exponentiates the cumulative sum to obtain prices.
- `plot_random_walk(...)` plots the simulated paths and return histogram and saves a PDF figure.

This script underpins the random-walk visualizations used when introducing EMH.

### `emh_efficiency_test.py`

Explores linear predictability of returns via autocorrelations in a controlled simulation setting.

Key elements:

- Simulates AR(1) return series with different autoregressive coefficients (for example, `rho = 0` for efficient returns and `rho = 0.3` for predictable returns).
- Implements a small helper to compute sample autocorrelations for multiple lags.
- Produces a figure comparing autocorrelation patterns for efficient and predictable returns, illustrating how departures from EMH show up in simple diagnostics.

The script provides the numerical and visual foundation for the “Testing for Linear Predictability” discussion.

---

## Section 4 · Regression and Signal Evaluation

### `ols_signal_example.py`

Demonstrates how ordinary least squares (OLS) regression can be used to relate strategy returns to a single trading signal.

Key elements:

- Generates synthetic signal values and strategy returns according to a simple linear model with added noise.
- Estimates the intercept and slope via NumPy’s least-squares solver.
- Produces a scatter plot of returns versus signal together with the fitted regression line to visualize the relationship.

This script illustrates the use of OLS as a diagnostic tool for signal evaluation before moving on to more complex strategies.

---

## Section 5 · Vectorized Backtesting with Python

### `vecback_lag_ols.py`

Implements a fully vectorized backtest of a lagged-returns OLS strategy on daily **EURUSD** data.

Key elements:

- Loads EURUSD prices from `data/epat_eod.csv` and converts them to log-returns.
- Builds a design matrix of lagged returns (for example, seven lags) and fits an OLS model to predict the next return.
- Converts predictions into long/short positions using the sign of the forecast, lagged by one day to avoid look-ahead bias.
- Applies a simple proportional transaction-cost model based on turnover.
- Constructs equity curves for:
  - a buy-and-hold EURUSD benchmark,  
  - the lagged-returns OLS strategy, and  
  - a coin-flip long/short control strategy.

The resulting figure makes it easy to compare the strategy against trivial benchmarks and to discuss risk and performance metrics.

---

## Section 6 · Object-Oriented Programming for Quant Finance

### `vecback_lag_ols_oop.py`

Refactors the vectorized lagged-returns backtest into a small object-oriented design that is easier to reuse and extend.

Key elements:

- Defines a `LagOLSBacktest`-style class that encapsulates:
  - data loading,  
  - feature construction (lagged returns),  
  - parameter estimation (OLS fit), and  
  - equity-curve generation with transaction costs.
- Exposes clear methods such as `fit()`, `run_strategy()`, and `plot_equity()` so that different parameter choices (number of lags, cost assumptions) can be explored with minimal changes to calling code.

This script shows how to move from a one-off vectorized backtest towards more structured, reusable research code.

---

## Section 7 · Event-Based Backtesting

### `event_back_minimal.py`

Implements a minimal event-based backtest for a daily EURUSD momentum strategy, mirroring the architecture discussed in the article.

Key elements:

- Defines simple event classes for market data, signals, orders, and fills.
- Implements core components:
  - a data handler that emits one `MarketEvent` per bar from EURUSD prices,  
  - a strategy that generates long/short signals based on the sign of yesterday’s log-return,  
  - a portfolio that updates positions and equity on fills, and  
  - an execution handler that fills orders at the current price.
- Runs an event loop that processes events from a queue and records the evolving equity curve.

The resulting figure illustrates how even a small event-driven engine can approximate the behavior of a live trading setup.

---

## Section 8 · Real-Time and Streaming Data with ZeroMQ

### `tick_server.py`

Simulates a **EURUSD** tick stream and publishes messages over a ZeroMQ `PUB` socket.

Key elements:

- Maintains a synthetic EURUSD price as a random walk with small Gaussian shocks.
- Sends JSON messages with timestamp, symbol, and price fields at a configurable rate.
- Serves as a simple stand-in for a real market-data feed in local experiments.

### `tick_client.py`

Demonstrates how to subscribe to the tick stream and process messages in real time.

Key elements:

- Connects to the server’s `PUB` endpoint via a `SUB` socket.
- Subscribes to all symbols (or a subset, if desired).
- Prints incoming ticks to the console, serving as a lightweight monitoring or debugging tool.

### `tick_database.py`

Shows how to persist the same tick stream into a local SQLite database for later analysis.

Key elements:

- Uses a `SUB` socket to receive the same tick messages as `tick_client.py`.
- Inserts each tick into a simple `ticks` table with timestamp, symbol, and price columns.
- Provides a minimal template for building local tick archives or replay mechanisms.

Together, these three scripts demonstrate how ZeroMQ can be used to decouple data producers from multiple independent consumers (loggers, analytics, strategies).

---

## Section 9 · Correlation, Causation, and Granger Tests

### `granger_example.py`

Constructs a small synthetic system in which one return series **X** helps to predict another series **Y** and visualizes the difference in explanatory power between two regression models.

Key elements:

- Simulates coupled AR(1) processes where lagged values of \( X_t \) enter the equation for \( Y_t \).
- Fits two linear models:
  - a restricted regression of \( Y_t \) on its own lag only, and  
  - a full regression of \( Y_t \) on its own lag and lagged \( X_t \).
- Computes and prints the \( R^2 \) values for both models.
- Generates a bar-chart figure comparing the \( R^2 \) of the restricted and full regressions to illustrate Granger-style predictive content.

This script provides the numerical backbone for the Granger-causality discussion in the article and slides.

### `granger_statsmodels_example.py`

Applies standard Granger-causality tests from `statsmodels` to the same synthetic system.

Key elements:

- Reuses the data-generating process from `granger_example.py`.
- Calls `statsmodels.tsa.stattools.grangercausalitytests` in both directions:
  - tests whether **X** Granger-causes **Y**, and  
  - tests whether **Y** Granger-causes **X**.
- Prints F-test p-values for a range of lags so that the direction and strength of predictive relationships can be assessed using standard statistical machinery.

This script complements the hand-rolled regression example and shows how to connect conceptual Granger-causality ideas to widely used econometric tooling.

---

## Appendix · Strategy Metrics and Diagnostics

### `strategy_metrics.py`

Provides a reusable `StrategyMetrics` class that turns one or more P\&L or return series into a comprehensive metrics table.

Key elements:

- Accepts either P\&L levels $x_t$ or periodic returns $r_t$ for one or more strategies.
- Computes, for each series:
  - total and annualized return,
  - annualized volatility,
  - Sharpe and Sortino ratios,
  - maximum drawdown and drawdown duration,
  - hit rate and skewness of the return distribution, and
  - excess-return statistics relative to an optional benchmark.
- Returns a `pandas.DataFrame` with metrics as the index and series names as columns, ready to be exported or merged with other reports.
- In the main block, loads three instruments (`EURUSD`, `SPY`, `AAPL`) from `data/epat_eod.csv`, uses `SPY` as a benchmark, and prints a rounded overview of the metrics for all three.

- Each script can be explored independently, but running them in the order outlined above mirrors the narrative progression of the article from EMH benchmarks to streaming and causality analysis.
## Usage Notes

- All scripts assume a standard virtual Python environment with `numpy`, `pandas`, `matplotlib`, and, where applicable, `statsmodels`, `pyzmq`, and `sqlite3` installed.
- Paths to data files (`data/epat_eod.csv`) and output figures (`figures/...`) are relative to the project root.
- Each script can be explored independently, but running them in the order outlined above mirrors the narrative progression of the article from EMH benchmarks to streaming and causality analysis.
