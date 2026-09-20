# Reef Point Equities Analyst

Cursor / Claude plugin for one-name equity research:

**SEC filings → statements → DCF / comps / LBO / SOTP → dilution & football field → official memo → Google Sheets → PPTX → native Google Slides**

One prompt:

```text
analyze TICKER
```

Also accepted: `analyze TICKER end-to-end`, `check out NVDA`, `full analysis of MSFT`.

This is a **workflow aid**. Every published note is labeled **not investment advice**.

## What’s inside

| Layer | What it does |
|---|---|
| Studio engine | 16 skills: intake, EDGAR, statements, DCF, trading comps, LBO, SOTP, competitive, unit econ, scenarios, catalysts, risk-audit, draft memo, slide notes |
| Reef Point overlays | Dilution / if-converted, transaction comps, replacement floor, yield/residual, football field + blend, memo pillars, research auditor, Sheets workbook, PPTX→Slides |
| Agents | 8 role cards (Research Lead → Deck Producer) |
| Commands | `/analyze-company`, `/dcf`, `/sec-pull`, `/slides` |
| Rule | Never invent SEC numbers; Buy/Hold/Sell from the field; no Zapier |
| Assets | `assets/rpc-logo.png`, `assets/house-template.pptx` |

**Not included:** IREN (or any name) as a packaged proof note. Run a ticker; do not treat example patterns as a rating. **Not included:** Zapier, vendored EDGAR clones, OAuth tokens.

## Install — Cursor

```bash
mkdir -p ~/.cursor/plugins/local
rsync -a --delete ./ ~/.cursor/plugins/local/reef-point-equities-analyst/
```

Restart Cursor or run **Developer: Reload Window**. Confirm skills under Customize / Plugins: `portfolio-research`, `full-company-analysis`, `sec-filings`.

**Project-local (no plugin UI):**

```bash
mkdir -p .cursor/skills .cursor/agents .cursor/rules
cp -R skills/* .cursor/skills/
cp -R agents/* .cursor/agents/
cp rules/*.mdc .cursor/rules/
```

## Install — Claude Code

```bash
# Local marketplace from this folder
claude plugin marketplace add "$(pwd)"
claude plugin install reef-point-equities-analyst
```

Or copy skills:

```bash
mkdir -p ~/.claude/skills ~/.claude/plugins/reef-point-equities-analyst
cp -R skills/* ~/.claude/skills/
rsync -a ./ ~/.claude/plugins/reef-point-equities-analyst/
```

Exact `claude plugin` flags depend on your Claude Code version. Copying `skills/` always works.

## EDGAR_IDENTITY (required)

SEC fair-access requires a real contact User-Agent on every request. Without it, EDGAR returns **403**.

```bash
export EDGAR_IDENTITY="Your Name you@email.com"
# persist in the shell you use for Agent terminals:
echo 'export EDGAR_IDENTITY="Your Name you@email.com"' >> ~/.zshrc
```

Optional Python stack:

```bash
pip install edgartools python-pptx openpyxl
# If EDGAR pulls fail with FileStorage / hishel errors:
pip install 'hishel==0.1.3'
```

Check:

```bash
echo "$EDGAR_IDENTITY"
python3 -c "import edgar; import importlib.metadata as m; print(m.version('edgartools'))"
```

Then pull:

```bash
python scripts/edgar_pull.py AAPL
```

Never bare-fetch `sec.gov`. Never commit OAuth tokens.

## Analyze a ticker

In Cursor Agent or Claude Code:

```text
analyze AAPL
```

The agent should load `portfolio-research`:

1. Confirm `EDGAR_IDENTITY` and `import edgar`
2. Studio steps 1–13 (intake → SEC → statements → models → draft memo). Skip studio `slides-deck` as the official deck.
3. House overlays: dilution → transaction comps → replacement → yield → football field
4. Official note: Buy / Hold / Sell from the field (`docs/{ticker}-equity-research.md` if the workspace has `docs/`, else `artifacts/{TICKER}/04-research/memo.md`)
5. Research auditor (halt on `FAIL` unless you override)
6. Optional earnings-call companion
7. Sheets workbook → Drive convert (if Google Drive is connected)
8. PPTX from `assets/house-template.pptx` + white RPC cover → Drive convert

Artifacts land under `artifacts/{TICKER}/`. See `references/artifact-layout.md`.

Lite: `quick look at TICKER` skips LBO + SOTP unless the name is multi-segment.

## Deck path

Official deck is **PPTX → Google Drive conversion-on-upload**, not `gws` and not markdown-first Slides API. Studio `slides-deck` may still write `05-deck/slide.md` as speaker notes.

Cover: full white, Reef Point Capital logo centered (`assets/rpc-logo.png`). Interior: takeaway line, hairlines, proprietary footer.

If Drive is missing or 401, authenticate Drive and stop. There is no Zapier fallback.

## Layout

```text
reef-point-equities-analyst/
├── .cursor-plugin/plugin.json
├── .claude-plugin/plugin.json
├── plugin.json
├── skills/                 # studio engine + Reef Point overlays
├── agents/
├── commands/
├── rules/
├── references/             # EDGAR identity, house style, deck spec
├── assets/rpc-logo.png
├── assets/house-template.pptx
├── scripts/edgar_pull.py
├── examples/prompts.md
├── INSTALL.md
└── README.md
```

## Provenance

Skill text is curated from public technique sources listed in `references/sources.md` (edgartools, analyst-kit, Anthropic financial-services, GeniusTrader memo shape). This repo ships **instructions + a thin EDGAR wrapper**, not those repos.

## License

MIT. Copyright (c) 2026 Chris Miller.

## Disclaimer

Educational / professional workflow aid. **Not investment advice.**
