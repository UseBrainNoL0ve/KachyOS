# Roadmap

## Phase 0 — Baseline

- Detect CachyOS version and kernel
- Inventory hardware and network interfaces
- Check firewall state
- Check virtualization/container prerequisites
- Record package manager state

## Phase 1 — Security Core

- Establish a clean security-tools taxonomy
- Add reproducible package definitions
- Add tool presence/version checks
- Add system health checks

## Phase 2 — CLI

Planned commands:

```text
sec status
sec tools
sec update
sec audit
sec network
sec lab
sec report
```

## Phase 3 — Lab Infrastructure

- Podman/Docker integration
- KVM/QEMU checks
- Isolated training networks
- Reproducible local vulnerable targets
- Lab lifecycle commands

## Phase 4 — GUI

- Security dashboard
- Tool manager
- Lab manager
- Network overview
- System health
- Reports/events view

## Phase 5 — Quality

- Unit tests
- Integration tests
- Shell/Python linting
- CI
- Documentation
- Release/versioning workflow

## Design principle

Every feature should either teach a concrete security/software-engineering concept, improve workstation usability, or make the environment more reproducible. Avoid installing tools merely for the appearance of a Kali-like environment.
