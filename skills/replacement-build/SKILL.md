---
name: replacement-build
description: >
  Asset-based valuation for the football field: book equity, PPE minus net
  debt, and the equity-funded replacement stack. A floor, not a cash-flow
  value. Triggers: asset-based, NAV, book value, replacement cost, PPE floor.
---

# Asset-based valuation (replacement / build floor)

Studio has no separate skill for this. On the field the bar is still the **replacement / build floor**, weight 0–15%. Never treat it as intrinsic value. The canvas sub-view and the deck appendix call it **Assets** so the three layers are visible.

## Three layers (same `value_shares`)

| Layer | What it is |
|---|---|
| Book | Reported book equity / `value_shares` |
| Tangible / PPE − net debt | `(PPE_net − net_debt) / value_shares` |
| Replacement stack | Equity-funded cost to reproduce **live or in-build** units, after the double-count subtraction |

Liquidation (orderly or forced) only if a filing, appraisal, or disclosed reserve exists. Otherwise `DATA_GAP`. Do not invent a haircut percent.

## Three stacked floors (same `value_shares`)

```
book_floor      = book_equity / value_shares
ppe_floor       = (PPE_net − net_debt) / value_shares
build_equity    = live_or_inbuild_units × ($/unit_dc + $/unit_kit) × equity_funded_pct
                  − net_debt
                  − double_count_of_PPE_already_in_the_stack
build_floor     = build_equity / value_shares
```

Units are whatever the 10-K actually counts (MW IT, rooms, vehicles, stores). `$/unit` must cite a filing, 8-K, or labeled IR figure — two disagreeing sources both stay on the page.

## Rules

1. **Floor, not a DCF.** No WACC, no terminal value.
2. **Live / in-build only** for the mid. Unbuilt pipeline gets a **probability haircut** or stays out.
3. **Do not double-count.** If PPE already is the campus, do not add a full replacement stack on top without subtracting the PPE you just counted.
4. **Financing matters.** If GPUs / kit are ~90% customer-prepaid or SPV-financed, only the **equity-funded** slice is a floor for equity holders.
5. Restricted cash stays out of net debt unless it is free to equity.

## When to skip

Skip only if the business is not asset-reproducible (pure software with no meaningful PPE, or a bank). Say why. A marketplace with a real warehouse/DC footprint still gets a PPE floor.

## Output

Low = min(book, PPE-ND). Mid = PPE-ND plus haircut pipeline land / option value. High = in-build + near-term committed capacity at the equity-funded stack.

Write `artifacts/{TICKER}/03-models/replacement.md` and the `Replacement` Sheets tab. The same three layers are the **Assets** sub-view under the Valuation tab and one deck appendix slide. Do not add a top-level canvas tab for this method.

## Worked pattern

Low = PPE − net debt (or book if tighter). Mid adds haircut pipeline. High = in-build + near-term committed capacity at the **equity-funded** stack. Do not copy another name’s $/unit.
