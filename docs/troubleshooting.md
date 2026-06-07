---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Troubleshooting -- qmatsim

## Common Issues

### Solver executable not found

The bash scripts (`run-DFT.sh`, `run-MD.sh`) check for `siesta` and `lmp_mpi` on `PATH` before
running. If either is missing the script exits with a descriptive error. Install the relevant
solver and verify it is accessible:

```bash
which siesta
which lmp_mpi
```

### Import errors after installation

If `import qmatsim` fails, confirm the package was installed from the repository root in editable
mode:

```bash
pip install -e ".[dev]"
python -m qmatsim --help
```

The canonical import root is `qmatsim/`, not `src/`. A `src/`-layout install will not find the
package.

### Structure validation failures

`python scripts/validate-structure.py` checks that the required directory layout is intact. If it
reports missing directories, the most likely cause is a partial clone or an accidental deletion of
a surface directory (`siesta/`, `lammps/`, `scripts/`, `tests/`).

### Pseudopotential not found

SIESTA calculations require pseudopotential files under `siesta/pseudopotentials/`. If a run
fails with a missing pseudopotential error, confirm the correct functional directory (GGA, LDA, or
GGA-SOC) contains the element's `.psf`, `.psml`, or `.upf` file.

### Test failures

The test suite (`pytest tests/`) runs CLI smoke tests via subprocess and does not require SIESTA
or LAMMPS to be installed. If tests fail, confirm the package is installed (`pip install -e .`)
and that the Python environment has `numpy` and `matplotlib`.

## Diagnostic Steps

1. Run `python scripts/validate-structure.py` to confirm directory layout.
2. Run `python -m qmatsim --help` to confirm the package is importable and the CLI is reachable.
3. Check solver executables are on `PATH` (`which siesta`, `which lmp_mpi`).
4. Run `pytest tests/` to verify CLI smoke tests pass without solvers.

## Known Failure Modes

No additional failure modes have been recorded beyond those above. New findings should be added
here when they recur more than once.
