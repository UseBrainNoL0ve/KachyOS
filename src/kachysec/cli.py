from __future__ import annotations

import argparse
from pathlib import Path

from .baseline import collect, to_json, to_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kachysec",
        description="Read-only security workstation diagnostics for CachyOS.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    baseline = subparsers.add_parser("baseline", help="Collect a read-only host baseline")
    baseline.add_argument("--format", choices=("json", "markdown"), default="markdown")
    baseline.add_argument("--output", type=Path, help="Write the report to a file")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "baseline":
        data = collect()
        rendered = to_json(data) if args.format == "json" else to_markdown(data)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"Baseline report written to {args.output}")
        else:
            print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
