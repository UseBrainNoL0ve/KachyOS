# Authorized Offensive Security Workflows

KachySec supports both defensive security engineering and offensive-security workflows when the operator owns the target or has explicit authorization.

## Supported workflow families

- Reconnaissance and asset discovery
- Network and service enumeration
- Web/API security assessment
- Vulnerability discovery and validation
- Authentication and password-auditing workflows
- Wireless assessment in controlled environments
- OSINT and metadata analysis
- Reverse engineering and debugging
- Forensics and incident-response analysis
- Exploit-development and security-research labs
- Container/VM-based intentionally vulnerable targets

## Operating model

KachySec separates **tool availability** from **target authorization**.

The workstation may catalog and manage dual-use security tools, but an operator must define an authorized scope before using them. Future offensive workflow automation should make that scope explicit rather than silently treating an arbitrary host as a target.

The preferred execution path is:

1. Define an owned or explicitly authorized target scope.
2. Select a workflow and inspect its commands.
3. Run against a local/isolated lab or an explicitly authorized target.
4. Record the operation and relevant evidence.
5. Review results and verify the expected outcome.
6. Clean up temporary lab state when applicable.

## Automation boundary

The current KachySec control plane remains conservative: discovery, planning, evidence, and package operations are explicit. Offensive tooling is cataloged and supported as a workstation capability, while autonomous exploitation, persistence, credential theft, destructive actions, and indiscriminate remote targeting are not implicit features of the control plane.

This boundary is intentional: the project should be useful for learning penetration testing and security research without turning a workstation manager into an unattended attack engine.

## Learning objective

Each offensive module should teach a concrete concept: reconnaissance, protocol analysis, attack-surface mapping, vulnerability validation, authentication security, exploit development, reverse engineering, or evidence handling.

The goal is a capable security workstation with reproducible, auditable workflows—not a collection of tools installed without context.
