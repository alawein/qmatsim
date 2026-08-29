# QMatSim

Status:      frozen
Category:    lab
Owner:       alawein
Visibility:  public
Purpose:     Quantum material simulation research workspace.
Next action: continue

## Abstract

QMatSim orchestrates strain-engineering simulations for 2D quantum materials: a
Python CLI drives SIESTA for DFT and LAMMPS for molecular dynamics from one set
of commands. It is for researchers who already run DFT/MD pipelines by hand and
want a single reproducible entry point instead of separate per-project scripts
for each solver.

It does not implement DFT or MD itself; it depends on SIESTA and LAMMPS and
orchestrates their inputs, execution, and postprocessing.

## Status

- Lifecycle: frozen
- Verification date: 2026-08-28
- Scope: Python package under `qmatsim/`, SIESTA/LAMMPS templates under
  `siesta/` and `lammps/`, and cluster scripts under `scripts/`

## Runtime requirements

- Python 3.9+ with `pip install -e ".[dev]"`
- External scientific dependencies: SIESTA (DFT) and LAMMPS (MD)
- SLURM scheduler scripts in `scripts/` for cluster workflows
- Validation: `python scripts/validate-structure.py`

## Reproducibility

```bash
python scripts/validate-structure.py
python -m pytest tests/test_cli_basic.py tests/test_qmatsim_cli.py -q
```

Requires SIESTA and LAMMPS on PATH; not run in CI.

```bash
qmatsim relax --material MoS2 --structure 1x10_rectangular
qmatsim minimize --structure 1x10_rectangular --mode compress
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

Committed examples exclude private cluster paths, scheduler credentials, and
machine-local outputs.

## Datasets

- Material definitions and templates in `siesta/` and `lammps/`
- No unpublished cluster datasets in the repo

## Architecture

```text
qmatsim/
├── docs/
├── lammps/            # MD inputs, data files, potentials
├── qmatsim/           # Python package and CLI
├── reports/
├── scripts/
├── siesta/            # DFT templates and materials
├── tests/
├── AGENTS.md
├── CLAUDE.md
├── SSOT.md
└── pyproject.toml
```

See [docs/architecture/topology.md](docs/architecture/topology.md) for on-disk
layout and role boundaries, and [docs/architecture.md](docs/architecture.md)
for solver boundaries and package layout.

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
- [docs/architecture/topology.md](docs/architecture/topology.md)
- [docs/architecture.md](docs/architecture.md)
