# Contributing to QMatSim

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md)
and the local repository rules in [AGENTS.md](AGENTS.md).

## Quick Start

```bash
git clone https://github.com/alawein/qmatsim.git
cd qmatsim
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m qmatsim --help
```

## Workflow

1. Branch from `main`.
2. Make the smallest coherent change.
3. Update docs when workflow, structure, or CLI behavior changes.
4. Run the repo validation commands before proposing the change.

## Validation

```bash
python scripts/validate-structure.py
python -m qmatsim --help
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
```

## Structure Rules

- Keep the canonical Python import surface at `qmatsim/`.
- Keep DFT assets under `siesta/`.
- Keep MD assets under `lammps/`.
- Keep workflow automation under `scripts/`.
- Do not introduce `src/` without an explicit migration decision and matching
  documentation update.

## Documentation

See:

- [README.md](README.md)
- [SSOT.md](SSOT.md)
- [docs/README.md](docs/README.md)
- [docs/architecture/STRUCTURE_DECISION.md](docs/architecture/STRUCTURE_DECISION.md)
