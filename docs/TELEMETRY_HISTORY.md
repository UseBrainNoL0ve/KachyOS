# Telemetry History

KachySec now keeps a bounded local history of defensive telemetry snapshots.

## Storage

Snapshots are stored under:

`~/.local/state/kachysec/telemetry/`

They contain only the fields already exposed by the local telemetry collector. They are not committed to Git automatically.

## CLI

Capture and display the current snapshot:

```bash
kachysec telemetry
```

Display recent history:

```bash
kachysec telemetry --history
kachysec telemetry --history --limit 20
```

The GUI also saves one snapshot on each refresh and shows the most recent entries in the Telemetry tab.

## Design boundary

This is local observation, not a remote monitoring agent. It does not probe other hosts, inspect packet contents, or perform automatic remediation.

The history layer is intentionally simple so it can later feed an event timeline and report generator without coupling storage to the GUI.
