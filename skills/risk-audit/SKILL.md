---
name: risk-audit
description: >
  Adversarial audit of thesis and numbers: accounting red flags, thesis killers,
  fabricated/stale figure checks, dilution/ARR/mix/path gates, and internal
  contradictions. Use before final memo/deck delivery or when user asks to
  fact-check the analysis.
version: "1.1.0"
---

# Risk Audit

<!-- Provenance: analyst-kit research-auditor agent; equity-research-skill kill criteria;
     strengthened after mix-transition / circular-ARR / dilution path failures -->

## Hard rules
- Fresh skeptical pass — treat figures as guilty until traced to artifacts.
- Output findings ranked by severity; do not silently "fix" the memo.
- **FAIL or required-fix** if any of these publish gates trip:
  - Official memo missing / pointer-only / `<~30` lines at `04-research/memo.md`
  - `05-deck/` empty or missing `slide.md` while slides marked complete
  - Undiluted $/sh presented as “the” value when converts/ATM/options exist and FD is knowable or should be DATA_GAP
  - ARR juxtaposed with GAAP revenue without **non-GAAP operating metric** label
  - ARR multiple used in SOTP/comps without disclosing tape-implied/circular when that is the source
  - Pure forward-segment multiples applied to materially different LTM mix without **mix transition** callout
  - DCF missing **TV as % of EV**

## Hunt list (in order)
1. Fabricated / unsourced figures
2. Stale period / FY vs calendar mixups
3. Unit/scale/currency errors
4. Math re-derive (margins, multiples, DCF bridge) — **required sample table**
5. Dilution / fully diluted consistency
6. ARR / non-GAAP labeling
7. Mix transition vs comps/SOTP peer set
8. Path discipline (memo.md full body; 05-deck populated)
9. Accounting red flags (revenue recognition, rising receivables vs sales, CFO vs NI divergence, goodwill impairments, off-balance commitments)
10. Thesis killers vs stated kill criteria
11. Internal contradictions (summary vs tables)

## Re-derive sample table (required)
Pick ≥3 quantitative claims from memo/models and re-compute from primary artifacts:

| Claim (as stated) | Source artifact | Re-derived value | Match? |
|-------------------|-----------------|------------------|--------|
| e.g. EV/ARR | sotp.md + filings | … | Y/N |
| e.g. $/sh FD | dcf.md + dilution | … | Y/N |
| e.g. TV % of EV | dcf.md | … | Y/N |

Do not skip this table — path/dilution/ARR audits failed when it was absent.

## Output format
```markdown
# Risk audit — {TICKER}
## Verdict: PASS | PASS_WITH_FIXES | FAIL
## Critical findings
## High
## Medium
## Gate checklist
- [ ] memo.md full body at 04-research/
- [ ] 05-deck/slide.md present (if deck claimed)
- [ ] basic vs FD $/sh (or DATA_GAP)
- [ ] ARR labeled non-GAAP; circular multiples disclosed
- [ ] mix transition callout if LTM ≠ forward
- [ ] TV as % of EV in DCF
## Trace sample (re-derive table)
## Required fixes before publish
```

## Outputs
```
artifacts/{TICKER}/04-research/risk_audit.md
```
