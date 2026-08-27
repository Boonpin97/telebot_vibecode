## Add `/ter` Full-Shell Command for Telegram

### Summary
Add a new Telegram-only `/ter <command>` command that executes arbitrary host shell commands in the foreground and streams stdout/stderr back to chat in real time. It should integrate with the existing per-chat locking, process tracking, `/stop`, and `/interrupt` behavior, but it must remain separate from model-driven `/cmd` so it is explicitly a direct shell path rather than an LLM turn.

Because you selected full host shell access, the implementation should include visible friction and audit by default: explicit banner text on first line of each run, command echoing, exit code reporting, working-directory disclosure, and persistent logging.

### Implementation Changes
- Add `/ter` as a new Telegram-only command.
- Route it through the Telegram/orchestrator command path, but handle it as a dedicated non-LLM execution path.
- Parse `/ter <command>` from raw Telegram message text.
- If no command is supplied, return usage/help text and do nothing.
- Execute commands on Windows via PowerShell using the bot’s host environment.
- Default working directory to `paths.workspace`.
- Stream both stdout and stderr back to the originating chat in real time.
- Reuse existing per-chat locking and `ProcessRegistry` integration.
- Support `/stop` to kill the shell subprocess tree.
- Support `/interrupt` using the existing soft-interrupt path where applicable.
- Register the subprocess with a distinct label such as `ter`.
- Return a final status/footer with exit code and elapsed duration.
- Keep `/ter` fully outside provider/session accounting.
- Do not create or update LLM sessions.
- Do not affect active model/provider.
- Do not increment session message counters.
- Do not trigger memory flush, compaction, or provider recovery logic.
- Add explicit host-risk warning text to usage/help and the initial run banner.

### Interfaces and Behavior
- Command shape: `/ter <shell command>`
- Transport scope: Telegram only
- Shell: PowerShell
- CWD: `paths.workspace`
- Environment: inherited bot process environment
- Output: stream stdout and stderr to chat
- Stdin: no interactive shell/session support in v1

### Failure Behavior
- Spawn failure returns immediate error text.
- Non-zero exit is reported as command failure, not as an internal bot error.
- Large output should be coalesced or truncated cleanly, with a visible truncation note when needed.

### Test Plan
- `/ter dir` is recognized and routed correctly on Telegram.
- `/ter` with no args returns usage text.
- Shell execution launches PowerShell with workspace cwd.
- Stdout and stderr are streamed back in order.
- Final status includes exit code.
- `/ter` does not alter model/provider/session state.
- `/ter` does not create a provider session when none exists.
- `/stop` aborts an active `/ter` subprocess tree.
- `/interrupt` follows the existing interrupt path where supported.
- `/ter` is not exposed on Matrix or API transports.

### Assumptions and Defaults
- Full host shell access is intentional and accepted.
- v1 is non-interactive: one command per invocation, no stdin passthrough.
- v1 uses the platform shell directly rather than aliases or an allowlist.
- v1 defaults to the agent workspace as cwd.
