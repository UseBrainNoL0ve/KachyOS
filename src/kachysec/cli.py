from __future__ import annotations

import argparse
from pathlib import Path

from .audit import collect_audit, render_audit
from .baseline import collect, to_json, to_markdown
from .operations import run_privileged
from .lab import collect_runtimes, discover_labs, render_lab_status
from .status import collect_status, render_status
from .tool_manager import build_install_plan, render_plan
from .tools import catalog, check_tools
from .updates import collect_updates, render_updates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kachysec",
        description="Security workstation diagnostics and management for CachyOS.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    baseline = subparsers.add_parser("baseline", help="Collect a read-only host baseline")
    baseline.add_argument("--format", choices=("json", "markdown"), default="markdown")
    baseline.add_argument("--output", type=Path, help="Write the report to a file")

    subparsers.add_parser("status", help="Show workstation health and tool summary")
    subparsers.add_parser("audit", help="Run a read-only security posture audit")
    subparsers.add_parser("updates", help="Show pending package updates without modifying the host")
    subparsers.add_parser("lab", help="Inspect local lab runtimes and definitions")
    subparsers.add_parser("gui", help="Launch the optional PySide6 security dashboard")

    tools = subparsers.add_parser("tools", help="Browse the security tool catalog")
    tools.add_argument("--missing", action="store_true", help="Show only missing tools")
    tools.add_argument("--category", help="Filter by category")
    tools.add_argument("--plan", action="store_true", help="Build a non-destructive package install plan")
    tools.add_argument("--install", action="store_true", help="Install the reviewed package plan after explicit confirmation")

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

    if args.command == "status":
        print(render_status(collect_status()), end="")
        return 0

    if args.command == "audit":
        print(render_audit(collect_audit()), end="")
        return 0

    if args.command == "updates":
        print(render_updates(collect_updates()), end="")
        return 0

    if args.command == "lab":
        print(render_lab_status(collect_runtimes(), discover_labs()), end="")
        return 0

    if args.command == "gui":
        from .gui import launch_gui
        return launch_gui()

    if args.command == "tools":
        plan = build_install_plan(list(catalog()))
        if args.install:
            print(render_plan(plan), end="")
            if not plan.packages:
                return 0
            print("\nType INSTALL to confirm the exact package list:")
            confirmation = input("> ").strip()
            result = run_privileged("install-tools", plan.packages, confirm=confirmation == "INSTALL")
            print(result.output)
            return result.returncode
        if args.plan:
            print(render_plan(plan), end="")
            return 0
        items = check_tools()
        if args.category:
            items = [item for item in items if item["category"] == args.category]
        if args.missing:
            items = [item for item in items if not item["installed"]]
        for item in items:
            marker = "[+]" if item["installed"] else "[-]"
            print(f"{marker} {item['name']:<24} {item['category']:<16} {item['purpose']}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
