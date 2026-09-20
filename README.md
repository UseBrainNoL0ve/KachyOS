# KachyOS Security Workstation

A modular cybersecurity workstation layer built on top of CachyOS.

> KachySec does not replace the CachyOS desktop, theme, compositor, or normal workflow. It adds a structured security-engineering control plane around the existing host.

## What this project is

KachySec combines host visibility, security posture checks, a broad dual-use security-tool catalog, authorized offensive-security workflows, package planning, explicit package operations, defensive telemetry, a live GUI, operation history, and isolated lab-runtime discovery.

- **Host visibility** — baseline inventory, runtime discovery, and package state.
- **Security posture** — lightweight, read-only audits.
- **Defensive telemetry** — local load, memory, listening sockets, and process-count observation with local history.
- **Evidence workflow** — persistent local baseline snapshots and structural diffing.
- **Tool universe** — networking, web/API security, vulnerability management, OSINT, forensics, reverse engineering, password auditing, wireless, and observability, covering both defensive and authorized offensive workflows.
- **Tool Manager** — package-candidate inspection and exact installation planning.
- **Operations** — explicit, reviewable privileged package execution with a local audit trail.
- **GUI dashboard** — live desktop view over the same Python service layer.
- **Offensive workflows** — structured support for authorized reconnaissance, enumeration, web/API assessment, vulnerability validation, password auditing, wireless assessment, reverse engineering, and security-research labs.
- **Lab Manager** — discovery of container/VM runtimes and local lab definitions, plus review-only lifecycle plans.
- **Security Assistant** — local-first copilot that reads the current KachySec state and helps explain, plan, and learn during security work.
- **Reproducible packaging** — native Arch/CachyOS PKGBUILD.
- **CI and tests** — automated Python test suite.

## Quick start

### Clone

```bash
git clone https://github.com/UseBrainNoL0ve/KachyOS.git
cd KachyOS
```

### Install

Development checkout:

```bash
python -m pip install --user .
```

Native CachyOS/Arch package:

```bash
makepkg -si
```

If packaging prerequisites are missing:

```bash
sudo pacman -S python python-pip python-build python-installer python-setuptools
```

Optional GUI dependency:

```bash
sudo pacman -S pyside6
```

### Verify

```bash
kachysec --help
kachysec status
kachysec audit
kachysec telemetry
```

### Launch

```bash
kachysec gui
```

The dashboard refreshes automatically every 10 seconds and also has a manual Refresh action.

## Command reference

| Command | What it does | Host changes |
| --- | --- | --- |
| `kachysec baseline` | Collects a read-only host inventory | No |
| `kachysec status` | Shows workstation health and tool/runtime summary | No |
| `kachysec audit` | Runs a lightweight security posture audit | No |
| `kachysec updates` | Shows pending pacman updates | No |
| `kachysec telemetry` | Shows local host telemetry and saves one local snapshot | No |
| `kachysec telemetry --history` | Shows recent saved telemetry snapshots | No |
| `kachysec assistant "..."` | Ask the local security copilot | No |
| `kachysec assistant --providers` | List available local assistant providers | No |
| `kachysec baseline-diff --latest` | Compares the two newest saved baseline snapshots | No |
| `kachysec tools` | Lists the security catalog | No |
| `kachysec tools --missing` | Lists missing catalog entries | No |
| `kachysec tools --category web` | Filters one discipline | No |
| `kachysec tools --plan` | Builds a pacman package plan | No |
| `kachysec tools --install` | Installs the reviewed package plan after explicit confirmation | **Yes** |
| `kachysec lab` | Discovers local lab runtimes and definitions | No |
| `kachysec lab --plan` | Builds a review-only lab lifecycle plan | No |
| `kachysec gui` | Opens the optional desktop dashboard | No |

## First-run workflow

```bash
mkdir -p reports
kachysec baseline --format markdown --output reports/baseline.md
kachysec status
kachysec tools --missing
kachysec tools --plan
kachysec audit
kachysec updates
kachysec telemetry
kachysec assistant "Explain the most important audit warning and what I should verify next."
kachysec lab --plan
kachysec gui
```

When package installation is deliberately required, review the exact plan first:

