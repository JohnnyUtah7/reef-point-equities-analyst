---
name: research-canvas
description: >
  Required research site after the official memo is locked. Any analyze,
  value, or pick-a-stock prompt writes one HTML file. That file is the GPT
  site, the Claude artifact, and the Grok handoff. Do not ask for a URL.
  Cursor canvas is optional and only if asked. Never Zapier.
---

# Research site

**Required** on any prompt that analyzes, values, or picks a public stock. Write the file. Then stop. Do not ask the user where the site lives.

## Do not

- Do not ask for a site URL, a GitHub repo, or a ChatGPT Sites publish step.
- Do not finish with a description of a page you did not write.
- Do not scaffold Next.js for this. One HTML file.

## The file

`docs/{ticker-lower}-reef-point-live.html`. Self-contained. No `fetch`. Numbers come from the official memo and the models. **No second model.**

The page shows two layers at once:

- **Published** — the memo’s Buy/Hold/Sell, price, and football field. This does not move when a knob moves.
- **Your scenario** — knobs recalculate a draft beside it. Label it draft.

Controls, all live: growth, margins, capex, discount rate, terminal growth, multiples, dilution. Presets: bear / base / bull, plus reset to the published assumptions.

Valuation sub-views: **Field · Comps · Precedents · Assets**. Comps starts on the researched peer set. The user can toggle peers. A toggle changes the draft implied price only.

Research opens on **By quarter** (they said / next print showed / kept). Sentiment does not rate the name.

Hand back the file path. If you can open it in a browser, open it.

Generate it by running the script. Do not hand-write a second page.

```bash
python3 scripts/build_research_site.py artifacts/{TICKER}/03-models/site.json
```

`site.json` is filled from the official memo: ticker, rating, target, last, base knobs, methods, peers, quarters, deals, assets. If the script did not run, the stock prompt is not done.

## Gate

If `docs/{ticker-lower}-equity-research.md` is missing or unlocked (no Buy/Hold/Sell + field), run `portfolio-research` first. Copy rating, PT, `value_shares`, and field inputs from that note. **No second model.**

## Publish paths (same numbers)

| Path | When |
|---|---|
| **HTML (default share)** | Claude artifact, GPT site, and the Grok bot’s handoff. One file: `docs/{ticker-lower}-reef-point-live.html`. No build step |
| **A. Native Cursor canvas** | User is in Cursor and wants a `.canvas.tsx` |
| **C. Sheets working canvas** | User wants Drive tabs without a web app |

Do not scaffold a second site for GPT or Grok. The bot and the Custom GPT hand over the HTML file. A Next.js app is optional and only if the user already asked for a self-hosted URL.

Every surface: **Not investment advice.** Rating / PT / share count **match the official memo**.

## Fixed tabs (do not add a slide per method)

1. Exec / rating
2. Business
3. Thesis
4. Financials
5. Valuation — field + method range on **one** surface. Inside it, sub-views: **Field · Comps · Precedents · Assets**. Comps defaults to the researched peer set; the user can toggle names. The toggle prints a draft implied $/sh and does **not** move the official call unless they lock the set into the memo.
6. Research / Calls — default sub-view **By quarter** (one row per call: they said / next print showed / kept). Ledger, slip clock, and language drift stay as the other sub-views. Sentiment does not rate the name.
7. Risks & catalysts
8. Sources / audits

White cover: full white, RPC logo centered, ticker + date small-caps under the mark. Interior: black / white / hairline. SpaceX / Anduril.

Circular field bars: **dashed**, excluded from the blend. Axis unit `$/ordinary share`. Last-print line + PT band.

## A. Native Cursor canvas

Follow `~/.cursor/skills-cursor/canvas/SKILL.md`:

1. Write **with the Write tool** to the workspace managed canvas path:  
   `~/.cursor/projects/<workspace-key>/canvases/<ticker>-reef-point-research.canvas.tsx`  
   Resolve `<workspace-key>` from the open project. Do not hardcode a machine path.
2. A store UUID `source.canvas.tsx` is an archive only. It does **not** compile. Put a file (or hardlink) in the managed `canvases/` folder.
3. First line: `// cursor-canvas-title: {TICKER} — Reef Point Research`.
4. Import only from `cursor/canvas`. Embed numbers. No `fetch`.
5. `Pill` + `useCanvasState<TabId>("tab", "exec")`.
6. Field = labeled SVG. Colors from `useHostTheme()` on the native canvas (SDK). House white-cover look lives on path B.

Save-tool compile = no TS errors. Return a markdown link to the **managed** `.canvas.tsx` path.

**Do not invent** `https://cursor.com/canvas/store-…` URLs. A share exists only after the user opens the rendered canvas and clicks **Publish** on the toolbar (paid plan + team + privacy mode that allows storage). Until then, canvases are local.

## B. Next.js web fallback

- Scaffold into a **subdirectory**, then move to repo root (`create-next-app` must not target `/workspace`).
- TypeScript + Tailwind. shadcn Tabs. Hairline, radius 0.
- Copy `assets/rpc-logo.png` → `public/rpc-logo.png`.
- Uncommon port (not 3000 / 5173 / 8080).
- Tab routes are server HTML: `/?tab=exec` `/?tab=business` `/?tab=thesis` `/?tab=financials` `/?tab=valuation` `/?tab=risks` `/?tab=sources`. Hash aliases (`#valuation`) redirect to the query form so a blocked client bundle still swaps panels.
- Copy matches the official note. Leave the dev server running and emit a preview tag.

Do not dirty an unrelated git checkout. Use the current workspace only if the user already has a canvas app there.

## C. Sheets working canvas

Different file from the official model workbook.

1. `docs/{ticker-lower}-canvas.xlsx`
2. Tabs: Exec · Thesis · Field · Statements · Dilution · Catalysts · Risks · Open · Sources
3. Figures from the official memo / studio artifacts only
4. Drive `create_file`, xlsx MIME, conversion on, title `{TICKER} Research Canvas — Reef Point`
5. Confirm `application/vnd.google-apps.spreadsheet`
6. `share_file` only if asked

## Pointer doc

Write or update `docs/{ticker-lower}-research-canvas.md` with native path, web branch/port, Sheets URL if any, and a link to the official note.

## Failure modes

- Second model / leftover stale rating — stop, re-read the official note.
- Native canvas written only to a store archive path — opens as source, will not preview or Publish. Put a file in the workspace managed `canvases/` folder.
- Hardcoded house hex on the native canvas — SDK rejects; put white-cover fidelity on path B.
- Zapier — do not.
- Expanding Valuation into one tab per method — do not. Sub-views under Valuation and under Research are the drill-down. Research sub-views: ledger, slip clock, language drift. Sentiment still does not rate the name.
