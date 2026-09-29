"""Run public multi-asset market analysis reports for Kairon Crypto Agent."""

import csv
from datetime import datetime
from pathlib import Path

from backtesting import run_signal_backtest, summarize_backtest
from asset_explainability import generate_asset_explanation
from fetch_market_data import get_klines
from market_condition import (
    SIGNAL_ORDER,
    count_signals,
    determine_market_condition,
    explain_market_condition,
)
from report_generator import generate_markdown_report
from strategy_rules import generate_basic_signal


SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
BACKTEST_SYMBOL = "BTCUSDT"
BACKTEST_CANDLE_LIMIT = 180
BACKTEST_LOOKBACK_WINDOW = 21
BACKTEST_FORWARD_DAYS = 7
POSITIVE_STRUCTURE_SIGNALS = ["WATCH_BUY"]
FURTHER_OBSERVATION_SIGNALS = ["OVERSOLD_WATCH"]
EXTENDED_OR_TECHNICAL_CAUTION_SIGNALS = [
    "OVERBOUGHT_WAIT",
    "WEAKNESS_AVOID",
    "OVERSOLD_BUT_WEAK",
]
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FOLDER = PROJECT_ROOT / "data"
REPORTS_FOLDER = PROJECT_ROOT / "reports"
LATEST_CSV_PATH = DATA_FOLDER / "kairon_analysis_latest.csv"
HISTORY_CSV_PATH = DATA_FOLDER / "kairon_analysis_history.csv"
LATEST_MARKDOWN_REPORT_PATH = REPORTS_FOLDER / "kairon_market_report_latest.md"
BACKTEST_CSV_PATH = DATA_FOLDER / "kairon_backtest_btcusdt.csv"
BACKTEST_SUMMARY_PATH = REPORTS_FOLDER / "kairon_backtest_summary.md"
MULTI_ASSET_BACKTEST_CSV_PATH = DATA_FOLDER / "kairon_backtest_multi_asset.csv"
MULTI_ASSET_BACKTEST_SUMMARY_PATH = (
    REPORTS_FOLDER / "kairon_multi_asset_backtest_summary.md"
)
CSV_COLUMNS = [
    "timestamp",
    "symbol",
    "current_price",
    "sma_7",
    "sma_21",
    "rsi_14",
    "change_7d",
    "signal",
    "interpretation",
]
BACKTEST_CSV_COLUMNS = [
    "date",
    "symbol",
    "current_price",
    "future_price",
    "forward_days",
    "forward_return_pct",
    "signal",
    "interpretation",
]


def _display_path(path: Path) -> str:
    """Return a portable path for console output."""
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def analyze_symbol(symbol: str) -> dict | None:
    """Fetch candles and generate a basic signal for one symbol."""
    try:
        candles = get_klines(symbol, interval="1d", limit=60)
    except RuntimeError as error:
        print(f"{symbol}")
        print(f"Analysis unavailable: {error}")
        print()
        return None

    if len(candles) < 22:
        print(f"{symbol}")
        print("Analysis unavailable: at least 22 daily candles are required.")
        print()
        return None

    closes = [candle["close"] for candle in candles]

    try:
        return generate_basic_signal(symbol, closes)
    except ValueError as error:
        print(f"{symbol}")
        print(f"Analysis unavailable: {error}")
        print()
        return None


def build_summary(analyses: list[dict]) -> dict:
    """Build a reusable summary dictionary from analysis results."""
    if not analyses:
        return {
            "strongest_asset": "unavailable",
            "weakest_asset": "unavailable",
            "assets_with_positive_structure": [],
            "assets_extended_or_technical_caution": [],
            "assets_requiring_further_observation": [],
        }

    strongest = max(analyses, key=lambda item: item["change_7d"])
    weakest = min(analyses, key=lambda item: item["change_7d"])
    assets_with_positive_structure = [
        item["symbol"]
        for item in analyses
        if item["signal"] in POSITIVE_STRUCTURE_SIGNALS
    ]
    assets_extended_or_technical_caution = [
        item["symbol"]
        for item in analyses
        if item["signal"] in EXTENDED_OR_TECHNICAL_CAUTION_SIGNALS
    ]
    assets_requiring_further_observation = [
        item["symbol"]
        for item in analyses
        if item["signal"] in FURTHER_OBSERVATION_SIGNALS
    ]

    return {
        "strongest_asset": f"{strongest['symbol']} ({strongest['change_7d']:.2f}%)",
        "weakest_asset": f"{weakest['symbol']} ({weakest['change_7d']:.2f}%)",
        "assets_with_positive_structure": assets_with_positive_structure,
        "assets_extended_or_technical_caution": assets_extended_or_technical_caution,
        "assets_requiring_further_observation": assets_requiring_further_observation,
    }


