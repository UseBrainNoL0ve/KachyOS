# Usage Guide

## Command overview

| Command | Purpose | Changes host? |
| --- | --- | --- |
| `baseline` | Collect host inventory | No |
| `status` | Summarize tools and runtimes | No |
| `audit` | Review basic security posture | No |
| `updates` | Show pending pacman updates | No |
| `tools` | Browse the security tool catalog | No |
| `tools --missing` | Show missing tools | No |
| `tools --category network` | Filter a discipline | No |
| `tools --plan` | Build a package installation plan | No |
| `lab` | Inspect lab runtimes/definitions | No |
| `gui` | Launch the desktop dashboard | No |

## Baseline

Use a Markdown report when you want a human-readable snapshot:

```bash
kachysec baseline --format markdown --output reports/baseline.md
```

Use JSON for automation:

```bash
kachysec baseline --format json --output reports/baseline.json
```

## Tool catalog

Start broad:

```bash
kachysec tools
```

Narrow it down:

```bash
kachysec tools --category web
kachysec tools --category reverse
kachysec tools --missing
```

The catalog is metadata and discovery. It does not imply that every tool is appropriate for every machine.

## Installation planning

```bash
kachysec tools --plan
```

The command resolves locally available pacman candidates and prints a deduplicated plan. It does not execute installation.

The intended lifecycle is:

**discover → inspect → plan → explicit confirmation → privileged install → verify**

This separation keeps package changes auditable and prevents accidental bulk installation.

## Audit

```bash
kachysec audit
```

The audit checks basic firewall state, pending updates, failed systemd units, SSH state, lab runtimes and selected sensitive-file permissions. It is a lightweight posture check, not a replacement for a full security assessment.

## Lab manager

```bash
kachysec lab
```

The lab manager only discovers available container/VM runtimes and local lab definitions. Future lab automation will target isolated environments that the user owns or is authorized to operate.

## GUI

```bash
kachysec gui
```

The dashboard provides:

- live 10-second refresh;
- tool search and filtering;
- selected-tool details;
- package-candidate inspection;
- installation-plan preview;
- audit and update panels;
- lab-runtime visibility.

GUI actions that change the system should remain explicit and reviewable.
