# FGV Crypto vs Global Markets — Research Summary

## Objective

This research analyzes whether global equity markets and foreign exchange variables can help explain or predict cryptocurrency prices using lagged market signals, moving averages, and interpretable regression models.

## Assets Analyzed

Crypto targets:

- BTC/USD
- ETH/USD
- XRP/USD
- SOL/USD
- BNB/USD

## Market Variables

Equity and index variables:

- NASDAQ
- NYSE
- Ibovespa
- Shanghai SSE
- Hang Seng
- Shenzhen
- Euronext
- London Stock Exchange
- DAX
- Nikkei
- Bombay/India
- Milan/Italy

FX variables in USD terms:

- JPY/USD
- EUR/USD
- GBP/USD
- CNY/USD
- BRL/USD
- INR/USD

## Methods Used

The project downloads historical prices with yfinance, normalizes daily time series by carrying forward missing market-day values, and engineers lagged and moving-average features.

Main modeling approach:

- Multiple Linear Regression
- Forward stepwise feature selection
- p-value threshold of 0.10
- VIF threshold of 10 to control multicollinearity
- Temporal train/test split
- Evaluation with R², adjusted R², AIC, BIC, RMSE, RMSE%, and mean error

Core features include lags such as 7, 14, 21, 28, and in some experiments up to 50 days, plus moving averages of 10, 20, and 30 days.

## Main Findings

NASDAQ appears repeatedly as one of the strongest explanatory variables, especially for BTC, ETH, SOL, and BNB.

BTC showed the clearest interpretable case: a simplified model using NASDAQ lags achieved roughly 0.58 test R² and about 13.6% RMSE.

ETH also showed useful signal in some benchmark runs, with test R² around 0.60.

SOL and BNB showed partial market linkage, often through NASDAQ features, but with weaker stability.

XRP appeared much less reliable, with several models producing poor or negative out-of-sample R².

## Limitations

The models are mostly linear and price-level based, which makes them fragile under regime changes.

High training performance often does not generalize well to test periods.

The project does not yet include richer crypto-native or macro variables such as:

- sentiment
- on-chain activity
- liquidity
- volatility
- funding rates
- stablecoin flows
- interest rates
- inflation
- news events

Some intermediate datasets referenced in notebooks are not committed, so the repository is more useful as a research artifact than as a fully productionized pipeline.

## Lessons for Kairon

Kairon can use this project as an interpretable baseline for crypto-market linkage.

Global risk assets, especially NASDAQ, should be treated as important context signals for BTC and major altcoins.

Kairon should avoid relying only on static linear models.

A stronger agent should combine:

- market variables
- regime detection
- walk-forward validation
- crypto-native data
- sentiment
- macro events
- uncertainty scoring

The biggest practical lesson is that traditional market signals can explain part of crypto behavior, but they are incomplete.

Kairon should use them as one layer in a broader multi-signal research and reasoning system.

## Suggested Future Integration

Future versions of Kairon may include a module called:

src/global_market_context.py

This module could monitor traditional market variables such as:

- NASDAQ
- S&P 500
- DXY
- VIX
- gold
- major FX pairs

This context should not replace technical analysis, but should complement it.

Kairon's future decision logic should combine:

- crypto technical indicators
- relative strength between crypto assets
- global risk market context
- volatility regime
- historical signal performance
- risk management rules

## Current Status

This document is a research reference only.

It does not modify the current Kairon signal engine.

It does not generate trades.

It does not provide financial advice.
