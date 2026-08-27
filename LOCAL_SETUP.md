# Local Ductor Setup

This guide covers running ductor from a local clone on Windows, installed in
editable mode so your code changes are what `ductor` actually runs.

Throughout this guide, `<repo>` means the directory you cloned into (for example
`C:\Users\<you>\projects\ductor`). The virtualenv is expected at `<repo>\.venv`.

The bundled `run-ductor.ps1` and `install-ductor-service.ps1` resolve their own
location automatically, so you never need to hardcode a path.

## Run from this clone

Use:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1
```

This forces `PYTHONUTF8=1` so Windows console encoding does not break Rich output.

## New machine setup

Recommended setup on another Windows machine:

```powershell
git clone <your-repo-url>
cd ductor

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Then run onboarding once:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1 onboarding
```

If you want ductor to start automatically after you sign in:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-ductor-service.ps1
```

Useful checks after setup:

```powershell
ductor --version
ductor status
ductor restart
ductor service status
ductor service logs
```

Important:

- keep this repo installed in editable mode with `pip install -e ".[dev]"`
- avoid mixing this repo venv with a separate global or `pipx` install of `ductor`
- after `ductor service install`, Windows Task Scheduler will start it about 10 seconds after you log in

## Your own credentials

**No credentials live in this repository.** Nothing you configure below is ever
committed, so a fresh clone is safe to publish and safe to hand to someone else.

Everything ductor needs at runtime is written outside the repo, under
`~/.ductor` (`C:\Users\<you>\.ductor` on Windows):

| What | Where | How it gets there |
|---|---|---|
| Telegram bot token, allowed user/group IDs, provider, model | `~/.ductor/config/config.json` | `ductor onboarding` |
| Matrix homeserver, user ID, password / access token | `~/.ductor/config/config.json` | `ductor onboarding` |
| Extra API keys passed through to the CLIs (e.g. `PPLX_API_KEY`) | `~/.ductor/.env` | you create it by hand |
| Webhook / direct-API tokens | `~/.ductor/config/config.json` | `ductor api enable`, webhook tools |

So taking this fork over on a new machine is just:

```powershell
git clone <your-fork-url>
cd <repo>

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"

powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1 onboarding
```

Onboarding prompts for **your** bot token and **your** Telegram user ID and
writes them to `~/.ductor`. See `config.example.json` in this repo for the full
set of options with placeholder values.

To get the two Telegram values:

- **Bot token** — message [@BotFather](https://t.me/BotFather), `/newbot`, copy the token
- **Your user ID** — message [@userinfobot](https://t.me/userinfobot), copy the numeric `Id`

If you ever need to start clean: `ductor reset` wipes `~/.ductor` and re-runs
onboarding. It does not touch the repo.

## First-time onboarding

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1 onboarding
```

In onboarding:

- choose `Telegram`
- choose `codex`
- point it at your Telegram bot token and allowed user ID
- skip Docker sandbox initially unless you specifically want it

## Background service

To install and start as a service:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-ductor-service.ps1
```

Useful follow-up commands:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1 service status
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1 service logs
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1 restart
```

## `C:\Users\<user>\.ductor`

You do not need to create or manage `~/.ductor` manually for normal setup.

`ductor onboarding` creates and maintains it for you, including:

- `config\config.json`
- `logs\`
- `workspace\`
- session and task state files

For a new machine, the recommended path is:

1. run onboarding and let it create a fresh `~/.ductor`
2. copy over only the config or custom files you actually want to keep
3. run `ductor restart` or reinstall the service if needed

Safe things to copy when migrating between machines:

- `C:\Users\<user>\.ductor\config\config.json`
- `C:\Users\<user>\.ductor\SHAREDMEMORY.md`
- custom files you intentionally added under `workspace\`

Do not copy blindly:

- `bot.pid`
- `logs\`
- `startup_state.json`
- `inflight_turns.json`
- other stale runtime/session artifacts unless you explicitly want continuity

## Editable development workflow

Because this repo was installed with `pip install -e ".[dev]"`, code changes in this clone are what `ductor` runs.

Typical workflow:

```powershell
cd <repo>
git pull
powershell -ExecutionPolicy Bypass -File .\run-ductor.ps1
```

If you change dependencies:

```powershell
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```
