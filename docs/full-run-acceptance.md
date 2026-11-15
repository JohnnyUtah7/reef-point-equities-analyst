# Full-run acceptance

Use `analyze CTOS` as the live acceptance case. Do not publish a fixture as research.

1. Record the exact active plugin root and version; run `scripts/check_release.py`. Record installed cache separately if testing source.
2. Discover hosted EDGAR tools and verify CTOS lookup. Only use local edgartools when hosted tools are unavailable; local identity is not a hosted prerequisite.
3. Retrieve latest periodic filings and earnings exhibit; preserve accession and reporting period. Verify all three statements, financing notes and dilution before valuation.
4. Reconcile DCF, comps and segment values, reconcile the football field to the memo, and complete research audit.
5. Render the actual issuer spec; exercise desktop/mobile navigation, scenario controls, reset and source links. Synthetic renderer tests are a separate result.
6. Use the current Sites workflow. Reuse project_id on retries. Confirm terminal deployment success and return its actual URL.

Report each gate independently. Blocked filings do not justify invented multiples, shares or a forced HOLD. A diagnostic preview must be requested or clearly separated, labeled UNRATED, and must never be reported as a completed full run.

## CTOS diagnostic run, 2026-11-14

The loaded cache was 1.3.12; local source was 1.4.0; GitHub main was 1.3.16. Local SEC and Sites Git host DNS resolution failed, and hosted EDGAR tools were not exposed in that conversation. A read-only IR preview was generated; financial validation, browser QA and live publication were incomplete. No official rating or target was issued. This record is a failed live acceptance attempt, not an issuer research note.

GitHub source updates do not deploy the EDGAR Worker, update the plugin directory submission, or reload a session's installed cache. Those require separately verified actions in their respective services.
