# Technique provenance (distilled, not copied)

This plugin ships curated skill text only — not the source repositories.

| Technique | Public source |
|---|---|
| EDGAR identity + `Company().get_financials()` | [dgunning/edgartools](https://github.com/dgunning/edgartools) |
| SEC filings User-Agent / 8-K exhibits | [mohitjandwani/analyst-kit](https://github.com/mohitjandwani/analyst-kit) |
| DCF formulas-over-hardcodes, odd sensitivity, center = base | [anthropics/financial-services](https://github.com/anthropics/financial-services) `dcf-model` |
| LBO sources & uses / returns | Anthropic `lbo-model` |
| Trading comps hierarchy | Anthropic `comps-analysis` |
| Competitive landscape outline-first | Anthropic `competitive-analysis` |
| Catalyst calendar structure | Anthropic `catalyst-calendar` |
| Unit economics (SaaS/ARR) | Anthropic PE unit-economics |
| Thesis pillars + kill criteria | [GeniusTrader-Harry/equity-research-skill](https://github.com/GeniusTrader-Harry/equity-research-skill) — **not** “commit direction before the model” |
| SOTP segment EV + holdco | [himself65/finance-skills](https://github.com/himself65/finance-skills) SOTP — not yfinance-first |
| Research auditor hunt + UNVERIFIED | analyst-kit `research-auditor` |
| Football field min/median/max + last-print | Anthropic Pitch Agent (idea only; branding rejected) |
| PPTX → native Slides | Drive conversion-on-upload ([google_workspace_mcp#822](https://github.com/taylorwilsdon/google_workspace_mcp/pull/822) pattern) |

## Rejected (do not re-introduce)

- Zapier / Make / n8n
- `gws` / jackchuka markdown-first as the official deck
- IB navy `#1F4E79` Pitch Agent chrome
- FMP / FinMind keys, analyst-kit telemetry
- Vendoring the source repos
- Hardcoded risk-free rate defaults (e.g. 4.5%) as if they were current
