"""Asset-level explanations for Kairon's existing analytical signals.

This module describes values and signals already produced by the indicator and
strategy layers. It does not generate or replace a signal.
"""

from __future__ import annotations

from strategy_rules import (
    RSI_EXTENDED_THRESHOLD,
    RSI_OVERSOLD_THRESHOLD,
    SIGNAL_METADATA,
)


NEAR_FLAT_PERFORMANCE_THRESHOLD = 1.0


def _symbol(asset_result: dict) -> str:
    """Return a readable asset symbol from an analysis result."""
    return str(asset_result.get("symbol", "The asset"))


def _moving_average_short_context(asset_result: dict) -> str:
    """Return a short phrase describing price relative to both SMAs."""
    symbol = _symbol(asset_result)
    current_price = asset_result["current_price"]
    sma_7 = asset_result["sma_7"]
    sma_21 = asset_result["sma_21"]

    if current_price > sma_7 and current_price > sma_21:
        return f"{symbol} is above both its 7-day SMA and 21-day SMA"

    if current_price < sma_7 and current_price > sma_21:
        return f"{symbol} is below its 7-day SMA but above its 21-day SMA"

    if current_price < sma_7 and current_price < sma_21:
        return f"{symbol} is below both its 7-day SMA and 21-day SMA"

    if current_price > sma_7 and current_price < sma_21:
        return (
            f"{symbol} is above its 7-day SMA but below its 21-day SMA"
        )

    return f"{symbol} is at one or more tracked moving-average levels"


def explain_price_vs_moving_averages(asset_result: dict) -> str:
    """Explain the asset's current price relative to the tracked SMAs."""
    symbol = _symbol(asset_result)
    current_price = asset_result["current_price"]
    sma_7 = asset_result["sma_7"]
    sma_21 = asset_result["sma_21"]

    if current_price > sma_7 and current_price > sma_21:
        return (
            f"{symbol} is trading above both the 7-day SMA and the 21-day SMA, "
            "indicating positive technical structure under this rule set."
        )

    if current_price < sma_7 and current_price > sma_21:
        return (
            f"{symbol} is trading below its 7-day SMA but above its 21-day SMA, "
            "indicating mixed short-term and medium-term structure."
        )

    if current_price < sma_7 and current_price < sma_21:
        return (
            f"{symbol} is trading below both tracked moving averages, "
            "indicating technical weakness under this rule set."
        )

    if current_price > sma_7 and current_price < sma_21:
        return (
            f"{symbol} is trading above its short-term moving average but below "
            "its 21-day moving average, indicating mixed technical structure."
        )

    return (
        f"{symbol} is trading at one or more tracked moving-average levels, "
        "so the price structure is not strictly above or below both averages."
    )


def explain_rsi(asset_result: dict) -> str:
    """Explain RSI using the thresholds already used by the strategy."""
    rsi = asset_result["rsi_14"]

    if rsi >= RSI_EXTENDED_THRESHOLD:
        return (
            f"RSI is elevated at {rsi:.2f}, so the asset is classified as "
            "extended under the current rule set."
        )

    if rsi <= RSI_OVERSOLD_THRESHOLD:
        return (
            f"RSI is {rsi:.2f}, which falls within the oversold range used by "
            "the model."
        )

    return (
        f"RSI is {rsi:.2f}, which remains below the extended threshold used by "
        "the model and above the oversold threshold."
    )


def explain_recent_performance(asset_result: dict) -> str:
    """Describe 7-day performance as context separate from the signal logic."""
    symbol = _symbol(asset_result)
    change_7d = asset_result["change_7d"]

    if abs(change_7d) < NEAR_FLAT_PERFORMANCE_THRESHOLD:
        performance = (
            f"{symbol} was relatively stable over the last 7 days, changing "
            f"{change_7d:.2f}%."
        )
    elif change_7d > 0:
        performance = f"{symbol} gained {change_7d:.2f}% over the last 7 days."
    else:
        performance = (
            f"{symbol} declined {abs(change_7d):.2f}% over the last 7 days."
        )

    return (
        f"{performance} This 7-day movement is contextual and does not "
        "independently determine the signal."
    )


def _classification_label(asset_result: dict) -> str:
    """Return the existing metadata label without creating a new classification."""
    signal = asset_result.get("signal", "UNKNOWN")
    return asset_result.get(
        "classification_label",
        SIGNAL_METADATA.get(signal, {}).get("classification_label", signal),
    )


def explain_signal_reasoning(asset_result: dict) -> str:
    """Explain the existing signal using its current indicator combination."""
    symbol = _symbol(asset_result)
    signal = asset_result["signal"]
    label = _classification_label(asset_result)
    rsi = asset_result["rsi_14"]

    if signal == "WATCH_BUY":
        return (
            f"{symbol} is trading above the moving-average thresholds used by "
            f"the model while RSI remains below the extended threshold. The "
            f"rule set therefore identifies {label}."
        )

    if signal == "OVERBOUGHT_WAIT":
        return (
            f"RSI is {rsi:.2f}, at or above the model's extended threshold of "
            f"{RSI_EXTENDED_THRESHOLD}. The rule set therefore classifies "
            f"{symbol} as {label}."
        )

    if signal == "WEAKNESS_AVOID":
        return (
            f"{symbol} is trading below key moving-average thresholds, so the "
            f"rule set classifies the asset as {label}."
        )

    if signal == "OVERSOLD_WATCH":
        return (
            f"RSI is {rsi:.2f}, within the oversold range, but the technical "
            f"structure does not meet the model's weak-trend condition. The "
            f"rule set therefore classifies {symbol} for further observation as "
            f"{label}."
        )

    if signal == "OVERSOLD_BUT_WEAK":
        return (
            f"{symbol} is oversold while also trading below key moving-average "
            f"thresholds. The combination results in an {label} classification."
        )

    if signal == "HOLD":
        return (
            f"{_moving_average_short_context(asset_result)}, but the moving-"
            f"average structure does not meet the positive or weak-trend sequence "
            f"used by the model, while RSI remains outside extended or oversold "
            f"conditions. The rule set therefore classifies {symbol} as {label}."
        )

    return (
        f"The existing signal is {signal}; this explanation uses the available "
        "signal metadata and indicator values without changing the signal."
    )


def _rsi_summary_phrase(asset_result: dict) -> str:
    """Return a concise RSI phrase for terminal output and report summaries."""
    rsi = asset_result["rsi_14"]

    if rsi >= RSI_EXTENDED_THRESHOLD:
        return "RSI is above the extended threshold"

    if rsi <= RSI_OVERSOLD_THRESHOLD:
        return "RSI is within the oversold range"

    return "RSI remains below the extended threshold"


def generate_asset_explanation(asset_result: dict) -> dict:
    """Build the complete explanation dictionary for one asset result.

    The returned text describes a signal that was already generated by
    ``strategy_rules.py``. This function never assigns a signal itself.
    """
    moving_average_context = explain_price_vs_moving_averages(asset_result)
    rsi_context = explain_rsi(asset_result)
    performance_context = explain_recent_performance(asset_result)
    classification_reasoning = explain_signal_reasoning(asset_result)
    concise_summary = (
        f"{_moving_average_short_context(asset_result)}, while "
        f"{_rsi_summary_phrase(asset_result)}."
    )

    return {
        "signal": asset_result.get("signal"),
        "classification_label": _classification_label(asset_result),
        "moving_average_context": moving_average_context,
        "rsi_context": rsi_context,
        "performance_context": performance_context,
        "classification_reasoning": classification_reasoning,
        "concise_summary": concise_summary,
    }
