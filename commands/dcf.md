---
name: dcf
description: Build a DCF for the given ticker using SEC-backed statements
---

# DCF

1. If `02-statements` missing, run `sec-filings` then `financial-statements`
2. Run `dilution-if-converted` when converts/ATM/options exist or may exist
3. Run `dcf-model` with `valuation-conventions` (odd 5×5, center = base, TV % of EV)
4. Open `artifacts/{TICKER}/03-models/dcf.md` — `$/sh` on if-converted count
