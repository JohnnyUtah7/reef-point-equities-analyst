# Changelog

## 1.3.0 — 2026-09-22

Valuation drill-downs and the management slip clock.

- CCA: user-picked peer set, or a researched set from the 10-K plus adjacent names. Always print P/E, EV/EBITDA, and EV/Sales; `NM` when the denominator is missing. A canvas toggle is a draft until the memo locks the set.
- Precedent deals and asset-based layers (book, PPE − net debt, equity-funded replacement) are required sub-views under Valuation and appendix slides after the 10-slide spine. Not new top-level tabs. Liquidation only if sourced.
- Earnings companion adds a slip clock (quarters dragged, walks) and a language-drift table. Tension is shown with HIGH / MED / LOW. “Lying” is not a fact. Sentiment still does not rate the name.

## 1.2.0 — 2026-09-21

Approved pack updates from the Reef Point Equities analyst audit.

- Plugin id **`reef-point-equities-analyst`** (was `reef-point-equity-research` 2.0.0)
- MIT license, Copyright 2026 Chris Miller
- `assets/rpc-logo.png` + generated `assets/house-template.pptx`
- `references/` — EDGAR identity, artifact layout, house style, deck spec, sources
- Official deck is `pptx-to-google-slides`; `slides-deck` / `gws` are notes only
- Stripped locked-name ratings, share-count examples, CosmosGolf, Agent Store paths, and “this Mac” install law
- Generic `EDGAR_IDENTITY="Your Name you@email.com"`
- Trigger: `analyze TICKER` → `portfolio-research`
- No company proof note in the pack

## 2.0.0 — 2026-09-20

First combined engine + house overlays in this repo (superseded by 1.2.0 numbering to match the pack plan).
