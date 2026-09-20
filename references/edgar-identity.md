# SEC EDGAR identity (required)

SEC fair-access policy requires a real contact User-Agent on every request.

## Environment

```bash
export EDGAR_IDENTITY="Your Name you@email.com"
```

## Python (edgartools)

```python
from edgar import set_identity
import os
set_identity(os.environ["EDGAR_IDENTITY"])
```

## Curl / stdlib

```
User-Agent: Your Name you@email.com
```

Without this, EDGAR returns **403**. Do not use bare WebFetch against sec.gov.

## Preferred pull paths (in order)

1. `edgartools` — `pip install edgartools` then `Company("AAPL").get_financials()`
2. Plugin script — `python scripts/edgar_pull.py AAPL`
3. Companyfacts JSON from `data.sec.gov` with the same User-Agent

## Dependency pin — hishel FileStorage

If EDGAR pulls fail with **FileStorage** / hishel cache errors:

```bash
pip install 'hishel==0.1.3'
```

**Pin note:** `hishel==1.1.8` broke FileStorage compatibility with the edgartools caching path used here. Prefer `hishel==0.1.3` until upstream is verified fixed. Record the pin in RUNLOG when applied.
