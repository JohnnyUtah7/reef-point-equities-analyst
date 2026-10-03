---
name: sec-pull
description: Pull EDGAR filings and standardized financials for one ticker into artifacts/{TICKER}/01-sec/.
---

# SEC pull

1. Confirm `$EDGAR_IDENTITY` and `import edgar`.
2. Run `skills/company-intake/SKILL.md` then `skills/sec-filings/SKILL.md`.
3. Prefer `python3 scripts/edgar_pull.py TICKER --out artifacts/TICKER/01-sec`.
4. Stop if identity is missing. Never WebFetch sec.gov.
