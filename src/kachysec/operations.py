from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess


@dataclass(frozen=True)
class OperationResult:
    operation: str
    command: tuple[str, ...]
    returncode: int
    started_at: str
    finished_at: str
    output: str


def log_path() -> Path:
    return Path.home() / ".local" / "state" / "kachysec" / "operations.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_privileged(operation: str, packages: tuple[str, ...], *, confirm: bool) -> OperationResult:
    started = _now()
    command = ("sudo", "pacman", "-S", "--needed", *packages)
    if not packages:
        result = OperationResult(operation, command, 0, started, _now(), "No packages selected.")
        append_operation(result)
        return result
    if not confirm:
        result = OperationResult(operation, command, 2, started, _now(), "Operation not confirmed; no changes made.")
        append_operation(result)
        return result
    try:
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        output = ((completed.stdout or "") + (completed.stderr or "")).strip()
        result = OperationResult(operation, command, completed.returncode, started, _now(), output)
    except (OSError, subprocess.SubprocessError) as exc:
        result = OperationResult(operation, command, 127, started, _now(), str(exc))
    append_operation(result)
    return result


def append_operation(result: OperationResult, path: Path | None = None) -> None:
    target = path or log_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(result), sort_keys=True) + "\n")


def read_operations(path: Path | None = None) -> list[dict[str, object]]:
    target = path or log_path()
    if not target.exists():
        return []
    records: list[dict[str, object]] = []
    for line in target.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records
