# Claude AI Assistant Guide

## Repository Context

**Name:** QMatSim  
**Type:** research-library  
**Purpose:** Multiscale simulation framework for strain engineering in 2D materials. Combines DFT (SIESTA) and MD (LAMMPS) calculations to study flat bands, lateral heterostructures, and electronic phases in transition metal dichalcogenides. Implements the computational framework from Alawein et al., Physical Review Materials 2025.

## Tech Stack

- **Language:** Python 3.9+
- **Core deps:** NumPy, Matplotlib
- **External tools:** SIESTA 4.1+ (DFT), LAMMPS stable (MD), SLURM (HPC)
- **Build:** setuptools (`pyproject.toml` + legacy `setup.py`)
- **Testing:** pytest, pytest-cov
- **Linting:** black, flake8, mypy

## Key Files

- `README.md` — Main documentation
- `pyproject.toml` — Package configuration
- `qmatsim/` — Core Python CLI framework
- `scripts/` — Bash automation tools for SLURM and workflow management
- `siesta/` — DFT calculation infrastructure
- `lammps/` — MD simulation infrastructure
- `tests/` — Test suite
- `docs/` — Documentation

## Development Guidelines

1. Follow existing code style — use `black` for formatting, `flake8` for linting, `mypy` for typing
2. Add tests for new features (`pytest`)
3. Update documentation for API changes
4. Use conventional commits
5. Support both SIESTA and LAMMPS backends

## Common Tasks

### Running Tests
```bash
pytest
pytest --cov=qmatsim
```

### Building
```bash
pip install -e ".[dev]"
```

### Running Simulations
```bash
qmatsim relax --material MoS2 --structure 1x10_rectangular
qmatsim minimize --structure ripple10 --mode compress
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

## Architecture

Multiscale simulation pipeline: Python CLI orchestrates DFT (SIESTA) and MD (LAMMPS) calculations with SLURM job management. The framework automates flat band discovery, strain-electronic correlation studies, and lateral heterostructure analysis across MoS2, MoSe2, WS2, and WSe2 systems.
