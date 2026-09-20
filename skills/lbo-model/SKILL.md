---
name: lbo-model
description: >
  Teaching-quality LBO: Sources & Uses, operating forecast, debt schedule,
  returns (IRR/MOIC), and sensitivity. Use for PE-style sponsor returns analysis
  or when user asks for LBO / leveraged buyout model.
version: "1.0.0"
---

# LBO Model

<!-- Provenance: Anthropic financial-services lbo-model (S&U, debt schedule,
     formulas-over-hardcodes, section checkpoints) -->

## Hard rules
- Label every leverage / rate / exit multiple assumption.
- Do not invent EBITDA or purchase price — tie to statements or user case.
- Educational default: simplified but complete S&U → returns path.

## Sections (build in order; verify each)
1. **Transaction assumptions** — Entry EBITDA, entry multiple, equity contribution %, debt tranches (amount, rate, amort), fees, exit year, exit multiple.
2. **Sources & Uses** — Must balance.
3. **Operating model** — Revenue, EBITDA, FCF available for debt paydown.
4. **Debt schedule** — Beginning, draws, amort, interest, mandatory/optional paydown, ending; cash sweep rules stated.
5. **Returns** — Sponsor MOIC & IRR (base); optional management rollover.
6. **Sensitivity** — Entry vs exit multiple; EBITDA growth vs exit multiple.

## Outputs
```
artifacts/{TICKER}/03-models/lbo.md
artifacts/{TICKER}/03-models/lbo.xlsx   # optional
```

## Teaching notes (include briefly in output)
- Why leverage amplifies equity returns and risk
- Covenant / refinance risk qualitatively
- Exit multiple vs entry (multiple expansion not a free lunch)
