from __future__ import annotations

import json
import platform
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CommandResult:
    command: str
    available: bool
    returncode: int | None
    stdout: str
    stderr: str


def run_command(command: list[str], timeout: int = 10) -> CommandResult:
    name = command[0]
    if shutil.which(name) is None:
        return CommandResult(" ".join(command), False, None, "", f"{name}: not found")
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return CommandResult(" ".join(command), True, None, "", str(exc))
    return CommandResult(
        " ".join(command),
        True,
        completed.returncode,
        completed.stdout.strip(),
        completed.stderr.strip(),
    )


def first_line(result: CommandResult) -> str | None:
    return result.stdout.splitlines()[0] if result.stdout else None


def collect() -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    os_release = Path("/etc/os-release").read_text(encoding="utf-8", errors="replace") if Path("/etc/os-release").exists() else ""

    commands: dict[str, list[str]] = {
        "kernel": ["uname", "-srvm"],
        "cpu": ["lscpu"],
        "memory": ["free", "-h"],
        "gpu": ["lspci"],
        "block_devices": ["lsblk", "-o", "NAME,SIZE,FSTYPE,MOUNTPOINTS"],
        "network_addresses": ["ip", "-br", "addr"],
        "routes": ["ip", "route"],
        "listening_sockets": ["ss", "-lntup"],
        "virtualization": ["systemd-detect-virt", "--vm"],
    }

    results: dict[str, Any] = {}
    for key, command in commands.items():
        result = run_command(command)
        if key == "gpu" and result.stdout:
            lines = [line for line in result.stdout.splitlines() if "VGA compatible controller" in line or "3D controller" in line or "Display controller" in line]
            result.stdout = "\n".join(lines)
        results[key] = asdict(result)

    tools = [
        "nmap", "tshark", "tcpdump", "wireshark", "burpsuite", "nuclei",
        "ghidra", "radare2", "gdb", "strace", "ltrace", "yara", "binwalk",
        "sleuthkit", "hashcat", "john", "ffuf", "gobuster", "sqlmap",
        "nikto", "mitmproxy", "lynis", "clamav",
    ]
    tool_presence = {tool: shutil.which(tool) is not None for tool in tools}

    package_result = run_command(["pacman", "-Qq"])
    package_count = len(package_result.stdout.splitlines()) if package_result.returncode == 0 else None

    firewall_candidates = {}
    for service in ("ufw", "firewalld"):
        status = run_command(["systemctl", "is-active", service])
        enabled = run_command(["systemctl", "is-enabled", service])
        firewall_candidates[service] = {
            "active": first_line(status),
            "enabled": first_line(enabled),
        }
    nft = run_command(["nft", "list", "ruleset"])
    firewall_candidates["nftables"] = {
        "available": nft.available,
        "has_rules": bool(nft.stdout) if nft.returncode == 0 else None,
    }

    runtimes = {
        name: first_line(run_command(command))
        for name, command in {
            "podman": ["podman", "--version"],
            "docker": ["docker", "--version"],
            "qemu": ["qemu-system-x86_64", "--version"],
            "virsh": ["virsh", "--version"],
        }.items()
    }

    return {
        "schema_version": 1,
        "collected_at": now,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "os_release": os_release,
        "package_count": package_count,
        "firewall": firewall_candidates,
        "runtimes": runtimes,
        "security_tools": tool_presence,
        "commands": results,
    }


def to_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def to_markdown(data: dict[str, Any]) -> str:
    lines = [
        "# KachyOS Baseline Report",
        "",
        f"- Collected: `{data['collected_at']}`",
        f"- Platform: `{data['platform']['system']} {data['platform']['release']}`",
        f"- Architecture: `{data['platform']['machine']}`",
        f"- Python: `{data['platform']['python']}`",
        f"- Installed packages: `{data['package_count'] if data['package_count'] is not None else 'unknown'}`",
        "",
        "## Security Tool Presence",
        "",
    ]
    for tool, present in data["security_tools"].items():
        lines.append(f"- {'[x]' if present else '[ ]'} `{tool}`")
    lines.extend(["", "## Firewall", ""])
    for name, state in data["firewall"].items():
        if isinstance(state, dict):
            details = ", ".join(f"{k}={v}" for k, v in state.items())
            lines.append(f"- `{name}`: {details}")
    lines.extend(["", "## Runtimes", ""])
    for name, version in data["runtimes"].items():
        lines.append(f"- `{name}`: `{version or 'not found'}`")
    lines.extend(["", "## Network", "", "```text", data["commands"]["network_addresses"]["stdout"], "```", "", "## Listening Sockets", "", "```text", data["commands"]["listening_sockets"]["stdout"], "```", ""])
    return "\n".join(lines)
