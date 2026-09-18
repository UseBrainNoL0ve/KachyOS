# Usage Guide

## Command overview

| Command | Purpose | Changes host? |
| --- | --- | --- |
| `baseline` | Collect host inventory | No |
| `status` | Summarize tools and runtimes | No |
| `audit` | Review basic security posture | No |
| `updates` | Show pending pacman updates | No |
| `telemetry` | Show local defensive telemetry | No |
| `tools` | Browse the security tool catalog | No |
| `tools --missing` | Show missing tools | No |
| `tools --category network` | Filter a discipline | No |
| `tools --plan` | Build a package installation plan | No |
| `tools --install` | Install the reviewed package plan after confirmation | **Yes** |
| `lab` | Inspect lab runtimes/definitions | No |
| `lab --plan` | Build a review-only lab lifecycle plan | No |
| `gui` | Launch the desktop dashboard | No |

## Baseline

```bash
kachysec baseline --format markdown --output reports/baseline.md
```

Use JSON for automation:

```bash
kachysec baseline --format json --output reports/baseline.json
```

Baseline output can contain host-specific information. Keep reports local unless they have been reviewed and redacted.

## Tool catalog

```bash
kachysec tools
kachysec tools --category web
kachysec tools --missing
```

The catalog is metadata and discovery. It does not imply that every tool is appropriate for every machine or authorized for every target.

## Installation planning and execution

Preview the exact package plan:

```bash
kachysec tools --plan
```

If an installation is intentionally required:

```bash
kachysec tools --install
```

The lifecycle is:

**discover → inspect → resolve → plan → review → explicit confirmation → privileged install → verify**

The explicit operation is logged locally.

## Audit and updates

```bash
kachysec audit
kachysec updates
```

The audit is a lightweight posture check, not a replacement for a full security assessment. Updates are inspection-only; KachySec does not run `pacman -Syu` through the update service.

## Telemetry

```bash
kachysec telemetry
```

Telemetry observes local load, memory, listening sockets, and process count. It does not perform remote probing or remediation.

## Lab manager

```bash
kachysec lab
kachysec lab --plan
```

The lab manager discovers runtimes and local definitions. The current lifecycle planner is review-only.

## GUI

```bash
kachysec gui
```

The dashboard provides live refresh, tool search/filtering, package-candidate inspection, install-plan preview, audit/update panels, lab visibility, telemetry, and local operation history.
