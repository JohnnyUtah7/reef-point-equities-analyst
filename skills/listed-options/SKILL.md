---
name: listed-options
description: >
  A simple listed-options picture after the valuation. Black-Scholes premium,
  breakeven, delta, and a payoff chart. Bull: long call and cash-secured short
  put. Bear: long put. Not a second valuation.
---

# Listed options

Run this after the football field, on the same page as the research site. One picture, usually **two to four months** out (about 60–120 days), not a one-year leap. Robinhood-simple on the trade: one or two contracts, premium, breakeven, max loss. The chart is the loud part. Do not build a vol surface, a greek ladder, or a multi-leg book.

## Inputs

Spot is the same last price as the memo. Strike, days (default **90**), rate, dividend yield, implied vol.

If implied vol is not from a dated option chain, label it **assumption**. Do not invent a print and call it the market.

```
d1 = (ln(S/K) + (r − q + σ²/2) T) / (σ √T)
d2 = d1 − σ √T
call = S e^{−qT} N(d1) − K e^{−rT} N(d2)
put  = K e^{−rT} N(−d2) − S e^{−qT} N(−d1)
```

Show premium, breakeven, delta, and max loss. Max loss on a long option is the premium. Max loss on a cash-secured short put is the strike minus the premium, times shares, and you say that.

## Which trades

- **Bull** (the default): one long call and one cash-secured short put, about 90 days out, struck off the bull path. 
- **Bear** (only if the user said bear): one long put, about 90 days out, struck off the downside case. That is the attack. Do not sell puts on a bear case.

The chart is the section. A filled payoff: green above zero, red below, last price, breakeven, and a slider that drags the expiration price along the curve. Price on the x-axis, profit per share on the y-axis. Max loss on the card is per contract (×100), not a bare per-share number that looks like the whole trade.

## Do not

- Do not let the option premium change the stock Buy/Hold/Sell.
- Do not sell puts when the cover is the bear case.
- Do not add a vol surface or a dozen strikes.
