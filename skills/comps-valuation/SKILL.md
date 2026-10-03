---
name: comps-valuation
description: >
  Comparable company analysis. User-picked peer set, or a researched set
  from the 10-K and adjacent names. Always show P/E, EV/EBITDA, and
  EV/Sales. Blank or NM — never invent a multiple.
---

# Comparable company analysis (CCA / trading comps)

Write `artifacts/{TICKER}/03-models/comps.md`. This is the trading-comps bar. Precedent deals are [transaction-comps](../transaction-comps/SKILL.md).

## Who picks the set

Two modes. Do not mix them silently.

1. **User-picked.** If the user names tickers, that is the set. Do not add or drop a name. Still write why each is imperfect. A name with no sourced denominator stays in the table as `NM` and out of the median.
2. **Researched default.** If the user does not name a set, build one:
   - Start with competitors named in the latest 10-K / 20-F.
   - Add adjacent public names in the same business (not the same SIC code alone).
   - Size: prefer 0.25×–4× revenue or enterprise value. Outside that band, keep the name only with a one-line why.
   - 6–12 candidates, 5–10 in the final median. Fewer is fine if you say so.
   - Exclusion list is part of the work: REITs, equipment vendors, pure miners on a cloud name, ADRs with a broken share count. Write the reason. Do not hide them.

The researched set is the one that feeds the official football field. A canvas toggle is a **draft what-if**. It does not rewrite the published blend unless the user says to lock the new set into the memo.

## Three ratios, every peer

Compute all three when the denominator exists. One column may be the one applied to the target. The other two still print.

| Ratio | Numerator | Denominator | Use when |
|---|---|---|---|
| P/E | Equity price × diluted shares, or market cap | LTM or NTM earnings to common | Stable profit |
| EV/EBITDA | Equity value + net debt − cash (standardized) | LTM or NTM EBITDA | Default operating multiple |
| EV/Sales | Same EV | LTM or NTM revenue | High growth, thin profit, or EBITDA `NM` |

Also show **P/S** (market cap / sales) when EV is a `DATA_GAP` (BTC treasury, leases, convertibles, or debt you cannot standardize). Say that P/S is the proxy, not a silent rename of EV/Sales.

**NM** — loss, transition-year earnings, missing standardized debt, or a blank filing. Never manufacture EBITDA to fill the column. Never build EV by ignoring treasuries, leases, or converts.

## Stats and the applied bar

- Label **LTM vs NTM** and the price date on every column.
- Stats on the **in-set** peers only, target excluded: min / 25th / **median** / 75th / max. Prefer median to mean.
- Outliers (>~2σ): footnote or drop, and say which.
- Own current multiple reprints the tape. Do not use it as the comp. Draw it dashed, weight 0, if you show it.
- Implied equity = chosen multiple × target metric → net-debt bridge if the multiple is EV → `/ value_shares`.

```
Metric used in the blend: <P/E | EV/EBITDA | EV/Sales | P/S proxy>
Why the others are not: <one line, or NM reason>
```

## Peer row contract

```
Ticker | Why in | Why imperfect | Price | Shares | Period | P/E | EV/EBITDA | EV/Sales | P/S if EV is NM | In researched set? | In this median?
```

## Canvas and deck

Valuation stays one tab. Sub-view **Comps**: the peer table, the three ratios, inclusion toggles, researched-set reset, and a draft implied $/sh that does not move the official call. Deck appendix slide after the 10-slide spine, not a replacement for the football field.

## Do not

- Do not invent a peer or a multiple.
- Do not let a toggle on the canvas change Buy/Hold/Sell by itself.
- Do not build the precedent-deal stack here.
