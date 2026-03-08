---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-01
---

# AGENTS — qmatsim

> Multiscale simulation framework for strain engineering in 2D materials.
> Based on Alawein et al., Physical Review Materials 2025.

## Repository Scope

Python CLI framework combining DFT (SIESTA) and MD (LAMMPS) calculations to
study flat bands, lateral heterostructures, and electronic phases in transition
metal dichalcogenides (MoS2, MoSe2, WS2, WSe2).

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `qmatsim/` | Core Python CLI framework |
| `scripts/` | Bash automation for SLURM and workflow management |
| `siesta/` | DFT calculation infrastructure |
| `lammps/` | MD simulation infrastructure |
| `tests/` | Test suite |
| `docs/` | Documentation |

## Commands

- `pip install -e ".[dev]"` -- install with dev dependencies
- `qmatsim --help` -- CLI usage
- `pytest` -- run tests
- `pytest --cov=qmatsim` -- run tests with coverage

## Agent Rules

- Read this file before making changes
- Support both SIESTA and LAMMPS backends
- Add tests for new features (`pytest`)
- Use `black` for formatting, `flake8` for linting, `mypy` for type checking
- SLURM scripts must include proper resource management headers
- Do not hardcode HPC paths -- use configuration files
- Update documentation for API changes
- Use conventional commit messages: `feat(scope):`, `fix(scope):`, etc.

## Naming Conventions

- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- CLI commands: `kebab-case`

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)