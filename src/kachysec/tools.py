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
    packages: tuple[str, ...] = ()
    scope: str = "local"


# This is intentionally a catalog, not an installer. Availability is detected locally;
# package installation will be an explicit, reviewable action in a later phase.
TOOL_CATALOG: tuple[ToolSpec, ...] = (
    # Core / system diagnostics
    ToolSpec("Nmap", "nmap", "network", "Network discovery and service enumeration for authorized systems.", ("nmap", "--version"), ("nmap",), "authorized"),
    ToolSpec("Nmap Scripting Engine", "nmap", "network", "Scriptable network assessment using Nmap NSE in authorized environments.", ("nmap", "--version"), ("nmap",), "authorized"),
    ToolSpec("TShark", "tshark", "network", "CLI packet analysis.", ("tshark", "--version"), ("wireshark-cli",), "local"),
    ToolSpec("tcpdump", "tcpdump", "network", "Packet capture and low-level network diagnostics.", ("tcpdump", "--version"), ("tcpdump",), "local"),
    ToolSpec("Wireshark", "wireshark", "network", "GUI packet analysis.", ("wireshark", "--version"), ("wireshark-qt",), "local"),
    ToolSpec("socat", "socat", "network", "Controlled socket relay and network diagnostics.", ("socat", "-V"), ("socat",), "authorized"),
    ToolSpec("netcat", "nc", "network", "Basic TCP/UDP connectivity diagnostics in controlled environments.", ("nc", "-h"), ("openbsd-netcat",), "authorized"),
    ToolSpec("iproute2", "ip", "network", "Linux interface, address, route and link diagnostics.", ("ip", "-V"), ("iproute2",), "local"),
    ToolSpec("ethtool", "ethtool", "network", "Network-interface capability and link diagnostics.", ("ethtool", "--version"), ("ethtool",), "local"),
    ToolSpec("mtr", "mtr", "network", "Combined route and latency diagnostics.", ("mtr", "--version"), ("mtr",), "authorized"),
    ToolSpec("bind-utils", "dig", "network", "DNS query and troubleshooting utilities.", ("dig", "-v"), ("bind",), "authorized"),
    ToolSpec("whois", "whois", "osint", "WHOIS/RDAP-oriented domain registration lookup.", ("whois", "--version"), ("whois",), "authorized"),
    ToolSpec("arping", "arping", "network", "Layer-2/ARP diagnostics for local networks.", ("arping", "--version"), ("arping",), "authorized"),
    ToolSpec("iftop", "iftop", "network", "Interactive interface traffic observation.", ("iftop", "-h"), ("iftop",), "local"),
    ToolSpec("nethogs", "nethogs", "network", "Per-process network traffic observation.", ("nethogs", "-V"), ("nethogs",), "local"),
    ToolSpec("bmon", "bmon", "network", "Interface bandwidth and packet statistics.", ("bmon", "--version"), ("bmon",), "local"),

    # Web / application security tooling
    ToolSpec("Burp Suite", "burpsuite", "web", "HTTP(S) interception and web application testing in authorized labs.", ("burpsuite", "--version"), ("burpsuite",), "authorized"),
    ToolSpec("OWASP ZAP", "zaproxy", "web", "Web application proxy and security testing for authorized applications.", ("zaproxy", "--version"), ("zaproxy",), "authorized"),
    ToolSpec("FFUF", "ffuf", "web", "Web content discovery for authorized targets.", ("ffuf", "-V"), ("ffuf",), "authorized"),
    ToolSpec("Gobuster", "gobuster", "web", "Web and DNS content discovery for authorized targets.", ("gobuster", "version"), ("gobuster",), "authorized"),
    ToolSpec("Feroxbuster", "feroxbuster", "web", "Recursive web content discovery for authorized targets.", ("feroxbuster", "--version"), ("feroxbuster",), "authorized"),
    ToolSpec("SQLMap", "sqlmap", "web", "SQL-injection assessment for authorized applications.", ("sqlmap", "--version"), ("sqlmap",), "authorized"),
    ToolSpec("Nikto", "nikto", "web", "Web-server security assessment for authorized targets.", ("nikto", "-Version"), ("nikto",), "authorized"),
    ToolSpec("mitmproxy", "mitmproxy", "web", "Interactive HTTP(S) inspection for controlled environments.", ("mitmproxy", "--version"), ("mitmproxy",), "authorized"),
    ToolSpec("HTTPie", "http", "web", "Readable HTTP client for API and service diagnostics.", ("http", "--version"), ("httpie",), "authorized"),
    ToolSpec("curl", "curl", "web", "HTTP, HTTPS and API transport diagnostics.", ("curl", "--version"), ("curl",), "authorized"),
    ToolSpec("wget", "wget", "web", "HTTP/FTP retrieval and reproducible resource checks.", ("wget", "--version"), ("wget",), "authorized"),
    ToolSpec("OpenSSL", "openssl", "crypto", "TLS, certificate and cryptographic diagnostics.", ("openssl", "version"), ("openssl",), "local"),
    ToolSpec("testssl.sh", "testssl", "web", "TLS configuration inspection for authorized endpoints.", ("testssl", "--version"), ("testssl.sh",), "authorized"),
    ToolSpec("WhatWeb", "whatweb", "web", "Web technology fingerprinting for authorized targets.", ("whatweb", "--version"), ("whatweb",), "authorized"),
    ToolSpec("Wapiti", "wapiti", "web", "Black-box web application security auditing in authorized labs.", ("wapiti", "--version"), ("wapiti",), "authorized"),
    ToolSpec("WPScan", "wpscan", "web", "WordPress security assessment for owned or authorized sites.", ("wpscan", "--version"), ("wpscan",), "authorized"),

    # Vulnerability management / defensive assessment
    ToolSpec("Nuclei", "nuclei", "vulnerability", "Template-based vulnerability assessment for authorized assets.", ("nuclei", "-version"), ("nuclei",), "authorized"),
    ToolSpec("Greenbone/OpenVAS", "gvm-cli", "vulnerability", "Vulnerability-management interface for authorized infrastructure.", ("gvm-cli", "--version"), ("gvm",), "authorized"),
    ToolSpec("Lynis", "lynis", "hardening", "Local Linux security auditing and hardening guidance.", ("lynis", "--version"), ("lynis",), "local"),
    ToolSpec("chkrootkit", "chkrootkit", "malware", "Local rootkit-oriented defensive checks.", ("chkrootkit", "-V"), ("chkrootkit",), "local"),
    ToolSpec("rkhunter", "rkhunter", "malware", "Local rootkit and system-integrity checks.", ("rkhunter", "--version"), ("rkhunter",), "local"),
    ToolSpec("ClamAV", "clamscan", "malware", "Local malware scanning.", ("clamscan", "--version"), ("clamav",), "local"),
    ToolSpec("YARA", "yara", "forensics", "Pattern matching for file and malware-analysis workflows.", ("yara", "--version"), ("yara",), "local"),
    ToolSpec("Sigma", "sigma", "detection", "Portable detection-rule tooling for security analytics.", ("sigma", "--version"), ("sigma-cli",), "local"),
    ToolSpec("Zeek", "zeek", "network-defense", "Network security monitoring and protocol analysis.", ("zeek", "--version"), ("zeek",), "local"),
    ToolSpec("Suricata", "suricata", "network-defense", "IDS/IPS and network threat detection for owned networks.", ("suricata", "--build-info"), ("suricata",), "local"),
    ToolSpec("Snort", "snort", "network-defense", "Network intrusion detection and packet inspection.", ("snort", "-V"), ("snort",), "local"),

    # OSINT / discovery
    ToolSpec("theHarvester", "theHarvester", "osint", "Open-source reconnaissance of public domain-related data.", ("theHarvester", "--version"), ("theharvester",), "authorized"),
    ToolSpec("Amass", "amass", "osint", "Asset discovery and DNS enumeration for authorized domains.", ("amass", "-version"), ("amass",), "authorized"),
    ToolSpec("Subfinder", "subfinder", "osint", "Passive subdomain discovery for authorized domains.", ("subfinder", "-version"), ("subfinder",), "authorized"),
    ToolSpec("Assetfinder", "assetfinder", "osint", "Passive hostname discovery for authorized domains.", ("assetfinder", "--help"), ("assetfinder",), "authorized"),
    ToolSpec("dnsx", "dnsx", "osint", "DNS resolution and probing for authorized assets.", ("dnsx", "-version"), ("dnsx",), "authorized"),
    ToolSpec("httpx", "httpx", "osint", "HTTP service probing for authorized assets.", ("httpx", "-version"), ("httpx-toolkit",), "authorized"),
    ToolSpec("ExifTool", "exiftool", "osint", "File metadata inspection and normalization.", ("exiftool", "-ver"), ("perl-image-exiftool",), "local"),
    ToolSpec("SpiderFoot", "spiderfoot", "osint", "OSINT collection and analysis platform.", ("spiderfoot", "--version"), ("spiderfoot",), "authorized"),

    # Forensics / incident response
    ToolSpec("Sleuth Kit", "fls", "forensics", "Digital-forensics command-line toolkit.", ("fls", "-V"), ("sleuthkit",), "local"),
    ToolSpec("Autopsy", "autopsy", "forensics", "GUI digital-forensics platform for local evidence analysis.", ("autopsy", "--version"), ("autopsy",), "local"),
    ToolSpec("Binwalk", "binwalk", "forensics", "Firmware and file-structure inspection.", ("binwalk", "--version"), ("binwalk",), "local"),
    ToolSpec("Foremost", "foremost", "forensics", "File carving from forensic images and local evidence.", ("foremost", "-V"), ("foremost",), "local"),
    ToolSpec("bulk_extractor", "bulk_extractor", "forensics", "Feature extraction from forensic images.", ("bulk_extractor", "-V"), ("bulk-extractor",), "local"),
    ToolSpec("dc3dd", "dc3dd", "forensics", "Forensic disk imaging with hashing and verification support.", ("dc3dd", "--help"), ("dc3dd",), "local"),
    ToolSpec("Guymager", "guymager", "forensics", "GUI forensic disk-imaging workflow.", ("guymager", "--version"), ("guymager",), "local"),
    ToolSpec("hashdeep", "hashdeep", "forensics", "Recursive hashing and file-integrity comparison.", ("hashdeep", "-V"), ("hashdeep",), "local"),
    ToolSpec("rhash", "rhash", "forensics", "File hashing and checksum generation.", ("rhash", "--version"), ("rhash",), "local"),
    ToolSpec("strings", "strings", "forensics", "Extract printable strings from binaries and files.", ("strings", "--version"), ("binutils",), "local"),

    # Reverse engineering / binary analysis
    ToolSpec("Ghidra", "ghidra", "reverse", "Static reverse-engineering workspace.", ("ghidra", "--version"), ("ghidra",), "local"),
    ToolSpec("radare2", "r2", "reverse", "Command-line reverse engineering and binary analysis.", ("r2", "-v"), ("radare2",), "local"),
    ToolSpec("Cutter", "cutter", "reverse", "GUI reverse-engineering environment built around radare2.", ("cutter", "--version"), ("cutter",), "local"),
    ToolSpec("GDB", "gdb", "debugging", "Native debugger for controlled local analysis.", ("gdb", "--version"), ("gdb",), "local"),
    ToolSpec("LLDB", "lldb", "debugging", "LLVM debugger for native application analysis.", ("lldb", "--version"), ("lldb",), "local"),
    ToolSpec("strace", "strace", "debugging", "Linux system-call tracing.", ("strace", "-V"), ("strace",), "local"),
    ToolSpec("ltrace", "ltrace", "debugging", "Library-call tracing for Linux processes.", ("ltrace", "-V"), ("ltrace",), "local"),
    ToolSpec("objdump", "objdump", "reverse", "ELF/object-file disassembly and inspection.", ("objdump", "--version"), ("binutils",), "local"),
    ToolSpec("readelf", "readelf", "reverse", "ELF headers, sections and symbols inspection.", ("readelf", "--version"), ("binutils",), "local"),
    ToolSpec("patchelf", "patchelf", "reverse", "ELF metadata inspection and controlled modification.", ("patchelf", "--version"), ("patchelf",), "local"),

    # Password auditing / cryptography for owned labs
    ToolSpec("Hashcat", "hashcat", "password-audit", "Password auditing in authorized labs and recovery workflows.", ("hashcat", "--version"), ("hashcat",), "authorized"),
    ToolSpec("John the Ripper", "john", "password-audit", "Password auditing in authorized environments.", ("john", "--version"), ("john",), "authorized"),
    ToolSpec("Hydra", "hydra", "password-audit", "Credential-auditing tool for explicitly authorized test services.", ("hydra", "-h"), ("hydra",), "authorized"),
    ToolSpec("Medusa", "medusa", "password-audit", "Parallel credential auditing for owned lab services.", ("medusa", "-V"), ("medusa",), "authorized"),
    ToolSpec("CeWL", "cewl", "password-audit", "Wordlist generation for authorized password-audit labs.", ("cewl", "--help"), ("cewl",), "authorized"),
    ToolSpec("Crunch", "crunch", "password-audit", "Controlled test wordlist generation.", ("crunch", "-h"), ("crunch",), "authorized"),
    ToolSpec("Hash-Identifier", "hashid", "password-audit", "Local hash-format identification assistance.", ("hashid", "--version"), ("hashid",), "local"),

    # Wireless / RF diagnostics
    ToolSpec("Aircrack-ng", "aircrack-ng", "wireless", "Wireless security auditing for owned or explicitly authorized networks.", ("aircrack-ng", "--help"), ("aircrack-ng",), "authorized"),
    ToolSpec("airodump-ng", "airodump-ng", "wireless", "Wireless capture diagnostics in authorized lab environments.", ("airodump-ng", "--help"), ("aircrack-ng",), "authorized"),
    ToolSpec("Kismet", "kismet", "wireless", "Wireless and network sensor/monitoring platform.", ("kismet", "--version"), ("kismet",), "authorized"),
    ToolSpec("iw", "iw", "wireless", "Linux wireless-interface diagnostics.", ("iw", "--version"), ("iw",), "local"),
    ToolSpec("wavemon", "wavemon", "wireless", "Wireless interface monitoring.", ("wavemon", "-v"), ("wavemon",), "local"),

    # Containers / virtualization / labs
    ToolSpec("Podman", "podman", "labs", "Rootless container runtime for isolated security labs.", ("podman", "--version"), ("podman",), "local"),
    ToolSpec("Docker", "docker", "labs", "Container runtime for isolated development and training labs.", ("docker", "--version"), ("docker",), "local"),
    ToolSpec("Docker Compose", "docker", "labs", "Multi-container lab orchestration through Docker Compose.", ("docker", "compose", "version"), ("docker-compose",), "local"),
    ToolSpec("QEMU", "qemu-system-x86_64", "virtualization", "Local virtual-machine execution for isolated labs.", ("qemu-system-x86_64", "--version"), ("qemu-desktop",), "local"),
    ToolSpec("libvirt", "virsh", "virtualization", "VM lifecycle and virtualization management.", ("virsh", "--version"), ("libvirt",), "local"),
    ToolSpec("virt-manager", "virt-manager", "virtualization", "GUI virtual-machine management.", ("virt-manager", "--version"), ("virt-manager",), "local"),
    ToolSpec("Vagrant", "vagrant", "labs", "Reproducible virtual lab environment orchestration.", ("vagrant", "--version"), ("vagrant",), "local"),

    # Developer / observability / system analysis
    ToolSpec("Git", "git", "development", "Version control for reproducible security engineering.", ("git", "--version"), ("git",), "local"),
    ToolSpec("GitHub CLI", "gh", "development", "GitHub repository, issue and workflow automation.", ("gh", "--version"), ("github-cli",), "local"),
    ToolSpec("Python", "python", "development", "Automation and security-engineering runtime.", ("python", "--version"), ("python",), "local"),
    ToolSpec("lsof", "lsof", "observability", "Process, file and socket relationship inspection.", ("lsof", "-v"), ("lsof",), "local"),
    ToolSpec("procps-ng", "ps", "observability", "Process and resource inspection.", ("ps", "--version"), ("procps-ng",), "local"),
    ToolSpec("htop", "htop", "observability", "Interactive process and resource monitoring.", ("htop", "--version"), ("htop",), "local"),
    ToolSpec("iotop", "iotop", "observability", "Disk I/O observation by process.", ("iotop", "--version"), ("iotop",), "local"),
    ToolSpec("bpftrace", "bpftrace", "observability", "eBPF-based tracing for authorized local diagnostics.", ("bpftrace", "--version"), ("bpftrace",), "local"),
    ToolSpec("perf", "perf", "observability", "Linux performance-counter and profiling tooling.", ("perf", "--version"), ("perf",), "local"),
    ToolSpec("sysstat", "iostat", "observability", "System performance and I/O statistics.", ("iostat", "-V"), ("sysstat",), "local"),

    # File / archive / text analysis useful in investigations
    ToolSpec("ripgrep", "rg", "analysis", "Fast local text search across source and evidence trees.", ("rg", "--version"), ("ripgrep",), "local"),
    ToolSpec("fd", "fd", "analysis", "Fast local file discovery.", ("fd", "--version"), ("fd",), "local"),
    ToolSpec("jq", "jq", "analysis", "JSON inspection and transformation for security reports.", ("jq", "--version"), ("jq",), "local"),
    ToolSpec("7-Zip", "7z", "analysis", "Archive inspection and extraction.", ("7z", "-h"), ("7zip",), "local"),
    ToolSpec("file", "file", "analysis", "File-type identification using magic signatures.", ("file", "--version"), ("file",), "local"),
    ToolSpec("xxd", "xxd", "analysis", "Hexadecimal inspection of files and byte streams.", ("xxd", "-h"), ("vim",), "local"),
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
            "scope": spec.scope,
            "packages": list(spec.packages),
            "installed": shutil.which(spec.binary) is not None,
        }
        for spec in specs
    ]


def summarize_tools(items: list[dict[str, object]]) -> dict[str, int]:
    installed = sum(1 for item in items if item["installed"])
    return {"total": len(items), "installed": installed, "missing": len(items) - installed}
