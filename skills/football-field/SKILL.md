---
name: football-field
description: >
  Build the published valuation football field and non-circular blend.
  Use after studio DCF/comps/SOTP and house dilution, txn, replacement, yield
  bars exist. Triggers: football field, blend, triangulation, price target.
---

# Football field

Studio has a triangulation table. The hub publishes a **field**: low / mid / high per method, same diluted count, current-price marker, **weights on non-circular mids only**.

Pitch Agent (`anthropics/financial-services` pitch-agent): min / median / max per method + last-print line. House adds circularity, skip-reasons, and rating tightness.

## Bars (one diluted count)

| Method | Owner | Low / mid / high |
|---|---|---|
| DCF (FCFF) | studio `dcf-model` + [dilution](../dilution-if-converted/SKILL.md) | WACC×g bear / base / bull on **if-converted** $/sh |
| Trading comps (CCA) | studio `comps-valuation` | 25th / median / 75th on the **researched** set, or the user’s locked set. Show P/E, EV/EBITDA, EV/Sales; `NM` if the denominator is missing. A canvas toggle is a draft until the memo is updated |
| Transaction comps | [transaction-comps](../transaction-comps/SKILL.md) | haircut failed closes; no paper pipeline. Deal table is a Valuation sub-view |
| SOTP / NAV | studio `sotp-valuation` | segment lows / mids / highs; net debt once |
| Asset-based / replacement | [replacement-build](../replacement-build/SKILL.md) | book, PPE − net debt, equity-funded stack. Floor, not a CF value. Liquidation only if sourced |
| Yield / residual | [yield-residual](../yield-residual/SKILL.md) | skip with why if N/A |
| LBO | studio `lbo-model` | **off the field** unless a real sponsor bid is the question |

## Circularity (hard)

A bar that **reprints the tape** may draw, **weight = 0**.

Tape-echo tests (any one fails → circular):

- Multiple is the **company’s own** current EV / the same KPI you are applying (e.g. market EV ÷ contracted ARR).
- Implied $/sh sits on last print by construction.
- Peer set is empty and you used the target’s own multiple.

Dashed on the canvas; footnote on the memo table. Own EV ÷ own ARR (or empty peer set using the target multiple) is the worked reject.

## Blend

Publish weights that sum to 100% of **live, non-circular** mids.

Starting recipe (Anthropic initiating-coverage), then override with confidence:

| Method | Typical weight | Raise when | Cut when |
|---|---|---|---|
| DCF | 40–60% | forecasts defensible; TV % of EV discussed | TV > ~75% of EV with no discussion |
| Trading comps | 15–40% | clean peer set, NTM metric | NM multiples, wrong mix (LTM still the old segment) |
| Transaction comps | 10–25% | real closed comps, name in-play | failed/withdrawn only; stale >5y |
| SOTP | 15–30% if live | multi-segment or mix shift | single-segment; circular ARR sleeve |
| Replacement | 0–15% | asset-heavy floor useful | already = book residual |
| Yield / residual | 0–20% if live | dividend or RI > book | skipped |

```
central = Σ (weight_i × mid_i)     # non-circular only
range   = interquartile of non-circular mids and highs
```

Do **not** set the range as a courtesy band around last price. Round the blend in public; show the raw weighted sum in the memo.

## How the name opens

Default prompt: **What do you think of IREN and the bull case next 12 months?**

Default is the **12-month bull case**.

- The user did not say bear. The cover is the bull path: what has to happen in the next year, and the bull price. The low DCF, or a tape that sits above every bar, is the **kill column** on the same page. Do not open the page with Sell at a fraction of the tape.
- The user said **bear**. The cover is that downside valuation and why. Options then attack it.

The field math does not change. Tape and last-print are **not** inputs to the blend.

The chart scales to the bars and the last price. If the bull price sits above that scale, pin it: **Bull $X off chart**. Do not stretch the axis until the bars collapse on the left.

Asset floors (book, PPE − net debt) draw. They do not become the cover price. If you cannot source a bull price above the tape, set `target_open: true` in `site.json`. The chip reads **HOLD · target open**. Do not print the floor as the target, and do not open with Sell at a fraction of the tape.

## Rating from the field

- Last **above the high of every non-circular bar** + a live kill → the kill is **Sell**. On a bull open, that Sell stays in the kill column.
- Last inside the range, thesis intact → **Hold** on the cover only if there is no bull path above the tape. Buy on the cover when the bull path clears the tape and the next kill is not the case you are publishing.
- Last **below the low**, pillars intact → **Buy**

User-stated direction wins if they assert one. Label `Draft view — not investment advice`.

## Table contract

```
Method | Low | Mid | High | Weight | In blend? | What moves it
```

Same `value_shares`, same net-debt identity, as-of price labeled. Skip a bar only with a one-line why.

## Drill-downs (not new bars)

The field stays one picture. Under it, three sub-views and three deck appendix slides: **Comps** (peer rows and the three ratios), **Precedents** (deal rows), **Assets** (book / PPE − ND / replacement). They explain the bars. They do not add a fourth blend.

## Do not

- Do not invent a parallel DCF/comps engine.
- Do not weight circular bars “a little.”
- Do not hide a Sell kill. On a bull open it is the miss case, not the cover.
