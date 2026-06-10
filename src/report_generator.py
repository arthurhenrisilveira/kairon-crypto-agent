"""Markdown report generation for Kairon Crypto Agent."""

from datetime import datetime


def _format_asset_list(symbols: list[str]) -> str:
    """Return a readable asset list for report sections."""
    return ", ".join(symbols) if symbols else "none"


def _get_market_condition(results: list[dict]) -> str:
    """Classify the broad market condition from generated signals."""
    watch_buy_count = sum(1 for item in results if item["signal"] == "WATCH_BUY")
    defensive_count = sum(
        1
        for item in results
        if item["signal"] in ["WEAKNESS_AVOID", "OVERSOLD_BUT_WEAK"]
    )

    if watch_buy_count >= 2:
        return "Risk-on"

    if defensive_count >= 2:
        return "Defensive"

    return "Neutral"


def _get_market_interpretation(market_condition: str) -> str:
    """Explain the broad market condition in beginner-friendly language."""
    if market_condition == "Risk-on":
        return (
            "Multiple assets are showing constructive watch-buy signals, "
            "which suggests a more favorable short-term crypto backdrop."
        )

    if market_condition == "Defensive":
        return (
            "Multiple assets are showing weakness or fragile oversold conditions, "
            "so caution is the dominant message."
        )

    return (
        "Signals are mixed across the tracked assets, so the market does not show "
        "a clear risk-on or defensive profile."
    )


def generate_markdown_report(results: list[dict], summary: dict) -> str:
    """Generate a Markdown market report from analysis results."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    market_condition = _get_market_condition(results)
    market_interpretation = _get_market_interpretation(market_condition)

    lines = [
        "# Kairon Crypto Agent — Market Report",
        "",
        "## Timestamp",
        "",
        timestamp,
        "",
        "## Market Condition",
        "",
        market_condition,
        "",
        "## Executive Summary",
        "",
        f"- Strongest asset: {summary['strongest_asset']}",
        f"- Weakest asset: {summary['weakest_asset']}",
        f"- Assets to watch: {_format_asset_list(summary['assets_to_watch'])}",
        f"- Assets to avoid: {_format_asset_list(summary['assets_to_avoid'])}",
        f"- Market interpretation: {market_interpretation}",
        "",
        "## Asset Analysis",
        "",
    ]

    for result in results:
        lines.extend(
            [
                f"### {result['symbol']}",
                "",
                f"- Current price: {result['current_price']:.2f}",
                f"- SMA 7: {result['sma_7']:.2f}",
                f"- SMA 21: {result['sma_21']:.2f}",
                f"- RSI 14: {result['rsi_14']:.2f}",
                f"- 7-day change: {result['change_7d']:.2f}%",
                f"- Signal: {result['signal']}",
                f"- Explanation: {result['explanation']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Research Context",
            "",
            (
                "Kairon also keeps a research layer based on the FGV Crypto vs "
                "Global Markets project, which suggests that global risk assets, "
                "especially NASDAQ, may be relevant context for BTC and major "
                "altcoins."
            ),
            "",
            "Reference: docs/research/fgv_crypto_global_markets_summary.md",
            "",
            "## Risk Note",
            "",
            (
                "This report is for educational analysis only. It does not execute "
                "trades and does not provide financial advice."
            ),
            "",
        ]
    )

    return "\n".join(lines)
