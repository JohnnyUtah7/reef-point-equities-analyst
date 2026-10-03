# Artifact layout

Write into the **open workspace**, not into the plugin folder.

```
artifacts/{TICKER}/
  RUNLOG.md
  00-intake.md
  01-sec/          company_meta.json filings_index.json financials.json notes.md
  02-statements/   normalized_is_bs_cf.md fcf_bridge.md
  03-models/       dcf.md comps.md lbo.md sotp.md sensitivity.md
                   txns.md replacement.md yield.md
  04-research/     competitive.md unit_economics.md catalysts.md
                   risk_audit.md hub_audit.md memo.md
docs/{ticker-lower}-equity-research.md      # OFFICIAL
docs/{ticker-lower}-earnings-calls.md
docs/{ticker-lower}-model.xlsx
docs/{ticker-lower}-valuation.pptx
```

`04-research/memo.md` points at the official note. Do not ship a locked rating inside this plugin.
