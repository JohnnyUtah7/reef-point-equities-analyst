# Provenance

Reef Point Equity Research **2.0.0** is the team product. It is **not** a byte-copy of the Mac-local Equity Research Studio 1.0.1 plugin (that pack is not in this repo). IREN was the first live name; this pack is the reusable engine.

Techniques distilled from public packs (not vendored):

| Source | What we kept |
|---|---|
| [dgunning/edgartools](https://github.com/dgunning/edgartools) | `EDGAR_IDENTITY`, `Company()`, `get_financials()`, 20-F/40-F/6-K fallback, no bare sec.gov fetch |
| [mohitjandwani/analyst-kit](https://github.com/mohitjandwani/analyst-kit) | User-Agent discipline, 8-K EX-99.1/99.2 for non-GAAP KPIs, auditor hunt + UNVERIFIED, never publish on FAIL |
| [anthropics/financial-services](https://github.com/anthropics/financial-services) | Formulas over hardcodes, odd 5×5 center=base, comps hierarchy, LBO S=U, Pitch Agent field = min/median/max + last-print |
| [GeniusTrader-Harry/equity-research-skill](https://github.com/GeniusTrader-Harry/equity-research-skill) | Pillars (claim / driver / mechanism / magnitude / timeframe / kill). **Rejected:** commit direction before the model |
| [himself65/finance-skills](https://github.com/himself65/finance-skills) | SOTP HQ line, net debt once. **Rejected:** yfinance-first |

House-only (not in those packs): if-converted table, circularity veto, replacement floor, yield skip rule, PPTX→Drive convert, Sheets workbook.

**Rejected as official:** Zapier, `gws`, jackchuka markdown-first slides, IB navy `#1F4E79`, CapIQ wait-forever.
