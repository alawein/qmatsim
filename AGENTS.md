---
type: normative
authority: canonical
audience: [agents, contributors, maintainers]
last-verified: 2026-03-09
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
| `qmatsim/` | Canonical Python package and CLI entrypoint |
| `scripts/` | Bash and Python automation for setup, SLURM, and validation |
| `siesta/` | DFT calculation infrastructure and templates |
| `lammps/` | MD simulation infrastructure and assets |
| `tests/` | CLI and package test suite |
| `docs/` | Theory, API, development, and structure documentation |

## Commands

- `pip install -e ".[dev]"` — install with development dependencies
- `python -m qmatsim --help` — CLI usage
- `python scripts/validate-structure.py` — verify canonical repo layout
- `python -m pytest -s tests/test_cli_basic.py tests/test_qmatsim_cli.py` — run
  the current CLI smoke tests

## Agent Rules

- Read this file before making changes
- Keep the canonical Python import surface rooted at `qmatsim/`
- Do not introduce a parallel `src/` tree without an explicit migration decision
- Support both SIESTA and LAMMPS backends
- Keep domain assets under `siesta/` and `lammps/`; do not scatter them across
  new root directories
- Add tests for new features
- Use `black` for formatting, `flake8` for linting, `mypy` for type checking
- SLURM scripts must include proper resource management headers
- Do not hardcode HPC paths; use configuration files and templates
- Update documentation for API or workflow changes
- Use conventional commit messages: `feat(scope):`, `fix(scope):`, etc.

## Naming Conventions

- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- CLI commands: `kebab-case`

See [CLAUDE.md](CLAUDE.md) | [SSOT.md](SSOT.md)
