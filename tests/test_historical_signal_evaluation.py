"""Deterministic tests for Kairon's historical signal evaluation."""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from historical_signal_evaluation import (  # noqa: E402
    calculate_forward_return,
    evaluate_historical_signals,
    get_sample_size_note,
    get_market_data_period,
    get_valid_signal_evaluation_period,
    summarize_asset_signal_performance,
    summarize_signal_performance,
)


def make_occurrence(
    asset: str,
    signal: str,
    returns_1d: float | None,
    returns_3d: float | None = None,
    returns_7d: float | None = None,
) -> dict:
    """Build a compact historical occurrence for summary tests."""
    return {
        "asset": asset,
        "date": "2025-01-01",
        "price": 100.0,
        "signal": signal,
        "sma_7": 99.0,
        "sma_21": 98.0,
        "rsi_14": 55.0,
        "change_7d": 1.0,
        "forward_return_1d": returns_1d,
        "forward_return_3d": returns_3d,
        "forward_return_7d": returns_7d,
    }


class HistoricalSignalEvaluationTests(unittest.TestCase):
    def test_calculate_forward_returns_for_all_horizons(self) -> None:
        prices = [100.0, 102.0, 103.0, 105.0, 106.0, 108.0, 109.0, 112.0]

        self.assertAlmostEqual(calculate_forward_return(prices, 0, 1), 2.0)
        self.assertAlmostEqual(calculate_forward_return(prices, 0, 3), 5.0)
        self.assertAlmostEqual(calculate_forward_return(prices, 0, 7), 12.0)

    def test_missing_future_data_returns_none(self) -> None:
        prices = [100.0, 102.0, 103.0]

        self.assertIsNone(calculate_forward_return(prices, 2, 1))
        self.assertIsNone(calculate_forward_return(prices, 0, 7))

    def test_return_statistics_include_average_median_positive_best_and_worst(self) -> None:
        occurrences = [
            make_occurrence("BTCUSDT", "HOLD", -2.0, -1.0, -2.0),
            make_occurrence("BTCUSDT", "HOLD", 1.0, 2.0, 1.0),
            make_occurrence("ETHUSDT", "HOLD", 4.0, 5.0, 4.0),
        ]

        summary = summarize_signal_performance(occurrences)["HOLD"]["7d"]

        self.assertEqual(summary["observations"], 3)
        self.assertAlmostEqual(summary["average_return"], 1.0)
        self.assertAlmostEqual(summary["median_return"], 1.0)
        self.assertAlmostEqual(summary["positive_return_percentage"], 66.6666667)
        self.assertAlmostEqual(summary["best_observed_return"], 4.0)
        self.assertAlmostEqual(summary["worst_observed_return"], -2.0)

    def test_sample_size_notes(self) -> None:
        self.assertEqual(
            get_sample_size_note(0),
            "No historical observations are available for this signal and horizon.",
        )
        self.assertIn("Very small historical sample", get_sample_size_note(5))
        self.assertIn(
            "Small historical sample. Interpret descriptive results cautiously.",
            get_sample_size_note(15),
        )
        self.assertIn("Moderate raw historical sample", get_sample_size_note(50))
        self.assertIn("overlapping observations", get_sample_size_note(50))
        self.assertIn("Larger raw historical sample", get_sample_size_note(100))
        self.assertIn("effective statistical sample size", get_sample_size_note(100))

    def test_pooled_signal_summary_keeps_all_signal_identifiers(self) -> None:
        occurrences = [
            make_occurrence("BTCUSDT", "WATCH_BUY", 1.0, 2.0, 3.0),
            make_occurrence("ETHUSDT", "HOLD", -1.0, -2.0, -3.0),
        ]

        summary = summarize_signal_performance(occurrences)

        self.assertEqual(summary["WATCH_BUY"]["total_occurrences"], 1)
        self.assertEqual(summary["HOLD"]["total_occurrences"], 1)
        self.assertEqual(summary["OVERSOLD_BUT_WEAK"]["total_occurrences"], 0)
        self.assertEqual(summary["OVERSOLD_BUT_WEAK"]["7d"]["observations"], 0)

    def test_asset_level_summary_keeps_assets_separate(self) -> None:
        occurrences = [
            make_occurrence("BTCUSDT", "WATCH_BUY", 1.0, 2.0, 3.0),
            make_occurrence("ETHUSDT", "WATCH_BUY", -1.0, -2.0, -3.0),
        ]

        summary = summarize_asset_signal_performance(occurrences)

        self.assertEqual(set(summary), {"BTCUSDT", "ETHUSDT"})
        self.assertAlmostEqual(
            summary["BTCUSDT"]["WATCH_BUY"]["7d"]["average_return"],
            3.0,
        )
        self.assertAlmostEqual(
            summary["ETHUSDT"]["WATCH_BUY"]["7d"]["average_return"],
            -3.0,
        )

    def test_multi_asset_evaluation_reuses_existing_signal_generation(self) -> None:
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": 100.0 + index}
            for index in range(30)
        ]

        evaluation = evaluate_historical_signals({"TESTUSDT": candles})

        self.assertEqual(evaluation["assets_evaluated"], ["TESTUSDT"])
        self.assertEqual(evaluation["total_occurrences"], 9)
        self.assertEqual(evaluation["signal_occurrences"]["OVERBOUGHT_WAIT"], 9)
        self.assertEqual(evaluation["signal_occurrences"]["HOLD"], 0)
        self.assertEqual(
            evaluation["asset_signal_performance"]["TESTUSDT"]
            ["OVERBOUGHT_WAIT"]["7d"]["observations"],
            2,
        )

    def test_market_and_valid_signal_periods_are_distinct(self) -> None:
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": 100.0 + index}
            for index in range(30)
        ]

        market_period = get_market_data_period({"TESTUSDT": candles})
        evaluation = evaluate_historical_signals({"TESTUSDT": candles})

        self.assertEqual(market_period, "2025-01-01 to 2025-01-30")
        self.assertEqual(
            get_valid_signal_evaluation_period(evaluation["occurrences"]),
            "2025-01-22 to 2025-01-30",
        )
        self.assertEqual(evaluation["market_data_period"], market_period)
        self.assertEqual(
            evaluation["valid_signal_evaluation_period"],
            "2025-01-22 to 2025-01-30",
        )
        self.assertEqual(len(evaluation["occurrences"]), 9)


if __name__ == "__main__":
    unittest.main()
