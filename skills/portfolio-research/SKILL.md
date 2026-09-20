---
name: portfolio-research
description: >
  Reef Point Equities orchestrator. Analyze one ticker end-to-end: run studio
  full-company-analysis for EDGAR/statements/models, then house overlays
  (dilution, field, txns, replacement, yield, auditor, memo pillars), Google
  Sheets, and PPTX→Google Slides. Triggers: "analyze TICKER", "analyze TICKER
  end-to-end", "check out NVDA", "full analysis of MSFT", "run the pipeline".
---

# Portfolio research

Hard constraints: **no Zapier**. **no parallel SEC/DCF stack** — call studio skills in this plugin. **no waiting on X / social**.

House look: [`../../references/house-style.md`](../../references/house-style.md)

## Overlay index (read these; do not guess)

| Step | Skill |
|---|---|
| Conventions | `valuation-conventions` |
| Dilution | `dilution-if-converted` |
| Txns | `transaction-comps` |
| Floor | `replacement-build` |
| Yield | `yield-residual` |
| Field | `football-field` |
| Memo shape | `memo-pillars` |
| Audit | `research-auditor` |
| Sheets | `sheets-workbook` |
| Deck | `pptx-to-google-slides` |
| Canvas | `research-canvas` (optional) |
| Calls | `earnings-call-analysis` (companion; no rating change) |

Do **not** treat any worked example in other files as a locked rating for a new name. If the workspace already has an official note for a ticker, **do not rewrite that rating** unless a new CRITICAL audit finding says so.

## 0. Env

```bash
echo "$EDGAR_IDENTITY"
python3 -c "import edgar; import importlib.metadata as m; print(m.version('edgartools'))"
```

Need `EDGAR_IDENTITY="Name email@domain.com"` and `import edgar`. Else stop and tell the operator to set identity (see `references/edgar-identity.md`).

If `import edgar` fails: `pip3 install edgartools`. **Pin `hishel==0.1.3`** if FileStorage breaks. Prefer `scripts/edgar_pull.py`. Never WebFetch sec.gov.

## 1. Studio 1–13, not official slides

Run `full-company-analysis` in this plugin (skip its step 14 `slides-deck` as official).

```
company-intake → sec-filings → financial-statements
→ dcf-model → comps-valuation → lbo-model (lite) → sotp-valuation
→ competitive-analysis → unit-economics → scenario-sensitivity
→ catalyst-calendar → risk-audit → equity-research-memo
```

Apply `valuation-conventions` **while** modeling (blue/black, odd grid, center = base, no invented multiples). Official deck is `pptx-to-google-slides`.

Reuse current `artifacts/{TICKER}/` if the latest 10-K/10-Q is already in `01-sec/`. Re-pull if not. Keep `RUNLOG.md` current after **each** phase.

Lite / `quick`: skip LBO + SOTP unless multi-segment. Still do SEC → DCF → comps → house overlay → memo → Sheets → PPTX.

8-K **EX-99.1 / EX-99.2** own non-GAAP KPIs (ARR, bookings). Label them. Foreign-private-issuer windows: earnings often live on **6-K**, not 8-K.

## 2. House overlay (this order)

1. **dilution-if-converted** — lock `value_shares`. Fix cover-share `$/sh`.
2. **transaction-comps** — precedents; failed closes haircut; no paper pipeline.
3. **replacement-build** — floor.
4. **yield-residual** — or skip with why.
5. **football-field** — six methods, circular weight 0, blend, rating tightness.
6. **memo-pillars** — official note. If the workspace has `docs/`, write `docs/{ticker-lower}-equity-research.md` and point `artifacts/{TICKER}/04-research/memo.md` at it **or** keep a full copy there. If no `docs/`, the studio memo path is official.
7. **research-auditor** — hunt list + UNVERIFIED. Do not publish on `FAIL` without user override.
8. **earnings-call-analysis** — companion only. **Do not** change the official rating or field.

Rating comes **from the field**, not from a pre-model direction commit.

## 3. Official memo

See `memo-pillars`. Exec table first. Disclaimer: not investment advice.

## 4. Sheets

Run `sheets-workbook`. Confirm spreadsheet MIME when Drive is connected.

## 5. Deck

Run `pptx-to-google-slides`. Master `assets/house-template.pptx`. Logo `assets/rpc-logo.png`. White cover. Football-field spine. Rec slide matches the memo.

## 6. Optional canvas

Only if asked. `research-canvas`. Not a substitute for memo / Sheets / deck.

## 7. Social / tape

Skip unless a tape source is actually connected. Never block the pipeline on it.

## Do not

- Zapier, Make, n8n, `gws`, Slides API authoring as official.
- A second EDGAR/DCF stack.
- Memorized SEC numbers.
- Publish on auditor `FAIL` without override.
- Rewrite a locked official note’s rating.

## Return

Official memo path · optional earnings-call path · Sheets URL · Slides URL · `artifacts/{TICKER}/` · open `DATA_GAP`s · UNVERIFIED list · rating + central PT.
