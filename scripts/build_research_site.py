#!/usr/bin/env python3
"""Write the research site. The page is the product.

  python3 scripts/build_research_site.py artifacts/IREN/03-models/site.json

Bull cover unless stance is bear. Knobs cannot explode the draft.
A bull price that sits far above the bars is pinned, not used as the axis.
Options are a few months out, with a filled payoff chart.
"""
from __future__ import annotations

import html
import json
import math
import sys
from pathlib import Path

REQUIRED = ("ticker", "rating", "target", "last", "base", "methods")
BASE_KEYS = ("growth", "margin", "capex", "wacc", "g", "multiple", "dilution")


def load_spec(path: Path) -> dict:
    spec = json.loads(path.read_text())
    missing = [key for key in REQUIRED if key not in spec]
    if missing:
        raise SystemExit(f"site spec missing {', '.join(missing)}")
    rating = str(spec["rating"]).upper()
    if rating not in {"BUY", "HOLD", "SELL"}:
        raise SystemExit(f"rating must be BUY, HOLD, or SELL, got {spec['rating']}")
    spec["rating"] = rating
    for key in BASE_KEYS:
        if key not in spec["base"]:
            raise SystemExit(f"base missing {key}")
    return spec


def open_view(spec: dict) -> dict:
    """Cover is the bull case unless the user said bear. A low DCF is the kill.

    Asset floors do not become the cover price. If no bull price is sourced,
    set target_open and the chip stays HOLD · target open.
    """
    last = float(spec["last"])
    model_target = float(spec["target"])
    model_rating = spec["rating"]
    bear = str(spec.get("stance") or "bull").lower() == "bear" or spec.get("user_said_bear") is True
    if spec.get("target_open"):
        return {
            "lead": "bear" if bear else "bull",
            "rating": "SELL" if bear else "HOLD",
            "target": None,
            "target_open": True,
            "kill_rating": "BUY" if bear else "SELL",
            "kill_target": None,
            "kill_open": True,
            "headline": spec.get("headline") or ("Bear case" if bear else "12-month bull case"),
            "story": spec.get("story") or (
                "The operating case is on the page. A dollar target is not, until the multiple and the share count are sourced."
            ),
        }
    highs = [
        float(m["hi"])
        for m in spec["methods"]
        if not m.get("circular") and not m.get("floor")
    ]
    field_high = max(highs) if highs else model_target
    bull = float(spec["bull_target"]) if spec.get("bull_target") is not None else field_high
    kill = float(spec["kill_target"]) if spec.get("kill_target") is not None else model_target
    if bear:
        return {
            "lead": "bear",
            "rating": "SELL",
            "target": kill,
            "target_open": False,
            "kill_rating": "BUY",
            "kill_target": bull,
            "kill_open": False,
            "headline": spec.get("headline") or "Bear case",
            "story": spec.get("story") or "Why the downside is the case, and how a put attacks it.",
        }
    if spec.get("cover_rating"):
        rating = str(spec["cover_rating"]).upper()
    elif bull > last:
        rating = "BUY"
    else:
        rating = "HOLD"
    if rating == "SELL":
        rating = "HOLD"
    return {
        "lead": "bull",
        "rating": rating,
        "target": bull,
        "target_open": False,
        "kill_rating": "SELL" if model_rating == "SELL" else str(spec.get("kill_rating") or "SELL"),
        "kill_target": kill,
        "kill_open": False,
        "headline": spec.get("headline") or "12-month bull case",
        "story": spec.get("story") or "What has to happen over the next year, and the price if it does.",
    }


def _clamp_ratio(base: float, knob: float, invert: bool = False) -> float:
    if base <= 0 or knob <= 0:
        return 1.0
    raw = (base / knob) if invert else (knob / base)
    return max(0.75, min(1.25, raw))


def draft_price(spec: dict, knobs: dict):
    """Base knobs reprint the cover price. The product of the knobs stays inside 0.7x–1.45x.

    An open target has no draft dollar.
    """
    view = open_view(spec)
    if view.get("target_open"):
        return None
    base = spec["base"]
    factor = (
        _clamp_ratio(float(base["growth"]), float(knobs["growth"]))
        * _clamp_ratio(float(base["margin"]), float(knobs["margin"]))
        * _clamp_ratio(float(base["capex"]), float(knobs["capex"]), invert=True)
        * _clamp_ratio(float(base["wacc"]), float(knobs["wacc"]), invert=True)
        * _clamp_ratio(float(base["g"]), float(knobs["g"]))
        * _clamp_ratio(float(base["multiple"]), float(knobs["multiple"]))
    )
    factor = max(0.7, min(1.45, factor))
    dilution = float(knobs.get("dilution") or 0)
    factor *= 1.0 / (1.0 + max(dilution, 0) / 100.0)
    return round(view["target"] * factor, 2)


