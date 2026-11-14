# Research site schema v2

Use `scripts/build_research_site.py` from the installed plugin root with an absolute workspace `site.json` path. The output is `docs/{ticker}-reef-point-live.html` beside the workspace's artifacts directory. One embedded calculation engine supplies both the base reconciliation check and browser interactions. No external fonts, scripts, APIs or assets are required by the output.

## Required published fields

`ticker`, `name`, `asof`, `rating` (BUY/HOLD/SELL), `target` (number or null with `target_open:true`), `last`, `methods`. The published rating/target come from the locked memo. `stance` defaults to `bull`; use `bear` when the user explicitly requests a short, put, downside thesis, or bear case. A stance is presentation and scenario selection, not permission to invent a Buy/Sell recommendation.

Each method: `name`, `lo`, `mid`, `hi`, `weight`, optional `circular`, optional `kind` (`dcf` or `comps`). Ranges must be ordered. Circular methods require weight 0. DCF ranges recompute at current WACC ±1 percentage point; a point with WACC ≤ g is invalid. Comps becomes a point estimate from the selected peer median. Other ranges remain supplied model outputs (only scaled for explicit additional dilution), and must be labeled as such. Do not imply every method is fully remodeled by every control.

## Reconciled FCFF model

`model` must contain:

- `base_revenue_m`: latest normalized revenue; positive.
- `forecast`: chronological array with at least two rows. Each has `year`, `revenue_m`, `ebit_margin_pct`, `tax_rate_pct`, `da_pct`, `capex_pct`, `nwc_pct`.
- `wacc_pct`, `terminal_growth_pct`, `net_debt_m`, `shares_m`.
- `expected_dcf_price`: the locked DCF result (not the blended price target).
- `source`: model/filing provenance, and `share_basis`: the validated if-converted share basis.

Percentages are percentage values, e.g. 12 not 0.12. Money and shares are in millions. EBIT margins must expense SBC. Cash tax applies only to positive EBIT; this engine does not create tax-loss assets. D&A and capex are percentages of revenue; ΔNWC is `nwc_pct × change in revenue`. If the official model uses a different reinvestment convention, do not force the data into this engine: adapt/reconcile the engine or ship read-only views with a DATA_GAP.

FCFF = EBIT − cash tax + D&A − capex − ΔNWC. Year-end PV; terminal FCFF = last forecast FCFF × (1+g); Gordon terminal value = terminal FCFF/(WACC−g). EV is forecast PV plus terminal PV; equity subtracts net debt; price divides by valuation shares. `expected_dcf_price` must reconcile within $0.02 or generation fails. Do not set the expected value from the renderer merely to bypass the check.

`model` may be absent for read-only research. Never substitute a capped price multiplier. Missing models disable scenario controls and leave a visible gap. Banks/insurers require specialized models and should not be forced into FCFF.

## Scenarios and risks

`presets`: objects named `bull`, `base`, `bear`, with justified model overrides. Default knobs: `growth_delta:0` (annual incremental compounding in percentage points over the supplied revenue path), `margin_delta:0` (EBIT margin pp), `capex_scale:100`, `wacc:model.wacc_pct`, `g:model.terminal_growth_pct`, `dilution:0` (extra unfunded dilution %), `debt_delta:0` ($m).

Always supply a researched `bull` preset for default ticker requests and a researched `bear` preset for explicit shorts. If unavailable, disclose the gap and show the reconciled base without relabeling it a sourced bull target. The cover may lead with the operating bull thesis while its numeric target stays open. The fixed published memo remains visible beside the draft case.

`risks`: `{title,text,source,shocks}`; shocks are additive changes to known controls. Multiple selected risks add their shocks. Explain each shock, and avoid double counting overlapping risks. Qualitative risks omit shocks. Changing capital structure beyond explicit extra dilution requires a new if-converted analysis, not an automatic repricing of convertibles.

## Rich views

