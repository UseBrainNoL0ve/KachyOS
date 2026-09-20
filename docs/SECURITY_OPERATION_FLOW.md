# Security Operation Flow

KachySec now models a security task as an explicit operator-controlled workflow:

`scope → preflight → plan → authorize → execute → verify → evidence`

## Why this exists

The toolkit catalog tells KachySec what a tool is. The workflow layer tells the operator **when and why** it belongs in an assessment. This keeps tool discovery separate from authorization and execution.

## Workflow families

- **Network Service Assessment** — authorized service discovery and validation.
- **Web Application Assessment** — controlled HTTP application testing.
- **Local Host Hardening Review** — defensive review of the CachyOS workstation.

## Safety model

A workflow plan is not an execution engine. It:

1. records the target and authorization statement;
2. identifies the environment;
3. shows the expected phases;
4. highlights operator-controlled actions;
5. produces a reviewable plan without executing commands.

Remote or network-active work requires an explicit authorization statement. Local/isolated labs are the preferred learning environment. State-changing operations remain separate from planning and require operator control.

## Learning loop

For each operation, the intended learning sequence is:

**understand the objective → inspect the tool → define scope → review the plan → authorize deliberately → observe output → verify the finding → preserve evidence.**

This is deliberately more structured than a command launcher: the user learns the security methodology rather than only memorizing tool syntax.
