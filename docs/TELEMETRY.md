# Defensive Telemetry

KachySec provides a small read-only host telemetry layer for the workstation dashboard and CLI.

## Signals
- 1-minute load average
- total and available memory
- locally listening TCP sockets
- locally listening UDP sockets
- process count

The collector reads local kernel/process information and the local `ss` command when available. It does not perform remote network probing, install software, change services, or modify firewall/network configuration.

## CLI
`kachysec telemetry`

## Design boundary
Telemetry is observation, not response automation. Future remediation should remain a separate explicit operation with a reviewable plan, confirmation boundary, operation log, and post-change verification.