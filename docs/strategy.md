# Strategy

Kairon Crypto Agent uses a simple educational rule set. The strategy layer is designed to explain market conditions, not to place trades.

## Objective

The first strategy goal is to classify a small set of major crypto assets into readable technical conditions. Each signal should help a beginner understand what the indicators suggest and what the main risk may be.

## Current Scope

- Assets: `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, and `SOLUSDT`
- Timeframe: daily candles
- Data source: public market data only
- Output: console summaries, Markdown reports, CSV exports, and educational backtest summaries

The project does not use API keys, does not authenticate with an exchange account, and does not execute trades.

## Indicators

The current signal engine uses:

- 7-day simple moving average
- 21-day simple moving average
- 14-period RSI
- 7-day percentage change

These indicators are intentionally basic so the project stays easy to inspect.

## Decision Logic

The rule set compares the current close with moving averages and RSI levels. It then returns one of the labels documented in `docs/signal_legend.md`.

Examples:

- `WATCH_BUY` means price structure is constructive, but confirmation is still required.
- `OVERBOUGHT_WAIT` means RSI is high and the project avoids chasing strength.
- `WEAKNESS_AVOID` means price is below important moving averages.
- `HOLD` means there is no clear technical setup.

## Risk Rules

Kairon signals are analytical classifications only. They should not be treated as buy or sell instructions.

The project should continue to avoid:

- API keys or account credentials
- Live trading features
- Trade execution
- Claims of guaranteed performance
- Overly complex logic that hides how the signal was created

## Backtesting

The backtest module checks how historical signals behaved over a later 7-day window. This is useful for learning, but it is not proof of future returns.

Backtest outputs are saved in:

- `reports/kairon_backtest_summary.md`
- `reports/kairon_multi_asset_backtest_summary.md`
- `data/kairon_backtest_btcusdt.csv`
- `data/kairon_backtest_multi_asset.csv`

## Research Context

See [FGV Crypto vs Global Markets - Research Summary](research/fgv_crypto_global_markets_summary.md) for baseline research on how global equity and FX variables may help contextualize crypto market behavior in future Kairon versions.
