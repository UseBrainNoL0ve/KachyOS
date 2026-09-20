# KachySec Assistant

KachySec includes a local-first cybersecurity copilot designed to stay alongside the operator during security work.

## Role

The assistant can:

- read a current KachySec status, audit, and tool snapshot;
- explain security concepts and tool output;
- help plan defensive investigations;
- help reason through explicitly authorized offensive-security workflows;
- suggest reviewable commands for owned systems, local labs, or authorized targets;
- explain what evidence to collect and how to verify results.

The assistant does **not** silently execute commands, select targets, infer authorization, or perform unattended exploitation.

## Local-first provider

The first provider is Ollama. When installed, `kachysec assistant` can send a prompt to a locally running model.

The model name is configurable through the CLI. The default is `qwen2.5:7b`; the operator must have the model installed locally.

Examples:

```
kachysec assistant "Explain this audit warning and what I should verify next."
kachysec assistant --model qwen2.5:7b "Help me understand this service enumeration result."
```

The prompt automatically includes a read-only KachySec status/audit/tool summary.

## Operating model

```
LIVE WORK
   ↓
KachySec state + evidence
   ↓
Assistant explanation / plan
   ↓
Operator review
   ↓
Explicit action
   ↓
Verification + evidence
```

This keeps the assistant useful during real security engineering without turning it into an unattended attack engine.

## Learning mode

The assistant is intentionally prompted to explain:

1. what is happening;
2. why the next step is useful;
3. what to verify;
4. what security concept the operator is learning.

This makes the feature a teaching layer rather than a command generator only.
