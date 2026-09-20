# IREN was the test run

Do **not** copy these figures onto another ticker.

Official Sell $28 note, earnings-call companion, and studio artifacts live in the Investment Research **project store**, not in this plugin:

- Official note: `docs/iren-equity-research.md`
- Calls: `docs/iren-earnings-calls.md`
- Pack: `artifacts/IREN/`

What the test proved: EDGAR pull → statements → DCF/comps/SOTP → house field (if-converted 423.80m, circular ARR weight 0) → Buy/Hold/Sell tightness.

What the test did **not** prove as a one-click product: Drive conversion (payload limits), canvas Publish (toolbar-only), X tape, a local `iren-model.xlsx` in docs/. Those are why 2.0.0 ships the memo **before** Sheets/deck and forbids per-skill cloud fan-out.
