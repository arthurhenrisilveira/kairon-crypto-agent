# Kairon Crypto Agent

Kairon Crypto Agent is a beginner-friendly educational and research-oriented Python project for exploring simple cryptocurrency market analysis.

This project is for educational and research purposes only. It does not provide financial advice, investment recommendations, trade signals, or automated trading.

The current version analyzes major crypto pairs with public market data, calculates basic technical indicators, assigns plain-English analytical classifications, and writes Markdown/CSV research outputs. It does not use API keys, does not authenticate with any exchange account, and does not execute trades.

Version 0.3 adds asset-level explainability, including dynamic moving-average and RSI context, recent-performance context, and signal reasoning. Version 0.2's explainable Market Condition layer remains available.

## Features

- Multi-asset analysis for `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, and `SOLUSDT`.
- Simple indicators: 7-day SMA, 21-day SMA, 14-period RSI, and 7-day percentage change.
- Beginner-friendly analytical classification names such as `WATCH_BUY`, `HOLD`, `WEAKNESS_AVOID`, and `OVERBOUGHT_WAIT`.
- Explainable Market Condition summaries based on transparent signal distribution rules.
- Asset-level explanations that use each asset's actual indicator values and existing signal classification.
- Dynamic moving-average, RSI, and recent-performance context in Markdown reports.
- Markdown research report saved locally to `reports/kairon_market_report_latest.md`.
- CSV exports saved to `data/` for current analysis and historical runs.
- Educational backtests that compare past signals with later 7-day returns.
- No API keys, no exchange account login, and no trade execution.

## Project Structure

```text
kairon-crypto-agent/
  docs/       Project notes, signal legend, disclaimer, and architecture overview
  reports/    Static sample Markdown reports
  src/        Python source code for data fetching, indicators, signals, reports, and backtests
  data/       Local generated CSV exports, ignored by git
```

## Requirements

- Python 3.10 or newer
- Internet access when running `python src/main.py`, because the script reads public market data
- `requests`, installed from `requirements.txt`

## Install

Clone the repository and enter the project folder:

```bash
git clone https://github.com/arthurhenrisilveira/kairon-crypto-agent.git
cd kairon-crypto-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

From the project root:

```bash
python src/main.py
```

The script prints an educational market summary, writes local research output files, and runs educational backtests. It only uses public market-data endpoints. It does not use credentials and does not place orders.

## Example Commands

Run the full analysis workflow:

```bash
python src/main.py
```

Check that the Python files compile without running the market workflow:

```bash
python -m py_compile src/main.py src/fetch_market_data.py src/indicators.py src/strategy_rules.py src/report_generator.py src/backtesting.py src/market_condition.py src/asset_explainability.py
```

Open the generated Markdown research report after a local run:

```bash
code reports/kairon_market_report_latest.md
```

If you do not use VS Code, open the same file with any text editor.

## Example Output

Console output starts like this. Values will change as market data changes:

```text
Kairon Crypto Agent - Multi-Asset Analysis
Educational research output only; not financial advice.
--------------------------------------------------

Asset: BTCUSDT
Signal: HOLD
Classification: Neutral Technical Structure
Research risk: Low-Medium
Summary: BTCUSDT is below its 7-day SMA but above its 21-day SMA, while RSI remains below the extended threshold.

Summary:
- Best relative 7-day performer: BTCUSDT (7.39%)
- Worst 7-day performer: ETHUSDT (-1.25%)
- Assets with positive technical structure: none
- Assets classified as extended or technically cautious: none
- Assets requiring further observation: none

Market Condition: Neutral
Explanation: Most tracked assets are classified as neutral under the current rule set, so no stronger market condition dominates.
Signal distribution:
- WATCH_BUY: 0
- OVERBOUGHT_WAIT: 0
- HOLD: 4
- WEAKNESS_AVOID: 0
- OVERSOLD_WATCH: 0
- OVERSOLD_BUT_WEAK: 0
```

The run also prints where files were saved:

```text
CSV export saved: data/kairon_analysis_latest.csv
CSV history updated: data/kairon_analysis_history.csv
Markdown report saved: reports/kairon_market_report_latest.md
Backtest CSV saved: data/kairon_backtest_btcusdt.csv
Backtest summary saved: reports/kairon_backtest_summary.md
Multi-asset backtest summary saved: reports/kairon_multi_asset_backtest_summary.md
```

## Reports

Static sample Markdown reports are committed in `reports/`:

- `reports/sample_market_report.md`
- `reports/sample_backtest_summary.md`
- `reports/sample_multi_asset_backtest_summary.md`

Generated CSV files are written to `data/` and ignored by git because they are local run outputs. Generated Markdown reports use the `reports/kairon_*` filenames and are also ignored by git so public commits do not publish current market snapshots.

## Documentation

- `docs/project_overview.md` explains the architecture.
- `docs/signal_legend.md` explains each signal label.
- `docs/market_condition.md` explains the v0.2 Market Condition methodology.
- `docs/asset_explainability.md` explains the v0.3 asset-level explanation layer.
- `docs/strategy.md` outlines the strategy research direction.
- `docs/disclaimer.md` contains the educational disclaimer.

## Disclaimer

This project is for educational and research purposes only. It does not provide financial advice, investment recommendations, trade signals, or automated trading. Crypto markets are risky and volatile. Kairon signals are analytical classifications generated by simple technical rules, not trade orders.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Roadmap

- Add tests for indicators, signal rules, report generation, and backtest summaries.
- Add optional offline sample data so beginners can run examples without network access.
- Make tracked assets configurable from a simple settings file.
- Add clearer error messages for unavailable public market data.
- Add richer risk and volatility context while keeping the project educational.
- Explore offline hypothetical scenario logging without connecting to exchanges.
