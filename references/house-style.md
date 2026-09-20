# Reef Point house style

Quality bar: desk density, SpaceX / Anduril surface. Not a public equity PDF. Not navy IB.

How a name is *run*: skill `portfolio-research`. Studio skills own filings and models. This file owns how the published note looks and how the rating is allowed to be written.

## Look

- Black, white, hairline rules, one muted accent (`#B91C1C` sparse). Tight grotesque type. No stock gradients, no navy-and-gold IB theme (`#1F4E79` — reject), no clip-art icons.
- Cover: full white field, `assets/rpc-logo.png` centered, ticker and date in small caps under the mark only if needed. No headers, no confidential strip on the cover.
- Interior: takeaway line at top of every content slide. Slide numbers. Proprietary footer. Logo small, top-right — never competing with the cover lockup.
- Condensed. One idea per slide. Tables over paragraphs. Football field is the valuation spine.

## Every name (executable)

1. **Studio first.** `full-company-analysis` steps 1–13. Apply `valuation-conventions`: formulas over hardcodes, blue inputs with source comments, odd 5×5, center = base. Do not memorize 10-K numbers.
2. **Dilution before `$/sh`.** `dilution-if-converted`. Official bars share one value-relevant count (usually ITM if-converted).
3. **Exec summary first in the published note:** Buy / Hold / Sell, target range, central target, upside/downside vs last, three bullets, key risk. Label `Draft view — not investment advice.` No conviction line on the cover.
4. **Three-statement model in Sheets** per `sheets-workbook`. Notes column on Assumptions. Checks tab must pass.
5. **Football field** per `football-field`. Methods: DCF, trading comps, transaction comps, SOTP / NAV, replacement, yield / residual. Skip only with why. Same diluted count.
6. **Blend** uses non-circular mids only. Starting weights: DCF 40–60, trading 15–40, txns 10–25, SOTP if live, replacement 0–15. A bar that reprints the tape (own EV ÷ own ARR) may show; weight = 0.
7. **Five audits + UNVERIFIED.** Filings vs model, share count, unit economics, peer set, residual vs implied (TV % of EV). Then `research-auditor`. Studio `risk-audit` is the first gate. Do not publish on `FAIL`.
8. **Rating tightness.** Call matches the field. Tape above every non-circular high + live kill = Sell, not a courtesy Hold. Pillars: claim / driver / mechanism / magnitude / timeframe / kill (`memo-pillars`). Rate **after** the field.
9. **Earnings calls** (`earnings-call-analysis`) are a companion. They do not move the rating.
10. **Deck path:** PPTX from `assets/house-template.pptx` → Drive conversion → native Slides. White RPC cover. No Zapier. No `gws` as official.

Official memo: `docs/{ticker-lower}-equity-research.md` when `docs/` exists; otherwise `artifacts/{TICKER}/04-research/memo.md`.
