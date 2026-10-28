# Historical Signal Evaluation

Kairon v0.4 added Historical Signal Evaluation through
`src/historical_signal_evaluation.py`. The layer answers a narrow descriptive
question:

> When an existing Kairon analytical classification appeared historically, what
> happened afterward in the available dataset?

It does not claim that a signal works, predicts future returns, or represents a
trade.

Kairon v0.5 extends this same evaluation with an unconditional baseline. Each
signal-conditioned return is compared with the same asset's unconditional
forward returns at the same horizon over the fixed post-warm-up eligible
asset-day population. Existing signal identifiers, thresholds, and generation
behavior are unchanged.

## Architecture

```text
Historical public candles
  -> existing strategy_rules.py
  -> historical signal occurrences
  -> forward-return evaluation
  -> asset-level baseline-relative statistics
  -> secondary pooled descriptive context
  -> Markdown report and CSV export
```

The evaluator calls `generate_basic_signal` from `strategy_rules.py` using only
the candles available on each historical signal day. It does not duplicate the
signal branches, optimize thresholds, or modify the generated signal.

## Forward Returns

Each historical occurrence includes simple percentage returns after:

- 1 day
- 3 days
- 7 days

The calculation is:

```text
(future closing price - signal-day closing price)
    / signal-day closing price * 100
```

If a future candle is not available, the occurrence keeps a missing value for
that horizon. The missing value is excluded from that horizon's statistics; it
is never fabricated.

### Indicator Warm-Up

Some historical candles are used only to initialize technical indicators such
as SMA 21 and RSI 14. As a result, the valid signal evaluation period begins
after the raw market-data period starts. Warm-up candles are not treated as
missing signal observations, and Kairon does not create synthetic indicator
values for them.

### Overlapping Forward Windows

Historical classifications can occur on consecutive or nearby dates. A
7-day return measured from one date can therefore overlap with the 7-day return
measured from the next date. Kairon keeps these raw occurrences in v0.4 and
does not remove them or calculate an adjusted sample size.

Forward-return windows may overlap when classifications occur on nearby dates.
As a result, historical observations are not necessarily statistically
independent.

### Observation Dependence

Observation counts represent raw historical signal occurrences, not independent
statistical samples. Forward windows can overlap, and BTC, ETH, BNB, and SOL
may respond to shared market conditions. Observations across assets are also not
necessarily independent because major crypto assets can move together during
broad market regimes.

## Statistics

For every existing signal and horizon, Kairon reports:

- valid observations
- average forward return
- median forward return
- percentage of positive forward returns
- best observed forward return
- worst observed forward return

The report includes all six existing signal identifiers:
`WATCH_BUY`, `OVERBOUGHT_WAIT`, `HOLD`, `WEAKNESS_AVOID`, `OVERSOLD_WATCH`, and
`OVERSOLD_BUT_WEAK`.

## Baseline and Relative Evaluation

The v0.5 unit of analysis is one eligible signal occurrence × asset × forward
horizon. The approved eligible-period interpretation is A: the reference
population is every asset-day for the same asset and horizon at or after the
fixed indicator warm-up boundary, without conditioning on signal
classification. The configured horizons remain 1 day, 3 days, and 7 days. A
baseline window still requires a usable signal-day close and future close; no
value is imputed. Signal collection may skip a date when prior historical
inputs are invalid, but that conditional classification failure does not remove
the date from the unconditional population. This keeps the baseline
denominator independent of signal outcomes. `valid_signal_evaluation_period`
continues to describe dates with collected signal occurrences and is not a
replacement for the fixed baseline population definition.

For each asset × signal × horizon, the report and evaluation data expose:

- `conditional_return_pct`: conditional mean and median forward return;
- `unconditional_return_pct`: same-asset, same-horizon baseline mean and median;
- `relative_difference_pct`: conditional minus unconditional mean and median;
- `sample_count` and `incomplete_future_window_count` for the conditional rows;
- baseline sample and incomplete-window counts; and
- `effective_n_note`, which keeps raw counts separate from independent-sample
  claims.

