# QMatSim

Status:      frozen
Category:    research
Owner:       alawein
Visibility:  public
Purpose:     Quantum material simulation research workspace.
Next action: continue

## Abstract

QMatSim is a strain-engineering workflow for 2D quantum materials built around
two explicit computational surfaces: SIESTA for DFT and LAMMPS for molecular
dynamics. The Python package is the orchestration layer; it does not replace the
underlying solvers. Public polish should emphasize reproducibility, solver
requirements, data provenance, and example outputs rather than abstracting away
the DFT/MD tooling.

## Status

- Lifecycle: `frozen`
- Category: `research`
- Owner: `alawein`
- Visibility: `public`
- Next action: `continue`

## Runtime requirements

- Python 3.x with `pip install -e ".[dev]"`
- External scientific dependencies: SIESTA (DFT) and LAMMPS (MD)
- SLURM scheduler scripts in `scripts/` for cluster workflows
- Validation: `python scripts/validate-structure.py`

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

## Reproducibility

```bash
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m qmatsim --help
qmatsim relax --material MoS2 --structure 1x10_rectangular
qmatsim minimize --structure 1x10_rectangular --mode compress
qmatsim analyze --material MoS2 --structure 1x10_rectangular
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
```

Keep private cluster paths, scheduler credentials, and machine-local outputs out
of committed examples. See [docs/architecture.md](docs/architecture.md) for
solver boundaries and package layout.

## Datasets

- Material definitions and templates in `siesta/` and `lammps/`
- Input provenance must be identified in public examples (generated, archived, or illustrative)
- No unpublished cluster datasets in the repo

## Docs map

- [docs/README.md](docs/README.md)
- [SSOT.md](SSOT.md)
- [LESSONS.md](LESSONS.md)
- [docs/architecture.md](docs/architecture.md)
