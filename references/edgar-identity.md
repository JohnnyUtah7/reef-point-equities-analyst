# EDGAR identity

SEC requires a real name and email on every request.

```bash
export EDGAR_IDENTITY="Your Name you@email.com"
```

Put that in `~/.zshrc` or `~/.bashrc`. Open a new terminal.

```bash
echo "$EDGAR_IDENTITY"
python3 scripts/edgar_pull.py AAPL --out /tmp/aapl-sec
```

- The script reads **only** the environment. Nothing in this repo is a token.
- Missing or no `@` → stop. Do not WebFetch `sec.gov`.
- If `FileStorage` / hishel errors: `pip3 install 'hishel==0.1.3'`.
