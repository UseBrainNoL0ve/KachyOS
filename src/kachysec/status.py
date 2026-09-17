from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass

from .tools import check_tools, summarize_tools


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def command_version(command: list[str]) -> str | None:
    if shutil.which(command[0]) is None:
        return None
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else None


def collect_status() -> dict[str, object]:
    tools = check_tools()
    tool_summary = summarize_tools(tools)
    checks = [
        Check("platform", "ok", f"{platform.system()} {platform.release()} ({platform.machine()})"),
        Check("python", "ok", platform.python_version()),
        Check("pacman", "ok" if shutil.which("pacman") else "missing", "native package manager"),
        Check("iproute2", "ok" if shutil.which("ip") else "missing", "network diagnostics"),
        Check("systemctl", "ok" if shutil.which("systemctl") else "missing", "service inspection"),
    ]
    return {
        "checks": [check.__dict__ for check in checks],
        "tools": tool_summary,
        "runtimes": {
            "podman": command_version(["podman", "--version"]),
            "docker": command_version(["docker", "--version"]),
            "qemu": command_version(["qemu-system-x86_64", "--version"]),
            "virsh": command_version(["virsh", "--version"]),
        },
    }


def render_status(data: dict[str, object]) -> str:
    lines = ["KACHYSEC STATUS", "=" * 14, ""]
    for check in data["checks"]:  # type: ignore[index]
        lines.append(f"[{check['status'].upper():7}] {check['name']}: {check['detail']}")
    tools = data["tools"]  # type: ignore[assignment]
    lines.extend([
        "",
        "SECURITY TOOLS",
        "--------------",
        f"Installed: {tools['installed']}",
        f"Missing:   {tools['missing']}",
        f"Catalog:   {tools['total']}",
        "",
        "RUNTIMES",
        "--------",
    ])
    for name, version in data["runtimes"].items():  # type: ignore[index]
        lines.append(f"{name:8}: {version or 'not found'}")
    return "\n".join(lines) + "\n"
