---
name: equity-research-memo
description: >
  Write a thesis-first equity research memo: direction, 2–4 pillars with
  mechanisms and kill criteria, risks, valuation summary, and what would change
  my mind. Use after models exist, or when user asks for a pitch / initiation /
  investment memo on a ticker.
version: "1.1.0"
---

# Equity Research Memo

<!-- Provenance: equity-research-skill (GeniusTrader) thesis pillars + kill
     criteria; Anthropic initiating-coverage report structure (simplified) -->

## Hard rules
- Skill structures evidence; **user owns direction** if they state one. If user
  asks you to propose a view, label it `Draft view — not advice` and show falsifiers.
- Every quantitative claim cites `01-sec/` or `03-models/` artifacts.
- Pillars must be falsifiable (kill criteria).
- **Official path (acceptance):** Write the **full memo body** to
  `artifacts/{TICKER}/04-research/memo.md`. A house/docs copy elsewhere is optional
  and is a *copy* only — studio acceptance still requires `04-research/memo.md`
  with full content (not a pointer stub; ≥ ~30 lines of substantive body).
- **Dilution:** Valuation section must show basic vs fully diluted $/sh when
  convertibles/ATM/options exist; state which share count. If if-converted shares
  are `DATA_GAP`, say so — do not present undiluted $/sh as “the” value.
- **ARR / non-GAAP:** Any ARR / contracted ARR / operating ARR must be labeled
  **non-GAAP operating metric**; never juxtapose with GAAP revenue without the label.
  If SOTP used an ARR multiple that is tape-implied/circular, disclose that.
- **Mix transition:** If LTM revenue mix differs materially from the forward thesis
  (e.g. BTC → AI), include an explicit **mix transition** callout; do not imply
  pure forward-segment multiples apply cleanly to LTM without labeling.

## Memo structure (target 6–12 pages md)
1. **Cover / one-pager** — Ticker, price/as-of, draft rating, 3-bullet thesis, valuation range (basic + FD if applicable), disclaimer.
2. **Business** — What they sell, who pays, unit of value (from intake + 10-K Item 1); **mix transition** callout if LTM ≠ forward mix.
3. **Industry / competition** — Link to `competitive-analysis` output.
4. **Thesis pillars (2–4)** — Each with: claim / driver / mechanism / magnitude / timeframe / **kill criterion**.
5. **Variant perception** — What you think the market underweights (labeled judgment).
6. **Financials snapshot** — From normalized statements; GAAP revenue vs any non-GAAP ARR clearly labeled.
7. **Valuation** — DCF + comps (+ SOTP/LBO if run); triangulation table; basic vs FD $/sh; TV as % of EV from DCF.
8. **Dilution / capital structure** — Converts, ATM, options; cite `dilution-if-converted` artifact when present.
9. **Risks & accounting flags** — From `risk-audit`.
10. **Catalysts** — From `catalyst-calendar`.
11. **What would change my mind** — Explicit.
12. **Appendix** — Sources index (form/date/accession).

## Outputs
```
artifacts/{TICKER}/04-research/memo.md    # OFFICIAL — full body required
```

Optional: copy to a house/docs path **after** writing the official file; never replace the official path with a pointer.

## RUNLOG gate
Do **not** mark this skill complete in RUNLOG if `04-research/memo.md` is missing,
pointer-only, or under ~30 lines of body.

## Anti-patterns
- Vague pillars ("strong brand") without mechanism/magnitude
- Rating without valuation support
- Copying bullish sell-side language without primary cites
- Pointer-only memo.md / writing the real memo only under docs/
- Undiluted $/sh presented as the sole equity value when converts exist
- ARR shown next to GAAP revenue without non-GAAP label
