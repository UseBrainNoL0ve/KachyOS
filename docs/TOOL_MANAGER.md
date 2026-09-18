# Tool Manager

The Tool Manager connects KachySec's security-tool catalog to the native pacman package manager without turning catalog inspection into implicit installation.

## Current capabilities

- Inspect native pacman package candidates.
- Detect whether candidate packages are installed.
- Resolve locally available candidates in a batched planning operation.
- Deduplicate package names across the catalog.
- Render an exact installation plan without modifying the host.
- Feed the same plan into the explicit package-operation layer.

## CLI

Preview a plan:

```bash
kachysec tools --plan
```

Execute a reviewed plan:

```bash
kachysec tools --install
```

The install command prints the exact package list and requires the literal confirmation token `INSTALL` before running:

```text
sudo pacman -S --needed <packages...>
```

The operation is recorded in local JSONL state after it finishes.

## GUI integration

The GUI can inspect individual tool metadata and build a complete installation plan. The GUI itself does not execute package installation.

## Lifecycle

The intended package lifecycle is:

**discover → inspect → resolve candidates → exact plan → review → explicit confirmation → privileged operation → verify**

Keeping these stages separate prevents a dashboard refresh or catalog lookup from becoming an unexpected system modification.

## Safety boundary

The catalog describes tools; it does not grant authorization to use them. Security tooling should only be operated against systems and environments the operator owns or is explicitly authorized to test.
