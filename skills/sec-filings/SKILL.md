---
name: sec-filings
description: >
  Pull 10-K / 10-Q / 8-K or 20-F / 6-K + XBRL via edgartools. Stop if
  EDGAR_IDENTITY is missing. Never WebFetch sec.gov.
---

# SEC filings

Prefer:

```bash
python3 scripts/edgar_pull.py {TICKER} --out artifacts/{TICKER}/01-sec
```

Then **read** the latest periodic and the latest earnings exhibit. Write cited excerpts only into `01-sec/notes.md`.

## Form map

| Status | Periodic | Earnings pack |
|---|---|---|
| Domestic | 10-K / 10-Q | 8-K Item 2.02 EX-99.1 / 99.2 |
| FPI | 20-F / 40-F | **6-K** (not 8-K) until they become a 10-K filer |

8-K/6-K exhibits own **non-GAAP KPIs** (ARR, bookings, Adj. EBITDA). Label them. Filing wins if a transcript vendor disagrees.

## Must cite

Every load-bearing number: **form, date, accession**. HTML link optional.

## Hard stops

- Missing `EDGAR_IDENTITY` → stop.
- `get_financials()` empty → try 20-F/40-F before `DATA_GAP`.
- Pin `hishel==0.1.3` if FileStorage errors.
- No bare `sec.gov` fetch. No second EDGAR client.

## Outputs

`company_meta.json` · `filings_index.json` · `periodic_filings.json` · `financials.json` · `financials_text.json` · `notes.md`
