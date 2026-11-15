---
name: sec-pull
description: Pull EDGAR filings and standardized financials for one ticker into artifacts/{TICKER}/01-sec/.
---

# SEC pull

1. Follow `skills/company-intake/SKILL.md` and `skills/sec-filings/SKILL.md`.
2. Discover callable hosted EDGAR tools first; no local identity is required for hosted calls.
3. Only for the local fallback, confirm `EDGAR_IDENTITY` is configured and `import edgar` succeeds, then run `python3 scripts/edgar_pull.py TICKER --out artifacts/TICKER/01-sec`.
4. Stop the local path if identity is missing. Never WebFetch sec.gov or run two competing SEC stacks.