def print_asset_report(analysis: dict) -> None:
    """Print one concise asset explanation block."""
    explanation = generate_asset_explanation(analysis)
    print(f"Asset: {analysis['symbol']}")
    print(f"Signal: {analysis['signal']}")
    print(f"Classification: {analysis['classification_label']}")
    print(f"Research risk: {analysis['research_risk_level']}")
    print(f"Summary: {explanation['concise_summary']}")
    print()


def print_summary(summary: dict) -> None:
    """Print a simple comparison summary across analyzed assets."""
    print("Summary:")
    print(f"- Best relative 7-day performer: {summary['strongest_asset']}")
    print(f"- Worst 7-day performer: {summary['weakest_asset']}")
    print(
        "- Assets with positive technical structure: "
        f"{', '.join(summary['assets_with_positive_structure']) or 'none'}"
    )
    print(
        "- Assets classified as extended or technically cautious: "
        f"{', '.join(summary['assets_extended_or_technical_caution']) or 'none'}"
    )
    print(
        "- Assets requiring further observation: "
        f"{', '.join(summary['assets_requiring_further_observation']) or 'none'}"
    )


def print_market_condition_summary(analyses: list[dict]) -> None:
    """Print a concise explainable market condition summary."""
    market_condition = determine_market_condition(analyses)
    explanation = explain_market_condition(analyses, market_condition)
    signal_counts = count_signals(analyses)

    print()
    print(f"Market Condition: {market_condition}")
    print(f"Explanation: {explanation}")
    print("Signal distribution:")

    for signal in SIGNAL_ORDER:
        print(f"- {signal}: {signal_counts[signal]}")


