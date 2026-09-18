from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .baseline import collect

@dataclass(frozen=True)
class BaselineDiff:
    added: tuple[str, ...]
    removed: tuple[str, ...]
    changed: tuple[str, ...]

def baseline_store() -> Path:
    return Path.home() / ".local" / "state" / "kachysec" / "baselines"

def save_baseline(data: dict[str, Any], *, path: Path | None = None) -> Path:
    target_dir = path or baseline_store()
    target_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = target_dir / f"baseline-{timestamp}.json"
    target.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target

def load_baseline(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        flattened: dict[str, Any] = {}
        for key, child in value.items():
            name = f"{prefix}.{key}" if prefix else key
            flattened.update(_flatten(child, name))
        return flattened
    if isinstance(value, list):
        return {prefix: value}
    return {prefix: value}

def diff_baselines(before: dict[str, Any], after: dict[str, Any]) -> BaselineDiff:
    old = _flatten(before)
    new = _flatten(after)
    added = tuple(sorted(new.keys() - old.keys()))
    removed = tuple(sorted(old.keys() - new.keys()))
    changed = tuple(sorted(key for key in old.keys() & new.keys() if old[key] != new[key]))
    return BaselineDiff(added, removed, changed)

def collect_and_save() -> Path:
    return save_baseline(collect())

def render_diff(diff: BaselineDiff, *, before: Path, after: Path) -> str:
    lines = [
        "# KachySec Baseline Diff", "",
        f"- Before: {before}", f"- After: {after}", "",
        f"Added fields: **{len(diff.added)}**",
        f"Removed fields: **{len(diff.removed)}**",
        f"Changed fields: **{len(diff.changed)}**", "",
    ]
    for title, values in (("Added", diff.added), ("Removed", diff.removed), ("Changed", diff.changed)):
        lines.extend([f"## {title}", ""])
        if values:
            lines.extend("- " + chr(96) + value + chr(96) for value in values)
        else:
            lines.append("- None")
        lines.append("")
    lines.append(
        "This comparison is structural; it does not by itself establish "
        "whether a change is secure or malicious."
    )
    return "\n".join(lines)

def latest_baselines(limit: int = 10) -> list[Path]:
    return sorted(baseline_store().glob("baseline-*.json"), reverse=True)[:limit]
