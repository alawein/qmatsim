---
type: canonical
source: _devkit/templates
sync: propagated
sla: none
---

# Contributing to qmatsim

Multiscale simulation framework for strain engineering in 2D materials.

This project follows the [alawein org contributing standards](https://github.com/alawein/alawein/blob/main/CONTRIBUTING.md).

## Getting Started

```bash
git clone https://github.com/alawein/qmatsim.git
cd qmatsim
pip install -e ".[dev]"
```

## Development Workflow

1. Branch off `main` using prefix: `feat/`, `fix/`, `docs/`, `chore/`, `test/`
2. Make your changes — keep PRs focused on a single concern
3. Run `python -m pytest -s tests/` to validate your changes before committing
4. Commit using [Conventional Commits](https://www.conventionalcommits.org/) — `type(scope): subject`
5. Open a Pull Request to `main`

## Code Standards

- Python 3.9+, black for formatting, flake8 + mypy for linting
- Root package layout (`qmatsim/`), not `src/`
- Keep SIESTA assets under `siesta/` and LAMMPS assets under `lammps/`
- Never hardcode HPC paths -- use templates and config files

## Pull Request Checklist

- [ ] CI passes (no failing checks)
- [ ] Tests added or updated for new functionality
- [ ] `python scripts/validate-structure.py && python -m pytest -s tests/` passes
- [ ] `CHANGELOG.md` updated under `[Unreleased]`
- [ ] No breaking changes without a version bump plan

## Reporting Issues

Open an issue on the [GitHub repository](https://github.com/alawein/qmatsim/issues) with steps to reproduce and relevant context.

## License

By contributing, you agree that your contributions will be licensed under [MIT](LICENSE).
