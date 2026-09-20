---
name: earnings-call-analysis
description: >
  Reef Point hub overlay. Pull ~2 years of quarterly earnings calls
  (prepared remarks + sell-side Q&A), build a promise-vs-delivery ledger,
  map management vernacular, score credibility tells with confidence
  labels, and write a companion memo section plus canvas-tab / one-slide
  copy. Triggers: earnings calls, transcripts, management credibility,
  "how they talk", IREN calls. Does not change the official rating.
---

# Earnings-call analysis (hub overlay)

Companion to the official note. **Not** a second SEC/DCF stack. Call studio `sec-filings` for 8-K / 6-K exhibits. **Do not** rewrite `docs/{ticker}-equity-research.md` rating or the football field.

IREN is the worked example only. Do not copy its rating.

Hard constraints: **no Zapier**. **no waiting on X**. **do not dirty CosmosGolf or any git checkout**. **never invent quotes**.

## Hard rules

1. **Never invent a quote, speaker, questioner, or filing number.** If the transcript is missing, write `DATA_GAP` and stop that claim.
2. Every excerpt cites **call date, speaker, role**. Q&A excerpts also cite **questioner + firm**.
3. Official numbers come from the **8-K / 6-K / 10-Q / 10-K**, not from a transcript vendor. If they disagree, keep the filing and flag the transcript as a vendor error.
4. **ARR, run-rate, “annualized,” GPU counts, and MW** are operating metrics unless the filing says GAAP. Label them.
5. **“Lying” is never a fact.** It is an analytic claim only, and only with a **HIGH / MED / LOW** confidence tag plus the two quotes that create the tension. Default verb: recast, hedge, walk, metric-shift.
6. Sentiment and the talk-read are **delivery analysis**, not a Buy/Hold/Sell input. The field still rates the name.
7. Cover **~8 quarterly calls if ~2 years exist**. Prepared remarks **and** sell-side Q&A. Skip a fireside unless the user asks.
8. Short excerpts only. Do not paste a vendor transcript into the store.

## 0. Env

```bash
echo "$EDGAR_IDENTITY"
python3 -c "import edgar; import importlib.metadata as m; print(m.version('edgartools'))"
```

Need `EDGAR_IDENTITY="Name email@domain.com"` and `import edgar`. Else stop. Pin `hishel==0.1.3` if FileStorage breaks. Prefer `scripts/edgar_pull.py`. Never bare-fetch `sec.gov`.

## 1. Sources (in this order)

| Priority | Where | Use for |
|---|---|---|
| 1 | Studio `sec-filings` + edgartools | 8-K Item 2.02 exhibits (press + **transcript if furnished**). FPI era: **6-K** earnings packs, not 8-K. |
| 2 | Company IR events page | Call date, deck, webcast. IR often has **no** text transcript. |
| 3 | Third-party transcript (Quartr / StockAnalysis / SA) | Prepared + Q&A when EDGAR has no EX-99 transcript. **Name the vendor.** |
| 4 | Official note + `artifacts/{TICKER}/01-sec/` | Cross-check figures. Do not re-pull a DCF. |

**FPI check (coverage audit):** If the issuer was a foreign private issuer for part of the window, earnings live on **6-K**, not 8-K. IREN: 6-K through May 2025; 8-K Item 2.02 from FY25 year-end.

Index every call before writing:

```
Call | Fiscal label | Calendar date | Period end | EDGAR form/acc/exhibit | IR URL | Transcript vendor | Q&A? |
```

If Q&A is missing → `DATA_GAP` on Q&A, still run prepared remarks.

## 2. Window

Default: last **eight** quarterly results calls (~2 fiscal years). Label **FY vs calendar** on every date (IREN FYE 30 Jun). Do not mix “Q2” without saying whose Q2.

Roster the desk each call: CEO / CFO / CCO / IR. Note replacements (IREN: Lincoln Tan → Mike Power; Belinda Nucifora → Anthony Lewis).

## 3. Promise ledger

Build a table **before** the narrative. One row per load-bearing promise.

```
ID | Promise (verbatim short) | First said (date, speaker) | Restated / recast | Check date | Outcome | Metric definition
```

Outcomes: `HIT` · `MISS` · `PARTIAL` · `OPEN` (not yet due) · `ABANDONED` · `DATA_GAP`.

