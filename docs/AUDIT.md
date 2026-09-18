# Read-only security audit

`kachysec audit` provides a host-local security posture snapshot without changing the system.

## Checks

The first audit layer covers:

- firewall tooling and reported state
- pending Arch package updates via `pacman -Qu`
- failed systemd units
- SSH service state
- Podman, Docker, QEMU and libvirt availability
- basic permissions on selected sensitive system files

Each check reports `PASS`, `WARN`, or `INFO`, plus evidence and a remediation hint when useful.

## Safety model

The audit is intentionally read-only. It does not install packages, enable or disable services, alter firewall rules, modify permissions, scan remote hosts, or execute exploitation workflows.

A `WARN` is an observation, not proof of compromise or a complete security assessment. Findings should be investigated with the underlying system tools before making changes.

## CLI

```bash
kachysec audit
```

The GUI will consume the same audit API so that CLI and GUI results stay consistent.
