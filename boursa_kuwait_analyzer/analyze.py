"""Claude-assisted assessment of a Kuwaiti bank-stock portfolio.

This module turns the quantitative metrics computed in ``portfolio.py`` into a
plain-language prompt and asks Claude for a qualitative position assessment via
the official Anthropic SDK. The Claude call is optional: if no API key is
configured, ``assess_portfolio`` returns a clear message instead of failing.
"""

from __future__ import annotations

import os

import pandas as pd

# Default model for the assessment. Override via the ``model`` argument.
DEFAULT_MODEL = "claude-sonnet-4-6"


def build_prompt(
    metrics: pd.DataFrame,
    weights: dict[str, float] | None = None,
    hhi: float | None = None,
) -> str:
    """Build the assessment prompt from the metrics table and holdings.

    ``metrics`` is the per-ticker DataFrame from ``portfolio.summarise``.
    ``weights`` optionally maps ticker -> portfolio weight; ``hhi`` is the
    Herfindahl concentration index of those weights.
    """
    lines: list[str] = []
    lines.append(
        "You are assisting with portfolio management for a basket of Kuwaiti "
        "bank stocks listed (or intended to be listed) on Boursa Kuwait."
    )
    lines.append("")
    lines.append(
        "IMPORTANT: The figures below are computed from ILLUSTRATIVE, SYNTHETIC "
        "sample prices, not real market data. Treat them as a worked example. "
        "Do not present your assessment as real investment advice."
    )
    lines.append("")
    lines.append("Per-ticker metrics (annualised unless noted):")
    lines.append(metrics.round(4).to_string())
    lines.append("")

    if weights:
        lines.append("Current portfolio weights:")
        for ticker, weight in weights.items():
            lines.append(f"  {ticker}: {weight:.2%}")
        lines.append("")

    if hhi is not None:
        lines.append(
            f"Portfolio concentration (Herfindahl-Hirschman Index): {hhi:.4f} "
            "(1.0 = single position; 1/N = equal weights across N positions)."
        )
        lines.append("")

    lines.append(
        "Please give a concise assessment covering: (1) the risk/return profile "
        "of each position, (2) overall portfolio concentration and "
        "diversification, and (3) which positions warrant closer review and why. "
        "Be explicit that this is an illustrative analysis on synthetic data."
    )
    return "\n".join(lines)


def assess_portfolio(
    metrics: pd.DataFrame,
    weights: dict[str, float] | None = None,
    hhi: float | None = None,
    model: str = DEFAULT_MODEL,
) -> str:
    """Ask Claude for a qualitative assessment of the portfolio.

    Reads ``ANTHROPIC_API_KEY`` from the environment. If it is not set, returns
    a clear, non-fatal message so callers (e.g. the CLI) can run offline. Any
    SDK/runtime error is also caught and surfaced as a readable string rather
    than propagating.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return (
            "[Claude assessment skipped: ANTHROPIC_API_KEY is not set. "
            "Set it to enable the LLM-assisted assessment.]"
        )

    prompt = build_prompt(metrics, weights=weights, hhi=hhi)

    try:
        # Imported lazily so the rest of the package works without `anthropic`.
        from anthropic import Anthropic

        client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        # response.content is a list of content blocks; collect the text blocks.
        parts = [block.text for block in response.content if block.type == "text"]
        return "\n".join(parts).strip()
    except Exception as exc:  # noqa: BLE001 - surface any failure to the caller
        return f"[Claude assessment failed: {type(exc).__name__}: {exc}]"
