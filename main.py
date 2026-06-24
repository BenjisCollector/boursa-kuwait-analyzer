"""CLI entry point for the Boursa Kuwait Stock Analyzer.

Loads the bundled illustrative sample data, computes the quantitative metrics
table, prints it, and — only if an Anthropic API key is set — prints Claude's
qualitative assessment.

Run:
    python main.py
"""

from __future__ import annotations

from boursa_kuwait_analyzer import TARGET_BANKS, __version__
from boursa_kuwait_analyzer.analyze import assess_portfolio
from boursa_kuwait_analyzer.data import fetch_prices
from boursa_kuwait_analyzer.portfolio import herfindahl_index, summarise

# Illustrative equal-ish weights for the sample basket. Synthetic, not advice.
EXAMPLE_WEIGHTS = {
    "NBK": 0.40,
    "KFH": 0.30,
    "GBK": 0.20,
    "BOUBYAN": 0.10,
}

# Illustrative annual risk-free rate (decimal) used for the Sharpe ratio.
RISK_FREE_RATE = 0.04


def main() -> None:
    print(f"Boursa Kuwait Stock Analyzer v{__version__}")
    print("Status: early scaffold (work in progress)\n")
    print(
        "NOTE: sample_data is ILLUSTRATIVE / SYNTHETIC placeholder data — "
        "not real Boursa Kuwait prices.\n"
    )

    # fetch_prices is currently a documented stub returning the sample data.
    tickers = list(EXAMPLE_WEIGHTS.keys())
    prices = fetch_prices(tickers)

    print(f"Loaded {len(prices)} trading days for: {', '.join(prices.columns)}\n")

    # --- Quantitative metrics (runs fully offline) ---
    metrics = summarise(prices, risk_free_rate=RISK_FREE_RATE)
    print("Per-ticker metrics (annualised unless noted):")
    print(metrics.round(4).to_string())
    print()

    hhi = herfindahl_index(EXAMPLE_WEIGHTS)
    print("Portfolio holdings (illustrative weights):")
    for ticker, weight in EXAMPLE_WEIGHTS.items():
        print(f"  {ticker:8s} {TARGET_BANKS.get(ticker, ticker):28s} {weight:6.2%}")
    print(f"\nConcentration (Herfindahl-Hirschman Index): {hhi:.4f}")
    print(f"(equal-weight floor for {len(EXAMPLE_WEIGHTS)} positions = "
          f"{1 / len(EXAMPLE_WEIGHTS):.4f})\n")

    # --- Claude-assisted assessment (only if an API key is set) ---
    print("-" * 60)
    print("Claude assessment:")
    print("-" * 60)
    assessment = assess_portfolio(metrics, weights=EXAMPLE_WEIGHTS, hhi=hhi)
    print(assessment)


if __name__ == "__main__":
    main()
