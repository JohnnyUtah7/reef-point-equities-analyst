---
name: sec-pull
description: Pull SEC filings and XBRL financials for a ticker
---

# SEC pull

1. Check `EDGAR_IDENTITY` (`references/edgar-identity.md`)
2. Run `company-intake` if needed
3. Run `sec-filings` (prefer `scripts/edgar_pull.py`)
4. Flag convertibles / ATM / options for `dilution-if-converted`
