from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from .telemetry import TelemetrySnapshot

DEFAULT_LIMIT = 500


def telemetry_history_store() -> Path:
    path = Path.home() / ".local" / "state" / "kachysec" / "telemetry"
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_snapshot(snapshot: TelemetrySnapshot, path: Path | None = None) -> Path:
    target_dir = path or telemetry_history_store()
    target_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{snapshot.timestamp:.6f}.json"
    target = target_dir / filename
    target.write_text(json.dumps(asdict(snapshot), sort_keys=True) + "\n", encoding="utf-8")
    return target


def load_snapshots(limit: int = DEFAULT_LIMIT, path: Path | None = None) -> list[TelemetrySnapshot]:
    if limit <= 0:
        return []
    target_dir = path or telemetry_history_store()
    if not target_dir.exists():
        return []
    snapshots: list[TelemetrySnapshot] = []
    for item in sorted(target_dir.glob("*.json"), reverse=True)[:limit]:
        try:
            data = json.loads(item.read_text(encoding="utf-8"))
            snapshots.append(TelemetrySnapshot(**data))
        except (OSError, TypeError, ValueError):
            continue
    return snapshots


def render_history(snapshots: list[TelemetrySnapshot]) -> str:
    lines = ["KachySec telemetry history (local, read-only)", ""]
    if not snapshots:
        lines.append("No saved telemetry snapshots.")
        return "\n".join(lines)
    for snapshot in snapshots:
        lines.append(
            f"{snapshot.timestamp:.3f} | load {snapshot.load_1m:.2f} | "
            f"memory {(snapshot.memory_total_kib - snapshot.memory_available_kib) / 1024:.0f}/"
            f"{snapshot.memory_total_kib / 1024:.0f} MiB | "
            f"tcp {snapshot.listening_tcp} | udp {snapshot.listening_udp} | "
            f"proc {snapshot.processes}"
        )
    return "\n".join(lines)
