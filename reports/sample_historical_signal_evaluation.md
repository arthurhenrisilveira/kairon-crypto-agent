# Kairon Historical Signal Evaluation

Sample output only. Historical descriptive analysis. Not investment guidance and not evidence of future performance.

The values in this file are illustrative sample data and are not current market information.

## Methodology

Historical signals were generated using the existing Kairon strategy rules, with only the candles available on each historical signal day. No signal optimization or parameter modification was performed.

Forward returns measure the percentage change from the signal-day closing price to the closing price 1, 3, or 7 days later. Missing future data is excluded from the relevant statistics.

Some historical candles are used only to initialize technical indicators such as SMA 21 and RSI 14. As a result, the valid signal evaluation period begins after the raw market-data period starts. Warm-up candles are not treated as missing signal observations.

Forward-return windows may overlap when classifications occur on nearby dates. As a result, historical observations are not necessarily statistically independent. BTC, ETH, BNB, and SOL may also respond to shared market conditions, so observations across assets are not necessarily independent.

Observation counts represent raw historical signal occurrences. Because forward windows can overlap and assets can move together, these counts should not be interpreted as effective independent sample sizes.

This report is descriptive historical analysis. Historical associations do not imply future performance, prediction, causality, or a trading instruction.

## Dataset Summary

- Assets evaluated: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT
- Market data period: 2025-01-01 to 2025-12-31
- Valid signal evaluation period: 2025-01-22 to 2025-12-31
- Raw historical signal observations: 1,360
- Forward horizons: 1D, 3D, 7D
- Signals evaluated: 6

## Signal Overview

| Signal | Raw historical occurrences | 1D valid obs | 3D valid obs | 7D valid obs |
| --- | ---: | ---: | ---: | ---: |
| WATCH_BUY | 180 | 180 | 178 | 174 |
| OVERBOUGHT_WAIT | 140 | 140 | 138 | 134 |
| HOLD | 540 | 540 | 538 | 534 |
| WEAKNESS_AVOID | 260 | 260 | 258 | 254 |
| OVERSOLD_WATCH | 110 | 110 | 108 | 104 |
| OVERSOLD_BUT_WEAK | 130 | 130 | 128 | 124 |

## Signal Evaluation

### WATCH_BUY

#### 1-day forward performance

- Valid historical observations: 180
- Average return: +0.42%
- Median return: +0.25%
- Positive outcomes: 55.56%
- Best observed return: +8.10%
- Worst observed return: -6.80%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 3-day forward performance

- Valid historical observations: 178
- Average return: +0.91%
- Median return: +0.54%
- Positive outcomes: 57.30%
- Best observed return: +13.20%
- Worst observed return: -10.40%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 7-day forward performance

- Valid historical observations: 174
- Average return: +1.84%
- Median return: +1.12%
- Positive outcomes: 58.62%
- Best observed return: +14.20%
- Worst observed return: -9.80%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

### OVERBOUGHT_WAIT

#### 1-day forward performance

- Valid historical observations: 140
- Average return: -0.18%
- Median return: -0.05%
- Positive outcomes: 47.14%
- Best observed return: +6.30%
- Worst observed return: -7.20%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 3-day forward performance

- Valid historical observations: 138
- Average return: -0.34%
- Median return: -0.18%
- Positive outcomes: 45.65%
- Best observed return: +9.40%
- Worst observed return: -11.60%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 7-day forward performance

- Valid historical observations: 134
- Average return: -0.62%
- Median return: -0.44%
- Positive outcomes: 43.28%
- Best observed return: +12.10%
- Worst observed return: -15.20%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

### HOLD

#### 1-day forward performance

- Valid historical observations: 540
- Average return: +0.10%
- Median return: +0.04%
- Positive outcomes: 51.85%
- Best observed return: +7.80%
- Worst observed return: -8.10%
- Sample note: Larger raw historical sample. Forward-return windows and cross-asset observations may not be independent, so the count should not be interpreted as an effective statistical sample size. Results remain descriptive.

#### 3-day forward performance

- Valid historical observations: 538
- Average return: +0.28%
- Median return: +0.12%
- Positive outcomes: 52.23%
- Best observed return: +11.30%
- Worst observed return: -12.50%
- Sample note: Larger raw historical sample. Forward-return windows and cross-asset observations may not be independent, so the count should not be interpreted as an effective statistical sample size. Results remain descriptive.

