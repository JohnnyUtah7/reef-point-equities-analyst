#!/usr/bin/env python3
"""Generate the reconciled, self-contained Reef Point research site."""
import json
import sys
from pathlib import Path
try:
    from scripts.research_terminal import build, render, validate_spec
except ModuleNotFoundError:
    from research_terminal import build, render, validate_spec

def load_spec(path):
    return validate_spec(json.loads(Path(path).read_text()))

def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: python3 scripts/build_research_site.py artifacts/TICKER/03-models/site.json")
    print(build(Path(argv[1])))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
