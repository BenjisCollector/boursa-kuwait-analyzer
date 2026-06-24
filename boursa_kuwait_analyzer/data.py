"""Data ingestion for the Boursa Kuwait Stock Analyzer.

`load_prices` is real, working pandas code that reads a CSV of daily close
prices. `fetch_prices` is a documented stub: it describes where real Boursa
Kuwait market data would come from and, for now, falls back to the bundled
illustrative sample so the rest of the pipeline runs end-to-end.
"""

from __future__ import annotations

import os

import pandas as pd

# Path to the bundled, clearly-synthetic sample data.
_SAMPLE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "sample_data",
    "kuwait_banks_sample.csv",
)


def load_prices(path: str) -> pd.DataFrame:
    """Load a CSV of daily close prices into a DataFrame.

    The CSV is expected to have a ``date`` column plus one column per ticker
    of close prices, e.g.::

        date,NBK,KFH,GBK,BOUBYAN
        2024-01-01,1.000,0.750,0.300,0.620
        2024-01-02,1.004,0.748,0.301,0.623

    Lines beginning with ``#`` are treated as comments and skipped, so the
    sample file can carry an inline "illustrative data" disclaimer.

    Returns a DataFrame indexed by a parsed, sorted DatetimeIndex, with one
    float column per ticker.
    """
    df = pd.read_csv(path, comment="#", parse_dates=["date"])
    df = df.set_index("date").sort_index()

    # Coerce every price column to numeric (non-parseable values -> NaN).
    df = df.apply(pd.to_numeric, errors="coerce")

    return df


def fetch_prices(tickers: list[str]) -> pd.DataFrame:
    """Fetch daily close prices for the given tickers.

    TODO (real Boursa Kuwait ingestion — NOT YET IMPLEMENTED)
    --------------------------------------------------------
    There is no clean, free public API for Boursa Kuwait market data. A real
    implementation would source prices from one of:

      * Boursa Kuwait's own market-data offering / official end-of-day files
        (https://www.boursakuwait.com.kw/) — typically licensed.
      * A licensed market-data vendor (e.g. Refinitiv/LSEG, Bloomberg, or a
        regional data provider) that carries Boursa Kuwait (XKUW) symbols.
      * A broker API with Kuwait market entitlements.

    The real version would:
      1. Map each logical ticker (NBK, KFH, ...) to the vendor's symbol.
      2. Request daily close prices over the desired date range (likely via
         ``requests`` against the vendor's REST endpoint, with auth).
      3. Normalise the response into the same wide DataFrame shape that
         ``load_prices`` returns (date index, one column per ticker).

    Until that exists, this stub returns the bundled illustrative sample so the
    pipeline runs. The returned data is SYNTHETIC and must not be treated as
    real market prices.
    """
    df = load_prices(_SAMPLE_PATH)

    # Return only the requested tickers that are present in the sample.
    available = [t for t in tickers if t in df.columns]
    if not available:
        return df
    return df[available]