#### 7-day forward performance

- Valid historical observations: 534
- Average return: +0.46%
- Median return: +0.18%
- Positive outcomes: 53.18%
- Best observed return: +16.40%
- Worst observed return: -17.80%
- Sample note: Larger raw historical sample. Forward-return windows and cross-asset observations may not be independent, so the count should not be interpreted as an effective statistical sample size. Results remain descriptive.

### WEAKNESS_AVOID

#### 1-day forward performance

- Valid historical observations: 260
- Average return: -0.35%
- Median return: -0.22%
- Positive outcomes: 43.08%
- Best observed return: +7.20%
- Worst observed return: -9.40%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 3-day forward performance

- Valid historical observations: 258
- Average return: -0.61%
- Median return: -0.38%
- Positive outcomes: 41.47%
- Best observed return: +10.80%
- Worst observed return: -14.10%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 7-day forward performance

- Valid historical observations: 254
- Average return: -1.08%
- Median return: -0.74%
- Positive outcomes: 39.76%
- Best observed return: +13.70%
- Worst observed return: -18.30%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

### OVERSOLD_WATCH

#### 1-day forward performance

- Valid historical observations: 110
- Average return: +0.15%
- Median return: +0.02%
- Positive outcomes: 50.91%
- Best observed return: +8.90%
- Worst observed return: -8.70%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 3-day forward performance

- Valid historical observations: 108
- Average return: +0.18%
- Median return: +0.04%
- Positive outcomes: 51.85%
- Best observed return: +12.40%
- Worst observed return: -13.20%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 7-day forward performance

- Valid historical observations: 104
- Average return: +0.21%
- Median return: +0.05%
- Positive outcomes: 50.96%
- Best observed return: +15.60%
- Worst observed return: -16.10%
- Sample note: Larger raw historical sample. Forward-return windows and cross-asset observations may not be independent, so the count should not be interpreted as an effective statistical sample size. Results remain descriptive.

### OVERSOLD_BUT_WEAK

#### 1-day forward performance

- Valid historical observations: 130
- Average return: -0.26%
- Median return: -0.14%
- Positive outcomes: 44.62%
- Best observed return: +8.00%
- Worst observed return: -10.20%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 3-day forward performance

- Valid historical observations: 128
- Average return: -0.39%
- Median return: -0.25%
- Positive outcomes: 43.75%
- Best observed return: +11.10%
- Worst observed return: -15.00%
- Sample note: Moderate raw historical sample. Results remain descriptive, and overlapping observations may reduce the effective amount of independent information.

#### 7-day forward performance

- Valid historical observations: 124
- Average return: -0.71%
- Median return: -0.31%
- Positive outcomes: 42.74%
- Best observed return: +14.80%
- Worst observed return: -19.40%
- Sample note: Larger raw historical sample. Forward-return windows and cross-asset observations may not be independent, so the count should not be interpreted as an effective statistical sample size. Results remain descriptive.

## Asset-Level Breakdown

The tables below keep assets separate. The values are illustrative and should not be assumed to apply equally across assets.

### BTCUSDT

| Signal | Signal occurrences | 1D valid obs | 3D valid obs | 7D valid obs | 7D average | 7D median | 7D positive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WATCH_BUY | 50 | 50 | 49 | 47 | +2.10% | +1.35% | 59.57% |
| OVERBOUGHT_WAIT | 30 | 30 | 29 | 27 | -0.48% | -0.31% | 44.44% |
| HOLD | 140 | 140 | 139 | 137 | +0.51% | +0.22% | 54.01% |
| WEAKNESS_AVOID | 55 | 55 | 54 | 52 | -1.22% | -0.82% | 38.46% |
| OVERSOLD_WATCH | 22 | 22 | 21 | 20 | +0.36% | +0.08% | 55.00% |
| OVERSOLD_BUT_WEAK | 28 | 28 | 27 | 25 | -0.84% | -0.40% | 40.00% |

### ETHUSDT

