# Install — Reef Point Equities Analyst

## A. Cursor plugin (recommended)

Cursor discovers plugins under `~/.cursor/plugins/local/<name>/` that contain `.cursor-plugin/plugin.json`.

1. Copy this folder:

   ```bash
   mkdir -p ~/.cursor/plugins/local
   rsync -a --delete \
     /path/to/reef-point-equities-analyst/ \
     ~/.cursor/plugins/local/reef-point-equities-analyst/
   ```

2. Restart Cursor **or** run **Developer: Reload Window**.

3. Open **Cursor Settings → Customize** (or Plugins) and confirm:
   - Skills: `portfolio-research`, `full-company-analysis`, `sec-filings`, `football-field`, …
   - Agents: `research-lead`, `sec-analyst`, …
   - Rules: equity research hard rules

4. Set EDGAR identity in the shell Agent terminals use:

   ```bash
   echo 'export EDGAR_IDENTITY="Your Name you@email.com"' >> ~/.zshrc
   export EDGAR_IDENTITY="Your Name you@email.com"
   ```

   Optionally set the same value in the plugin’s Configure / variables UI (`EDGAR_IDENTITY`).

5. Optional tooling:

   ```bash
   pip install edgartools python-pptx openpyxl
   pip install 'hishel==0.1.3'   # if FileStorage / hishel 1.x breaks EDGAR pulls
   ```

6. Demo:

   ```text
   analyze AAPL
   ```

### Zip install

```bash
cd /path/to
zip -r reef-point-equities-analyst.zip reef-point-equities-analyst \
  -x '*/__pycache__/*' '*.pyc' '.git/*'
# Unzip into ~/.cursor/plugins/local/ on the other machine
```

## B. Project-local skills (no plugin UI)

```bash
cd your-research-repo
mkdir -p .cursor/skills .cursor/agents .cursor/rules
cp -R /path/to/reef-point-equities-analyst/skills/* .cursor/skills/
cp -R /path/to/reef-point-equities-analyst/agents/* .cursor/agents/
cp /path/to/reef-point-equities-analyst/rules/*.mdc .cursor/rules/
```

Cursor also loads `.claude/skills/` — copy there for dual IDE use.

## C. Claude Code

This folder includes `.claude-plugin/plugin.json` and root `plugin.json`:

```text
claude plugin marketplace add /path/to/reef-point-equities-analyst
claude plugin install reef-point-equities-analyst
```

Exact marketplace commands depend on how you host the repo. Copying `skills/` into `~/.claude/skills/` always works.

## Post-install verification

- [ ] `~/.cursor/plugins/local/reef-point-equities-analyst/.cursor-plugin/plugin.json` exists
- [ ] Agent sees skill `portfolio-research`
- [ ] `echo $EDGAR_IDENTITY` prints Name + email
- [ ] `python3 -c "import edgar"` works if you installed edgartools
- [ ] (Optional) Google Drive MCP authenticated for Sheets / Slides conversion

## Caveats

| Topic | Note |
|---|---|
| EDGAR 403 | Missing or invalid User-Agent identity |
| hishel FileStorage | Pin `hishel==0.1.3` |
| Google Slides / Sheets | Drive MCP; conversion-on-upload. No Zapier. |
| Rate limits | Pre-cache a demo ticker before a live pull |
| Size | Skills/agents text + logo/template; keep giant vendor clones out |
| Advice | Outputs are not investment advice |
