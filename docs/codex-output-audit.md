# Codex output audit — 25 October 2026

Scope: GitHub main 1.3.16 source, local release ZIP, installed skill visibility, generated HTML, and protocol tests. This is a software/output audit, not an audit of a current stock recommendation.

## Results

- Plugin skills are available in this Codex session, but the installed package reports 1.3.12. GitHub/release ZIP report 1.3.16. Opening a PR does not update an installed plugin or publish a marketplace release.
- The ZIP differs from current GitHub in `edgar-mcp/src/protocol.ts` and `edgar-mcp/test/protocol.test.ts`; local source was refreshed from GitHub.
- Generator regression suite: 17 tests pass. EDGAR protocol unit tests pass.
- EDGAR_IDENTITY is configured and edgartools 4.6.3 is installed. A fresh live data pull was not verified; network access is restricted in this execution environment.
- Browser execution/localhost binding is restricted here. Visual source review is complete; interactive browser QA and hosted Sites publication remain unverified.

## Fixed

1. The generator used a derived bullish cover as the published call. The published chip now takes the memo's rating/target directly; case exploration stays separate.
2. Sliders are a bounded multiplier, not FCFF recomputation. The UI now says this explicitly. A fresh model run is required for a revised valuation.
3. Nonzero baseline dilution no longer shifts the reset value away from its case anchor.
4. Embedded JSON escapes HTML delimiters to prevent script termination through imported peer text.
5. The peer median initializes on load and is labeled as P/S, rather than implying a per-share valuation.
6. Self-contained branded layout, responsive styling, accessible focus states, and Business/Thesis/Financials/Risks/Sources views. Missing content is DATA_GAP, not invented research.
7. Fixed a macOS symlink-path assumption in the existing test.

## Release acceptance still required

- Install the merged release into a fresh Codex session; verify the displayed version.
- Run `analyze TICKER` with a real SEC filer; retain filing accessions, normalized statements, dilution, model, field, memo, audit and site.json.
- Match the published chip and share basis against the locked memo.
- Exercise all tabs, presets, reset, peer toggles and payoff controls at desktop and mobile widths. Confirm no console errors or external asset requests.
- Publish through Sites and verify the returned private URL. Test Drive conversions separately.

## Product limits

The bullish/bearish case policy remains in `open_view`; it is not the official published call. Scenario controls remain illustrative rather than a second financial engine. Comps controls show a P/S median only; EV/Sales, EV/EBITDA and P/E still belong in the official model. Options use theoretical pricing and assumed IV when no IV is supplied. The original full-analysis instructions should be read together with these explicit UI limitations.
