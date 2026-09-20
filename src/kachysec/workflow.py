from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class WorkflowPhase(str, Enum):
    SCOPE = "SCOPE"
    PREFLIGHT = "PREFLIGHT"
    PLAN = "PLAN"
    AUTHORIZE = "AUTHORIZE"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    EVIDENCE = "EVIDENCE"


@dataclass(frozen=True)
class TargetScope:
    target: str
    authorization: str
    environment: str = "local-lab"

    @property
    def is_explicit(self) -> bool:
        return bool(self.target.strip() and self.authorization.strip())

    @property
    def is_isolated_lab(self) -> bool:
        value = self.environment.strip().lower()
        return value in {"local-lab", "isolated-lab", "localhost"}


@dataclass(frozen=True)
class WorkflowStep:
    phase: WorkflowPhase
    title: str
    description: str
    operator_required: bool = False


@dataclass(frozen=True)
class SecurityWorkflow:
    name: str
    objective: str
    tool_categories: tuple[str, ...]
    steps: tuple[WorkflowStep, ...]


@dataclass(frozen=True)
class WorkflowPlan:
    workflow: SecurityWorkflow
    scope: TargetScope
    selected_tool: str | None
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def ready_for_operator_review(self) -> bool:
        return self.scope.is_explicit and not self.warnings


WORKFLOWS: tuple[SecurityWorkflow, ...] = (
    SecurityWorkflow(
        "Network Service Assessment",
        "Map exposed services and validate expected network surface on an authorized target.",
        ("network",),
        (
            WorkflowStep(WorkflowPhase.SCOPE, "Define target scope", "Record an exact host, lab network, or owned asset and authorization.", True),
            WorkflowStep(WorkflowPhase.PREFLIGHT, "Inspect local tooling", "Verify the selected scanner and supporting utilities are available."),
            WorkflowStep(WorkflowPhase.PLAN, "Build assessment plan", "Describe discovery, service enumeration, verification, and evidence collection."),
            WorkflowStep(WorkflowPhase.AUTHORIZE, "Operator approval", "Confirm target, boundaries, rate limits, and intended activity.", True),
            WorkflowStep(WorkflowPhase.EXECUTE, "Run assessment", "Execute only after explicit operator authorization.", True),
            WorkflowStep(WorkflowPhase.VERIFY, "Validate findings", "Separate observed facts from scanner output and false positives.", True),
            WorkflowStep(WorkflowPhase.EVIDENCE, "Capture evidence", "Store relevant output locally with timestamps and scope metadata.", True),
        ),
    ),
    SecurityWorkflow(
        "Web Application Assessment",
        "Structure authorized HTTP application testing without silently escalating activity.",
        ("web", "vulnerability"),
        (
            WorkflowStep(WorkflowPhase.SCOPE, "Define application scope", "Record the authorized URL, application boundary, and excluded paths.", True),
            WorkflowStep(WorkflowPhase.PREFLIGHT, "Inspect proxy and scanner", "Verify the selected web tooling and local lab/runtime state."),
            WorkflowStep(WorkflowPhase.PLAN, "Build test plan", "Organize passive inspection, controlled discovery, validation, and evidence."),
            WorkflowStep(WorkflowPhase.AUTHORIZE, "Operator approval", "Confirm authorization and test intensity before active requests.", True),
            WorkflowStep(WorkflowPhase.EXECUTE, "Run assessment", "Execute the approved checks against the scoped application.", True),
            WorkflowStep(WorkflowPhase.VERIFY, "Validate findings", "Reproduce relevant observations and document confidence."),
            WorkflowStep(WorkflowPhase.EVIDENCE, "Capture evidence", "Preserve request/response or scanner evidence locally where appropriate.", True),
        ),
    ),
    SecurityWorkflow(
        "Local Host Hardening Review",
        "Review the CachyOS host for defensive configuration and observable security issues.",
        ("hardening", "malware", "observability"),
        (
            WorkflowStep(WorkflowPhase.SCOPE, "Define host scope", "Use the local host and specify the review boundary."),
            WorkflowStep(WorkflowPhase.PREFLIGHT, "Collect baseline", "Gather read-only host, service, package, and security observations."),
            WorkflowStep(WorkflowPhase.PLAN, "Prioritize review", "Group findings by exposure, evidence, and remediation impact."),
            WorkflowStep(WorkflowPhase.AUTHORIZE, "Operator approval", "Confirm which configuration changes, if any, may be considered.", True),
            WorkflowStep(WorkflowPhase.EXECUTE, "Apply approved changes", "State-changing remediation is always a separate operator action.", True),
            WorkflowStep(WorkflowPhase.VERIFY, "Re-check baseline", "Compare observations before and after approved changes.", True),
            WorkflowStep(WorkflowPhase.EVIDENCE, "Capture evidence", "Record findings, decisions, and verification results locally.", True),
        ),
    ),
)


def workflows() -> tuple[SecurityWorkflow, ...]:
    return WORKFLOWS


def find_workflow(name: str) -> SecurityWorkflow:
    for workflow in WORKFLOWS:
        if workflow.name == name:
            return workflow
    raise KeyError(name)


def build_workflow_plan(
    workflow: SecurityWorkflow,
    scope: TargetScope,
    selected_tool: str | None = None,
) -> WorkflowPlan:
    warnings: list[str] = []
    if not scope.target.strip():
        warnings.append("Target scope is empty.")
    if not scope.authorization.strip():
        warnings.append("Authorization statement is missing.")
    if not scope.is_isolated_lab and not scope.authorization.strip().lower().startswith(("owned", "authorized", "explicitly authorized")):
        warnings.append("Non-lab targets require a clear authorization statement.")
    if selected_tool and not selected_tool.strip():
        selected_tool = None
    return WorkflowPlan(workflow, scope, selected_tool, tuple(warnings))


def render_workflow_plan(plan: WorkflowPlan) -> str:
    lines = [
        f"KACHYSEC // {plan.workflow.name.upper()}",
        "=" * 72,
        f"Objective: {plan.workflow.objective}",
        f"Target: {plan.scope.target or '<unset>'}",
        f"Environment: {plan.scope.environment}",
        f"Authorization: {plan.scope.authorization or '<unset>'}",
        f"Selected tool: {plan.selected_tool or '<none>'}",
        "",
        "PIPELINE",
    ]
    for step in plan.workflow.steps:
        marker = "[OPERATOR]" if step.operator_required else "[SYSTEM]"
        lines.append(f"{step.phase.value:10} {marker:10} {step.title} — {step.description}")
    lines.extend(("", "STATUS"))
    if plan.warnings:
        lines.extend(f"WARNING: {warning}" for warning in plan.warnings)
    else:
        lines.append("READY FOR OPERATOR REVIEW")
    lines.append("No command is executed by workflow planning.")
    return "\n".join(lines)
