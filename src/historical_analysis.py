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
    "price",
    "signal",
    "sma_7",
    "sma_21",
    "rsi_14",
    "change_7d",
    "forward_return_1d",
    "forward_return_3d",
    "forward_return_7d",
]


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
    report_path.write_text(
        generate_historical_evaluation_markdown(evaluation),
        encoding="utf-8",
    )


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
