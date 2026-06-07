---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [agents, contributors, maintainers]
last_updated: 2026-04-15
last-verified: 2026-04-15
---

# AGENTS: QMatSim

## Workspace identity

QMatSim is a research-library repo for SIESTA and LAMMPS workflows in strained
2D quantum materials.

## Directory structure

- `qmatsim/`: primary Python source
- `siesta/`: DFT assets
- `lammps/`: MD assets
- `scripts/`: validation and scheduler automation
- `tests/`: required verification

## Governance rules

1. Keep the Python import surface rooted at `qmatsim/`.
2. Do not add a parallel `src/` tree.
3. Keep `siesta/` and `lammps/` organized as explicit backend surfaces.
4. Avoid hardcoded HPC paths in reusable scripts.
5. Comments should explain backend, strain, and scheduler assumptions.

## Code conventions

- Type hints and accurate docstrings on public Python surfaces
- Conventional commits only
- Update tests when CLI behavior changes

## Build and test commands

```bash
pip install -e ".[dev]"
python scripts/validate-structure.py
python -m qmatsim --help
python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py
black qmatsim/
flake8 qmatsim/
mypy qmatsim/
```
