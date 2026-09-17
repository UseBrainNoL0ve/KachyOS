# Phase 0 — Baseline Scanner

The baseline scanner establishes a read-only snapshot of the CachyOS host before security tooling or configuration changes are introduced.

## What it collects

- Kernel and platform information
- CPU, memory, GPU and block-device information
- Network addresses, routes and listening sockets
- Firewall service state where available
- Container and virtualization runtime presence
- Installed package count
- Presence of selected security engineering tools

## Safety model

The scanner is intentionally read-only. It does not install packages, change firewall rules, modify services, create users, alter networking, or perform active network probing.

## Local usage

The workstation is designed to run natively on CachyOS rather than requiring a persistent project-local Python virtual environment. For development, use the repository's native package/build workflow or an isolated CI environment.

Typical installed usage:

```bash
kachysec baseline --output reports/baseline.md
kachysec baseline --format json --output reports/baseline.json
```

Run the test suite from a development checkout with the project's configured Python tooling.

## Privacy

Baseline reports can contain local IP addresses, hostnames, mount paths, socket information and other host-specific metadata. Keep reports local by default and redact sensitive details before sharing or committing anything publicly.
