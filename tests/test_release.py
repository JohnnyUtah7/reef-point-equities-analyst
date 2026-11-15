import json
import tempfile
import unittest
from pathlib import Path
from scripts.check_release import check, MANIFESTS

class ReleaseTests(unittest.TestCase):
    def test_actual_release_agrees(self):
        self.assertEqual(check()['manifests'], 6)

    def test_detects_stale_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in MANIFESTS:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(json.dumps({'version': '1.4.1'}))
            (root / '.claude-plugin/marketplace.json').write_text(
                json.dumps({'metadata': {'version': '1.3.12'}}))
            with self.assertRaisesRegex(ValueError, 'version mismatch'):
                check(root)

if __name__ == '__main__':
    unittest.main()
