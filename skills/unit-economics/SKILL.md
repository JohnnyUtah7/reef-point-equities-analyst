---
name: unit-economics
description: >
  Analyze margins, ROIC, capital allocation, and (when relevant) SaaS-style unit
  economics (LTV/CAC, NDR, ARR). Use for quality-of-business assessment and capital
  cycle insight.
version: "1.1.0"
---

# Unit Economics & Capital Returns

<!-- Provenance: Anthropic PE unit-economics; general ROIC / FCFF quality checks -->

## Hard rules
- Match metrics to business model (do not force LTV/CAC on a retailer).
- ROIC needs invested capital definition stated (goodwill in/out).
- **ARR / non-GAAP (hard):** ARR, contracted ARR, operating ARR, NDR, RPO-as-run-rate must be labeled **non-GAAP operating metric**. Never present ARR as if it were GAAP revenue or juxtapose without the label.

## Steps
1. **Model ID** — Product, subscription, transactional, marketplace, hybrid.
2. **Margin stack** — Gross → operating → FCF margin, 3–5Y trend (from statements) — GAAP basis.
3. **ROIC / ROE** — NOPAT / invested capital; trend vs WACC (spread).
4. **Capital allocation** — CapEx vs growth, buybacks, dividends, M&A; from CF statement + 10-K narrative (cited).
5. **If SaaS-like and disclosed** — NDR, churn, RPO/backlog, CAC payback, ARR — only from filings/exhibits; each ARR-like metric labeled non-GAAP.
6. **Scorecard** — 5–8 bullets: quality signals vs warning signs.

## Outputs
```
artifacts/{TICKER}/04-research/unit_economics.md
```
