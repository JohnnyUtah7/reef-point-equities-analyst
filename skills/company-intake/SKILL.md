---
name: company-intake
description: >
  Ticker or company name → CIK, FYE, peer seed, artifacts/{TICKER}/. First
  step of analyze TICKER. Stop with UNRESOLVED if EDGAR cannot map the name.
---

# Company intake

Write `artifacts/{TICKER}/00-intake.md` and create the folder tree.

## Resolve

```bash
python3 scripts/edgar_pull.py {TICKER}
```

If the user gave a name not a ticker, try `Company("Name")` via the same script once you have a ticker candidate. Do not guess a CIK.

| Field | Required |
|---|---|
| Legal name | Yes |
| Ticker + exchange | Yes or `UNRESOLVED` |
| CIK | Yes or stop |
| Reporting currency | Yes |
| Fiscal year-end | Yes |
| Filer status | 10-K vs 20-F / FPI vs domestic |
| Cover shares + as-of | If the latest periodic is in the pull |
| Last price + as-of | Dated; label `PRICE_GAP` if not live |
| Business one-liner | From Item 1 / 20-F Item 4, cited |
| Draft peer seed | 4–8 names; confirm later in comps |

## Issuer class (sets later skips)

| Class | Later |
|---|---|
| Single-segment operating co | SOTP skip OK |
| Multi-segment / conglomerate | SOTP required |
| Asset-heavy (DC, rooms, fleet, PPE) | Replacement live |
| Asset-light software | Replacement skip |
| Bank / insurer | Specialized-model flag; no fake FCFF sufficiency |
| No dividend + RI ≤ 0 | Yield skip |

## Do not

- Invent a ticker for a private company.
- Copy IREN peers, FYE, or share count.
- Continue the pipeline on `UNRESOLVED`.
