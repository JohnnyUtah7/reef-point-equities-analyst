---
name: sec-filings
description: >
  Pull 10-K / 10-Q / 8-K filings and XBRL financials from SEC EDGAR using
  edgartools or User-Agent-compliant fetches. Use when the user needs filings,
  financial statements from EDGAR, risk factors, MD&A, or any SEC primary source.
  Requires EDGAR_IDENTITY.
version: "1.1.0"
---

# SEC Filings

<!-- Provenance: edgartools core skill; analyst-kit sec-filings User-Agent patterns -->

## Hard rules
- **Never invent filing numbers.** If pull fails, write the error and stop.
- Cite `form`, `filing_date`, `accession` on every extracted figure.
- Set identity first — see `references/edgar-identity.md`. Bare WebFetch to sec.gov → 403.

## Prerequisites
```bash
export EDGAR_IDENTITY="Your Name you@email.com"
pip install edgartools   # preferred
# Pin note (FileStorage): if EDGAR pull fails on hishel FileStorage errors,
# pin hishel==0.1.3 — hishel 1.1.8 broke compatibility with edgartools caching.
pip install 'hishel==0.1.3'
```

## Preferred pull (edgartools)
```python
from edgar import Company, set_identity
import os
set_identity(os.environ["EDGAR_IDENTITY"])
c = Company("AAPL")
fins = c.get_financials()
# income_statement / balance_sheet / cash_flow as available
filings = c.get_filings(form=["10-K", "10-Q", "8-K"])
```

Or thin wrapper:
```bash
python ${CURSOR_PLUGIN_ROOT}/scripts/edgar_pull.py AAPL
# or relative: python scripts/edgar_pull.py AAPL
```

## Steps
1. Confirm `EDGAR_IDENTITY` is set; if missing, stop and ask.
2. Resolve company from `00-intake.md` ticker.
3. Pull filings index (last ~3 years of 10-K/10-Q + recent 8-K).
4. Extract structured financials (XBRL) into JSON/text tables.
5. Optionally extract: Item 1A risk factors headings, MD&A revenue driver quotes (with page/section cite).
6. Flag convertible notes / ATM / equity overhang for `dilution-if-converted`.
7. Write artifacts; update RUNLOG.
8. On **FileStorage / hishel** errors → pin `hishel==0.1.3` and retry (see references/edgar-identity.md).

## Outputs
```
artifacts/{TICKER}/01-sec/filings_index.json
artifacts/{TICKER}/01-sec/financials_text.json   # or financials.json
artifacts/{TICKER}/01-sec/notes.md                # cited excerpts only
```

## Anti-patterns
- Scraping HTML without User-Agent
- Mixing FY and calendar quarters without labeling
- Using "remembered" revenue from training data
