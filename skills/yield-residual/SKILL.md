---
name: yield-residual
description: >
  Dividend-yield or residual-income bar for the football field. Skip with a
  one-line why when it only reprints book. Triggers: residual income, excess
  return, dividend yield, DDM.
---

# Yield / residual

Banks/insurers remain a studio `DATA_GAP` unless the user asks for a specialized model (this plugin does not add one).

## When it is a real bar

| Variant | Use when | Skip when |
|---|---|---|
| Forward dividend yield | Board-declared DPS, history of paying | `DPS = 0` in the 10-K |
| Residual income (excess return) | Positive NI and ROE / ROIC vs `r_e` | NI or EBIT ≤ 0; RI ≤ 0 so value reprints book |
| DDM / excess return (banks) | User asks **and** you have a bank model | Studio already flagged “specialized model needed” |

## Formulas

**Dividend (simple bar, not a DCF)**

```
fwd_DPS     = last_declared_annual  OR  NTM consensus (label which)
yield_value = fwd_DPS / required_yield
required_yield = r_e   # same Ke as studio WACC build, or a labeled assumption
```

**Residual income**

```
RI_t = NI_t − r_e × Book_{t-1}
V_0  = Book_0 + Σ PV(RI_t) + TV_RI
$/sh = V_0 / value_shares
```

`r_e` = studio CAPM Ke. Book = latest reported book equity. Clean NI (flag one-offs). If every `RI_t` is ≤ 0, **skip** — the bar equals the replacement book floor.

Do **not** treat SBC as a free add-back here. Treat SBC as a real cost.

## Output

If live: low / mid / high on the field. If skip: one line with the filing cite (no dividend; RI reprints book).

Write `artifacts/{TICKER}/03-models/yield.md` even on skip.
