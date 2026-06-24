"""Quantitative portfolio metrics on a price DataFrame.

All functions operate on a wide DataFrame of daily close prices (date index,
one column per ticker), as produced by ``data.load_prices`` /
``data.fetch_prices``. The finance math here is real and standard.

Conventions
-----------
* ``TRADING_DAYS = 252`` is the usual annualisation factor for daily data.
* "Returns" are simple (arithmetic) daily returns: r_t = P_t / P_{t-1} - 1.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Standard number of trading days per year, used to annualise daily figures.
TRADING_DAYS = 252


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Simple daily returns from close prices.

    r_t = P_t / P_{t-1} - 1. The first row is NaN (no prior price) and is
    dropped, so the result has one fewer row than ``prices``.
    """
    return prices.pct_change().dropna(how="all")


def annualised_return(prices: pd.DataFrame) -> pd.Series:
    """Annualised mean return per ticker (arithmetic).

    Mean daily simple return scaled by TRADING_DAYS. This is the arithmetic
    annualisation, consistent with how the Sharpe ratio below is built from
    daily means; it is not a geometric/CAGR figure.
    """
    returns = daily_returns(prices)
    return returns.mean() * TRADING_DAYS


def annualised_volatility(prices: pd.DataFrame) -> pd.Series:
    """Annualised volatility (standard deviation of returns) per ticker.

    Daily return std scaled by sqrt(TRADING_DAYS), the standard variance-scales-
    linearly-with-time assumption. Uses the sample std (ddof=1, pandas default).
    """
    returns = daily_returns(prices)
    return returns.std() * np.sqrt(TRADING_DAYS)


def sharpe_ratio(prices: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.Series:
    """Annualised Sharpe ratio per ticker.

    Sharpe = (annualised return - risk_free_rate) / annualised volatility.

    ``risk_free_rate`` is an *annual* rate expressed as a decimal (e.g. 0.04
    for 4%). Tickers with zero volatility yield NaN (division by zero) rather
    than an infinity, which is the safer thing to surface.
    """
    ann_ret = annualised_return(prices)
    ann_vol = annualised_volatility(prices)

    # Avoid divide-by-zero: where vol is 0, the Sharpe ratio is undefined.
    excess = ann_ret - risk_free_rate
    return excess.divide(ann_vol.replace(0.0, np.nan))


def max_drawdown(prices: pd.DataFrame) -> pd.Series:
    """Maximum drawdown per ticker, as a negative fraction.

    The maximum drawdown is the largest peak-to-trough decline over the period:

        drawdown_t = P_t / (running max of P up to t) - 1
        max_drawdown = min over t of drawdown_t

    Returned values are <= 0 (e.g. -0.18 means a 18% peak-to-trough fall).
    """
    running_max = prices.cummax()
    drawdown = prices.divide(running_max) - 1.0
    return drawdown.min()


def herfindahl_index(weights) -> float:
    """Herfindahl-Hirschman Index (HHI) of portfolio concentration.

    HHI = sum of squared weights. ``weights`` may be a dict, list, Series, or
    array. Weights are normalised to sum to 1 before squaring, so the inputs do
    not need to be pre-normalised.

    Interpretation:
      * 1.0  -> fully concentrated in a single position.
      * 1/N  -> perfectly equal weights across N positions (the minimum).
    A lower HHI means a more diversified portfolio.
    """
    w = np.asarray(list(weights.values()) if isinstance(weights, dict) else weights,
                   dtype=float)

    total = w.sum()
    if total == 0:
        raise ValueError("weights sum to zero; cannot normalise")

    w = w / total
    return float(np.sum(w ** 2))


def summarise(prices: pd.DataFrame, risk_free_rate: float = 0.0) -> pd.DataFrame:
    """Convenience: per-ticker metrics table as a tidy DataFrame.

    Columns: annualised_return, annualised_volatility, sharpe_ratio,
    max_drawdown. One row per ticker.
    """
    return pd.DataFrame(
        {
            "annualised_return": annualised_return(prices),
            "annualised_volatility": annualised_volatility(prices),
            "sharpe_ratio": sharpe_ratio(prices, risk_free_rate),
            "max_drawdown": max_drawdown(prices),
        }
    )
