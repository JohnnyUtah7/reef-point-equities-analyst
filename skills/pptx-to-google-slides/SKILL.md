---
name: pptx-to-google-slides
description: Generate a real .pptx (python-pptx), then convert it to native Google Slides by uploading through Google Drive (conversion-on-upload). Never use Zapier. Use when the user wants a slide deck, Google Slides URL, equity-research presentation, or PPTX→Slides conversion.
---

# PPTX → Google Slides

Hard constraint: **do not use Zapier**. There is no Zapier fallback.

Canonical path (Drive conversion-on-upload):

1. Author a real `.pptx` (python-pptx).
2. Upload those bytes to Google Drive with media MIME = PowerPoint and **conversion enabled**.
3. Confirm the created file MIME is `application/vnd.google-apps.presentation`.
4. Return `https://docs.google.com/presentation/d/{fileId}/edit`.

Documented by Google (“Import to Google Docs types”) and by [google_workspace_mcp#822](https://github.com/taylorwilsdon/google_workspace_mcp/pull/822) / [camoa/claude-skills pptx_import](https://github.com/camoa/claude-skills/commit/fc2bfe8a69762d107cc3460045ca8a54fdd4f7f6).

**Rejected as official:** studio `slides-deck`, `gws auth login`, jackchuka `p-md-to-slides` (markdown → Slides API, Tailor navy/cream themes). Those may write `artifacts/{TICKER}/05-deck/slide.md` as speaker notes only.

## When to use

- Deck step of `portfolio-research` / `analyze TICKER end-to-end`.
- Any “make a Google Slides deck” request in this project.
- Rebuild if the official memo rating or PT changed. Do not patch a stale deck.

## House contract

- Master: `assets/house-template.pptx`.
- Logo: `assets/rpc-logo.png`.
- Cover: white, logo centered, optional small-caps ticker + date. No header, no confidential strip, no slide number.
- Interior: takeaway line, slide numbers, proprietary footer, small RPC logo top-right.
- Numbers **only** from `docs/{ticker}-equity-research.md` + `artifacts/{TICKER}/` + the Sheets named ranges. No new unsourced figures.
- Visual: SpaceX / Anduril. **Not** Pitch Agent IB navy `#1F4E79`, not jackchuka Tailor navy/cream.

## Required 10-slide spine

1. Cover (white RPC)
2. Agenda
3. Business / model (three-up)
4. Thesis pillars (claim + kill on the page)
5. Financial snapshot (KPI table from the memo)
6. **Football field** (all live bars, last-print line, circular dashed)
7. Method deep-dive (one slide; pick the load-bearing method — usually DCF)
8. Risks + killing conditions
9. Catalysts
10. Recommendation = memo Buy/Hold/Sell + range + central + disclaimer

If you need a comps table, replace slide 7 or add **one** appendix slide — do not expand into one slide per method on a 10-pager (canvas is the higher-level surface).

## Required tools

**Google Drive MCP** (`Google-drive`): `create_file`, `get_file_metadata`, `search_files`. Optional `share_file` if asked.

If Drive is missing / 401: **authenticate Drive and stop**. No Zapier.

## Step-by-step

### 1. Author PPTX

```
pip install python-pptx   # or: pip3 install -r scripts/requirements.txt
```

- Widescreen `Inches(13.333)` × `Inches(7.5)`. Calibri/Arial, solid fills, simple tables.
- Avoid OLE, SmartArt, huge images (Drive importer + MCP base64 limits).
- Save `docs/{ticker-lower}-valuation.pptx`.

### 2. Name the Drive file

Title **without** `.pptx` (becomes the Slides name). Example: `{TICKER} Valuation — Equity Research`. `parentId` = research or ticker folder; create if needed.

### 3. Upload + convert

```text
title:                 <deck title, no .pptx>
contentMimeType:       application/vnd.openxmlformats-officedocument.presentationml.presentation
base64Content:         <base64 of the .pptx bytes>
disableConversionToGoogleType: false
parentId:              <optional folder id>
```

Do **not** set `disableConversionToGoogleType: true`.

### 4. Verify native Slides

MIME must be `application/vnd.google-apps.presentation`. If still PPTX, retry once with conversion on; then **fail loudly**.

### 5. QC (Pitch Agent `ib-check-deck`, house-flavored)

Pull **three** figures at random from the deck and trace them to the official memo or Sheets named range. Totals tie. As-of dates match. Rec slide matches the memo rating. Footer year is current.

### 6. Return

```text
https://docs.google.com/presentation/d/{fileId}/edit
```

Plus local PPTX path, file id, MIME, folder URL.

## Failure modes

| Failure | Do |
|---|---|
| Drive 401 / mcp_auth | Authenticate Drive. Stop. No Zapier. |
| base64 too large | Strip images; retry. |
| Stored as raw PPTX | Retry conversion on; else fail. |
| Garbled import | Simplify PPTX; re-upload. |
| Memo rating changed since PPTX | Rebuild; do not patch a stale deck. |
| Zapier offered | Ignore. |

## Do not

- Zapier / Make / n8n / email-to-Drive.
- `gws` or jackchuka as official publish.
- Paste bodies into a blank Slides file instead of conversion.
- Wait on Zapier auth.
- Modify unrelated git repos to “help” conversion.
