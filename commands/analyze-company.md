---
name: analyze-company
description: Run Reef Point equity research end-to-end on one ticker. Official memo, field, and the HTML research site.
---

# Analyze company

Read and execute `skills/full-company-analysis/SKILL.md`.

**Ticker** = the symbol the user named (e.g. `/analyze-company NVDA`). If none, ask once.

Mode = **full** unless they said `lite` / `quick look`.

Do not wait on X. Do not use Zapier. Do not copy another name’s figures. Do not rewrite a locked official note.

Before you finish, write `docs/{ticker-lower}-reef-point-live.html`. That file is the site. Do not ask for a URL.
