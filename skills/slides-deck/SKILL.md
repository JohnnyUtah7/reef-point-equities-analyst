---
name: slides-deck
description: >
  Write speaker-note markdown (slide.md) for a research deck. Official publish
  is pptx-to-google-slides (house PPTX → Drive convert). Use when the user
  wants notes, or as a companion to the official deck.
version: "1.1.0"
---

# Slides Deck

<!-- Provenance: p-md-to-slides (jackchuka); google-slides-skill (idanbeck);
     Anthropic pptx-author as PPTX fallback -->

## Hard rules
- Deck content must trace to `04-research/memo.md` and `03-models/` — no new unsourced numbers on slides.
- Title slide includes as-of date + disclaimer: not investment advice.
- Write **markdown slide notes**. Official render is `pptx-to-google-slides`.
- **Required path:** Always write `artifacts/{TICKER}/05-deck/slide.md`. If PPTX
  or Google Slides is produced, also place or symlink the binary/export under
  `05-deck/` (e.g. `deck.pptx`) and record path/URL in `deck_link.txt` **and** RUNLOG.
- **RUNLOG gate:** Do **not** mark slides-deck complete if `05-deck/` is empty or
  lacks `slide.md`.
- **Dilution on slides:** Show basic vs fully diluted $/sh (or flag DATA_GAP); never
  show undiluted as “the” value when converts/ATM/options exist.
- **ARR:** Label ARR / contracted ARR as **non-GAAP operating metric** on any slide
  that shows it; disclose tape-implied ARR multiples.
- **Mix transition:** If LTM mix ≠ forward thesis, include a callout slide or callout
  box (do not apply unlabeled pure-AI comps to BTC-heavy LTM).
- **DCF slide:** Must show **TV as % of EV**.

## Slide map (12–16 slides typical)
1. Title / disclaimer
2. One-pager thesis
3. Business at a glance (+ **mix transition** if applicable)
4. Industry & competition
5. Financial snapshot (GAAP vs non-GAAP ARR labeled)
6. Unit economics / quality
7. Valuation triangulation (DCF vs comps vs SOTP; basic + FD)
8. DCF deep dive (1–2) — include **TV as % of EV**
9. Dilution / fully diluted bridge (when converts/ATM/options)
10. Comps table (+ mix caveat if needed)
11. Scenarios / tornado
12. Catalysts
13. Risks & kill criteria
14. Appendix / sources

## Markdown format (p-md-to-slides compatible)
```markdown
# {TICKER} Equity Research

## Slide 1 — Title
**Speaker notes:** ...
**Slide elements:**
- Company | Ticker | Date
- Disclaimer

## Slide 2 — Thesis
...
```

## Render path
**Official deck is `pptx-to-google-slides`.** This skill only writes notes.

1. Always write `artifacts/{TICKER}/05-deck/slide.md`
2. Hand off to `pptx-to-google-slides` for the house PPTX + Drive convert
3. If asked for notes only, stop after `slide.md` — do not invent a Slides URL
4. Do **not** treat `gws auth login` or markdown-first Slides API as official

## Outputs
```
artifacts/{TICKER}/05-deck/slide.md          # REQUIRED
artifacts/{TICKER}/05-deck/deck_link.txt     # URL or path
artifacts/{TICKER}/05-deck/deck.pptx         # optional PPTX or symlink
```

## Caveats for operators
- Official publish needs Google Drive (conversion-on-upload). No Zapier.
- Never commit OAuth tokens into the plugin.
