# Security Policy

## Scope

KachySec is a workstation-management project for defensive security engineering **and explicitly authorized offensive-security testing**.

The project supports dual-use security tooling for activities such as reconnaissance, service enumeration, web/API assessment, vulnerability validation, password auditing, wireless assessment, reverse engineering, exploit-development research, and controlled security labs.

## Authorization boundary

Use offensive capabilities only against systems, applications, networks, devices, or lab targets that you own or are explicitly authorized to test.

Tool catalog inclusion is not authorization. A tool being available in KachySec does not grant permission to target a third party.

## Operational safety

The control plane favors:

- explicit target scope;
- reviewable commands and plans;
- local or isolated labs for experimentation;
- operation/evidence logging where practical;
- post-operation verification;
- explicit privilege boundaries.

KachySec should not silently turn a workstation manager into an unattended attack engine. Future offensive automation should preserve clear scope and operator confirmation.

## Reporting

Do not publish sensitive host information, credentials, private keys, tokens, baseline reports, or network details in issues or pull requests.

For a suspected software vulnerability in KachySec, provide a minimal reproduction and affected component through the repository's private security-reporting mechanism when available.
