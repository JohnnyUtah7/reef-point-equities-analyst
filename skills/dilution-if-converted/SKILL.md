---
name: dilution-if-converted
description: >
  Build the mandatory share-count / if-converted table before any $/share
  output. Use after studio statements exist, before the football field.
  Triggers: dilution, convertibles, if-converted, diluted shares, ATM, warrants.
version: "1.2.0"
---

# Dilution / if-converted

Studio DCF often prices on **cover shares**. Official `$/sh` uses the **value-relevant** count. Do not invent a second DCF — take studio equity value and re-divide.

## Sources (cite form / date / accession)

| Count | Where |
|---|---|
| Cover ordinary (+ class shares) | 10-K / 10-Q cover |
| Diluted WAS | Income statement (period average — not a spot count) |
| Converts, warrants, prepaid forwards | Debt / equity notes |
| Options / RSUs | Share-based payment note + diluted-EPS footnote |
| ATM / shelf remaining | Prospectus + subsequent 8-K / cover update |
| Conversion conditions met? | Convertible note (price tests, trading-price condition) |

Never reuse a remembered share count. Re-pull from `artifacts/{TICKER}/01-sec/`.

## Table (mandatory)

For each convertible / warrant / option tranche:

| Field | Rule |
|---|---|
| Principal / notional | Face, not carrying, for share math |
| Conversion / strike price | From the note |
| Shares if converted | `principal ÷ conversion price` |
| ITM vs last | `last > conversion price` **and** conditions met |
| Settle | Share (worse for holders) vs cash (no shares; cash leaves EV) |

**ITM if-converted count**

```
value_shares = cover_ordinary
             + ITM_convert_shares
             + treasury_method_option_shares
             + ITM_warrant_shares
             − prepaid_forward_offset   # only if notional sourced
```

**Treasury method (options / warrants)** — ITM only:

```
incremental_shares = n × (Px − strike) / Px
```

OTM paper stays in the table, **out** of `value_shares`, unless you are valuing at a price that puts them ITM (show that haircut on the bull bar).

## Equity-side add-back

If you assume **share settle** of ITM converts:

```
if_converted_equity = studio_equity_value + ITM_principal
$/sh = if_converted_equity / value_shares
```

If **cash settle**: no share add; subtract cash from equity. Label which you used. Default = share settle (conservative).

Carrying debt vs principal: keep studio net-debt on **carrying + unrestricted cash** unless the note says otherwise; document the principal gap as a sensitivity.

## ATM / shelf

`remaining_capacity = authorized − issued_under_prospectus` (cite the as-of cover date). Do **not** put the full shelf into `value_shares`. Flag as a soft kill on `$/sh` if the company is printing through a down tape.

## Checks

- [ ] Cover ≠ diluted WAS ≠ if-converted — all three shown
- [ ] Official field uses **one** diluted count on every bar
- [ ] Bull case re-tests OTM converts at the bull price
- [ ] Prepaid forwards / capped calls: sourced or `DATA_GAP`
- [ ] Studio `dcf.md` cover-share `$/sh` is **not** the published mid

## Outputs

```
artifacts/{TICKER}/01-sec/dilution_if_converted.md
```

DCF, comps, SOTP, memo, slides, and risk-audit **must** consume this artifact when present and label `$/sh` as basic vs FD.

## Do not

- Do not run a second EDGAR stack. Call `sec-filings`.
- Do not use diluted WAS as the spot count.
- Do not drop OTM paper from the table just because it is out of the count.
- Do not invent conversion rates, principal, or share counts.
