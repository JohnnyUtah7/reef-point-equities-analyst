---
name: scenario-sensitivity
description: >
  Build bull / base / bear scenarios and tornado / two-way sensitivity on key
  value drivers. Use after DCF/comps exist, or when user asks for scenarios,
  stress test, or tornado chart.
version: "1.0.0"
---

# Scenario & Sensitivity

<!-- Provenance: analyst-kit creating-financial-models sensitivity; Anthropic DCF
     scenario blocks -->

## Hard rules
- Scenarios differ by **named drivers**, not arbitrary price targets.
- Bear case must be plausible (not cartoon); bull must not assume infinite margin expansion without mechanism.

## Steps
1. **Driver list** — e.g. rev growth Y1–5, EBIT margin, WACC, terminal g, exit multiple.
2. **Three scenarios** — Table of driver values; narrative trigger for each.
3. **Value outputs** — Equity value / share under each; probability weights optional (label subjective).
4. **Tornado** — One-way swing each driver ± stated amount; rank by value impact.
5. **Two-way** — Reuse DCF WACC×g table; ensure base at center.
6. **Decision use** — Which driver kills the thesis first? Link to memo kill criteria.

## Outputs
```
artifacts/{TICKER}/03-models/sensitivity.md
```
