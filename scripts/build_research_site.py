#!/usr/bin/env python3
"""Write the required research site from a memo-backed JSON spec.

Usage:
  python3 scripts/build_research_site.py artifacts/NBIS/03-models/site.json

The HTML file is the deliverable. Published Buy/Hold/Sell is fixed.
Knobs only move the draft scenario.
"""
from __future__ import annotations

import html
import json
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


def draft_price(spec: dict, knobs: dict) -> float:
    """Published target scaled by how far the knobs sit from base. Base knobs reprint the target."""
    base = spec["base"]

    def ratio(name: str, invert: bool = False) -> float:
        b = float(base[name])
        k = float(knobs[name])
        if b == 0 or k == 0:
            return 1.0
        return (b / k) if invert else (k / b)

    factor = (
        ratio("growth")
        * ratio("margin")
        * ratio("capex", invert=True)
        * ratio("wacc", invert=True)
        * ratio("g")
        * ratio("multiple")
    )
    dilution = float(knobs["dilution"])
    factor *= 1.0 / (1.0 + dilution / 100.0)
    return round(float(spec["target"]) * factor, 2)


def out_path(spec: dict, spec_path: Path) -> Path:
    parts = spec_path.resolve().parts
    if "artifacts" in parts:
        root = Path(*parts[: parts.index("artifacts")])
    else:
        root = spec_path.resolve().parent
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    return docs / f"{spec['ticker'].lower()}-reef-point-live.html"


def _esc(value) -> str:
    return html.escape(str(value), quote=True)


def _rows(items, keys) -> str:
    body = []
    for item in items:
        cells = "".join(f"<td>{_esc(item.get(key, ''))}</td>" for key in keys)
        body.append(f"<tr>{cells}</tr>")
    return "\n".join(body)


