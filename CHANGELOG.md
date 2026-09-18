# Changelog

## Unreleased

### Security assistant milestone
- Added a local-first KachySec Assistant backed by an optional Ollama provider.
- Added read-only workstation context to assistant prompts.
- Added CLI and asynchronous GUI chat support.
- Kept assistant actions advisory: no autonomous command execution or target selection.


### SOC-lite telemetry milestone
- Added bounded local telemetry history under `~/.local/state/kachysec/telemetry/`.
- Added `kachysec telemetry --history` and GUI history rendering.
- Kept telemetry storage local and observation-only.

### Evidence milestone
- Added persistent local baseline snapshots and structural baseline diffing.
- Added `baseline-diff --latest` for quick before/after inspection.
- Kept evidence artifacts local by default to reduce accidental host-data publication.

### Large milestone
- Added review-only lab orchestration plans with explicit isolation metadata.
- Batched pacman package resolution to reduce catalog planning overhead.
- Added explicit package installation with confirmation and local operation history.
- Added GUI operation history visibility.

### Added
- Expanded security-tool catalog and package metadata.
- Read-only Tool Manager with pacman candidate inspection and install-plan generation.
- PySide6 dashboard with automatic refresh, category filtering and tool detail inspection.
- Lab Manager for container/VM runtime discovery.
- CLI commands for tool planning and lab discovery.
- Installation and usage documentation.
- Additional unit tests and GitHub Actions coverage.

### Safety
- Package installation remains an explicit, confirmation-gated operation.
- Lab lifecycle operations remain read-only in the current release.
