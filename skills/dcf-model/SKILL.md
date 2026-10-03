---
name: dcf-model
description: >
  Unlevered FCFF DCF with WACC/CAPM, Gordon + exit cross-check, odd 5×5
  sensitivity (center = base). Base year from statements only.
---

# DCF model

Apply `valuation-conventions` while you build. Write `artifacts/{TICKER}/03-models/dcf.md`.

```
Ke   = rf + β × ERP          # rf = dated 10y UST; no 4.5% default
Kd   = pre_tax_debt × (1 − t)
WACC = We×Ke + Wd×Kd
TV   = FCF_{n+1} / (WACC − g)   or   Year-N EBITDA × exit
EV   = Σ PV(FCFF) + PV(TV)
Eq   = EV − net_debt − NCI + associates
```

- Explicit 5–10 years. g < WACC. Flag TV **>75% of EV**.
- Net debt: say cash definition (restricted out unless free to equity).
- Cover shares for the **draft** `$/sh` only. Official mid waits for `dilution-if-converted`.
- Sensitivity: **5×5**, center cell = base WACC and g, center output = model `$/sh`.

Revenue path is **judgment** with a mechanism. Do not set year-1 revenue = contracted ARR.

## Do not

- Invent base-year revenue.
- Add back SBC by default.
- Copy another name’s WACC, beta, or revenue path.
