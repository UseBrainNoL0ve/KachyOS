# Phase 1 — Security Core

Phase 1 turns the baseline collector into a small security-workstation control plane.

## Commands

```bash
kachysec status
kachysec tools
kachysec tools --missing
kachysec tools --category network
```

`status` reports host prerequisites, runtime presence, and the current tool inventory.
`tools` exposes a categorized catalog without installing anything.

## Design rules

- Discovery is separated from installation.
- Native CachyOS/Arch packages remain the preferred installation source where practical.
- Tool presence is reported without assuming that every workstation needs every tool.
- Security operations remain scoped to systems and environments the operator owns or is explicitly authorized to test.
