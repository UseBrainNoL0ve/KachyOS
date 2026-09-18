# Package Manager Abstraction

The package-manager layer is the boundary between KachySec and the native CachyOS/Arch package manager.

## Current capabilities

- Detect whether `pacman` is available.
- Inspect installed package names.
- Resolve locally available candidate package names.
- Build a unique package installation plan without executing it.
- Hand the reviewed plan to the explicit operations layer.

## Change boundary

Package installation is not part of discovery.

The explicit CLI operation `kachysec tools --install`:

1. builds the current package plan;
2. prints the exact packages;
3. requires the literal `INSTALL` confirmation;
4. invokes `sudo pacman -S --needed ...`;
5. records the result locally.

This keeps privileged host changes outside catalog and discovery code.

## Future work

A stronger package abstraction can add:

- post-install verification;
- transaction-aware evidence;
- failure classification;
- rollback-aware UX where the package manager supports it;
- better candidate metadata and repository provenance.
