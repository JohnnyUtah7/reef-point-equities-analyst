# Reef Point Equities analyst

One pack for Cursor, Claude, Codex, and Grok. **One SEC-listed ticker in. Official memo, football field, Sheets, and white-cover deck out.**

This repo is the product you install and share. It does **not** ship a rating or a worked company note.

```
analyze TICKER
```

or `/analyze-company TICKER`. Fast path: `/analyze-lite TICKER`.

Install: [INSTALL.md](./INSTALL.md). Identity: [references/edgar-identity.md](./references/edgar-identity.md). Layout: [references/artifact-layout.md](./references/artifact-layout.md). Runbook: [docs/ticker-runbook.md](./docs/ticker-runbook.md).

## What you get

| Layer | What it does |
|---|---|
| EDGAR | `scripts/edgar_pull.py` → `artifacts/{TICKER}/01-sec/` |
| Models | Statements, DCF, comps (user-picked or researched; P/E, EV/EBITDA, EV/Sales), LBO (lite), SOTP |
| House overlay | Dilution, precedent deals, asset-based floor (book / PPE − net debt / replacement), yield, football field |
| Calls | One row per quarter: what they said, what the next print showed, kept or not. Does not rate the name |
| Publish | Official note, then the HTML research site. That file is the handoff. Sheets and PPTX follow |

Trigger `analyze TICKER` → `portfolio-research` → studio steps 1–13, then field, official memo, Sheets, white-cover PPTX.

Rating is **Buy / Hold / Sell after the field**. Cover-share `$/sh` is not official. Circular own-ARR bars draw and get **weight 0**.

Official deck is `pptx-to-google-slides`. `slides-deck` / `gws` are speaker notes only.

## Any ticker?

**Yes, if they file with the SEC** (10-K/10-Q or 20-F/6-K). Same skills, ticker in the path.

| Works | Does not |
|---|---|
| US listed, FPI, multi-segment | Private companies, no CIK |
| Asset-heavy or asset-light (skip rules) | Non-US only with no SEC file |
| Lite mode for a same-day look | Banks/insurers as a full bank model (flagged, not faked) |

Do not copy another name’s share count, WACC, or rating.

## Hard no

Zapier. Bare `sec.gov` fetch. Invented multiples. Courtesy Hold when the field is Sell. `gws` as the official deck. Waiting on X.

## Where it runs

Same `skills/` tree. Manifests only point at it.

| Deployment | How |
|---|---|
| Cursor | `.cursor-plugin/plugin.json`. Canvas is `.canvas.tsx` |
| Claude | `.claude-plugin/plugin.json`. Shareable page is the HTML file (artifact) |
| Codex / Custom GPT | `.codex-plugin/plugin.json`. Instructions: [adapters/gpt-instructions.md](./adapters/gpt-instructions.md). The site is that same HTML file |
| Grok bot | `.grok-plugin/plugin.json` plus [adapters/grok-bot.md](./adapters/grok-bot.md). The bot has no canvas. It hands back the HTML file |

**Draft view — not investment advice.**

MIT — Copyright 2026 Chris Miller.
