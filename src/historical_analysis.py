"""Run Kairon's descriptive historical signal evaluation workflow."""

from __future__ import annotations

import csv
from pathlib import Path

from fetch_market_data import get_klines
from historical_report_generator import generate_historical_evaluation_markdown
from historical_signal_evaluation import FORWARD_HORIZONS, evaluate_historical_signals
from market_condition import SIGNAL_ORDER


SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
HISTORICAL_CANDLE_LIMIT = 365
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
REPORTS_FOLDER = PROJECT_ROOT / "reports"
HISTORICAL_OCCURRENCES_CSV_PATH = (
    DATA_FOLDER / "kairon_historical_signal_occurrences.csv"
)
HISTORICAL_REPORT_PATH = (
    REPORTS_FOLDER / "kairon_historical_signal_evaluation_latest.md"
)
OCCURRENCE_CSV_COLUMNS = [
    "asset",
    "date",
    "signal_timestamp",
    "price",
    "signal",
    "sma_7",
    "sma_21",
    "rsi_14",
    "change_7d",
    "forward_return_1d",
    "forward_timestamp_1d",
    "forward_return_3d",
    "forward_timestamp_3d",
    "forward_return_7d",
    "forward_timestamp_7d",
]
OCCURRENCE_CSV_COLUMNS.extend(
    column
    for horizon in FORWARD_HORIZONS
    for column in (
        f"conditional_return_pct_{horizon}d",
        f"unconditional_return_pct_{horizon}d",
        f"relative_difference_pct_{horizon}d",
        f"sample_count_{horizon}d",
        f"incomplete_future_window_count_{horizon}d",
        f"effective_n_note_{horizon}d",
    )
)


def _display_path(path: Path) -> str:
    """Return a repository-relative path for terminal output."""
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def fetch_historical_candles(
    symbols: list[str] = SYMBOLS,
    candle_limit: int = HISTORICAL_CANDLE_LIMIT,
) -> dict[str, list[dict]]:
    """Fetch public historical candles without exchange authentication."""
    candles_by_asset = {}

    for symbol in symbols:
        try:
            candles_by_asset[symbol.upper()] = get_klines(
                symbol,
                interval="1d",
                limit=candle_limit,
            )
        except RuntimeError as error:
            print(f"Historical data unavailable for {symbol}: {error}")

    return candles_by_asset


def write_occurrence_csv(
    evaluation: dict,
    csv_path: Path = HISTORICAL_OCCURRENCES_CSV_PATH,
) -> None:
    """Write detailed historical signal occurrences to CSV."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=OCCURRENCE_CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(
            {
                column: occurrence.get(column)
                for column in OCCURRENCE_CSV_COLUMNS
            }
            for occurrence in evaluation["occurrences"]
        )


def write_historical_report(
    evaluation: dict,
    report_path: Path = HISTORICAL_REPORT_PATH,
) -> None:
    """Generate and save the historical evaluation Markdown report."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = generate_historical_evaluation_markdown(evaluation).rstrip()
    report = f"{report}\n\n{generate_baseline_relative_markdown(evaluation)}"
    report_path.write_text(
        report,
        encoding="utf-8",
    )


def _format_report_percentage(value: float | None) -> str:
    """Format a baseline-relative percentage for Markdown."""
    if value is None:
        return "not available"
    return f"{value:+.2f}%"


