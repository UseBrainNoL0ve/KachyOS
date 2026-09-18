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

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests
kachysec baseline --output reports/baseline.md
kachysec baseline --format json --output reports/baseline.json
```

Reports are local diagnostics and should be reviewed before any host-changing automation is introduced.
