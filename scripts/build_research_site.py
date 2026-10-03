#!/usr/bin/env python3
"""Write the research site. The page is the product.

  python3 scripts/build_research_site.py artifacts/IREN/03-models/site.json

Bull cover unless stance is bear. Knobs cannot explode the draft.
Options are a few months out, with a payoff chart.
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
    """Cover is the bull case unless the user said bear. A low DCF is the kill."""
    last = float(spec["last"])
    model_target = float(spec["target"])
    model_rating = spec["rating"]
    bear = str(spec.get("stance") or "bull").lower() == "bear" or spec.get("user_said_bear") is True
    highs = [float(m["hi"]) for m in spec["methods"] if not m.get("circular")]
    field_high = max(highs) if highs else model_target
    bull = float(spec["bull_target"]) if spec.get("bull_target") is not None else field_high
    kill = float(spec["kill_target"]) if spec.get("kill_target") is not None else model_target
    if bear:
        return {
            "lead": "bear",
            "rating": "SELL",
            "target": kill,
            "kill_rating": "BUY",
            "kill_target": bull,
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
        "kill_rating": "SELL" if model_rating == "SELL" else str(spec.get("kill_rating") or "SELL"),
        "kill_target": kill,
        "headline": spec.get("headline") or "12-month bull case",
        "story": spec.get("story") or "What has to happen over the next year, and the price if it does.",
    }


def _clamp_ratio(base: float, knob: float, invert: bool = False) -> float:
    if base <= 0 or knob <= 0:
        return 1.0
    raw = (base / knob) if invert else (knob / base)
    return max(0.75, min(1.25, raw))


def draft_price(spec: dict, knobs: dict) -> float:
    """Base knobs reprint the cover price. The product of the knobs stays inside 0.7x–1.45x."""
    view = open_view(spec)
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
    if view["lead"] == "bear":
        strike = float(spec.get("put_strike") or round(spot * 0.95, 2))
        put = black_scholes(spot, strike, years, rate, div, vol, "put")
        trade = {"name": "Long put", "side": "long", "kind": "put", "strike": strike, **put, "max_loss": put["premium"]}
        return {"days": days, "vol": vol, "assumed": assumed, "trades": [trade]}
    call_k = float(spec.get("call_strike") or round(spot * 1.05, 2))
    put_k = float(spec.get("put_strike") or round(spot * 0.90, 2))
    call = black_scholes(spot, call_k, years, rate, div, vol, "call")
    put = black_scholes(spot, put_k, years, rate, div, vol, "put")
    return {
        "days": days,
        "vol": vol,
        "assumed": assumed,
        "trades": [
            {"name": "Long call", "side": "long", "kind": "call", "strike": call_k, **call, "max_loss": call["premium"]},
            {"name": "Cash-secured put", "side": "short", "kind": "put", "strike": put_k, **put, "max_loss": round(put_k - put["premium"], 2)},
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


def _table(items, keys, headers) -> str:
    head = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body = []
    for item in items:
        cells = "".join(f"<td>{_esc(item.get(k, ''))}</td>" for k in keys)
        body.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def field_svg(methods, last, cover, kill) -> str:
    vals = [float(m["lo"]) for m in methods] + [float(m["hi"]) for m in methods] + [float(last), float(cover), float(kill)]
    hi = max(vals) * 1.08 or 1
    lo = 0
    span = hi - lo
    w, label, plot, top, rh = 720, 132, 520, 36, 36
    h = top + len(methods) * rh + 28

    def x(v):
        return label + (float(v) - lo) / span * plot

    rows = []
    for i, m in enumerate(methods):
        y = top + i * rh + 8
        color = "#9CA3AF" if m.get("circular") else ("#047857" if float(m["mid"]) >= float(last) else "#B91C1C")
        dash = ' stroke-dasharray="4 3"' if m.get("circular") else ""
        rows.append(
            f'<text x="{label - 8}" y="{y + 12}" text-anchor="end" font-size="12">{_esc(m["name"])}</text>'
            f'<rect x="{x(m["lo"]):.1f}" y="{y}" width="{max(x(m["hi"]) - x(m["lo"]), 2):.1f}" height="14" fill="{color}" fill-opacity="0.85"{dash}/>'
            f'<line x1="{x(m["mid"]):.1f}" y1="{y - 2}" x2="{x(m["mid"]):.1f}" y2="{y + 16}" stroke="#0A0A0A" stroke-width="2"/>'
        )
    marks = (
        f'<line x1="{x(last):.1f}" y1="18" x2="{x(last):.1f}" y2="{h - 22}" stroke="#0A0A0A"/>'
        f'<text x="{x(last):.1f}" y="14" text-anchor="middle" font-size="11">Last ${float(last):.0f}</text>'
        f'<line x1="{x(cover):.1f}" y1="18" x2="{x(cover):.1f}" y2="{h - 22}" stroke="#047857" stroke-width="2"/>'
        f'<text x="{x(cover):.1f}" y="{h - 6}" text-anchor="middle" font-size="11" fill="#047857">Bull ${float(cover):.0f}</text>'
    )
    return (
        f'<svg class="field" viewBox="0 0 {w} {h}" role="img" aria-label="Football field of valuation methods">'
        + "".join(rows) + marks + "</svg>"
    )


def render(spec: dict) -> str:
    view = open_view(spec)
    book = option_book(spec, view)
    field = field_svg(spec["methods"], spec["last"], view["target"], view["kill_target"])
    payload = json.dumps({
        "rating": view["rating"],
        "target": view["target"],
        "last": float(spec["last"]),
        "base": spec["base"],
        "lead": view["lead"],
        "book": book,
        "peers": spec.get("peers") or [],
        "revenue_m": spec.get("revenue_m"),
        "shares_m": spec.get("shares_m"),
    })
    vol_note = "IV is an assumption" if book["assumed"] else "IV from the spec"
    cards = []
    for trade in book["trades"]:
        cards.append(
            f'<article class="opt"><h3>{_esc(trade["name"])}</h3>'
            f'<p>${trade["premium"]:.2f} · Δ {trade["delta"]:.2f}</p>'
            f'<p>Breakeven ${_esc(trade["breakeven"])} · max loss ${_esc(trade["max_loss"])}</p>'
            f'<p class="note">{book["days"]} days · K {_esc(trade["strike"])} · {vol_note} {book["vol"]:.0%}</p></article>'
        )
    peers = spec.get("peers") or []
    quarters = spec.get("quarters") or []
    deals = spec.get("deals") or []
    assets = spec.get("assets") or []
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
  h1 {{ font-size:28px; letter-spacing:-0.03em; margin:0 0 6px; }}
  h2 {{ font-size:13px; letter-spacing:0.14em; text-transform:uppercase; color:var(--muted); margin:28px 0 10px; }}
  .sub {{ color:var(--muted); margin:0 0 16px; }}
  .row {{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }}
  .chip {{ border:1px solid var(--ink); padding:8px 12px; font-weight:700; }}
  .chip.kill {{ color:var(--down); border-color:var(--down); }}
  nav button, .subnav button, button {{ border:1px solid var(--ink); background:#fff; padding:8px 12px; font:inherit; cursor:pointer; }}
  nav button[aria-pressed="true"], .subnav button[aria-pressed="true"] {{ background:#0A0A0A; color:#fff; }}
  section[hidden], .pane[hidden] {{ display:none; }}
  .story {{ font-size:18px; max-width:42rem; }}
  table {{ width:100%; border-collapse:collapse; }}
  th, td {{ border-bottom:1px solid var(--line); text-align:left; padding:8px 4px; vertical-align:top; }}
  .field {{ width:100%; height:auto; }}
  label {{ display:block; margin:12px 0; color:var(--muted); font-size:13px; }}
  input[type=range] {{ width:100%; accent-color:#0A0A0A; }}
  .opts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
  .opt {{ border:1px solid var(--line); padding:12px; }}
  .opt h3 {{ margin:0 0 6px; }}
  .chart {{ width:100%; height:auto; background:#FAFAFA; border:1px solid var(--line); }}
  .note {{ color:var(--muted); font-size:12px; }}
</style>
</head>
<body>
<header>
  <p class="note">REEF POINT · EQUITIES VALUATION</p>
  <h1>{_esc(spec.get('name') or spec['ticker'])} · {_esc(spec['ticker'])}</h1>
  <p class="sub">{_esc(spec.get('asof',''))} · last ${_esc(spec['last'])} · {_esc(spec.get('disclaimer','Draft view — not investment advice.'))}</p>
  <div class="row">
    <span class="chip" id="published">{_esc(view['rating'])} · ${_esc(view['target'])}</span>
    <span class="chip kill">Kill {_esc(view['kill_rating'])} · ${_esc(view['kill_target'])}</span>
    <span class="chip" id="draft">Draft · ${_esc(view['target'])}</span>
  </div>
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
    {field}
  </section>
  <section id="val" hidden>
    <div class="subnav row">
      <button type="button" data-pane="field" aria-pressed="true">Field</button>
      <button type="button" data-pane="comps" aria-pressed="false">Comps</button>
      <button type="button" data-pane="txns" aria-pressed="false">Precedents</button>
      <button type="button" data-pane="assets" aria-pressed="false">Assets</button>
    </div>
    <div class="pane" data-pane="field">{field}</div>
    <div class="pane" data-pane="comps" hidden>
      <p>Researched peers. A toggle moves the draft multiple, not the published call.</p>
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
    <div class="opts">{''.join(cards)}</div>
    <svg id="payoff" class="chart" viewBox="0 0 720 280" role="img" aria-label="Option payoff at expiration"></svg>
    <label>Stock price at expiration <output id="v-spot"></output>
      <input id="spot" type="range" min="{max(1, float(spec['last'])*0.4):.2f}" max="{max(float(view['target'])*1.4, float(spec['last'])*1.8):.2f}" step="0.5" value="{float(spec['last'])}"/>
    </label>
  </section>
  <h2>Your scenario</h2>
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
  <p class="note">The published chip does not move. Draft stays within 0.7× to 1.45× of that price.</p>
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
  const knobs = readKnobs();
  document.getElementById("draft").textContent = "Draft · $" + draftPrice(knobs);
  published.textContent = SPEC.rating + " · $" + SPEC.target;
}}
function setKnobs(knobs) {{
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
document.getElementById("reset").addEventListener("click", function () {{ setKnobs(SPEC.base); }});
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
  for (let i = 0; i <= 48; i++) {{
    const s = min + (max - min) * i / 48;
    let y = 0;
    trades.forEach(function (t) {{ y += pnl(t, s); }});
    pts.push([s, y]);
  }}
  const ys = pts.map(function (p) {{ return p[1]; }});
  const yMin = Math.min(0, Math.min.apply(null, ys));
  const yMax = Math.max(0, Math.max.apply(null, ys));
  const W = 720, H = 280, L = 36, R = 16, T = 16, B = 28;
  function X(s) {{ return L + (s - min) / (max - min) * (W - L - R); }}
  function Y(v) {{ return T + (yMax - v) / (yMax - yMin || 1) * (H - T - B); }}
  let d = "";
  pts.forEach(function (p, i) {{ d += (i ? "L" : "M") + X(p[0]).toFixed(1) + " " + Y(p[1]).toFixed(1); }});
  const zero = Y(0);
  const here = pts.reduce(function (best, p) {{ return Math.abs(p[0] - spot) < Math.abs(best[0] - spot) ? p : best; }}, pts[0]);
  svg.innerHTML = '<line x1="'+L+'" y1="'+zero+'" x2="'+(W-R)+'" y2="'+zero+'" stroke="#E5E7EB"/>'
    + '<path d="'+d+'" fill="none" stroke="#0A0A0A" stroke-width="2.5"/>'
    + '<line x1="'+X(SPEC.last)+'" y1="'+T+'" x2="'+X(SPEC.last)+'" y2="'+(H-B)+'" stroke="#6B7280" stroke-dasharray="3 3"/>'
    + '<circle cx="'+X(spot)+'" cy="'+Y(here[1])+'" r="6" fill="'+(here[1] >= 0 ? "#047857" : "#B91C1C")+'"/>'
    + '<text x="'+X(spot)+'" y="14" text-anchor="middle" font-size="11">$' + here[1].toFixed(2) + '</text>';
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
