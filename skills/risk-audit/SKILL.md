---
name: risk-audit
description: >
  First adversarial gate on studio artifacts. PASS / PASS_WITH_FIXES / FAIL.
  House research-auditor still runs on the official memo.
---

# Risk audit (studio gate)

Write `artifacts/{TICKER}/04-research/risk_audit.md` **before** the official memo.

Hunt: fabricated numbers, scale (thousands vs millions), ARR treated as GAAP, cover-only `$/sh`, circular own-multiple, TV % of EV hidden, BS/CF breaks, peer multiples invented.

```
VERDICT: PASS | PASS_WITH_FIXES | FAIL
```

FAIL if a load-bearing figure cannot be traced. The house `research-auditor` re-runs dilution and circularity on the published note. Do not skip this gate.
