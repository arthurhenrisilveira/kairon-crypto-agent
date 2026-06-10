"""Run public multi-asset market analysis reports for Kairon Crypto Agent."""

import csv
from datetime import datetime
from pathlib import Path

from fetch_market_data import get_klines
from report_generator import generate_markdown_report
from strategy_rules import generate_basic_signal


SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]
WATCH_SIGNALS = ["WATCH_BUY", "OVERSOLD_WATCH"]
AVOID_SIGNALS = ["WEAKNESS_AVOID", "OVERBOUGHT_WAIT", "OVERSOLD_BUT_WEAK"]
DATA_FOLDER = Path("data")
REPORTS_FOLDER = Path("reports")
LATEST_CSV_PATH = DATA_FOLDER / "kairon_analysis_latest.csv"
HISTORY_CSV_PATH = DATA_FOLDER / "kairon_analysis_history.csv"
LATEST_MARKDOWN_REPORT_PATH = REPORTS_FOLDER / "kairon_market_report_latest.md"
CSV_COLUMNS = [
    "timestamp",
    "symbol",
    "current_price",
    "sma_7",
    "sma_21",
    "rsi_14",
    "change_7d",
    "signal",
    "explanation",
]


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
            "assets_to_watch": [],
            "assets_to_avoid": [],
        }

    strongest = max(analyses, key=lambda item: item["change_7d"])
    weakest = min(analyses, key=lambda item: item["change_7d"])
    assets_to_watch = [
        item["symbol"] for item in analyses if item["signal"] in WATCH_SIGNALS
    ]
    assets_to_avoid = [
        item["symbol"] for item in analyses if item["signal"] in AVOID_SIGNALS
    ]

    return {
        "strongest_asset": f"{strongest['symbol']} ({strongest['change_7d']:.2f}%)",
        "weakest_asset": f"{weakest['symbol']} ({weakest['change_7d']:.2f}%)",
        "assets_to_watch": assets_to_watch,
        "assets_to_avoid": assets_to_avoid,
    }


def print_asset_report(analysis: dict) -> None:
    """Print one asset analysis block."""
    print(analysis["symbol"])
    print(f"Current price: {analysis['current_price']:.2f}")
    print(f"SMA 7: {analysis['sma_7']:.2f}")
    print(f"SMA 21: {analysis['sma_21']:.2f}")
    print(f"RSI 14: {analysis['rsi_14']:.2f}")
    print(f"7-day change: {analysis['change_7d']:.2f}%")
    print(f"Signal: {analysis['signal']}")
    print(f"Explanation: {analysis['explanation']}")
    print()


def print_summary(summary: dict) -> None:
    """Print a simple comparison summary across analyzed assets."""
    print("Summary:")
    print(f"- Strongest asset: {summary['strongest_asset']}")
    print(f"- Weakest asset: {summary['weakest_asset']}")
    print(f"- Assets to watch: {', '.join(summary['assets_to_watch']) or 'none'}")
    print(f"- Assets to avoid: {', '.join(summary['assets_to_avoid']) or 'none'}")


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
                "explanation": analysis["explanation"],
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
        print(f"CSV export saved: {LATEST_CSV_PATH}")
        print(f"CSV history updated: {HISTORY_CSV_PATH}")
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
        print(f"Markdown report saved: {LATEST_MARKDOWN_REPORT_PATH}")
    except OSError as error:
        print(f"Markdown report failed: {error}")


def main() -> None:
    """Run the public multi-asset analysis report."""
    analyses = []

    print("Kairon Crypto Agent — Multi-Asset Analysis")
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
    write_csv_exports(analyses)
    write_markdown_report(analyses, summary)


if __name__ == "__main__":
    main()