def build_csv_rows(analyses: list[dict]) -> list[dict]:
    """Convert analysis results into rows ready for CSV export."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    rows = []

    for analysis in analyses:
        rows.append(
            {
                "timestamp": timestamp,
                "symbol": analysis["symbol"],
                "current_price": analysis["current_price"],
                "sma_7": analysis["sma_7"],
                "sma_21": analysis["sma_21"],
                "rsi_14": analysis["rsi_14"],
                "change_7d": analysis["change_7d"],
                "signal": analysis["signal"],
                "interpretation": analysis["interpretation"],
            }
        )

    return rows


def write_csv_exports(analyses: list[dict]) -> None:
    """Write the latest analysis and append to the historical CSV log."""
    if not analyses:
        print()
        print("CSV export skipped: no analysis results to save.")
        return

    rows = build_csv_rows(analyses)

    try:
        DATA_FOLDER.mkdir(exist_ok=True)

        with LATEST_CSV_PATH.open("w", newline="", encoding="utf-8") as latest_file:
            writer = csv.DictWriter(latest_file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

        history_exists = HISTORY_CSV_PATH.exists()
        with HISTORY_CSV_PATH.open("a", newline="", encoding="utf-8") as history_file:
            writer = csv.DictWriter(history_file, fieldnames=CSV_COLUMNS)
            if not history_exists:
                writer.writeheader()
            writer.writerows(rows)

        print()
        print(f"CSV export saved: {_display_path(LATEST_CSV_PATH)}")
        print(f"CSV history updated: {_display_path(HISTORY_CSV_PATH)}")
    except OSError as error:
        print()
        print(f"CSV export failed: {error}")


def write_markdown_report(analyses: list[dict], summary: dict) -> None:
    """Generate and save the latest Markdown market report."""
    if not analyses:
        print("Markdown report skipped: no analysis results to save.")
        return

    try:
        REPORTS_FOLDER.mkdir(exist_ok=True)
        report_text = generate_markdown_report(analyses, summary)
        LATEST_MARKDOWN_REPORT_PATH.write_text(report_text, encoding="utf-8")
        print(f"Markdown report saved: {_display_path(LATEST_MARKDOWN_REPORT_PATH)}")
    except OSError as error:
        print(f"Markdown report failed: {error}")


def _format_signal_return_line(signal: str, average_return: float, count: int) -> str:
    """Format one signal summary line."""
    return f"- {signal}: {average_return:.2f}% across {count} signal(s)"


def print_backtest_summary(symbol: str, summary: dict) -> None:
    """Print a beginner-friendly educational backtest summary."""
    print()
    print("Kairon Crypto Agent - Simple Backtest")
    print(f"Symbol: {symbol}")
    print(f"Total signals: {summary['total_signals']}")
    print(
        "Average 7-day forward return: "
        f"{summary['average_forward_return']:.2f}%"
    )
    print("Average return by signal:")

    if not summary["average_forward_return_by_signal"]:
        print("- none")
    else:
        for signal, average_return in summary[
            "average_forward_return_by_signal"
        ].items():
            count = summary["count_by_signal"][signal]
            print(_format_signal_return_line(signal, average_return, count))

    print(
        "Signal with highest average forward return: "
        f"{summary['best_signal_by_average_return']}"
    )
    print(
        "Signal with lowest average forward return: "
        f"{summary['worst_signal_by_average_return']}"
    )
    print(
        "Note: this educational backtest reviews historical behavior and is not "
        "proof of future performance. Signals are analytical classifications, "
        "not trade orders."
    )


def write_backtest_csv(results: list[dict], csv_path: Path = BACKTEST_CSV_PATH) -> None:
    """Export detailed educational backtest results to CSV."""
    if not results:
        print("Backtest CSV export skipped: no results to save.")
        return

    try:
        DATA_FOLDER.mkdir(exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=BACKTEST_CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(results)
        print(f"Backtest CSV saved: {_display_path(csv_path)}")
    except OSError as error:
        print(f"Backtest CSV export failed: {error}")


def generate_backtest_summary_markdown(symbol: str, summary: dict) -> str:
    """Generate a Markdown summary for the educational backtest."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    lines = [
        "# Kairon Crypto Agent - Backtest Summary",
        "",
        "## Timestamp",
        "",
        timestamp,
        "",
        "## Backtest Setup",
        "",
        f"- Symbol: {symbol}",
        f"- Candle history: last {BACKTEST_CANDLE_LIMIT} daily candles",
        f"- Lookback window: {BACKTEST_LOOKBACK_WINDOW} candles",
        f"- Forward return window: {BACKTEST_FORWARD_DAYS} days",
        "",
        "## Educational Use Note",
        "",
        (
            "Signals are analytical classifications generated by simple technical "
            "rules. They are not trade orders, investment recommendations, or "
            "financial advice."
        ),
        "",
        "## Results",
        "",
        f"- Total signals: {summary['total_signals']}",
        (
            "- Average 7-day forward return: "
            f"{summary['average_forward_return']:.2f}%"
        ),
        (
            "- Signal with highest average forward return: "
            f"{summary['best_signal_by_average_return']}"
        ),
        (
            "- Signal with lowest average forward return: "
            f"{summary['worst_signal_by_average_return']}"
        ),
        "",
        "## Average Return by Signal",
        "",
    ]

    if not summary["average_forward_return_by_signal"]:
        lines.append("- none")
    else:
        for signal, average_return in summary[
            "average_forward_return_by_signal"
        ].items():
            count = summary["count_by_signal"][signal]
            lines.append(_format_signal_return_line(signal, average_return, count))

    lines.extend(
        [
            "",
            "## Educational Note",
            "",
            (
                "This backtest is for educational analysis only. It reviews how "
                "historical Kairon signals behaved over a later 7-day window, but "
                "it is not proof of future performance and does not execute trades. "
                "Signals are analytical classifications, not trade orders."
            ),
            "",
        ]
    )

    return "\n".join(lines)