**Definition check (coverage + overclaim):** before calling a recast a miss, ask whether the unit changed.

- IT MW vs gross MW vs “AI Cloud capacity”
- GPU count vs ARR vs GAAP revenue
- Contracted ARR vs operating ARR vs recognized revenue
- Construction complete vs customer **acceptance** / handoff
- “On schedule for this year” vs a named quarter

A 480 MW “AI Cloud” target and a 300 MW “IT load” target may be the same stack or not. If you cannot prove the identity, `DATA_GAP` — do not write “they cut guidance.”

## 4. Delivery vs prior promises

For each live ID: what they said they would grow, what grew.

- Prefer filing numbers for the check.
- Say whether growth is **contracted**, **operating**, or **GAAP**.
- Back-end ramps: write the company’s own lag language (e.g. capacity late in the quarter → revenue next quarter).

## 5. Vernacular

10–20 house phrases. Quote once, cite, then say what the phrase is **for** (moat story, scarcity, capital flywheel, optionality). Track which phrases survive a strategy change (IREN: “ones and zeros,” “time-to-compute,” founding digital/physical gap).

## 6. Credibility tells

Hunt list (do not need all):

| Tell | What to look for |
|---|---|
| Hedge | “may,” “potentially,” “we reserve the right,” then a hard number in the same breath |
| Recast | Same object, new date / new unit / new inclusion rule |
| Metric shopping | Scoreboard moves from hash-rate → ARR → $/MW → “funding flywheel” when the old metric stalls |
| Walk | A named program (distributions, 50 EH, colo-first Childress) quietly dropped |
| Track-record claim | “We have never missed a date” vs a later slip — quote both |
| Vendor error | Transcript number that the 8-K contradicts |

Each tell: **two cites + confidence**.

```
TELL: …
CONFIDENCE: HIGH | MED | LOW
WHY: one line
NOT: lying-as-fact
```

`HIGH` = same object, same unit, dated quotes. `MED` = definition might have moved. `LOW` = one source or vendor-only.

## 7. Sentiment + talk-read

Two short blocks.

**Sentiment (what they sold that day):** mining cash-flow / pivot / victory-lap / transition-pain / sold-out platform. One line per call.

**Talk-read (how they will talk next, not a price):** which scoreboard they will defend, which miss they will not volunteer, which hedge they will reuse. Label `judgment`. Not a catalyst calendar — studio already has that.

## 8. What was said vs how it was delivered

Per regular speaker (not the operator):

| Speaker | Said (content) | How (delivery) |
|---|---|---|
| CEO | … | founding myth, sports analogy, certainty after hedge |
| CFO | … | ranges, “circa,” capex caveats |
| CCO | … | demand/scarcity, “happy to take that” |
| IR | … | roster only unless they answer |

Q&A: name the **repeat questioners**. What they keep asking is the Street’s kill list.

## 9. Outputs

Write **one** companion: `docs/{ticker-lower}-earnings-calls.md`.

Required sections, in order:

1. Banner: official rating **unchanged**; link the note.
2. Call index (table in §1).
3. Promise ledger.
4. Delivery vs promises.
5. Vernacular.
6. Credibility tells (confidence).
7. Sentiment + talk-read.
8. Said vs delivered.
9. **Memo section** — paste-ready for the official note. Does **not** change Buy/Hold/Sell, PT, or pillars. Max ~1 page.
10. **Canvas tab copy** — one tab, tables, takeaway line, `Not investment advice.`
11. **Deck slide stub** — takeaway + 4–6 rows. Deck worker builds the slide later.
12. `DATA_GAP` list.
13. Sources (form / date / accession / vendor).

Do **not** edit the official note unless the user says to paste the memo section in.

## Do not

- Invent quotes or “remembered” Q&A.
- Dump a Quartr/SA transcript into the store.
- Treat ARR as GAAP.
- Call a definition change a lie.
- Change the official rating or field.
- Stand up a parallel EDGAR/DCF pipeline.
- Wait on X. Use Zapier. Touch CosmosGolf.

## Return

Companion path · call count · HIT/MISS/OPEN/PARTIAL/ABANDONED counts · open `DATA_GAP`s · whether a filed transcript existed · rating unchanged.
