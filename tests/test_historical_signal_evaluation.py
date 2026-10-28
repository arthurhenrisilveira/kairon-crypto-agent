"""Deterministic tests for Kairon's historical signal evaluation."""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from historical_signal_evaluation import (  # noqa: E402
    _populate_occurrence_baseline_metrics,
    calculate_forward_return,
    evaluate_historical_signals,
    get_sample_size_note,
    get_market_data_period,
    get_valid_signal_evaluation_period,
    summarize_asset_baseline_relative_performance,
    summarize_asset_signal_performance,
    summarize_pooled_baseline_relative_performance,
    summarize_unconditional_performance,
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

    def test_unconditional_baseline_uses_all_asset_days_and_counts_incomplete(self) -> None:
        prices = [100.0] * 21 + [100.0, 105.0, 115.5, 231.0]
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": price}
            for index, price in enumerate(prices)
        ]

        baseline = summarize_unconditional_performance(
            {"BTCUSDT": candles},
            horizons=(1,),
        )

        summary = baseline["BTCUSDT"]["1d"]
        self.assertEqual(summary["sample_count"], 3)
        self.assertEqual(summary["incomplete_future_window_count"], 1)
        self.assertAlmostEqual(summary["average_return"], (5 + 10 + 100) / 3)
        self.assertAlmostEqual(summary["median_return"], 10.0)

    def test_relative_difference_reports_mean_and_median_separately(self) -> None:
        prices = [100.0] * 21 + [100.0, 105.0, 115.5, 231.0]
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": price}
            for index, price in enumerate(prices)
        ]
        occurrences = [
            make_occurrence("BTCUSDT", "HOLD", 20.0),
            make_occurrence("BTCUSDT", "HOLD", 20.0),
        ]
        baseline = summarize_unconditional_performance(
            {"BTCUSDT": candles},
            horizons=(1,),
        )

        relative = summarize_asset_baseline_relative_performance(
            occurrences,
            baseline,
            horizons=(1,),
        )
        result = relative["BTCUSDT"]["HOLD"]["1d"]

        self.assertAlmostEqual(
            result["conditional_return_pct"]["mean"],
            20.0,
        )
        self.assertAlmostEqual(
            result["unconditional_return_pct"]["median"],
            10.0,
        )
        self.assertAlmostEqual(
            result["relative_difference_pct"]["mean"],
            20.0 - ((5 + 10 + 100) / 3),
        )
        self.assertAlmostEqual(
            result["relative_difference_pct"]["median"],
            10.0,
        )
        self.assertEqual(result["sample_count"], 2)
        self.assertEqual(result["incomplete_future_window_count"], 0)
        self.assertEqual(result["unconditional_sample_count"], 3)
        self.assertEqual(result["unconditional_incomplete_future_window_count"], 1)

    def test_missing_or_zero_future_prices_are_excluded_without_imputation(self) -> None:
        self.assertIsNone(calculate_forward_return([100.0, None], 0, 1))
        self.assertIsNone(calculate_forward_return([100.0, 0.0], 0, 1))

        prices = [100.0] * 21 + [100.0, None, 110.0]
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": price}
            for index, price in enumerate(prices)
        ]
        baseline = summarize_unconditional_performance(
            {"BTCUSDT": candles},
            horizons=(1,),
        )

        summary = baseline["BTCUSDT"]["1d"]
        self.assertEqual(summary["sample_count"], 0)
        self.assertEqual(summary["incomplete_future_window_count"], 3)
        self.assertIsNone(summary["average_return"])

    def test_baseline_uses_fixed_warmup_population_not_signal_evaluation(self) -> None:
        prices = [100.0] * 21 + [None, 100.0, 105.0, 110.0]
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": price}
            for index, price in enumerate(prices)
        ]

        evaluation = evaluate_historical_signals({"BTCUSDT": candles}, horizons=(1,))

        self.assertEqual(evaluation["total_occurrences"], 0)
        self.assertEqual(
            evaluation["baseline_performance"]["BTCUSDT"]["1d"]["sample_count"],
            2,
        )
        self.assertEqual(
            evaluation["baseline_performance"]["BTCUSDT"]["1d"]
            ["incomplete_future_window_count"],
            2,
        )

    def test_pooled_baseline_matches_signal_occurrence_composition(self) -> None:
        btc_prices = [100.0] * 21 + [100.0, 101.0, 102.01, 103.0301]
        eth_prices = [100.0] * 21 + [2**index for index in range(10)]
        btc_candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": price}
            for index, price in enumerate(btc_prices)
        ]
        eth_candles = [
            {"date": f"2025-02-{index + 1:02d}", "close": price}
            for index, price in enumerate(eth_prices)
        ]
        occurrences = [
            make_occurrence("BTCUSDT", "HOLD", 10.0)
            for _ in range(9)
        ] + [make_occurrence("ETHUSDT", "HOLD", 10.0)]

        pooled = summarize_pooled_baseline_relative_performance(
            occurrences,
            {"BTCUSDT": btc_candles, "ETHUSDT": eth_candles},
            horizons=(1,),
        )
        result = pooled["HOLD"]["1d"]

        self.assertEqual(
            result["pooled_baseline_asset_weights"],
            {"BTCUSDT": 9, "ETHUSDT": 1},
        )
        self.assertAlmostEqual(result["unconditional_return_pct"]["mean"], 10.9)
        self.assertAlmostEqual(result["unconditional_return_pct"]["median"], 1.0)
        self.assertNotAlmostEqual(
            result["unconditional_return_pct"]["mean"],
            (1.0 + 100.0) / 2,
        )
        self.assertNotAlmostEqual(
            result["unconditional_return_pct"]["mean"],
            (3 * 1.0 + 9 * 100.0) / 12,
        )
        self.assertNotAlmostEqual(
            result["unconditional_return_pct"]["median"],
            100.0,
        )

    def test_occurrence_relative_difference_is_row_level_arithmetic(self) -> None:
        candles = [
            {"date": f"2025-01-{index + 1:02d}", "close": 100.0 + index}
            for index in range(30)
        ]
        evaluation = evaluate_historical_signals(
            {"TESTUSDT": candles},
            horizons=(1, 3, 7),
        )

        self.assertTrue(evaluation["occurrences"])
        for occurrence in evaluation["occurrences"]:
            for horizon in (1, 3, 7):
                key = f"{horizon}d"
                conditional = occurrence[f"conditional_return_pct_{key}"]
                unconditional = occurrence[f"unconditional_return_pct_{key}"]
                relative = occurrence[f"relative_difference_pct_{key}"]
                if conditional is None or unconditional is None:
                    self.assertIsNone(relative)
                else:
                    self.assertAlmostEqual(
                        relative,
                        conditional - unconditional,
                    )

        missing_conditional = [
            occurrence
            for occurrence in evaluation["occurrences"]
            if occurrence["conditional_return_pct_7d"] is None
        ]
        self.assertTrue(missing_conditional)
        self.assertTrue(
            all(
                occurrence["relative_difference_pct_7d"] is None
                for occurrence in missing_conditional
            )
        )

    def test_relative_difference_is_none_when_baseline_is_unavailable(self) -> None:
        occurrence = make_occurrence("BTCUSDT", "HOLD", 5.0)
        _populate_occurrence_baseline_metrics(
            occurrence,
            {
                "unconditional_return_pct": {"mean": None},
                "sample_count": 0,
                "incomplete_future_window_count": 1,
                "effective_n_note": "baseline unavailable",
            },
            1,
        )

        self.assertEqual(occurrence["conditional_return_pct_1d"], 5.0)
        self.assertIsNone(occurrence["unconditional_return_pct_1d"])
        self.assertIsNone(occurrence["relative_difference_pct_1d"])

    def test_multi_asset_output_keeps_asset_and_pooled_relative_results(self) -> None:
        increasing = [
            {"date": f"2025-01-{index + 1:02d}", "close": 100.0 + index}
            for index in range(30)
        ]
        decreasing = [
            {"date": f"2025-01-{index + 1:02d}", "close": 200.0 - index}
            for index in range(30)
        ]

        evaluation = evaluate_historical_signals(
            {"BTCUSDT": increasing, "ETHUSDT": decreasing}
        )

        self.assertEqual(
            set(evaluation["baseline_performance"]),
            {"BTCUSDT", "ETHUSDT"},
        )
        self.assertEqual(
            set(evaluation["asset_baseline_relative_performance"]),
            {"BTCUSDT", "ETHUSDT"},
        )
        self.assertEqual(
            set(evaluation["pooled_baseline_relative_performance"]),
            set(evaluation["signal_performance"]),
        )
        self.assertIn(
            "relative_difference_pct",
            evaluation["asset_signal_performance"]["BTCUSDT"]
            ["OVERBOUGHT_WAIT"]["1d"],
        )
        self.assertIn(
            "unconditional_return_pct",
            evaluation["signal_performance"]["OVERBOUGHT_WAIT"]["1d"],
        )


if __name__ == "__main__":
    unittest.main()
