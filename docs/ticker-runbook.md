# Ticker runbook

You type a ticker. The plugin runs this. Same path for IREN, NVDA, or the next name.

**Command:** `/analyze-company TICKER`  
**Chat:** `analyze TICKER end-to-end`  
**Fast:** `/analyze-lite TICKER`

Orchestrator skill: `skills/full-company-analysis/SKILL.md`.

## Before you start

```bash
echo "$EDGAR_IDENTITY"          # must be "Name email@domain.com"
python3 -c "import edgar"
```

If either fails, stop. `pip3 install -r scripts/requirements.txt`. Pin `hishel==0.1.3` if FileStorage breaks.

## End-to-end

```
0   Env
1   edgar_pull.py → intake + 01-sec
2   Normalize IS/BS/CF + FCFF bridge
3   DCF, trading comps
    LBO lite (skip on lite mode)
    SOTP if multi-segment
    Competitive, unit econ, scenarios, catalysts
    Studio risk-audit
4   Dilution lock (value_shares)
    Transaction comps, replacement, yield (or skip with why)
    Football field + blend + rating
5   Official docs/{ticker}-equity-research.md
6   House auditor (UNVERIFIED). Halt on FAIL
7   Earnings calls companion (full mode; does not change the rating)
8   Sheets workbook → Drive  (PENDING is OK)
9   PPTX → Google Slides     (PENDING is OK)
10  Canvas / X               optional, never block
```

**The official memo is done at step 6.** Steps 8–10 are publish surfaces. Do not hold the rating hostage to Drive or a canvas share URL.

## What to type vs what not to do

| Do | Don't |
|---|---|
| `analyze NVDA end-to-end` | Paste IREN’s field into NVDA |
| `/analyze-lite AAPL` for a same-day look | Wait on X enrollment |
| One agent, update RUNLOG | Spawn a worker per skill |
| Skip replacement on pure software | Invent EV/EBITDA when debt is a DATA_GAP |
| Skip yield if DPS=0 and RI reprints book | Courtesy Hold when tape is above every live bar |

## Issuer cheat sheet

| You have | Run |
|---|---|
| US 10-K filer | Full or lite |
| FPI (20-F / 6-K) | Full; earnings on 6-K |
| Two+ real segments | SOTP required |
| Bank / insurer | Flag; do not ship a fake FCFF as sufficient |
| No CIK | Stop. `UNRESOLVED` |

## Outputs that mean “done”

1. `docs/{ticker-lower}-equity-research.md` — Buy/Hold/Sell, range, central, field, pillars, kills
2. `artifacts/{TICKER}/RUNLOG.md` — every phase checked
3. Dilution table and one `value_shares` on every bar
4. Auditor `PASS` or `PASS_WITH_FIXES` (or user override of `FAIL`)
5. Sheets / Slides URLs **or** `PENDING` with the reason

## Why the IREN test took forever

We built fifteen studio skills and a house overlay **while** covering the name, then farmed deck, Sheets, eight earnings calls, and a canvas to separate cloud agents. Drive rejected a large PPTX; canvas Publish is a human toolbar click; X was not enrolled. None of that is required to lock a rating.

Next name: one session, this runbook, memo first.
