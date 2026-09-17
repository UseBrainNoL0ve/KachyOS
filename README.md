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

## Current status

The project already has a read-only host baseline collector and a broad tool-universe catalog. The catalog covers network, web, vulnerability assessment, OSINT, forensics, reverse engineering, password auditing, wireless, lab infrastructure, observability and analysis utilities.

The workstation is designed to run directly on the CachyOS host. A native Arch/CachyOS `PKGBUILD` is included for the eventual system installation path; the project does not require a local Python virtual environment.

## Security scope

Automation is designed for systems and environments the user owns or is explicitly authorized to test. The catalog does not imply that every tool should be installed or used against arbitrary systems.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md).
