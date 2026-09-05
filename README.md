# QMatSim

Status:      frozen
Category:    lab
Owner:       alawein
Visibility:  public
Purpose:     Thin CLI package for separately managed quantum-material workspaces.
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
- Scope: the published Python CLI under `qmatsim/`; repository workspace assets
  under `siesta/`, `lammps/`, and `scripts/` are not wheel contents
- Release follow-up: establish a versioned, license-reviewed scientific workspace bundle
  before making a paper-scale reproducibility claim

## Installation and solver-free verification

Install the thin CLI package:

```bash
pip install QMatSim
qmatsim verify-fixture
```

Expected output:

```json
{"fixture": "qmatsim-solver-free-v1", "schema_version": 1, "solvers_required": false, "status": "ok"}
```

This command is deterministic, bundled in the wheel, and does not require
SIESTA, LAMMPS, SLURM, or a scientific workspace. The Python test suite is also
solver-free:

```bash
python -m pytest
```

## Scientific workspaces and solvers

`relax`, `minimize`, and `analyze` are workspace operations, not standalone
wheel features. They require a separately obtained and documented scientific
workspace plus locally installed SIESTA/LAMMPS. Cluster paths, scheduler
settings, notification addresses, pseudopotential locations, and scratch roots
must be supplied by local configuration; none are portable defaults.

The repository directories `siesta/`, `lammps/`, and `scripts/` remain source
workspace surfaces for maintainers. They are intentionally excluded from the
published wheel. See [the thin-package decision](docs/architecture/THIN_PACKAGE_DECISION.md)
for the boundary and follow-up required before a paper-scale reproduction claim.

## Datasets

No versioned, immutable scientific workspace/data bundle is published by this
package. Do not treat the wheel as a data distribution or a solver installation.

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
