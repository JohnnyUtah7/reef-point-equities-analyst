---
name: sotp-valuation
description: >
  Sum-of-the-parts valuation for multi-segment companies: segment financials,
  segment-appropriate multiples or mini-DCFs, corporate net debt/cash, ARR
  multiple disclosure, and conglomerate discount discussion. Use for diversified
  issuers or when user asks for SOTP / sum of the parts.
version: "1.1.0"
---

# Sum-of-the-Parts (SOTP)

<!-- Provenance: claude-finance-skills sum-of-the-parts-valuation; equity-research
     segment thinking -->

## Hard rules
- Segment revenue/operating income must cite 10-K Note / Item 1 segment disclosure.
- Do not double-count shared corporate costs — show allocation or holdco cost line.
- Net debt applied **once** at the equity bridge.
- **Dilution (hard):** Equity bridge → $/sh must show **basic vs fully diluted** when converts/ATM/options exist; label share count; if-converted DATA_GAP → do not present undiluted as “the” value.
- **ARR / non-GAAP (hard):** If any segment uses ARR / contracted ARR / operating ARR, label it a **non-GAAP operating metric**. SOTP using ARR multiples must disclose if the multiple is **tape-implied / circular** (e.g. mix-shift names: tape EV ÷ own ARR). Prefer independent peer ARR multiples when available; if using tape-implied, say so explicitly and do not treat it as independent corroboration.

## Steps
1. **Segment map** — List reportable segments + geographic if useful; % of sales / op income; note LTM vs forward mix if transitioning.
2. **Method per segment** — Trading multiple vs peers **or** abbreviated DCF; state why. For ARR-based segments: disclose multiple source (peer vs tape-implied).
3. **Corporate / unallocated** — HQ costs, excess cash, investments, pensions, NCI.
4. **Gross SOTP EV** — Sum segment EVs.
5. **Equity bridge** — − net debt − NCI + associates/non-core − other claims (incl. convert treatment if if-converted).
6. **Per-share** — Basic and fully diluted.
7. **Conglomerate discount** — Optional scenario (0–20%) with rationale; show with/without.
8. **Cross-check** — vs single-firm DCF and comps; explain gaps; call out circular ARR multiples.

## Outputs
```
artifacts/{TICKER}/03-models/sotp.md
```

## When to skip
- Single-segment pure-play → note N/A and point to DCF/comps.
