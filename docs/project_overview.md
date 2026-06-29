# Project Overview

Kairon Crypto Agent is organized as a small Python command-line project. The goal is to make the market-analysis flow easy to read, modify, and learn from.

## Architecture

The main workflow starts in `src/main.py`.

1. `src/main.py` defines the tracked symbols, orchestrates analysis, prints console summaries, writes CSV exports, writes Markdown reports, and runs educational backtests.
2. `src/fetch_market_data.py` fetches public market data. It does not use API keys or authenticate with an exchange account.
3. `src/indicators.py` contains simple technical indicator helpers such as SMA, RSI, and percentage change.
4. `src/strategy_rules.py` combines indicator values into beginner-friendly analytical signals.
5. `src/report_generator.py` turns analysis results into a Markdown market report.
6. `src/backtesting.py` runs educational historical signal checks and summarizes later 7-day returns.

## Data Flow

```text
Public market data
  -> fetch_market_data.py
  -> indicators.py
  -> strategy_rules.py
  -> main.py
  -> reports/*.md and data/*.csv
```

## Outputs

Markdown reports are generated in `reports/`:

- `reports/kairon_market_report_latest.md`
- `reports/kairon_backtest_summary.md`
- `reports/kairon_multi_asset_backtest_summary.md`

CSV exports are generated in `data/`:

- `data/kairon_analysis_latest.csv`
- `data/kairon_analysis_history.csv`
- `data/kairon_backtest_btcusdt.csv`
- `data/kairon_backtest_multi_asset.csv`

The `data/` CSV files are local run outputs and are ignored by git.

## Safety Boundaries

Kairon is educational software. It does not execute trades, does not manage real funds, does not request API keys, and does not authenticate with an exchange account. Signals are analytical classifications only.

## Portability

Output paths are resolved relative to the repository root, not a personal machine path. This lets the project run from different terminals and operating systems without depending on a local user directory.
