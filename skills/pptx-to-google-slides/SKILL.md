---
name: pptx-to-google-slides
description: >
  Generate a real .pptx (python-pptx) from the house template, then convert it
  to native Google Slides by uploading through Google Drive (conversion-on-upload).
  Never use Zapier. Use when the user wants a slide deck, Google Slides URL,
  equity-research presentation, or PPTX→Slides conversion.
---

# PPTX → Google Slides

Hard constraint: **do not use Zapier**. There is no Zapier fallback.

Canonical path (Drive conversion-on-upload):

1. Author a real `.pptx` (python-pptx) from `assets/house-template.pptx`.
2. Upload those bytes to Google Drive with media MIME = PowerPoint and **conversion enabled**.
3. Confirm the created file MIME is `application/vnd.google-apps.presentation`.
4. Return `https://docs.google.com/presentation/d/{fileId}/edit`.

**Rejected as official:** studio `slides-deck`, `gws auth login`, markdown → Slides API. Those may write `artifacts/{TICKER}/05-deck/slide.md` as speaker notes only.

## When to use

- Deck step of `portfolio-research` / `analyze TICKER`.
- Any “make a Google Slides deck” request after an official memo exists.
- Rebuild if the official memo rating or PT changed.

## House contract

- Master: `assets/house-template.pptx` (`references/deck-template-spec.md`).
- Logo: `assets/rpc-logo.png`.
- Cover: white, logo centered, optional small-caps ticker + date. No header, no confidential strip, no slide number.
- Interior: takeaway line, slide numbers, proprietary footer, small RPC logo top-right.
- Numbers **only** from the official memo + `artifacts/{TICKER}/` + Sheets named ranges. No new unsourced figures.
- Visual: black / white / hairline. **Not** IB navy `#1F4E79`.

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

If you need a comps table, replace slide 7 or add **one** appendix slide.

## Required tools

**Google Drive** (`create_file`, `get_file_metadata`, `search_files`). Optional `share_file` if asked.

If Drive is missing / 401: **authenticate Drive and stop**. Leave the local PPTX. No Zapier.

## Step-by-step

### 1. Author PPTX

```
pip install python-pptx
```

- Widescreen `Inches(13.333)` × `Inches(7.5)`. Calibri/Arial, solid fills, simple tables.
- Avoid OLE, SmartArt, huge images (Drive importer + MCP base64 limits).
- Save `docs/{ticker-lower}-valuation.pptx` or `artifacts/{TICKER}/05-deck/deck.pptx`.

### 2. Name the Drive file

Title **without** `.pptx` (becomes the Slides name). Example: `{TICKER} Valuation — Equity Research`.

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

### 5. QC

Pull **three** figures at random from the deck and trace them to the official memo or Sheets named range. Totals tie. As-of dates match. Rec slide matches the memo rating. Footer year is current.

### 6. Return

```text
https://docs.google.com/presentation/d/{fileId}/edit
```

Plus local PPTX path, file id, MIME.

## Failure modes

| Failure | Do |
|---|---|
| Drive 401 | Authenticate Drive. Stop. No Zapier. |
| base64 too large | Strip images; retry. |
| Stored as raw PPTX | Retry conversion on; else fail. |
| Garbled import | Simplify PPTX; re-upload. |
| Memo rating changed since PPTX | Rebuild; do not patch a stale deck. |

## Do not

- Zapier / Make / n8n / email-to-Drive.
- `gws` as official publish.
- Paste bodies into a blank Slides file instead of conversion.
