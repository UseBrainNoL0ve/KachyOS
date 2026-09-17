# Architecture

KachyOS is an additive security layer for an existing CachyOS installation.

```text
CachyOS
  |
  +-- Existing desktop/theme/workflow
  |
  +-- Security Workstation Layer
        |
        +-- Core checks
        +-- Tool catalog
        +-- CLI automation
        +-- GUI dashboard
        +-- Lab orchestration
        +-- Reports and logs
        +-- Tests / CI
```

## Principles

1. Do not replace the host desktop environment.
2. Prefer native Arch/CachyOS packages where practical.
3. Keep optional tooling modular so the base system remains maintainable.
4. Separate host management from isolated lab environments.
5. Make privileged operations explicit and auditable.
6. Prefer read-only discovery before making system changes.
7. Test automation before applying it to the host.
