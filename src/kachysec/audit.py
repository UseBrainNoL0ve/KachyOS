from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AuditCheck:
    name: str
    status: str
    summary: str
    evidence: str = ""
    remediation: str = ""


def _run(command: list[str], timeout: int = 5) -> tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return result.returncode, (result.stdout or result.stderr).strip()


def _service_state(service: str) -> str:
    code, output = _run(["systemctl", "is-active", service])
    if code == 0:
        return output or "active"
    return output or "inactive"


def collect_audit() -> list[AuditCheck]:
    checks: list[AuditCheck] = []

    firewall = None
    for command in (("ufw", "status"), ("firewall-cmd", "--state"), ("nft", "list", "ruleset")):
        if shutil.which(command[0]):
            code, output = _run(list(command))
            if command[0] == "nft":
                firewall = "ruleset present" if code == 0 and output else "no ruleset reported"
            elif command[0] == "ufw":
                firewall = output.splitlines()[0] if output else "unknown"
            else:
                firewall = output or "unknown"
            break
    if firewall is None:
        checks.append(AuditCheck("firewall", "WARN", "No supported firewall command was detected."))
    elif "inactive" in firewall.lower() or "not running" in firewall.lower():
        checks.append(AuditCheck("firewall", "WARN", "Firewall does not report an active state.", firewall, "Review the host firewall configuration before exposing network services."))
    else:
        checks.append(AuditCheck("firewall", "PASS", "Firewall tooling reports a configured state.", firewall))

    if shutil.which("pacman"):
        code, output = _run(["pacman", "-Qu"], timeout=15)
        if code == 0 and output:
            count = len(output.splitlines())
            checks.append(AuditCheck("updates", "WARN", f"{count} package update(s) are available.", output, "Review updates and apply them explicitly with the system package manager."))
        else:
            checks.append(AuditCheck("updates", "PASS", "No pending package updates were reported by pacman."))
    else:
        checks.append(AuditCheck("updates", "INFO", "pacman was not detected; package update status was not checked."))

    code, output = _run(["systemctl", "--failed", "--no-legend", "--no-pager"])
    if code == 0 and output:
        count = len(output.splitlines())
        checks.append(AuditCheck("failed_units", "WARN", f"{count} failed systemd unit(s) reported.", output, "Inspect failed units with systemctl status and journalctl before taking action."))
    else:
        checks.append(AuditCheck("failed_units", "PASS", "No failed systemd units were reported."))

    ssh = _service_state("sshd.service")
    if ssh == "active":
        checks.append(AuditCheck("ssh", "INFO", "SSH service is active.", ssh, "If SSH is not required, review whether it should remain enabled and reachable."))
    else:
        checks.append(AuditCheck("ssh", "PASS", "SSH service is not active.", ssh))

    for runtime, command in (("podman", ["podman", "--version"]), ("docker", ["docker", "--version"]), ("qemu", ["qemu-system-x86_64", "--version"]), ("libvirt", ["virsh", "--version"])):
        if shutil.which(command[0]):
            _, output = _run(command)
            checks.append(AuditCheck(f"runtime:{runtime}", "PASS", f"{runtime} tooling is available.", output))
        else:
            checks.append(AuditCheck(f"runtime:{runtime}", "INFO", f"{runtime} tooling is not installed."))

    sensitive_paths = [Path("/etc/shadow"), Path("/etc/sudoers")]
    for path in sensitive_paths:
        try:
            mode = path.stat().st_mode & 0o777
        except OSError:
            continue
        if mode & 0o004:
            checks.append(AuditCheck(f"permissions:{path}", "WARN", f"{path} is world-readable.", oct(mode), "Review the file permissions and restore least-privilege access if appropriate."))
        else:
            checks.append(AuditCheck(f"permissions:{path}", "PASS", f"{path} is not world-readable.", oct(mode)))

    return checks


def render_audit(checks: list[AuditCheck]) -> str:
    lines = ["KachySec security audit (read-only)", ""]
    for check in checks:
        lines.append(f"[{check.status:<4}] {check.name}: {check.summary}")
        if check.evidence:
            first = check.evidence.splitlines()[0]
            lines.append(f"       evidence: {first}")
        if check.remediation:
            lines.append(f"       action:   {check.remediation}")
    return "\n".join(lines) + "\n"
