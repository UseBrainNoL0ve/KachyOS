# Phase 1 — Security Core

Phase 1 turns the baseline collector into a security-workstation control plane.

## Commands

```bash
kachysec status
kachysec tools
kachysec tools --missing
kachysec tools --category network
kachysec audit
kachysec updates
kachysec telemetry
```

## Tool universe

The catalog covers:

- network diagnostics and packet analysis;
- web and API security tooling;
- vulnerability assessment;
- Linux hardening and malware defense;
- OSINT and asset discovery;
- digital forensics and incident response;
- reverse engineering and debugging;
- password auditing for owned/authorized labs;
- wireless security diagnostics;
- containers and virtual machines;
- observability and performance analysis;
- file, archive, metadata, and report analysis;
- development and GitHub workflow utilities.

Each entry records a human-readable purpose, executable used for detection, verification command, candidate native package name, and scope.

The catalog is an inventory layer, not an automatic installer. Missing tools do not trigger package installation, service changes, network changes, or privilege escalation.

## Installation model

The workstation target is the host system itself. Native Arch/CachyOS packaging is the preferred installation path where practical.

The Tool Manager separates candidate resolution and plan generation from privileged execution.

## Design rules

- Discovery is separated from installation.
- Native packages remain the preferred source where practical.
- Tool presence is reported without assuming every workstation needs every tool.
- CLI and GUI consume the same service layer.
- High-impact operations require explicit user action.
- Security operations remain scoped to systems and environments the operator owns or is explicitly authorized to test.
