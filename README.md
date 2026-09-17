# KachyOS Security Workstation

A modular cybersecurity workstation layer built on top of CachyOS.

> The goal is not to replace CachyOS or imitate its desktop environment. KachyOS keeps the existing system identity and adds a structured, reproducible security engineering toolkit around it.

## Goals

- Preserve the existing CachyOS desktop, theme and workflow.
- Organize security tooling by discipline instead of installing an unstructured tool dump.
- Provide reproducible setup and health checks.
- Support isolated local labs, containers and virtual machines.
- Build useful GUI and CLI automation for defensive security engineering and authorized testing.
- Keep configuration auditable and GitHub-friendly.

## Planned modules

- `core/` — system checks, package state and prerequisites
- `tools/` — security tool definitions and installation metadata
- `cli/` — command-line management interface
- `gui/` — local security dashboard
- `labs/` — isolated training/lab environments
- `docs/` — architecture, setup and learning notes
- `tests/` — automated tests

## Security scope

Automation is designed for systems and environments the user owns or is explicitly authorized to test. The project intentionally avoids destructive or unauthorized attack automation.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md).
