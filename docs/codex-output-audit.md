# Research site v1.4.0 review — 25 October 2026

The user-supplied IREN artifact is the depth and interaction benchmark. The plugin now generates a company-independent financial terminal instead of a capped target-price multiplier.

Implemented: reconciled annual FCFF, source/period-tagged statement inputs, balance-sheet net-debt bridge, EBITDA and reported FCF cross-checks, DCF sensitivities and tornado, peer selection across four metrics, precedents, SOTP, book/PPE/replacement methods, editable non-circular blend weights, model-linked risks, statement tables, promise ledger and evidence views. Published recommendation is fixed; bull or bear is an exploratory thesis, never an automatic rating override.

Local checks pass: 11 Python renderer/regression tests, independent Node valuation arithmetic, and latest upstream EDGAR protocol tests. CI repeats these and exercises the generated synthetic HTML in Chromium at desktop/mobile sizes, saving screenshots. Consult the current PR check for its result; adding tests alone is not evidence they passed.

Release gates remain: visual comparison with the supplied artifact; a live SEC-data-to-site run with statement, forecast, dilution and memo reconciliation; native Sites publication and URL verification; install/refresh in Codex and verify loaded version. The session initially exposed 1.3.12. A source PR or ZIP does not update it.

Schema v2 migration is documented in references/research-site-schema.md. Missing models remain read-only. Existing legacy options payoff UI is not carried into this terminal; options research remains in its dedicated plugin skill. Sector-specific models such as LBO, residual income and dividend valuation may be supplied as disclosed static ranges; they are not advertised as recalculating with FCFF controls.

This is a software audit using explicitly synthetic fixtures, not a live stock recommendation or certification of financial sources. Source tags establish traceability; the analyst must still verify cited filings and normalization. No source identifiers or company values should be invented to satisfy schema checks.
