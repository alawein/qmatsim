# QMatSim

QMatSim is a strain-engineering workflow for 2D quantum materials built around
two explicit computational surfaces: SIESTA for DFT and LAMMPS for molecular
dynamics. The Python package is the orchestration layer. It is not pretending
to replace the underlying solvers.

The repository is organized to keep templates, materials, scheduler scripts,
and analysis commands close to the scientific problem instead of hiding them
behind a generic application shell.

## Core surfaces

- `qmatsim/`: canonical Python package and CLI entrypoint
- `siesta/`: DFT templates, materials, and helper assets
- `lammps/`: MD inputs, data files, and potentials
- `scripts/`: setup, validation, and SLURM automation
- `tests/`: CLI smoke tests
- `docs/`: theory, API, and development notes

## Quick start

```bash
git clone https://github.com/alawein/qmatsim.git
cd qmatsim
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m qmatsim --help
```

## CLI

```bash
qmatsim relax --material MoS2 --structure 1x10_rectangular
qmatsim minimize --structure 1x10_rectangular --mode compress
qmatsim analyze --material MoS2 --structure 1x10_rectangular
```

## Development

```bash
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
black qmatsim/
flake8 qmatsim/
mypy qmatsim/
python scripts/validate-structure.py
```

## Documentation

Start with [docs/README.md](docs/README.md) for theory notes, development
guides, and the structure decision behind the rooted-package layout.
