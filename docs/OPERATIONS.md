# Operations and audit trail

KachySec separates discovery, planning, and privileged execution.

## Package installation lifecycle

1. Inspect the local catalog.
2. Resolve native package candidates.
3. Build an exact, deduplicated package plan.
4. Review the package list.
5. Require explicit confirmation.
6. Run `sudo pacman -S --needed ...`.
7. Record the command, timestamps, exit code, and output locally.
8. Re-run discovery to verify the resulting state.

The operation layer never runs an unconfirmed package operation.

## Confirmation boundary

The CLI requires the literal token:

```text
INSTALL
```

A failed or missing confirmation is logged as an unexecuted operation and does not invoke pacman.

## Local log

Execution records are appended to:

```text
~/.local/state/kachysec/operations.jsonl
```

The file is local state and should not be committed to Git.

## GUI history

The dashboard's **History** panel reads the same JSONL state and displays recent operations, return codes, timestamps, commands, and the first output line.

## Safety boundary

GUI refresh, audits, telemetry, and planning remain read-only. Privileged changes happen only through an explicit action. KachySec does not silently install a large tool set or alter firewall/service configuration.
