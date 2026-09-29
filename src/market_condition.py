"""Explainable market condition helpers for Kairon Crypto Agent."""

from __future__ import annotations


SIGNAL_ORDER = [
    "WATCH_BUY",
    "OVERBOUGHT_WAIT",
    "HOLD",
    "WEAKNESS_AVOID",
    "OVERSOLD_WATCH",
    "OVERSOLD_BUT_WEAK",
]

POSITIVE_STRUCTURE_SIGNALS = ["WATCH_BUY"]
EXTENDED_SIGNALS = ["OVERBOUGHT_WAIT"]
NEUTRAL_SIGNALS = ["HOLD"]
OBSERVATION_SIGNALS = ["OVERSOLD_WATCH"]
DEFENSIVE_SIGNALS = ["WEAKNESS_AVOID", "OVERSOLD_BUT_WEAK"]


def count_signals(asset_results: list[dict]) -> dict:
    """Count each known signal while keeping zero-count signals visible."""
    counts = {signal: 0 for signal in SIGNAL_ORDER}

    for result in asset_results:
        signal = result.get("signal")
        if signal in counts:
            counts[signal] += 1

    return counts


def calculate_signal_distribution(asset_results: list[dict]) -> dict:
    """Calculate each signal's share of the analyzed asset set."""
    counts = count_signals(asset_results)
    total_assets = len(asset_results)

    if total_assets == 0:
        return {signal: 0.0 for signal in SIGNAL_ORDER}

    return {
        signal: round((count / total_assets) * 100, 2)
        for signal, count in counts.items()
    }


def determine_market_condition(asset_results: list[dict]) -> str:
    """Classify the broad market condition from signal distribution.

    Rules are intentionally simple and transparent:
    - Mixed: positive structure and defensive weakness appear together.
    - Constructive: most assets show WATCH_BUY and none show defensive weakness.
    - Defensive / Weak: several assets show WEAKNESS_AVOID or OVERSOLD_BUT_WEAK.
    - Extended / Cautious: several assets show OVERBOUGHT_WAIT.
    - Neutral: most assets show HOLD, or no stronger rule applies.
    """
    total_assets = len(asset_results)
    if total_assets == 0:
        return "Unavailable"

    counts = count_signals(asset_results)
    positive_count = sum(counts[signal] for signal in POSITIVE_STRUCTURE_SIGNALS)
    extended_count = sum(counts[signal] for signal in EXTENDED_SIGNALS)
    neutral_count = sum(counts[signal] for signal in NEUTRAL_SIGNALS)
    defensive_count = sum(counts[signal] for signal in DEFENSIVE_SIGNALS)

    if positive_count > 0 and defensive_count > 0:
        return "Mixed"

    if positive_count > total_assets / 2 and defensive_count == 0:
        return "Constructive"

    if defensive_count >= 2:
        return "Defensive / Weak"

    if extended_count >= 2:
        return "Extended / Cautious"

    if neutral_count > total_assets / 2:
        return "Neutral"

    return "Neutral"


