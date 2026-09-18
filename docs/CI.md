# Continuous Integration

The repository uses GitHub Actions to run the unit-test suite on pushes and pull requests.

The CI environment is intentionally isolated from the native CachyOS workflow. Local development can continue to use the system Python and native package manager while CI creates a disposable Python environment.

Current checks:

- install the package from pyproject.toml;
- run the unittest suite;
- execute without installing or changing security tooling on the runner.
