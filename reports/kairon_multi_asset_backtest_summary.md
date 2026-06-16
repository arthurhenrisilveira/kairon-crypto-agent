# Kairon Crypto Agent — Multi-Asset Backtest Summary

## Timestamp

2026-06-15T21:34:26

## Methodology

This educational backtest uses public Binance daily candles. For each asset, Kairon generates historical signals using only candles available up to that date, then compares the current close with the close 7 days later.

- Assets: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT
- Candle history: last 180 daily candles per asset
- Lookback window: 21 candles
- Forward return window: 7 days

## Asset-Level Summary

### BTCUSDT

- Total signals: 152
- Average 7-day forward return: -1.46%
- Best signal: HOLD
- Worst signal: OVERSOLD_WATCH

### ETHUSDT

- Total signals: 152
- Average 7-day forward return: -2.47%
- Best signal: HOLD
- Worst signal: OVERSOLD_BUT_WEAK

### BNBUSDT

- Total signals: 152
- Average 7-day forward return: -1.64%
- Best signal: HOLD
- Worst signal: OVERSOLD_BUT_WEAK

### SOLUSDT

- Total signals: 152
- Average 7-day forward return: -2.80%
- Best signal: OVERSOLD_WATCH
- Worst signal: OVERBOUGHT_WAIT

## Best and Worst Assets

- Best performing asset by average forward return: BTCUSDT (-1.46%)
- Worst performing asset by average forward return: SOLUSDT (-2.80%)

## Interpretation

This report compares how Kairon's simple historical signals behaved across major crypto assets. Differences between assets can help identify where the current rule set has been more or less aligned with later price movement, but the sample is small and should be treated as a learning tool.

## Educational Risk Note

This backtest is for educational analysis only. It does not connect to a Binance account, does not use API keys, does not execute trades, and is not proof of future performance. Signals are analytical classifications, not trade orders.
