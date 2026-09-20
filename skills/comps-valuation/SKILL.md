---
name: comps-valuation
description: >
  Trading comps: peer set, EV/Rev, EV/EBITDA, P/E, quartiles → implied value.
  Blank or NM — never invent a multiple.
---

# Trading comps

Write `artifacts/{TICKER}/03-models/comps.md`.

- 6–12 peers. Inclusion / exclusion rationale (mix, size, FYE).
- Metric: EV/EBITDA default; EV/Rev if lossy/high growth; P/E if stable profit; P/B if financials; P/S only if EV is a `DATA_GAP` (say why).
- Stats: min / 25th / **median** / 75th / max. Prefer median.
- Label LTM vs NTM. Dated prices.
- Implied equity = multiple × target metric → net debt bridge → `/ value_shares` (after dilution exists; until then show cover and mark draft).

**NM** if the denominator is loss, transition-year junk, or missing standardized debt. Do not build a fake EV by ignoring BTC treasuries, leases, or convertibles.

Transaction comps are a **different** skill.
