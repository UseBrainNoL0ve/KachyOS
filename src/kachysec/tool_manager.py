from __future__ import annotations

from dataclasses import dataclass
import shutil
import subprocess

from .tools import ToolSpec


@dataclass(frozen=True)
class PackageCandidate:
    tool: str
    package: str
    installed: bool
    available: bool


@dataclass(frozen=True)
class InstallPlan:
    packages: tuple[str, ...]
    tools: tuple[str, ...]


def _run(command: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return result.returncode, (result.stdout or result.stderr).strip()


def _pacman_available() -> bool:
    return shutil.which("pacman") is not None


def _installed_packages() -> set[str]:
    if not _pacman_available():
        return set()
    code, output = _run(["pacman", "-Qq"], timeout=30)
    return set(output.splitlines()) if code == 0 else set()


def _available_packages(packages: set[str]) -> set[str]:
    if not packages or not _pacman_available():
        return set()
    code, output = _run(["pacman", "-Ssq", *sorted(packages)], timeout=30)
    if code != 0:
        return set()
    available = set(output.splitlines())
    return packages & available


def inspect_candidates(spec: ToolSpec) -> list[PackageCandidate]:
    installed = _installed_packages()
    available = _available_packages(set(spec.packages))
    return [
        PackageCandidate(spec.name, package, package in installed, package in available)
        for package in spec.packages
    ]


def build_install_plan(specs: list[ToolSpec]) -> InstallPlan:
    if not _pacman_available():
        return InstallPlan((), ())
    all_packages = {package for spec in specs for package in spec.packages}
    installed = _installed_packages()
    available = _available_packages(all_packages)
    packages: list[str] = []
    tools: list[str] = []
    for spec in specs:
        candidate = next(
            (package for package in spec.packages if package in available and package not in installed),
            None,
        )
        if candidate:
            packages.append(candidate)
            tools.append(spec.name)
    return InstallPlan(tuple(dict.fromkeys(packages)), tuple(tools))


def render_plan(plan: InstallPlan) -> str:
    lines = ["KachySec tool installation plan (no changes)", ""]
    if not plan.packages:
        lines.append("No installable missing tool packages were detected.")
        return "\n".join(lines) + "\n"
    lines.append(f"Packages: {len(plan.packages)}")
    lines.extend(f"- {package}" for package in plan.packages)
    lines.extend(("", f"Tools covered: {len(plan.tools)}", "This is a plan only. No package installation was executed."))
    return "\n".join(lines) + "\n"
