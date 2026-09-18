from __future__ import annotations

import argparse
from pathlib import Path

from .audit import collect_audit, render_audit
from .baseline import collect, to_json, to_markdown
from .evidence import diff_baselines, latest_baselines, load_baseline, render_diff, save_baseline
from .lab import build_lab_plans, collect_runtimes, discover_labs, render_lab_plans, render_lab_status
from .operations import run_privileged
from .status import collect_status, render_status
from .telemetry import collect_telemetry, render_telemetry
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
    subparsers.add_parser("telemetry", help="Show local defensive host telemetry (read-only)")

    baseline_diff = subparsers.add_parser("baseline-diff", help="Compare two saved baseline JSON snapshots")
    baseline_diff.add_argument("before", type=Path, nargs="?")
    baseline_diff.add_argument("after", type=Path, nargs="?")
    baseline_diff.add_argument("--latest", action="store_true", help="Compare the two newest saved snapshots")

    lab = subparsers.add_parser("lab", help="Inspect local lab runtimes and definitions")
    lab.add_argument("--plan", action="store_true", help="Build a review-only lab lifecycle plan")
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
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            rendered = to_json(data) if args.format == "json" else to_markdown(data)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"Baseline report written to {args.output}")
            saved = save_baseline(data)
            print(f"Snapshot saved to {saved}")
        else:
            print(to_json(data) if args.format == "json" else to_markdown(data), end="")
        return 0

    if args.command == "baseline-diff":
        if args.latest:
            snapshots = latest_baselines(2)
            if len(snapshots) < 2:
                print("Need at least two saved baselines.")
                return 2
            before, after = snapshots[1], snapshots[0]
        elif args.before and args.after:
            before, after = args.before, args.after
        else:
            print("Provide BEFORE AFTER or use --latest.")
            return 2
        try:
            diff = diff_baselines(load_baseline(before), load_baseline(after))
        except (OSError, ValueError) as exc:
            print(f"Could not read baseline snapshots: {exc}")
            return 2
        print(render_diff(diff, before=before, after=after))
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

    if args.command == "telemetry":
        print(render_telemetry(collect_telemetry()))
        return 0

    if args.command == "lab":
        labs = discover_labs()
        if args.plan:
            print(render_lab_plans(build_lab_plans(labs)), end="")
        else:
            print(render_lab_status(collect_runtimes(), labs), end="")
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
