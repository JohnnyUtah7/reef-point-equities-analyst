---
name: sotp-valuation
description: >
  Segment map, per-segment multiple or mini-DCF, holdco, conglomerate
  discount. Skip single-segment with why. Circular own-ARR sleeves weight 0.
---

# SOTP / NAV

Write `artifacts/{TICKER}/03-models/sotp.md`.

Use when **2+ reportable segments in different industries**. Else skip.

```
segment_EV_i = segment_metric_i × peer_median_i
Gross EV     = Σ segment_EV − unallocated HQ (or 8× ongoing HQ cost)
Equity       = Gross EV − ND − NCI − prefs − pension + cash + non-core
             − coupling haircut 5–15% if vertically tied
             − tax leakage 10–20% if a spin is the thesis
```

Net debt **once**. A sleeve that is market EV / the company’s **own** ARR is circular — draw it, weight 0 on the field.

Conglomerate discount without a catalyst (13D, strategic review, announced spin) is dead money — show it, do not sell it.
