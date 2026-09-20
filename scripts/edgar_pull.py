#!/usr/bin/env python3
"""Pull SEC company meta, filings index, and standardized financials.

Requires EDGAR_IDENTITY="Name email@domain.com" and edgartools.
Pin hishel==0.1.3 if FileStorage breaks.

Usage:
  python3 scripts/edgar_pull.py IREN
  python3 scripts/edgar_pull.py IREN --out artifacts/IREN/01-sec
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def _die(msg: str, code: int = 1) -> None:
    print(f"edgar_pull: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _jsonable(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    try:
        import pandas as pd

        if isinstance(obj, pd.DataFrame):
            return json.loads(obj.to_json(orient="split", date_format="iso"))
        if isinstance(obj, pd.Series):
            return json.loads(obj.to_json(date_format="iso"))
    except Exception:
        pass
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return str(obj)


def _set_identity() -> str:
    identity = (os.environ.get("EDGAR_IDENTITY") or "").strip()
    if not identity or "@" not in identity:
        _die(
            "EDGAR_IDENTITY missing or invalid. Export "
            'EDGAR_IDENTITY="Your Name you@company.com" and retry.'
        )
    try:
        from edgar import set_identity
    except ImportError:
        _die("edgartools is not installed. pip3 install -r scripts/requirements.txt")
    set_identity(identity)
    return identity


def _company(ticker: str):
    from edgar import Company

    try:
        return Company(ticker)
    except Exception as exc:
        _die(f"Company({ticker!r}) failed: {exc}")


def _filings_index(company, limit: int = 80) -> list[dict]:
    forms = ["10-K", "10-Q", "8-K", "20-F", "40-F", "6-K", "S-1", "S-3", "424B5"]
    rows: list[dict] = []
    try:
        filings = company.get_filings(form=forms)
    except TypeError:
        filings = company.get_filings()
    except Exception as exc:
        return [{"error": str(exc)}]

    try:
        iterable = list(filings)[:limit]
    except Exception:
        try:
            iterable = filings.head(limit) if hasattr(filings, "head") else []
        except Exception:
            iterable = []

    for f in iterable:
        rows.append(
            {
                "form": str(getattr(f, "form", "") or getattr(f, "Form", "")),
                "filing_date": str(
                    getattr(f, "filing_date", "")
                    or getattr(f, "filingDate", "")
                    or ""
                ),
                "accession": str(
                    getattr(f, "accession_number", "")
                    or getattr(f, "accession_no", "")
                    or getattr(f, "accession", "")
                    or ""
                ),
                "period": str(getattr(f, "period_of_report", "") or getattr(f, "period", "") or ""),
            }
        )
    return rows


def _financials_dump(company) -> dict:
    out: dict = {"source": "edgartools", "ok": False}
    fin = None
    for attr in ("get_financials", "financials"):
        obj = getattr(company, attr, None)
        if obj is None:
            continue
        try:
            fin = obj() if callable(obj) else obj
            if fin:
                break
        except Exception as exc:
            out.setdefault("errors", []).append(f"{attr}: {exc}")
    if not fin:
        out["error"] = "get_financials() returned empty (try 20-F / 40-F / 6-K path in notes)"
        return out

    out["ok"] = True
    for name, aliases in (
        ("income_statement", ("income_statement", "income", "get_income_statement")),
        ("balance_sheet", ("balance_sheet", "balance", "get_balance_sheet")),
        ("cash_flow", ("cash_flow_statement", "cashflow", "cash_flow", "get_cash_flow_statement")),
    ):
        for alias in aliases:
            val = getattr(fin, alias, None)
            if val is None:
                continue
            try:
                val = val() if callable(val) else val
            except Exception as exc:
                out.setdefault("errors", []).append(f"{name}.{alias}: {exc}")
                continue
            out[name] = _jsonable(val)
            break
    out["raw_repr"] = str(fin)[:8000]
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="EDGAR pull for Reef Point equity research")
    parser.add_argument("ticker", help="Listed ticker, e.g. IREN or NVDA")
    parser.add_argument("--out", default=None, help="Output directory (default artifacts/TICKER/01-sec)")
    parser.add_argument("--limit", type=int, default=80, help="Max filings in the index")
    args = parser.parse_args()

    ticker = args.ticker.strip().upper()
    if not ticker.isalnum():
        _die(f"Refusing ticker {ticker!r} — use letters/numbers only")

    identity = _set_identity()
    out_dir = Path(args.out or f"artifacts/{ticker}/01-sec")
    out_dir.mkdir(parents=True, exist_ok=True)

    company = _company(ticker)
    cik = getattr(company, "cik", None) or getattr(company, "cik_str", None)
    name = getattr(company, "name", None) or getattr(company, "legal_name", None)

    meta = {
        "ticker": ticker,
        "name": str(name) if name else None,
        "cik": int(cik) if str(cik).isdigit() else cik,
        "identity_set": True,
        "identity_present": True,
        "pulled_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "source": "edgartools",
        "script": "scripts/edgar_pull.py",
    }
    (out_dir / "company_meta.json").write_text(json.dumps(meta, indent=2) + "\n")

    index = _filings_index(company, limit=args.limit)
    (out_dir / "filings_index.json").write_text(json.dumps(index, indent=2) + "\n")
    periodic = [r for r in index if str(r.get("form", "")).upper() in {"10-K", "10-Q", "20-F", "40-F"}]
    (out_dir / "periodic_filings.json").write_text(json.dumps(periodic, indent=2) + "\n")

    financials = _financials_dump(company)
    financials["ticker"] = ticker
    financials["cik"] = meta["cik"]
    (out_dir / "financials.json").write_text(json.dumps(financials, indent=2, default=str) + "\n")
    (out_dir / "financials_text.json").write_text(
        json.dumps({"ticker": ticker, "text": financials.get("raw_repr", "")}, indent=2) + "\n"
    )

    notes = out_dir / "notes.md"
    if not notes.exists():
        notes.write_text(
            f"# {ticker} — SEC notes\n\n"
            f"Pulled {meta['pulled_at']}. CIK `{meta['cik']}`. Identity set (`{identity.split()[-1]}`).\n\n"
            "Agent: cite form / date / accession in this file. Do not invent quotes.\n"
            "If `financials.json` has `ok: false`, try 20-F / 40-F / 6-K (FPI) before declaring UNRESOLVED.\n"
        )

    print(json.dumps({"ok": True, "ticker": ticker, "cik": meta["cik"], "out": str(out_dir)}, indent=2))


if __name__ == "__main__":
    main()
