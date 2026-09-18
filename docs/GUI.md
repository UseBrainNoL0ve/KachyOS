# Security Dashboard

KachySec includes an optional PySide6 dashboard built on the same service APIs used by the CLI.

## Current panels

- **Overview** — live tool coverage, pending updates, audit state, and runtime availability.
- **Tools** — searchable catalog, category filtering, tool metadata, package candidates, and install-plan preview.
- **Audit** — read-only security posture findings.
- **Updates** — package version transitions reported by pacman.
- **Labs** — runtime availability and local lab definitions.
- **Telemetry** — local defensive host telemetry.
- **History** — recent privileged operations recorded in local JSONL state.

## Refresh model

The dashboard performs an initial snapshot and refreshes automatically every 10 seconds. A manual **Refresh** button is also available.

Refreshes call the shared read-only service layer. They do not install packages, alter firewall rules, modify services, start labs, or probe remote networks.

## Tool workflow

The Tools panel separates inspection from change:

1. Search or filter the catalog.
2. Inspect a tool's executable, scope, package candidates, and verification command.
3. Build an exact installation plan.
4. Review the plan.
5. If installation is genuinely required, use the explicit CLI operation `kachysec tools --install` and confirm the exact package list.

The GUI's **Build Install Plan** action is planning only.

## Operations history

Successful, failed, and unconfirmed package operations are recorded locally at:

```text
~/.local/state/kachysec/operations.jsonl
```

The History panel displays recent records for local accountability. This state is intentionally outside the Git repository.

## Native CachyOS workflow

The GUI is optional. The core CLI and services remain usable without PySide6.

On Arch/CachyOS, install the optional GUI dependency with:

```bash
sudo pacman -S pyside6
```

The dashboard uses Qt Fusion styling with palette-aware values so it can remain visually consistent without replacing the host desktop theme.

## Safety boundary

The GUI is a presentation layer over the security-workstation services. Read-only discovery and planning are safe defaults. High-impact host changes require a separate explicit operation and confirmation boundary.
