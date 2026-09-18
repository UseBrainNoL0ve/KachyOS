# Tool Manager

The tool manager is intentionally split into inspection and execution.

## Current capabilities

- Inspect native pacman package candidates.
- Detect whether candidate packages are installed.
- Build a deduplicated installation plan.
- Render the plan without modifying the host.

## Safety boundary

The current implementation does not execute package installation.

The intended workflow is:

1. inspect the selected tool metadata;
2. resolve native package candidates;
3. show the exact package plan;
4. require explicit confirmation;
5. perform a privileged package operation;
6. verify the resulting tool state.

This prevents a GUI refresh or accidental click from becoming an implicit system modification.

## GUI integration

The same manager API is intended for the future Tool Manager panel. The GUI should show package candidates, installation state, and the exact proposed operation before any privileged action is introduced.