- `business`, `thesis`, `language`, `audits`: arrays of strings or `{title,text,source,kill}` cards.
- `statements`: array of `{title,units,source,periods:[...],rows:[{label,values:[...]}]}`. These filing snapshots never change with scenarios.
- `peers`: `{ticker,default,pe,ev_ebitda,ev_sales,ps,source}`. Missing or nonpositive ratios are NM. Include P/E, EV/EBITDA, EV/Sales even where NM.
- `comps_basis`: `{revenue_m,ebitda_m,net_income_m}` with a common valuation period; explain it in source material. EV methods subtract scenario net debt; P/E and P/S are equity multiples.
- `quarters`: `{call,date,said,showed,kept,source}`.
- `ledger`: `{promise,date,outcome,evidence,source}`. Outcomes: KEPT, MISSED, OPEN, REVISED.
- `catalysts`: `{date,event,estimated,source}`. Unsourced dates must set estimated true.
- `sources`: strings or `{title,url,form,date,accession,note}`. Only HTTP(S) links are active.
- `data_gaps`: strings. An empty array is not an audit certification.
- `deals`: `{name,status,multiple,source,note}`; `assets`: `{layer,ps,note,source}`.

The synthetic example in `examples/research-site-v2.json` demonstrates the schema, not investment research. Do not reuse its numbers for a real issuer.

## Shareability

Generate one HTML; the same bytes serve as the standalone artifact and Sites content. Publish through the host's current Sites skill, private by default unless the user requests public. Return only an actual successful deployment URL. If hosting fails, return the HTML and the exact blocker, not an invented URL. Scenario JSON export is a local draft record, not a new published memo. Check desktop/mobile layouts, tab switching, preset/reset, peer selection, risk toggles, invalid scenarios and theme before claiming browser QA.


## Statement input lineage and additional valuation engines

Supply `fundamentals` keyed by `revenue_m`, `ebit_m`, `net_income_m`, `da_m`, `cfo_m`, `capex_m`, `cash_m`, `debt_m`, `lease_debt_m`, `net_debt_adjustments_m`, `book_equity_m`, and `ppe_m`. Every entry carries `{value, statement, period, source}`. Sources should identify filing accession/URL and note/table. USD millions; capex is a positive cash outflow. Use null for missing, never a fabricated zero. Cash must be unrestricted. Avoid counting leases twice if debt already includes them; make the adjustment explicit. Align income and cash-flow periods; balance-sheet figures are point-in-time. Show normalization and FX separately.

The generator reconciles model base revenue to the revenue input and net debt to debt + leases − cash + adjustments. EBITDA = EBIT + D&A; reported CFO − capex is a separate levered cash-flow metric, never substituted for FCFF. Explicit forward/normalized `comps_basis` overrides require `comps_basis_source` with period and provenance.

A `kind: "precedents"` method uses `transactions` entries `{name, metric, multiple, source, include}`; metric is ev_ebitda or ev_sales. Min/median/max observed multiples apply to the target statement metric; deduct net debt once. Do not silently add a control premium.

A `kind: "sotp"` method uses `sotp.segments` entries `{name, metric_m, multiple_low, multiple_base, multiple_high, source}` and optional `holdco_value_m`, `discount_pct`. Sum segment EVs, subtract capitalized holdco value, apply the stated discount, subtract consolidated net debt once, divide by shares. Explicitly reconcile segment metrics to consolidated totals or explain eliminations.

`kind: "book"` uses book equity without deducting debt again. `kind: "ppe"` deducts net debt from net PPE and is an asset cross-check, not a guaranteed liquidation floor. `kind: "replacement"` uses `replacement.layers` entries `{name, low_m, base_m, high_m, source}`; sum then deduct net debt. Source valuation-cost assumptions independently from reported accounting values.

The annual growth control adds percentage points to each supplied year's revenue growth and compounds from the preceding scenario year. Forecast assumptions are estimates, not reported figures. The engine does not automatically re-underwrite convertible instruments or financing proceeds when dilution changes.
