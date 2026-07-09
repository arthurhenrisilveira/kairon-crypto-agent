"""Educational signal backtesting helpers for Kairon Crypto Agent."""

from datetime import datetime

from strategy_rules import generate_basic_signal


def _format_candle_date(candle: dict) -> str:
    """Convert a Binance candle open time into a readable date."""
    timestamp_seconds = candle["open_time"] / 1000
    return datetime.fromtimestamp(timestamp_seconds).date().isoformat()


def run_signal_backtest(
    symbol: str,
    candles: list[dict],
    lookback_window: int = 21,
    forward_days: int = 7,
) -> list[dict]:
    """Test historical signals against future returns.

    This is an educational backtest only. It checks what happened after past
    signals, but it is not proof that the same behavior will repeat.
    """
    results = []
    minimum_signal_candles = max(lookback_window, 22)
    last_start_index = len(candles) - forward_days

    for current_index in range(minimum_signal_candles - 1, last_start_index):
        candles_so_far = candles[: current_index + 1]
        closes = [candle["close"] for candle in candles_so_far]
        signal_result = generate_basic_signal(symbol, closes)

        current_price = candles[current_index]["close"]
        future_price = candles[current_index + forward_days]["close"]
        forward_return_pct = ((future_price - current_price) / current_price) * 100

        results.append(
            {
                "date": _format_candle_date(candles[current_index]),
                "symbol": symbol.upper(),
                "current_price": current_price,
                "future_price": future_price,
                "forward_days": forward_days,
                "forward_return_pct": forward_return_pct,
                "signal": signal_result["signal"],
                "interpretation": signal_result["interpretation"],
            }
        )

    return results


def summarize_backtest(results: list[dict]) -> dict:
    """Summarize an educational signal backtest."""
    if not results:
        return {
            "total_signals": 0,
            "average_forward_return": 0.0,
            "average_forward_return_by_signal": {},
            "count_by_signal": {},
            "best_signal_by_average_return": "unavailable",
            "worst_signal_by_average_return": "unavailable",
        }

    total_return = sum(item["forward_return_pct"] for item in results)
    average_forward_return = total_return / len(results)

    returns_by_signal: dict[str, list[float]] = {}
    for item in results:
        signal = item["signal"]
        returns_by_signal.setdefault(signal, []).append(item["forward_return_pct"])

    average_forward_return_by_signal = {}
    count_by_signal = {}
    for signal, signal_returns in returns_by_signal.items():
        average_forward_return_by_signal[signal] = sum(signal_returns) / len(
            signal_returns
        )
        count_by_signal[signal] = len(signal_returns)

    best_signal = max(
        average_forward_return_by_signal,
        key=average_forward_return_by_signal.get,
    )
    worst_signal = min(
        average_forward_return_by_signal,
        key=average_forward_return_by_signal.get,
    )

    return {
        "total_signals": len(results),
        "average_forward_return": average_forward_return,
        "average_forward_return_by_signal": average_forward_return_by_signal,
        "count_by_signal": count_by_signal,
        "best_signal_by_average_return": best_signal,
        "worst_signal_by_average_return": worst_signal,
    }
