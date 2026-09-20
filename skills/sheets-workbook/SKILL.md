---
name: sheets-workbook
description: >
  Build the official three-statement + methods workbook (openpyxl formulas,
  blue inputs, odd sensitivity) and convert to native Google Sheets via Drive.
  Triggers: Google Sheets model, xlsx workbook, football field spreadsheet.
---

# Sheets workbook

Required on `analyze TICKER`. Not a second DCF engine — it **hosts** studio numbers as live formulas.

## File

`docs/{ticker-lower}-model.xlsx` when `docs/` exists; else `artifacts/{TICKER}/03-models/{ticker}-model.xlsx`. Author with **openpyxl**. Then Drive conversion-on-upload (same trick as PPTX).

```
title:                 {TICKER} Model — Reef Point
contentMimeType:       application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
disableConversionToGoogleType: false
```

Confirm MIME `application/vnd.google-apps.spreadsheet`. Return `https://docs.google.com/spreadsheets/d/{id}/edit`. No Zapier. No Sheets API authoring from scratch.

If Drive is missing / 401: write the local xlsx, say Drive is required for native Sheets, and stop. Do not invent a URL.

## Tabs (this order)

| Tab | What |
|---|---|
| Cover | Ticker, as-of, rating, last, PT range / central, `value_shares`, FX if any |
| Assumptions | Every driver; **Notes** column mandatory (`[source]` or `my modeling`) |
| IS | 3–5 historical years + forecast, same tab |
| BS | Historical + forecast; must balance |
| CF | CFO + CFI + CFF = Δ cash; ending cash = BS cash |
| FCF | EBIT → NOPAT → +D&A −CapEx −ΔNWC = FCFF |
| Football field | Low / mid / high / weight / in-blend flag; blend formula |
| DCF | WACC build, PV, TV, equity bridge, if-converted `$/sh` |
| Comps | Peer inputs + formula multiples + quartile stats |
| Txns | Precedent table + applied `$/sh` |
| SOTP | Segment EVs + holdco + ND once |
| Replacement | Book / PPE / build stack |
| Sensitivity | Odd 5×5; **center = base** |
| Checks | TRUE/FALSE: BS, cash tie, S=U if LBO, blend weights = 100% of live bars |
| Sources | Form / date / accession |

Skip Yield tab if the method was skipped; note it on Cover.

## Conventions (`valuation-conventions`)

- Blue `#0000FF` inputs, black formulas, purple same-tab, green cross-sheet.
- Comment on every blue cell when written.
- Units row on every tab (USD millions unless said).
- Center sensitivity cell fill `#BDD7EE`, bold.
- Named ranges: `PT_Central`, `ValueShares`, `LastPrice`, `WACC`, `NetDebt`, each method mid.

## Formulas the field tab must have

```
central = SUMPRODUCT(weights, mids) / SUM(weights_of_in_blend)
```

Circular bars: `InBlend = FALSE`. Weights of live bars sum to 1.

DCF `$/sh` on Cover **links** to the if-converted cell, not a paste of studio markdown.

## Recalc / audit

If you have a recalc helper, run it. Else openpyxl-write formulas and document that Sheets will calculate on open. Then run `research-auditor` hunt item 4 on the blend and EV bridge.

Checks tab failures block publish.

## Do not

- Hardcode the blend or `$/sh` in Python and paste values.
- Call this the research canvas (that is a different skill).
