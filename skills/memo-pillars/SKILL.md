---
name: memo-pillars
description: >
  Pillar / kill memo shape for the official Reef Point note. Overlays studio
  equity-research-memo. Rate after the football field, not before the model.
  Triggers: thesis pillars, kill criteria, what would change my mind, steel-man.
---

# Memo pillars

Studio memo is thesis-first but thin. Official note follows this shape. **Do not commit direction before the model.** Rate **after** the football field.

## Vocabulary

| Word | Meaning |
|---|---|
| Direction | Buy / Hold / Sell |
| Thesis | Direction **plus** the pillars |
| Pillar | One testable argument — all five elements required |
| Killing condition | Pre-specified observable that falsifies a pillar |

Never call the rating alone “the thesis.”

## Pillar (all five, or rewrite)

| Element | What |
|---|---|
| Claim | Differentiated view in one sentence |
| Driver | Which P&L / BS line (from the driver tree) |
| Mechanism | Causal story |
| Magnitude | Quantified, right unit, vs a stated baseline |
| Timeframe | Year or window |

Template: *“[Driver] will [direction] [magnitude] by [date] because [mechanism], driving [P&L impact].”*

Bad: “Strong brand / AI tailwind.” No driver, no magnitude, no kill.

**2–4 pillars.** Distinct drivers. Flag if the edge vs Street **or** vs bear is < ~10% of spot. Magnitudes in the memo are structuring tools. Studio / Sheets **re-derive** the model inputs. If they disagree, that is an audit surprise — do not silently align.

## Killing conditions (sacred)

2–3 per pillar. Specific, observable, forward-looking, tied to the mechanism.

```
KC{n} — short label (Pillar P{n})
- Trigger: number or event checkable in a public source
- What it kills: P{n}; JOINT P{m} if the same trigger breaks another
- Cadence: every earnings / monthly / on event
- Source for monitoring: 10-Q line, 8-K, transcript, docket
- Why this falsifies: ≤30 words
```

IDs never renumber. Dropped IDs retire. **Verbatim** into “What would change my mind” — do not paraphrase.

Calibrate so the **base case does not trip** the KC. If base already crosses the threshold, the KC is mis-set.

A pillar with no accepted kill is dropped.

## Steel-man (risks)

2–3 **strongest** counters. Not a parallel thesis.

Each: claim (strongest bear) → mechanism (which pillar it hits) → **why we reject** (≤3 cited bullets).

Unacceptable rejections: “management says no,” “hasn’t happened yet,” “Street isn’t worried.”

## Citation forms (every number)

- `[source, p.N]` — opened this session
- `[source]` — substance verified, page not opened
- `[est, not disclosed]` or `DATA_GAP` — not a fact
- `[computed from X, Y]` — derived

No orphan numbers. Modeling vs sourced must be visually distinct (“my modeling: …”).

## Official memo map

`docs/{ticker-lower}-equity-research.md` when `docs/` exists; else `artifacts/{TICKER}/04-research/memo.md`.

1. Exec table: **Buy / Hold / Sell**, range, central, last, dilution, EV bridge, three bullets, key risk. `Draft view — not investment advice.`
2. Business (cited)
3. Pillars + variant perception
4. Three statements
5. Football field + one subsection per method
6. Risks = steel-man + numbered kill flags
7. Catalysts (sourced or `ESTIMATED`)
8. What would change my mind = KC list verbatim
9. Sources index (form / date / accession)
10. Audit-pass log

User-stated direction wins. If they do not state one, the field sets it (`football-field`).

## Rejected

- Commit long/short **before** the model
- Mandatory Q&A pause between phases
- Wait-forever CapIQ
- Cover “conviction” line
