"""Basic technical indicators for market analysis."""


def calculate_simple_moving_average(values: list[float], period: int) -> float:
    """Return the simple moving average for the last period values."""
    if period <= 0:
        raise ValueError("SMA period must be greater than zero.")

    if len(values) < period:
        raise ValueError(f"At least {period} values are required to calculate SMA.")

    recent_values = values[-period:]
    return sum(recent_values) / period


def calculate_percentage_change(first_value: float, last_value: float) -> float:
    """Return the percentage change from first_value to last_value."""
    if first_value == 0:
        raise ValueError("Cannot calculate percentage change from zero.")

    return ((last_value - first_value) / first_value) * 100


def calculate_rsi(closes: list[float], period: int = 14) -> float:
    """Calculate a simple RSI using average gains and losses."""
    if period <= 0:
        raise ValueError("RSI period must be greater than zero.")

    if len(closes) < period + 1:
        raise ValueError(f"At least {period + 1} closes are required to calculate RSI.")

    recent_closes = closes[-(period + 1):]
    gains = []
    losses = []

    for index in range(1, len(recent_closes)):
        change = recent_closes[index] - recent_closes[index - 1]

        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    average_gain = sum(gains) / period
    average_loss = sum(losses) / period

    if average_loss == 0:
        return 100.0

    relative_strength = average_gain / average_loss
    return 100 - (100 / (1 + relative_strength))
