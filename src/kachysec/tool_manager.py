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


def _run(command: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return result.returncode, (result.stdout or "").strip()


def _installed(package: str) -> bool:
    code, _ = _run(["pacman", "-Q", package])
    return code == 0


def inspect_candidates(spec: ToolSpec) -> list[PackageCandidate]:
    return [
        PackageCandidate(
            spec.name,
            package,
            _installed(package) if shutil.which("pacman") else False,
            bool(shutil.which("pacman")) and _run(["pacman", "-Si", package])[0] == 0,
        )
        for package in spec.packages
    ]


def build_install_plan(specs: list[ToolSpec]) -> InstallPlan:
    packages: list[str] = []
    tools: list[str] = []
    for spec in specs:
        candidate = next(
            (c for c in inspect_candidates(spec) if c.available and not c.installed),
            None,
        )
        if candidate:
            packages.append(candidate.package)
            tools.append(spec.name)
    return InstallPlan(tuple(dict.fromkeys(packages)), tuple(tools))


def render_plan(plan: InstallPlan) -> str:
    lines = ["KachySec tool installation plan (no changes)", ""]
    if not plan.packages:
        lines.append("No installable missing tool packages were detected.")
        return "\n".join(lines) + "\n"
    lines.append(f"Packages: {len(plan.packages)}")
    lines.extend(f"- {package}" for package in plan.packages)
    lines.append("")
    lines.append("This is a plan only. No package installation was executed.")
    return "\n".join(lines) + "\n"
