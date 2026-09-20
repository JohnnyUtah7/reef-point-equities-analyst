# Reef Point Equity Research

Cursor plugin. **One ticker in. Official memo, football field, Sheets, and deck out.**

IREN was the first live test. This pack is the product you install and share — not a second IREN write-up.

```
/analyze-company NVDA
```

or, in chat: `analyze NVDA end-to-end`

## What you get

| Layer | What it does |
|---|---|
| EDGAR | `scripts/edgar_pull.py` → `artifacts/{TICKER}/01-sec/` |
| Models | Statements, DCF, trading comps, LBO (lite), SOTP |
| House overlay | Dilution, transaction comps, replacement, yield, football field |
| Publish | Official note, auditor, earnings-call companion, Sheets, PPTX → Google Slides |

Rating is **Buy / Hold / Sell after the field**. Cover-share `$/sh` is not official. Circular own-ARR bars draw and get **weight 0**.

## Any ticker?

**Yes, if they file with the SEC** (10-K/10-Q or 20-F/6-K). Same skills, same folders, ticker in the path.

| Works | Does not |
|---|---|
| US listed, FPI, multi-segment | Private companies, no CIK |
| Asset-heavy or asset-light (skip rules) | Non-US only with no SEC file |
| Lite mode for a fast look | Banks/insurers as a full bank model (flagged, not faked) |

Do **not** copy IREN’s 423.80m shares, $4bn ARR, 11.7% WACC, or Sell $28 onto the next name.

## Install

See [INSTALL.md](./INSTALL.md). Short version:

```bash
git clone <this-repo>
ln -s "$(pwd)" ~/.cursor/plugins/local/reef-point-equity-research
export EDGAR_IDENTITY="Your Name you@company.com"   # ~/.zshrc
pip3 install -r scripts/requirements.txt
```

Reload Cursor. Settings → Cursor Settings → Plugins: confirm **reef-point-equity-research**.

## Commands

| Command | Mode |
|---|---|
| `/analyze-company TICKER` | Full |
| `/analyze-lite TICKER` | SEC → DCF → comps → field → memo → Sheets → PPTX |
| `/sec-pull TICKER` | Filings only |
| `/dcf TICKER` | Refresh DCF |
| `/slides TICKER` | Official 10-slide deck |

Runbook (same content as the orchestrator skill): [docs/ticker-runbook.md](./docs/ticker-runbook.md).

## IREN test (do not treat as current publish kit)

Proof note lives in the Investment Research project, not in this plugin. Local pointer: [examples/IREN/README.md](./examples/IREN/README.md).

The test was slow because we **built the stack while running the name**, then fan-out workers for deck/Sheets/canvas. The product path is **one agent, one RUNLOG**. Memo ships even if Drive convert is `PENDING`.

## Hard no

Zapier. Bare `sec.gov` fetch. Invented multiples. Courtesy Hold when the field is Sell. `gws` as the official deck.

**Draft view — not investment advice.**
