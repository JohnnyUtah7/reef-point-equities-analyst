"""Renderer contracts: statement reconciliation, safe payloads and portable output."""
import copy,json,re,subprocess,tempfile,unittest
from pathlib import Path
from scripts.build_research_site import build,render,validate_spec
ROOT=Path(__file__).resolve().parents[1]
class ResearchSiteTests(unittest.TestCase):
    def setUp(self):self.s=json.loads((ROOT/'examples/research-site-v2.json').read_text())
    def test_statement_bridge_reconciles(self):
        s=validate_spec(self.s)
        self.assertEqual(s['comps_basis']['ebitda_m'],25)
        self.assertEqual(s['rating'],'HOLD')
        self.assertEqual(s['target'],24)
    def test_bad_balance_sheet_rejected(self):
        self.s['fundamentals']['cash_m']['value']+=1
        with self.assertRaisesRegex(ValueError,'net debt'):validate_spec(self.s)
    def test_bad_revenue_rejected(self):
        self.s['fundamentals']['revenue_m']['value']+=1
        with self.assertRaisesRegex(ValueError,'base revenue'):validate_spec(self.s)
    def test_bad_dcf_rejected(self):
        self.s['model']['expected_dcf_price']+=1
        with self.assertRaisesRegex(ValueError,'reconcile'):validate_spec(self.s)
    def test_incomplete_sources_rejected(self):
        del self.s['fundamentals']['cash_m']['source']
        with self.assertRaisesRegex(ValueError,'source'):validate_spec(self.s)
    def test_numbers_and_weights(self):
        for value in (True,float('nan'),-1):
            s=copy.deepcopy(self.s);s['last']=value
            with self.assertRaises(ValueError):validate_spec(s)
        self.s['methods'][0]['weight']=-1
        with self.assertRaises(ValueError):validate_spec(self.s)
    def test_circular_weight_rejected(self):
        self.s['methods'][0]['circular']=True
        with self.assertRaises(ValueError):validate_spec(self.s)
    def test_safe_embedding(self):
        attack='</script><script>alert(1)</script>__APP__'
        self.s['story']=attack
        text=render(self.s)
        self.assertNotIn('<script>alert(1)',text)
        payload=re.search(r'<script id="research-data" type="application/json">(.*?)</script>',text,re.S)
        if payload is None:payload=re.search(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',text,re.S)
        self.assertEqual(json.loads(payload.group(1))['story'],attack)
    def test_portable_output_and_script_syntax(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'artifacts/DEMO/03-models/site.json';path.parent.mkdir(parents=True);path.write_text(json.dumps(self.s))
            dest=build(path)
            self.assertEqual(dest,Path(tmp).resolve()/'docs/demo-reef-point-live.html')
            text=dest.read_text()
            self.assertNotIn('fonts.googleapis.com',text)
            for token in ('Valuation football field','statement-bridge','sensitivity','tornado','ledger','method-detail'):
                self.assertTrue(token in text,token)
            for i,script in enumerate(re.findall(r'<script>(.*?)</script>',text,re.S)):
                f=Path(tmp)/('script'+str(i)+'.js');f.write_text(script);subprocess.run(['node','--check',str(f)],check=True,capture_output=True)
    def test_missing_model_is_read_only(self):
        del self.s['model'];self.assertIn('Model unavailable',render(self.s))
    def test_unsafe_ticker(self):
        self.s['ticker']='../../bad'
        with self.assertRaises(ValueError):validate_spec(self.s)
if __name__=='__main__':unittest.main()
