---
type: guide
authority: canonical
audience: [ai-agents, contributors]
last-verified: 2026-03-09
---

# CLAUDE.md — qmatsim

## Repository Context

**Name:** QMatSim
**Type:** research-library
**Purpose:** Multiscale simulation framework for strain engineering in 2D
materials. Combines DFT (SIESTA) and MD (LAMMPS) calculations to study flat
bands, lateral heterostructures, and electronic phases in transition metal
dichalcogenides. Implements the computational framework from Alawein et al.,
Physical Review Materials 2025.

## Tech Stack

- **Language:** Python 3.9+
- **Core deps:** NumPy, Matplotlib
- **External tools:** SIESTA 4.1+ (DFT), LAMMPS stable (MD), SLURM (HPC)
- **Build:** setuptools via `pyproject.toml`
- **Testing:** pytest, pytest-cov
- **Linting:** black, flake8, mypy

## Canonical Structure

- `qmatsim/` — rooted Python package and CLI module
- `scripts/` — setup, SLURM, validation, and workflow automation
- `siesta/` — DFT infrastructure and assets
- `lammps/` — MD infrastructure and assets
- `docs/` — theory, API, development, and architecture docs
- `tests/` — CLI smoke tests

Do not introduce a parallel `src/` tree without an explicit migration decision.
This repo’s documented structure exception is intentional.

## Common Tasks

### Validation

```bash
python scripts/validate-structure.py
python -m qmatsim --help
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
```

### Installation

```bash
pip install -e ".[dev]"
```

### Running Simulations

```bash
qmatsim relax --material MoS2 --structure 1x10_rectangular
qmatsim minimize --structure 1x10_rectangular --mode compress
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

## Architecture

QMatSim is a Python CLI orchestrator layered on top of two domain surfaces:

- `siesta/` for DFT inputs, templates, and materials
- `lammps/` for MD inputs, data files, and potentials

The Python package coordinates those surfaces and delegates the heavy workflow
execution to shell automation under `scripts/`.

## Governance

See [AGENTS.md](AGENTS.md) for rules and [SSOT.md](SSOT.md) for the current
state.
