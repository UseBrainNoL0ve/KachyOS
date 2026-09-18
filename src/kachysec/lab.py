from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess


@dataclass(frozen=True)
class RuntimeStatus:
    name: str
    binary: str
    installed: bool
    version: str = ""


@dataclass(frozen=True)
class LabDefinition:
    name: str
    path: str
    kind: str
    description: str


DEFAULT_LABS = (
    LabDefinition("containers", "labs/containers", "podman/docker", "Container-based isolated training environments."),
    LabDefinition("virtual-machines", "labs/vms", "qemu/libvirt", "VM-based isolated training environments."),
)


def _run(command: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return result.returncode, (result.stdout or result.stderr).strip()


def collect_runtimes() -> list[RuntimeStatus]:
    probes = (
        ("Podman", "podman", ["podman", "--version"]),
        ("Docker", "docker", ["docker", "--version"]),
        ("QEMU", "qemu-system-x86_64", ["qemu-system-x86_64", "--version"]),
        ("libvirt", "virsh", ["virsh", "--version"]),
        ("virt-manager", "virt-manager", ["virt-manager", "--version"]),
    )
    result = []
    for name, binary, command in probes:
        installed = shutil.which(binary) is not None
        version = _run(command)[1] if installed else ""
        result.append(RuntimeStatus(name, binary, installed, version.splitlines()[0] if version else ""))
    return result


def discover_labs(root: Path | None = None) -> list[LabDefinition]:
    base = root or Path.cwd()
    return [
        lab for lab in DEFAULT_LABS
        if (base / lab.path).exists()
    ]


def render_lab_status(runtimes: list[RuntimeStatus], labs: list[LabDefinition]) -> str:
    lines = ["KachySec lab manager (read-only)", ""]
    lines.append("Runtimes:")
    for runtime in runtimes:
        marker = "[+]" if runtime.installed else "[-]"
        suffix = f" — {runtime.version}" if runtime.version else ""
        lines.append(f"{marker} {runtime.name}{suffix}")
    lines.extend(("", "Lab definitions:"))
    if labs:
        lines.extend(f"- {lab.name} [{lab.kind}] — {lab.description}" for lab in labs)
    else:
        lines.append("- No local lab definitions discovered.")
    lines.extend(("", "No containers or virtual machines were started or modified."))
    return "\n".join(lines) + "\n"
