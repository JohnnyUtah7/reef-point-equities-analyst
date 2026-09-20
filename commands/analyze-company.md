---
name: analyze-company
description: Run Reef Point Equities end-to-end pipeline for a ticker (portfolio-research)
---

# Analyze company

Run skill `portfolio-research` for the ticker provided in the argument or chat.

```text
analyze TICKER
```

1. Confirm ticker
2. Ensure `EDGAR_IDENTITY` is set (prompt if not)
3. Execute portfolio-research (studio 1–13 + house overlays + Sheets + PPTX)
4. Return paths to official memo, Sheets, and deck
