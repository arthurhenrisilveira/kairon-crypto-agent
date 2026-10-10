"""Markdown rendering for Kairon's historical signal evaluation."""

from __future__ import annotations

from historical_signal_evaluation import FORWARD_HORIZONS
from market_condition import SIGNAL_ORDER


def _format_return(value: float | None) -> str:
    """Format a return without hiding unavailable observations."""
    if value is None:
        return "not available"
    return f"{value:+.2f}%"


def _format_percentage(value: float | None) -> str:
    """Format a percentage statistic."""
    if value is None:
        return "not available"
    return f"{value:.2f}%"


def _format_observations(value: int) -> str:
    """Format an observation count for Markdown."""
    return str(value)


def _signal_overview_rows(evaluation: dict) -> list[str]:
    """Build rows for the pooled signal overview table."""
    rows = []
    signal_performance = evaluation["signal_performance"]

    for signal in SIGNAL_ORDER:
        signal_summary = signal_performance[signal]
        horizon_observations = [
            str(signal_summary[f"{horizon}d"]["observations"])
            for horizon in FORWARD_HORIZONS
        ]
        rows.append(
            "| "
            f"{signal} | {signal_summary['total_occurrences']} | "
            f"{' | '.join(horizon_observations)} |"
        )

    return rows


def _signal_evaluation_section(evaluation: dict) -> list[str]:
    """Build detailed pooled statistics for every signal and horizon."""
    lines = ["## Signal Evaluation", ""]
    signal_performance = evaluation["signal_performance"]

    for signal in SIGNAL_ORDER:
        lines.extend([f"### {signal}", ""])
        signal_summary = signal_performance[signal]

        for horizon in FORWARD_HORIZONS:
            horizon_key = f"{horizon}d"
            statistics = signal_summary[horizon_key]
            lines.extend(
                [
                    f"#### {horizon}-day forward performance",
                    "",
                    (
                        "- Valid historical observations: "
                        f"{_format_observations(statistics['observations'])}"
                    ),
                    f"- Average return: {_format_return(statistics['average_return'])}",
                    f"- Median return: {_format_return(statistics['median_return'])}",
                    (
                        "- Positive outcomes: "
                        f"{_format_percentage(statistics['positive_return_percentage'])}"
                    ),
                    (
                        "- Best observed return: "
                        f"{_format_return(statistics['best_observed_return'])}"
                    ),
                    (
                        "- Worst observed return: "
                        f"{_format_return(statistics['worst_observed_return'])}"
                    ),
                    f"- Sample note: {statistics['sample_size_note']}",
                    "",
                ]
            )

    return lines


