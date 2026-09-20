---
name: competitive-analysis
description: >
  Map peers, industry structure, moat hypotheses, positioning, and mix-transition
  context. Use when the user asks who competes with a company, for a market map,
  or as part of full company analysis before the memo.
version: "1.1.0"
---

# Competitive Analysis

<!-- Provenance: Anthropic financial-services competitive-analysis (outline-first) -->

## Hard rules
- Outline before deep write-up when producing a long competitive deck.
- Peer facts need sources; moat statements are hypotheses until evidenced.
- **Mix transition (hard):** If LTM revenue mix differs materially from the forward thesis (e.g. BTC mining → AI cloud), require an explicit **mix transition** callout: what % LTM is still “old” mix, what the company guides toward, and which peer set applies to which mix. Do not treat the firm as a pure forward-segment peer without labeling.

## Steps
1. **Scope** — Protagonist + competitor set (confirm vs intake).
2. **Mix transition** — LTM segment/revenue mix vs forward thesis; call out material gaps before peer mapping.
3. **Industry structure** — Customers, suppliers, substitutes, new entrants, rivalry (Porter-lite, short).
4. **Peer cards** — For each peer: offering overlap, scale, margin/growth snapshot, differentiation; tag peers as LTM-relevant vs forward-relevant when mix is shifting.
5. **Positioning** — 2×2 or table (e.g. growth vs margin, price vs performance) — state axes.
6. **Moat hypotheses** — Network, switching costs, cost advantage, intangible, scale — evidence vs wishful.
7. **Share / TAM** — Only with cited market research or company-disclosed share; else `DATA_GAP`.
8. **Implications for thesis** — What must be true for protagonist to win; how mix transition affects comps and narrative.

## Outputs
```
artifacts/{TICKER}/04-research/competitive.md
```
