# Install — Reef Point Equity Research

Share **this repo**. Teammates do not need the old Mac-local `equity-research-studio` 1.0.1 folder. That pack was the engine we tested on IREN; **this plugin is the product**.

## 1. Clone

```bash
git clone <repo-url> reef-point-equity-research
cd reef-point-equity-research
```

## 2. Register as a local Cursor plugin

```bash
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)" ~/.cursor/plugins/local/reef-point-equity-research
```

The folder must contain `.cursor-plugin/plugin.json` at the **plugin root** (this repo root).

Quit Cursor fully (`Cmd+Q`) and reopen, or **Developer: Reload Window**.

Settings → Cursor Settings → **Include third-party Plugins, Skills, and other configs** → on.

Confirm the plugin name `reef-point-equity-research` and that skills / commands / agents loaded.

If you still have `~/.cursor/plugins/local/equity-research-studio`, leave it or remove it — do **not** run both orchestrators on the same name. This repo wins.

## 3. Python

```bash
pip3 install -r scripts/requirements.txt
```

If an EDGAR pull raises `FileStorage` / hishel errors:

```bash
pip3 install 'hishel==0.1.3'
```

## 4. SEC identity (required)

SEC wants a real name + email on every request.

```bash
# ~/.zshrc or ~/.bashrc
export EDGAR_IDENTITY="Your Name you@company.com"
```

Open a new terminal. Check:

```bash
echo "$EDGAR_IDENTITY"
python3 scripts/edgar_pull.py AAPL --out /tmp/aapl-sec
```

Stop if identity is missing. Never WebFetch `sec.gov`.

## 5. Optional publish surfaces

| Surface | Need |
|---|---|
| Official memo + artifacts | Plugin + EDGAR only |
| Native Google Sheets / Slides | Google Drive MCP connected in Cursor |
| X tape | X plugin **enrolled** (optional; never block) |
| Native Cursor canvas | Only if someone asks; not required |

No Zapier. No `gws auth login`.

## 6. First run (not IREN)

```
/analyze-lite MSFT
```

or

```
analyze MSFT end-to-end
```

Expect `artifacts/MSFT/` and `docs/msft-equity-research.md` in **the workspace you have open**, not inside the plugin directory.

## Team share

1. Push this repo to the firm Git host.
2. Send INSTALL.md. Each analyst uses **their own** `EDGAR_IDENTITY`.
3. Do not email a zip of IREN artifacts as “the model.” The plugin is the model kit; each name gets a new `artifacts/{TICKER}/`.
