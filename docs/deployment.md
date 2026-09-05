---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Deployment and Release -- qmatsim

QMatSim is a thin Python CLI package, not a deployed service or a bundled HPC
workspace. The wheel is installable independently; scientific solver workflows require a
separately managed workspace and local solver configuration.

## Package installation and verification

```bash
pip install QMatSim
qmatsim verify-fixture
```

The expected single-line JSON result is documented in the README. This command and
`pytest` do not require SIESTA, LAMMPS, SLURM, or external workspace data.

For source contributors, use `pip install -e ".[dev]"` and run
`python scripts/validate-structure.py` before tests.

## External Solver Requirements

The scientific workspace and SIESTA/LAMMPS must be obtained and configured separately.
The package wheel does not include templates, pseudopotentials, data, or executables. When
running a prepared workspace, place the solver executables on `PATH`:

- `siesta` (version 4.1 or later)
- `lmp_mpi`

The bash scripts in `scripts/` check for both executables at startup and exit early with a
descriptive message if either is missing.

## HPC / SLURM

Workspace automation scripts include SLURM submission helpers. Set cluster-specific paths,
partitions, resource limits, mail settings, `QMATSIM_SCRATCH_ROOT`,
`QMATSIM_WORKSPACE_ROOT`, and `QMATSIM_PSEUDOPOTENTIAL_ROOT` in local configuration or
submission wrappers; do not commit them.

## Release Strategy

The Python package is intentionally thin. A future scientific release must publish a
separately versioned, checksummed, license-reviewed workspace/data bundle and document its
solver/container versions before claiming scientific reproducibility.

## Rollback

Because there is no deployed service, rollback means reverting to an earlier commit:

```bash
git checkout <commit-sha>
pip install -e ".[dev]"
```
