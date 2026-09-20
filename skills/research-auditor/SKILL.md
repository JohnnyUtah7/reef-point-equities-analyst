---
name: research-auditor
description: >
  Adversarial publish gate with hunt list and UNVERIFIED class. Run after the
  official memo draft, before Sheets/deck. Overlays studio risk-audit — does
  not replace it. Triggers: audit this research, fact-check, UNVERIFIED, risk audit.
---

# Research auditor

Studio `risk-audit` is the first gate and writes `artifacts/{TICKER}/04-research/risk_audit.md`. This overlay re-runs on the **official** note.

## Stance

Fresh context. Every figure is guilty until traced. You did not produce these numbers — do not rationalize them. “It sounds right” is not verification. Do not rewrite the thesis; find what is wrong.

## Hunt list (hardest-failure first)

1. **Fabricated / hallucinated** — revenue, margin, EPS, multiple, share count, quote, customer name that does not appear in `01-sec/`, `03-models/`, or a cited URL. Round or “remembered” numbers first.
2. **Stale / wrong period** — “latest quarter” that isn’t; FY vs calendar; TTM vs annual; pre/post split; price as-of mismatch.
3. **Unit / currency / scale** — thousands vs millions (10-K often in thousands), local vs USD, per-share vs total, bps vs %.
4. **Math re-derive** — growth, margins, EV bridge, DCF PV, blend weights, if-converted `$/sh`. Use `python3 -c`. Do not trust the stated result.
5. **Unsupported / overreach** — “X drove Y”, TAM, “market is missing…”, guidance stated as fact.
6. **Internal contradictions** — exec table vs field vs DCF sheet; rating vs field rule.
7. **Citation integrity** — does the cited 10-K/8-K actually say that? Spot-check 2–4 load-bearing cites against `01-sec/`.
8. **Method bias** — look-ahead, cherry-picked peers, circular ARR bars in the blend.

**Always**

9. **Dilution** — cover vs WAS vs if-converted; ATM freshness; ITM principal add-back.
10. **Circularity / TV** — circular bars have weight 0; TV as % of EV is written.

Verify **load-bearing** claims in full. Spot-check the rest. Say what you checked.

## Classes

| Class | Meaning |
|---|---|
| CRITICAL | Fabricated / wrong number the thesis or rating rests on |
| MAJOR | Material error that does not by itself sink the rating |
| MINOR | Scale, wording, stale as-of on a non-load-bearing figure |
| **UNVERIFIED** | Could not confirm either way — **not** CONFIRMED, **not** a fabrication. Name the source that would settle it |

## Verdict

```
VERDICT: PASS | PASS_WITH_FIXES | FAIL
SUMMARY: 2–3 sentences + single biggest risk

CRITICAL:
MAJOR:
MINOR:
UNVERIFIED:
CHECKED: … · SAMPLED: … · NOT CHECKED: …
```

- **FAIL** if any CRITICAL exists (or a recommendation built on bad data).
- **PASS_WITH_FIXES** if only MAJOR / MINOR remain, **or** you ran out of sources — never a false PASS.
- **PASS** only if load-bearing claims were actively verified and nothing material remains.

**Do not publish** the official memo, Sheets, or deck on `FAIL` without an explicit user override.

## Output

Write `artifacts/{TICKER}/04-research/hub_audit.md`. If you change the official memo, add an **audit-pass** block at the bottom (what changed and why). Do **not** change a locked official rating unless this audit finds a new CRITICAL in that file.