The baseline uses the same forward-return formula as signal occurrences. A
window is excluded when its signal-day or future close is missing, zero,
non-finite, or outside available data. No value is imputed, and excluded counts
remain visible. Signal-day and forward timestamps are retained in the
occurrence export. Its horizon-qualified `conditional_return_pct_*`,
`unconditional_return_pct_*`, and `relative_difference_pct_*` columns carry the
occurrence return, same-asset baseline mean, and their row-level arithmetic
difference respectively. If either return is unavailable, the row-level
relative difference is `None`. Aggregate asset-signal mean and median relative
metrics remain in the asset-level summaries, pooled summaries, and Markdown
report.

Asset-level results are primary. Pooled results are occurrence-weighted
descriptive context only and can hide asset-level heterogeneity. For each
signal and horizon, the total weight assigned to an asset's unconditional
distribution equals its count of valid conditional occurrences for that signal
and horizon. The pooled mean is the resulting weighted empirical mean; the
pooled median is a deterministic weighted empirical median. Raw baseline
sample and incomplete-window counts remain counts of the underlying contributing
asset-day windows, not independent-sample claims. The output reports
descriptive comparisons only; no inferential tests or confidence intervals are
calculated.

## Sample-Size Notes

### What Sample Size Means Here

The report uses raw valid historical observations for each signal and horizon.
These counts are communication categories only. They are not statistical
significance thresholds, confidence levels, power calculations, or effective
sample-size estimates. A large raw count can still contain overlapping
forward-return windows and cross-asset observations that are not independent.

The communication categories are:

- 0: no historical observations are available for the signal and horizon.
- 1-9: very small sample; results are insufficient for meaningful
  interpretation.
- 10-29: small historical sample; interpret descriptive results cautiously.
- 30-99: moderate raw historical sample; results remain descriptive, and
  overlapping observations may reduce the effective amount of independent
  information.
- 100 or more: larger raw historical sample; forward-return windows and
  cross-asset observations may not be independent, so the count should not be
  interpreted as an effective statistical sample size. Results remain
  descriptive.

## Pooled and Asset-Level Results

The pooled summary combines occurrences across the configured assets so that a
researcher can inspect secondary descriptive context. The asset-level breakdown
keeps each asset and signal combination separate and now includes the aligned
unconditional baseline. For a given signal and horizon, pooled baseline asset
weights come from valid conditional occurrence counts, not equal asset weights
and not total unconditional asset-day counts. Pooled results should not be
assumed to apply equally to every asset or generalized beyond the evaluated
observations.

The report's asset-level tables provide compact 7-day descriptive statistics,
while the pooled signal sections provide full statistics for 1-day, 3-day, and
7-day horizons.

## Relationship to Existing Backtesting

The existing `src/backtesting.py` remains unchanged. It reviews a selected
simplified historical signal workflow and summarizes a later forward window.
Historical Signal Evaluation is broader and descriptive: it records every
analytical classification, evaluates three horizons, and does not assume that a
classification represents a trade.

In particular:

- `WATCH_BUY` does not mean buy.
- `WEAKNESS_AVOID` does not mean sell.
- The statistics do not provide recommendations or portfolio instructions.

## Data and Outputs

Run the standalone workflow with:

```bash
python src/historical_analysis.py
```

The workflow reads public daily market candles using the project's existing
data-fetching helper. It uses a bounded recent historical window to keep the
beginner workflow practical. It writes:

- `reports/kairon_historical_signal_evaluation_latest.md`
- `data/kairon_historical_signal_occurrences.csv`

Both are generated local outputs and are ignored by Git.

## Limitations

The evaluation is limited by the available historical time period, changing
market regimes, crypto volatility, asset selection and survivorship
limitations, indicator warm-up, overlapping forward-return windows,
non-independent observations, autocorrelation, cross-asset dependence, pooled
heterogeneity, multiple-horizon interpretation, data-snooping risk, and the
simple technical rule set. It does not include transaction costs, slippage,
taxes, position sizing, portfolio simulation, inferential tests, confidence
intervals, or an adjusted effective sample-size calculation. Historical results
do not guarantee future performance.

## Educational Disclaimer

Kairon Crypto Agent is an educational and research project. Historical Signal
Evaluation is descriptive historical analysis, not financial advice, an
investment recommendation, a trade signal, or automated trading output.
