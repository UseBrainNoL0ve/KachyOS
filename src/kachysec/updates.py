from __future__ import annotations

from dataclasses import dataclass
import shutil
import subprocess


@dataclass(frozen=True)
class PackageUpdate:
    name: str
    current: str
    available: str
    repository: str = ""


def _run(command: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return result.returncode, (result.stdout or result.stderr).strip()


def _parse_pacman_updates(output: str) -> list[PackageUpdate]:
    updates: list[PackageUpdate] = []
    for line in output.splitlines():
        line = line.strip()
        if not line or line.startswith("::"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        name, versions = parts[0], parts[1]
        if "->" not in versions:
            continue
        current, available = versions.split("->", 1)
        repository = parts[2] if len(parts) > 2 else ""
        updates.append(PackageUpdate(name, current, available, repository))
    return updates


def collect_updates() -> list[PackageUpdate]:
    if not shutil.which("pacman"):
        return []
    code, output = _run(["pacman", "-Qu"])
    if code != 0:
        return []
    return _parse_pacman_updates(output)


def render_updates(updates: list[PackageUpdate]) -> str:
    lines = ["KachySec package updates (read-only)", ""]
    if not updates:
        lines.append("No pending package updates reported by pacman.")
        return "\n".join(lines) + "\n"
    lines.append(f"{len(updates)} update(s) available:")
    for update in updates:
        repo = f" [{update.repository}]" if update.repository else ""
        lines.append(f"- {update.name}: {update.current} -> {update.available}{repo}")
    lines.append("")
    lines.append("No packages were installed or modified.")
    return "\n".join(lines) + "\n"
