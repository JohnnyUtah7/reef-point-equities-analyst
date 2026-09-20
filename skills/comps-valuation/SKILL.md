---
name: comps-valuation
description: >
  Build trading comps / multiples valuation: peer set, operating metrics,
  EV/Revenue, EV/EBITDA, P/E, mix-transition caveats, and statistical summary
  (quartiles). Use for relative valuation, IPO/M&A context, or triangulation
  with DCF.
version: "1.1.0"
---

# Comps Valuation (Trading Comps)

<!-- Provenance: Anthropic financial-services comps-analysis (source hierarchy;
     institutional table layout) -->

## Hard rules
- Prefer SEC/primary data for fundamentals; market data needs as-of timestamps.
- Do **not** invent peer multiples — if a peer lacks data, leave blank and exclude from median or mark `NM`.
- Document peer inclusion/exclusion rationale.
- **Dilution (hard):** Implied equity value → $/sh must state basic vs fully diluted share count when converts/ATM/options exist; DATA_GAP on FD → flag; do not present undiluted as “the” value.
- **Mix transition (hard):** If LTM revenue mix differs materially from the forward thesis (e.g. BTC-heavy LTM vs AI/HPC forward), require an explicit **mix transition** callout. Do **not** apply pure-AI (or other forward-segment) peer multiples to BTC-heavy (or otherwise mismatched) LTM without labeling the mismatch and preferably showing a mix-adjusted or segment-weighted view.
- **ARR:** If using ARR multiples, label ARR as **non-GAAP operating metric** and disclose tape-implied/circular multiples.

## Steps
1. **Peer set** — Start from intake draft; refine by business mix, growth, margin, geography, size. 6–12 names typical. Align peers to **current LTM mix** and note if forward mix implies a different peer set.
2. **Mix transition check** — Compare LTM segment/revenue mix vs stated forward thesis. If material gap → write callout before applying multiples.
3. **Metrics table** — For target + peers: price, mkt cap, net debt, EV, revenue, EBITDA, EPS, growth, margins; basic + FD shares for target.
4. **Multiples** — EV/Rev, EV/EBITDA, P/E (NTM if available else LTM — label clearly), maybe EV/FCF; ARR multiples only with non-GAAP label + source of multiple.
5. **Stats** — Min / 25th / median / 75th / max; highlight target percentile.
6. **Implied value** — Apply peer median (and 25th/75th) multiples to target metrics → equity value range → $/sh basic and FD.
7. **Caveats** — Accounting differences, one-offs, different FYE, growth gaps, **mix transition**, dilution.

## Outputs
```
artifacts/{TICKER}/03-models/comps.md
artifacts/{TICKER}/03-models/comps.xlsx   # optional
```

## Data priority
1. User-provided / MCP institutional feeds (if configured)
2. SEC filings for fundamentals
3. Market quotes with timestamp
4. Web only as last resort — flag lower confidence