def write_backtest_summary_markdown(symbol: str, summary: dict) -> None:
    """Export the educational backtest summary to Markdown."""
    try:
        REPORTS_FOLDER.mkdir(exist_ok=True)
        summary_text = generate_backtest_summary_markdown(symbol, summary)
        BACKTEST_SUMMARY_PATH.write_text(summary_text, encoding="utf-8")
        print(f"Backtest summary saved: {_display_path(BACKTEST_SUMMARY_PATH)}")
    except OSError as error:
        print(f"Backtest summary export failed: {error}")


def run_backtest_for_symbol(symbol: str) -> tuple[list[dict], dict] | None:
    """Run one educational backtest using public Binance market data."""
    try:
        candles = get_klines(symbol, interval="1d", limit=BACKTEST_CANDLE_LIMIT)
    except RuntimeError as error:
        print()
        print(f"Backtest unavailable for {symbol}: {error}")
        return None

    results = run_signal_backtest(
        symbol,
        candles,
        lookback_window=BACKTEST_LOOKBACK_WINDOW,
        forward_days=BACKTEST_FORWARD_DAYS,
    )
    summary = summarize_backtest(results)
    return results, summary


def run_btc_backtest() -> tuple[list[dict], dict] | None:
    """Run and export the existing BTCUSDT educational backtest."""
    backtest = run_backtest_for_symbol(BACKTEST_SYMBOL)
    if backtest is None:
        return None

    results, summary = backtest

    print_backtest_summary(BACKTEST_SYMBOL, summary)
    write_backtest_csv(results)
    write_backtest_summary_markdown(BACKTEST_SYMBOL, summary)
    return results, summary


def build_asset_summary(symbol: str, summary: dict) -> dict:
    """Create a compact row for a multi-asset backtest summary."""
    return {
        "symbol": symbol,
        "total_signals": summary["total_signals"],
        "average_forward_return": summary["average_forward_return"],
        "best_signal_by_average_return": summary["best_signal_by_average_return"],
        "worst_signal_by_average_return": summary["worst_signal_by_average_return"],
    }


def print_multi_asset_backtest(asset_summaries: list[dict]) -> None:
    """Print the consolidated multi-asset educational backtest."""
    print()
    print("Kairon Crypto Agent - Multi-Asset Backtest")

    if not asset_summaries:
        print("No multi-asset backtest results were available.")
        return

    for asset in asset_summaries:
        print()
        print(f"Symbol: {asset['symbol']}")
        print(f"Total signals: {asset['total_signals']}")
        print(
            "Average 7-day forward return: "
            f"{asset['average_forward_return']:.2f}%"
        )
        print(
            "Signal with highest average forward return: "
            f"{asset['best_signal_by_average_return']}"
        )
        print(
            "Signal with lowest average forward return: "
            f"{asset['worst_signal_by_average_return']}"
        )


def _get_best_asset(asset_summaries: list[dict]) -> dict | None:
    """Find the asset with the highest average forward return."""
    if not asset_summaries:
        return None
    return max(asset_summaries, key=lambda item: item["average_forward_return"])


def _get_worst_asset(asset_summaries: list[dict]) -> dict | None:
    """Find the asset with the lowest average forward return."""
    if not asset_summaries:
        return None
    return min(asset_summaries, key=lambda item: item["average_forward_return"])


def _format_asset_performance(asset: dict | None) -> str:
    """Format one asset performance result for Markdown."""
    if asset is None:
        return "unavailable"
    return f"{asset['symbol']} ({asset['average_forward_return']:.2f}%)"


