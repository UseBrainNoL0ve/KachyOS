# Package Manager Abstraction

The package-manager service is the boundary between KachySec and the native CachyOS/Arch package manager.

Current capabilities:

- detect whether pacman is available;
- inspect whether a candidate package is installed;
- read the installed version;
- build a unique package installation plan without executing it.

No package installation or removal is performed by this layer.

The design keeps privileged host changes outside discovery code. A later explicit package-management feature can add confirmation, privilege handling, logging, and rollback-aware UX without coupling those concerns to the tool catalog.
