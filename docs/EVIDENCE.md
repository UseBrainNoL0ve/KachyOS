# Baseline Evidence and Diffing

KachySec can persist local baseline snapshots and compare them structurally over time.

## Snapshot storage

When a baseline is written with --output, KachySec also stores a JSON snapshot under:

~/.local/state/kachysec/baselines/

These snapshots are local evidence artifacts. They are not committed to Git automatically.

## Capture a snapshot

```bash
mkdir -p reports
kachysec baseline --format markdown --output reports/baseline.md
```

The human-readable report is written to the requested path and a machine-readable JSON snapshot is saved in local state.

## Compare snapshots

Use two explicit files:

```bash
kachysec baseline-diff BEFORE.json AFTER.json
```

Or compare the two newest local snapshots:

```bash
kachysec baseline-diff --latest
```

The diff engine reports added, removed and changed structural fields. It deliberately does not label a change as malicious or secure; interpretation remains an investigation step.

## Why this matters

This introduces a basic evidence workflow:

1. capture a known state;
2. make or review an authorized change;
3. capture another state;
4. compare the two states;
5. investigate meaningful differences.

The next evidence layer can build on this with post-operation verification and exportable security reports.
