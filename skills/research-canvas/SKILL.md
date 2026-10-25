---
name: research-canvas
description: >
  Build and publish the required detailed, interactive research site for every
  ticker, analyze, value, or stock-opinion request. Lead with the bull case unless
  the user requests a short/bear case. Use the same self-contained HTML for Codex
  Sites and Claude artifacts; model controls, field, financials, evidence and risks.
---

# Research site — the primary deliverable

A ticker alone triggers the complete research workflow. Do not ask what the user means. Run `full-company-analysis` if the official memo, dilution and valuation models do not exist. Default to a researched bull case; explicit short/put/bear requests lead with the bear case. Direction is a thesis and scenario, not an instruction to fabricate favorable findings or overwrite the published memo.

## Generate, verify, share

1. Read the locked official memo and model outputs. Preserve its rating, target, share basis and sourced figures.
2. Read `references/research-site-schema.md` from the plugin root. Populate workspace `artifacts/{TICKER}/03-models/site.json` with schema v2, rich research content and reconciled FCFF inputs. Supply bull/base/bear presets from researched assumptions, never copied from another ticker.
3. Resolve the installed plugin root from this skill's path. Run its script with the absolute workspace spec path:
   `python3 <plugin-root>/scripts/build_research_site.py <workspace>/artifacts/{TICKER}/03-models/site.json`
4. Base DCF must reconcile to the official DCF result within $0.02. Fix model/schema mismatch instead of bypassing the check. Do not rewrite the expected result from the renderer. A missing model remains read-only with DATA_GAP; no heuristic multiplier.
5. Inspect the generated `docs/{ticker-lower}-reef-point-live.html`. Check published memo fidelity, source links, financial units, excluded circular bars, and obvious missing sections. Exercise controls and desktop/mobile layout when browser QA is available. Report unverified checks accurately.
6. On Codex, apply the current Sites skill and publish this same HTML, private by default unless public is requested. Return the actual deployment URL and HTML file. Hosting failure must not erase the HTML deliverable; report the blocker. Do not end on an offer to publish later, ask for a site URL, or invent one.
7. On Claude, return the same HTML as the artifact. Cursor canvas is optional if specifically requested and must follow its current host canvas skill. Do not scaffold a second Next.js page or use Zapier.

## Required experience

- White RPC cover, strong executive hierarchy, light/dark theme, desktop model rail and mobile drawer.
- Bull-case cover by default, bear-case cover for explicit shorts. Keep the published memo visible and fixed beside the exploratory scenario. If a directional preset is missing, disclose it; do not label the base as a sourced bull/bear target.
- Overview, Business, Thesis, Financials, DCF model, Valuation, Research, Risks & catalysts, Sources / audits.
- FCFF forecast and equity bridge, live 5×5 WACC/g sensitivity and tornado, scenario presets/reset, explicit dilution/debt controls.
- Valuation subviews: Field / Comps / Precedents / Assets; dynamic DCF/comps, disclosed static ranges, editable non-circular blend weights. Circular methods always weight 0.
- Quarter evidence, filterable promise ledger, timeline and language/credibility cards. Sentiment does not set the rating.
- Model-linked risk shocks and sourced/estimated catalyst dates. Missing data stays visible.
- One offline-capable file with embedded branding and code. No external assets or runtime fetch. Include “Draft research — not investment advice.”

Keep sector-specific details in the data and official models, not hardcoded into this plugin. The site is the product; do not replace it with a prose description, a video mockup, or a placeholder page.
