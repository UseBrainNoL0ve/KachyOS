# Installation

KachySec is designed for CachyOS/Arch Linux and can be used without a Python virtual environment.

## Option 1 — Development checkout

Clone the repository and install it into the user environment:

```bash
git clone https://github.com/UseBrainNoL0ve/KachyOS.git
cd KachyOS
python -m pip install --user .
```

If your Python packaging setup requires it, install the build prerequisites first:

```bash
sudo pacman -S python python-pip python-build python-installer python-setuptools
```

The optional GUI requires PySide6:

```bash
sudo pacman -S pyside6
```

Verify:

```bash
kachysec --help
kachysec status
kachysec audit
```

## Option 2 — Native package

The repository contains a `PKGBUILD` for a native Arch/CachyOS package:

```bash
git clone https://github.com/UseBrainNoL0ve/KachyOS.git
cd KachyOS
makepkg -si
```

This path is intended for a real workstation installation. Review the PKGBUILD before building any package.

## First-run checklist

1. Run `kachysec baseline --format markdown --output baseline.md`.
2. Run `kachysec status` to see available security tooling.
3. Run `kachysec tools --missing` to inspect missing catalog entries.
4. Run `kachysec tools --plan` to generate a non-destructive package plan.
5. Run `kachysec audit` to review host posture.
6. Run `kachysec lab` to inspect local lab runtimes.
7. Run `kachysec gui` for the desktop dashboard.

## Privacy

Baseline and audit output can contain hostnames, IP addresses, mount paths, service names and other local-system information. Review or redact reports before publishing them.
