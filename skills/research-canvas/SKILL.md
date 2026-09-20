---
name: research-canvas
description: >
  Optional shareable research surface after the official memo is locked.
  Paths: native Cursor canvas, Next.js web fallback, or a Drive Sheets
  working book. Never Zapier. Not a substitute for the memo, model, or deck.
---

# Research canvas

Optional. Default `analyze TICKER` does **not** require this.

## Gate

If the official note is missing or unlocked (no Buy/Hold/Sell + field), run `portfolio-research` first. Copy rating, PT, `value_shares`, and field inputs from that note. **No second model.**

## Pick one publish path (or A+B together)

| Path | When |
|---|---|
| **A. Native Cursor canvas** | User is in Cursor and wants a `.canvas.tsx` |
| **B. Next.js web fallback** | User wants a shareable browser URL |
| **C. Sheets working canvas** | User wants Drive tabs without a web app |

Do not invent a fourth. Every surface: **Not investment advice.** Rating / PT / share count **match the official memo**.

## Fixed tabs (do not add a slide per method)

1. Exec / rating
2. Business
3. Thesis
4. Financials
5. Valuation — field + method range on **one** surface
6. Risks & catalysts
7. Sources / audits

White cover: full white, RPC logo centered (`assets/rpc-logo.png`), ticker + date small-caps under the mark. Interior: black / white / hairline.

Circular field bars: **dashed**, excluded from the blend. Axis unit `$/ordinary share`. Last-print line + PT band.

## A. Native Cursor canvas

If the Cursor canvas skill is available, follow it:

1. Write a `.canvas.tsx` into the workspace managed `canvases/` folder: `{ticker}-reef-point-research.canvas.tsx`.
2. First line: `// cursor-canvas-title: {TICKER} — Reef Point Research`.
3. Import only from `cursor/canvas`. Embed numbers. No `fetch`.
4. Tab state via the canvas SDK. Field = labeled SVG.

Do **not** invent share URLs. A public share exists only after the user publishes from the canvas toolbar.

## B. Next.js web fallback

- Scaffold into a **subdirectory**, then move files if needed (`create-next-app` must not target a parent it cannot write).
- TypeScript + Tailwind. Hairline, radius 0.
- Copy `assets/rpc-logo.png` → `public/rpc-logo.png`.
- Uncommon port (not 3000 / 5173 / 8080).
- Tab routes as server HTML query params so a blocked client bundle still swaps panels.
- Copy matches the official note.

Use the current workspace only if the user already has a canvas app there. Do not modify unrelated repos.

## C. Sheets working canvas

Different file from the official model workbook.

1. `docs/{ticker-lower}-canvas.xlsx` or `artifacts/{TICKER}/04-research/canvas.xlsx`
2. Tabs: Exec · Thesis · Field · Statements · Dilution · Catalysts · Risks · Open · Sources
3. Figures from the official memo / studio artifacts only
4. Drive upload, xlsx MIME, conversion on, title `{TICKER} Research Canvas — Reef Point`
5. Confirm `application/vnd.google-apps.spreadsheet`
6. `share_file` only if asked

## Failure modes

- Second model / leftover stale rating — stop, re-read the official note.
- Zapier — do not.
- Expanding Valuation into one tab per method — do not.