def explain_market_condition(
    asset_results: list[dict],
    market_condition: str,
) -> str:
    """Explain why the market condition was assigned."""
    counts = count_signals(asset_results)
    total_assets = len(asset_results)

    if total_assets == 0:
        return "No asset results were available for market condition analysis."

    positive_count = sum(counts[signal] for signal in POSITIVE_STRUCTURE_SIGNALS)
    extended_count = sum(counts[signal] for signal in EXTENDED_SIGNALS)
    neutral_count = sum(counts[signal] for signal in NEUTRAL_SIGNALS)
    defensive_count = sum(counts[signal] for signal in DEFENSIVE_SIGNALS)

    if market_condition == "Mixed":
        return (
            "Positive technical structure and defensive technical weakness appear "
            "at the same time, so the tracked market profile is mixed under the "
            "current rule set."
        )

    if market_condition == "Constructive":
        return (
            "Most tracked assets show positive technical structure, and no assets "
            "show defensive weakness under the current rule set."
        )

    if market_condition == "Defensive / Weak":
        return (
            "Several tracked assets show technical weakness or oversold-with-weak-"
            "trend classifications under the current rule set."
        )

    if market_condition == "Extended / Cautious":
        return (
            "Several tracked assets appear extended under the RSI rule, while "
            "defensive weakness is not the dominant condition."
        )

    if neutral_count > total_assets / 2:
        return (
            "Most tracked assets are classified as neutral under the current rule "
            "set, so no stronger market condition dominates."
        )

    if extended_count == 1:
        return (
            "Signals are mostly neutral or mixed without a dominant profile, with "
            "one asset showing an extended technical condition."
        )

    if positive_count == 1 or defensive_count == 1:
        return (
            "Signals are mixed across the tracked assets, but no single condition "
            "is broad enough to dominate the market classification."
        )

    return (
        "Signals are mixed across the tracked assets without a clear dominant "
        "profile under the current rule set."
    )


def get_market_condition_drivers(asset_results: list[dict]) -> list[str]:
    """Describe the asset groups driving the market condition."""
    if not asset_results:
        return ["No asset results were available for driver analysis."]

    drivers = []
    assets_by_signal = _group_assets_by_signal(asset_results)

    if assets_by_signal["WATCH_BUY"]:
        drivers.append(
            _format_driver(
                assets_by_signal["WATCH_BUY"],
                "shows",
                "show",
                "positive technical structure under the moving-average rule.",
            )
        )

    if assets_by_signal["OVERBOUGHT_WAIT"]:
        drivers.append(
            _format_driver(
                assets_by_signal["OVERBOUGHT_WAIT"],
                "appears",
                "appear",
                "extended under the RSI rule.",
            )
        )

    if assets_by_signal["HOLD"]:
        drivers.append(
            _format_driver(
                assets_by_signal["HOLD"],
                "is",
                "are",
                "classified as neutral by the current rule set.",
            )
        )

    if assets_by_signal["WEAKNESS_AVOID"]:
        drivers.append(
            _format_driver(
                assets_by_signal["WEAKNESS_AVOID"],
                "remains",
                "remain",
                "technically weak under the moving-average rule.",
            )
        )

    if assets_by_signal["OVERSOLD_WATCH"]:
        drivers.append(
            _format_driver(
                assets_by_signal["OVERSOLD_WATCH"],
                "shows",
                "show",
                "an oversold reading that requires further observation.",
            )
        )

    if assets_by_signal["OVERSOLD_BUT_WEAK"]:
        drivers.append(
            _format_driver(
                assets_by_signal["OVERSOLD_BUT_WEAK"],
                "shows",
                "show",
                "an oversold reading while trend measures remain weak.",
            )
        )

    return drivers


def _group_assets_by_signal(asset_results: list[dict]) -> dict:
    """Group asset symbols by signal name."""
    assets_by_signal = {signal: [] for signal in SIGNAL_ORDER}

    for result in asset_results:
        signal = result.get("signal")
        symbol = result.get("symbol", "Unknown")
        if signal in assets_by_signal:
            assets_by_signal[signal].append(symbol)

    return assets_by_signal


def _format_driver(
    symbols: list[str],
    singular_verb: str,
    plural_verb: str,
    description: str,
) -> str:
    """Format one driver sentence with simple singular/plural grammar."""
    verb = singular_verb if len(symbols) == 1 else plural_verb
    return f"{_format_symbol_list(symbols)} {verb} {description}"


def _format_symbol_list(symbols: list[str]) -> str:
    """Format a short symbol list for explanatory text."""
    if len(symbols) == 1:
        return symbols[0]

    if len(symbols) == 2:
        return f"{symbols[0]} and {symbols[1]}"

    return f"{', '.join(symbols[:-1])}, and {symbols[-1]}"
