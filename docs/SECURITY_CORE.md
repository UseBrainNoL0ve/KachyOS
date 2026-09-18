# Phase 1 — Security Core

Phase 1 turns the baseline collector into a security-workstation control plane.

## Commands

```bash
kachysec status
kachysec tools
kachysec tools --missing
kachysec tools --category network
```

`status` reports host prerequisites, runtime presence, and the current tool inventory.
`tools` exposes the catalog without installing anything.

## Tool universe

The catalog is deliberately broad rather than a short "top tools" list. It covers:

- network diagnostics and packet analysis
- web and API security tooling
- vulnerability assessment
- Linux hardening and malware defense
- OSINT and asset discovery
- digital forensics and incident response
- reverse engineering and debugging
- password auditing for owned labs
- wireless security diagnostics
- containers and virtual machines
- observability and performance analysis
- file, archive, metadata and report analysis
- development and GitHub workflow utilities

Each entry records a human-readable purpose, executable used for detection, verification command, candidate native package name, and scope. This lets the GUI and CLI present the same inventory later without maintaining separate lists.

The catalog is an inventory layer, not an automatic installer. A missing tool does not cause package installation, service changes, network changes, or privilege escalation.

## Installation model

The workstation target is the host system itself: no project-local Python virtual environment is required. Native Arch/CachyOS packaging will be added as the installation path so the resulting `kachysec` command behaves like a normal system utility.

## Design rules

- Discovery is separated from installation.
- Native CachyOS/Arch packages remain the preferred installation source where practical.
- Tool presence is reported without assuming that every workstation needs every tool.
- GUI and CLI will consume the same catalog and core APIs.
- Security operations remain scoped to systems and environments the operator owns or is explicitly authorized to test.
- High-impact operations require an explicit user action rather than a background refresh.
