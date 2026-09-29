"""Deterministic tests for Kairon's asset-level explanations."""

from pathlib import Path
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from asset_explainability import (  # noqa: E402
    explain_price_vs_moving_averages,
    explain_recent_performance,
    explain_rsi,
    explain_signal_reasoning,
    generate_asset_explanation,
)


def make_asset_result(**overrides: object) -> dict:
    """Build a small deterministic analysis result for unit tests."""
    result = {
        "symbol": "TESTUSDT",
        "current_price": 95.0,
        "sma_7": 100.0,
        "sma_21": 90.0,
        "rsi_14": 63.1,
        "change_7d": -0.56,
        "signal": "HOLD",
        "classification_label": "Neutral Technical Structure",
    }
    result.update(overrides)
    return result


class AssetExplainabilityTests(unittest.TestCase):
    def test_price_above_both_moving_averages(self) -> None:
        result = make_asset_result(current_price=110.0, sma_7=100.0, sma_21=90.0)
        explanation = explain_price_vs_moving_averages(result)
        self.assertIn("above both", explanation)
        self.assertIn("positive technical structure", explanation)

    def test_price_below_sma_7_but_above_sma_21(self) -> None:
        result = make_asset_result(current_price=95.0, sma_7=100.0, sma_21=90.0)
        explanation = explain_price_vs_moving_averages(result)
        self.assertIn("below its 7-day SMA but above its 21-day SMA", explanation)
        self.assertIn("mixed", explanation)

    def test_price_below_both_moving_averages(self) -> None:
        result = make_asset_result(current_price=80.0, sma_7=100.0, sma_21=90.0)
        explanation = explain_price_vs_moving_averages(result)
        self.assertIn("below both tracked moving averages", explanation)
        self.assertIn("technical weakness", explanation)

    def test_normal_rsi(self) -> None:
        explanation = explain_rsi(make_asset_result(rsi_14=63.1))
        self.assertIn("RSI is 63.10", explanation)
        self.assertIn("below the extended threshold", explanation)

    def test_high_rsi(self) -> None:
        explanation = explain_rsi(make_asset_result(rsi_14=73.3))
        self.assertIn("RSI is elevated at 73.30", explanation)
        self.assertIn("extended", explanation)

    def test_oversold_rsi(self) -> None:
        explanation = explain_rsi(make_asset_result(rsi_14=27.4))
        self.assertIn("RSI is 27.40", explanation)
        self.assertIn("oversold range", explanation)

    def test_positive_recent_performance(self) -> None:
        explanation = explain_recent_performance(make_asset_result(change_7d=2.85))
        self.assertIn("gained 2.85%", explanation)
        self.assertIn("does not independently determine the signal", explanation)

    def test_negative_recent_performance(self) -> None:
        explanation = explain_recent_performance(make_asset_result(change_7d=-4.24))
        self.assertIn("declined 4.24%", explanation)

    def test_near_flat_recent_performance(self) -> None:
        explanation = explain_recent_performance(make_asset_result(change_7d=-0.56))
        self.assertIn("relatively stable", explanation)
        self.assertIn("-0.56%", explanation)

    def test_hold_reasoning(self) -> None:
        result = make_asset_result(signal="HOLD")
        explanation = explain_signal_reasoning(result)
        self.assertIn("outside extended or oversold conditions", explanation)
        self.assertIn("Neutral Technical Structure", explanation)

    def test_overbought_wait_reasoning(self) -> None:
        result = make_asset_result(
            signal="OVERBOUGHT_WAIT",
            rsi_14=73.3,
            classification_label="Extended Technical Structure",
        )
        explanation = explain_signal_reasoning(result)
        self.assertIn("extended threshold of 70", explanation)
        self.assertIn("Extended Technical Structure", explanation)

    def test_oversold_but_weak_reasoning(self) -> None:
        result = make_asset_result(
            current_price=80.0,
            sma_7=100.0,
            sma_21=90.0,
            rsi_14=27.4,
            signal="OVERSOLD_BUT_WEAK",
            classification_label="Oversold With Weak Trend",
        )
        explanation = explain_signal_reasoning(result)
        self.assertIn("oversold", explanation)
        self.assertIn("below key moving-average thresholds", explanation)
        self.assertIn("Oversold With Weak Trend", explanation)

    def test_generated_explanation_has_expected_fields(self) -> None:
        explanation = generate_asset_explanation(make_asset_result())
        self.assertEqual(
            set(
                [
                    "signal",
                    "classification_label",
                    "moving_average_context",
                    "rsi_context",
                    "performance_context",
                    "classification_reasoning",
                    "concise_summary",
                ]
            ),
            set(explanation),
        )


if __name__ == "__main__":
    unittest.main()