def _cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def black_scholes(spot: float, strike: float, years: float, rate: float, div: float, vol: float, kind: str) -> dict:
    kind = "call" if kind == "call" else "put"
    if years <= 0 or vol <= 0 or spot <= 0 or strike <= 0:
        intrinsic = max(spot - strike, 0) if kind == "call" else max(strike - spot, 0)
        return {"premium": round(intrinsic, 2), "delta": 0.5, "breakeven": round(strike + intrinsic if kind == "call" else strike - intrinsic, 2)}
    d1 = (math.log(spot / strike) + (rate - div + 0.5 * vol * vol) * years) / (vol * math.sqrt(years))
    d2 = d1 - vol * math.sqrt(years)
    disc_r = math.exp(-rate * years)
    disc_q = math.exp(-div * years)
    if kind == "call":
        premium = spot * disc_q * _cdf(d1) - strike * disc_r * _cdf(d2)
        delta = disc_q * _cdf(d1)
        breakeven = strike + premium
    else:
        premium = strike * disc_r * _cdf(-d2) - spot * disc_q * _cdf(-d1)
        delta = disc_q * (_cdf(d1) - 1.0)
        breakeven = strike - premium
    return {"premium": round(max(premium, 0.01), 2), "delta": round(delta, 2), "breakeven": round(breakeven, 2)}


def option_book(spec: dict, view: dict) -> dict:
    spot = float(spec.get("spot") or spec["last"])
    days = int(spec.get("days") or 90)
    years = days / 365.0
    rate = float(spec.get("rate") or 0.04)
    div = float(spec.get("div_yield") or 0.0)
    assumed = spec.get("iv") is None
    vol = float(spec["iv"]) if spec.get("iv") is not None else 0.35
    multiplier = 100

    def pack(name, side, kind, strike, quote):
        per_share = quote["premium"] if side == "long" else round(strike - quote["premium"], 2)
        return {
            "name": name,
            "side": side,
            "kind": kind,
            "strike": strike,
            **quote,
            "max_loss": per_share,
            "max_loss_contract": round(per_share * multiplier, 2),
        }

    if view["lead"] == "bear":
        strike = float(spec.get("put_strike") or round(spot * 0.95, 2))
        put = black_scholes(spot, strike, years, rate, div, vol, "put")
        return {"days": days, "vol": vol, "assumed": assumed, "multiplier": multiplier, "trades": [pack("Long put", "long", "put", strike, put)]}
    call_k = float(spec.get("call_strike") or round(spot * 1.05, 2))
    put_k = float(spec.get("put_strike") or round(spot * 0.90, 2))
    call = black_scholes(spot, call_k, years, rate, div, vol, "call")
    put = black_scholes(spot, put_k, years, rate, div, vol, "put")
    return {
        "days": days,
        "vol": vol,
        "assumed": assumed,
        "multiplier": multiplier,
        "trades": [
            pack("Long call", "long", "call", call_k, call),
            pack("Cash-secured put", "short", "put", put_k, put),
        ],
    }


def out_path(spec: dict, spec_path: Path) -> Path:
    parts = spec_path.resolve().parts
    root = Path(*parts[: parts.index("artifacts")]) if "artifacts" in parts else spec_path.resolve().parent
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    return docs / f"{spec['ticker'].lower()}-reef-point-live.html"


def _esc(value) -> str:
    return html.escape(str(value), quote=True)


def _px(value) -> str:
    if value is None:
        return "open"
    number = float(value)
    sign = "-" if number < 0 else ""
    number = abs(number)
    if abs(number - round(number)) < 1e-9:
        body = f"{int(round(number)):,}"
    else:
        body = f"{number:,.2f}"
    return f"{sign}${body}"


def _chip(view_key_rating: str, value, open_flag: bool) -> str:
    if open_flag or value is None:
        return f"{view_key_rating} · target open" if "Kill" not in view_key_rating else f"{view_key_rating} · open"
    return f"{view_key_rating} · {_px(value)}"


