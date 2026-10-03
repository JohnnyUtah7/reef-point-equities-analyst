# Ticker runbook

Type a ticker. The plugin runs this.

**Command:** `/analyze-company TICKER`  
**Chat:** `analyze TICKER`  
**Fast:** `/analyze-lite TICKER`

Orchestrator: `skills/portfolio-research/SKILL.md` → `skills/full-company-analysis/SKILL.md`.

## Before you start

```bash
echo "$EDGAR_IDENTITY"          # "Your Name you@email.com"
python3 -c "import edgar"
```

Stop if either fails. See [references/edgar-identity.md](../references/edgar-identity.md).

## End-to-end

```
0   Env
1   edgar_pull.py → intake + artifacts/{TICKER}/01-sec
2   Normalize IS/BS/CF + FCFF bridge
3   DCF, trading comps
    LBO lite (skip on lite)
    SOTP if multi-segment
    Competitive, unit econ, scenarios, catalysts
    risk-audit
4   Dilution lock (value_shares)
    Txns, replacement, yield (or skip with why)
    Football field + blend + rating
5   Official docs/{ticker}-equity-research.md
6   House auditor (UNVERIFIED). Halt on FAIL
7   Earnings calls companion (full; does not change the rating)
8   Sheets → Drive     PENDING is OK (local xlsx still written)
9   PPTX → Slides      PENDING is OK (local pptx still written)
10  Canvas / X         optional, never block
```

**The official memo is done at step 6.** Do not hold the rating for Drive or a canvas URL.

## Issuer cheat sheet

| You have | Run |
|---|---|
| US 10-K filer | Full or lite |
| FPI (20-F / 6-K) | Full; earnings on 6-K |
| Two+ real segments | SOTP required |
| Bank / insurer | Flag; do not ship fake FCFF as enough |
| No CIK | Stop. `UNRESOLVED` |

## Done means

1. `docs/{ticker-lower}-equity-research.md` — Buy/Hold/Sell, range, central, field, pillars, kills  
2. `artifacts/{TICKER}/RUNLOG.md`  
3. One `value_shares` on every bar  
4. Auditor `PASS` / `PASS_WITH_FIXES` (or override of `FAIL`)  
5. Sheets / Slides URLs **or** `PENDING`
