---
type: canonical
owner: platform-engineering
last-reviewed: 2026-03-31
---

# Deployment and Release -- qmatsim

QMatSim is a research library and HPC workflow repository. It is not deployed as a running
service and has no production environment. The relevant "deployment" context is local
installation on a workstation or HPC cluster so that `qmatsim`, SIESTA, and LAMMPS can be
invoked together.

## Local Installation

```bash
git clone https://github.com/alawein/qmatsim.git
cd qmatsim
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m qmatsim --help
```

`validate-structure.py` confirms that the expected directory layout is intact before any
simulation work begins.

## External Solver Requirements

SIESTA and LAMMPS must be installed separately and their executables placed on `PATH`:

- `siesta` (version 4.1 or later)
- `lmp_mpi`

The bash scripts in `scripts/` check for both executables at startup and exit early with a
descriptive message if either is missing.

## HPC / SLURM

Workflow automation scripts in `scripts/` include SLURM submission helpers. Cluster-specific
paths, partition names, and resource limits must be set in local configuration files that are
not committed to this repository.

## Release Strategy

There is no published package release at this time. The repository is consumed by cloning and
installing in editable mode (`pip install -e .`). Version information is tracked in
`pyproject.toml`.

## Rollback

Because there is no deployed service, rollback means reverting to an earlier commit:

```bash
git checkout <commit-sha>
pip install -e ".[dev]"
```
