# Provenance

Reef Point Equities analyst **1.2.0**. Filings engine + house publish overlays. No company note is vendored.

Techniques distilled from public packs (not cloned into this repo):

| Source | What we kept |
|---|---|
| [dgunning/edgartools](https://github.com/dgunning/edgartools) | `EDGAR_IDENTITY`, `Company()`, `get_financials()`, 20-F/40-F/6-K fallback, no bare sec.gov fetch |
| [mohitjandwani/analyst-kit](https://github.com/mohitjandwani/analyst-kit) | 8-K EX-99.1/99.2 for non-GAAP KPIs, auditor hunt + UNVERIFIED, never publish on FAIL |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | Formulas over hardcodes, odd 5×5 center=base, comps hierarchy, LBO S=U, field = min/median/max + last-print |
| [GeniusTrader-Harry/equity-research-skill](https://github.com/GeniusTrader-Harry/equity-research-skill) | Pillars (claim / driver / mechanism / magnitude / timeframe / kill). **Rejected:** commit direction before the model |
| [himself65/finance-skills](https://github.com/himself65/finance-skills) | SOTP HQ line, net debt once. **Rejected:** yfinance-first |

House-only: if-converted table, circularity veto, replacement floor, yield skip, PPTX→Drive convert, Sheets workbook.

**Rejected as official:** Zapier, `gws`, jackchuka markdown-first slides, IB navy `#1F4E79`, CapIQ wait-forever.
