---
name: sec-filings
description: >
  Pull 10-K / 10-Q / 8-K or 20-F / 6-K + XBRL via edgartools. Stop if
  EDGAR_IDENTITY is missing. Never WebFetch sec.gov.
---

# SEC filings

When the Reef Point EDGAR MCP is connected, call it first:

1. `company_lookup` for CIK, name, exchange, SIC.
2. `recent_filings` for the latest 10-K or 20-F, the latest 10-Q, and the latest 8-K or 6-K.
3. `company_facts` for revenue, shares, cash, and debt.

Cite form, period end, filed date, and accession from the tool result. Do not replace those figures with a model output.

If the MCP is not connected, use the local pull:

```bash
python3 scripts/edgar_pull.py {TICKER} --out artifacts/{TICKER}/01-sec
```

Do not run both for the same ticker. Then **read** the latest periodic and the latest earnings exhibit. Write cited excerpts only into `01-sec/notes.md`.

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
- No bare `sec.gov` fetch. One EDGAR path per ticker: the MCP, or `edgar_pull.py`.

## Outputs

`company_meta.json` · `filings_index.json` · `periodic_filings.json` · `financials.json` · `financials_text.json` · `notes.md`
