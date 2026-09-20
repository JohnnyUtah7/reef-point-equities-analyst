# Changelog

## 2.0.0 — 2026-09-20

Team product. IREN was the test run.

- One Cursor plugin: `reef-point-equity-research`
- Orchestrator `full-company-analysis` is ticker-generic (`{TICKER}` paths)
- House overlays shipped **inside** the plugin (dilution, field, txns, replacement, yield, auditor, Sheets, PPTX→Slides, earnings calls)
- `scripts/edgar_pull.py` + `hishel==0.1.3` pin
- Commands: `/analyze-company`, `/analyze-lite`, `/sec-pull`, `/dcf`, `/slides`
- Memo ships before Drive/canvas; those may be `PENDING`
- Not a byte-copy of Mac-local Equity Research Studio 1.0.1 (that pack is not in this repo)
