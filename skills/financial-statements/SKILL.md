---
name: financial-statements
description: >
  Normalize income statement, balance sheet, and cash flow into a clean working
  model; build FCF bridge (EBIT → NOPAT → FCFF); label non-GAAP ARR and share
  counts. Use after sec-filings when you need standardized historicals for DCF,
  comps, or unit economics.
version: "1.1.0"
---

# Financial Statements Normalization

<!-- Provenance: analyst-kit analyzing-financial-statements; Anthropic 3-statement conventions -->

## Hard rules
- Every line item cites filing form/date from `01-sec/`.
- Label units (USD mm / bn) and scale consistently.
- Flag one-time items; do not silently "adjust" without a reconciling line.
- **ARR / non-GAAP (hard):** ARR, contracted ARR, operating ARR, RPO (when used as run-rate), and similar metrics are **non-GAAP operating metrics**. Always label them as such in tables and prose. Never juxtapose with GAAP revenue in the same cell/column without the non-GAAP label and a clear separation (e.g. separate subsection “Non-GAAP operating metrics”).
- **Shares:** Report basic and diluted weighted-average shares from the statements; note convertible / ATM overhang for the dilution skill.

## Inputs
- `artifacts/{TICKER}/01-sec/financials_*.json` (+ intake)

## Steps
1. **Map taxonomy** — Align XBRL tags to standard lines: Revenue, COGS, Gross profit, OpEx, EBIT, Interest, EBT, Tax, Net income; BS cash, ST/LT debt, equity; CF CFO, CapEx, FCF.
2. **History table** — 3–5 fiscal years (+ LTM if 10-Q available). Show YoY growth. GAAP revenue only in GAAP tables.
3. **Non-GAAP operating metrics (separate block)** — ARR / contracted ARR / etc. only if disclosed; each labeled **non-GAAP operating metric** with form/date cite.
4. **FCF bridge**
   ```
   EBIT
   - Taxes on EBIT (NOPAT)
   + D&A
   - CapEx
   - ΔNWC (increase in NWC = use)
   = FCFF
   ```
5. **Quality checks** — BS balances; CF cash roll-forward vs BS cash; diluted shares vs basic; net debt = ST+LT debt − cash; convert notes flagged for `dilution-if-converted`.
6. **Write** normalized markdown tables + assumptions (tax rate used, NWC definition).

## Outputs
```
artifacts/{TICKER}/02-statements/normalized_is_bs_cf.md
artifacts/{TICKER}/02-statements/fcf_bridge.md
```

## Failure modes
- Banks/insurers → standard FCFF bridge may not apply; note specialized model needed.
- Negative NWC businesses → document definition carefully.
- Treating ARR as GAAP revenue → FAIL under risk-audit.
