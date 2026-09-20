---
name: football-field
description: >
  Build the published valuation football field and non-circular blend.
  Use after studio DCF/comps/SOTP and house dilution, txn, replacement, yield
  bars exist. Triggers: football field, blend, triangulation, price target.
---

# Football field

Studio has a triangulation table. This plugin publishes a **field**: low / mid / high per method, same diluted count, current-price marker, **weights on non-circular mids only**.

## Bars (one diluted count)

| Method | Owner | Low / mid / high |
|---|---|---|
| DCF (FCFF) | `dcf-model` + `dilution-if-converted` | WACC×g bear / base / bull on **if-converted** `$/sh` |
| Trading comps | `comps-valuation` | 25th / median / 75th applied to target metric ÷ same shares |
| Transaction comps | `transaction-comps` | haircut failed closes; no paper pipeline |
| SOTP / NAV | `sotp-valuation` | segment lows / mids / highs; net debt once |
| Replacement / build | `replacement-build` | floor, not a CF value |
| Yield / residual | `yield-residual` | skip with why if N/A |
| LBO | `lbo-model` | **off the field** unless a real sponsor bid is the question |

## Circularity (hard)

A bar that **reprints the tape** may draw, **weight = 0**.

Tape-echo tests (any one fails → circular):

- Multiple is the **company’s own** current EV / the same KPI you are applying (e.g. market EV ÷ contracted ARR).
- Implied `$/sh` sits on last print by construction.
- Peer set is empty and you used the target’s own multiple.

Dashed on the canvas; footnote on the memo table.

## Blend

Publish weights that sum to 100% of **live, non-circular** mids.

Starting recipe, then override with confidence:

| Method | Typical weight | Raise when | Cut when |
|---|---|---|---|
| DCF | 40–60% | forecasts defensible; TV % of EV discussed | TV > ~75% of EV with no discussion |
| Trading comps | 15–40% | clean peer set, NTM metric | NM multiples, wrong mix |
| Transaction comps | 10–25% | real closed comps, name in-play | failed/withdrawn only; stale >5y |
| SOTP | 15–30% if live | multi-segment or mix shift | single-segment; circular ARR sleeve |
| Replacement | 0–15% | asset-heavy floor useful | already = book residual |
| Yield / residual | 0–20% if live | dividend or RI > book | skipped |

```
central = Σ (weight_i × mid_i)     # non-circular only
range   = interquartile of non-circular mids and highs
```

Do **not** set the range as a courtesy band around last price. Round the blend in public; show the raw weighted sum in the memo.

## Rating from the field

Tape and last-print are **not** inputs to the blend.

- Last **above the high of every non-circular bar** + a live kill → **Sell**
- Last inside the range, thesis intact → **Hold** (Buy only if field mid > last **and** next kill is not live)
- Last **below the low**, pillars intact → **Buy**

User-stated direction wins if they assert one. Label `Draft view — not investment advice`.

## Table contract

```
Method | Low | Mid | High | Weight | In blend? | What moves it
```

Same `value_shares`, same net-debt identity, as-of price labeled. Skip a bar only with a one-line why.

Write the field into the official memo and `artifacts/{TICKER}/03-models/` as needed.

## Do not

- Do not invent a parallel DCF/comps engine.
- Do not weight circular bars “a little.”
- Do not Hold as courtesy when the math is Sell.
