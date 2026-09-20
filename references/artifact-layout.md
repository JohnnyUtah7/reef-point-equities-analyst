# Artifact layout

All run outputs for ticker `TICKER` land under:

```
artifacts/{TICKER}/
  00-intake.md
  01-sec/
    filings_index.json
    financials.json            # or financials_text.json
    notes.md
    dilution_if_converted.md
  02-statements/
    normalized_is_bs_cf.md
    fcf_bridge.md
  03-models/
    dcf.md
    comps.md
    lbo.md
    sotp.md
    sensitivity.md
    txns.md
    replacement.md
    yield.md
  04-research/
    competitive.md
    unit_economics.md
    catalysts.md
    risk_audit.md
    hub_audit.md
    memo.md                    # full body, or pointer to official docs/ note
  05-deck/
    slide.md                   # speaker notes (optional once PPTX exists)
    deck.pptx                  # or symlink to docs/{ticker}-valuation.pptx
    deck_link.txt
  RUNLOG.md
```

When the workspace has a `docs/` folder (research hub):

| Artifact | Path |
|---|---|
| Official published note | `docs/{ticker-lower}-equity-research.md` |
| Earnings-call companion | `docs/{ticker-lower}-earnings-calls.md` |
| Workbook | `docs/{ticker-lower}-model.xlsx` |
| Deck PPTX | `docs/{ticker-lower}-valuation.pptx` |

Plugin masters (do not overwrite per-ticker):

| Asset | Path |
|---|---|
| Logo | `assets/rpc-logo.png` |
| Deck master | `assets/house-template.pptx` |

## Path discipline

| Artifact | Official path | Rule |
|---|---|---|
| Equity research memo | `04-research/memo.md` **and** `docs/{ticker}-equity-research.md` when `docs/` exists | Full body (≥ ~30 lines). A pointer-only studio file is allowed only if the `docs/` note is the full official body and RUNLOG records that path. |
| Deck | PPTX from house template + Drive Slides URL | `slide.md` is notes. Empty `05-deck/` with no PPTX → incomplete. |
| Dilution | `01-sec/dilution_if_converted.md` | Required when converts/ATM/options exist. |

### RUNLOG completion gates

- Cannot mark the memo complete if there is no full body at the official path.
- Cannot mark the deck complete if there is no PPTX (or Slides URL) and no `slide.md`.
- Cannot mark valuation complete if `$/sh` used cover shares while converts were knowable.

Create missing folders as you go. Never overwrite without updating RUNLOG.
