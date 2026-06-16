"""Basic strategy rules for Kairon Crypto Agent."""

from indicators import (
    calculate_percentage_change,
    calculate_rsi,
    calculate_simple_moving_average,
)


SIGNAL_METADATA = {
    "WATCH_BUY": {
        "executive_label": "Potential Buy Setup",
        "action_recommendation": (
            "Monitor for possible entry, but require confirmation before acting."
        ),
        "risk_level": "Medium",
        "decision_type": "Watchlist / Conditional Entry",
        "plain_english_meaning": (
            "The asset shows positive technical structure, but this is not an "
            "automatic buy."
        ),
    },
    "OVERBOUGHT_WAIT": {
        "executive_label": "Overbought / Wait",
        "action_recommendation": (
            "Avoid chasing the price. Wait for a pullback or better setup."
        ),
        "risk_level": "Medium-High",
        "decision_type": "Wait",
        "plain_english_meaning": (
            "The asset may be extended after a strong move."
        ),
    },
    "HOLD": {
        "executive_label": "Neutral / Hold",
        "action_recommendation": "Do not take new action. Continue monitoring.",
        "risk_level": "Low-Medium",
        "decision_type": "No Action",
        "plain_english_meaning": "There is no clear technical setup.",
    },
    "WEAKNESS_AVOID": {
        "executive_label": "Weakness / Avoid",
        "action_recommendation": (
            "Avoid new entries until the asset recovers technical strength."
        ),
        "risk_level": "High",
        "decision_type": "Avoid",
        "plain_english_meaning": (
            "The asset is trading below key moving averages and shows short-term "
            "weakness."
        ),
    },
    "OVERSOLD_WATCH": {
        "executive_label": "Oversold / Watch",
        "action_recommendation": (
            "Monitor for a possible rebound, but wait for confirmation."
        ),
        "risk_level": "High",
        "decision_type": "Watchlist Only",
        "plain_english_meaning": (
            "The asset may be oversold, but oversold does not mean automatic buy."
        ),
    },
    "OVERSOLD_BUT_WEAK": {
        "executive_label": "Oversold but Weak",
        "action_recommendation": (
            "Avoid aggressive entry. Wait for reversal confirmation."
        ),
        "risk_level": "Very High",
        "decision_type": "Defensive / Avoid Aggressive Entry",
        "plain_english_meaning": (
            "The asset looks oversold, but the trend remains weak. This may be a "
            "falling-knife setup."
        ),
    },
}


def get_signal_metadata(signal: str) -> dict:
    """Return executive action metadata for a Kairon signal."""
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
        explanation = "Price is above both moving averages and RSI is not overbought."
    elif rsi_14 >= 70:
        signal = "OVERBOUGHT_WAIT"
        explanation = "RSI is high, so wait for a better entry."
    elif current_price < sma_7 < sma_21 and rsi_14 <= 30:
        signal = "OVERSOLD_BUT_WEAK"
        explanation = (
            "RSI is low, but price remains below both moving averages. "
            "This may be a falling-knife risk."
        )
    elif current_price < sma_7 < sma_21:
        signal = "WEAKNESS_AVOID"
        explanation = "Price is below both moving averages, suggesting short-term weakness."
    elif rsi_14 <= 30:
        signal = "OVERSOLD_WATCH"
        explanation = "RSI is low and may deserve monitoring, but confirmation is needed."
    else:
        signal = "HOLD"
        explanation = "No clear setup."

    metadata = get_signal_metadata(signal)

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "sma_7": sma_7,
        "sma_21": sma_21,
        "rsi_14": rsi_14,
        "change_7d": change_7d,
        "signal": signal,
        "explanation": explanation,
        "executive_label": metadata["executive_label"],
        "action_recommendation": metadata["action_recommendation"],
        "risk_level": metadata["risk_level"],
        "decision_type": metadata["decision_type"],
        "plain_english_meaning": metadata["plain_english_meaning"],
    }
