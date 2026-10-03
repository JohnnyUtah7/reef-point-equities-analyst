---
name: scenario-sensitivity
description: >
  Bull / base / bear, tornado, two-way WACC×g. Center of the 5×5 is the base DCF.
---

# Scenario / sensitivity

Write `artifacts/{TICKER}/03-models/sensitivity.md`.

- Three cases: bear / base / bull with **mechanisms**, not ±10% haircuts alone.
- Odd 5×5 WACC × g; **center = base**.
- Optional: growth × margin, β × rf.
- Each cell is a full DCF, not a linear interpolation.
- Tornado: the five drivers that actually move `$/sh`.

Bull must re-test OTM converts at the bull price (see dilution skill).