def _asset_breakdown_section(evaluation: dict) -> list[str]:
    """Build compact descriptive tables for each asset and signal."""
    lines = [
        "## Asset-Level Breakdown",
        "",
        (
            "The tables below keep assets separate. Their pooled results should "
            "not be assumed to apply equally to every asset. Asset-level rows "
            "show the 7-day descriptive statistics; the pooled sections above "
            "show full statistics for all horizons."
        ),
        "",
    ]

    for asset in evaluation["assets_evaluated"]:
        lines.extend(
            [
                f"### {asset}",
                "",
                "| Signal | Raw occurrences | 1D valid obs | 3D valid obs | 7D valid obs | 7D average | 7D median | 7D positive |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )

        asset_summary = evaluation["asset_signal_performance"].get(asset, {})
        for signal in SIGNAL_ORDER:
            signal_summary = asset_summary.get(signal)
            if signal_summary is None:
                continue
            seven_day = signal_summary["7d"]
            lines.append(
                "| "
                f"{signal} | {signal_summary['total_occurrences']} | "
                f"{signal_summary['1d']['observations']} | "
                f"{signal_summary['3d']['observations']} | "
                f"{seven_day['observations']} | "
                f"{_format_return(seven_day['average_return'])} | "
                f"{_format_return(seven_day['median_return'])} | "
                f"{_format_percentage(seven_day['positive_return_percentage'])} |"
            )

        lines.append("")

    if not evaluation["assets_evaluated"]:
        lines.append("No asset-level historical results were available.")
        lines.append("")

    return lines


def _interpretation_for_signal(signal: str, seven_day: dict) -> str:
    """Create one neutral observation from a signal's 7-day statistics."""
    observations = seven_day["observations"]
    if observations == 0:
        return (
            f"No 7-day observations were available for {signal} in the available "
            "historical sample."
        )

    median_return = seven_day["median_return"]
    positive_percentage = seven_day["positive_return_percentage"]

    if median_return > 0 and positive_percentage > 50:
        return (
            f"Within the available historical sample, {signal} occurrences were "
            "followed by a positive median 7-day return, with positive returns "
            f"in {positive_percentage:.2f}% of valid observations."
        )

    if median_return < 0 and positive_percentage < 50:
        return (
            f"Within the available historical sample, {signal} occurrences were "
            "followed by a negative median 7-day return, with positive returns "
            f"in {positive_percentage:.2f}% of valid observations."
        )

    return (
        f"{signal} occurrences produced mixed subsequent outcomes in the "
        "available historical sample."
    )


def _research_interpretation_section(evaluation: dict) -> list[str]:
    """Build neutral, descriptive observations from pooled 7-day statistics."""
    lines = [
        "## Research Interpretation",
        "",
        (
            "These observations describe the available historical sample only. "
            "They are not recommendations, predictions, or evidence that a signal "
            "will behave similarly in the future."
        ),
        "",
    ]

    for signal in SIGNAL_ORDER:
        seven_day = evaluation["signal_performance"][signal]["7d"]
        lines.append(f"- {_interpretation_for_signal(signal, seven_day)}")

    lines.append("")
    return lines


def generate_historical_evaluation_markdown(evaluation: dict) -> str:
    """Generate a complete Markdown historical evaluation report."""
    assets = evaluation["assets_evaluated"]
    horizons = ", ".join(f"{horizon}D" for horizon in FORWARD_HORIZONS)

    lines = [
        "# Kairon Historical Signal Evaluation",
        "",
        (
            "Historical descriptive analysis only. Not investment guidance and not "
            "evidence of future performance."
        ),
        "",
        "## Methodology",
        "",
        (
            "Historical signals were generated using the existing Kairon strategy "
            "rules, with only the candles available on each historical signal day. "
            "No signal optimization or parameter modification was performed."
        ),
        "",
        (
            "Forward returns measure the percentage change from the signal-day "
            "closing price to the closing price 1, 3, or 7 days later. Missing "
            "future data is recorded as unavailable and excluded from statistics."
        ),
        "",
        (
            "Some historical candles are used only to initialize technical "
            "indicators such as SMA 21 and RSI 14. As a result, the valid signal "
            "evaluation period begins after the raw market-data period starts. "
            "Warm-up candles are not treated as missing signal observations."
        ),
        "",
        (
            "Forward-return windows may overlap when classifications occur on "
            "nearby dates. As a result, historical observations are not necessarily "
            "statistically independent."
        ),
        "",
        (
            "BTC, ETH, BNB, and SOL may respond to shared market conditions. "
            "Observations across assets are therefore also not necessarily "
            "independent."
        ),
        "",
        (
            "Observation counts represent raw historical signal occurrences. "
            "Because forward windows can overlap and assets can move together, "
            "these counts should not be interpreted as effective independent "
            "sample sizes."
        ),
        "",
        (
            "This report is descriptive historical analysis. An association between "
            "a classification and a later return does not imply future performance, "
            "causality, or a trading instruction."
        ),
        "",
        "## Dataset Summary",
        "",
        f"- Assets evaluated: {', '.join(assets) if assets else 'none'}",
        f"- Market data period: {evaluation['market_data_period']}",
        (
            "- Valid signal evaluation period: "
            f"{evaluation['valid_signal_evaluation_period']}"
        ),
        f"- Raw historical signal observations: {evaluation['total_occurrences']}",
        f"- Forward horizons: {horizons}",
        f"- Signals evaluated: {len(SIGNAL_ORDER)}",
        "",
        "## Signal Overview",
        "",
        "| Signal | Raw historical occurrences | 1D valid obs | 3D valid obs | 7D valid obs |",
        "| --- | ---: | ---: | ---: | ---: |",
        *_signal_overview_rows(evaluation),
        "",
        *_signal_evaluation_section(evaluation),
        *_asset_breakdown_section(evaluation),
        *_research_interpretation_section(evaluation),
        "## Limitations",
        "",
        "- The available historical time period is limited.",
        "- Market regimes can change, so historical associations may not persist.",
        "- Crypto assets can be volatile.",
        "- Asset selection and survivorship create limitations.",
        "- Technical indicators require a warm-up period before valid signals can be generated.",
        "- Forward-return windows can overlap, so observations are not necessarily independent.",
        "- Observations are not necessarily independent across assets because major crypto assets may share market drivers.",
        "- The evaluation uses a simple technical rule set.",
        "- No transaction costs, slippage, taxes, position sizing, or portfolio simulation are included.",
        "- No causal inference or statistical significance claim is made.",
        "- No adjusted effective sample-size calculation is performed.",
        "- Historical results do not guarantee future performance.",
        "",
        "## Educational Use Note",
        "",
        (
            "Kairon Crypto Agent is an educational and research project. Signals "
            "remain analytical classifications and should not be interpreted as "
            "buy, sell, or hold recommendations."
        ),
        "",
    ]

    return "\n".join(lines)
