# Lab Manager

KachySec treats local security labs as a separate boundary from the host workstation.

## Runtime discovery

The current lab manager detects:

- Podman
- Docker
- QEMU
- libvirt
- virt-manager

It does not currently create, start, stop, delete, or reconfigure containers or virtual machines.

## Review-only lab plans

`kachysec lab --plan` converts discovered lab definitions into a reviewable lifecycle plan containing:

- lab name;
- runtime kind;
- local path;
- declared network boundary;
- planned action.

The current action is intentionally `review-only`.

## Intended lifecycle

The future execution layer should follow:

1. discover runtime capabilities;
2. validate the lab definition;
3. show resources and network boundaries;
4. require explicit confirmation;
5. create/start the isolated environment;
6. run authorized training exercises;
7. collect results;
8. verify the environment state;
9. tear the environment down.

Training targets should be local, isolated, intentionally owned, and explicitly authorized.

## Directory layout

Future lab definitions can live under:

```text
labs/
├── containers/
└── vms/
```

The current implementation deliberately stops before lifecycle execution so network-affecting and privileged behavior can be reviewed separately.
