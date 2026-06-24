"""Boursa Kuwait Stock Analyzer.

Early scaffold (work in progress). Loads daily close prices for Kuwaiti bank
stocks, computes quantitative portfolio metrics, and uses Claude to produce a
qualitative position assessment.
"""

__version__ = "0.1.0"

# Major Kuwaiti banks listed on Boursa Kuwait that this project targets.
# Tickers are working identifiers for the scaffold, not official exchange symbols.
TARGET_BANKS = {
    "NBK": "National Bank of Kuwait",
    "KFH": "Kuwait Finance House",
    "GBK": "Gulf Bank",
    "BOUBYAN": "Boubyan Bank",
    "BURG": "Burgan Bank",
    "CBK": "Commercial Bank of Kuwait",
    "AUB": "Ahli United Bank",
    "WARBA": "Warba Bank",
}
