# Roadmap

## Completed foundation

### Phase 0 — Baseline
- CachyOS/platform and kernel detection
- Hardware and network inventory
- Firewall and virtualization/container checks
- Package-manager state
- Read-only reporting

### Phase 1 — Security Core
- Security-tool taxonomy
- Tool presence/version checks
- Runtime checks
- Read-only security audit
- Package update inspection
- Native package metadata and planning

### Control Plane
- Explicit package installation with confirmation
- Local JSONL operation history
- Review-only lab lifecycle planning
- Defensive host telemetry
- PySide6 dashboard with shared service APIs
- Native PKGBUILD, tests, CI, and documentation

## Next milestones

### Phase 2 — Evidence and change verification
- Persistent telemetry history
- Baseline snapshot storage
- Baseline diff engine
- Post-operation verification
- Evidence bundles
- Markdown/JSON/HTML security reports

### Phase 3 — SOC-lite monitoring
- Event timeline
- Process/socket detail views
- Bounded local event history
- Non-blocking live GUI monitoring
- Alert-oriented observations without automatic remediation

### Phase 4 — Controlled lab lifecycle
- Explicit lab execution plans
- Local/isolated container lifecycle
- VM lifecycle with explicit boundaries
- Preflight and postflight verification
- Teardown and cleanup
- Operation history integration

### Phase 5 — Quality and release
- Broader integration tests
- Static analysis and linting
- Documentation consistency checks
- Release/versioning workflow
- Reproducible package builds

## Design principle

Every feature should teach a concrete security/software-engineering concept, improve workstation usability, or make the environment more reproducible. Avoid installing tools merely for the appearance of a Kali-like environment.
