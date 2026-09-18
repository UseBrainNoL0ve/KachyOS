# Lab Manager

KachySec treats local labs as a separate security boundary.

## Runtime discovery

The current lab manager detects:

- Podman
- Docker
- QEMU
- libvirt
- virt-manager

It does not start, stop, create, delete or network containers/VMs. The new `kachysec lab --plan` command only produces a reviewable lifecycle plan.

## Architecture

The intended lab lifecycle is:

1. discover runtime capabilities;
2. validate a lab definition;
3. show the resources and network boundaries;
4. ask for explicit confirmation;
5. create/start the isolated environment only after a separate explicit execution action;
6. run authorized training exercises;
7. collect results;
8. tear the environment down.

Training targets should be local, isolated and intentionally owned/authorized.

## Directory layout

Future lab definitions can live under:

```text
labs/
├── containers/
└── vms/
```

The first implementation deliberately stops at discovery so the lifecycle can be reviewed before privileged or network-affecting automation is introduced.
