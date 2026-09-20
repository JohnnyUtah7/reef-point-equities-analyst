---
name: transaction-comps
description: >
  Precedent / transaction comps bar for the football field. Studio has trading
  comps only. Triggers: precedent transactions, deal comps, M&A multiples,
  control premium, failed deal haircut.
---

# Transaction comps

Studio trading comps do **not** own this bar. Distilled from Anthropic initiating-coverage precedent process. House adds failed-close haircuts and no paper-pipeline rule.

## Universe

- Same or adjacent industry; size **0.5×–2×** target (or state why not).
- Prefer last **3–5 years**. Weight recent higher.
- **Announced and closed** first. Withdrawn / terminated stay in the table with a **haircut** — do not treat the signed mark as a print.
- 5–10 deals if they exist; fewer is fine if you say so. **Do not invent multiples.**

## Sources (priority)

1. Target/acquirer **8-K, S-4, proxy** (offer price, exchange ratio, EV, close/terminate).
2. Studio `01-sec/` if the target is the subject.
3. Dated press / IR only if the filing is missing — label lower confidence.
4. CapIQ / FactSet if a data tool is actually connected. Never wait on one.

If a multiple cannot be sourced: `[UNSOURCED]` and exclude from the median.

## Spread

| Column | Required |
|---|---|
| Announce / close (or terminate) dates | Yes |
| Target / acquirer | Yes |
| Equity value and EV | Yes — show both |
| Structure (cash / stock / mix) | Yes |
| Target LTM revenue / EBITDA at announce | If disclosed |
| EV / Rev, EV / EBITDA | If denominator exists; else NM |
| Control premium vs unaffected price (1–2 days pre-announce) | If public target |
| Status | Closed / pending / **terminated** |
| Rationale (one line) | Yes |

```
Transaction EV = equity offer + assumed net debt − cash acquired
Premium        = (offer − unaffected) / unaffected
```

Typical control premium **20–40%**. Strategic + synergy deals sit above financial sponsors. Treat that band as context, not a hardcoded input.

## Apply to the name

Pick **one** physical metric that matches the comps (EBITDA, MW, rooms, subscribers). Apply the median (and 25th / 75th) to **in-existence or in-build** capacity only.

```
implied_equity = (metric × multiple) − net_debt   # if the multiple is EV
$/sh           = implied_equity / value_shares    # same count as the field
```

**Vetoes**

- Do not put **paper pipeline** capacity on a live-asset multiple.
- Failed close: use the signed metric as a **low/mid** only after an explicit haircut.
- Transition-year EBITDA (loss / wind-down) → NM. A *forward* analog belongs in the high with a flag, not the mid.
- Do not silently mix equity value / unit with EV / unit.

## Output

`artifacts/{TICKER}/03-models/txns.md` (and the `Txns` tab in the Sheets workbook). Field row: low / mid / high / skip-reason.

## Do not

- Do not vendor a deal database.
- Do not build a second trading-comps stack (`comps-valuation` owns that).
- Do not use merger accretion/dilution as this bar — that is acquirer EPS, not a target football-field method.
