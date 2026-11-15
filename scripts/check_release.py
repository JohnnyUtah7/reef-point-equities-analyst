#!/usr/bin/env python3
"""Verify the selected source release; does not claim an installed upgrade."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json',
             '.cursor-plugin/plugin.json', '.grok-plugin/plugin.json')

def check(root=ROOT):
    versions = {p: json.loads((root / p).read_text())['version'] for p in MANIFESTS}
    versions['.claude-plugin/marketplace.json'] = json.loads(
        (root / '.claude-plugin/marketplace.json').read_text())['metadata']['version']
    if len(set(versions.values())) != 1:
        raise ValueError('Plugin version mismatch: ' + json.dumps(versions, sort_keys=True))
    return {'plugin_root': str(root.resolve()), 'version': versions['plugin.json'],
            'manifests': len(versions), 'scope': 'source release only; connections and live run not verified'}

if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
