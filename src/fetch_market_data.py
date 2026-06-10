"""Helpers for fetching public Binance spot market data."""

from __future__ import annotations

import requests


BINANCE_TICKER_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"


def get_current_price(symbol: str) -> float:
    """Fetch the current public spot price for a Binance symbol."""
    try:
        response = requests.get(
            BINANCE_TICKER_PRICE_URL,
            params={"symbol": symbol.upper()},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except requests.RequestException as error:
        raise RuntimeError(f"Could not fetch current price for {symbol}: {error}") from error
    except (KeyError, ValueError) as error:
        raise RuntimeError(f"Unexpected Binance price response for {symbol}.") from error


def get_multiple_prices(symbols: list[str]) -> dict[str, float]:
    """Fetch current public spot prices for multiple Binance symbols."""
    prices: dict[str, float] = {}

    for symbol in symbols:
        normalized_symbol = symbol.upper()
        prices[normalized_symbol] = get_current_price(normalized_symbol)

    return prices


def get_klines(symbol: str, interval: str = "1d", limit: int = 100) -> list[dict]:
    """Fetch public Binance candlestick data for a symbol."""
    try:
        response = requests.get(
            BINANCE_KLINES_URL,
            params={
                "symbol": symbol.upper(),
                "interval": interval,
                "limit": limit,
            },
            timeout=10,
        )
        response.raise_for_status()
        raw_candles = response.json()
    except requests.RequestException as error:
        raise RuntimeError(f"Could not fetch candles for {symbol}: {error}") from error

    try:
        candles = []
        for candle in raw_candles:
            candles.append(
                {
                    "open_time": candle[0],
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5]),
                    "close_time": candle[6],
                }
            )
        return candles
    except (IndexError, TypeError, ValueError) as error:
        raise RuntimeError(f"Unexpected Binance candle response for {symbol}.") from error
