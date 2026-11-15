# EDGAR identity

The hosted EDGAR server supplies its configured SEC identity. Users of the connected hosted tools do not need local edgartools or EDGAR_IDENTITY.

The following setup applies only to the local Python fallback. SEC requests require a descriptive User-Agent with contact information.

```bash
export EDGAR_IDENTITY="Your Name you@email.com"
```

Put that in `~/.zshrc` or `~/.bashrc`. Open a new terminal.

```bash
python3 -c "import os; print('Identity configured:', bool(os.environ.get('EDGAR_IDENTITY')))"
python3 scripts/edgar_pull.py AAPL --out /tmp/aapl-sec
```

- The script reads **only** the environment. Nothing in this repo is a token.
- Missing or no `@` → stop. Do not WebFetch `sec.gov`.
- If `FileStorage` / hishel errors: `pip3 install 'hishel==0.1.3'`.