def generate_multi_asset_backtest_markdown(asset_summaries: list[dict]) -> str:
    """Generate the consolidated educational multi-asset backtest report."""
    timestamp = datetime.now().isoformat(timespec="seconds")
    best_asset = _get_best_asset(asset_summaries)
    worst_asset = _get_worst_asset(asset_summaries)

    lines = [
        "# Kairon Crypto Agent - Multi-Asset Backtest Summary",
        "",
        "## Timestamp",
        "",
        timestamp,
        "",
        "## Methodology",
        "",
        (
            "This educational backtest uses public Binance daily candles. For each "
            "asset, Kairon generates historical signals using only candles available "
            "up to that date, then compares the current close with the close "
            f"{BACKTEST_FORWARD_DAYS} days later."
        ),
        "",
        f"- Assets: {', '.join(SYMBOLS)}",
        f"- Candle history: last {BACKTEST_CANDLE_LIMIT} daily candles per asset",
        f"- Lookback window: {BACKTEST_LOOKBACK_WINDOW} candles",
        f"- Forward return window: {BACKTEST_FORWARD_DAYS} days",
        "",
        "## Educational Use Note",
        "",
        (
            "Signals are analytical classifications generated by simple technical "
            "rules. They are not trade orders, investment recommendations, or "
            "financial advice."
        ),
        "",
        "## Asset-Level Summary",
        "",
    ]

    if not asset_summaries:
        lines.append("- No backtest results were available.")
    else:
        for asset in asset_summaries:
            lines.extend(
                [
                    f"### {asset['symbol']}",
                    "",
                    f"- Total signals: {asset['total_signals']}",
                    (
                        "- Average 7-day forward return: "
                        f"{asset['average_forward_return']:.2f}%"
                    ),
                    (
                        "- Signal with highest average forward return: "
                        f"{asset['best_signal_by_average_return']}"
                    ),
                    (
                        "- Signal with lowest average forward return: "
                        f"{asset['worst_signal_by_average_return']}"
                    ),
                    "",
                ]
            )

    lines.extend(
        [
            "## Relative Average Forward Returns",
            "",
            (
                "- Asset with highest average forward return: "
                f"{_format_asset_performance(best_asset)}"
            ),
            (
                "- Asset with lowest average forward return: "
                f"{_format_asset_performance(worst_asset)}"
            ),
            "",
            "## Interpretation",
            "",
            (
                "This report compares how Kairon's simple historical signals behaved "
                "across major crypto assets. Differences between assets can help "
                "identify where the current rule set has been more or less aligned "
                "with later price movement, but the sample is small and should be "
                "treated as a learning tool."
            ),
            "",
            "## Educational Risk Note",
            "",
            (
                "This backtest is for educational analysis only. It does not connect "
                "to a Binance account, does not use API keys, does not execute "
                "trades, and is not proof of future performance. Signals are "
                "analytical classifications, not trade orders."
            ),
            "",
        ]
    )

    return "\n".join(lines)


def write_multi_asset_backtest_summary(asset_summaries: list[dict]) -> None:
    """Save the consolidated multi-asset backtest Markdown report."""
    try:
        REPORTS_FOLDER.mkdir(exist_ok=True)
        report_text = generate_multi_asset_backtest_markdown(asset_summaries)
        MULTI_ASSET_BACKTEST_SUMMARY_PATH.write_text(report_text, encoding="utf-8")
        print(
            "Multi-asset backtest summary saved: "
            f"{_display_path(MULTI_ASSET_BACKTEST_SUMMARY_PATH)}"
        )
    except OSError as error:
        print(f"Multi-asset backtest summary export failed: {error}")


def run_multi_asset_backtest() -> None:
    """Run consolidated educational backtests for all configured assets."""
    all_results = []
    asset_summaries = []

    for symbol in SYMBOLS:
        backtest = run_backtest_for_symbol(symbol)
        if backtest is None:
            continue

        results, summary = backtest
        all_results.extend(results)
        asset_summaries.append(build_asset_summary(symbol, summary))

    print_multi_asset_backtest(asset_summaries)
    write_backtest_csv(all_results, MULTI_ASSET_BACKTEST_CSV_PATH)
    write_multi_asset_backtest_summary(asset_summaries)


def main() -> None:
    """Run the public multi-asset analysis report."""
    analyses = []

    print("Kairon Crypto Agent - Multi-Asset Analysis")
    print("Educational research output only; not financial advice.")
    print("--------------------------------------------------")
    print()

    for symbol in SYMBOLS:
        analysis = analyze_symbol(symbol)
        if analysis is None:
            continue

        analyses.append(analysis)
        print_asset_report(analysis)

    summary = build_summary(analyses)
    print_summary(summary)
    print_market_condition_summary(analyses)
    write_csv_exports(analyses)
    write_markdown_report(analyses, summary)
    run_btc_backtest()
    run_multi_asset_backtest()


if __name__ == "__main__":
    main()