def generate_baseline_relative_markdown(evaluation: dict) -> str:
    """Render the additive v0.5 baseline-relative report section."""
    horizons = evaluation["forward_horizons"]
    lines = [
        "## Baseline & Relative Signal Evaluation",
        "",
        (
            "Asset-level results are primary. Each conditional signal summary is "
            "compared with the unconditional return of the same asset and horizon "
            "over the fixed post-warm-up eligible asset-day population. Pooled "
            "results below are secondary occurrence-weighted descriptive context "
            "only."
        ),
        "",
        (
            "Relative difference equals conditional summary minus unconditional "
            "summary, reported separately for mean and median. Missing, zero, "
            "non-finite, or unavailable future prices are excluded without "
            "imputation."
        ),
        "",
        (
            "Occurrence-weighted pooled baseline means that, separately for each "
            "signal and horizon, each asset's unconditional return distribution "
            "receives a total weight equal to that asset's valid conditional "
            "occurrence count. Baseline asset-day counts do not determine the "
            "cross-asset weights. The pooled median is the deterministic weighted "
            "empirical median, not an average of asset medians."
        ),
        "",
        "### Asset-Level Results",
        "",
        (
            "| Asset | Signal | Horizon | Conditional mean | Unconditional mean | "
            "Relative mean | Conditional median | Unconditional median | "
            "Relative median | Conditional N | Conditional incomplete | "
            "Baseline N | Baseline incomplete |"
        ),
        (
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | "
            "---: | ---: | ---: | ---: | ---: |"
        ),
    ]

    for asset in evaluation["assets_evaluated"]:
        asset_results = evaluation["asset_baseline_relative_performance"].get(
            asset,
            {},
        )
        for signal, signal_results in asset_results.items():
            for horizon in horizons:
                result = signal_results[f"{horizon}d"]
                conditional = result["conditional_return_pct"]
                unconditional = result["unconditional_return_pct"]
                relative = result["relative_difference_pct"]
                lines.append(
                    "| "
                    f"{asset} | {signal} | {horizon}D | "
                    f"{_format_report_percentage(conditional['mean'])} | "
                    f"{_format_report_percentage(unconditional['mean'])} | "
                    f"{_format_report_percentage(relative['mean'])} | "
                    f"{_format_report_percentage(conditional['median'])} | "
                    f"{_format_report_percentage(unconditional['median'])} | "
                    f"{_format_report_percentage(relative['median'])} | "
                    f"{result['sample_count']} | "
                    f"{result['incomplete_future_window_count']} | "
                    f"{result['unconditional_sample_count']} | "
                    f"{result['unconditional_incomplete_future_window_count']} |"
                )

    lines.extend(
        [
            "",
            "### Pooled Secondary Context",
            "",
            (
                "These pooled rows combine raw observations across assets for "
                "each signal. Their baseline statistics use the signal/horizon "
                "occurrence composition described above. They can hide "
                "asset-level heterogeneity and are descriptive context only; do "
                "not generalize them beyond the evaluated observations."
            ),
            "",
            (
                "| Signal | Horizon | Conditional mean | Unconditional mean | "
                "Relative mean | Conditional median | Unconditional median | "
                "Relative median | Conditional N | Conditional incomplete | "
                "Baseline N | Baseline incomplete |"
            ),
            (
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | "
                "---: | ---: | ---: | ---: |"
            ),
        ]
    )

    for signal, signal_results in evaluation[
        "pooled_baseline_relative_performance"
    ].items():
        for horizon in horizons:
            result = signal_results[f"{horizon}d"]
            conditional = result["conditional_return_pct"]
            unconditional = result["unconditional_return_pct"]
            relative = result["relative_difference_pct"]
            lines.append(
                "| "
                f"{signal} | {horizon}D | "
                f"{_format_report_percentage(conditional['mean'])} | "
                f"{_format_report_percentage(unconditional['mean'])} | "
                f"{_format_report_percentage(relative['mean'])} | "
                f"{_format_report_percentage(conditional['median'])} | "
                f"{_format_report_percentage(unconditional['median'])} | "
                f"{_format_report_percentage(relative['median'])} | "
                f"{result['sample_count']} | "
                f"{result['incomplete_future_window_count']} | "
                f"{result['unconditional_sample_count']} | "
                f"{result['unconditional_incomplete_future_window_count']} |"
            )

    lines.extend(
        [
            "",
            (
                "Effective sample-size note: raw counts are descriptive and are "
                "not independent sample claims; overlapping windows, "
                "autocorrelation, cross-asset dependence, pooled heterogeneity, "
                "multiple horizons, and data-snooping limitations require "
                "cautious interpretation. Rule and horizon choices remain fixed."
            ),
        ]
    )
    return "\n".join(lines)


def run_historical_evaluation() -> dict:
    """Fetch public data, evaluate signals, and export both report formats."""
    candles_by_asset = fetch_historical_candles()
    evaluation = evaluate_historical_signals(
        candles_by_asset,
        horizons=FORWARD_HORIZONS,
    )
    write_occurrence_csv(evaluation)
    write_historical_report(evaluation)
    return evaluation


def print_completion_summary(evaluation: dict) -> None:
    """Print the concise completion summary for the standalone workflow."""
    assets = ", ".join(evaluation["assets_evaluated"]) or "none"
    horizons = ", ".join(f"{horizon}D" for horizon in FORWARD_HORIZONS)

    print()
    print("Historical Signal Evaluation complete.")
    print(f"Assets evaluated: {assets}")
    print(f"Market data period: {evaluation['market_data_period']}")
    print(
        "Valid signal period: "
        f"{evaluation['valid_signal_evaluation_period']}"
    )
    print(f"Raw historical observations: {evaluation['total_occurrences']}")
    print(f"Signals evaluated: {len(SIGNAL_ORDER)}")
    print(f"Forward horizons: {horizons}")
    print()
    print("Report:")
    print(_display_path(HISTORICAL_REPORT_PATH))
    print()
    print("Data:")
    print(_display_path(HISTORICAL_OCCURRENCES_CSV_PATH))


def main() -> None:
    """Run the standalone historical evaluation workflow."""
    evaluation = run_historical_evaluation()
    print_completion_summary(evaluation)


if __name__ == "__main__":
    main()
