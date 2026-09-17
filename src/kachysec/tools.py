from __future__ import annotations

from dataclasses import dataclass
import shutil
from typing import Iterable


@dataclass(frozen=True)
class ToolSpec:
    name: str
    binary: str
    category: str
    purpose: str
    verification: tuple[str, ...]


TOOL_CATALOG: tuple[ToolSpec, ...] = (
    ToolSpec("Nmap", "nmap", "network", "Network discovery and service enumeration for authorized systems.", ("nmap", "--version")),
    ToolSpec("TShark", "tshark", "network", "CLI packet analysis.", ("tshark", "--version")),
    ToolSpec("tcpdump", "tcpdump", "network", "Packet capture and low-level network diagnostics.", ("tcpdump", "--version")),
    ToolSpec("Wireshark", "wireshark", "network", "GUI packet analysis.", ("wireshark", "--version")),
    ToolSpec("Ghidra", "ghidra", "reverse", "Static reverse-engineering workspace.", ("ghidra", "--version")),
    ToolSpec("radare2", "radare2", "reverse", "Command-line reverse engineering and binary analysis.", ("radare2", "-v")),
    ToolSpec("GDB", "gdb", "debugging", "Native debugger for controlled local analysis.", ("gdb", "--version")),
    ToolSpec("strace", "strace", "debugging", "Linux system-call tracing.", ("strace", "-V")),
    ToolSpec("YARA", "yara", "forensics", "Pattern matching for file and malware-analysis workflows.", ("yara", "--version")),
    ToolSpec("Binwalk", "binwalk", "forensics", "Firmware and file-structure inspection.", ("binwalk", "--version")),
    ToolSpec("Sleuth Kit", "sleuthkit", "forensics", "Digital-forensics command-line toolkit.", ("fls", "-V")),
    ToolSpec("Hashcat", "hashcat", "password-audit", "Password auditing in authorized labs and recovery workflows.", ("hashcat", "--version")),
    ToolSpec("John the Ripper", "john", "password-audit", "Password auditing in authorized environments.", ("john", "--version")),
    ToolSpec("FFUF", "ffuf", "web", "Web content discovery for authorized targets.", ("ffuf", "-V")),
    ToolSpec("Gobuster", "gobuster", "web", "Web and DNS content discovery for authorized targets.", ("gobuster", "version")),
    ToolSpec("SQLMap", "sqlmap", "web", "SQL-injection assessment for authorized applications.", ("sqlmap", "--version")),
    ToolSpec("Nikto", "nikto", "web", "Web-server security assessment for authorized targets.", ("nikto", "-Version")),
    ToolSpec("mitmproxy", "mitmproxy", "web", "Interactive HTTP(S) inspection for controlled environments.", ("mitmproxy", "--version")),
    ToolSpec("Lynis", "lynis", "hardening", "Local Linux security auditing and hardening guidance.", ("lynis", "--version")),
    ToolSpec("ClamAV", "clamscan", "malware", "Local malware scanning.", ("clamscan", "--version")),
)


def catalog() -> tuple[ToolSpec, ...]:
    return TOOL_CATALOG


def check_tools(specs: Iterable[ToolSpec] = TOOL_CATALOG) -> list[dict[str, object]]:
    return [
        {
            "name": spec.name,
            "binary": spec.binary,
            "category": spec.category,
            "purpose": spec.purpose,
            "installed": shutil.which(spec.binary) is not None,
        }
        for spec in specs
    ]


def summarize_tools(items: list[dict[str, object]]) -> dict[str, int]:
    installed = sum(1 for item in items if item["installed"])
    return {"total": len(items), "installed": installed, "missing": len(items) - installed}
