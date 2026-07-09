"""Basic strategy rules for Kairon Crypto Agent."""

from indicators import (
    calculate_percentage_change,
    calculate_rsi,
    calculate_simple_moving_average,
)


SIGNAL_METADATA = {
    "WATCH_BUY": {
        "classification_label": "Positive Technical Structure",
        "signal_interpretation": (
            "The asset shows constructive technical structure under this rule set "
            "and may deserve further observation."
        ),
        "research_risk_level": "Medium",
        "research_classification": "Observation / Confirmation Required",
        "plain_english_meaning": (
            "The asset is above the moving-average thresholds used by this "
            "educational model."
        ),
    },
    "OVERBOUGHT_WAIT": {
        "classification_label": "Extended Technical Structure",
        "signal_interpretation": "The asset appears extended under this rule set.",
        "research_risk_level": "Medium-High",
        "research_classification": "Extended Condition",
        "plain_english_meaning": (
            "The asset may be extended after a strong move."
        ),
    },
    "HOLD": {
        "classification_label": "Neutral Technical Structure",
        "signal_interpretation": (
            "The rule set does not identify a clear positive or defensive "
            "technical condition."
        ),
        "research_risk_level": "Low-Medium",
        "research_classification": "Neutral Condition",
        "plain_english_meaning": "There is no clear technical condition.",
    },
    "WEAKNESS_AVOID": {
        "classification_label": "Technical Weakness",
        "signal_interpretation": (
            "The asset remains technically weak under this rule set."
        ),
        "research_risk_level": "High",
        "research_classification": "Weakness Condition",
        "plain_english_meaning": (
            "The asset is trading below key moving averages and shows short-term "
            "weakness."
        ),
    },
    "OVERSOLD_WATCH": {
        "classification_label": "Oversold Observation",
        "signal_interpretation": (
            "The asset shows an oversold reading under this rule set and requires "
            "further observation."
        ),
        "research_risk_level": "High",
        "research_classification": "Oversold Observation",
        "plain_english_meaning": (
            "The asset may be oversold, but that reading alone does not imply a "
            "favorable condition."
        ),
    },
    "OVERSOLD_BUT_WEAK": {
        "classification_label": "Oversold With Weak Trend",
        "signal_interpretation": (
            "The asset shows an oversold reading while trend measures remain weak "
            "under this rule set."
        ),
        "research_risk_level": "Very High",
        "research_classification": "Defensive / Weak Trend",
        "plain_english_meaning": (
            "The asset looks oversold, but the trend remains weak. This may "
            "represent elevated downside risk."
        ),
    },
}


def get_signal_metadata(signal: str) -> dict:
    """Return educational metadata for a Kairon signal."""
    normalized_signal = signal.upper()

    if normalized_signal not in SIGNAL_METADATA:
        raise ValueError(f"Unknown signal: {signal}")

    return SIGNAL_METADATA[normalized_signal].copy()


def generate_basic_signal(symbol: str, closes: list[float]) -> dict:
    """Generate a preliminary signal from close prices."""
    if len(closes) < 22:
        raise ValueError("At least 22 close prices are required for this signal.")

    current_price = closes[-1]
    sma_7 = calculate_simple_moving_average(closes, 7)
    sma_21 = calculate_simple_moving_average(closes, 21)
    rsi_14 = calculate_rsi(closes, 14)
    change_7d = calculate_percentage_change(closes[-8], current_price)

    if current_price > sma_7 > sma_21 and rsi_14 < 70:
        signal = "WATCH_BUY"
        interpretation = (
            "Price is above both moving averages and RSI is below the overbought "
            "threshold."
        )
    elif rsi_14 >= 70:
        signal = "OVERBOUGHT_WAIT"
        interpretation = (
            "RSI is high, so this rule set classifies the asset as extended."
        )
    elif current_price < sma_7 < sma_21 and rsi_14 <= 30:
        signal = "OVERSOLD_BUT_WEAK"
        interpretation = (
            "RSI is low, but price remains below both moving averages. "
            "The rule set classifies this as elevated downside risk."
        )
    elif current_price < sma_7 < sma_21:
        signal = "WEAKNESS_AVOID"
        interpretation = (
            "Price is below both moving averages, suggesting short-term technical "
            "weakness."
        )
    elif rsi_14 <= 30:
        signal = "OVERSOLD_WATCH"
        interpretation = (
            "RSI is low and may deserve further observation under this rule set."
        )
    else:
        signal = "HOLD"
        interpretation = "The rule set does not identify a clear technical condition."

    metadata = get_signal_metadata(signal)

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "sma_7": sma_7,
        "sma_21": sma_21,
        "rsi_14": rsi_14,
        "change_7d": change_7d,
        "signal": signal,
        "interpretation": interpretation,
        "classification_label": metadata["classification_label"],
        "signal_interpretation": metadata["signal_interpretation"],
        "research_risk_level": metadata["research_risk_level"],
        "research_classification": metadata["research_classification"],
        "plain_english_meaning": metadata["plain_english_meaning"],
    }
