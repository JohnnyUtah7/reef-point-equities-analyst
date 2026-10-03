---
name: full-company-analysis
description: >
  Reef Point product orchestrator. Analyze ANY listed ticker end-to-end:
  EDGAR → statements → models → dilution → football field → official memo →
  auditor → earnings calls → the HTML research site → Sheets → PPTX/Slides.
  Triggers: analyze TICKER, value TICKER, pick a stock, check out NVDA,
  full analysis of MSFT, /analyze-company.
---

# Full company analysis

This is the **team product**. One ticker in. Official note, field, and the HTML research site out. Workbook and deck follow. The site is the thing you hand the user. Do not ask them for a URL.

Do not copy another name’s shares, ARR, WACC, or rating. Do not rewrite a locked official note.

Hard constraints: **no Zapier**. **no parallel SEC/DCF stack**. **no waiting on X**. **no invented filing numbers**. **no CosmosGolf / foreign checkout dirt**.

## Who this works for

| Issuer | Path |
|---|---|
| US 10-K / 10-Q filer | Full |
| FPI (20-F / 40-F / 6-K) | Full, with FPI rules in `sec-filings` and `earnings-call-analysis` |
| Multi-segment | Full + SOTP required |
| Asset-light software | Skip `replacement-build` with why |
| No dividend / negative RI | Skip `yield-residual` with why |
| Bank / insurer | Flag specialized model; do **not** pretend FCFF is enough; skip yield engine |
| Private / no EDGAR CIK | Stop at intake `UNRESOLVED` |
| Non-US only, no SEC file | Stop. Do not scrape a random IR PDF and call it a 10-K |

Lite (`/analyze-lite`, `quick look`): skip LBO + SOTP (unless 2+ reportable segments) + earnings calls + the Cursor `.canvas.tsx`. Still write the HTML site. Still do SEC → DCF → comps → dilution → field → official memo → Sheets → PPTX.

## 0. Env (stop if fail)

```bash
echo "$EDGAR_IDENTITY"
python3 -c "import edgar, importlib.metadata as m; print(m.version('edgartools'))"
```

Need `EDGAR_IDENTITY="Name email@domain.com"` and `import edgar`. Else:

```bash
pip3 install -r scripts/requirements.txt
# if FileStorage / hishel blows up:
pip3 install 'hishel==0.1.3'
```

Never WebFetch `sec.gov`. Prefer `python3 scripts/edgar_pull.py {TICKER}`.

## Artifact contract

```
artifacts/{TICKER}/
  RUNLOG.md
  00-intake.md
  01-sec/          company_meta.json filings_index.json financials.json notes.md
  02-statements/   normalized_is_bs_cf.md fcf_bridge.md
  03-models/       dcf.md comps.md lbo.md sotp.md sensitivity.md
                   txns.md replacement.md yield.md
  04-research/     competitive.md unit_economics.md catalysts.md
                   risk_audit.md hub_audit.md memo.md   # memo.md points at official
docs/{ticker-lower}-equity-research.md      # OFFICIAL
docs/{ticker-lower}-earnings-calls.md       # companion, no rating change
docs/{ticker-lower}-model.xlsx
docs/{ticker-lower}-valuation.pptx
```

Update `RUNLOG.md` after **each** phase. Reuse `01-sec/` if the latest 10-K/10-Q/20-F is already there.

## Pipeline (do not reorder 1–7)

```
0  Env
1  company-intake → sec-filings          (script first)
2  financial-statements
3  valuation-conventions while modeling
   dcf-model → comps-valuation
   lbo-model (lite unless sponsor bid)
   sotp-valuation (required if multi-segment; else skip with why)
   competitive-analysis → unit-economics
   scenario-sensitivity → catalyst-calendar
   risk-audit
4  dilution-if-converted
   transaction-comps → replacement-build → yield-residual
   football-field                         (rating comes from here)
5  memo-pillars → official docs/{ticker}-equity-research.md
   equity-research-memo is a draft only; official file wins
6  research-auditor                      HALT on FAIL unless user overrides
7  earnings-call-analysis                companion; does not change the rating
8  sheets-workbook → Drive convert       (memo can ship before this)
9  pptx-to-google-slides → Drive convert (rebuild if rating moved)
10 research-canvas HTML                   REQUIRED — docs/{ticker-lower}-reef-point-live.html
    Cursor .canvas.tsx                   only if they asked for a Cursor canvas
11 X                                     only if enrolled — never block
```

Phases 8–9 and 11 **must not** block the official memo. Drive can fail; `PENDING` is allowed for Sheets and Slides. **Phase 10 is not optional.** After the memo and the field exist, write the HTML file before you finish. Do not ask for a site URL, a repository, or a ChatGPT Sites publish step. Do not stop after describing the page.

Calls (phase 7) may run in parallel with phase 4 once `01-sec/` exists.

## Parallel vs serial

| Must be serial | Can overlap |
|---|---|
| Env → intake → SEC → statements | — |
| DCF / comps / SOTP after statements | Comp intel, unit econ, catalysts after SEC |
| Dilution **before** any official `$/sh` | Earnings calls after SEC (not after the memo) |
| Field → official memo → auditor → HTML site | Sheets and PPTX after auditor, in parallel |
| — | Cursor `.canvas.tsx`, X |

Full mode on a new name is **one focused agent session**, not a week of fan-out. Do not spawn a worker per skill. One lead, tools, RUNLOG.

## Rating tightness

From `football-field`:

- Last **above the high of every non-circular bar** + a live kill → **Sell**
- Last inside the range, thesis intact → **Hold** (Buy only if field mid > last **and** next kill is not live)
- Last **below the low**, pillars intact → **Buy**

User-stated direction wins. Label `Draft view — not investment advice.`

## Acceptance

- [ ] `00-intake.md` has CIK or `UNRESOLVED`
- [ ] SEC figures cite form/date/accession
- [ ] Studio `risk-audit` and house `research-auditor` not `FAIL` (or user override)
- [ ] Dilution table; official `$/sh` on if-converted count
- [ ] Field with skip-reasons; circular bars out of the blend; weights published
- [ ] Exec: Buy/Hold/Sell + range + central; rating matches the field
- [ ] Pillars have claim/driver/mechanism/magnitude/timeframe/kill
- [ ] `docs/{ticker-lower}-equity-research.md` is official
- [ ] Sheets URL (MIME spreadsheet) — or `PENDING` with why (memo already shipped)
- [ ] Slides URL (MIME presentation) — or `PENDING` with why
- [ ] `docs/{ticker-lower}-reef-point-live.html` exists, opens, and the published call matches the memo
- [ ] Disclaimer; no Zapier

## Return

HTML site path · official memo path · earnings-call companion · Sheets URL or PENDING · Slides URL or PENDING · `artifacts/{TICKER}/` · open DATA_GAPs · UNVERIFIED list · rating + central PT.

## Proof (do not copy)

Do not vendor a company note in this plugin. Official call stays in the workspace `docs/` file. Do not rewrite a locked note from this skill.
