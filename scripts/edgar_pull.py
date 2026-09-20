#!/usr/bin/env python3
"""Thin EDGAR financials puller for Equity Research Studio.

Requires: pip install edgartools
Requires: EDGAR_IDENTITY="Name email@domain.com"

Usage:
  python scripts/edgar_pull.py AAPL
  python scripts/edgar_pull.py AAPL --out artifacts/AAPL/01-sec
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description="Pull SEC financials via edgartools")
    p.add_argument("ticker", help="Ticker symbol, e.g. AAPL")
    p.add_argument("--out", default=None, help="Output directory")
    args = p.parse_args()
    ticker = args.ticker.upper().strip()
    out = Path(args.out or f"artifacts/{ticker}/01-sec")
    out.mkdir(parents=True, exist_ok=True)

    identity = os.environ.get("EDGAR_IDENTITY", "").strip()
    if not identity:
        print("ERROR: Set EDGAR_IDENTITY='Your Name you@email.com'", file=sys.stderr)
        return 2

    try:
        from edgar import Company, set_identity
    except ImportError:
        print("ERROR: pip install edgartools", file=sys.stderr)
        return 2

    set_identity(identity)
    company = Company(ticker)
    meta = {
        "ticker": ticker,
        "name": getattr(company, "name", None) or str(company),
        "cik": getattr(company, "cik", None),
        "identity_set": True,
        "source": "edgartools",
    }
    (out / "company_meta.json").write_text(json.dumps(meta, indent=2, default=str))

    try:
        fins = company.get_financials()
        # Best-effort dumps; structure varies by edgartools version
        payload = {"ticker": ticker, "notes": "See printed statements; serialize below if available"}
        for attr in ("income_statement", "balance_sheet", "cash_flow"):
            fn = getattr(fins, attr, None)
            if callable(fn):
                try:
                    stmt = fn()
                    payload[attr] = str(stmt)
                except Exception as e:  # noqa: BLE001
                    payload[attr] = f"ERROR: {e}"
        (out / "financials_text.json").write_text(json.dumps(payload, indent=2))
    except Exception as e:  # noqa: BLE001
        (out / "financials_error.txt").write_text(str(e))
        print(f"WARN: get_financials failed: {e}", file=sys.stderr)

    # Recent filings index
    try:
        filings = company.get_filings(form=["10-K", "10-Q", "8-K"])
        rows = []
        for i, f in enumerate(filings):
            if i >= 40:
                break
            rows.append(
                {
                    "form": getattr(f, "form", None),
                    "filing_date": str(getattr(f, "filing_date", "")),
                    "accession": str(getattr(f, "accession_number", getattr(f, "accession_no", ""))),
                }
            )
        (out / "filings_index.json").write_text(json.dumps(rows, indent=2))
    except Exception as e:  # noqa: BLE001
        (out / "filings_error.txt").write_text(str(e))

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
