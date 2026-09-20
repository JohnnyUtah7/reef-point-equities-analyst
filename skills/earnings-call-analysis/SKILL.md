---
name: earnings-call-analysis
description: >
  Pull ~2 years of quarterly earnings calls (prepared remarks + sell-side Q&A),
  build a promise-vs-delivery ledger, map management vernacular, score
  credibility tells with confidence labels, and write a companion memo section.
  Triggers: earnings calls, transcripts, management credibility, "how they talk".
  Does not change the official rating.
---

# Earnings-call analysis

Companion to the official note. **Not** a second SEC/DCF stack. Call `sec-filings` for 8-K / 6-K exhibits. **Do not** rewrite the official rating or the football field.

Hard constraints: **no Zapier**. **never invent quotes**. **no waiting on social feeds**.

## Hard rules

1. **Never invent a quote, speaker, questioner, or filing number.** If the transcript is missing, write `DATA_GAP` and stop that claim.
2. Every excerpt cites **call date, speaker, role**. Q&A excerpts also cite **questioner + firm**.
3. Official numbers come from the **8-K / 6-K / 10-Q / 10-K**, not from a transcript vendor. If they disagree, keep the filing and flag the transcript as a vendor error.
4. **ARR, run-rate, “annualized,” unit counts** are operating metrics unless the filing says GAAP. Label them.
5. **“Lying” is never a fact.** It is an analytic claim only, and only with a **HIGH / MED / LOW** confidence tag plus the two quotes that create the tension. Default verb: recast, hedge, walk, metric-shift.
6. Sentiment and the talk-read are **delivery analysis**, not a Buy/Hold/Sell input. The field still rates the name.
7. Cover **~8 quarterly calls if ~2 years exist**. Prepared remarks **and** sell-side Q&A. Skip a fireside unless the user asks.
8. Short excerpts only. Do not paste a vendor transcript into the workspace.

## 0. Env

```bash
echo "$EDGAR_IDENTITY"
python3 -c "import edgar"
```

Need identity and `import edgar`. Else stop. Pin `hishel==0.1.3` if FileStorage breaks. Prefer `scripts/edgar_pull.py`. Never bare-fetch `sec.gov`.

## 1. Sources (in this order)

| Priority | Where | Use for |
|---|---|---|
| 1 | `sec-filings` + edgartools | 8-K Item 2.02 exhibits (press + **transcript if furnished**). FPI era: **6-K** earnings packs, not 8-K. |
| 2 | Company IR events page | Call date, deck, webcast. IR often has **no** text transcript. |
| 3 | Third-party transcript (named vendor) | Prepared + Q&A when EDGAR has no EX-99 transcript. **Name the vendor.** |
| 4 | Official note + `artifacts/{TICKER}/01-sec/` | Cross-check figures. Do not re-pull a DCF. |

**FPI check:** If the issuer was a foreign private issuer for part of the window, earnings live on **6-K**, not 8-K. Label FY vs calendar on every date.

Index every call before writing:

```
Call | Fiscal label | Calendar date | Period end | EDGAR form/acc/exhibit | IR URL | Transcript vendor | Q&A? |
```

If Q&A is missing → `DATA_GAP` on Q&A, still run prepared remarks.

## 2. Window

Default: last **eight** quarterly results calls (~2 fiscal years). Roster the desk each call: CEO / CFO / IR. Note replacements.

## 3. Promise ledger

Build a table **before** the narrative. One row per load-bearing promise.

```
ID | Promise (verbatim short) | First said (date, speaker) | Restated / recast | Check date | Outcome | Metric definition
```

Outcomes: `HIT` · `MISS` · `PARTIAL` · `OPEN` (not yet due) · `ABANDONED` · `DATA_GAP`.

**Definition check:** before calling a recast a miss, ask whether the unit changed (capacity vs recognized revenue, contracted vs operating ARR, construction complete vs customer acceptance). If you cannot prove identity, `DATA_GAP`.

## 4. Delivery vs prior promises

For each live ID: what they said they would grow, what grew. Prefer filing numbers. Say whether growth is **contracted**, **operating**, or **GAAP**.

## 5. Vernacular

10–20 house phrases. Quote once, cite, then say what the phrase is **for**.

## 6. Credibility tells

| Tell | What to look for |
|---|---|
| Hedge | Soft modal, then a hard number in the same breath |
| Recast | Same object, new date / new unit / new inclusion rule |
| Metric shopping | Scoreboard moves when the old metric stalls |
| Walk | A named program quietly dropped |
| Track-record claim | “We have never missed…” vs a later slip — quote both |
| Vendor error | Transcript number that the 8-K contradicts |

Each tell: **two cites + confidence**. `HIGH` = same object, same unit, dated quotes. `MED` = definition might have moved. `LOW` = one source or vendor-only.

```
TELL: …
CONFIDENCE: HIGH | MED | LOW
WHY: one line
NOT: lying-as-fact
```

## 7. Sentiment + talk-read

**Sentiment (what they sold that day):** one line per call.

**Talk-read (how they will talk next, not a price):** labeled `judgment`. Not a catalyst calendar — `catalyst-calendar` already owns that.

## 8. What was said vs how it was delivered

Per regular speaker. Q&A: name the **repeat questioners**.

## 9. Outputs

Write **one** companion: `docs/{ticker-lower}-earnings-calls.md` when `docs/` exists; else `artifacts/{TICKER}/04-research/earnings-calls.md`.

Required sections, in order:

1. Banner: official rating **unchanged**; link the note.
2. Call index.
3. Promise ledger.
4. Delivery vs promises.
5. Vernacular.
6. Credibility tells (confidence).
7. Sentiment + talk-read.
8. Said vs delivered.
9. **Memo section** — paste-ready. Does **not** change Buy/Hold/Sell, PT, or pillars. Max ~1 page.
10. **Canvas / deck stub** — takeaway + 4–6 rows.
11. `DATA_GAP` list.
12. Sources (form / date / accession / vendor).

Do **not** edit the official note unless the user says to paste the memo section in.

## Do not

- Invent quotes or “remembered” Q&A.
- Dump a vendor transcript into the workspace.
- Treat ARR as GAAP.
- Call a definition change a lie.
- Change the official rating or field.
- Stand up a parallel EDGAR/DCF pipeline.

## Return

Companion path · call count · HIT/MISS/OPEN/PARTIAL/ABANDONED counts · open `DATA_GAP`s · whether a filed transcript existed · rating unchanged.
