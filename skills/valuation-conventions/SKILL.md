---
name: valuation-conventions
description: >
  DCF / comps / LBO conventions applied on top of studio models. Not a second
  engine. Use when building or reviewing studio dcf/comps/lbo artifacts or the
  Sheets workbook.
---

# Valuation conventions

Studio **runs** `dcf-model`, `comps-valuation`, `lbo-model`. This file is the executable convention layer.

## Do not

- Do not fetch a second set of 10-K numbers. Use `02-statements/` + `01-sec/`.
- Do not switch to yfinance-first valuation.
- Do not restyle the published deck in IB navy (`#1F4E79`) or Times New Roman.

## Workbook law

| Font | Meaning |
|---|---|
| Blue `#0000FF` | Hardcoded input — only historicals, drivers, market data |
| Black | Formula (`=`, `SUM`, operators) |
| Purple `#800080` | Same-tab link, no calc (`=B9`) |
| Green `#008000` | Cross-sheet link (`=Assumptions!B5`) |

Every blue cell gets a comment **as it is written**: `Source: [form], [date], [accession or URL]`. No “TODO: source.”

No Python-computed values in calc cells. `ws["D20"] = "=D19*(1+$B$8)"` is correct.

Named ranges for any number that will appear on a slide. Checks tab: BS balances, CF cash = BS cash, Sources = Uses.

## DCF (studio still builds it)

```
FCFF = EBIT × (1 − t) + D&A − CapEx − ΔNWC
Ke   = rf + β × ERP          # + size premium only if labeled
Kd   = pre_tax_debt × (1 − t)
WACC = We×Ke + Wd×Kd
TV   = FCF_{n+1} / (WACC − g)     # g < WACC; g ≤ long-run GDP-ish
     or Year-N EBITDA × exit multiple
EV   = Σ PV(FCFF) + PV(TV)
Eq   = EV − net_debt − NCI + associates
```

- rf = **current** 10y UST, dated. Not a hardcoded default.
- β: label judgment vs raw. ERP 5.0–6.0% and labeled.
- Target capital structure if current is distorted; say so.
- Mid-year convention optional; if used, periods 0.5, 1.5, … and say so.
- Projection 5–10 years (longer runway → longer explicit).
- **TV sanity:** typically 50–70% of EV; **flag >75%** / discuss >80%.
- SBC: treat as **real cost** (do not add back unless you disclose a second case).
- Diluted / if-converted shares — `dilution-if-converted`, not cover-only.

**Sensitivity (non-negotiable)**

- Odd grid: **5×5** (or 7×7). Never 4×4.
- **Center cell = base** WACC and g (and the center output equals the model `$/sh`).
- Highlight the center (medium-blue fill is fine **inside the workbook**; not on the deck).
- Three tables if you have room: WACC×g, growth×margin, β×rf.
- Each cell is a **full** DCF formula, not a linear approximation.

Confirm after: raw inputs → revenue path → FCF → WACC → equity bridge → sensitivity. Do not dump a finished grid on an unconfirmed base year.

## Trading comps (studio still builds it)

Source hierarchy: configured institutional feed → SEC fundamentals → dated market quotes → web last, flagged.

- 6–12 peers. Inclusion / exclusion rationale.
- Blank or `NM` — never invent a multiple.
- Stats: min / 25th / **median** / 75th / max. Prefer median to mean.
- Label LTM vs NTM. Prefer NTM when estimates exist.
- Metric choice: EV/Rev (high growth / loss), EV/EBITDA (default), P/E (stable profitable), P/B (financials).
- Outliers: drop or footnote. Implied value = chosen multiple × target metric → equity bridge → `/ value_shares`.

## SOTP (studio still builds it)

Use when 2+ reportable segments in **different** industries. Skip single-segment (point at DCF/comps).

```
segment_EV_i = segment_EBITDA_i × peer_median_multiple_i
Gross EV     = Σ segment_EV − unallocated HQ (or 8× ongoing HQ cost)
Equity       = Gross EV − ND − NCI − prefs − pension gap + cash + non-core
             − synergy-destruction 5–15% if vertically coupled
             − tax leakage 10–20% if a spin is the thesis
$/sh         = Equity / value_shares
```

Net debt **once**. A sleeve that is just market EV / the company’s own ARR is **circular** — draw it, weight 0.

## LBO (lite unless sponsor bid)

Build in order; verify each: assumptions → **Sources = Uses** → operating → debt schedule → IRR / MOIC → sensitivity.

- Interest on **beginning** balance to break circ (or document iteration).
- Cash sweep respects tranche priority; balances `MAX(0, …)`.
- IRR signs: investment negative, exit positive.
- Odd entry×exit (or growth×exit) grid; center = base IRR/MOIC.
- On the football field **only** if a real sponsor bid is the question.

## Keep / reject

Keep: `[UNSOURCED]` rather than a guessed precedent multiple; field = min / median / max + last-print; every deck number traces to a named range / memo cell.

Reject: IB navy branding, CapIQ as a hard dependency, Office JS as the official authoring path, `gws` / Slides API as publish.
