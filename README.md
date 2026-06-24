# Boursa Kuwait Stock Analyzer

Pulls Boursa Kuwait market + bank financial data and uses Claude to assess
Kuwaiti bank-stock positions for portfolio management.

**Demonstrates: financial data engineering + quantitative portfolio analysis + LLM-assisted reasoning**

> **Status: early scaffold (work in progress).**
> The quantitative analytics run fully offline today. The Claude-assisted
> assessment runs when an Anthropic API key is provided. Real Boursa Kuwait
> data ingestion is **not yet implemented** (see the honest note below).

---

## What it does

```
            ┌──────────────┐      ┌──────────────────┐      ┌─────────────────────┐
   data ───▶│ data.py      │ ───▶ │ portfolio.py     │ ───▶ │ analyze.py          │
            │ load prices  │      │ compute metrics  │      │ Claude assessment   │
            └──────────────┘      └──────────────────┘      └─────────────────────┘
            CSV of daily          returns, volatility,       prompt summarising the
            close prices          Sharpe, max drawdown,      metrics + holdings →
                                  concentration (HHI)        Claude → text opinion
```

1. **Data** — `data.py` loads a CSV of daily close prices into a pandas
   DataFrame (`load_prices`). `fetch_prices` is a documented stub describing
   where real Boursa Kuwait data would be sourced.
2. **Metrics** — `portfolio.py` computes the standard quantitative measures
   used to size and risk-check positions (correct, commented finance math).
3. **Assessment** — `analyze.py` builds a prompt from the computed metrics and
   holdings and asks Claude for a qualitative portfolio assessment.

## Target banks

The project targets the major Kuwaiti banks listed on Boursa Kuwait:

| Ticker idea | Bank |
|-------------|------|
| NBK         | National Bank of Kuwait |
| KFH         | Kuwait Finance House |
| GBK         | Gulf Bank |
| BOUBYAN     | Boubyan Bank |
| BURG        | Burgan Bank |
| CBK         | Commercial Bank of Kuwait |
| AUB         | Ahli United Bank |
| WARBA       | Warba Bank |

## How to run

```bash
# 1. (optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. run the analyzer (works fully offline — prints the metrics table)
python main.py
```

Running `python main.py` with no API key computes and prints the metrics table
from the illustrative sample data and skips the Claude step with a clear message.

To enable the Claude-assisted assessment, set an Anthropic API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python main.py
```

## Honest notes (please read)

- **No fabricated results.** Nothing in this repo reports real Boursa Kuwait
  prices or returns. The numbers you see come from the clearly-synthetic
  sample data and are computed live.
- **`sample_data/kuwait_banks_sample.csv` is illustrative placeholder data, not
  real prices.** It exists only so the pipeline runs end-to-end offline.
- **Real Boursa Kuwait data ingestion is a TODO.** There is no clean free public
  API for Boursa Kuwait. `fetch_prices()` documents the intended real sources
  (Boursa Kuwait market data / a licensed market-data vendor) but currently
  returns the sample data so the scaffold runs.

## Project layout

```
boursa-kuwait-analyzer/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── main.py
├── boursa_kuwait_analyzer/
│   ├── __init__.py
│   ├── data.py          # load_prices (real) + fetch_prices (documented stub)
│   ├── portfolio.py     # returns, vol, Sharpe, max drawdown, HHI (real math)
│   └── analyze.py       # builds prompt + calls Claude
└── sample_data/
    └── kuwait_banks_sample.csv   # ILLUSTRATIVE synthetic prices only
```