def render(spec: dict) -> str:
    base = spec["base"]
    methods = spec["methods"]
    peers = spec.get("peers") or []
    quarters = spec.get("quarters") or []
    deals = spec.get("deals") or []
    assets = spec.get("assets") or []
    payload = json.dumps(
        {
            "rating": spec["rating"],
            "target": spec["target"],
            "last": spec["last"],
            "base": base,
            "methods": methods,
            "peers": peers,
            "revenue_m": spec.get("revenue_m"),
            "shares_m": spec.get("shares_m"),
        }
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{_esc(spec['ticker'])} — Equities Valuation</title>
<style>
  :root {{ --ink:#111; --muted:#525252; --line:#e5e5e5; --bg:#fff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:14px/1.45 Helvetica, Arial, sans-serif; color:var(--ink); background:var(--bg); }}
  header, main {{ max-width:980px; margin:0 auto; padding:20px 16px; }}
  h1 {{ font-size:22px; margin:0 0 4px; }}
  .sub {{ color:var(--muted); margin:0 0 12px; }}
  .row {{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }}
  .chip {{ border:1px solid var(--ink); padding:4px 10px; font-weight:600; }}
  .chip.draft {{ background:#111; color:#fff; }}
  nav button, .subnav button, button {{ border:1px solid #111; background:#fff; padding:6px 10px; font:inherit; cursor:pointer; }}
  nav button[aria-pressed="true"], .subnav button[aria-pressed="true"] {{ background:#111; color:#fff; }}
  section[hidden] {{ display:none; }}
  table {{ width:100%; border-collapse:collapse; margin:12px 0; }}
  th, td {{ border-bottom:1px solid var(--line); text-align:left; padding:6px 4px; vertical-align:top; }}
  label {{ display:block; margin:8px 0; }}
  input[type="range"] {{ width:100%; }}
  .note {{ color:var(--muted); font-size:12px; }}
  .bar {{ height:10px; background:#111; }}
  .bar.dash {{ background:#fff; border:1px dashed #111; }}
</style>
</head>
<body>
<header>
  <h1>{_esc(spec.get('name') or spec['ticker'])} · {_esc(spec['ticker'])}</h1>
  <p class="sub">{_esc(spec.get('asof', ''))} · last ${_esc(spec['last'])} · {_esc(spec.get('disclaimer', 'Draft view — not investment advice.'))}</p>
  <div class="row">
    <span class="chip" id="published">{_esc(spec['rating'])} · ${_esc(spec['target'])}</span>
    <span class="chip draft" id="draft">Draft · ${_esc(spec['target'])}</span>
  </div>
</header>
<main>
  <nav class="row" aria-label="Sections">
    <button type="button" data-tab="exec" aria-pressed="true">Exec</button>
    <button type="button" data-tab="val" aria-pressed="false">Valuation</button>
    <button type="button" data-tab="res" aria-pressed="false">Research</button>
  </nav>
  <section id="exec">
    <p>Published call stays on the white chip. Knobs move only the draft.</p>
    <div id="field"></div>
  </section>
  <section id="val" hidden>
    <div class="subnav row">
      <button type="button" data-pane="field" aria-pressed="true">Field</button>
      <button type="button" data-pane="comps" aria-pressed="false">Comps</button>
      <button type="button" data-pane="txns" aria-pressed="false">Precedents</button>
      <button type="button" data-pane="assets" aria-pressed="false">Assets</button>
    </div>
    <div class="pane" data-pane="field"><div id="field2"></div></div>
    <div class="pane" data-pane="comps" hidden>
      <p>Researched set is the default. Toggles change the draft multiple only.</p>
      <div id="peers"></div>
      <p>Draft comps: <b id="compsOut">—</b></p>
    </div>
    <div class="pane" data-pane="txns" hidden>
      <table><thead><tr><th>Deal</th><th>Status</th><th>Note</th></tr></thead>
      <tbody>{_rows(deals, ('name','status','note'))}</tbody></table>
    </div>
    <div class="pane" data-pane="assets" hidden>
      <table><thead><tr><th>Layer</th><th>$ / sh</th><th>Note</th></tr></thead>
      <tbody>{_rows(assets, ('layer','ps','note'))}</tbody></table>
    </div>
  </section>
  <section id="res" hidden>
    <p>By quarter. Sentiment does not rate the name.</p>
    <table><thead><tr><th>Call</th><th>Date</th><th>They said</th><th>Next print</th><th>Kept?</th></tr></thead>
    <tbody>{_rows(quarters, ('call','date','said','showed','kept'))}</tbody></table>
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
  <p class="note">Published {_esc(spec['rating'])} ${_esc(spec['target'])} does not move. Range {_esc(spec.get('range', ''))}.</p>
</main>
<script>
const SPEC = {payload};
const published = document.getElementById("published");
function ratio(name, knobs, invert) {{
  const b = +SPEC.base[name], k = +knobs[name];
  if (!b || !k) return 1;
  return invert ? b / k : k / b;
}}
function draftPrice(knobs) {{
  let factor = ratio("growth", knobs) * ratio("margin", knobs) * ratio("capex", knobs, true)
    * ratio("wacc", knobs, true) * ratio("g", knobs) * ratio("multiple", knobs);
  factor *= 1 / (1 + (+knobs.dilution) / 100);
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
  const on = [];
  document.querySelectorAll("#peers input").forEach(function (el) {{
    if (el.checked && el.dataset.ps !== "nm") on.push(+el.dataset.ps);
  }});
  on.sort(function (a, b) {{ return a - b; }});
  let med = null;
  if (on.length) med = on.length % 2 ? on[(on.length - 1) / 2] : (on[on.length / 2 - 1] + on[on.length / 2]) / 2;
  const out = document.getElementById("compsOut");
  if (med == null || !SPEC.revenue_m || !SPEC.shares_m) out.textContent = "—";
  else out.textContent = med.toFixed(1) + "× → $" + Math.round(med * SPEC.revenue_m / SPEC.shares_m);
}}
function setKnobs(knobs) {{
  Object.keys(knobs).forEach(function (name) {{
    document.getElementById(name).value = knobs[name];
  }});
  paint();
}}
function preset(name) {{
  const b = Object.assign({{}}, SPEC.base);
  if (name === "bear") {{
    b.growth *= 0.7; b.margin *= 0.8; b.capex *= 1.2; b.wacc += 1; b.g = Math.max(0, b.g - 0.5); b.multiple *= 0.8;
  }} else if (name === "bull") {{
    b.growth *= 1.3; b.margin *= 1.15; b.capex *= 0.85; b.wacc = Math.max(4, b.wacc - 1); b.g += 0.5; b.multiple *= 1.2;
  }}
  setKnobs(b);
}}
document.querySelectorAll("nav button").forEach(function (btn) {{
  btn.addEventListener("click", function () {{
    document.querySelectorAll("nav button").forEach(function (b) {{ b.setAttribute("aria-pressed", b === btn ? "true" : "false"); }});
    ["exec","val","res"].forEach(function (id) {{ document.getElementById(id).hidden = id !== btn.dataset.tab; }});
  }});
}});
document.querySelectorAll(".subnav button").forEach(function (btn) {{
  btn.addEventListener("click", function () {{
    document.querySelectorAll(".subnav button").forEach(function (b) {{ b.setAttribute("aria-pressed", b === btn ? "true" : "false"); }});
    document.querySelectorAll("#val .pane").forEach(function (pane) {{ pane.hidden = pane.dataset.pane !== btn.dataset.pane; }});
  }});
}});
document.querySelectorAll("input[type=range]").forEach(function (el) {{ el.addEventListener("input", paint); }});
document.querySelectorAll("[data-preset]").forEach(function (btn) {{
  btn.addEventListener("click", function () {{ preset(btn.dataset.preset); }});
}});
document.getElementById("reset").addEventListener("click", function () {{ setKnobs(SPEC.base); }});
const peers = document.getElementById("peers");
(SPEC.peers || []).forEach(function (peer) {{
  const label = document.createElement("label");
  const box = document.createElement("input");
  box.type = "checkbox";
  box.dataset.ps = peer.ps == null ? "nm" : String(peer.ps);
  box.checked = !!peer.default && peer.ps != null;
  box.disabled = peer.ps == null;
  box.addEventListener("change", paint);
  label.appendChild(box);
  label.appendChild(document.createTextNode(" " + peer.ticker + " " + (peer.ps == null ? "NM" : peer.ps + "×") + " — " + (peer.why || "")));
  peers.appendChild(label);
}});
function field(host) {{
  const max = Math.max.apply(null, SPEC.methods.map(function (m) {{ return m.hi; }}).concat([SPEC.last, SPEC.target]));
  host.innerHTML = "";
  SPEC.methods.forEach(function (m) {{
    const row = document.createElement("div");
    const bar = document.createElement("div");
    bar.className = "bar" + (m.circular ? " dash" : "");
    bar.style.width = Math.max(2, (m.hi - m.lo) / max * 100) + "%";
    bar.style.marginLeft = (m.lo / max * 100) + "%";
    row.textContent = m.name + " $" + m.mid + (m.circular ? " circular" : "");
    row.appendChild(bar);
    host.appendChild(row);
  }});
}}
field(document.getElementById("field"));
field(document.getElementById("field2"));
setKnobs(SPEC.base);
</script>
</body>
</html>
"""


def build(spec_path: Path) -> Path:
    spec = load_spec(spec_path)
    # Base knobs must reprint the published target. Fail the build if they do not.
    echoed = draft_price(spec, spec["base"])
    if abs(echoed - float(spec["target"])) > 0.02:
        raise SystemExit(f"base knobs draft {echoed} != published target {spec['target']}")
    dest = out_path(spec, spec_path)
    dest.write_text(render(spec))
    return dest


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: python3 scripts/build_research_site.py artifacts/TICKER/03-models/site.json")
    dest = build(Path(argv[1]))
    print(dest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
