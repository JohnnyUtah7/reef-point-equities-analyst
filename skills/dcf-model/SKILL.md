---
name: dcf-model
description: >
  Build a teaching-quality DCF: historical bridge, explicit FCF projections,
  WACC (CAPM), terminal value (Gordon and/or exit multiple), equity bridge,
  basic vs fully diluted per-share, TV as % of EV, and sensitivity tables. Use
  when valuing a company intrinsically or when the orchestrator reaches the
  valuation stage.
version: "1.1.0"
---

# DCF Model

<!-- Provenance: Anthropic financial-services dcf-model (formulas-over-hardcodes,
     odd-sized sensitivity with center = base); analyst-kit creating-financial-models -->

## Hard rules
- **Never invent base-year financials** — pull from `02-statements/` or cite filing.
- List **Assumptions** block before results (growth, margins, WACC components, g or exit multiple, shares, net debt).
- Prefer live Excel formulas over Python-hardcoded outputs when writing `.xlsx`.
- Sensitivity: **odd** grid (5×5); **center cell = base case**.
- **Dilution (hard):** Always compute and show **basic vs fully diluted** share counts when convertibles/ATM/options/RSUs/warrants exist. Per-share values must state which share count. If if-converted shares are `DATA_GAP`, flag it and do **not** present undiluted $/sh as “the” value. Prefer inputs from `dilution-if-converted` / `01-sec/dilution_if_converted.md`.
- **TV visibility (hard):** Report **terminal value as % of enterprise value** in the valuation summary (flag if >80% without discussion).

## Inputs
- Normalized statements + FCF bridge
- Market: price, beta, risk-free, ERP, target debt/equity (sourced or assumed with label)
- Basic shares, diluted / if-converted shares, net debt (cite 10-K/10-Q); convert notes when present

## Workflow
1. **Confirm base year** with user or RUNLOG (rev, EBIT margin, FCF, basic shares, diluted shares, net debt).
2. **Project** 5–10 years: revenue growth path, margin path, D&A%, CapEx%, NWC% — each driver explicit.
3. **WACC**
   - Ke = rf + β × ERP (+ size premium if used, labeled)
   - Kd = pre-tax cost of debt × (1 − tax)
   - WACC = We×Ke + Wd×Kd
4. **Terminal value**
   - Gordon: TV = FCF_{n+1} / (WACC − g), with g ≤ long-run GDP-ish and g < WACC
   - Optional exit multiple on Year-N EBITDA/EBIT — show both if useful
   - Compute **TV / EV %** for the chosen TV method
5. **Bridge** — Enterprise value = PV(FCF) + PV(TV); Equity = EV − net debt (+ associates − NCI as needed).
6. **Per-share** — Equity ÷ basic shares **and** Equity ÷ fully diluted / if-converted shares (label each). If FD shares DATA_GAP → show basic only with explicit gap flag; never imply undiluted is “the” fair value.
7. **Sensitivity** — WACC vs g (and optionally growth vs margin). Highlight base cell.
8. **Sanity** — Implied vs market price; implied exit multiple; **TV as % of EV**.

## Outputs
```
artifacts/{TICKER}/03-models/dcf.md
artifacts/{TICKER}/03-models/dcf.xlsx   # optional
```

## Output sections (markdown minimum)
1. Assumptions (dated, sourced) — include basic + FD share counts
2. Projection table
3. WACC build
4. Valuation summary (EV, equity, $/sh basic, $/sh FD, **TV as % of EV**, upside/downside vs market)
5. Sensitivity
6. Limitations (incl. dilution DATA_GAPs)
