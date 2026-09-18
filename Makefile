PYTHON ?= python

.PHONY: test install gui baseline status audit updates lab telemetry baseline-diff

test:
	$(PYTHON) -m unittest discover -s tests -v

install:
	$(PYTHON) -m pip install --user .

gui:
	kachysec gui

baseline:
	kachysec baseline --format markdown --output reports/baseline.md

status:
	kachysec status

audit:
	kachysec audit

updates:
	kachysec updates

lab:
	kachysec lab

telemetry:
	kachysec telemetry