```bash
kachysec tools --plan
kachysec tools --install
```

The install command asks for the literal confirmation token `INSTALL`, then invokes `sudo pacman -S --needed ...` and records the operation in local JSONL state.

## GUI guide

### Overview

Live workstation coverage, update count, audit state, runtime availability, and the current safe-by-design workflow.

### Tools

Search by name, category, purpose, or binary. Filter by category and select a tool to inspect its purpose, executable, scope, installed state, package candidates, and verification command.

**Build Install Plan** previews the exact package operation without installing anything.

### Audit

Displays read-only posture checks with evidence and review guidance.

### Updates

Shows package version transitions reported by `pacman -Qu`. KachySec does not silently apply system updates.

### Labs

Shows container/VM tooling and discovered local lab definitions. The current lifecycle planner is review-only; it does not create or start containers or virtual machines.

### Telemetry

Shows local host telemetry. The collector is observation-only and does not probe remote hosts or perform remediation.

### Assistant

The Assistant tab provides an always-available local cybersecurity copilot. It receives a read-only KachySec status/audit/tool snapshot, answers asynchronously so the GUI stays responsive, and keeps commands as reviewable suggestions rather than executing them.

The default provider is local Ollama. The model field can be changed without modifying the workstation configuration.

### History

Shows recent locally recorded privileged operations from `~/.local/state/kachysec/operations.jsonl`. This state stays on the host and is never committed automatically.

## Architecture

```text
CachyOS host
    │
    └── KachySec
        ├── baseline
        ├── status
        ├── audit
        ├── updates
        ├── telemetry
        ├── tool catalog
        ├── tool manager
        ├── operations + local audit trail
        ├── lab manager
        ├── security assistant
        └── PySide6 GUI
             ├── Overview
             ├── Assistant
             ├── Tools
             ├── Audit
             ├── Updates
             ├── Labs
             ├── Telemetry
             └── History
```

Core services are separate from presentation, so CLI and GUI consume the same logic.

## Security model

KachySec is designed for systems and environments the operator owns or is explicitly authorized to test.

Current automation is deliberately conservative:

- discovery before modification;
- package planning before installation;
- no automatic bulk installation;
- privileged package changes require an explicit confirmation;
- no automatic service or firewall changes;
- telemetry is local observation only;
- no unattended remote attack execution from the dashboard;
- offensive workflows are intended for owned or explicitly authorized targets;
- commands should be reviewable before execution and bounded by an explicit scope;
- lab lifecycle planning is review-only until a separate execution layer is introduced;
- reports and local state may contain host-specific information and should be reviewed before publication.

Tool catalog inclusion is not authorization to use a tool against a third-party system.

## Documentation

- [Installation](docs/INSTALL.md)
- [Usage Guide](docs/USAGE.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Security Core](docs/SECURITY_CORE.md)
- [Audit](docs/AUDIT.md)
- [Package Updates](docs/UPDATES.md)
- [Tool Manager](docs/TOOL_MANAGER.md)
- [Operations](docs/OPERATIONS.md)
- [Lab Manager](docs/LABS.md)
- [Authorized Offensive Workflows](docs/OFFENSIVE_WORKFLOWS.md)
- [Security Assistant](docs/ASSISTANT.md)
- [Telemetry](docs/TELEMETRY.md)
- [Telemetry history](docs/TELEMETRY_HISTORY.md)
- [Evidence](docs/EVIDENCE.md)
- [GUI](docs/GUI.md)
- [CI](docs/CI.md)
- [Package Manager](docs/PACKAGE_MANAGER.md)

## Development

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the same test suite on pushes and pull requests.

## Project status

**Implemented:** Phase 0 baseline, Phase 1 security-core foundations, dual-use security tool catalog/manager, read-only audit and update services, explicit package operations with local history, lab-runtime discovery and review-only planning, defensive telemetry, baseline evidence snapshots/diffing, authorized offensive-workflow documentation, the PySide6 dashboard, and a local-first security assistant.

**Next engineering layer:** event timeline, evidence/report generation, non-blocking live monitoring, and controlled lab lifecycle execution with verification.

## License

MIT. See the repository license metadata.
