from __future__ import annotations

from dataclasses import dataclass
import shutil
import subprocess
from typing import Iterable

from .tools import ToolSpec


@dataclass(frozen=True)
class PackageState:
    package: str
    installed: bool
    version: str = ""


def _run(command: list[str], timeout: int = 5) -> tuple[int, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return result.returncode, (result.stdout or result.stderr).strip()


def pacman_available() -> bool:
    return shutil.which("pacman") is not None


def package_state(package: str) -> PackageState:
    if not pacman_available():
        return PackageState(package, False)
    code, output = _run(["pacman", "-Q", package])
    if code != 0 or not output:
        return PackageState(package, False)
    parts = output.split()
    return PackageState(package, True, parts[-1] if len(parts) >= 2 else "")


def inspect_tool_packages(spec: ToolSpec) -> list[PackageState]:
    return [package_state(package) for package in spec.packages]


def summarize_package_states(states: Iterable[PackageState]) -> dict[str, int]:
    items = list(states)
    installed = sum(1 for state in items if state.installed)
    return {"total": len(items), "installed": installed, "missing": len(items) - installed}


def build_install_plan(specs: Iterable[ToolSpec]) -> list[str]:
    """Return candidate package names only; never executes a package install."""
    plan: list[str] = []
    seen: set[str] = set()
    for spec in specs:
        for package in spec.packages:
            if package not in seen:
                seen.add(package)
                plan.append(package)
    return plan
