# Contributing

## Development setup

KachySec targets Python 3.11+ on CachyOS/Arch Linux.

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

## Design rules

- Keep host discovery read-only unless a change operation is explicitly designed and reviewed.
- Keep privileged operations separate from discovery and planning.
- Prefer standard-library implementations for host inspection where practical.
- Keep CLI and GUI logic dependent on shared service modules rather than duplicating subprocess logic.
- Add tests for new parsing, planning and state-collection behavior.
- Document security scope and side effects for new operations.

## Pull requests

A useful pull request should explain:

1. what changed;
2. why it changed;
3. what was tested;
4. whether it can modify the host, network or lab state;
5. any new dependency or packaging requirement.
