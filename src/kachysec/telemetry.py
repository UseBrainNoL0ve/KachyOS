from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import time

@dataclass(frozen=True)
class TelemetrySnapshot:
    timestamp: float
    load_1m: float
    memory_total_kib: int
    memory_available_kib: int
    listening_tcp: int
    listening_udp: int
    processes: int

def _memory() -> tuple[int, int]:
    total = available = 0
    try:
        for line in Path('/proc/meminfo').read_text(encoding='utf-8').splitlines():
            key, value = line.split(':', 1)
            amount = int(value.strip().split()[0])
            if key == 'MemTotal': total = amount
            elif key == 'MemAvailable': available = amount
    except (OSError, ValueError):
        pass
    return total, available

def _process_count() -> int:
    try: return sum(1 for item in Path('/proc').iterdir() if item.name.isdigit())
    except OSError: return 0

def _socket_counts() -> tuple[int, int]:
    if shutil.which('ss') is None: return 0, 0
    try:
        result = subprocess.run(['ss','-H','-lntup'], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.SubprocessError): return 0, 0
    tcp = udp = 0
    for line in result.stdout.splitlines():
        fields = line.split()
        if fields and fields[0].startswith('tcp'): tcp += 1
        elif fields and fields[0].startswith('udp'): udp += 1
    return tcp, udp

def collect_telemetry() -> TelemetrySnapshot:
    try: load_1m = float(Path('/proc/loadavg').read_text(encoding='utf-8').split()[0])
    except (OSError, ValueError, IndexError): load_1m = 0.0
    total, available = _memory()
    tcp, udp = _socket_counts()
    return TelemetrySnapshot(time.time(), load_1m, total, available, tcp, udp, _process_count())

def render_telemetry(snapshot: TelemetrySnapshot) -> str:
    used = max(snapshot.memory_total_kib - snapshot.memory_available_kib, 0)
    return ('KachySec defensive telemetry (read-only)\n\n'
            f'Load (1m): {snapshot.load_1m:.2f}\n'
            f'Memory: {used / 1024:.0f} MiB used / {snapshot.memory_total_kib / 1024:.0f} MiB total\n'
            f'Listening TCP: {snapshot.listening_tcp}\n'
            f'Listening UDP: {snapshot.listening_udp}\n'
            f'Processes: {snapshot.processes}\n\n'
            'Telemetry performs local observation only; it does not probe remote hosts or change the system.')