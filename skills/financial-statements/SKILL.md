---
name: financial-statements
description: >
  Normalize IS / BS / CF from the SEC pull. EBIT → NOPAT → FCFF bridge.
  Do not invent a base year.
---

# Financial statements

Source: `artifacts/{TICKER}/01-sec/financials.json` + notes. Units: state the 10-K scale (often **thousands**) and publish models in **millions** (÷ 1,000). Write the scale on every table.

## Outputs

`artifacts/{TICKER}/02-statements/normalized_is_bs_cf.md`  
`artifacts/{TICKER}/02-statements/fcf_bridge.md`

## Normalize

3–5 historical years if present. Same periods on IS/BS/CF.

```
Gross profit = Revenue − COGS          # say if D&A is inside COGS
EBIT        = operating income as filed (flag one-offs)
NOPAT       = EBIT × (1 − t)
FCFF        = NOPAT + D&A − CapEx − ΔNWC
```

Flag, do not silently “adjust”: impairments, SBC, unrealized gains, debt inducement, deferred-revenue CFO.

## Checks

- BS balances (assets = liab + equity) or explain rounding.
- CF: CFO + CFI + CFF = Δ cash; ending cash = BS cash.
- Segment split only from 8-K/10-K notes, not from memory.

## Do not

- Use another name’s 10-K scale or mix as a default.
- Treat ARR / bookings as GAAP revenue.
- Add back SBC as if it were free cash (house: SBC is a real cost).
