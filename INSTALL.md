# Install — Reef Point Equities analyst

Packaged plugin: **`reef-point-equities-analyst` 1.3.0**. Share **this repo**. Do not install from CosmosGolf or any other checkout. Do not copy a locked official note into the plugin.

Each analyst uses **their own** `EDGAR_IDENTITY`. See [references/edgar-identity.md](./references/edgar-identity.md).

## Cursor (local plugin)

```bash
git clone <this-repo-url> reef-point-equities-analyst
cd reef-point-equities-analyst
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)" ~/.cursor/plugins/local/reef-point-equities-analyst
```

Equivalent: `rsync -a ./ ~/.cursor/plugins/local/reef-point-equities-analyst/`

The folder must contain `.cursor-plugin/plugin.json` at the plugin root.

```bash
pip3 install -r scripts/requirements.txt
export EDGAR_IDENTITY="Your Name you@email.com"   # ~/.zshrc
```

If FileStorage / hishel breaks: `pip3 install 'hishel==0.1.3'`.

Quit Cursor (`Cmd+Q`) and reopen, or **Developer: Reload Window**.

Settings → Cursor Settings → **Include third-party Plugins, Skills, and other configs** → on.

Confirm plugin name `reef-point-equities-analyst`.

If `~/.cursor/plugins/local/equity-research-studio` still exists, do **not** run both orchestrators on the same name. This pack wins.

## Claude (marketplace / skill copy)

Copy `skills/` into `~/.claude/skills/` (or add this repo as a Claude marketplace plugin). Commands live in `commands/`. Same `EDGAR_IDENTITY`. Same `analyze TICKER` trigger.

## First run

```
analyze MSFT
```

or `/analyze-lite MSFT`.

Expect `artifacts/MSFT/` and `docs/msft-equity-research.md` in the **open workspace**, not inside the plugin directory.

## Optional surfaces

| Surface | Need |
|---|---|
| Official memo + artifacts | Plugin + EDGAR only |
| Native Google Sheets / Slides | Google Drive MCP. Local xlsx/pptx still written if Drive 401 |
| X tape | Enrolled X plugin — never block |
| Native Cursor canvas | Only if asked |

No Zapier. No `gws auth login`.
