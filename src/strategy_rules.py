"""Basic strategy rules for Kairon Crypto Agent."""

from indicators import (
    calculate_percentage_change,
    calculate_rsi,
    calculate_simple_moving_average,
)


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

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "sma_7": sma_7,
        "sma_21": sma_21,
        "rsi_14": rsi_14,
        "change_7d": change_7d,
        "signal": signal,
        "explanation": explanation,
    }
