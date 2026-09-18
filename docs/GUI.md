# Security Dashboard

KachySec includes an optional PySide6 dashboard built on the same read-only service APIs used by the CLI.

## Current panels

- Overview cards for tool coverage, updates, audit warnings, and runtimes.
- Searchable tool catalog.
- Read-only security audit.
- Package update visibility.
- System/runtime status.

The dashboard refreshes automatically and also exposes a manual Refresh action.

## Native CachyOS workflow

Arch Linux ships PySide6 as the pyside6 package in the Extra repository. The GUI can therefore remain a native system dependency instead of requiring a project-local Python virtual environment.

The GUI intentionally performs discovery only. It does not install packages, change firewall rules, modify services, or perform active network probing.
