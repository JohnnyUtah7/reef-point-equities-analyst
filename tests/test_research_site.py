"""The research site is generated every time, and knobs do not move the published call."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.build_research_site import build, draft_price, load_spec, open_view

ROOT = Path(__file__).resolve().parents[1]

SPEC = {
    "ticker": "NBIS",
    "name": "Nebius",
    "asof": "3 Oct 2026",
    "last": 90,
    "rating": "HOLD",
    "target": 100,
    "range": [70, 140],
    "shares_m": 200,
    "revenue_m": 500,
    "disclaimer": "Draft view — not investment advice.",
    "base": {
        "growth": 20,
        "margin": 25,
        "capex": 30,
        "wacc": 11,
        "g": 2.5,
        "multiple": 8,
        "dilution": 0,
    },
    "methods": [
        {"name": "DCF", "lo": 70, "mid": 100, "hi": 140, "weight": 0.55, "circular": False},
        {"name": "Trading", "lo": 60, "mid": 80, "hi": 110, "weight": 0.25, "circular": False},
        {"name": "Own ARR", "lo": 90, "mid": 90, "hi": 90, "weight": 0, "circular": True},
    ],
    "peers": [
        {"ticker": "IREN", "ps": 26, "why": "adjacent", "default": True},
        {"ticker": "APLD", "ps": 13.4, "why": "HPC", "default": True},
        {"ticker": "CORZ", "ps": None, "why": "no revenue", "default": False},
    ],
    "quarters": [
        {"call": "Q1", "date": "1 May 2026", "said": "Grow revenue", "showed": "Next print pending", "kept": "OPEN"}
    ],
    "deals": [{"name": "None closed", "status": "n/a", "note": "DATA_GAP"}],
    "assets": [{"layer": "Book", "ps": 12, "note": "filing"}],
}


class ResearchSiteTests(unittest.TestCase):
    def test_base_knobs_reprint_the_published_target(self):
        cover = open_view(SPEC)["target"]
        self.assertEqual(draft_price(SPEC, SPEC["base"]), cover)

    def test_a_knob_moves_the_draft_only(self):
        knobs = dict(SPEC["base"])
        knobs["growth"] = 40
        self.assertGreater(draft_price(SPEC, knobs), open_view(SPEC)["target"])

    def test_a_wild_knob_cannot_explode_the_draft(self):
        knobs = dict(SPEC["base"])
        knobs["growth"] = 56
        knobs["capex"] = 0
        cover = open_view(SPEC)["target"]
        self.assertLessEqual(draft_price(SPEC, knobs), round(cover * 1.45, 2))

    def test_bull_open_does_not_cover_with_sell(self):
        spec = dict(SPEC)
        spec["rating"] = "SELL"
        spec["target"] = 170
        spec["last"] = 334
        spec["stance"] = "bull"
        view = open_view(spec)
        self.assertNotEqual(view["rating"], "SELL")
        self.assertEqual(view["kill_rating"], "SELL")
        self.assertEqual(view["kill_target"], 170)

    def test_build_writes_the_site_every_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "artifacts" / "NBIS" / "03-models" / "site.json"
            spec_path.parent.mkdir(parents=True)
            spec_path.write_text(json.dumps(SPEC))
            dest = build(spec_path)
            self.assertEqual(dest, Path(tmp) / "docs" / "nbis-reef-point-live.html")
            text = dest.read_text()
            self.assertIn('id="published">BUY · $140', text)
            self.assertIn("Football field", text)
            self.assertIn('id="payoff"', text)
            self.assertIn("By quarter", text)
            self.assertIn("Precedents", text)
            self.assertIn("Assets", text)
            self.assertIn("data-tab=\"res\"", text)
            self.assertIn("id=\"reset\"", text)
            for name in ("growth", "margin", "capex", "wacc", "g", "multiple", "dilution"):
                self.assertIn(f'id="{name}"', text)
            script = text.split("<script>")[1].split("</script>")[0]
            Path("/tmp/site-page.js").write_text(script)
            subprocess.check_call(["node", "--check", "/tmp/site-page.js"])
            # The published chip is rewritten from the spec, never from the knobs.
            self.assertIn('published.textContent = SPEC.rating + " · $" + SPEC.target', script)
            self.assertIn('document.getElementById("draft").textContent = "Draft · $" + draftPrice(knobs)', script)

    def test_refuses_a_spec_without_a_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "site.json"
            bad = dict(SPEC)
            del bad["rating"]
            path.write_text(json.dumps(bad))
            with self.assertRaises(SystemExit):
                load_spec(path)

    def test_stock_prompts_must_run_the_generator(self):
        skill = (ROOT / "skills" / "full-company-analysis" / "SKILL.md").read_text()
        site = (ROOT / "skills" / "research-canvas" / "SKILL.md").read_text()
        rules = (ROOT / "rules" / "equity-research-hard-rules.mdc").read_text()
        gpt = (ROOT / "adapters" / "gpt-instructions.md").read_text()
        for text in (skill, site, rules, gpt):
            self.assertIn("reef-point-live.html", text)
            self.assertTrue(
                "Do not ask for a URL" in text or "Do not ask for a site URL" in text,
                text[:80],
            )
        self.assertIn("build_research_site.py", site)
        self.assertIn("Codex Sites", gpt)
        self.assertIn("What do you think of IREN", gpt)
        self.assertNotIn("OPTIONAL — only if asked", skill)


if __name__ == "__main__":
    unittest.main()
