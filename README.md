# Kairon Crypto Agent

Kairon Crypto Agent is a beginner-friendly educational Python project for exploring simple cryptocurrency market analysis.

The current version analyzes major crypto pairs with public market data, calculates basic technical indicators, assigns plain-English signal labels, and writes Markdown/CSV reports. It does not use API keys, does not authenticate with any exchange account, and does not execute trades.

## Features

- Multi-asset analysis for `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, and `SOLUSDT`.
- Simple indicators: 7-day SMA, 21-day SMA, 14-period RSI, and 7-day percentage change.
- Beginner-friendly signal labels such as `WATCH_BUY`, `HOLD`, `WEAKNESS_AVOID`, and `OVERBOUGHT_WAIT`.
- Markdown market report saved to `reports/kairon_market_report_latest.md`.
- CSV exports saved to `data/` for the latest analysis and historical runs.
- Educational backtests that compare past signals with later 7-day returns.
- No API keys, no exchange account login, and no trade execution.

## Project Structure

```text
kairon-crypto-agent/
  docs/       Project notes, signal legend, disclaimer, and architecture overview
  reports/    Sample generated Markdown reports
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
git clone https://github.com/your-username/kairon-crypto-agent.git
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

The script prints a market summary, writes report files, and runs educational backtests. It only uses public market-data endpoints. It does not use credentials and does not place orders.

## Example Commands

Run the full analysis workflow:

```bash
python src/main.py
```

Check that the Python files compile without running the market workflow:

```bash
python -m py_compile src/main.py src/fetch_market_data.py src/indicators.py src/strategy_rules.py src/report_generator.py src/backtesting.py
```

Open the latest generated Markdown report:

```bash
code reports/kairon_market_report_latest.md
```

If you do not use VS Code, open the same file with any text editor.

## Example Output

Console output starts like this. Values will change as market data changes:

```text
Kairon Crypto Agent - Multi-Asset Analysis
--------------------------------------------------

BTCUSDT
Current price: 66292.01
SMA 7: 64506.03
SMA 21: 66519.82
RSI 14: 48.45
7-day change: 7.39%
Signal: HOLD
Executive action: Do not take new action. Continue monitoring.
Risk level: Low-Medium
Decision type: No Action
Explanation: No clear setup.
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

Sample Markdown reports are committed in `reports/`:

- `reports/kairon_market_report_latest.md`
- `reports/kairon_backtest_summary.md`
- `reports/kairon_multi_asset_backtest_summary.md`

Generated CSV files are written to `data/` and ignored by git because they are local run outputs.

## Documentation

- `docs/project_overview.md` explains the architecture.
- `docs/signal_legend.md` explains each signal label.
- `docs/strategy.md` outlines the strategy research direction.
- `docs/disclaimer.md` contains the educational disclaimer.

## Disclaimer

This project is for educational and research purposes only. It is not financial advice, investment advice, trading advice, or a recommendation to buy or sell any asset. Crypto markets are risky and volatile. Kairon signals are analytical classifications, not trade orders. Always do your own research.

## Roadmap

- Add tests for indicators, signal rules, report generation, and backtest summaries.
- Add optional offline sample data so beginners can run examples without network access.
- Make tracked assets configurable from a simple settings file.
- Add clearer error messages for unavailable public market data.
- Add richer risk and volatility context while keeping the project educational.
- Explore a paper-trading simulator that records hypothetical decisions without placing live orders.
