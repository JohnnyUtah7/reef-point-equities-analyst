---
name: company-intake
description: >
  Parse a ticker or company name, normalize identity (ticker, CIK, exchange,
  sector), seed peer list and artifact folder. Use when the user says "check out
  AAPL", "analyze NVDA", "look at this company", or at the start of any full
  pipeline before SEC pulls.
version: "1.0.0"
---

# Company Intake

<!-- Provenance: analyst-kit single-stock-deep-dive intake + edgartools Company() resolve -->

## Hard rules
- Never invent CIK or fiscal year-end. Resolve from EDGAR or label `UNRESOLVED`.
- Create `artifacts/{TICKER}/` before any other skill writes files.

## Inputs
- Free text: ticker, name, or URL ("check out this company: NVDA")
- Optional: peer overrides, currency, fiscal calendar hint

## Steps
1. **Parse** — Extract ticker (prefer explicit symbols). If only a name, resolve via `Company("Name")` / EDGAR ticker map. Normalize to uppercase ASCII ticker.
2. **Identity block** — Write:
   - Legal name, ticker, exchange, CIK, SIC/sector (if available)
   - Reporting currency, FYE month
   - Latest share price source + as-of date (or `PRICE_GAP`)
3. **Seed peers** — Propose 4–8 comps with one-line rationale; mark as draft until `comps-valuation` / `competitive-analysis` confirm.
4. **Artifact bootstrap** — Create layout per `references/artifact-layout.md`. Write `artifacts/{TICKER}/00-intake.md` and append a line to `RUNLOG.md`.
5. **Handoff** — Return TICKER + path to intake file. Next skill: `sec-filings`.

## Output contract
```
artifacts/{TICKER}/00-intake.md
artifacts/{TICKER}/RUNLOG.md
```

## Failure modes
- Ambiguous name (e.g. "Meta") → ask which entity / show candidates; do not guess.
- Non-US issuer → note ADR/foreign filer; SEC XBRL may be limited.
