---
name: replacement-build
description: >
  Replacement / build-cost floor for the football field. Not a cash-flow
  value. Triggers: replacement cost, build cost, PPE floor, reproduction cost.
---

# Replacement / build cost

This is a **floor**, weight 0–15% in the blend. Never treat it as intrinsic value.

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
3. **Do not double-count.** If PPE already is the plant, do not add a full replacement stack on top without subtracting the PPE you just counted.
4. **Financing matters.** If kit is mostly customer-prepaid or SPV-financed, only the **equity-funded** slice is a floor for equity holders.
5. Restricted cash stays out of net debt unless it is free to equity.

## When to skip

Skip only if the business is not asset-reproducible (pure software with no meaningful PPE, or a bank). Say why. A marketplace with a real warehouse/DC footprint still gets a PPE floor.

## Output

Low = min(book, PPE-ND). Mid = PPE-ND plus haircut pipeline land / option value. High = in-build + near-term committed capacity at the equity-funded stack.

Write `artifacts/{TICKER}/03-models/replacement.md` and the `Replacement` Sheets tab.
