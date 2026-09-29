# Asset-Level Explainability

Kairon v0.3 adds an asset-level explanation layer in
`src/asset_explainability.py`. Its purpose is to make each generated signal
auditable and easier to learn from by connecting the classification to the
actual price, moving averages, RSI, and recent performance values for that
asset.

## Explanation Flow

The strategy layer remains the source of truth for individual asset signals:

```text
indicator values
  -> strategy_rules.py generates the signal
  -> asset_explainability.py describes that signal
  -> report_generator.py and main.py present the explanation
```

The explanation layer never independently assigns a signal and never changes
the signal returned by `strategy_rules.py`.

## Moving-Average Context

`explain_price_vs_moving_averages` compares the current price with the actual
7-day and 21-day SMAs already calculated by the project. It describes four
common structures:

- Above both averages: positive technical structure under the rule set.
- Below the 7-day SMA but above the 21-day SMA: mixed short-term and
  medium-term structure.
- Below both averages: technical weakness under the rule set.
- Above the 7-day SMA but below the 21-day SMA: mixed technical structure.

These descriptions are contextual. The existing `WATCH_BUY` and
`WEAKNESS_AVOID` rules also require a specific ordering between the two SMAs,
so being above or below both averages alone does not change a signal.

## RSI Interpretation

`explain_rsi` reuses the thresholds already present in the strategy:

- RSI at or above 70 is described as elevated or extended.
- RSI at or below 30 is described as within the oversold range.
- Values between those thresholds are described as below the extended
  threshold and above the oversold threshold.

The explanation layer does not introduce a new RSI rule.

## Recent Performance

`explain_recent_performance` describes the actual 7-day percentage change as
additional context. Positive changes are described as gains, negative changes
as declines, and movements smaller than 1 percentage point in either direction
as relatively stable. This wording threshold is descriptive only. Recent
performance does not independently determine the signal.

The Research Summary uses neutral relative-performance wording:

- Best relative 7-day performer
- Worst 7-day performer

This avoids implying that the best performer had a positive return when all
tracked assets were negative.

## Classification Reasoning

`explain_signal_reasoning` uses the signal already present in the asset result
and connects it to the current indicator combination. For example:

- `HOLD` describes an indicator combination that does not meet the positive or
  weak-trend sequence while RSI is outside the extended and oversold ranges.
- `OVERBOUGHT_WAIT` points to RSI at or above the existing extended threshold.
- `OVERSOLD_BUT_WEAK` describes the combination of an oversold RSI and price
  below the key moving-average thresholds.

The wording follows the branch order and conditions in `strategy_rules.py`; it
does not reproduce a second signal-generation function.

## Output Fields

`generate_asset_explanation` returns a dictionary containing:

- `moving_average_context`
- `rsi_context`
- `performance_context`
- `classification_reasoning`
- `concise_summary`

It also includes the existing signal and classification label for convenient
report and terminal rendering.

## Limitations

Asset explanations are limited to the indicators and simple rule set currently
used by Kairon. They do not include order-book depth, liquidity, macroeconomic
events, on-chain data, sentiment, portfolio context, or an individual's risk
tolerance. Public market data can change, and these descriptions are not
predictions or proof of future behavior.

## Educational Disclaimer

Kairon Crypto Agent is for educational and research purposes only. Asset-level
explanations are descriptive classifications generated from simple technical
rules. They are not financial advice, investment recommendations, trade orders,
or automated trading output.
