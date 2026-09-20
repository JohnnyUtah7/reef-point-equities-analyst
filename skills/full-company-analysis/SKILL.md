---
name: full-company-analysis
description: >
  Studio engine for one ticker: intake → SEC → statements → dilution → DCF →
  comps → LBO (lite) → SOTP → competitive → unit economics → scenarios →
  catalysts → risk audit → draft memo. User-facing end-to-end trigger is
  portfolio-research ("analyze TICKER"). Use this skill when asked for the
  studio pack only, or as the engine inside portfolio-research.
version: "1.2.0"
---

# Full Company Analysis — Orchestrator

<!-- Chains all Equity Research Studio skills. Personas: Research Lead agent. -->

## Mission
From a simple prompt with a ticker/name, produce:
1. Research memo at **`artifacts/{TICKER}/04-research/memo.md`** (full body — official)
2. Model pack under `03-models/`
3. Google Slides-ready deck: **`05-deck/slide.md`** required; PPTX/Slides link under `05-deck/` if produced

## Hard rules (inherit global rules)
- Never skip SEC pull to "save time" with memorized numbers.
- On `DATA_GAP` or EDGAR failure: record in RUNLOG, continue only sections that do not depend on missing data, and surface gaps on memo cover.
- Risk audit runs **before** final memo polish and **before** slides render.
- Demo mode: if user says `quick` / `lite`, skip LBO + SOTP unless multi-segment; still do SEC → DCF → comps → memo → slides.
- **Path discipline:** Official memo = `04-research/memo.md` with full content. House/docs copies are copies only — acceptance still requires the studio path. Deck must leave `05-deck/slide.md`; empty `05-deck/` → slides-deck incomplete.
- **Dilution:** If convertibles/ATM/options exist, run `dilution-if-converted` (or equivalent section) before per-share valuation; show basic vs fully diluted.
- **ARR / mix / TV:** Enforce non-GAAP ARR labels, mix-transition callouts, and TV as % of EV (see hard rules).

## Trigger parsing
| User says | Action |
|-----------|--------|
| analyze {TICKER} / end-to-end | Hand off to `portfolio-research` (this skill is the engine) |
| studio pack / full-company-analysis only | Steps 1–13 here |
| quick look at {TICKER} | Lite pipeline, then still hand field/memo to `portfolio-research` if they asked for a rating |
| just DCF for {TICKER} | Hand off to `dcf-model` only |
| slides for {TICKER} | Hand off to `pptx-to-google-slides` |

## Pipeline order
```
1.  company-intake
2.  sec-filings
3.  financial-statements
3b. dilution-if-converted   # when converts/ATM/options/RSUs disclosed or suspected
4.  dcf-model
5.  comps-valuation
6.  lbo-model          # lite teaching case unless user wants full PE
7.  sotp-valuation     # skip with note if single-segment
8.  competitive-analysis
9.  unit-economics
10. scenario-sensitivity
11. catalyst-calendar
12. risk-audit         # gate
13. equity-research-memo
14. slides-deck          # NOTES ONLY — official deck is pptx-to-google-slides
```

When the user said `analyze TICKER` / end-to-end, **hand off to `portfolio-research`** after step 13 (or instead of running this file as the top orchestrator). `portfolio-research` adds dilution/field/Sheets/official PPTX and a required Buy/Hold/Sell.

Update `artifacts/{TICKER}/RUNLOG.md` after **each** step:
```
## RUNLOG
- [x] intake 2026-09-20T...
- [ ] sec-filings
...
```

## Agent routing (optional parallelism)
After statements exist, Research Lead may dispatch in parallel:
- Financial Modeler → DCF, LBO, SOTP (+ dilution extract)
- Comps Analyst → comps
- Competitive Intel → competitive + unit economics
Then join → scenarios → Risk Auditor → Equity Strategist (memo) → Deck Producer.

## Acceptance checklist
- [ ] `00-intake.md` has CIK or explicit UNRESOLVED
- [ ] SEC artifacts cite form/date
- [ ] If converts/ATM/options: basic **and** fully diluted share counts shown; per-share values labeled; if-converted `DATA_GAP` flagged (no undiluted-as-the-value)
- [ ] ARR / contracted ARR / operating ARR labeled **non-GAAP operating metric**; ARR multiples disclose tape-implied/circular if applicable
- [ ] Mix transition callout if LTM mix ≠ forward thesis (no unlabeled pure-AI multiples on BTC-heavy LTM, etc.)
- [ ] DCF assumptions listed; sensitivity center = base; **TV as % of EV** stated
- [ ] Comps peer rationale present
- [ ] `04-research/memo.md` exists with **full memo body** (≥ ~30 lines substantive; not pointer-only). Optional house/docs copy does not satisfy this gate.
- [ ] Memo has pillars + kill criteria + disclaimer + dilution/ARR/mix callouts as applicable
- [ ] Risk audit verdict not FAIL (or FAIL acknowledged by user); includes re-derive sample table
- [ ] `05-deck/slide.md` exists; `05-deck/` not empty; PPTX/Slides path recorded in RUNLOG/`deck_link.txt` if produced
- [ ] RUNLOG did **not** mark memo/slides complete without the path gates above

## Outputs (final)
```
artifacts/{TICKER}/RUNLOG.md
artifacts/{TICKER}/04-research/memo.md      # official full memo
artifacts/{TICKER}/05-deck/slide.md         # required
artifacts/{TICKER}/05-deck/deck_link.txt     # URL or path
artifacts/{TICKER}/05-deck/deck.pptx         # optional
```

## One-liner demo
User: `Analyze AAPL end-to-end`
You: run this skill with TICKER=AAPL; announce each phase briefly; deliver memo path + deck path at end.