def _table(items, keys, headers) -> str:
    if not items:
        return "<p class=\"note\">Nothing sourced for this table.</p>"
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body = []
    for item in items:
        cells = "".join(f"<td>{_esc(item.get(k, ''))}</td>" for k in keys)
        body.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def _ticks(axis_hi: float) -> list[float]:
    if axis_hi <= 0:
        return [0.0]
    raw = axis_hi / 4.0
    mag = 10 ** math.floor(math.log10(raw))
    nice = 10 * mag
    for step in (1, 2, 2.5, 5, 10):
        if raw <= step * mag:
            nice = step * mag
            break
    ticks = []
    value = 0.0
    while value <= axis_hi + nice * 0.01:
        ticks.append(round(value, 4))
        value += nice
        if len(ticks) > 8:
            break
    return ticks


def _on_axis(value, axis_hi: float) -> bool:
    if value is None:
        return False
    return 0 <= float(value) <= axis_hi + 1e-9


def field_svg(methods, last, cover, kill) -> str:
    """Scale to the bars and the last price. A bull price above that scale is pinned."""
    last_f = float(last)
    cover_f = None if cover is None else float(cover)
    kill_f = None if kill is None else float(kill)
    bar_vals = [last_f]
    for method in methods:
        bar_vals.extend((float(method["lo"]), float(method["hi"])))
    axis_hi = (max(bar_vals) * 1.08) if bar_vals else 1.0
    if axis_hi <= 0:
        axis_hi = 1.0
    off_cover = cover_f is not None and not _on_axis(cover_f, axis_hi)
    off_kill = kill_f is not None and not _on_axis(kill_f, axis_hi)
    label_w, plot, gutter, top, rh = 156, 500, 108, 36, 44
    w = label_w + plot + gutter
    h = top + max(len(methods), 1) * rh + 32

    def x(value: float) -> float:
        return label_w + (float(value) / axis_hi) * plot

    font = 'font-family="Open Sans, Helvetica, Arial, sans-serif"'
    parts = [
        f'<svg class="field" viewBox="0 0 {w} {h}" role="img" aria-label="Football field of valuation methods" '
        f'data-axis-hi="{axis_hi:.4f}" data-off-cover="{1 if off_cover else 0}" {font}>',
        f'<rect x="{label_w}" y="{top - 8}" width="{plot}" height="{h - top - 16}" fill="#FAFAFA"/>',
    ]
    for tick in _ticks(axis_hi):
        if tick > axis_hi:
            continue
        parts.append(
            f'<line x1="{x(tick):.1f}" y1="{top - 8}" x2="{x(tick):.1f}" y2="{h - 24}" stroke="#E5E7EB"/>'
            f'<text x="{x(tick):.1f}" y="{h - 8}" text-anchor="middle" font-size="11" fill="#6B7280">{_px(tick)}</text>'
        )
    for i, method in enumerate(methods):
        y = top + i * rh
        lo, hi, mid = float(method["lo"]), float(method["hi"]), float(method["mid"])
        color = "#9CA3AF" if method.get("circular") or method.get("floor") else ("#047857" if mid >= last_f else "#B91C1C")
        dash = ' stroke="#6B7280" stroke-width="1" stroke-dasharray="4 3"' if method.get("circular") else ""
        x0, x1 = x(lo), x(hi)
        if x1 - x0 < 8:
            mid_x = (x0 + x1) / 2
            x0, x1 = mid_x - 4, mid_x + 4
        width = max(x1 - x0, 2)
        parts.append(
            f'<text x="{label_w - 10}" y="{y + 16}" text-anchor="end" font-size="12">{_esc(method["name"])}</text>'
            f'<rect data-name="{_esc(method["name"])}" x="{x0:.1f}" y="{y + 6}" width="{width:.1f}" height="16" fill="{color}" fill-opacity="0.9"{dash}/>'
            f'<line x1="{x(mid):.1f}" y1="{y + 3}" x2="{x(mid):.1f}" y2="{y + 25}" stroke="#0A0A0A" stroke-width="2"/>'
        )
        shown = _px(mid) if abs(hi - lo) < 0.5 else f"{_px(lo)}–{_px(hi)}"
        text_x = x1 + 8
        anchor = "start"
        if text_x + 6.4 * len(shown) > label_w + plot - 4:
            text_x = max(label_w + 4, x0 - 8)
            anchor = "end"
        parts.append(
            f'<text x="{text_x:.1f}" y="{y + 18}" text-anchor="{anchor}" font-size="11" fill="#6B7280">{shown}</text>'
        )
    parts.append(
        f'<line x1="{x(last_f):.1f}" y1="16" x2="{x(last_f):.1f}" y2="{h - 24}" stroke="#0A0A0A"/>'
        f'<text x="{x(last_f):.1f}" y="12" text-anchor="middle" font-size="11">Last {_px(last_f)}</text>'
    )
    if kill_f is not None and not off_kill:
        parts.append(
            f'<line x1="{x(kill_f):.1f}" y1="16" x2="{x(kill_f):.1f}" y2="{h - 24}" stroke="#B91C1C" stroke-dasharray="3 3"/>'
        )
    if cover_f is not None and not off_cover:
        parts.append(
            f'<line x1="{x(cover_f):.1f}" y1="16" x2="{x(cover_f):.1f}" y2="{h - 24}" stroke="#047857" stroke-width="2"/>'
            f'<text x="{min(x(cover_f), label_w + plot - 4):.1f}" y="{h - 8}" text-anchor="end" font-size="11" fill="#047857">Bull {_px(cover_f)}</text>'
        )
    if off_cover:
        parts.append(
            f'<text x="{label_w + plot + 10}" y="{top + 18}" font-size="12" font-weight="700" fill="#047857">Bull {_px(cover_f)}</text>'
            f'<text x="{label_w + plot + 10}" y="{top + 34}" font-size="11" fill="#047857">off chart</text>'
        )
    if off_kill:
        parts.append(
            f'<text x="{label_w + plot + 10}" y="{top + 58}" font-size="12" font-weight="700" fill="#B91C1C">Kill {_px(kill_f)}</text>'
            f'<text x="{label_w + plot + 10}" y="{top + 74}" font-size="11" fill="#B91C1C">off chart</text>'
        )
    if cover_f is None:
        parts.append(
            f'<text x="{label_w + plot + 10}" y="{top + 18}" font-size="12" font-weight="700">Bull</text>'
            f'<text x="{label_w + plot + 10}" y="{top + 34}" font-size="11" fill="#6B7280">$/sh open</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def render(spec: dict) -> str:
    view = open_view(spec)
    book = option_book(spec, view)
    field = field_svg(spec["methods"], spec["last"], view["target"], view["kill_target"])
    payload = json.dumps({
        "rating": view["rating"],
        "target": view["target"],
        "target_open": bool(view.get("target_open")),
        "last": float(spec["last"]),
        "base": spec["base"],
        "lead": view["lead"],
        "book": book,
        "peers": spec.get("peers") or [],
        "revenue_m": spec.get("revenue_m"),
        "shares_m": spec.get("shares_m"),
    })
    vol_note = "IV is an assumption, not the listed chain" if book["assumed"] else "IV from the spec"
    cards = []
    for trade in book["trades"]:
        cards.append(
            f'<article class="opt"><h3>{_esc(trade["name"])}</h3>'
            f'<p class="px">{_px(trade["premium"])} <span>/ share</span></p>'
            f'<p>Δ {trade["delta"]:.2f} · breakeven {_px(trade["breakeven"])}</p>'
            f'<p>Max loss {_px(trade["max_loss_contract"])} / contract</p>'
            f'<p class="note">{book["days"]} days · K {_px(trade["strike"])} · {vol_note} · {book["vol"]:.0%}</p></article>'
        )
    peers = spec.get("peers") or []
    quarters = spec.get("quarters") or []
    deals = spec.get("deals") or []
    assets = spec.get("assets") or []
    facts = spec.get("facts") or []
    fact_html = ""
    if facts:
        cells = "".join(
            f'<div><b>{_esc(item.get("v",""))}</b><span>{_esc(item.get("k",""))}</span></div>'
            for item in facts
        )
        fact_html = f'<div class="facts">{cells}</div>'
    sources = spec.get("sources") or []
    source_html = ""
    if sources:
        items = "".join(f"<li>{_esc(item)}</li>" for item in sources)
        source_html = f"<h2>Sources</h2><ul class=\"note\">{items}</ul>"
    field_note = spec.get("field_note") or "Bars and the last price set the scale. A bull price above that scale is marked off chart."
    published = _chip(view["rating"], view["target"], view.get("target_open"))
    kill_chip = _chip(f"Kill {view['kill_rating']}", view["kill_target"], view.get("kill_open"))
    draft = "Draft · open" if view.get("target_open") else f"Draft · {_px(view['target'])}"
    slider_max = max(float(spec["last"]) * 1.8, float(view["target"]) * 1.25) if view.get("target") else float(spec["last"]) * 1.8
    if view.get("target_open"):
        scenario_html = (
            "<h2>Your scenario</h2>"
            "<p class=\"note\">No locked price, so there is no draft slider. A slider here would print a second model.</p>"
        )
    else:
        scenario_html = """<h2>Your scenario</h2>
  <div class="row">
    <button type="button" data-preset="bear">Bear</button>
    <button type="button" data-preset="base">Base</button>
    <button type="button" data-preset="bull">Bull</button>
    <button type="button" id="reset">Reset</button>
  </div>
  <label>Growth <output id="v-growth"></output><input id="growth" type="range" min="0" max="80" step="0.5"/></label>
  <label>Margin <output id="v-margin"></output><input id="margin" type="range" min="0" max="80" step="0.5"/></label>
  <label>Capex <output id="v-capex"></output><input id="capex" type="range" min="0" max="80" step="0.5"/></label>
  <label>Discount rate <output id="v-wacc"></output><input id="wacc" type="range" min="4" max="20" step="0.1"/></label>
  <label>Terminal growth <output id="v-g"></output><input id="g" type="range" min="0" max="6" step="0.1"/></label>
  <label>Multiple <output id="v-multiple"></output><input id="multiple" type="range" min="0" max="40" step="0.1"/></label>
  <label>Dilution % <output id="v-dilution"></output><input id="dilution" type="range" min="0" max="40" step="0.5"/></label>
  <p class="note" id="knobNote">The published chip does not move. Draft stays within 0.7× to 1.45× of that price.</p>"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{_esc(spec['ticker'])} — Equities Valuation</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap"/>
<style>
  :root {{ --ink:#0A0A0A; --muted:#6B7280; --line:#E5E7EB; --up:#047857; --down:#B91C1C; --font:"Open Sans",Helvetica,Arial,sans-serif; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:#fff; color:var(--ink); font:15px/1.45 var(--font); }}
  header, main {{ max-width:1040px; margin:0 auto; padding:28px 20px; }}
  header {{ border-top:3px solid var(--ink); }}
  h1 {{ font-size:28px; letter-spacing:-0.03em; margin:0 0 6px; }}
  h2 {{ font-size:13px; letter-spacing:0.14em; text-transform:uppercase; color:var(--muted); margin:28px 0 10px; }}
  .sub {{ color:var(--muted); margin:0 0 16px; }}
  .row {{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }}
  .chip {{ border:1px solid var(--ink); padding:8px 12px; font-weight:700; }}
  .chip.kill {{ color:var(--down); border-color:var(--down); }}
  nav button, .subnav button, button {{ border:1px solid var(--ink); background:#fff; padding:8px 12px; font:inherit; cursor:pointer; }}
  nav button[aria-pressed="true"], .subnav button[aria-pressed="true"] {{ background:#0A0A0A; color:#fff; }}
  section[hidden], .pane[hidden] {{ display:none; }}
  .story {{ font-size:18px; max-width:44rem; }}
  .facts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); border-top:1px solid var(--line); border-bottom:1px solid var(--line); margin:18px 0 8px; }}
  .facts div {{ padding:12px 14px 12px 0; }}
  .facts b {{ display:block; font-size:18px; letter-spacing:-0.02em; }}
  .facts span {{ color:var(--muted); font-size:12px; }}
  .panel {{ border:1px solid var(--line); padding:8px 8px 0; margin-top:8px; overflow-x:auto; }}
  table {{ width:100%; border-collapse:collapse; }}
  th, td {{ border-bottom:1px solid var(--line); text-align:left; padding:8px 4px; vertical-align:top; }}
  .field {{ width:100%; height:auto; }}
  label {{ display:block; margin:12px 0; color:var(--muted); font-size:13px; }}
  input[type=range] {{ width:100%; accent-color:#0A0A0A; }}
  .opts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
  .opt {{ border:1px solid var(--line); padding:12px; }}
  .opt h3 {{ margin:0 0 6px; font-size:15px; }}
  .opt .px {{ font-size:22px; font-weight:700; margin:0 0 6px; letter-spacing:-0.03em; }}
  .opt .px span {{ font-size:13px; font-weight:400; color:var(--muted); }}
  .chart {{ width:100%; height:auto; background:#fff; border:1px solid var(--line); }}
  .note {{ color:var(--muted); font-size:12px; }}
  ul.note {{ padding-left:18px; }}
  @media (max-width:640px) {{
    h1 {{ font-size:22px; }}
    header, main {{ padding:20px 14px; }}
    .story {{ font-size:16px; }}
  }}
</style>
</head>
<body>
<header>
  <p class="note">REEF POINT · EQUITIES VALUATION</p>
  <h1>{_esc(spec.get('name') or spec['ticker'])} · {_esc(spec['ticker'])}</h1>
  <p class="sub">{_esc(spec.get('asof',''))} · last {_px(spec['last'])} · {_esc(spec.get('disclaimer','Draft view — not investment advice.'))}</p>
  <div class="row">
    <span class="chip" id="published">{_esc(published)}</span>
    <span class="chip kill">{_esc(kill_chip)}</span>
    <span class="chip" id="draft">{_esc(draft)}</span>
  </div>
  {fact_html}
</header>
<main>
  <nav class="row">
    <button type="button" data-tab="exec" aria-pressed="true">Exec</button>
    <button type="button" data-tab="val" aria-pressed="false">Valuation</button>
    <button type="button" data-tab="res" aria-pressed="false">Research</button>
    <button type="button" data-tab="opt" aria-pressed="false">Options</button>
  </nav>
  <section id="exec">
    <h2>{_esc(view['headline'])}</h2>
    <p class="story">{_esc(view['story'])}</p>
    <div class="panel">{field}</div>
    <p class="note">{_esc(field_note)}</p>
  </section>
  <section id="val" hidden>
    <div class="subnav row">
      <button type="button" data-pane="field" aria-pressed="true">Field</button>
      <button type="button" data-pane="comps" aria-pressed="false">Comps</button>
      <button type="button" data-pane="txns" aria-pressed="false">Precedents</button>
      <button type="button" data-pane="assets" aria-pressed="false">Assets</button>
    </div>
    <div class="pane" data-pane="field"><div class="panel">{field}</div><p class="note">{_esc(field_note)}</p></div>
    <div class="pane" data-pane="comps" hidden>
      <p>{_esc(spec.get('comps_note') or 'Researched peers. A toggle moves the draft multiple, not the published call.')}</p>
      <div id="peers"></div>
      <p>Draft comps <b id="compsOut">—</b></p>
    </div>
    <div class="pane" data-pane="txns" hidden>
      {_table(deals, ('name','status','note'), ('Deal','Status','Note'))}
    </div>
    <div class="pane" data-pane="assets" hidden>
      {_table(assets, ('layer','ps','note'), ('Layer','$ / sh','Note'))}
    </div>
  </section>
  <section id="res" hidden>
    <h2>By quarter</h2>
    <p class="note">What they said, what the next print showed, whether it was kept. This does not rate the name.</p>
    {_table(quarters, ('call','date','said','showed','kept'), ('Call','Date','They said','Next print','Kept?'))}
  </section>
  <section id="opt" hidden>
    <h2>Options · {book['days']} days</h2>
    <p class="note">One contract is 100 shares. The chart is profit per share at expiration. Premium does not change the stock call.</p>
    <div class="opts">{''.join(cards)}</div>
    <svg id="payoff" class="chart" viewBox="0 0 720 320" role="img" aria-label="Option payoff at expiration"></svg>
    <p class="note">Green is profit, red is loss, the solid mark is the last price, gray dashes are breakevens. Drag the expiration price.</p>
    <label>Stock price at expiration <output id="v-spot"></output>
      <input id="spot" type="range" min="{max(1, float(spec['last'])*0.45):.2f}" max="{slider_max:.2f}" step="0.5" value="{float(spec['last'])}"/>
    </label>
  </section>
  {scenario_html}
  {source_html}
</main>
<script>
const SPEC = {payload};
const published = document.getElementById("published");
function clampRatio(b, k, invert) {{
  if (b <= 0 || k <= 0) return 1;
  const raw = invert ? b / k : k / b;
  return Math.max(0.75, Math.min(1.25, raw));
}}
function draftPrice(knobs) {{
  if (SPEC.target_open) return null;
  let factor = clampRatio(SPEC.base.growth, knobs.growth) * clampRatio(SPEC.base.margin, knobs.margin)
    * clampRatio(SPEC.base.capex, knobs.capex, true) * clampRatio(SPEC.base.wacc, knobs.wacc, true)
    * clampRatio(SPEC.base.g, knobs.g) * clampRatio(SPEC.base.multiple, knobs.multiple);
  factor = Math.max(0.7, Math.min(1.45, factor));
  factor *= 1 / (1 + Math.max(+knobs.dilution, 0) / 100);
  return Math.round(SPEC.target * factor * 100) / 100;
}}
function readKnobs() {{
  const knobs = {{}};
  ["growth","margin","capex","wacc","g","multiple","dilution"].forEach(function (name) {{
    knobs[name] = +document.getElementById(name).value;
    document.getElementById("v-" + name).textContent = knobs[name];
  }});
  return knobs;
}}
function paint() {{
  if (SPEC.target_open || !document.getElementById("growth")) {{
    document.getElementById("draft").textContent = "Draft · open";
    published.textContent = SPEC.rating + " · target open";
    return;
  }}
  const knobs = readKnobs();
  document.getElementById("draft").textContent = "Draft · $" + draftPrice(knobs);
  published.textContent = SPEC.rating + " · $" + SPEC.target;
}}
function setKnobs(knobs) {{
  if (!document.getElementById("growth")) {{ paint(); return; }}
  Object.keys(SPEC.base).forEach(function (name) {{ document.getElementById(name).value = knobs[name]; }});
  paint();
}}
function preset(name) {{
  const b = Object.assign({{}}, SPEC.base);
  if (name === "bear") {{ b.growth *= 0.85; b.margin *= 0.9; b.wacc += 0.5; b.multiple *= 0.9; }}
  if (name === "bull") {{ b.growth *= 1.15; b.margin *= 1.08; b.wacc = Math.max(4, b.wacc - 0.5); b.multiple *= 1.1; }}
  setKnobs(b);
}}
document.querySelectorAll("nav button").forEach(function (btn) {{
  btn.addEventListener("click", function () {{
    document.querySelectorAll("nav button").forEach(function (b) {{ b.setAttribute("aria-pressed", b === btn ? "true" : "false"); }});
    ["exec","val","res","opt"].forEach(function (id) {{ document.getElementById(id).hidden = id !== btn.dataset.tab; }});
    if (btn.dataset.tab === "opt") drawPayoff();
  }});
}});
document.querySelectorAll(".subnav button").forEach(function (btn) {{
  btn.addEventListener("click", function () {{
    document.querySelectorAll(".subnav button").forEach(function (b) {{ b.setAttribute("aria-pressed", b === btn ? "true" : "false"); }});
    document.querySelectorAll("#val .pane").forEach(function (pane) {{ pane.hidden = pane.dataset.pane !== btn.dataset.pane; }});
  }});
}});
document.querySelectorAll("#growth,#margin,#capex,#wacc,#g,#multiple,#dilution").forEach(function (el) {{ el.addEventListener("input", paint); }});
document.querySelectorAll("[data-preset]").forEach(function (btn) {{ btn.addEventListener("click", function () {{ preset(btn.dataset.preset); }}); }});
const resetBtn = document.getElementById("reset");
if (resetBtn) resetBtn.addEventListener("click", function () {{ setKnobs(SPEC.base); }});
const peers = document.getElementById("peers");
(SPEC.peers || []).forEach(function (peer) {{
  const label = document.createElement("label");
  const box = document.createElement("input");
  box.type = "checkbox";
  box.checked = !!peer.default && peer.ps != null;
  box.disabled = peer.ps == null;
  box.dataset.ps = peer.ps == null ? "nm" : String(peer.ps);
  box.addEventListener("change", function () {{
    const on = [];
    document.querySelectorAll("#peers input").forEach(function (el) {{ if (el.checked && el.dataset.ps !== "nm") on.push(+el.dataset.ps); }});
    on.sort(function (a,b) {{ return a-b; }});
    const out = document.getElementById("compsOut");
    if (!on.length) {{ out.textContent = "—"; return; }}
    const med = on.length % 2 ? on[(on.length-1)/2] : (on[on.length/2-1] + on[on.length/2]) / 2;
    out.textContent = med.toFixed(1) + "×";
  }});
  label.appendChild(box);
  label.appendChild(document.createTextNode(" " + peer.ticker + " " + (peer.ps == null ? "NM" : peer.ps + "×")));
  peers.appendChild(label);
}});
function pnl(trade, s) {{
  const intrinsic = trade.kind === "call" ? Math.max(s - trade.strike, 0) : Math.max(trade.strike - s, 0);
  return trade.side === "short" ? trade.premium - intrinsic : intrinsic - trade.premium;
}}
function drawPayoff() {{
  const svg = document.getElementById("payoff");
  const spot = +document.getElementById("spot").value;
  document.getElementById("v-spot").textContent = "$" + spot.toFixed(2);
  const min = +document.getElementById("spot").min;
  const max = +document.getElementById("spot").max;
  const trades = SPEC.book.trades;
  const pts = [];
  for (let i = 0; i <= 80; i++) {{
    const s = min + (max - min) * i / 80;
    let y = 0;
    trades.forEach(function (t) {{ y += pnl(t, s); }});
    pts.push([s, y]);
  }}
  const ys = pts.map(function (p) {{ return p[1]; }});
  let yMin = Math.min(0, Math.min.apply(null, ys));
  let yMax = Math.max(0, Math.max.apply(null, ys));
  if (yMax - yMin < 1) {{ yMax += 1; yMin -= 1; }}
  const W = 720, H = 320, L = 56, R = 18, T = 28, B = 36;
  function X(s) {{ return L + (s - min) / (max - min) * (W - L - R); }}
  function Y(v) {{ return T + (yMax - v) / (yMax - yMin || 1) * (H - T - B); }}
  const zero = Y(0);
  function cross(a, b) {{
    const t = (0 - a[1]) / (b[1] - a[1]);
    return [a[0] + (b[0] - a[0]) * t, 0];
  }}
  const pieces = [];
  let run = [pts[0]];
  for (let i = 1; i < pts.length; i++) {{
    const a = pts[i - 1], b = pts[i];
    const split = (a[1] >= 0 && b[1] < 0) || (a[1] < 0 && b[1] >= 0);
    if (split && a[1] !== b[1]) {{
      const z = cross(a, b);
      run.push(z);
      pieces.push(run);
      run = [z, b];
    }} else {{
      run.push(b);
    }}
  }}
  pieces.push(run);
  let fills = "";
  pieces.forEach(function (piece) {{
    const mid = piece[Math.floor(piece.length / 2)][1];
    const color = mid >= 0 ? "#047857" : "#B91C1C";
    let d = "M" + X(piece[0][0]).toFixed(1) + " " + zero.toFixed(1);
    piece.forEach(function (p) {{ d += "L" + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1); }});
    d += "L" + X(piece[piece.length - 1][0]).toFixed(1) + " " + zero.toFixed(1) + "Z";
    fills += '<path d="' + d + '" fill="' + color + '" fill-opacity="0.2" stroke="none"/>';
  }});
  let line = "";
  pts.forEach(function (p, i) {{ line += (i ? "L" : "M") + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1); }});
  const here = trades.reduce(function (sum, t) {{ return sum + pnl(t, spot); }}, 0);
  const color = here >= 0 ? "#047857" : "#B91C1C";
  let marks = "";
  trades.forEach(function (t) {{
    if (t.breakeven >= min && t.breakeven <= max) {{
      marks += '<line x1="' + X(t.breakeven).toFixed(1) + '" y1="' + T + '" x2="' + X(t.breakeven).toFixed(1) + '" y2="' + (H - B) + '" stroke="#9CA3AF" stroke-dasharray="2 3"/>';
    }}
  }});
  function money(v) {{
    const sign = v < 0 ? "-" : "";
    return sign + "$" + Math.abs(v).toFixed(0);
  }}
  const yLabels = [yMax, 0, yMin].map(function (v) {{
    return '<text x="' + (L - 8) + '" y="' + (Y(v) + 4) + '" text-anchor="end" font-size="11" fill="#6B7280">' + money(v) + '</text>';
  }}).join("");
  svg.setAttribute("data-pnl", here.toFixed(2));
  svg.innerHTML = yLabels
    + '<line x1="' + L + '" y1="' + zero.toFixed(1) + '" x2="' + (W - R) + '" y2="' + zero.toFixed(1) + '" stroke="#E5E7EB"/>'
    + fills
    + '<path d="' + line + '" fill="none" stroke="#0A0A0A" stroke-width="2.5"/>'
    + '<line x1="' + X(SPEC.last).toFixed(1) + '" y1="' + T + '" x2="' + X(SPEC.last).toFixed(1) + '" y2="' + (H - B) + '" stroke="#0A0A0A" stroke-dasharray="4 3"/>'
    + '<text x="' + X(SPEC.last).toFixed(1) + '" y="' + (H - 14) + '" text-anchor="middle" font-size="11" fill="#6B7280">Last</text>'
    + marks
    + '<circle cx="' + X(spot).toFixed(1) + '" cy="' + Y(here).toFixed(1) + '" r="7" fill="' + color + '" stroke="#fff" stroke-width="2"/>'
    + '<text x="' + X(spot).toFixed(1) + '" y="16" text-anchor="middle" font-size="13" font-weight="700" fill="' + color + '">' + (here >= 0 ? "+" : "-") + "$" + Math.abs(here).toFixed(2) + '</text>';
}}
document.getElementById("spot").addEventListener("input", drawPayoff);
setKnobs(SPEC.base);
drawPayoff();
</script>
</body>
</html>
"""


def build(spec_path: Path) -> Path:
    spec = load_spec(spec_path)
    view = open_view(spec)
    if not view.get("target_open"):
        echoed = draft_price(spec, spec["base"])
        if abs(echoed - float(view["target"])) > 0.02:
            raise SystemExit(f"base knobs draft {echoed} != cover {view['target']}")
    dest = out_path(spec, spec_path)
    dest.write_text(render(spec))
    return dest


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: python3 scripts/build_research_site.py artifacts/TICKER/03-models/site.json")
    print(build(Path(argv[1])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
