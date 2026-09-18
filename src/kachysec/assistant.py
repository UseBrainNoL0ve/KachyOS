from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Iterable

from .audit import collect_audit
from .status import collect_status
from .tools import check_tools, summarize_tools


SYSTEM_PROMPT = """You are KachySec Assistant, a local-first cybersecurity learning copilot.
Help the operator understand defensive security and explicitly authorized offensive security.
Prefer owned systems, local isolated labs, and clearly scoped authorized targets.
Explain why a step is useful, what evidence to collect, and what could go wrong.
Do not invent authorization, targets, results, or tool output.
Do not execute commands yourself. Return commands as reviewable suggestions only.
When a request is ambiguous, ask for the missing scope or context.
Keep the operator in control of every state-changing or network-active action.
"""


@dataclass(frozen=True)
class AssistantContext:
    status: str
    audit: str
    tool_summary: str

    def as_text(self) -> str:
        return (
            "KACHYSEC LIVE CONTEXT\n"
            f"STATUS\n{self.status}\n\n"
            f"AUDIT\n{self.audit}\n\n"
            f"TOOLS\n{self.tool_summary}"
        )


@dataclass(frozen=True)
class AssistantResponse:
    provider: str
    text: str


def collect_context() -> AssistantContext:
    status = collect_status()
    audit = collect_audit()
    tools = check_tools()
    summary = summarize_tools(tools)
    status_text = "\n".join(f"{item.name}: {item.value}" for item in status)
    audit_text = "\n".join(f"[{item.status}] {item.name}: {item.summary}" for item in audit)
    summary_text = json.dumps(summary, sort_keys=True)
    return AssistantContext(status_text, audit_text, summary_text)


def build_prompt(question: str, context: AssistantContext | None = None) -> str:
    context = context or collect_context()
    return (
        f"{SYSTEM_PROMPT}\n\n{context.as_text()}\n\n"
        "OPERATOR QUESTION\n"
        f"{question.strip()}\n\n"
        "Answer with: 1) assessment, 2) next safe step, 3) what to verify, "
        "and 4) learning note. If a command is useful, label it as a reviewable command "
        "and keep it scoped to an owned/local/authorized environment."
    )


def ollama_available() -> bool:
    return shutil.which("ollama") is not None


def ask_ollama(question: str, model: str = "qwen2.5:7b") -> AssistantResponse:
    if not ollama_available():
        raise RuntimeError("Ollama is not installed or is not on PATH.")
    prompt = build_prompt(question)
    completed = subprocess.run(
        ["ollama", "run", model, prompt],
        text=True,
        capture_output=True,
        check=False,
        timeout=180,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Ollama returned a non-zero exit status."
        raise RuntimeError(detail)
    return AssistantResponse(provider=f"ollama:{model}", text=completed.stdout.strip())


def available_providers() -> Iterable[str]:
    if ollama_available():
        yield "ollama"


def render_response(response: AssistantResponse) -> str:
    return f"KachySec Assistant [{response.provider}]\n\n{response.text}\n"
