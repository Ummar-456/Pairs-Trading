# MSFT-AAPL Pairs Trading Strategy

## Overview

This repository contains a Python script implementing a statistical arbitrage pairs trading strategy using historical stock price data for Microsoft (MSFT) and Apple (AAPL). The strategy operates on the principle of mean reversion, identifying temporary mispricings in the relationship between the two stocks.

## Methodology

1.  **Data Acquisition:** Downloads the last 10 years of daily closing prices for MSFT and AAPL using the `yfinance` library.
2.  **Hedge Ratio Calculation:** Performs an Ordinary Least Squares (OLS) regression (`statsmodels`) with MSFT price as the dependent variable and AAPL price as the independent variable to determine the optimal hedge ratio.
3.  **Spread Calculation:** Computes the spread series as: `Spread = MSFT_Price - hedge_ratio * AAPL_Price`.
4.  **Signal Generation:**
    *   Calculates the rolling mean and standard deviation of the spread.
    *   Trading bands are set at `mean ± 1 * standard_deviation`.
    *   A **long entry** signal (Buy MSFT, Sell AAPL) is generated when the spread crosses below the lower band.
    *   A **short entry** signal (Sell MSFT, Buy AAPL) is generated when the spread crosses above the upper band.
    *   Positions are held until an opposite signal is triggered (using `ffill` for persistence).
5.  **Backtesting & Performance:**
    *   Calculates daily returns for the strategy based on the positions held.
    *   Computes the cumulative return of the strategy, assuming an initial investment of $20,000.
    *   Generates a plot of the cumulative portfolio value over time using `matplotlib`.
    *   Evaluates detailed performance metrics using the `quantstats` library.

## Key Libraries

*   `yfinance`: For downloading stock data.
*   `pandas`: For data manipulation and analysis.
*   `numpy`: For numerical operations.
*   `statsmodels`: For OLS regression.
*   `matplotlib`: For plotting results.
*   `quantstats`: For performance and risk analysis reporting.

## How to Run

1.  Ensure you have Python installed.
2.  Install the required libraries:
    ```
    pip install yfinance pandas numpy statsmodels matplotlib quantstats
    ```
3.  Execute the Python script:
    ```
    python your_script_name.py
    ```
    (Replace `your_script_name.py` with the actual filename).

## Performance Summary (Approx. 2015-05 to 2025-04)

The backtest yielded the following key performance indicators:

*   **Cumulative Return:** 484.24%
*   **CAGR:** 13.06%
*   **Sharpe Ratio:** 0.65
*   **Sortino Ratio:** 0.98
*   **Annual Volatility:** 39.63%
*   **Max Drawdown:** -66.67%
*   **Calmar Ratio:** 0.20

*(Note: Full metrics are outputted by the script using `quantstats`)*

## Visualization

The script outputs a plot (`Cumulative_Strategy_Returns.png`) showing the growth of the initial investment over the backtesting period.

## Disclaimer

This script is provided for educational and informational purposes only. It does not constitute financial advice or a recommendation to trade. Financial markets involve risk, and past performance is not indicative of future results. Use this code at your own risk.
