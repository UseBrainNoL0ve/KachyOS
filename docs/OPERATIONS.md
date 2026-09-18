# Operations and audit trail

KachySec separates discovery, planning and privileged execution.

## Package installation lifecycle

1. Inspect the local catalog.
2. Build an exact package plan.
3. Review the package list.
4. Require explicit confirmation.
5. Run `sudo pacman -S --needed ...`.
6. Record the command, timestamps, exit code and output locally.
7. Re-run discovery to verify the resulting state.

The operation layer never runs an unconfirmed package operation.

## Local log

Execution records are appended to:

`~/.local/state/kachysec/operations.jsonl`

The file is local state and should not be committed to Git.

## Safety boundary

GUI refresh, audits and planning remain read-only. Privileged changes happen only through an explicit action. KachySec does not silently install a large tool set or alter firewall/service configuration.
