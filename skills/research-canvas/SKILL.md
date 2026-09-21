---
name: research-canvas
description: >
  Optional shareable research surface after the official memo is locked.
  Three paths: native Cursor canvas, Next.js web fallback, or a Drive Sheets
  working book. Never Zapier. Not a substitute for the memo, model, or deck.
---

# Research canvas

Optional. Default `analyze TICKER` does **not** require this.

## Gate

If `docs/{ticker-lower}-equity-research.md` is missing or unlocked (no Buy/Hold/Sell + field), run `portfolio-research` first. Copy rating, PT, `value_shares`, and field inputs from that note. **No second model.**

## Pick one publish path (or A+B together)

| Path | When |
|---|---|
| **A. Native Cursor canvas** | User is in Cursor and wants a `.canvas.tsx` |
| **B. Next.js web fallback** | User wants a shareable browser URL |
| **C. Sheets working canvas** | User wants Drive tabs without a web app |

A+B is the usual pair when they want Cursor plus a browser URL. C is the Drive-only working surface. Do not invent a fourth.

Every surface: **Not investment advice.** Rating / PT / share count **match the official memo**.

## Fixed tabs (do not add a slide per method)

1. Exec / rating
2. Business
3. Thesis
4. Financials
5. Valuation — field + method range on **one** surface
6. Risks & catalysts
7. Sources / audits

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
- Expanding Valuation into one tab per method — do not.