| Signal | Signal occurrences | 1D valid obs | 3D valid obs | 7D valid obs | 7D average | 7D median | 7D positive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WATCH_BUY | 44 | 44 | 43 | 42 | +1.72% | +0.96% | 57.14% |
| OVERBOUGHT_WAIT | 38 | 38 | 37 | 36 | -0.81% | -0.51% | 41.67% |
| HOLD | 135 | 135 | 134 | 133 | +0.38% | +0.15% | 52.63% |
| WEAKNESS_AVOID | 70 | 70 | 69 | 67 | -1.04% | -0.71% | 40.30% |
| OVERSOLD_WATCH | 29 | 29 | 28 | 27 | +0.11% | +0.02% | 51.85% |
| OVERSOLD_BUT_WEAK | 31 | 31 | 30 | 29 | -0.62% | -0.28% | 44.83% |

### BNBUSDT

| Signal | Signal occurrences | 1D valid obs | 3D valid obs | 7D valid obs | 7D average | 7D median | 7D positive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WATCH_BUY | 36 | 36 | 36 | 35 | +1.49% | +0.88% | 57.14% |
| OVERBOUGHT_WAIT | 33 | 33 | 32 | 31 | -0.56% | -0.43% | 41.94% |
| HOLD | 132 | 132 | 131 | 130 | +0.42% | +0.19% | 53.08% |
| WEAKNESS_AVOID | 65 | 65 | 64 | 63 | -0.96% | -0.63% | 41.27% |
| OVERSOLD_WATCH | 30 | 30 | 29 | 28 | +0.18% | +0.04% | 53.57% |
| OVERSOLD_BUT_WEAK | 34 | 34 | 33 | 32 | -0.69% | -0.33% | 43.75% |

### SOLUSDT

| Signal | Signal occurrences | 1D valid obs | 3D valid obs | 7D valid obs | 7D average | 7D median | 7D positive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| WATCH_BUY | 50 | 50 | 50 | 50 | +2.06% | +1.18% | 60.00% |
| OVERBOUGHT_WAIT | 39 | 39 | 40 | 40 | -0.65% | -0.48% | 42.50% |
| HOLD | 133 | 133 | 134 | 134 | +0.53% | +0.16% | 53.73% |
| WEAKNESS_AVOID | 70 | 70 | 71 | 72 | -1.11% | -0.78% | 38.89% |
| OVERSOLD_WATCH | 29 | 29 | 30 | 29 | +0.25% | +0.08% | 51.72% |
| OVERSOLD_BUT_WEAK | 37 | 37 | 38 | 38 | -0.72% | -0.30% | 42.11% |

## Research Interpretation

These observations describe the available historical sample only. They are not recommendations, predictions, or evidence that a signal will behave similarly in the future.

- Within the available historical sample, WATCH_BUY occurrences were followed by a positive median 7-day return, with positive returns in 58.62% of valid observations.
- Within the available historical sample, OVERBOUGHT_WAIT occurrences were followed by a negative median 7-day return, with positive returns in 43.28% of valid observations.
- Within the available historical sample, HOLD occurrences were followed by a positive median 7-day return, with positive returns in 53.18% of valid observations.
- Within the available historical sample, WEAKNESS_AVOID occurrences were followed by a negative median 7-day return, with positive returns in 39.76% of valid observations.
- Within the available historical sample, OVERSOLD_WATCH occurrences produced mixed subsequent outcomes in the available historical sample.
- Within the available historical sample, OVERSOLD_BUT_WEAK occurrences were followed by a negative median 7-day return, with positive returns in 42.74% of valid observations.

## Limitations

- The available historical time period is limited.
- Market regimes can change, so historical associations may not persist.
- Crypto assets can be volatile.
- Asset selection and survivorship create limitations.
- Technical indicators require a warm-up period before valid signals can be generated.
- Forward-return windows can overlap, so observations are not necessarily independent.
- Observations are not necessarily independent across assets because major crypto assets may share market drivers.
- The evaluation uses a simple technical rule set.
- No transaction costs, slippage, taxes, position sizing, or portfolio simulation are included.
- No causal inference or statistical significance claim is made.
- No adjusted effective sample-size calculation is performed.
- Historical results do not guarantee future performance.

## Educational Use Note

Kairon Crypto Agent is an educational and research project. Signals remain analytical classifications and should not be interpreted as buy, sell, or hold recommendations.
