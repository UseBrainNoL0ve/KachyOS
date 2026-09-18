# Package Updates

KachySec can inspect pending Arch/CachyOS package updates without changing the host.

## CLI

kachysec updates

The command reads pacman -Qu and renders the package name, current version, and available version.

## Safety model

The update service is intentionally read-only. It does not run pacman -Syu, install packages, remove packages, or modify repositories.

The Tool Manager exposes an install-plan builder. It resolves locally available pacman candidates, deduplicates package names, and only renders a plan; execution remains a separate, explicit operation.

## Why this exists

The update layer gives the future GUI a stable service boundary: the dashboard can show update state without implementing package-manager subprocess logic itself.
