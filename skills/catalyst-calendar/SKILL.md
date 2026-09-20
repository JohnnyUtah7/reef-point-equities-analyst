---
name: catalyst-calendar
description: >
  Build a calendar of earnings, filings, product, regulatory, and macro catalysts
  for a ticker or small universe. Use for event planning, preview notes, or full
  analysis packaging.
version: "1.0.0"
---

# Catalyst Calendar

<!-- Provenance: Anthropic equity-research catalyst-calendar -->

## Hard rules
- Dates must be sourced (company IR, SEC filing, exchange calendar) or marked `ESTIMATED`.
- Do not invent FDA/PDUFA or court dates.

## Steps
1. Horizon — next 30 / 90 / 180 days (ask if unclear).
2. Gather:
   - Earnings date/time (pre/post)
   - 10-K/10-Q expected windows
   - Investor days, conferences
   - Product launches, regulatory, contracts (cited)
   - Debt maturities / capital actions if material
3. Table: Date | Event | Type | Source | Thesis relevance (H/M/L)
4. **Positioning note** — What would surprise vs a base case (judgment, labeled).

## Outputs
```
artifacts/{TICKER}/04-research/catalysts.md
```
